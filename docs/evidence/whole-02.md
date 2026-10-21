# whole-02 evidence: multiplying and dividing (pre-algebra unit 1)

## The core (be3617e; probed 2026-10-09, build/proto/p1_probe*.sh)

- INT÷ is gold and Rmdr blue on the ÷ key (abacus layout/stu32-v0.json, row 4 key 4); both are
  floored (firmware work/017, rule 5). In RPN, `59 ENTER 9 GOLD INT÷` gives 6 and `BLUE Rmdr` 5.
- On the algebraic line they type functions: `IDIV(59,9)` and `RMDR(59,9)`, the comma gold on the
  point key (row 7 key 2); ▶ closes the bracket (optional at the line's end). Vector tokens IDIV,
  RMDR and `,`.

## Expected values

Oracle: build/proto/whole02.py. Asserted by hand: 46 × 23 by partial products, 46 × 3's column and
carry, 46 × 2 tens; divmod of 59 by 9 with its check; long division of 1000 by 7 step by step (10, 30,
20, and the remainders 3, 2, 6); the exercises (37 × 15, 37 × 5's carry, 100 by 12, 365 by 7 with its
check). 11 examples in both entries (22 vectors), 11 display vectors.

## Non-author read (2026-10-09)

Every value checked correct. Taken: 58 ÷ 9 = 6.4444 was a trap, its remainder 4 looking like the
decimal's digits (now 59: 6.5556, remainder 5, and the decimal said not to be the remainder); "a 0 for
the tens" was wrong (now 46 × 2 tens = 92 tens = 920); the hand steps were skipped under "easy" (now
46 × 3 and 37 × 5 by column, "easy" dropped); the divisor defined, and which number comes before the
comma; long division's "bring down", "holds", and why a remainder becomes tens explained, with where
each answer digit is written; answer 3 starts as the lesson does and is checked; what Rmdr types; the
wording of where both keys are printed made to match.

## Checks

make check at be3617e: 11/11 vectors in each entry, the student run in order in each. Controls (4):
INT÷ without its gold shift; RPN's Rmdr with the divisor first; the comma left out; the remainder
misquoted. All red.

## Dividing in parts (2026-10-21, sense-making section 6, abacus #9439)

Two moves before long division:
- **Parts:** 117 ÷ 9 as 90 ÷ 9 + 27 ÷ 9 = 10 + 3 = 13 (P01). 117 is said to be a new number, bigger than the 59
  above, and the split is chosen by tens that 9 goes into (90, not 100).
- **Halving both:** 156 ÷ 12 = 78 ÷ 6 = 39 ÷ 3 = 13 (P02 39 ÷ 3, P03 156 ÷ 12). It's taught on its own terms
  (half the rolls in boxes half the size fill the same number of boxes), not through frac-01, which is unit 5 to
  this lesson's unit 1. It's said to work only while both numbers are even; 39 is odd, so it stops there.

**The twins:**
- DP1T1 is 112 ÷ 8 in parts, 80 ÷ 8 + 32 ÷ 8 = 14; its slip is the first part only, 10.
- DP3T1 is 132 ÷ 12 by halving, 66 ÷ 6 = 33 ÷ 3 = 11; its slips are 66 ÷ 12 = 5.5 (only the 132 halved) and
  132 ÷ 6 = 22 (only the 12 halved).

DP1T1 began as P1T1, which graph.py refused because expr-01 already has it.

**Oracle:** exact arithmetic, asserted first (scratchpad sense_vectors.py):
- 90 + 27 = 117 = 9 × 13, and 100 isn't a multiple of 9;
- 156/12 = 78/6 = 39/3 = 13, with 156, 12, 78 and 6 even and 39 odd;
- 80/8 + 32/8 = 14 = 112/8;
- 132/12 = 66/6 = 33/3 = 11, 66/12 = 11/2 and 132/6 = 22.

3 new examples in both entries (6 vectors) and 3 display vectors; the twins' 7 rows in both entries (14).

**Checks:** First run (all 56): red, 54/56, on three of my own faults: a why block naming 78, which P03 does not show; the twin CV1T1 naming K01 with K02 and K03 between them (it now names K03); a why block after C03 naming 20 and 30. All three fixed. Rerun at 6e51b56 on expr-02 and whole-02: make check 2/2, make controls rc 0. Three planted faults in copies under build/plant, each red for its own reason: P01 quoted 14.0000 (prose against display vector and device), CV1T1A expecting 4 (the core gave 3), and C03's RPN keys with 5 + for 5 − (keys against vector). The other 54 were green on the first run, and only these two lessons and TOPICS changed after it; graph.py passed on all 55.
