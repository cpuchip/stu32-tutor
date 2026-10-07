# lin-03 evidence

## Expected values (2026-10-06, core 25dca53)

The oracle is build/proto/lin03.py (exact fractions; r from the exact r², square root at 60 digits,
rounded to 34). It asserts the parabola's m = 0, b = 1, r² = 0 and the line's m = 2, b = 3, r = 1
before the vectors run.

| Vector | What | Exact |
|---|---|---|
| Q01 | fn-02's q at x = 0..4 (3 0 -1 0 3) | n 5 |
| Q02 | r | 0 |
| Q03 | m | 0 |
| Q04 | b, the mean of the values | 1 |
| Q05 | ŷ at x = 2 (q(2) = -1) | 1 |
| P01 | f(x) = 2x + 3 at x = 0..4: r | 1 |
| P02, P03 | m, b | 2, 3 |
| F01-F04 | flat: y = 4 at x = 1..3: r refused; C; m, b | STAT ERROR; n 3; 0, 4 |
| E01 | doubling 2 4 8 16 32 at x = 1..5: r | 0.9332565252573827415251642949128384 |
| E01B-E01D | ŷ at x = 1, 3, 6 (data 2, 8; doubling 64) | -2, 12.4, 34 (m 36/5, b -46/5) |

Every value matched the core to all 34 digits; r = 0 and r = 1 come out exact on the core.

## Sources and probes

- The parabola's r and m probed with keyrun --sequence at 25dca53 before the vectors were written
  (r 0, m 0, both exact).
- Why the best line is flat: the points are symmetric about x = 2, so the sum of (x - x̄)(y - ȳ) is 0;
  the lesson says it in words (the halves fall and rise by the same amounts).
- Flat data: probed first (keyrun --sequence, 25dca53): r gives STAT ERROR, C leaves n = 3, m 0
  and b 4. abacus found the same independently (#4446).

## Non-author read (2026-10-06)

Ten findings; nine taken. The largest: the exercise proved the wrong shape by extrapolation, which
lin-02 had already called risky for any line; the answer now looks at the steps first, then shows
the misfit inside the data (the line gives -2 at x = 1, below zero for something that starts at 2,
and 12.4 at x = 3 where the data says 8). r's wording made exact throughout ("no sloping line"), and
the r = 1 sentence limited to a sloping line, with a new section on exactly flat data (STAT ERROR),
which also corrected lin-02. "Average rise" dropped; the mirror argument completed; "model" defined;
"call them unrelated" replaced. Not taken: the reader read the line as above the points at the ends;
the vectors say below (-2 against 2 at x = 1; 26.8 against 32 at x = 5), and the lesson says so.

## Checks

`make check`: 16/16 vectors in 33s and 35s, from a fresh and a used core; 17 keys blocks; 16
quotes. Controls: q(2) keyed without its sign, the curve's r misquoted, the doubling estimate quoted
as the doubling, flat data's r quoted as 0; all red.

## Abacus's accuracy read (#4460, 2026-10-06)

Accepted at 3786117 (16/16 in order, every controls set red). The doubling data recomputed by hand:
m 7.2, b -9.2, ŷ -2 / 12.4 / 26.8 / 34, r = 72/√5952 = 0.93326. (a) |r| = 1 exactly when every
point is on one sloping line (the Cauchy-Schwarz equality case). (b) r divides by y's spread, zero
for flat data. (c) The mirror argument holds for data symmetric about its middle x; the lesson
states that condition ("The points mirror each other about x = 2"), and any reuse must keep it.
(d) Low at the ends, high in the middle, as the lesson says.
