# start-01 evidence: getting started with the calculator (pre-algebra unit 0)

abacus #5112, on frac-01: every topic frac-01 required was taught only in the algebra course (rpn-01,
num-02), which starts in RPN, so a learner beginning pre-algebra on the algebraic line would meet
them nowhere first; graph.py passed it because "taught in another course" was allowed (my rule from
#5027). Two answers, both abacus's proposals: this lesson, pre-algebra's own start, alg first with
RPN offered; and graph.py's rule that a required topic is taught earlier in the same course or in a
prerequisite course the manifest names. Its topics are its own (calc-setup, calc-shift-keys,
calc-soft-keys, calc-first-calculation, calc-ans, calc-frac-display, calc-frac-arrows): the same idea
in two courses is two topics.

## Probed before writing (2026-10-08, core c7ab388; build/proto/alg_probe5.sh)

- The line writes minus as an ASCII `-` (`100-ANS`), where × and ÷ are their own signs.
- GOLD LASTx types ANS on the line mid-calculation (`100-ANS`, 76); its vector token is LASTX.
- RPN's x↔y is the vector token XY; `100 x↔y −` after 24 gives 76.
- 1 ÷ 3 with fraction display on shows `0 1/3` with ▼ in the status band, in both entries; →FRAC
  again shows `0.3333`.
- Fraction display turned on before typing works on the line (`9÷4`, `2 1/4`).

## Expected values

Oracle: build/proto/start01.py; each example in both entries (ID@alg: N= and %LINE=; ID@rpn: X=),
1/3 rounded once to 34 digits (below 1/3, so ▼). Every hand step in the prose is asserted there:
7 + 5, 12 × 2, 100 − 24; 20 = 8 × 2 + 4 and 4/8 = 1/2; 2.5 = 2 + 5/10; 45 + 38 by tens and ones;
9 = 4 × 2 + 1. 20 vectors, 10 display vectors; the core agreed at the first run.

| Vector | What | Shown |
|---|---|---|
| C01, C02, C03 | 7 + 5; × 2; 100 − ANS | 12.0000, 24.0000, 76.0000 |
| F01, F02 | 20 ÷ 8; →FRAC | 2.5000; 2 1/2 |
| F03, F04 | 1 ÷ 3 (▼); →FRAC off | 0 1/3; 0.3333 |
| E01 | 45 + 38 | 83.0000 |
| E02, E03 | →FRAC, 9 ÷ 4; off | 2 1/4; 2.2500 |

## Non-author read (2026-10-08)

All arithmetic correct. Taken:
- No hand work shown though the exercises expect it: each example now does it by hand first, the
  flour's leftover 4 cups shared among 8 batches included, and answer 2 says why the 1 cup left over
  is 1/4 each.
- The RPN rule "ENTER to finish it" was broken by C02 and C03 without a word: now said why (ENTER
  finishes a typed number so the next is not run into it; an answer is already finished).
- The RPN reading never said what a stack is, which way − works, or what the screen shows: a pile,
  the four lines and X at the bottom, and − takes X away from Y.
- "GOLD LASTx" types ANS though it says LASTx: now said, with why ANS is needed here (− first would
  work out 24 − 100).
- The title said "algebraic first" in the RPN reading too: now "Getting started with the calculator"
  (the course's unit 0 keeps its title).
- The arrow paragraph: ▲ and the 4095 limit dropped from a first lesson (frac-01's mention of 4095
  went with it); "0.3333, the same number" is now "rounded to four digits".
- Words: "decimal point", simplest form shown (4/8 shows as 1/2), STU and the two other modes, the
  other FRAC above E, the setup's choices as soft keys, RPN and ALG spelled out.
- Exercise 2 asks for "a whole number and a fraction"; a line on what to do when hand and calculator
  disagree.

Not taken: x↔y's place on the keyboard is not given (rpn-01 does not give it either, and I have not
verified it from the layout); the reader's "2 ENTER × gives 4" was their own reasoning, untested, and
the lesson does not need it.

## Checks

`make check`: 10/10 vectors in STU alg and STU rpn, fresh and used core, 25 quotes, the student run in
order in each entry. Controls (8): the setup printed without its entry; an answer without FIX 4's
digits; ANS's line misquoted; LASTx without its shift; the RPN subtraction without x↔y; →FRAC as a
fresh example; the arrow the wrong way; exercise 2 without →FRAC. All red.
