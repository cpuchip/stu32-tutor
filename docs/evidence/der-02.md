# der-02 evidence: the power rule

Unit 11's second lesson, as planned in the syllabus (abacus #5263, #5271). The rule is shown by hand
from the averages for x, x² and x³. Its general form, for n = 1, 2, 3 and on, follows from a counting
argument: of the n brackets of (a + h), a term with exactly one h takes it from one of n, so those terms
are n·aⁿ⁻¹h. Sums and constant multiples come
from the averages, and a polynomial's derivative is built term by term. In every mode an average
checks the rule; in STU, so does D/DX.

## What the core does (probed 2026-10-08, core c7ab388)

- **Casimir's D/DX** (build/proto/der_probe.sh):

  | Input | D/DX |
  |---|---|
  | X^3-4×X+1 | 3×X^2-4 |
  | 1÷X | -1÷X^2 |
  | X^2+3×X | 2×X+3 |
  | 7 | 0 |

- **XEQ on an equation leaves Equation mode.** The first draft turned it off again after B02's XEQ
  and so turned it back on; the student run caught that, since R01's digits typed into a new
  equation, though B03's own vector passed. B03 came out, and the prose says XEQ leaves Equation
  mode.
- **D/DX with no XEQ after it leaves Equation mode on.** R03 and E02C turn it off, as der-01's E02C
  does, and a control removes R03.
- **The 1/x key's vector token** is INV (as prob-01b's M01), not 1/X.

## Expected values

Oracle: build/proto/der02.py, modelling the keys. The hand algebra is asserted in exact fractions:
- the averages for x, x², x³ and a constant, at several a and h;
- (a + h)ⁿ's first two terms plus a remainder in h² or more, for n = 1 to 8;
- the count of tuples with exactly one h over n brackets is n, for n = 1 to 8;
- (a² + 2ah + h²)(a + h) written out term by term;
- n = −1 by algebra: (1/(a + h) − 1/a) ÷ h = −1/(a(a + h)).

| Vector | What | Value |
|---|---|---|
| P01 | (f(2.001) − 1) ÷ 0.001, f(x) = x³ − 4x + 1 | 8.006001 (FIX 4: 8.0060) |
| B02 | XEQ of 3×X^2-4 at 2 | 8 |
| R01 | (1/2.001 − 0.5) ÷ 0.001 | −0.24987506… (exactly −1/(2 × 2.001) before rounding; FIX 4: −0.2499) |
| E01 | (5 × 1.001⁴ − 5) ÷ 0.001 | 20.030020005 |
| E02 | (1.001² + 3 × 1.001 − 4) ÷ 0.001 | 5.001 |

11 vectors, 5 display vectors.

## Checks

**`make check`:**
- 33s and 35s: 4/4 vectors.
- STU: 11/11, the D/DX blocks STU-only.
- Each mode worked through in order.

**Controls (6), all red:**
- the cube's x↔y left out;
- an average quoted as exactly 8;
- Casimir's text misquoted;
- 1/x's average with + for −;
- exercise 2 with no ENTER;
- Equation mode left on after D/DX of 1/x.

## Non-author read (2026-10-08)

Every stack trace, expansion and value checked correct. Taken:
- **"For any whole number n" let in n = 0,** where n·xⁿ⁻¹ is 0·x⁻¹. Now n = 1, 2, 3 and on; constants
  keep their own rule; x⁰ = 1 is said where the x row needs it.
- **The coefficient n had no reason;** the general case pointed at an unproved binomial theorem. Now
  the counting argument (n brackets; exactly one h, n ways), within reach at this level.
- **The sum and multiple rules claimed to come "straight from the averages"** without showing them.
  Now each shows its average, states the multiple rule in general, and says a difference is a sum
  with a multiple of −1 (which "−4x gives −4" needed).
- **"Most derivatives can be written down at once"** overstated: now "any polynomial's".
- **P01's stack wording:** "that copy" pointed at the wrong copy, and why two copies are needed was
  not said. Now yˣ uses the copy in Y and the last one waits for 4 ×; the + 1 then − 1 is explained.
- **Exercise 2's second ENTER was unneeded:** x² uses only X. Now one ENTER, with the contrast to yˣ
  said. The vector and the control changed with it; 5.001 is unchanged.
- **The 1/x average** now says it divides by 0.001. n = −1 is proved in the lesson by algebra, over a
  common bottom, with x = 0 excluded, so "looks right" became "the algebra proves it".
- **The (a + h)³ multiplication** is written out.
