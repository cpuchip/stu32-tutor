# poly-01 evidence

## Expected values (2026-10-07, core 25dca53)

The oracle is build/proto/poly01.py: p(x) = 2x³ - 3x² + 4x - 5 and r(x) = x³ - 2x + 1 in exact
fractions, both directly and by Horner, asserted equal before the vectors run.

| Vector | What | Exact |
|---|---|---|
| H01A | 4 ENTER ENTER ENTER 2 | X 2 being typed, Y Z T 4 |
| H01C | × 3: the lift | X 3 being typed, Y 8, Z 4, T 4 (a 4 off the top) |
| H01B | − | X 5, Y Z T 4 (T copied down) |
| H01 | × 4 + × 5 − | p(4) = 91 |
| H02 | p(2) | 7 |
| P01A, P01 | program P | 15 lines, P015 |
| P02, P03 | p(1.5), p(-1) | 1, -14 |
| E01 | r(2) with the 0 coefficient | 5 |
| E02A, E02 | program N, r(0.5) | N015; 0.125 |

All exact on the core at 25dca53, in 33s and 35s modes.

## Sources and probes

- The stack: rpn-01's "T copies down" and num-01's "falls off the top"; the narration is pinned by
  the stopping points H01A, H01C (the lift) and H01B (the drop).
- Letters (keymap.c LETTER table): P is letter 15, on the E key; N is letter 13, on the x↔y key.
  Neither labels a program in an earlier lesson (F G H K, Q T U, R S): a student's calculator keeps
  programs (fn-01), and an existing label is refused with DUPLICAT.LBL.
- A first-draft choice changed before any reader saw it: p(3) made the partial result 2x - 3 equal
  to x (3), the confusion lin-01's reader found; the worked example is p(4) (partials 5 and 24).

## Non-author read (2026-10-07)

Nine findings, all taken. The largest: the narration said the supply of x never runs out because
"each step has dropped one 4 and T has copied one down", but the 4 is lost when a coefficient is
typed (the lift pushes T's 4 off the top) and won back by the drop; a stopping point (H01C) now
shows the lift. Also: linear functions are degree 1 or 0 (a flat line), not just 1; the constant
term and the degree defined properly; the factoring shown in two steps, with "parentheses" as the
earlier lessons say; "add −3" said to be subtracting 3; the chain sentence made exact; "it" made
unambiguous; the second exercise now writes a program (N), and the first says why the 1 and the 0
are keyed; p(1.5) given its check; "you start a program with x in X".

## Checks

`make check`: 12/12 vectors in 33s and 35s, from a fresh and a used core; 13 keys blocks; 11
quotes. Controls: the stack filled with two ENTERs, a coefficient's sign lost, the missing power's
0 left out; all red.

## Abacus's accuracy read (#4478, 2026-10-07)

Accepted at a8957a6 with one fix, made: "each coefficient you type pushes one 4 off the top" is
true only after the first, which replaced the copy ENTER left (H01A); now "the first coefficient
only replaced the copy ENTER left in X; each later coefficient...". The degree definition and
"degree 1 (or 0, for a flat line)" confirmed (y = 0 has no degree by convention; not added). The
supply argument right as amended. The 036b plan for keyrun confirmed, its control (auto-ENTER off
turns the 35s pass red) due when 036b lands.
