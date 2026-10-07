/* resolve: a lesson's printed key names to the device's keys, in the device's own order.
 *
 * Shared by keyrun (the checker) and any page that presses a lesson's keys on the live calculator,
 * so both read a name the same way. It depends only on the firmware's app and keymap: no trace, no
 * main. Pressing is the caller's (keyrun logs and settles; a page draws), through a callback. */
#ifndef STU32_RESOLVE_H
#define STU32_RESOLVE_H

#include <stddef.h>

#include "app.h"

/* The key a printed name means in the state the device is in now, or -1 (none) or -2 (more than
   one), with *why saying which. */
int kr_resolve(const app_state *a, const char *name, const char **why);

/* Presses one key; tok is the index of the printed name it came from. */
typedef void (*kr_press_fn)(void *ctx, app_state *a, int key, int tok);

/* Presses printed key names in order through press: GOLD and BLUE as the shift keys, a number with
   no key of its own as its digit keys. 0, or 2 with err holding why a name resolved to no key
   ("KEY n 'name': ..."). */
int kr_press_names(app_state *a, char **tok, int ntok, kr_press_fn press, void *ctx,
                   char *err, size_t errcap);

#endif
