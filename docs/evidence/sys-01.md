# sys-01 evidence: two equations at once

## Expected values (2026-10-07, core d75fc75)

Oracle: build/proto/sys01.py, exact fractions. Every number is a short decimal, so each operation's
34-digit rounding is exact and the core must give these values exactly; it does (17/17 vectors,
26/26 expectations). The oracle also solves each system by Cramer's rule (x = (ce − bf)/(ae − bd),
y = (af − cd)/(ae − bd)) and asserts the lesson's elimination steps against it.

| Vector | What | Value |
|---|---|---|
| C01, C02 | the pair (5, 10): 2x + 3y and x + y | 40, 15 |
| C03, C04 | the pair (8, 7): 2x + 3y and x + y | 37, 15 |
| L01, L02 | elimination: y = 37 − 2 × 15, then x = 15 − y | 7, 8 |
| F01, F02 | the fruit: y = (6.5 − 0.75 × 6) ÷ (1.25 − 0.75), then x = 6 − y | 4, 2 |
| P01 | parallel lines: 0 = 5 − 3 | 2 |
| P02 | one line twice: 0 = 6 − 2 × 3 | 0 |
| E01..E01C | 3x + 2y = 16, x + y = 6: x, y, and the check 3x + 2y | 4, 2, 16 |
| E02 | 2x − y = 1, 4x − 2y = 5: 0 = 5 − 2 × 1 | 3 |
| E03, E03B | the coins: y, then x | 15, 25 |
| E04 | 3x − y = 2, 6x − 2y = 4: 0 = 4 − 2 × 2 | 0 |

The slopes quoted in "No solution, or every solution" (−1 and −2/3, and the exercise lines'
y = 2x − 1, y = 2x − 2.5, y = 3x − 2) are asserted in the oracle where they decide something (the
tickets' slopes differ) and checked by hand otherwise.

## Sources and probes

- STO and RCL with the letters X (on 6) and Y (on 1), as rpn-02; the layout from abacus
  layout/stu32-v0.json (row 5: X on 6; row 6: Y on 1).
- The built-in 2×2 solver was probed for unit 8 and is not used here: at d75fc75 its key path stops
  at SOLVE _ and takes a typed coefficient as a letter (abacus #4778; ruled into firmware unit 043,
  #4780). The solver lesson (sys-02) waits for 043.

## Non-author read (2026-10-07)

No arithmetic errors; every keys block matches its vector and every quoted display its value. The
findings, all taken:
- The tickets made a child's ticket (8) dearer than an adult's (7): swapped (37, adult 8, child 7).
- The variable X and the screen's X line were never told apart ("Keep it in X" read as doing
  nothing): the eq-01 convention is stated in "Before you start", and the text says "store it in the
  variable X".
- "Two lines that are not parallel cross at exactly one point" missed the same line twice: "two
  different lines with different slopes". "Each equation is a line": "the graph of each equation in
  these systems is a line".
- Rewriting ax + by = c as y = mx + b was never taught: shown for both ticket equations, with the
  slopes −1 and −2/3, which is also why the tickets have one answer.
- Dividing both sides, and taking one equation from another, were used but only multiplying was
  justified: all three stated before elimination.
- Exercise 1 eliminates y, which the lesson never did: "either unknown can be eliminated; pick the one
  whose numbers make it easiest", and the answer says which.
- "Parallel" was used before it was defined: defined where first used.
- The fruit's y written without parentheses read wrongly under num-01's order: parenthesised.
- P01's 2 could be read as a value of x or y: said plainly that it is what is left on the right.
- Exercise 2's keys gave −3 while the prose said 0 = 3: the keys now work 5 − 2 × 1, as the prose.
- No exercise had every pair a solution: exercise 4 added (one line twice).
- 5 cents as 0.05 dollars said; "each a 5-cent or a 10-cent coin"; "or endlessly many" in the opening;
  "a pair among them"; "Each section's examples are one chain" (false) replaced by the house line.
- `requires:` gained mult-before-add, fraction-bar and falling-flat.

## Checks

`make check`: 17/17 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (4): the pair quoted as fitting both, elimination the wrong way round, the
fruit's bottom reversed, no solution read off 0 = 0; all red.

## Abacus's accuracy read (#4793, 2026-10-07)

Accepted at f5dc8a0. Every value rechecked by hand. (1) multiplying both sides by any number, dividing by
a non-zero one, and equals taken from equals: true. (2) the slopes −1 and −2/3, distinct, meet once
(vertical lines are not in play). (3) same slope, different intercepts: parallel. (4) 0 = 0 the same
line, 0 = c (c not 0) none, including when both unknowns go at once.
