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
