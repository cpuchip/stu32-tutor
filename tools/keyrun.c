/* keyrun: presses a lesson's printed keys on the device's own key layer and compares the result
 * with the lesson's vector.
 *
 *   keyrun KEYS VECTOR_TRACE
 *
 * KEYS is one line of key names as a lesson prints them (lesson-format.md). Each name is resolved
 * to a key number from the firmware's keymap, never from a table of ours (resolve.c, shared with
 * the learning page), and the keys go through app_key exactly as the device's do. Every op that reaches the core is logged (trace.c).
 *
 * VECTOR_TRACE is the log the firmware's vector runner wrote for the same example. The two must
 * agree twice: the same ops with the same arguments in the same order, and the same core state
 * image once the vector's ops are replayed on a fresh core. The second catches two paths that
 * issue the same ops from different starting states.
 *
 * Output: "OK n ops", or what differs, naming the printed key that issued it. Exit 0 when they
 * agree, 1 when they differ, 2 when a key name cannot be resolved or a file is malformed. */
#define _POSIX_C_SOURCE 200809L    /* mkstemp, fdopen */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "app.h"
#include "calc.h"
#include "keymap.h"
#include "keys.h"
#include "report.h"
#include "resolve.h"
#include "state.h"

extern FILE *trace_out;
extern int trace_token;
extern long trace_lines;
abn_status __real_ab_do_arg(ab_calc *c, ab_op op, int arg);

#define MAX_OPS 4096
#define MAX_TOK 512
#define IMG_CAP (256 * 1024)

typedef struct { int op, arg, tok; } op_rec;

static uint32_t now;
static app_graph gbuf;                  /* the graph buffer the device keeps in PSRAM */
static const pwr_inputs PWR = {true, true, 80, false};

static void settle(app_state *a)
{
    /* A running program, a pause, or a graph still drawing its columns (unit 033) is not at rest. */
    for (int i = 0; i < 1000000 && (a->running || a->pause || a->graphing); i++) app_tick(a, &PWR, now += 1);
    app_tick(a, &PWR, now += 1);
}

static void press(app_state *a, int key)
{
    /* On the 35s a key with a message showing only clears it (unit 017 rule 4). The app layer does
       that itself, without an op; the runner sends the key's op and the core applies the same rule.
       So a key the app took that way is logged as its op (the state image then checks the two
       agree), as trace.c does for ab_view_key. */
    const km_action *act = km_lookup(key, a->shift);
    bool m35_msg = a->c->msg && a->c->m35 && act->kind == KM_OP &&
                   !(getenv("KEYRUN_FAULT") && strcmp(getenv("KEYRUN_FAULT"), "no-m35-rule") == 0);
    long before = trace_lines;
    app_key(a, key, now += 100);
    if (m35_msg && !a->c->msg && trace_lines == before && trace_out) {
        fprintf(trace_out, "%d %d %d\n", act->op, act->arg, trace_token);
        trace_lines++;
    }
    settle(a);
}

static int read_trace(const char *path, op_rec *ops, int cap, char *untraced, size_t ucap)
{
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); exit(2); }
    char line[256];
    int n = 0;
    untraced[0] = '\0';
    while (fgets(line, sizeof line, f)) {
        if (strncmp(line, "UNTRACED ", 9) == 0) {
            if (!untraced[0]) snprintf(untraced, ucap, "%s", line + 9);
            continue;
        }
        if (n == cap) { fprintf(stderr, "%s: more than %d ops\n", path, cap); exit(2); }
        if (sscanf(line, "%d %d %d", &ops[n].op, &ops[n].arg, &ops[n].tok) != 3) {
            fprintf(stderr, "%s: malformed line: %s", path, line);
            exit(2);
        }
        n++;
    }
    fclose(f);
    return n;
}

/* keyrun's press for resolve.c: the token is set first, so every op the key issues names it. */
static void press_tok(void *ctx, app_state *a, int key, int tok)
{
    (void)ctx;
    trace_token = tok;
    press(a, key);
}

/* Presses printed key names in order; 0, or 2 after printing why a name resolved to no key. */
static int press_names(app_state *a, char **tok, int ntok)
{
    static char err[512];
    int r = kr_press_names(a, tok, ntok, press_tok, NULL, err, sizeof err);
    if (r) printf("%s\n", err);
    trace_token = -1;
    return r;
}

/* keyrun --sequence FILE: a student working through a lesson. Each line is "ID<TAB>keys"; every
   line is pressed on ONE device, in order, with nothing reset between them (the setup first). After
   each line the X line and the status band are printed, so a quoted display can be compared with
   what the student would actually see at that point. */
static int sequence(const char *path)
{
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); return 2; }
    static ab_calc c;
    static app_state a;
    static screen_ui ui;
    static screen_page page;
    ab_init(&c);
    app_init(&a, &c, now);
    app_graph_buffer(&a, &gbuf);         /* a graph is drawn as on the device (unit 033) */
    static char line[8192];
    while (fgets(line, sizeof line, f)) {
        line[strcspn(line, "\r\n")] = '\0';
        char *tab = strchr(line, '\t');
        if (!tab) continue;
        *tab = '\0';
        char *tok[MAX_TOK];
        int ntok = 0;
        for (char *t = strtok(tab + 1, " "); t; t = strtok(NULL, " ")) {
            if (ntok == MAX_TOK) { fprintf(stderr, "more than %d keys\n", MAX_TOK); return 2; }
            tok[ntok++] = t;
        }
        if (press_names(&a, tok, ntok)) { printf("IN %s\n", line); return 2; }
        app_ui(&a, &ui);
        screen_lines(&c, &ui, &page);
        static char rep[4096];
        if (kr_report(&c, &page, line, rep, sizeof rep) < 0) { fprintf(stderr, "report too long\n"); return 2; }
        fputs(rep, stdout);
    }
    fclose(f);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc == 3 && strcmp(argv[1], "--sequence") == 0) return sequence(argv[2]);
    if (argc != 3) {
        fprintf(stderr, "usage: keyrun KEYS VECTOR_TRACE | keyrun --sequence FILE\n");
        return 2;
    }
    static char keys[8192];
    snprintf(keys, sizeof keys, "%s", argv[1]);
    char *tok[MAX_TOK];
    int ntok = 0;
    for (char *t = strtok(keys, " \t"); t; t = strtok(NULL, " \t")) {
        if (ntok == MAX_TOK) { fprintf(stderr, "more than %d keys\n", MAX_TOK); return 2; }
        tok[ntok++] = t;
    }

    /* The key path: a fresh device, as tally's app and the device start. */
    static ab_calc c;
    static app_state a;
    ab_init(&c);
    app_init(&a, &c, now);
    app_graph_buffer(&a, &gbuf);         /* a graph is drawn as on the device (unit 033) */
    const dev_settings set0 = a.set;
    char apath[] = "/tmp/keyrun-app-XXXXXX";
    int fd = mkstemp(apath);
    if (fd < 0) { perror("mkstemp"); return 2; }
    trace_out = fdopen(fd, "w");
    if (press_names(&a, tok, ntok)) return 2;
    fclose(trace_out);
    trace_out = NULL;
    /* KEYRUN_FAULT=state: a planted fault (CLx behind the trace's back) that only the state
       comparison can see, for falsifying it (lesson-format.md, "Controls"). */
    if (getenv("KEYRUN_FAULT") && strcmp(getenv("KEYRUN_FAULT"), "state") == 0)
        __real_ab_do_arg(&c, AB_CLX, 0);

    static uint8_t img_app[IMG_CAP], img_vec[IMG_CAP];
    size_t n_app = ab_state_save(&c, img_app, sizeof img_app);

    /* An example ends with the device at rest: keys that only arm a shift, open a menu or a
       prompt, or change a device setting issue no op and leave no trace in the core's image. */
    const char *left = a.shift ? "a shift armed" : a.menu >= 0 ? "a menu open" : a.prompt_op >= 0 ? "a prompt waiting"
                     : a.confirm_op >= 0 ? "a yes/no prompt waiting" : memcmp(&a.set, &set0, sizeof set0) ? "a device setting changed" : NULL;
    /* KEYRUN_OPEN_PROMPT=1: check.py sets it for a block the next block continues, so a stopping
       point may wait at a prompt ("SOLVE _") that the continuation answers. Nothing else is let off. */
    bool open_ok = getenv("KEYRUN_OPEN_PROMPT") && a.prompt_op >= 0 && !a.shift && a.menu < 0 &&
                   a.confirm_op < 0 && !memcmp(&a.set, &set0, sizeof set0);
    if (left && !open_ok) { printf("LEFT: the keys end with %s\n", left); return 1; }

    /* What the device's screen shows on its X line (screen.c), for the quoted displays. */
    static screen_ui ui;
    static screen_page page;
    app_ui(&a, &ui);
    screen_lines(&c, &ui, &page);

    static op_rec A[MAX_OPS], V[MAX_OPS];
    char ua[256], uv[256];
    int na = read_trace(apath, A, MAX_OPS, ua, sizeof ua);
    remove(apath);
    int nv = read_trace(argv[2], V, MAX_OPS, uv, sizeof uv);
    if (ua[0] || uv[0]) {
        printf("UNTRACED: the %s path called %s", ua[0] ? "key" : "vector", ua[0] ? ua : uv);
        return 1;
    }
    for (int i = 0; i < na || i < nv; i++) {
        if (i >= na) { printf("DIFF at op %d: the vector goes on (op %d arg %d); the keys stop\n", i + 1, V[i].op, V[i].arg); return 1; }
        if (i >= nv) { printf("DIFF at op %d: key %d '%s' issues op %d arg %d; the vector has stopped\n", i + 1, A[i].tok + 1, tok[A[i].tok], A[i].op, A[i].arg); return 1; }
        if (A[i].op != V[i].op || A[i].arg != V[i].arg) {
            printf("DIFF at op %d: key %d '%s' issues op %d arg %d; the vector has op %d arg %d\n", i + 1,
                   A[i].tok + 1, A[i].tok >= 0 ? tok[A[i].tok] : "?", A[i].op, A[i].arg, V[i].op, V[i].arg);
            return 1;
        }
    }

    /* The vector's ops replayed on a fresh core, as the runner runs them (no slices). */
    static ab_calc r;
    ab_init(&r);
    for (int i = 0; i < nv; i++) {
        ab_do_arg(&r, (ab_op)V[i].op, V[i].arg);
        while (r.stop == AB_STOP_SLICE) ab_continue(&r);
    }
    size_t n_vec = ab_state_save(&r, img_vec, sizeof img_vec);
    if (n_app != n_vec || memcmp(img_app, img_vec, n_app) != 0) {
        size_t at = 0;
        while (at < n_app && at < n_vec && img_app[at] == img_vec[at]) at++;
        printf("STATE: the same %d ops leave different core images (%zu and %zu bytes, first difference at byte %zu)\n",
               na, n_app, n_vec, at);
        return 1;
    }
    printf("OK %d ops\nX\t%s\t%s\nYL\t%s\t%s\nSTATUS\t%s\n", na, kr_kind(page.x.kind), page.x.text,
           kr_kind(page.y.kind), page.y.text, page.status.text);
    static char gline[512];
    if (kr_graph_line(&page, "-", gline, sizeof gline) > 0) fputs(gline, stdout);
    return 0;
}
