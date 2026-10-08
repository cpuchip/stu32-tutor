/* device: how the harness drives the app layer (device.h). */
#include "apps.h"
#include "device.h"

static uint32_t now;                                    /* the device's clock, in ms */
static const pwr_inputs PWR = {true, true, 80, false};  /* on USB power, a healthy battery */
static char ctx[APP_CTX_MAX];                           /* the app framework's state, as the device gives it
                                                           (apps.h v1.1; primer #4652) */

void kr_device_init(ab_calc *c, app_state *a, app_graph *g)
{
    now = 0;
    ab_init(c);
    app_init(a, c, now);
    app_graph_buffer(a, g);
    app_ctx_buffer(a, ctx, APP_CTX_MAX);
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

void kr_key_now(app_state *a, int key)
{
    app_key(a, key, now);
}

void kr_key_up_now(app_state *a, int key)
{
    app_key_up(a, key, now);
}

void kr_advance(app_state *a, uint32_t ms)
{
    while (ms--) app_tick(a, &PWR, now += 1);
}
