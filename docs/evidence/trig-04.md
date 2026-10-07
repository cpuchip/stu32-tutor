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

(3, 4)'s θ at 8f304cd was 0.93 units below the correctly rounded truth (…659), a pin that predates
unit 034, which made →POL's θ correctly rounded (abacus #4685). From the repin to d75fc75 it is exact:
P01, P02 and D-P02 now assert …659, and nothing is pinned.

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

## Accuracy read (abacus, #4691)

Accepted, every value and statement. On (1): a point on the negative x axis gives 180, not −180, so
"from −180 to 180" holds only read as −180 < θ ≤ 180; "Say 'up to and including 180' if it's quoted."
Taken: "from just above −180 up to and including 180 degrees (a point straight left gets 180, never
−180)". Probed at d75fc75: 0 ENTER 1 CHS →POL and 0 CHS ENTER 1 CHS →POL both give 180 after x<>y.

## Checks

`make check`: 10/10 vectors in 33s, 35s and STU, from a fresh and a used core; 11 keys blocks.
Controls: →POL with x and y swapped, the second-quadrant angle quoted as ATAN's, →REC with r and θ
swapped; all red.
