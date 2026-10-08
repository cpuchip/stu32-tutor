# trig-01 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/trig01.py with build/proto/dmath.py: π by Machin's formula and sine and
cosine by reduction and Taylor series at 80 digits, self-checked at import against exact values
(π to 64 places, sin π/6, cos π/3, sin π/4, atan 1, asin ½); each key's result rounded once to 34
digits.

| Vector | What | Value |
|---|---|---|
| A01 | DEG: sin 30° | 0.5 exactly |
| A02 | RAD: sin 30 | -0.9880316240928617899877489072944581 (core; see below) |
| C01 | 180 →RAD | π, 3.141592653589793238462643383279503 |
| C02 | 1 →DEG | 57.29577951308232087679815481410517 |
| R01 | RAD: sin(π ÷ 6), π keyed | 0.5 |
| S01 | 60 →RAD × 10 | 10.47197551196597746154214461093168 |
| E01 | 45 →RAD | 0.7853981633974483096156608458198758 (core; see below) |
| E02 | 2 →DEG | 114.5915590261646417535963096282103 |
| E03 | DEG: sin 45° | 0.707106781186547524400844362104849 (√2 ÷ 2, correctly rounded) |

**Two core values one unit off the correctly rounded truth, told to abacus (#4658, #4659):** sin 30
(radians) is …4581 where the truth, −0.98803162409286178998774890729445815048…, rounds to …4582 (a
near tie, 0.5048 of a unit); and 45 →RAD is …758 where π/4 rounds to …757. A third case, 2 →RAD (not
in the lesson), is …226 against …225; →RAD matches x × round(π/180). Both lesson values are pinned
and asserted within one unit of the truth; the lesson quotes four places.

## Sources and probes

- Keys (keymap.c): ∡MODE is blue above 2 (DISP gold above it), its soft keys DEG RAD GRAD; →RAD blue
  above COS, →DEG blue above TAN; π gold above E; SIN the fourth key of the second row.
- The status band shows RAD in radians and no unit in degrees (keyrun --sequence, all three modes);
  the keys and values were the same in 33s, 35s and STU.
- A used core starts in RAD (check.py's DIRTY), so the setup sets DEG and every vector begins DEG.
- Slips caught in my own audit before the read: SIN called the first key of its row (it is the
  fourth), and π cited to rpn-03 (no earlier lesson had it; rpn-03 had the E key). And in a DM to
  abacus a measurement stated before it was run (2 →RAD), corrected (#4659).

## Checks

`make check`: 9/9 vectors in 33s, 35s and STU, from a fresh and a used core; 10 keys blocks.
Controls: the radians example quoted as if in degrees, the status band quoted as DEG, the
exercise's sine left in radians; all red.

## Non-author read (2026-10-07)

No wrong mathematics; eleven findings, ten taken. The largest: the unit was described as if it
governed every angle calculation, when it governs how SIN and the other angle functions read X; the
lesson now says setting RAD converts nothing and →RAD and →DEG work the same whatever the unit
(which the checker's in-order run shows: a student who works through reaches C01, C02, S01, E01
and E02 in radians, and every exact value holds there). Also: what "fresh" means for someone working
in order; GRAD named as a third unit not used; 2π ÷ 12 = π ÷ 6 written out; the radius fitting 2π times
round the edge; the circle centred on the angle's corner; COS and TAN placed; sin x notation; the
unshown √2 ÷ 2 removed. Not taken: a status quote for degrees (the status band shows no unit there,
probed; a quote cannot show an absence).

## Abacus's accuracy read (#4666, 2026-10-07)

Accepted at ad71fb2. The three one-unit cases recomputed at 120 digits (the truths right; 45 × round(π/180)
is the core's …758): not a defect, since radian trig and →RAD/→DEG are under 003 amendment 1's 8-unit
bar (034 made DEG and GRAD trig correctly rounded); the coming single-input hp Ziv unit will make them
correct, and they repin to exact then. The unit's scope (fn_torad never reads the mode; 35s guide p.4-14),
DEG showing no unit (screen.c), GRAD's 400, the keys (layout/stu32-v0.json) and the quoted values confirmed.

## Repin to 7776c7c (2026-10-07): firmware 044, correct rounding

044 (abacus #4905; soroban #4902, its work/044-vectors.txt N01 to N03) makes radian trig and
→RAD correctly rounded. A02 (RAD 30 SIN) and E01 (45 →RAD) failed alone on their one-unit pins,
as the watch predicted, and are now the oracle's exact values: −0.9880316240928617899877489072944582
and 0.7853981633974483096156608458198757. build/proto/trig01.py has no pins left. The prose's four-place
quotes did not move.
