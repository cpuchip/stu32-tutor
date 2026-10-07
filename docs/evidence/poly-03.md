# poly-03 evidence

## Expected values (2026-10-07, core 7c96617)

The oracle is build/proto/poly03.py: each quadratic's discriminant and roots in exact fractions,
asserted before the vectors run.

| Vector | What | Exact |
|---|---|---|
| Q01 | x² - 4x + 3: a, b, c stored | A 1, B -4, C 3 |
| Q02A | stopped after RCL A | X 1, Y 4, Z 16 |
| Q02 | b² - 4ac, kept in D | 4 |
| Q03, Q04 | (-b ± √D) / 2a | 3, 1 |
| Z01, Z02 | x² - 6x + 9: discriminant, root | 0, 3 |
| N01-N03 | x² + 2x + 5: discriminant, its root, C | -16, SQRT(NEG), -16 |
| E01-E01C | 2x² + 3x - 2: discriminant, roots | 25, 0.5, -2 |

All exact on the core at 7c96617, in 33s and 35s modes.

## Sources and probes

- Letters (keymap.c LETTER table): A on √x, B on eˣ, C on LN, D on yˣ (letters 0-3, keys 6-9).
- x² gold above √x (num-01); SQRT(NEG) as fn-03 quoted it (abacus #4415, appendix F p.F-4).
- The discriminant's stack: RCL B, x² gives b²; 4 lifts it to Y; RCL A lifts it to Z; × drops it
  to Y (4a in X); RCL C lifts it to Z; × drops it to Y (4ac in X); − gives b² - 4ac. Pinned by the
  stopping point Q02A (X 1, Y 4, Z 16) and Q02's result.

## Non-author read (2026-10-07)

Eight findings (and a ninth that the exercise matches); all taken. The largest: the first draft said b² "waits in Y until the − at the
end", but it rides up to Z twice (at RCL A and RCL C) and comes back down after each ×; a stopping
point (Q02A) now shows it, and the narration follows it. Also: the discriminant decides how many
*real* roots; the formula written ÷ (2a), with 2a said to be 2 × a; "its roots" named as x² + 2x + 5's;
a zero discriminant gives the same root twice, a double root; the root keys narrated (−b + √D waits
in Y while 2a is built); a reminder that after RCL D the √x key is the square root, not the letter A;
the SQRT(NEG) cleared with C as in fn-03 (N03, X -16).

## Checks

`make check`: 13/13 vectors in 33s and 35s, from a fresh and a used core; 14 keys blocks; 13
quotes. Controls: b stored without its sign, dividing by 2 instead of 2a, the negative
discriminant's refusal misquoted; all red.
