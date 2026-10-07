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

/* The report after a step named id: the X line, the line above it, the status band, X Y Z T as exact
   numbers (a complex one as its two parts joined by "i", "" for a vector), and the GRAPH line:
     X<TAB>id<TAB>kind<TAB>text
     YL<TAB>id<TAB>kind<TAB>text
     STATUS<TAB>id<TAB>text
     VAL<TAB>id<TAB>x<TAB>y<TAB>z<TAB>t
     GRAPH<TAB>...          (only with a graph shown)
   The length written, or -1 when out is too small. */
int kr_report(const ab_calc *c, const screen_page *page, const char *id, char *out, size_t cap);

#endif
