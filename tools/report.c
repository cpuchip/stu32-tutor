/* report: what a student sees after a step (report.h). */
#include <stdio.h>
#include <string.h>

#include "report.h"

static const char *const KIND[] = {"value", "entry", "eqn", "program", "message", "prompt", "view"};

const char *kr_kind(int kind)
{
    return kind >= 0 && kind <= SCREEN_VIEW ? KIND[kind] : "?";
}

int kr_graph_line(const screen_page *page, const char *id, char *out, size_t cap)
{
    if (cap) out[0] = '\0';
    if (!page->graph_on) return 0;
    const screen_graph_text *g = &page->graph;
    int n = snprintf(out, cap, "GRAPH\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", id, g->readout, g->xmin, g->xmax, g->ymin,
                     g->ymax, g->note);
    return n < 0 || (size_t)n >= cap ? -1 : n;
}

/* A stack level as exact text: a complex number as its two parts joined by "i"; "" for a vector. A
   coincidence in X alone (a stray digit that still lands on the right X) must not pass, so all four
   levels are reported. */
static void level_text(const ab_val *v, char *out, size_t cap)
{
    out[0] = '\0';
    if (v->kind == AB_REAL) abn_to_text(&v->re, out, (int)cap);
    else if (v->kind == AB_COMPLEX) {
        char re[96], im[96];
        abn_to_text(&v->re, re, sizeof re);
        abn_to_text(&v->im, im, sizeof im);
        snprintf(out, cap, "%si%s", re, im);
    }
}

int kr_report(const ab_calc *c, const screen_page *page, const char *id, char *out, size_t cap)
{
    char val[4][200], ans[200], shown[200];
    const ab_val *lv[4] = {&c->x, &c->y, &c->z, &c->t};
    for (int i = 0; i < 4; i++) level_text(lv[i], val[i], sizeof val[i]);
    level_text(&c->ans, ans, sizeof ans);
    level_text(c->hist_at >= 0 ? &c->hist_val[c->hist_at] : &c->ans, shown, sizeof shown);
    int n = snprintf(out, cap, "X\t%s\t%s\t%s\nYL\t%s\t%s\t%s\nSTATUS\t%s\t%s\nVAL\t%s\t%s\t%s\t%s\t%s\n"
                     "ANS\t%s\t%s\t%s\n",
                     id, kr_kind(page->x.kind), page->x.text, id, kr_kind(page->y.kind), page->y.text,
                     id, page->status.text, id, val[0], val[1], val[2], val[3], id, ans, shown);
    if (n < 0 || (size_t)n >= cap) return -1;
    int g = kr_graph_line(page, id, out + n, cap - (size_t)n);
    return g < 0 ? -1 : n + g;
}
