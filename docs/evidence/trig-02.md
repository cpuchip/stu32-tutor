# trig-02 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/trig02.py with dmath.py (80 digits, self-checked; acos added, checked
against acos ½ = π/3): trig of degrees and the inverses in degrees, each key rounded once.

| Vector | What | FIX 4 |
|---|---|---|
| L01, L02 | 5 sin 70°, 5 cos 70° | 4.6985, 1.7101 |
| T01 | 12 tan 35° | 8.4025 |
| A01-A03 | ASIN 0.6, ACOS 0.8, ATAN 0.75 | 36.8699 each (36.86989764584402129685561255909341, all three equal) |
| E01 | ATAN(1/12) | 4.7636 |
| E02 | ACOS(0.28) | 73.7398 (core …681; see below) |
| E02B | 2.5 sin of that | 2.4000 |

ACOS 0.28 in degrees is 1.13 units off the correctly rounded truth (…682), confirmed by abacus at 120
digits (#4667): inside the inverse trig's present 8-unit bar, and named for the coming single-input hp
Ziv unit. Pinned within 2 units; repin to exact when that unit lands.

## Sources and probes

- ASIN, ACOS, ATAN gold above SIN, COS, TAN (keymap.c keys 15-17).
- The setup is trig-01's (DEG); every vector begins MODE33 FIX4 DEG.

## Non-author read (2026-10-07)

No wrong mathematics; twelve findings, all taken. The largest: no picture, when every setup turns on
telling opposite from adjacent; a labelled right triangle now stands under the definitions. Also: why
the ratios depend only on the angle (two right triangles sharing A share all three angles, the angles
adding to 180, so one is a scaled copy); the tree's height measured from eye level, with the eye height
to add; the ladder's adjacent side as the ground, not its foot; how SIN uses the stack (X alone, the 5
waiting in Y) and the order of "SIN 2.5 ×"; the chain wording; "work them out"; Pythagoras' rule named
for the 3-4-5 triangle (no earlier lesson has it); the ramp's 12 m "measured along the ground"; sin⁻¹
notation and the inverses' range, with a promise that trig-03 shows a sine belonging to more than one
angle; multiplying both sides by 5 said.

## Checks

`make check`: 9/9 vectors in 33s, 35s and STU, from a fresh and a used core; 10 keys blocks.
Controls: the ladder's height with cos, an angle from SIN instead of ASIN, the tree's height from the
wrong ratio; all red.

## Abacus's accuracy read (#4679, 2026-10-07)

Accepted at 132660e. Every quoted value checked against mpmath; E02B's 2.4000 is exact, since
sin(acos 0.28) = √(1 − 0.0784) = 0.96. (1) AA similarity; (2) the converse of Pythagoras, "c the
longest" the right condition; (3) the inverses' ranges for ratios in (0, 1), fine as a promise for
trig-03; (4) a function leaves stack lift on.
