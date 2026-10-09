/* judge: whether an answer is right (judge.h). A number is held as its significant digits and an
   exponent, value = digits x 10^exp, normalised (no leading or trailing zeros in the digits; zero is
   no digits). Equality compares those; a tolerance computes |got - center| exactly by aligned digit
   arithmetic and compares it with tol. */
#include <ctype.h>
#include <string.h>

#include "judge.h"

#define MAXD 72             /* significant digits a number may carry */
#define SPAN 512            /* the widest aligned sum computed exactly */

typedef struct {
    int neg;
    int n;                  /* digits held; 0 for zero */
    long exp;
    char d[SPAN + 2];       /* digits, most significant first, as 0..9 (a parsed number has at most
                               MAXD; a difference may have up to SPAN) */
} dec;

static int parse(const char *s, dec *x)
{
    memset(x, 0, sizeof *x);
    if (!s)
        return -1;
    while (isspace((unsigned char)*s))
        s++;
    if (*s == '+' || *s == '-')
        x->neg = *s++ == '-';
    int digits = 0, point = 0, after = 0;
    char buf[MAXD + 8];
    int nb = 0;
    for (; *s; s++) {
        if (isdigit((unsigned char)*s)) {
            digits++;
            if (point)
                after++;
            if (nb == 0 && *s == '0')
                continue;                   /* leading zeros carry no digit */
            if (nb >= MAXD)
                return -1;
            buf[nb++] = (char)(*s - '0');
        } else if (*s == '.' && !point) {
            point = 1;
        } else {
            break;
        }
    }
    if (!digits)
        return -1;
    long e = 0;
    if (*s == 'E' || *s == 'e') {
        s++;
        int eneg = 0;
        if (*s == '+' || *s == '-')
            eneg = *s++ == '-';
        if (!isdigit((unsigned char)*s))
            return -1;
        for (; isdigit((unsigned char)*s); s++) {
            e = e * 10 + (*s - '0');
            if (e > 100000)
                return -1;
        }
        if (eneg)
            e = -e;
    }
    while (isspace((unsigned char)*s))
        s++;
    if (*s)
        return -1;
    /* The digits kept are the significant ones; the exponent counts from the last digit typed. Leading
       zeros after the point were skipped above but still count toward `after`. */
    long ex = e - after;
    while (nb > 0 && buf[nb - 1] == 0) {    /* trailing zeros into the exponent */
        nb--;
        ex++;
    }
    x->n = nb;
    memcpy(x->d, buf, (size_t)nb);
    x->exp = nb ? ex : 0;
    if (!nb)
        x->neg = 0;                         /* -0 is 0 */
    return 0;
}

static int same(const dec *a, const dec *b)
{
    return a->n == b->n && (a->n == 0 || (a->neg == b->neg && a->exp == b->exp && !memcmp(a->d, b->d, (size_t)a->n)));
}

/* The position just above a number's leading digit: its value is below 10^top. Zero has none. */
static long top(const dec *a) { return a->exp + a->n; }

/* Compare magnitudes: -1, 0 or 1. */
static int cmp_mag(const dec *a, const dec *b)
{
    if (!a->n || !b->n)
        return (a->n > 0) - (b->n > 0);
    if (top(a) != top(b))
        return top(a) < top(b) ? -1 : 1;
    int m = a->n < b->n ? a->n : b->n;
    int c = memcmp(a->d, b->d, (size_t)m);
    if (c)
        return c < 0 ? -1 : 1;
    return (a->n > b->n) - (a->n < b->n);
}

/* |a - b|, exactly, when the two are within SPAN digits of each other. Beyond that the smaller lies
   more than SPAN - MAXD places below the larger's last digit, and the larger is returned: off from the
   exact difference by less than one part in 10^(SPAN - MAXD), which no tolerance a vector can write
   (at most MAXD digits) can tell apart. */
static void absdiff(const dec *a, const dec *b, dec *out)
{
    memset(out, 0, sizeof *out);
    if (!a->n || !b->n) {
        *out = a->n ? *a : *b;
        out->neg = 0;
        return;
    }
    long lo = a->exp < b->exp ? a->exp : b->exp;
    long hi = (top(a) > top(b) ? top(a) : top(b)) + 1;      /* room for a carry */
    if (hi - lo > SPAN) {
        *out = cmp_mag(a, b) >= 0 ? *a : *b;
        out->neg = 0;
        return;
    }
    int len = (int)(hi - lo);
    signed char x[SPAN + 2] = {0}, y[SPAN + 2] = {0};        /* least significant first */
    for (int i = 0; i < a->n; i++)
        x[a->exp - lo + (a->n - 1 - i)] = a->d[i];
    for (int i = 0; i < b->n; i++)
        y[b->exp - lo + (b->n - 1 - i)] = b->d[i];
    signed char r[SPAN + 2] = {0};
    if (a->neg != b->neg) {                                  /* opposite signs: magnitudes add */
        int carry = 0;
        for (int i = 0; i < len; i++) {
            int s = x[i] + y[i] + carry;
            r[i] = (signed char)(s % 10);
            carry = s / 10;
        }
    } else {                                                 /* same sign: the larger less the smaller */
        signed char *big = x, *small = y;
        if (cmp_mag(a, b) < 0) {
            big = y;
            small = x;
        }
        int borrow = 0;
        for (int i = 0; i < len; i++) {
            int s = big[i] - small[i] - borrow;
            borrow = s < 0;
            r[i] = (signed char)(s + (borrow ? 10 : 0));
        }
    }
    int msd = len - 1;
    while (msd >= 0 && r[msd] == 0)
        msd--;
    if (msd < 0)
        return;                                              /* zero */
    int lsd = 0;
    while (r[lsd] == 0)
        lsd++;
    int n = msd - lsd + 1;
    for (int i = 0; i < n; i++)
        out->d[i] = (char)r[msd - i];
    out->n = n;
    out->exp = lo + lsd;
    while (out->n > 0 && out->d[out->n - 1] == 0) {
        out->n--;
        out->exp++;
    }
}

int judge_equal(const char *want, const char *got)
{
    dec a, b;
    if (parse(want, &a) || parse(got, &b))
        return -1;
    return same(&a, &b);
}

int judge_within(const char *center, const char *tol, const char *got)
{
    dec c, t, g, d;
    if (parse(center, &c) || parse(tol, &t) || parse(got, &g) || t.neg)
        return -1;
    absdiff(&g, &c, &d);
    return cmp_mag(&d, &t) <= 0;
}

int judge_expect(const char *expectation, const char *got)
{
    if (!expectation || !isupper((unsigned char)expectation[0]))
        return -1;
    const char *p = expectation + 1;
    if (*p == '=')
        return judge_equal(p + 1, got);
    if (*p != '#')
        return -1;
    p++;
    const char *comma = strchr(p, ',');
    if (!comma || strchr(comma + 1, ','))
        return -1;
    char center[128];
    size_t n = (size_t)(comma - p);
    if (n == 0 || n >= sizeof center)
        return -1;
    memcpy(center, p, n);
    center[n] = '\0';
    return judge_within(center, comma + 1, got);
}
