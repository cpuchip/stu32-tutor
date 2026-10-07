/* resolve: a lesson's printed key names to the device's keys (resolve.h). Every name is resolved
 * from the firmware's keymap and the screen's own labels, never from a table of ours. */
#include <stdio.h>
#include <string.h>

#include "keymap.h"
#include "keys.h"
#include "resolve.h"

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

/* The order is the device's: a waiting prompt reads letters first, an open menu's labels are the
   soft keys, then the legends in the shift in effect. */
int kr_resolve(const app_state *a, const char *name, const char **why)
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
    /* The soft keys are whatever the screen labels them now (app_ui): an open menu's items, the
       equation bar's, CLR ALL?'s Y and N, CONST's page. A label is matched with its spaces ignored,
       since printed keys are split on spaces ("()" is the bar's "( )"). */
    int soft = -1;
    {
        static screen_ui ui;
        app_ui(a, &ui);
        for (int i = 0; i < SCREEN_SOFT; i++) {
            const char *l = ui.soft[i], *n = name;
            if (!l || !*l) continue;
            while (*l && *n) {
                if (*l == ' ') { l++; continue; }
                if (*l != *n) break;
                l++; n++;
            }
            while (*l == ' ') l++;
            if (!*l && !*n) soft = soft_key(i);
        }
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

int kr_press_names(app_state *a, char **tok, int ntok, kr_press_fn press, void *ctx,
                   char *err, size_t errcap)
{
    for (int i = 0; i < ntok; i++) {
        const char *why = "";
        if (strcmp(tok[i], "GOLD") == 0 || strcmp(tok[i], "BLUE") == 0) {
            press(ctx, a, shift_key(tok[i][0] == 'G' ? 1 : 2), i);
            continue;
        }
        int k = kr_resolve(a, tok[i], &why);
        if (k < 0 && is_number(tok[i]) && strlen(tok[i]) > 1) {
            for (const char *p = tok[i]; *p; p++) {         /* a number: its digit keys */
                char one[2] = {*p, '\0'};
                int d = kr_resolve(a, one, &why);
                if (d < 0) { snprintf(err, errcap, "KEY %d '%s': digit '%s': %s", i + 1, tok[i], one, why); return 2; }
                press(ctx, a, d, i);
            }
            continue;
        }
        if (k < 0) { snprintf(err, errcap, "KEY %d '%s': %s", i + 1, tok[i], why); return 2; }
        press(ctx, a, k, i);
    }
    return 0;
}
