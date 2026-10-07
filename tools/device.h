/* device: how the harness drives the STU-32's app layer, as the device does: one source for keyrun
 * and the learning page (primer #4573), so neither holds a copy of how a key is pressed. It depends
 * only on the firmware's core and app: no trace, no main. */
#ifndef STU32_DEVICE_H
#define STU32_DEVICE_H

#include "app.h"
#include "calc.h"

/* A fresh device: the core initialised, the app started at time 0, and the graph buffer the device
   keeps in PSRAM attached (unit 033: without it no graph is drawn). */
void kr_device_init(ab_calc *c, app_state *a, app_graph *g);

/* One key, 100 ms after the last event, with nothing settled after it. */
void kr_key(app_state *a, int key);

/* Ticks until the device is at rest: no program running, no pause, no graph still drawing its columns;
   then one tick more. */
void kr_settle(app_state *a);

/* A key pressed and settled: kr_key, then kr_settle. */
void kr_press(app_state *a, int key);

#endif
