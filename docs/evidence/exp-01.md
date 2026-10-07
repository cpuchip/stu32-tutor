# exp-01 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/exp01.py. It models the keystrokes, each operation rounded once to 34
digits, half even, not the ideal maths: E01's 2000 × 1.03²⁵ rounds 1.03²⁵ first (exact, then rounded:
unit 038) and then the product, and that ends one unit in the last digit below the once-rounded ideal
product (…752 against …753). The first oracle rounded once and the vector failed; the keys were right.

| Vector | What | Exact |
|---|---|---|
| G01 | 500 × 1.04¹⁰ | 740.12214245917196288 |
| G02 | 500 + 20 × 10 | 700 |
| D01A | 80 ENTER 0.5 ENTER 15 ENTER 6 ÷ | X 2.5, Y 0.5, Z 80, T 80 |
| D01 | then yˣ ×: 80 × 0.5^2.5 = 10√2 | 14.14213562373095048801688724209698 (correctly rounded) |
| R01 | (1452 / 1200)^(1/2) | 1.1 |
| E01 | 2000 × 1.03²⁵ by the keys | 4187.555859308429526297187681803752 |
| E02 | 18000 × 0.85⁴ | 9396.1125 |
| E03 | (9261 / 8000)^(1/3) | 1.05 |

All exact or correctly rounded on the core at 8f304cd, in 33s and 35s modes.

## Sources and probes

- yˣ and ˣ√y (gold above yˣ) and "a power of one half is a square root": num-03.
- The full stack in D01A and T copying down on the drop: rpn-01; pinned by the stopping point.
- Two hand values of mine were wrong and the oracle's asserts caught both before any vector ran:
  18000 × 0.85⁴ (I wrote a wrong numerator) and an exercise built on 1.08³ that was really 1.08².

## Non-author read (2026-10-07)

No mathematical errors; seven findings, all taken. A fractional number of steps justified (the decay
is continuous; 0.5^2.5 = 0.5² × √0.5, num-03's half powers). D01's stack traced, with a stopping point
(D01A) after ÷, the 80 in T and copied down. "Not halfway" made to compare amounts, not times (20 to
14.1421 in three hours, 14.1421 to 10 in the next three). The percent-to-factor rule for decay (1 − r ÷
100) taught in the body, not only in an answer. The 21% rise warned against halving (1200, 1320,
1452), with the equation 1200 × b × b = 1452 written. The cause of fast growth stated as the cause
(each year's increase is bigger), not the growing gap. lin-03 recalled as a line describing doubling
badly, not failing to follow it. A third exercise added for the root.

## Checks

`make check`: 8/8 vectors in 33s and 35s, from a fresh and a used core; 9 keys blocks; 8 quotes.
Controls: 4% growth keyed as a factor of 0.04, 15% loss as 1.15, the decay quoted as halfway; all red.

## Abacus's accuracy read (#4546, 2026-10-07)

Accepted at c0480c4. The values checked; modelling each operation rounded once is the right oracle
(E01: 2000 × the rounded 1.03²⁵); statements (1)-(4) right.
