/* judge: whether an answer is right (judge.h). A number is held as its significant digits and an
   exponent, value = digits x 10^exp, normalised (no leading or trailing zeros in the digits; zero is
   no digits). Equality compares those; a tolerance computes |got - center| exactly by aligned digit
   arithmetic and compares it with tol. */
#include <ctype.h>
#include <stdlib.h>
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

/* The forms for answers that are not the calculator's number (T65; primer #15625, #15627): a word or a bit
   string, a number written in a base, and a table's cells. Text is compared with ASCII spaces removed and ASCII
   letters folded to lower case. */
#define TEXTMAX 256

static int text_norm(const char *s, size_t n, char *out)
{
    size_t k = 0;
    for (size_t i = 0; i < n && s[i]; i++) {
        unsigned char c = (unsigned char)s[i];
        if (isspace(c))
            continue;
        if (k >= TEXTMAX)
            return -1;
        out[k++] = (char)tolower(c);
    }
    out[k] = '\0';
    return (int)k;
}

static int text_cell(const char *want, size_t wn, const char *got, size_t gn)
{
    char a[TEXTMAX + 1], b[TEXTMAX + 1];
    int la = text_norm(want, wn, a), lb = text_norm(got, gn, b);
    if (la <= 0)
        return -1;
    if (lb < 0)
        return 0;
    return strcmp(a, b) == 0;
}

static int digit_of(unsigned char c)
{
    if (isdigit(c))
        return c - '0';
    c = (unsigned char)tolower(c);
    return c >= 'a' && c <= 'z' ? c - 'a' + 10 : -1;
}

/* A number's digits in a base: spaces dropped, leading zeros dropped, letters folded. 1 when every digit is
   one the base has and there is at least one, 0 otherwise. */
static int base_digits(int base, const char *s, size_t n, char *out)
{
    size_t k = 0;
    int any = 0;
    for (size_t i = 0; i < n && s[i]; i++) {
        unsigned char c = (unsigned char)s[i];
        if (isspace(c))
            continue;
        int d = digit_of(c);
        if (d < 0 || d >= base)
            return 0;
        any = 1;
        if (k == 0 && d == 0)
            continue;
        if (k >= TEXTMAX)
            return 0;
        out[k++] = (char)tolower(c);
    }
    out[k] = '\0';
    return any;
}

static int base_cell(int base, const char *want, size_t wn, const char *got, size_t gn)
{
    char a[TEXTMAX + 1], b[TEXTMAX + 1];
    if (base != 2 && base != 8 && base != 10 && base != 16)
        return -1;
    if (!base_digits(base, want, wn, a))
        return -1;
    if (!base_digits(base, got, gn, b))
        return 0;
    return strcmp(a, b) == 0;
}

/* "2:101101" (a number in base 2): its base, and where its digits start; 0 when s is not that form. */
static int base_prefix(const char *s, size_t n, const char **digits)
{
    static const char *const bases[] = {"2:", "8:", "10:", "16:"};
    for (int i = 0; i < 4; i++) {
        size_t m = strlen(bases[i]);
        if (n > m && !strncmp(s, bases[i], m)) {
            *digits = s + m;
            return (int)strtol(bases[i], NULL, 10);
        }
    }
    return 0;
}

int judge_text(const char *want, const char *got)
{
    if (!want || !got)
        return -1;
    return text_cell(want, strlen(want), got, strlen(got));
}

int judge_base(int base, const char *want, const char *got)
{
    if (!want || !got)
        return -1;
    return base_cell(base, want, strlen(want), got, strlen(got));
}

/* One cell of a grid expectation against one cell of the learner's: a base cell ("2:101") by value, any other
   as text. */
static int grid_cell(const char *w, size_t wn, const char *g, size_t gn)
{
    const char *digits;
    int base = base_prefix(w, wn, &digits);
    if (base)
        return base_cell(base, digits, wn - (size_t)(digits - w), g, gn);
    return text_cell(w, wn, g, gn);
}

/* The i-th comma-separated cell of s: its start and length; 0 when s has no such cell. */
static int nth_cell(const char *s, int i, const char **start, size_t *len)
{
    for (int k = 0; ; k++) {
        const char *e = strchr(s, ',');
        size_t n = e ? (size_t)(e - s) : strlen(s);
        if (k == i) {
            *start = s;
            *len = n;
            return 1;
        }
        if (!e)
            return 0;
        s = e + 1;
    }
}

static int cells_in(const char *s)
{
    int n = 1;
    for (; *s; s++)
        n += *s == ',';
    return n;
}

int judge_grid(const char *want, const char *got)
{
    if (!want || !got || !*want)
        return -1;
    int n = cells_in(want), verdict = 1;
    for (int i = 0; i < n; i++) {
        const char *w = NULL, *g = NULL;
        size_t wn = 0, gn = 0;
        nth_cell(want, i, &w, &wn);
        int c = grid_cell(w, wn, "", 0);
        if (c < 0)
            return -1;                      /* a cell the expectation cannot hold */
        if (!nth_cell(got, i, &g, &gn))
            verdict = 0;
        else if (grid_cell(w, wn, g, gn) != 1)
            verdict = 0;
    }
    if (cells_in(got) != n)
        verdict = 0;
    return verdict;
}

int judge_cell(const char *grid, int i, const char *got)
{
    const char *w = NULL;
    size_t wn = 0;
    if (!grid || !got || i < 0 || !nth_cell(grid, i, &w, &wn))
        return -1;
    return grid_cell(w, wn, got, strlen(got));
}

int judge_expect(const char *expectation, const char *got)
{
    if (!expectation || !isupper((unsigned char)expectation[0]))
        return -1;
    if (!strncmp(expectation, "TEXT=", 5))
        return judge_text(expectation + 5, got);
    if (!strncmp(expectation, "GRID=", 5))
        return judge_grid(expectation + 5, got);
    if (!strncmp(expectation, "BASE=", 5)) {
        const char *digits;
        const char *v = expectation + 5;
        int base = base_prefix(v, strlen(v), &digits);
        return base ? judge_base(base, digits, got) : -1;
    }
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
