# trig-04 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/trig04.py with dmath.py (80 digits): r by the square root of x² + y², θ by
atan with the quadrant placed (atan2), →REC by r cos θ and r sin θ, each rounded once.

| Vector | What | FIX 4 |
|---|---|---|
| P01, P02 | (3, 4) →POL: r, then θ | 5.0000, 53.1301 (core …658; see below) |
| Q01, Q02 | (−3, 4) →POL θ; ATAN(4 ÷ −3) | 126.8699, -53.1301 |
| R01, R02 | (10, 30°) →REC: x, y | 8.6603, 5.0000 |
| E01, E01B | (−5, −12) →POL: r, θ | 13.0000, -112.6199 (exact: -112.6198649480404261729490108766797) |
| E02, E02B | (2, 135°) →REC: x, y | -1.4142, 1.4142 |

(3, 4)'s θ on this core is 0.93 units below the correctly rounded truth (…659): the pin 8f304cd
predates unit 034, which made →POL's θ correctly rounded (abacus #4685: on 734bb48 it is exact). Pinned
within 2 units now; exact at the next repin.

## Sources and probes

- →POL and →REC in the ANGLE menu (blue above SIN): y in Y and x in X in, r in X and θ in Y out; →REC
  the reverse (keyrun --sequence, all three modes, the same).

## Non-author read (2026-10-07)

No mathematical errors; ten findings, all taken. The largest: exercise 1's point (5, −12) is one where
ATAN alone already gives the right angle, so it did not test the lesson's point; it is now (−5, −12),
where ATAN points the opposite way, and the answer says so. Also: →POL's range (−180 to 180) taught,
with adding 360 (trig-03); "polar form" defined as (r, θ); a picture of the point, r, θ, x and y, and
why x = r cos θ (the point is r times as far out as trig-03's P); "the centre" named as O;
r = √(x² + y²) stated, squaring removing signs; ATAN's range said to be new here and where its −53.1301
points (3, −4), with "add 180"; "correct side" for "right side"; the back-reference moved from fn-02's
x and q axes to trig-03; the angle unit mentioned.

## Checks

`make check`: 10/10 vectors in 33s, 35s and STU, from a fresh and a used core; 11 keys blocks.
Controls: →POL with x and y swapped, the second-quadrant angle quoted as ATAN's, →REC with r and θ
swapped; all red.
