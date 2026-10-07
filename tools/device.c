/* device: how the harness drives the app layer (device.h). */
#include "device.h"

static uint32_t now;                                    /* the device's clock, in ms */
static const pwr_inputs PWR = {true, true, 80, false};  /* on USB power, a healthy battery */

void kr_device_init(ab_calc *c, app_state *a, app_graph *g)
{
    now = 0;
    ab_init(c);
    app_init(a, c, now);
    app_graph_buffer(a, g);
}

void kr_key(app_state *a, int key)
{
    app_key(a, key, now += 100);
}

void kr_settle(app_state *a)
{
    for (int i = 0; i < 1000000 && (a->running || a->pause || a->graphing); i++) app_tick(a, &PWR, now += 1);
    app_tick(a, &PWR, now += 1);
}

void kr_press(app_state *a, int key)
{
    kr_key(a, key);
    kr_settle(a);
}
