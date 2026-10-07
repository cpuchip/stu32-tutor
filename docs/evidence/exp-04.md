# exp-04 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/exp04.py. XEQ's values (left minus right) are the keys' rounding of the
exact expressions. SOLVE's roots are numeric: each was measured on the core (the script's probe mode
runs the vectors with placeholders and reads the core's answers) and is accepted only within 1E-30 of
the true root, found by Newton's method at 60 digits; the values below are the core's, pinned.

| Vector | What | Value |
|---|---|---|
| Q01 | eˣ = 3x typed | EXP(X)=3×X |
| Q02-Q04 | eˣ − 3x at 0, 1, 2 | 1, e − 3, e² − 6 (1.0000, -0.2817, 1.3891) |
| S01 | SOLVE from 0 and 1 | 0.6190612867359451121523269940209228 (6 units in the 34th digit above the true root) |
| S02 | SOLVE from 1 and 2 | 1.512134551657842473896739678072039 (the true root correctly rounded) |
| T01 | 500 × 1.04ᵀ = 1000, from 10 and 30 | 17.67298768512971317198964813362912 (exp-03's log quotient is …911) |
| E01-E01C | 2ˣ = x + 3 typed; 2ˣ − x − 3 at −3, 0, 3 | 0.125, -2, 2 |
| E02, E03 | SOLVE from −3 and 0; from 0 and 3 | -2.862500371220298824887996366649381, 2.444907554610207051743845256107619 |

Both of eˣ = 3x's roots, and the keys and screens, were the same in 33s, 35s and STU (probed before
the vectors).

## Sources and probes

- eˣ in Equation mode types EXP with its opening bracket and ▶ steps out of it, as ABS in eq-03
  (vector token >); probed, keyrun --sequence, all three modes.
- T is on the 8 key (fn-02).
- A slip caught by the oracle: three of the pinned roots were first written as typed placeholders
  rather than measured values; the probe run replaced them and the 1E-30 assert checks each.

## Non-author read (2026-10-07)

Nine findings, all taken. The largest: the answer said "two sign changes, so two solutions", and the
lesson said eˣ and 3x "cross twice: once in each gap", turning "at least one" into an exact count with
nothing to cap it (an exponential has no degree, as poly-02's polynomials had). Now: a sign change
means at least one crossing, and the cap is the shape: a straight line can cross a curve that bends
one way (eˣ, 2ˣ) at most twice. The "in the end" argument, which did not prove "from 2 on", is gone
with it. Also: "keeps both to 34 digits" was false (S02's guess replaced the first root in X); the
ABS reference now matches eq-03's own words (its opening bracket, ▶ steps out); ln(3x) bracketed and
"no rearranging" limited to the calculator's functions; 500 × 1.04ᵀ = 1000 tied to exp-03 by dividing by
500; "first reaches double"; EQN off and which guess goes where said in the prose.

## Checks

`make check`: 13/13 vectors in 33s, 35s and STU, from a fresh and a used core; 14 keys blocks.
Controls: EXP( typed without ▶, guesses straddling both roots, a sign misread at x = 1; all red.

## Abacus's accuracy read (#4646, 2026-10-07)

Accepted at 7f1d58f (24/24 in 33s, 35s and STU). the roots match Newton; SOLVE's …912 against the true …911 honestly taught; a convex curve meets a
line at most twice; Lambert W right.
