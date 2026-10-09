# expr-01 evidence: letters for numbers (pre-algebra unit 2)

## The core (be3617e; probed 2026-10-09, build/proto/p2_probe.sh)

On the algebraic line, `4 STO N` stores 4 (STO with a line typed evaluates it first, firmware 029 rule
8); `3 × RCL N + 5 ENTER` writes the line `3×N+5` and gives 17. In RPN, `3 ENTER RCL N × 5 +` gives 17.
The letters: N on x↔y, A on √x, X on 6 (abacus layout/stu32-v0.json); after STO or RCL the next key
means only its letter (rpn-02's wording).

## Expected values

Oracle: build/proto/expr01.py: 7 × 12; 3n + 5 at 4 and 10, multiplying first; the exercises 2a + 9 at
6, 3n + 2 at 15, a × a − a at 5. 11 examples in both entries, 11 display vectors.

## Non-author read (2026-10-09)

All values correct. Taken: "start-01's keys STO and RCL" was false (start-01 teaches neither), and the
learner was never told how to type a letter: STO, RCL and the letter keys are now taught here; the
order rule covers × and ÷ before + and −, as an agreement everyone uses, not a reading of the story;
the story's price change made one sentence at a time; n is stored under N, and the letters needn't
match is said; x beside × removed (exercise 3 uses a); an expression has no = sign; answer 2 uses
the stored letter as its own instructions say; RPN's RCL needs no ENTER, said.

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): a number typed where RCL
N should be; the wrong letter stored; the line quoted without its ×; RPN adding before multiplying.
All red.
