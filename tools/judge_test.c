/* judge_test: tools/judge.c on the command line, for tools/judge_check.py. Each line of stdin is
   "expectation<TAB>value" (or "CELL i<TAB>grid<TAB>value" for judge_cell); each line of stdout is the
   answer for it: 1, 0 or -1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "judge.h"

int main(void)
{
    static char line[1024];
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = '\0';
        char *tab = strchr(line, '\t');
        if (!tab) {
            puts("-1");
            continue;
        }
        *tab = '\0';
        /* "CELL i<TAB>grid<TAB>value": judge_cell, the page's mark for one cell of a table (T65). */
        if (!strncmp(line, "CELL ", 5)) {
            char *tab2 = strchr(tab + 1, '\t');
            if (!tab2) {
                puts("-1");
                continue;
            }
            *tab2 = '\0';
            printf("%d\n", judge_cell(tab + 1, atoi(line + 5), tab2 + 1));
            continue;
        }
        printf("%d\n", judge_expect(line, tab + 1));
    }
    return 0;
}
