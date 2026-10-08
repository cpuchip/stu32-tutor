# seq-01 evidence: sequences and sums

## Expected values (2026-10-07, core c7ab388)

Oracle: build/proto/seq01.py, exact integers and fractions; each formula is asserted against the
terms added one by one. 12/12 vectors, and 9/9 display vectors (FIX 4 with the thousands comma).

| Vector | What | Value |
|---|---|---|
| A01 | row 15: 20 + 14 × 2 | 48 |
| A02 | 15 rows: 15 × (20 + 48) ÷ 2 | 510 (= the 15 terms added) |
| G01 | 3, 6, 12, …: the 10th, 3 × 2⁹ | 1536 |
| G02 | the first 10: 3 × (2¹⁰ − 1) ÷ (2 − 1) | 3069 (= the 10 terms added) |
| P01A..P02 | program Z, loop W: Σ(18 + 2k), k = 1..15 | 510 in X and T; 5 then 17 lines |
| E01, E01B | 7, 11, 15, …: the 30th; the first 30 | 123; 1950 |
| E02 | 2 × 0.75⁵ (the 5th bounce) | 0.474609375, shown 0.4746 |
| E03 | 2¹⁰ − 1 | 1023 |

## Sources and probes

- The loop keys and the counter format are fn-02's (ISG, GTO, IP in the POW menu); STO + is rpn-02's.
- Labels Z and W: no earlier lesson uses them (every LBL: in the lessons' vectors is F, G, H, K, N, P, Q,
  R, S, T or U), so a learner working on from the earlier lessons meets no DUPLICAT.LBL.
- W012 RTN, the loop's last line, is checked on the device by the student run.

## Non-author read (2026-10-07)

No wrong number; every block matched its vector, and the loop runs k = 1 to 15 as said. Taken:
- The geometric sum's division by r − 1 was never seen (the example has r − 1 = 1): rS − S = (r − 1)S
  is now said, with the condition r ≠ 1 (and r = 1 the sum n times the first).
- "leaving 3072 − 3, and S = 3 × (2¹⁰ − 1)" skipped 3072 = 3 × 2¹⁰: said.
- 18 + 2k appeared from nowhere: derived from 20 + (k − 1) × 2.
- The nth term's n − 1 against exp-01's a × bⁿ after n steps: said, since it is exercise 2's trap.
- Exercise 2: by the lesson's own rule a learner takes 2 as the first term and gets 0.63; the answer now
  takes the first bounce, 1.5, as the first term, and shows 1.5 × 0.75⁴ = 2 × 0.75⁵.
- No checkpoint for the 17-line program: W012 RTN quoted, with what to do if it differs.
- "needs no formula" overstated (the term is a formula): "no sum formula".
- "GTO goes back to W until the count passes 15" made GTO decide: ISG's skip ends the loop, as in fn-02.
- E01B typed 123 again after "carrying on": it now uses the 123 in X.
- Wording: "n times (the first term plus the last)"; "the two lines", not rows; "is a geometric
  sequence"; "multiplied by r once for each of those steps"; "each term of S doubled is the term after
  it"; "the first n terms"; "the variable T (on 8)", "I (on R↓)"; the counter, not the total, is
  fn-02's.
- Not taken: an exercise on the loop. Changing the program needs fn-01's line editing and a long chain,
  and the loop is here as a check on the formula, not the lesson's point; the next lesson that sums
  with a program can exercise it.

## Checks

`make check`: 12/12 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (3): the nth term with n steps, the geometric sum quoted as the next term,
the loop's row as 20 + 2k; all red.

## Abacus's accuracy read (#4961, 2026-10-07)

Accepted at 789ac73, every value recomputed in exact fractions (2 × 0.75⁵ = 243/512 = 1.5 × 0.75⁴). (1) the
pairing, (2) (r − 1)S = a(rⁿ − 1) with r = 1 handled, (3) the n − 1 against exp-01, (4) exercise 2's first
term: true.
