/* stu32-calc: the STU-32's core in a container, one call at a time (proposal stu32-calc, ruled by
 * abacus #5737). The image's entry point.
 *
 *   stu32-calc keys [--mode STU|33s|35s] [--entry alg|rpn] [--angle DEG|RAD|GRAD] [--fix N]
 *       stdin: one step per line, printed key names (docs/lesson-format.md), optionally "ID<TAB>keys".
 *       With --mode, the lessons' setup is pressed first, as step "setup". Every step is pressed on
 *       ONE device, in order, by keyrun --sequence (the student run make check passes).
 *   stu32-calc vectors [--display]
 *       stdin: a vectors file (ID | note | MODE33 FIXn keys | expectations), or with --display a
 *       display-vectors file. The firmware's own runner judges it.
 *   stu32-calc casim OP ARG...
 *       Casimir's CLI at the firmware's CASIM_PIN, by op name.
 *   stu32-calc pins
 *
 * The answer is one JSON object on stdout, always carrying the pins. Exit 0: done (a FAIL is
 * done). Exit 1: a bad request. Exit 124: a limit was hit.
 *
 * The limits (abacus #5737): the runner is a child in its own process group, with CPU 10 s, address
 * space 192 MB, no file writes and no core files; a 15 s wall clock kills the whole group; its
 * output is capped at 64 KiB and stdin at 64 KiB. Each limit is a status (TIMEOUT, OUTPUT_LIMIT,
 * INPUT_LIMIT, KILLED), never silence. The container adds its own limits, and the caller's wrapper
 * (calc/run.sh) an outer deadline. STU32_CALC_TEST_NO_INNER=1 turns off the CPU limit and the wall
 * clock, so a test can show the outer layers stop a runaway on their own; =cpu turns off the CPU limit
 * alone, so a test can show the wall clock (the runners never block, so the CPU limit comes first). */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define IN_CAP (64 * 1024)
#define OUT_CAP (64 * 1024)
#define ERR_CAP (8 * 1024)
#define CPU_S 10
#define WALL_MS 15000L
#define AS_BYTES (192UL * 1024 * 1024)
#define MAX_STEPS 1000
#define MAX_ARG 1024

static const char *root(void)
{
    const char *r = getenv("STU32_CALC_ROOT");     /* the image sets nothing: /opt/stu32 */
    return r && *r ? r : "/opt/stu32";
}

static int no_inner(void)
{
    const char *t = getenv("STU32_CALC_TEST_NO_INNER");
    return t && strcmp(t, "1") == 0;
}

static int no_cpu_limit(void)
{
    const char *t = getenv("STU32_CALC_TEST_NO_INNER");
    return no_inner() || (t && strcmp(t, "cpu") == 0);
}

static long now_ms(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000L + ts.tv_nsec / 1000000L;
}

/* ---- JSON out ---- */

/* A string as JSON: quotes, backslashes and control bytes escaped; a byte that is not part of
   valid UTF-8 becomes U+FFFD, so the output always parses. */
static void jstr_n(const char *s, size_t n)
{
    const unsigned char *p = (const unsigned char *)s;
    putchar('"');
    for (size_t i = 0; i < n;) {
        unsigned char c = p[i];
        if (c == '"' || c == '\\') { putchar('\\'); putchar(c); i++; continue; }
        if (c < 0x20) { printf("\\u%04x", c); i++; continue; }
        if (c < 0x80) { putchar(c); i++; continue; }
        size_t len = c >= 0xF0 && c <= 0xF4 ? 4 : c >= 0xE0 ? 3 : c >= 0xC2 && c < 0xE0 ? 2 : 0;
        int ok = len && i + len <= n;
        for (size_t k = 1; ok && k < len; k++) ok = (p[i + k] & 0xC0) == 0x80;
        if (ok) { fwrite(p + i, 1, len, stdout); i += len; }
        else { fputs("\\ufffd", stdout); i++; }
    }
    putchar('"');
}

static void jstr(const char *s) { jstr_n(s, strlen(s)); }

/* The pins file: "name value" lines, written at build time. */
static void jpins(void)
{
    char path[512];
    snprintf(path, sizeof path, "%s/pins", root());
    FILE *f = fopen(path, "r");
    fputs("\"pins\":{", stdout);
    if (f) {
        char line[512];
        int first = 1;
        while (fgets(line, sizeof line, f)) {
            line[strcspn(line, "\r\n")] = '\0';
            char *sp = strchr(line, ' ');
            if (!sp || sp == line) continue;
            *sp = '\0';
            if (!first) putchar(',');
            first = 0;
            jstr(line);
            putchar(':');
            jstr(sp + 1);
        }
        fclose(f);
    }
    putchar('}');
}

static int fail_request(const char *cmd, const char *detail)
{
    fputs("{\"status\":\"BAD_REQUEST\",\"command\":", stdout);
    jstr(cmd);
    fputs(",\"detail\":", stdout);
    jstr(detail);
    putchar(',');
    jpins();
    puts("}");
    return 1;
}

/* ---- the child, under the limits ---- */

typedef struct {
    char *out, *err;
    size_t out_len, err_len;
    int out_limit, timed_out, signaled, sig, exit_code, spawn_failed;
    long wall_ms;
} run_result;

static void limit(int res, rlim_t soft, rlim_t hard)
{
    struct rlimit r = {soft, hard};
    setrlimit(res, &r);
}

static void append(char **buf, size_t *len, size_t cap, const char *src, size_t n, int *over)
{
    if (*len + n > cap) { n = cap - *len; *over = 1; }
    memcpy(*buf + *len, src, n);
    *len += n;
}

static void run(char *const argv[], const char *in, size_t in_len, run_result *r)
{
    memset(r, 0, sizeof *r);
    r->out = calloc(1, OUT_CAP + 1);
    r->err = calloc(1, ERR_CAP + 1);
    int pin[2], pout[2], perr[2];
    if (!r->out || !r->err || pipe(pin) || pipe(pout) || pipe(perr)) { r->spawn_failed = 1; return; }
    long t0 = now_ms();
    pid_t pid = fork();
    if (pid < 0) { r->spawn_failed = 1; return; }
    if (pid == 0) {
        setpgid(0, 0);
        /* The hard limit a second above the soft one: at the soft limit the kernel sends SIGXCPU, which
           names the cause; with the two equal it sends SIGKILL at once (measured: KILLED, signal 9). */
        if (!no_cpu_limit()) limit(RLIMIT_CPU, CPU_S, CPU_S + 1);
        limit(RLIMIT_AS, AS_BYTES, AS_BYTES);
        limit(RLIMIT_FSIZE, 0, 0);
        limit(RLIMIT_CORE, 0, 0);
        dup2(pin[0], 0);
        dup2(pout[1], 1);
        dup2(perr[1], 2);
        for (int fd = 3; fd < 64; fd++) close(fd);
        execv(argv[0], argv);
        _exit(127);
    }
    setpgid(pid, pid);                  /* also here: whichever runs first, the group exists */
    close(pin[0]);
    close(pout[1]);
    close(perr[1]);
    fcntl(pin[1], F_SETFL, O_NONBLOCK);
    int fin = pin[1], fout = pout[0], ferr = perr[0];
    size_t sent = 0;
    if (in_len == 0) { close(fin); fin = -1; }
    int over_err = 0, done = 0, status = 0;
    long deadline = t0 + WALL_MS;
    while (!done) {
        struct pollfd fds[3];
        int n = 0, iin = -1, iout = -1, ierr = -1;
        if (fin >= 0) { iin = n; fds[n++] = (struct pollfd){fin, POLLOUT, 0}; }
        if (fout >= 0) { iout = n; fds[n++] = (struct pollfd){fout, POLLIN, 0}; }
        if (ferr >= 0) { ierr = n; fds[n++] = (struct pollfd){ferr, POLLIN, 0}; }
        long left = deadline - now_ms();
        if (!no_inner() && left <= 0) {
            r->timed_out = 1;
            kill(-pid, SIGKILL);
            kill(pid, SIGKILL);
            break;
        }
        int wait = no_inner() ? 50 : (int)(left < 50 ? left : 50);
        if (n) poll(fds, (nfds_t)n, wait);
        else { struct timespec ts = {0, 10 * 1000000L}; nanosleep(&ts, NULL); }
        char buf[4096];
        if (iin >= 0 && (fds[iin].revents & (POLLOUT | POLLERR | POLLHUP))) {
            ssize_t w = write(fin, in + sent, in_len - sent);
            if (w > 0) sent += (size_t)w;
            if ((w < 0 && errno != EAGAIN) || sent == in_len) { close(fin); fin = -1; }
        }
        if (iout >= 0 && (fds[iout].revents & (POLLIN | POLLHUP | POLLERR))) {
            ssize_t k = read(fout, buf, sizeof buf);
            if (k <= 0) { close(fout); fout = -1; }
            else {
                append(&r->out, &r->out_len, OUT_CAP, buf, (size_t)k, &r->out_limit);
                if (r->out_limit) { kill(-pid, SIGKILL); kill(pid, SIGKILL); break; }
            }
        }
        if (ierr >= 0 && (fds[ierr].revents & (POLLIN | POLLHUP | POLLERR))) {
            ssize_t k = read(ferr, buf, sizeof buf);
            if (k <= 0) { close(ferr); ferr = -1; }
            else append(&r->err, &r->err_len, ERR_CAP, buf, (size_t)k, &over_err);
        }
        if (fout < 0 && ferr < 0 && waitpid(pid, &status, WNOHANG) == pid) done = 1;
    }
    if (fin >= 0) close(fin);
    if (fout >= 0) close(fout);
    if (ferr >= 0) close(ferr);
    if (!done) waitpid(pid, &status, 0);
    r->wall_ms = now_ms() - t0;
    if (WIFSIGNALED(status)) { r->signaled = 1; r->sig = WTERMSIG(status); }
    else if (WIFEXITED(status)) r->exit_code = WEXITSTATUS(status);
}

/* The status a limit gives, or NULL when none was hit. */
static const char *limit_status(const run_result *r)
{
    if (r->timed_out) return "TIMEOUT";
    if (r->out_limit) return "OUTPUT_LIMIT";
    if (r->signaled && r->sig == SIGXCPU) return "TIMEOUT";      /* the CPU limit */
    if (r->signaled) return "KILLED";
    return NULL;
}

static void jrun_tail(const run_result *r, const char *lim)
{
    printf(",\"wall_ms\":%ld", r->wall_ms);
    if (lim) {
        fputs(",\"limit\":", stdout);
        if (r->timed_out) printf("\"wall %ld s\"", WALL_MS / 1000);
        else if (r->out_limit) printf("\"output %d KiB\"", OUT_CAP / 1024);
        else if (r->signaled && r->sig == SIGXCPU) printf("\"cpu %d s\"", CPU_S);
        else printf("\"signal %d\"", r->sig);
    }
    if (r->err_len && (lim || r->exit_code)) {
        fputs(",\"stderr\":", stdout);
        jstr_n(r->err, r->err_len);
    }
    putchar(',');
    jpins();
    puts("}");
}

/* ---- stdin, bounded and timed ---- */

static char *read_input(size_t *len, const char **why)
{
    char *buf = malloc(IN_CAP + 1);
    *len = 0;
    *why = NULL;
    if (!buf) { *why = "out of memory"; return NULL; }
    long deadline = now_ms() + WALL_MS;
    for (;;) {
        long left = deadline - now_ms();
        if (left <= 0) { *why = "TIMEOUT"; return buf; }
        struct pollfd p = {0, POLLIN, 0};
        int k = poll(&p, 1, (int)left);
        if (k == 0) continue;
        if (k < 0) { if (errno == EINTR) continue; break; }
        ssize_t n = read(0, buf + *len, IN_CAP + 1 - *len);
        if (n <= 0) break;
        *len += (size_t)n;
        if (*len > IN_CAP) { *why = "INPUT_LIMIT"; return buf; }
    }
    buf[*len] = '\0';
    return buf;
}

static int input_failed(const char *cmd, const char *why)
{
    printf("{\"status\":\"%s\",\"command\":", why);
    jstr(cmd);
    fputs(",\"limit\":", stdout);
    if (strcmp(why, "INPUT_LIMIT") == 0) printf("\"input %d KiB\"", IN_CAP / 1024);
    else printf("\"wall %ld s, reading input\"", WALL_MS / 1000);
    putchar(',');
    jpins();
    puts("}");
    return 124;
}

static int has_control(const char *s, int allow_tab)
{
    for (; *s; s++)
        if ((unsigned char)*s < 0x20 && !(allow_tab && *s == '\t')) return 1;
    return 0;
}

/* ---- keys ---- */

/* MODE's soft key for a mode, as the lessons print it (the setup's {mode}; MODE33 and MODE35 are
   the vectors' tokens, not keys). */
static const char *mode_key(const char *m)
{
    return !strcmp(m, "STU") || !strcmp(m, "33s") || !strcmp(m, "35s") ? m : NULL;
}

/* keyrun's report, a step at a time: X, YL, STATUS, VAL and sometimes GRAPH (tools/report.c). */
static void jsteps(char *out)
{
    fputs("\"steps\":[", stdout);
    int open = 0, first = 1;
    for (char *line = strtok(out, "\n"); line; line = strtok(NULL, "\n")) {
        char *f[8];
        int n = 0;
        for (char *p = line; n < 8;) {
            f[n++] = p;
            char *t = strchr(p, '\t');
            if (!t) break;
            *t = '\0';
            p = t + 1;
        }
        if (!strcmp(f[0], "X") && n == 4) {
            if (open) putchar('}');
            if (!first) putchar(',');
            first = 0;
            open = 1;
            fputs("{\"id\":", stdout); jstr(f[1]);
            fputs(",\"x\":{\"kind\":", stdout); jstr(f[2]);
            fputs(",\"text\":", stdout); jstr(f[3]); putchar('}');
        } else if (!open) {
            continue;
        } else if (!strcmp(f[0], "YL") && n == 4) {
            fputs(",\"y\":{\"kind\":", stdout); jstr(f[2]);
            fputs(",\"text\":", stdout); jstr(f[3]); putchar('}');
        } else if (!strcmp(f[0], "STATUS") && n == 3) {
            fputs(",\"status_band\":", stdout); jstr(f[2]);
        } else if (!strcmp(f[0], "VAL") && n == 6) {
            fputs(",\"stack\":{\"X\":", stdout); jstr(f[2]);
            fputs(",\"Y\":", stdout); jstr(f[3]);
            fputs(",\"Z\":", stdout); jstr(f[4]);
            fputs(",\"T\":", stdout); jstr(f[5]); putchar('}');
        } else if (!strcmp(f[0], "GRAPH") && n == 8) {
            fputs(",\"graph\":{\"readout\":", stdout); jstr(f[2]);
            fputs(",\"xmin\":", stdout); jstr(f[3]);
            fputs(",\"xmax\":", stdout); jstr(f[4]);
            fputs(",\"ymin\":", stdout); jstr(f[5]);
            fputs(",\"ymax\":", stdout); jstr(f[6]);
            fputs(",\"note\":", stdout); jstr(f[7]); putchar('}');
        }
    }
    if (open) putchar('}');
    putchar(']');
}

static int valid_id(const char *s)
{
    size_t n = strlen(s);
    if (n == 0 || n > 32) return 0;
    for (; *s; s++)
        if (!(( *s >= 'A' && *s <= 'Z') || (*s >= 'a' && *s <= 'z') || (*s >= '0' && *s <= '9') ||
              *s == '_' || *s == '-' || *s == '.'))
            return 0;
    return 1;
}

static int cmd_keys(int argc, char **argv)
{
    const char *mode = NULL, *entry = NULL, *angle = NULL;
    int fix = -1;
    for (int i = 0; i < argc; i++) {
        const char *a = argv[i], *v = i + 1 < argc ? argv[i + 1] : NULL;
        if (!v) return fail_request("keys", "a flag without its value");
        if (!strcmp(a, "--mode")) mode = v;
        else if (!strcmp(a, "--entry")) entry = v;
        else if (!strcmp(a, "--angle")) angle = v;
        else if (!strcmp(a, "--fix")) {
            char *end;
            long n = strtol(v, &end, 10);
            if (*end || n < 0 || n > 11) return fail_request("keys", "--fix takes 0 to 11");
            fix = (int)n;
        } else return fail_request("keys", "unknown flag (--mode, --entry, --angle, --fix)");
        i++;
    }
    if (mode && !mode_key(mode)) return fail_request("keys", "--mode takes STU, 33s or 35s");
    if (entry && strcmp(entry, "alg") && strcmp(entry, "rpn"))
        return fail_request("keys", "--entry takes alg or rpn");
    if (entry && (!mode || strcmp(mode, "STU")))
        return fail_request("keys", "--entry needs --mode STU: algebraic entry is STU mode's alone");
    if (angle && strcmp(angle, "DEG") && strcmp(angle, "RAD") && strcmp(angle, "GRAD"))
        return fail_request("keys", "--angle takes DEG, RAD or GRAD");
    if (!mode && (entry || angle || fix >= 0))
        return fail_request("keys", "--entry, --angle and --fix are part of the setup: give --mode too");

    size_t in_len;
    const char *why;
    char *in = read_input(&in_len, &why);
    if (!in) return fail_request("keys", why);
    if (why) return input_failed("keys", why);

    /* The sequence keyrun reads: the setup, then "ID<TAB>keys" per step. */
    size_t cap = in_len + MAX_STEPS * 48 + 4096;     /* each step gains at most an ID, a tab and a newline */
    char *seq = malloc(cap), *at = seq;
    if (!seq) return fail_request("keys", "out of memory");
    if (mode) {
        at += sprintf(at, "setup\tBLUE MODE %s", mode_key(mode));
        if (entry) at += sprintf(at, " BLUE MODE %s", !strcmp(entry, "alg") ? "ALG" : "RPN");
        at += sprintf(at, " GOLD DISP FIX %d", fix >= 0 ? fix : 4);
        if (angle) at += sprintf(at, " BLUE ∡MODE %s", angle);
        *at++ = '\n';
    }
    int steps = 0;
    for (char *line = strtok(in, "\n"); line; line = strtok(NULL, "\n")) {
        line[strcspn(line, "\r")] = '\0';
        if (!*line) continue;
        if (has_control(line, 1)) return fail_request("keys", "a step holds a control character");
        if (++steps > MAX_STEPS) return fail_request("keys", "more than 1000 steps");
        char *tab = strchr(line, '\t'), id[40];
        const char *keys = line;
        if (tab) {
            *tab = '\0';
            if (!valid_id(line)) return fail_request("keys", "a step ID is 1 to 32 of A-Z a-z 0-9 _ - .");
            snprintf(id, sizeof id, "%s", line);
            keys = tab + 1;
            if (strchr(keys, '\t')) return fail_request("keys", "a step holds a second tab");
        } else snprintf(id, sizeof id, "S%d", steps);
        at += sprintf(at, "%s\t%s\n", id, keys);
    }
    if (!steps && !mode) return fail_request("keys", "no steps on stdin");

    char bin[512];
    snprintf(bin, sizeof bin, "%s/bin/keyrun", root());
    char *args[] = {bin, "--sequence", "/dev/stdin", NULL};
    run_result r;
    run(args, seq, (size_t)(at - seq), &r);
    if (r.spawn_failed) return fail_request("keys", "the runner could not start");
    const char *lim = limit_status(&r);
    const char *status = lim ? lim : r.exit_code == 0 ? "OK" : r.exit_code == 2 ? "BAD_KEY" : "RUNNER_ERROR";
    printf("{\"status\":\"%s\",\"command\":\"keys\"", status);
    r.out[r.out_len] = '\0';
    if (!lim && r.exit_code == 2) {
        /* keyrun prints what it could not press, then "IN <the step>" (tools/keyrun.c), after the
           reports of the steps before it: the detail is those lines alone. */
        fputs(",\"detail\":", stdout);
        size_t n = 0;
        static char det[2048];
        for (const char *p = r.out; *p;) {
            const char *e = strchr(p, '\n');
            size_t len = e ? (size_t)(e - p) : strlen(p);
            int report = !strncmp(p, "X\t", 2) || !strncmp(p, "YL\t", 3) || !strncmp(p, "STATUS\t", 7) ||
                         !strncmp(p, "VAL\t", 4) || !strncmp(p, "GRAPH\t", 6);
            if (!report && n + len + 1 < sizeof det) {
                if (n) det[n++] = '\n';
                memcpy(det + n, p, len);
                n += len;
            }
            p += len + (e ? 1 : 0);
        }
        jstr_n(det, n);
    } else if (!lim && r.exit_code) printf(",\"exit\":%d", r.exit_code);
    putchar(',');
    jsteps(r.out);
    jrun_tail(&r, lim);
    return lim ? 124 : r.exit_code == 2 ? 1 : 0;
}

/* ---- vectors ---- */

static int cmd_vectors(int argc, char **argv)
{
    int display = 0;
    for (int i = 0; i < argc; i++) {
        if (!strcmp(argv[i], "--display")) display = 1;
        else return fail_request("vectors", "unknown flag (--display)");
    }
    size_t in_len;
    const char *why;
    char *in = read_input(&in_len, &why);
    if (!in) return fail_request("vectors", why);
    if (why) return input_failed("vectors", why);
    for (size_t i = 0; i < in_len; i++)
        if ((unsigned char)in[i] < 0x20 && in[i] != '\t' && in[i] != '\n' && in[i] != '\r')
            return fail_request("vectors", "the file holds a control character");
    char bin[512];
    snprintf(bin, sizeof bin, "%s/bin/%s", root(), display ? "fmt_vectors" : "vectors");
    char *args[] = {bin, "/dev/stdin", NULL};
    run_result r;
    run(args, in, in_len, &r);
    if (r.spawn_failed) return fail_request("vectors", "the runner could not start");
    const char *lim = limit_status(&r);
    const char *status = lim ? lim : r.exit_code == 0 ? "PASS" : r.exit_code == 1 ? "FAIL" : "RUNNER_ERROR";
    printf("{\"status\":\"%s\",\"command\":\"vectors\",\"display\":%s", status, display ? "true" : "false");
    if (!lim && r.exit_code > 1) printf(",\"exit\":%d", r.exit_code);
    fputs(",\"report\":[", stdout);
    r.out[r.out_len] = '\0';
    int first = 1;
    for (char *line = strtok(r.out, "\n"); line; line = strtok(NULL, "\n")) {
        if (!first) putchar(',');
        first = 0;
        jstr(line);
    }
    putchar(']');
    jrun_tail(&r, lim);
    return lim ? 124 : 0;
}

/* ---- casim ---- */

static const char *const OPS[] = {"derive", "simplify", "expand", "collect", "subst", "solve", "integrate",
                                  "defint", "factor", "pdiv", "pgcd", "cancel", NULL};

static int cmd_casim(int argc, char **argv)
{
    if (argc < 1) return fail_request("casim", "an op name first");
    int known = 0;
    for (int i = 0; OPS[i]; i++) known |= !strcmp(argv[0], OPS[i]);
    if (!known)
        return fail_request("casim", "op is one of derive simplify expand collect subst solve integrate "
                                     "defint factor pdiv pgcd cancel");
    if (argc > 8) return fail_request("casim", "at most 7 arguments after the op");
    for (int i = 0; i < argc; i++) {
        if (strlen(argv[i]) > MAX_ARG) return fail_request("casim", "an argument longer than 1024 bytes");
        if (has_control(argv[i], 0)) return fail_request("casim", "an argument holds a control character");
    }
    char bin[512];
    snprintf(bin, sizeof bin, "%s/bin/casim", root());
    char *args[10] = {bin};
    for (int i = 0; i < argc; i++) args[i + 1] = argv[i];
    args[argc + 1] = NULL;
    run_result r;
    run(args, "", 0, &r);
    if (r.spawn_failed) return fail_request("casim", "the CLI could not start");
    const char *lim = limit_status(&r);
    while (r.out_len && (r.out[r.out_len - 1] == '\n' || r.out[r.out_len - 1] == '\r')) r.out_len--;
    /* The CLI exits 0 with an answer, 1 with one of Casimir's statuses as its text (UNDEFINED,
       IMPROPER, SYNTAX n, ...), and 2 with its usage on stderr (measured at dbb6d4c). */
    const char *status = lim ? lim : r.exit_code == 0 ? "OK" : r.exit_code == 1 ? "CASIM_STATUS" : "BAD_REQUEST";
    printf("{\"status\":\"%s\",\"command\":\"casim\",\"op\":", status);
    jstr(argv[0]);
    if (!lim) printf(",\"exit\":%d", r.exit_code);
    fputs(",\"text\":", stdout);
    jstr_n(r.out, r.out_len);
    jrun_tail(&r, lim);             /* with the usage as stderr, after exit 2 */
    return lim ? 124 : r.exit_code >= 2 ? 1 : 0;
}

int main(int argc, char **argv)
{
    signal(SIGPIPE, SIG_IGN);
    setvbuf(stdout, NULL, _IOFBF, 1 << 16);
    if (argc < 2) return fail_request("", "usage: stu32-calc keys|vectors|casim|pins ...");
    const char *cmd = argv[1];
    int rc;
    if (!strcmp(cmd, "keys")) rc = cmd_keys(argc - 2, argv + 2);
    else if (!strcmp(cmd, "vectors")) rc = cmd_vectors(argc - 2, argv + 2);
    else if (!strcmp(cmd, "casim")) rc = cmd_casim(argc - 2, argv + 2);
    else if (!strcmp(cmd, "pins")) {
        fputs("{\"status\":\"OK\",\"command\":\"pins\",", stdout);
        jpins();
        puts("}");
        rc = 0;
    } else rc = fail_request(cmd, "usage: stu32-calc keys|vectors|casim|pins ...");
    fflush(stdout);
    return rc;
}
