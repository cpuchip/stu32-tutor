/* judge: whether an answer is right, as one comparison for the learning page and the harness (primer
 * #5229; docs/proposals/lore-and-assessment.md). It works on decimal text alone: no core, no trace, no
 * main, so the page compiles it beside report.c. `make check` proves it agrees with the firmware's
 * vector runner on every expectation in every lesson (tools/judge_check.py). */
#ifndef STU32_JUDGE_H
#define STU32_JUDGE_H

/* A number's text: an optional sign, digits with an optional point, and an optional exponent
   (E or e, its own sign): "12.002", "-0.5", "+12002E-3" (keyrun's VAL form), "1E-15". Up to 72
   significant digits. A complex value ("2i4") or a vector is not a number here. */

/* 1 when want and got are the same number (trailing zeros and the exponent's form aside; -0 is 0),
   0 when they differ, -1 when either is not a number. */
int judge_equal(const char *want, const char *got);

/* 1 when |got - center| <= tol exactly, 0 when not, -1 when any is not a number or tol < 0. */
int judge_within(const char *center, const char *tol, const char *got);

/* An expectation as the vectors write it, against the value the learner's keys left: "X=12.002"
   (exact), "X#12,1E-15" (within), any register letter (X, Y, Z, T, or N for the algebraic line's
   answer). 1 right, 0 wrong, -1 when the expectation or the value cannot be read. */
int judge_expect(const char *expectation, const char *got);

#endif
