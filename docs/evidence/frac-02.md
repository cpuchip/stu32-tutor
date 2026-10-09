# frac-02 evidence: adding and subtracting fractions (pre-algebra unit 5)

## Expected values

Oracle: build/proto/frac02.py, in exact fractions, each value also asserted exact at 34 digits (no
accuracy arrow): 1/4 + 3/8 by LCM 8; the tops-and-bottoms slip, 4/12 = 1/3, below 3/8; 2/5 + 1/2 by
LCM 10; 7/8 − 1/4; 3/4 + 1/2 = 1 1/4; exercises 1/2 + 1/8, 3/5 − 1/10 (simplified to 1/2), 3/8 + 3/4 =
1 1/8. The hand-only 1/4 + 1/6 = 5/12 by LCM 12, and over 24 to the same 5/12, asserted. 7 examples
in both entries, displays at FRAC 4095 P.

## Non-author read (2026-10-09)

All values correct. Taken: why a common bottom is a common multiple (cutting pieces multiplies the
bottom), that any works and why the smallest; the examples never needed the LCM (each pair had one
bottom dividing the other), so 1/4 + 1/6 added, by hand since twelfths do not end; ÷ before + on the
line said, so frac-03's left to right is not misapplied; the multipliers shown; "simplify at the end"
in the method; "4 pieces of what size?"; four quarters make a whole.

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): the slip quoted as the
answer; + typed for ÷; RPN taking away in the wrong order; the mixed number misquoted. All red.
