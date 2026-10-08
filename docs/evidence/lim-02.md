# lim-02 evidence: rates of change

## Expected values (2026-10-07, core c7ab388)

Oracle: build/proto/lim02.py, modelling the keys: each operation rounded once to 34 digits, half even.
Here that rounding decides the last answers, so the oracle computes them step by step (1 + h, its square,
twice it, minus 2, divided by h) and asserts the boundary: 1 + 5 × 10⁻³⁴ rounds to 1 (a tie, to even),
1 + 6 × 10⁻³⁴ to 1 + 10⁻³³. 14/14 vectors, 12/12 display vectors; the core agreed on every one.

| Vector | What | Value (shown) |
|---|---|---|
| A01 | average speed, 1 to 3: (2 × 3² − 2 × 1²) ÷ (3 − 1) | 8 |
| P01A, P01 | program D, 12 lines, from GTO . . | D012 RTN |
| D01..D03B | h = 0.1, 0.01, 0.001, −0.001 | 4.2, 4.02, 4.002, 3.998 |
| D04 | h = 10⁻²⁰ | exactly 4 (the true 4 + 2 × 10⁻²⁰ lost its 2h² in squaring) |
| D05 | h = 10⁻³⁴ | 0 (1 + h rounds to 1) |
| D06 | h = 6 × 10⁻³⁴ | 6.666…7 (1 + h rounds to 1 + 10⁻³³; 4 × 10⁻³³ ÷ 6 × 10⁻³⁴) |
| E01 | h = 10⁻⁴⁰ | 0 |
| E02, E02B | x³ at 2, h = 0.001, 0.0001 | 12.006001, 12.00060001 |
| E03 | 2ˣ, 0 to 3: (2³ − 1) ÷ 3 | 2.333… |

## Sources and probes

- The label D: no other lesson's vectors use it.
- The spacing of 34-digit numbers near 1 (the 34th digit is 10⁻³³ above 1, 10⁻³⁴ below): abacus #4983.

## Non-author read (2026-10-07)

Every display matched; program D and A01 traced right. Taken:
- The instant rate used h > 0 only, though lim-01 checks both sides: D03B at h = −0.001 (3.998), and the
  algebra said to cover both signs.
- "divided by h that is 4 + 2h" needed h ≠ 0, and (1 + h)² = 1 + 2h + h² was skipped: both said.
- "1 + h would need a 35th digit, so it is just 1" read as "dropped", then h = 6 × 10⁻³⁴ rounded up: the
  rule is rounding to the nearer step, and each case now says which side of halfway it is.
- The cancellation account misplaced the error ("the last few digits", "the rounding in those"): the
  subtraction is exact, leaves one digit, and the rounding of 1 + h becomes the whole answer; 40 ÷ 6
  shown; cancellation defined as the subtraction exposing earlier rounding, not losing digits itself.
- "4.0000, as it should" at h = 10⁻²⁰ hid that the 2h² term was already lost: said (and the oracle's note
  "still 4 to 34 digits" corrected).
- "the derivative" made "the derivative of d at t = 1"; "calculus is largely about finding it" softened;
  the three names (instantaneous rate, rate at an instant, derivative) tied together.
- The program's recovery line, GTO . .'s reason, and DUPLICAT.LBL on a second entry; neg-e cited with E;
  the chain's extent said.
- "0.001 already showed 4 clearly" became "suggested 4".
- Exercises: one on the digit floor (h = 10⁻⁴⁰, chained), x³ at two h with its algebra, 2ˣ keyed with yˣ.
- Wording: 18 metres; "two different points where it has values"; the slope sentence; requires gained
  fraction-bar and powers-first.

## Checks

`make check`: 14/14 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (3): program D without taking away d(1), h = 10⁻³⁴ quoted as 4, the average
speed quoted as the instant one; all red.
