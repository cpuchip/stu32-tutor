/* judge_test: tools/judge.c on the command line, for tools/judge_check.py. Each line of stdin is
   "expectation<TAB>value"; each line of stdout is judge_expect's answer for it: 1, 0 or -1. */
#include <stdio.h>
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
        printf("%d\n", judge_expect(line, tab + 1));
    }
    return 0;
}
