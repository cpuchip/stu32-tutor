/* trace: logs every operation that reaches the core from outside it.
 *
 * Linked with -Wl,--wrap=ab_do_arg (and the other entry points below) into both the firmware's
 * vector runner and keyrun, so the two paths can be compared op for op. Calls inside calc.c
 * (a program running its own lines) are not wrapped by the linker, so only the outside callers
 * (the runner's tokens, the device's app layer) are logged.
 *
 * The runner opens the log from STU_TRACE at start; keyrun sets trace_out itself. */
#include <stdio.h>
#include <stdlib.h>

#include "calc.h"

FILE *trace_out;
int trace_token = -1;           /* keyrun: the prose token being pressed, for the report */

abn_status __real_ab_do_arg(ab_calc *c, ab_op op, int arg);
void __real_ab_memory_clear(ab_calc *c);
abn_status __real_ab_eqn_add(ab_calc *c, const char *text);

static int depth;

abn_status __wrap_ab_do_arg(ab_calc *c, ab_op op, int arg)
{
    if (trace_out && depth == 0) fprintf(trace_out, "%d %d %d\n", (int)op, arg, trace_token);
    depth++;
    abn_status st = __real_ab_do_arg(c, op, arg);
    depth--;
    return st;
}

/* Entry points that change the core without an op: logged so a comparison that meets one fails
   by name instead of passing on a stream that missed it. */
void __wrap_ab_memory_clear(ab_calc *c)
{
    if (trace_out && depth == 0) fprintf(trace_out, "UNTRACED ab_memory_clear %d\n", trace_token);
    __real_ab_memory_clear(c);
}

abn_status __wrap_ab_eqn_add(ab_calc *c, const char *text)
{
    if (trace_out && depth == 0) fprintf(trace_out, "UNTRACED ab_eqn_add %d\n", trace_token);
    return __real_ab_eqn_add(c, text);
}

__attribute__((constructor)) static void trace_open(void)
{
    const char *path = getenv("STU_TRACE");
    if (path && *path) {
        trace_out = fopen(path, "w");
        if (!trace_out) { perror(path); exit(2); }
    }
}
