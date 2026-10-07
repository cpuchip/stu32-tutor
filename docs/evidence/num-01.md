# num-01 evidence

## Expected values (2026-10-06)

Recomputed with Python integers and fractions, independently of the core:

| Vector | Computation | Exact |
|---|---|---|
| N01 | 3 + 4 x 5 | 23 |
| N01A | 3 ENTER 4 ENTER 5, before x | X 5, Y 4, Z 3 |
| N02 | (6 + 2) / 4 | 2 |
| N03 | 2 x 3^2 | 18 |
| N04 | (2 x 3)^2 | 36 |
| N05 | (10 - 4) / (5 - 2) | 2 |
| N05A | 10 ENTER 4 - 5 ENTER 2, before the second - | X 2, Y 5, Z 6 |
| N06 | -(3^2) | -9 |
| N07 | (-3)^2 | 9 |
| N08 | 2 + 3 x (4 + 1)^2, left to right | X 77, Y 2 (T's 2 copied down) |
| N09 | the same, inside out | 77 |
| E01 | 5 + 6 x 2 | 17 |
| E02 | (9 - 3)^2 / 4 | 9 |
| E03 | 4 x 3^2 - 10 | 26 |

Displays at FIX 4: 23.0000, -9.0000, 9.0000, 77.0000.

## Self-audit before the non-author read

Tracing every stack sentence by hand found two wrong placements before any reader saw them: the
draft said the 3 in N01 and the 6 in N05 waited in Y, but both are in Z while the next pair is
typed (the same error rpn-01's reader caught in its S07). Both sentences were corrected and then
backed by vectors that stop mid-example (N01A, N05A), so the narration is checked by the core and
not only by the trace. The draft's comparison with calculators that have an equals key was cut
(a claim about other machines, and a posture the teaching agent's check warns against), and an
antithesis ("23, not 35") was rewritten.

## Non-author read (2026-10-06)

The reader traced the stack after every key and found every value and every stack sentence
right after the self-audit's fixes. Seven findings about what the lesson claimed or assumed, all
taken, each new claim with a vector:

- **"Inside out is the safer habit" overreached:** it holds for + and x only. For 20 - 3 x 4
  inside out, the 20 lands in X; the lesson now teaches x<>y before the - (N10: 8), shows the
  wrong way (N10A: -8, no error), and practises it (E04: 50 - 2 x 3^2 = 32).
- **N08's reason was wrong:** the 2 reaches Y by dropping from T to Z to Y, not by T's copying;
  and "as long as they fit" now shows what a fifth level does (N08B: ENTER after the 1 pushes the 2
  off, leaving X 1, Y 1, Z 4, T 3).
- +/- on a finished result (N06) was used before it was said; now said.
- The order statement lacked left to right within a rank and where a leading minus sits; added.
  The reader's aside about spreadsheets reading -3^2 as 9 was not verified this session, so it
  is not in the lesson.
- N05's answer and N05A's typed digit were both 2; N05 is now (12 - 4) / (5 - 3) = 4 (N05A: X 3,
  Y 5, Z 8).
- "the same two keys" was three presses (GOLD x^2); now "operations". N01 now also shows the
  inside-out way (N01B: 23).

## Checks

`make check` at 867ddd5: 19/19 vectors and 27/27 expectations in 33s and 35s, from a fresh and a
used core; 20 keys blocks, 19 of 19 vectors shown, pressed in both modes; 5 displays quoted.

## Abacus's accuracy read (#4286, 2026-10-06)

Arithmetic right throughout; N01A and N05A back their narration. Three fixes, all taken. N08's
narration broke the stopping-point rule: it now has N08S (after the 1: X 1, Y 4, Z 3, T 2) and N08T
(before the last +: X 75, Y 2), both probed by abacus and passing here. N08B's "the + would have
nothing to add it to" was wrong: carried on, the last + adds a leftover 3 and gives 19 with no error
(N08C, now taught as the silent wrong answer). The leading-minus reason ("counts as a subtraction")
broke on 4 x -3 and is now the bare convention, matching the 35s's precedence (p.6-14, per
abacus). Applying the rule to the rest of the lesson found one more unbacked position, N10's "the
20 in X and the 12 in Y", now N10S. The spreadsheet aside stays out (abacus: Excel's page lists
negation above ^ but gives no -3^2 example, so "9" would be an inference).
