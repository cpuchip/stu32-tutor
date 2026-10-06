/* keyrun: presses a lesson's printed keys on the device's own key layer and compares the result
 * with the lesson's vector.
 *
 *   keyrun KEYS VECTOR_TRACE
 *
 * KEYS is one line of key names as a lesson prints them (lesson-format.md). Each name is resolved
 * to a key number from the firmware's keymap, never from a table of ours, and the keys go through
 * app_key exactly as the device's do. Every op that reaches the core is logged (trace.c).
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
#include "state.h"

extern FILE *trace_out;
extern int trace_token;
abn_status __real_ab_do_arg(ab_calc *c, ab_op op, int arg);

#define MAX_OPS 4096
#define MAX_TOK 512
#define IMG_CAP (256 * 1024)

typedef struct { int op, arg, tok; } op_rec;

static uint32_t now;
static const pwr_inputs PWR = {true, true, 80, false};

static int shift_key(int s)
{
    for (int k = 0; k < KB_KEYS; k++) {
        const km_action *a = km_lookup(k, KM_FACE);
        if (a->kind == KM_SHIFT && a->arg == s) return k;
    }
    return -1;
}

static int soft_key(int i)
{
    for (int k = 0; k < KB_KEYS; k++) {
        const km_action *a = km_lookup(k, KM_FACE);
        if (a->kind == KM_SOFT && a->arg == i) return k;
    }
    return -1;
}

static void settle(app_state *a)
{
    for (int i = 0; i < 1000000 && (a->running || a->pause); i++) app_tick(a, &PWR, now += 1);
    app_tick(a, &PWR, now += 1);
}

static void press(app_state *a, int key)
{
    app_key(a, key, now += 100);
    settle(a);
}

/* The key a printed name means in the state the device is in now, or -1 (none) or -2 (more than
   one). The order is the device's: a waiting prompt reads letters first, an open menu's labels are
   the soft keys, then the legends in the shift in effect. */
static int resolve(const app_state *a, const char *name, const char **why)
{
    if (a->prompt_op >= 0 && (a->prompt_kind == KM_ARG_VAR || a->prompt_kind == KM_ARG_LABEL ||
                              a->prompt_kind == KM_ARG_TARGET) && name[0] >= 'A' && name[0] <= 'Z' &&
        name[1] == '\0') {
        for (int k = 0; k < KB_KEYS; k++) {
            const km_letter *l = km_letter_of(k);
            if (l->kind == KL_LETTER && l->value == name[0] - 'A') return k;
        }
        *why = "no key carries that letter";
        return -1;
    }
    int soft = -1;
    if (a->menu >= 0) {
        const km_menu *m = km_menu_at(a->menu);
        for (int i = 0; m && i < KM_SOFT_KEYS; i++)
            if (m->item[i].kind != KM_NONE && strcmp(m->item[i].legend, name) == 0) soft = soft_key(i);
    }
    int found = -1, count = 0;
    for (int k = 0; k < KB_KEYS; k++) {
        const km_action *x = km_lookup(k, a->shift);
        if (x->kind != KM_NONE && x->legend && strcmp(x->legend, name) == 0) {
            found = k;
            count++;
        }
    }
    /* A reader cannot tell a soft key's label from a printed legend of the same name. */
    if (soft >= 0 && count) { *why = "an open menu's label and a printed legend share that name"; return -2; }
    if (soft >= 0) return soft;
    if (count == 1) return found;
    if (count > 1) { *why = "more than one key has that legend in this shift"; return -2; }
    *why = a->shift ? "no key has that legend in the shift pressed before it"
                    : "no key has that legend on its face (a shifted legend needs GOLD or BLUE first)";
    return -1;
}

static int is_number(const char *s)
{
    int digits = 0;
    for (; *s; s++) {
        if (*s >= '0' && *s <= '9') digits++;
        else if (*s != '.') return 0;
    }
    return digits > 0;
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

int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "usage: keyrun KEYS VECTOR_TRACE\n");
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
    const dev_settings set0 = a.set;
    char apath[] = "/tmp/keyrun-app-XXXXXX";
    int fd = mkstemp(apath);
    if (fd < 0) { perror("mkstemp"); return 2; }
    trace_out = fdopen(fd, "w");
    for (int i = 0; i < ntok; i++) {
        trace_token = i;
        const char *why = "";
        if (strcmp(tok[i], "GOLD") == 0 || strcmp(tok[i], "BLUE") == 0) {
            press(&a, shift_key(tok[i][0] == 'G' ? 1 : 2));
            continue;
        }
        int k = resolve(&a, tok[i], &why);
        if (k < 0 && is_number(tok[i]) && strlen(tok[i]) > 1) {
            for (const char *p = tok[i]; *p; p++) {         /* a number: its digit keys */
                char one[2] = {*p, '\0'};
                int d = resolve(&a, one, &why);
                if (d < 0) { printf("KEY %d '%s': digit '%s': %s\n", i + 1, tok[i], one, why); return 2; }
                press(&a, d);
            }
            continue;
        }
        if (k < 0) { printf("KEY %d '%s': %s\n", i + 1, tok[i], why); return 2; }
        press(&a, k);
    }
    trace_token = -1;
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
    if (left) { printf("LEFT: the keys end with %s\n", left); return 1; }

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
    static const char *const KIND[] = {"value", "entry", "eqn", "program", "message", "prompt", "view"};
    printf("OK %d ops\nX\t%s\t%s\n", na, page.x.kind >= 0 && page.x.kind <= SCREEN_VIEW ? KIND[page.x.kind] : "?",
           page.x.text);
    return 0;
}
