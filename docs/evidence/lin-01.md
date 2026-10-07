# lin-01 evidence

## Expected values (2026-10-06, core 25dca53)

| Vector | What | Exact |
|---|---|---|
| L01 | slope through (3, 9) and (5, 13): (13 - 9) / (5 - 3) | 2 |
| L02 | kept in M | M = 2 |
| L03A | stopping point: 9 RCL M 3 | Z 9, Y 2, X 3 being typed |
| L03 | b = 9 - 2 x 3, kept in B | 3 |
| L04 | the line at x = 5: 5 x 2 + 3 | 13 |
| L05 | slope through (0, 10) and (5, 0) | -2 |
| L06 | slope through (1, 4) and (3, 4) | 0 |
| L07 | slope through (3, 1) and (3, 5): run 0 | DIVIDE BY 0 |
| L07B | C: the run in X, the rise in Y | X 0, Y 4 |
| L07C | x<>y: the rise | 4 |
| E01 | slope through (-1, 5) and (3, 13) | 2 |
| E01B | b = 5 - 2 x (-1) | 7 |
| E02 | slope through (0, 1) and (4, 4) | 0.75 |

All exact on the core at 25dca53, in 33s and 35s modes. The oracle is computed independently in
exact fractions before the vectors run (build/proto/lin01.py asserts each slope and intercept, and
that m, x and y differ in every worked point).

## Sources and probes

- Letters (keymap.c LETTER table): M is letter 12, on the ENTER key; B is letter 1, on the eˣ key.
- DIVIDE BY 0 as fn-03 quoted it (abacus #4415: the guides' appendix F, p.F-1).
- The stack in L03: pinned by the stopping point L03A (9 in Z, m in Y, 3 being typed) and L03's
  result; the narrated drop after × is the stack's rule from rpn-01.

## Non-author read (2026-10-06)

Eight findings, all taken. The largest: the first draft's points made m and x both 2 (and y = 2 in
the exercise), so a learner could swap them and still get the answer; the points are now (3, 9)
and (5, 13), and (-1, 5) and (3, 13), with m, x and y distinct, and the oracle asserts it. Also:
the stack in "9 RCL M 3 × −" walked through, with a stopping point quoting the 3 being typed; the
rule b = y - mx stated in letters; rise and run taken from the same point in the same order; "a
function gives one output for each input" said before the vertical line uses it, and "the input 3"
for "x = 3"; the chain sentence made true (L07B carries on); x↔y added so the rise in Y is seen
(L07C); the axes tied to fn-02 and the y axis called the vertical axis; STO M said to be STO then
ENTER. One of my own: "as in eq-02" dropped, since eq-02 solves formulas with SOLVE, not by hand.

## Checks

`make check`: 13/13 vectors in 33s and 35s, from a fresh and a used core; 14 keys blocks; 12 quotes,
each on the device and again in the in-order run. Controls: the slope keyed run over rise, the
vertical line's message misquoted, the intercept quoted as the slope; all red.
