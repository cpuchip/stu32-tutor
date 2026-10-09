# whole-01 evidence: adding and subtracting (pre-algebra unit 1)

Pre-algebra's first lesson after start-01 (abacus #5387: units 1 to 5, Thornwick, algebraic first
with RPN offered, hand first). It introduces Hesk and Tobin (their lore homes).

## The core (be3617e)

The device shows FIX 4 with a comma every three digits left of the point (`5,331.0000`), measured
when the first quotes failed; pa_lib's FIX 4 formats so, and the lesson says so where the first long
number appears. A control plants a quote without the comma.

## Expected values

Oracle: build/proto/whole01.py (on build/proto/pa_lib.py). Every column of every hand computation is
asserted, carries and borrows included: 3452 + 1879, 742 − 368 (two borrows), the trade-down chain in
5000 − 2768, the estimates (with the rounding rule's cases), the slip 3452 + 879, and each exercise's
columns and estimate. 7 examples, each in both entries (14 vectors), 7 display vectors.

## Non-author read (2026-10-09)

Every column checked correct. Taken: the ordinary borrow was never taught though exercise 3 needed
it (now 742 − 368 before the zeros case); the 9s in "5000 as 4 thousands, 9 hundreds…" came from
nowhere (now the trade-down chain); "each place is worth ten of the place to its right" was imprecise
and joined two ideas (now like-with-like columns, and one of a place traded for ten of the next);
the rounding rule was missing; the answers gave no estimates; why a carried ten is written as 1; in
RPN, − takes the second number from the first.

## Checks

make check at be3617e: 7/7 vectors in STU alg and in STU rpn, the student run in order in each.
Controls (4): a carry dropped in the quoted sum; a quote without the comma; RPN's subtraction in the
wrong order; + typed for −. All red.
