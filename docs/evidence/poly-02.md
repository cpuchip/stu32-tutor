# poly-02 evidence

## Expected values (2026-10-07, core 7c96617)

The oracle is build/proto/poly02.py: c(x) = x³ - 6x² + 11x - 6 = (x - 1)(x - 2)(x - 3) and
d(x) = x³ - 7x + 6 = (x - 1)(x - 2)(x + 3), their values at the bracketing points in exact
fractions, and each root asserted a zero before the vectors run.

| Vector | What | Exact |
|---|---|---|
| R01 | c typed as an expression | X^3-6×X^2+11×X-6 |
| R02-R05 | c(0), c(1.5), c(2.5), c(4) | -6, 0.375, -0.375, 6 |
| S01, S02 | SOLVE from 0 and 1.5; from 1.5 and 2.5 | 1, 2 (exact) |
| S03 | SOLVE from 2.5 and 4 | 3.000000000000000000000000000000003 |
| N01 | x² + 1 | NO ROOT FND |
| E01-E01E | d(x) = x³ - 3x + 1 typed; d(-2) .. d(2) | -1, 3, 1, -1, 3 |
| E02 | SOLVE from -2 and -1 | -1.879385241571816768108218554649463 (all 34 digits right) |
| E03 | SOLVE from 0 and 1 | 0.3472963553338606977034332535386298 (2 in the last digit off: ...296 rounded) |
| E04 | SOLVE from 1 and 2 | 1.532088886237956070404785301110833 (all 34 digits right) |

S03 is SOLVE's numeric root, 3E-33 above 3. The oracle accepts a core root only within 1E-30 of the
true one and the vector pins the core's value (measured at 7c96617): a repin that changes SOLVE's
search may move it, and the vector will say so.

## Sources and probes

- Probed first (keyrun --sequence, 7c96617): SOLVE on an expression with no = finds where it is 0;
  XEQ on it gives its value; x² + 1 gives NO ROOT FND, and after C, X holds SOLVE's last try (a
  number near 1E-25), which the lesson does not quote (it is the search's, not the maths').
- The guesses: the variable's value and the X line (eq-03); XEQ leaves Equation mode, so STO works
  after it (eq-01).

The exercise's true roots (2cos 40°, 2cos 80°, 2cos 160°) by Newton's method at 60 digits in the
oracle; each core root asserted within 1E-30 of its true value, and pinned.

## Non-author read (2026-10-07)

No mathematical errors; eight findings, all taken. The largest: the exercise handed over the
bracketing points, so it never practised deciding where to look; it is now x³ - 3x + 1, whose roots
are not whole numbers, with only "the whole numbers from -2 to 2" given, and the answer reasons from
the count. Also: a root can touch the axis without a sign change, and a gap can hide two ((x - 2)²);
"at most three roots" given its reason through the factors; "usually" restored from eq-03 for
which root SOLVE finds; the 34th-digit remark tied to rpn-03's 34 digits and worded so it reads one
way, with "each closer than the last" softened; the expression without = tied to fn-02; "real"
defined; the missing x² term noted. A first draft of the exercise used x³ - 7x + 6, dropped because
its roots are whole numbers that the value table hits exactly.

## Checks

`make check`: 18/18 vectors in 33s and 35s, from a fresh and a used core; 19 keys blocks; 17
quotes. Controls: guesses straddling two roots, a sign misread in the table, x² + 1 quoted as having
a root; all red.

## Abacus's accuracy read (#4486, 2026-10-07)

Accepted at e244559. Values confirmed, and the exercise's roots independently with mpmath at 60
digits (0.3472...6295920 rounds to ...6296; the core's ...6298 is 2 units off, as the evidence says).
(1) An expression equated to zero: the 33s guide p.7-1 and p.7-5. (2) The factor theorem, "at most
n". (3), (4) Honest hedges about a numeric search. (5) NO ROOT FND: the 33s guide p.F-3 and the 35s
guide p.F-4, read from the rendered pages.
