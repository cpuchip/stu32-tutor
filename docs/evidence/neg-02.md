# neg-02 evidence: multiplying and dividing negatives (pre-algebra unit 4)

## The core (be3617e)

INT÷ and Rmdr floor (firmware work/017; abacus #5444): IDIV(−7,2) = −4 and RMDR(−7,2) = 1, measured on
the line and the stack; IDIV(−10,3) = −4, RMDR 2.

## Expected values

Oracle: build/proto/neg02.py: 3 × (−4), (−3) × (−4), the pattern from 3 down to −3, and its reason
(taking away −4 adds 4); (−12) ÷ 4 and ÷ (−4) with their multiplication questions; the floor of −7 ÷ 2
and its check; exercises (−6) × 5, (−8) × (−3), (−20) ÷ (−5), the floor of −10 ÷ 3 with its remainder,
and 15 ÷ (−3). 13 examples in both entries.

## Non-author read (2026-10-09)

All values correct. Taken: −4 called "the whole number below −3.5", though neg-01 defines −4 as an
integer, not a whole number (now "integer"); the pattern was offered as the reason, but a pattern is
evidence (now the reason: each step takes away one more −4, and taking away −4 adds 4); a negative
times a positive (exercise 1) needed order-doesn't-matter; the pond story finished, both ways; "so"
in the division rule made a step; the remainder pictured on the number line (the multiple at or left
of the number), "positive divisor" explained, the long INT÷ sentence split; "neither is wrong" about
truncating calculators; "size" defined; a floor exercise and a positive ÷ negative.

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): (−)×(−) quoted negative;
the floored quotient quoted as chopped (−3); the divisor's sign left off; RPN's Rmdr of 7, not −7. All
red.
