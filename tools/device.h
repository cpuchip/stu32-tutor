/* device: how the harness drives the STU-32's app layer, as the device does: one source for keyrun
 * and the learning page (primer #4573), so neither holds a copy of how a key is pressed. It depends
 * only on the firmware's core and app: no trace, no main. */
#ifndef STU32_DEVICE_H
#define STU32_DEVICE_H

#include "app.h"
#include "calc.h"

/* A fresh device: the core initialised, the app started at time 0, the graph buffer the device keeps
   in PSRAM attached (unit 033: without it no graph is drawn), and the app framework's context buffer
   (APP_CTX_MAX, owned by device.c). */
void kr_device_init(ab_calc *c, app_state *a, app_graph *g);

/* One key, 100 ms after the last event, with nothing settled after it. */
void kr_key(app_state *a, int key);

/* Ticks until the device is at rest: no program running, no pause, no graph still drawing its columns;
   then one tick more. */
void kr_settle(app_state *a);

/* A key pressed and settled: kr_key, then kr_settle. */
void kr_press(app_state *a, int key);

/* The device's clock moved forward ms, one tick a millisecond, as real time passes: for a page that
   runs an app (a game) live (primer #5069). keyrun does not use it. */
void kr_advance(app_state *a, uint32_t ms);

/* One key at the clock's present time, with no jump: for a live app whose step is the time elapsed
   between ticks (primer #5109), where kr_key's 100 ms would lurch it. */
void kr_key_now(app_state *a, int key);

/* That key released at the clock's present time: an app that steers by held keys (Babal) ends a turn
   on the release (primer #5126). */
void kr_key_up_now(app_state *a, int key);

#endif
