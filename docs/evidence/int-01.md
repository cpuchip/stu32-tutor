# int-01 evidence: area under a curve

## Expected values (2026-10-07, core c7ab388)

Oracle: build/proto/int01.py, exact fractions. The rectangle sums are exact (each term a short decimal),
so the core must give them exactly; it does. The built-in integral is numeric: x² from 0 to 3 comes out
exactly 9 with an uncertainty of 3 × 10⁻⁴ at FIX 4 (and 3 × 10⁻⁸ when run at FIX 8, probed), while
3x² from 0 to 2 comes out 8 + 10⁻³³ and x from −2 to 1 near −1.5, so those vectors assert the exact
value within 10⁻³⁰. 11/11 vectors, 13 expectations; 5/5 display vectors.

| Vector | What | Value (shown) |
|---|---|---|
| P01A, P01 | program A with loop B, 26 lines, from GTO . . | B017 RTN |
| A01..A03 | n = 3, 30, 300 right-end rectangles under x² on [0, 3] | 14, 9.455, 9.04505 |
| I01..I01C | x² typed; ∫ from 0 to 3 in X; the uncertainty brought down | X^2; ∫=9.0000; 0.0003 |
| S01 | ∫ of x from −1 to 1 | ∫=0.0000 |
| E01 | ∫ of 3x² from 0 to 2 | ∫=8.0000 (8 within 10⁻³⁰) |
| E02 | ∫ of x from −2 to 1 | ∫=-1.5000 (−1.5 within 10⁻³⁰) |

## Sources and probes

- ∫ is gold above 8 (keymap: a prompt for a variable, "∫FN d _"); the lower end in Y, the upper in X;
  the result an ∫= view with the uncertainty in Y; the same in 33s, 35s and STU mode (probed).
- Labels A and B: no other lesson's vectors use them.

## Non-author read (2026-10-07)

Program A traced by hand for n = 3 (14) and every value matched. Taken:
- "the limit is the area, called the integral" against signed area later: the integral is the limit of
  the sums of height × width, the area only when the curve stays above the axis; the limit's kind (the
  number of strips growing) said.
- "14 is too much" needed x² rising on [0, 3]; "the thinner, the closer" made "for a curve like this
  one"; "close in on 9" made "seem to", with ∫ confirming.
- "The calculator can find that limit" made "estimate the integral"; the ∫ paragraph's contradictions
  (good to the places shown, yet 0.0003 out, yet exactly 9): Y is the calculator's cautious bound, not
  the error, and the true error can be far smaller; the bound shown on screen (I01C); "run ∫ again" at
  FIX 8.
- Why signed area: rectangles below the axis have negative height. "The two triangles cancel" now says
  the region's area is 1 while the integral is 0; "a mirror image of the same size".
- B017 checks B's lines only (17, from LBL B to RTN), not A's first nine: said.
- The counter: n whole from 1 to 999, and n = 30 written 1.030.
- GTO . .'s reason; why Equation mode goes off before typing the ends; "limit" as the ends, a second
  meaning, said.
- The exercise repeated the keys: a second one on signed area against area (−1.5 against 2.5).
- requires: times-matters, solve, solve-prompts, swap-roll, fix added; arithmetic-sum dropped.
- Not taken: an exercise on program A for another curve (A is written for x² on [0, 3]; a general sum
  program is a later lesson's).

## Checks

`make check`: 11/11 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (3): the strips' heights at their left ends, three rectangles quoted as the
area, the integral's ends the wrong way round; all red.
