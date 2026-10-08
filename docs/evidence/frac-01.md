# frac-01 evidence: equivalent fractions (pre-algebra P5's pilot)

Decision 63 (Michael, abacus #5022): hand first, calculator second; young learners default to
algebraic entry, with RPN offered. The pilot proposed in docs/courses/pre-algebra.md: P5's first
lesson, equivalent fractions, the place a pre-algebra year spends most of its time and where
fraction display can check hand work exactly. It is the first lesson to offer entries (`entries: alg
rpn`, STU mode only), so it is also the entry axis's first real test.

The bakery is a placeholder world (who the learners are and the story they would enjoy are
Michael's open questions 1 and 4). No character is named: the baker and a customer.

## What the core does on the algebraic line (probed 2026-10-08, core c7ab388)

Measured with the vector runner and keyrun before any prose (build/proto/alg_probe*.sh):
- `STU ALG FIX4 2 + 3 ENTER` passes `N=5 %LINE=2+3`, and X stays 0: an ALG result is ANS, shown in
  X's place, and the stack is left alone (029 rule 6). So the algebraic vectors expect N=.
- keyrun agrees with the vector when the setup presses the entry right after the mode, before the
  display setting; pressed after DISP, the ops come in another order and keyrun reports a DIFF. So
  the setup's form is fixed: `BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4`.
- `RPN` as an explicit token works in STU and 33s modes, so a lesson offering both entries sets RPN
  as plainly as ALG. `MODE33 ALG` and `MODE35 ALG` are refused (029's S04, S05): alg is STU's alone.
- The line in Y's place is reported by keyrun as an `eqn` line (`YL eqn 2+3`): the `line` quote kind.
- `=` is no key's legend: ENTER is the line's =. `(` is not a legend either; the soft key `()` types a
  pair and `▶` steps out (`(2+3)×4` = 20).
- A typed fraction (`.2.4`, num-02's way) is not a fraction on the line: the second point is just a
  point. On the line a fraction is a division, which is how this lesson teaches it anyway.
- `6 ÷ 8 ENTER` with fraction display on shows `0 3/4`; the display carries through a student's
  run.
- ANS by the student's key: gold LASTx types ANS on the line (`2+ANS`, 7), and its vector token is
  LASTX; the ANS token is another op, which the printed key does not issue.

## Expected values

Oracle: build/proto/frac01.py. Every example is an exact division or product, checked in exact
fractions, and only fractions whose decimals end are used (halves, quarters, fifths, eighths), so
no accuracy arrow appears; num-02 teaches the arrows. Every hand step the prose states is asserted
there too (1/2 = 2/4 = 3/6 = 4/8; 6/8 by 2; 12/16 by 2 twice or by 4; 2 does not divide 111, 3 does
not divide 296, 111 = 3 × 37; 20 = 5 × 4; 18/24 by 6, or 2 then 3; 6/15 by 3, 8/20 by 4).

| Vector | What | Shown |
|---|---|---|
| Q01, Q02 | 2 ÷ 4, 1 ÷ 2 | 0 1/2, 0 1/2 |
| Q03 | 6 ÷ 8 | 0 3/4 |
| Q04 | 111 ÷ 296 | 0 3/8 |
| Q05 | 8 × 37 | 296 |
| E01, E02 | 12 ÷ 20, 18 ÷ 24 | 0 3/5, 0 3/4 |
| E03, E03B | 6 ÷ 15, 8 ÷ 20 | 0 2/5, 0 2/5 |

Each in both entries (ID@alg with N= and %LINE=, ID@rpn with X=): 18 vectors, 9 display vectors. The
core agreed on every one at the first run, in both entries.

## Non-author read (2026-10-08)

Every hand computation checked and correct. Taken:
- "3/4 cannot be made any smaller" could be read as the amount shrinking, the very misreading the
  lesson fights: now "cannot be written with smaller numbers", and simplest form is "the same amount,
  in the smallest numbers that can name it".
- Dividing needed "evenly": dividing 6/8 by 4 gives 1.5/2. "Divides" is now defined once (goes into
  it with nothing left over) before it is used.
- Multiplying needed "whole number"; the why is shown for × 3 as well as × 2 (cut each piece into 3).
- "X shows" means nothing to a learner on the algebraic line: every result is now "The screen shows".
- Why a fraction is a division was never said: sharing 2 pies among 4 people.
- "When hand work is slow" turned the lesson's own rule around without saying so: it now says the
  calculator goes first here, for once. "3 does not divide 296" read as a random test: now "3 divides
  111 (111 = 3 × 37), but not 296". The step from dividing to multiplying is said. The old Q05 (3 × 37)
  was circular after "111 ÷ 3 is 37": dropped, and the learner works 8 × 37 by hand (240 + 56) before
  the calculator checks it. "About 3 pies in every 8" was exact: now "exactly".
- "Fraction display shows a fraction in simplest form" holds for a bottom number up to 4095 (num-02's
  limit), now said; frac-not-exact added to requires.
- The setup paragraph was too dense and never named the choice: now two short steps, and the reader
  is told to choose ALG (or RPN, in that reading).
- Exercise 1 asked for a target bottom number the lesson never showed: a worked example added (1/2
  with a bottom of 8); and its check shows 3/5, not the learner's 12/20, which is now explained.

The reader found the RPN reading natural without the algebraic sentences.

## The entry axis on this lesson

`make check`: 9/9 vectors in STU alg and in STU rpn, each from a fresh and a used core; 10 blocks in
each reading; 19 quotes (the algebraic line's own among them, kind="line"); the student run in order
in each entry. Controls (14, tools/controls.py): alg offered in 33s and 35s; the entry pressed after
DISP; a setup with no {entry}; an unknown entry; an algebraic result expected in X; RPN keys in an
alg block and the reverse; the line misquoted; the line's sentence left in the RPN reading; an RPN
vector missing; two alg variants of one block; a variant and a span naming no entry; →FRAC left out
of the setup. All red; one harmless change (a block's RPN variant written first) stays green. One
control as first written passed: it removed `e="alg"` from a quote that sat inside an alg span, which
the span already scopes; the redundant attribute came out of the lesson and the control now removes
the span.
