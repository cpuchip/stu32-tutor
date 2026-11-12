/* report: what a student sees after a step, as keyrun --sequence prints it and the learning page's
 * gate compares it (primer #4555): one source, so the page and the checker cannot drift. It depends
 * only on the core and the screen's lines: no trace, no main. */
#ifndef STU32_REPORT_H
#define STU32_REPORT_H

#include <stddef.h>

#include "calc.h"
#include "screen.h"

/* A screen line's kind by name ("value", "entry", ...), or "?". */
const char *kr_kind(int kind);

/* The GRAPH line for a graph shown ("GRAPH<TAB>id<TAB>readout<TAB>xmin<TAB>xmax<TAB>ymin<TAB>ymax<TAB>note\n"),
   or nothing when no graph shows. The length written, or -1 when out is too small. */
int kr_graph_line(const screen_page *page, const char *id, char *out, size_t cap);

/* The DRAWN line for an equation STU draws in 2D (unit 080: screen_page's textbook_on), what the area draws as text
   ("DRAWN<TAB>id<TAB>drawn\n": × only where drawn, e^u, |u|, √u, a÷b), or nothing when none is drawn. The length
   written, or -1 when out is too small. */
int kr_drawn_line(const screen_page *page, const char *id, char *out, size_t cap);

/* The EXPR line when a stack level holds an expression or a name (unit 082): X Y Z T each as STU's text (calc.h's
   ab_expr_text, a name as its letter), "none" for a number ("EXPR<TAB>id<TAB>x<TAB>y<TAB>z<TAB>t\n"), or nothing
   when every level is a number. The length written, or -1 when out is too small. */
int kr_expr_line(const ab_calc *c, const char *id, char *out, size_t cap);

/* The report after a step named id: the X line, the line above it, the status band, X Y Z T as exact
   numbers (a complex one as its two parts joined by "i", "" for a vector or an expression), and the GRAPH, DRAWN and
   EXPR lines:
     X<TAB>id<TAB>kind<TAB>text
     YL<TAB>id<TAB>kind<TAB>text
     STATUS<TAB>id<TAB>text
     VAL<TAB>id<TAB>x<TAB>y<TAB>z<TAB>t
     ANS<TAB>id<TAB>ans<TAB>shown
     GRAPH<TAB>...          (only with a graph shown)
     DRAWN<TAB>id<TAB>drawn  (only with an equation drawn in 2D)
     EXPR<TAB>id<TAB>x<TAB>y<TAB>z<TAB>t  (only with an expression on the stack)
     XMARK<TAB>id<TAB>mark  (always: ≈ drawn before X's number on STU's home, or -; unit 096)
   ANS is the last result (calc.h's ans: algebraic entry's result, the stack untouched) and shown the value an
   algebraic X line shows: a history entry while one is selected, else ans (screen.c's rule; soroban #5854).
   The length written, or -1 when out is too small. */
int kr_report(const ab_calc *c, const screen_page *page, const char *id, char *out, size_t cap);

#endif
