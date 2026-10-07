# The prerequisite graph: audit (2026-10-07)

Michael asked for the lessons as a linked graph, "if a student feels they missed a topic they can
navigate back to where we taught it" (abacus decision 60). abacus put it first (#4717). The shape:
lessons/TOPICS names each topic, its lesson and the section that teaches it (- for a lesson's
opening); each lesson's front matter `requires:` names the topics it leans on; tools/graph.py checks
both in `make check`, and plants six faults in `make controls` (all red). The lesson graph is derived:
A needs B when A requires a topic B teaches. Field shapes sent to primer first (#4738).

## How the requires lines were found

A first TOPICS (119 topics) was drafted from the section headings and first lines of every
section. Four non-author readers then read every line of their lessons (rpn and num; eq and fn; lin
and poly; exp and trig), with TOPICS beside them, and reported for each lesson: the topics it uses
without teaching, with line and quote; forward references; gaps (used, taught nowhere); and TOPICS
fixes. The rule for a requirement: a learner who skipped the teaching lesson would be lost or misled
at that line. A key named only as a landmark ("gold, above √x") and an idea re-taught in place are
not requirements. The setup is: every lesson after rpn-01 requires `setup` (and `shift-keys` where
it presses shifted keys beyond the setup); pressing FIX in the setup does not by itself require
rpn-03's `fix`, since rpn-01 says what FIX 4 does. Only num-04, which leans on how FIX behaves,
requires `fix` and `fix-overflow`.

What was checked by the author: every TOPICS heading (by graph.py), and the readers' claims about
sections and the content findings below, against the lines they cite. The requires lines take the
readers' cited dependencies under the rule above; they were not each re-read. Result: 141 topics,
28 lessons, 101 lesson links, no cycle.

## TOPICS fixes the readers made (all taken)

- Missing topics, now named: soft keys and menus, the stack levels, ← (rpn-01); VIEW (rpn-02); C
  clears a message, 1/x (num-03); the program pointer (fn-01); a program running another (fn-02);
  ŷ (lin-02, taught in "The line", not "Estimating"); half-life (folded into decay); a power of a
  power (exp-02); doubling time (exp-03); a line meeting a one-way curve at most twice (exp-04);
  Pythagoras (trig-02); yˣ in an equation, at most n roots (poly-02); and the ideas taught in
  openings with no heading: function (fn-01), linear function (lin-01), model (lin-03), polynomial
  and degree (poly-01), root (poly-02), quadratic (poly-03), radian (trig-01), the trig ratios
  (trig-02).
- Wrong sections, moved: the letters on the keys (rpn-02's opening section), recall arithmetic ("RCL
  brings it back"), the equation list (eq-01's "The × matters", where it is first taught; eq-02
  keeps "EQN shows the last equation you viewed"), domain (fn-03's "Dividing by zero"), LN (exp-03's
  "What power?").
- Titles widened or corrected: the setup ("a mode and FIX": rpn-02 and num-04 use FIX 2); num-01's
  last section (a full stack loses T, and working from the inside out; the four levels are rpn-01's);
  −3² with +/− on a result; typing a negative power of ten; XEQ's prompt and R/S; keying into a stopped
  program; falling, flat and vertical lines; a double root; complex numbers and typing them;
  conjugate pairs; a full turn and negative angles; the ranges of ASIN and ACOS.

## Content findings in accepted lessons

The readers found these in the prose; each was checked against the lesson's line. All but 10 are
made (build/proto/fix_audit.py), in 14 lessons, which lessons/ACCEPTED holds back until abacus has
seen them. How each was made: 1, C named as the bottom left key (layout/stu32-v0.json) at its first
mention (rpn-02) and first press (num-03); 2, the "33" dropped; 3, significant digits defined where
rpn-03 first says them; 4, "types and solves"; 5, "from eq-01 and poly-02"; 6, lin-01 and exp-01
named; 7, "a pair of the form p + qi and p − qi"; 8, the reference to fn-02's TABLE section put in an
STU span; 9, "multiplying powers of one number adds the powers (num-04 did it with powers of ten)";
11, the three digits dropped; 12, poly-01's opening says to press GOLD GTO . . if a program is still
stopped from fn-03. 10 stays open: the claim wants a picture, which the site's graphs can give.

1. The C key is never introduced or located: num-03 is the first to press it ("Press C to clear the
   message"), and eq-01, fn-01, fn-03, lin-01, lin-03, poly-02..04 and exp-03 lean on it.
2. num-02 says the status band "also shows the mode, 33", in every mode.
3. rpn-03 uses "significant digits" (FIX, ENG) without saying what they are.
4. eq-02 says "this lesson uses all three" (typing, XEQ, SOLVE); it never presses XEQ.
5. exp-04 says "SOLVE, from poly-02"; SOLVE is eq-01's.
6. exp-01 says "(unit 4)" and lin-03 "which unit 6 meets": a learner sees lesson ids, never unit
   numbers.
7. poly-04 uses a and b for the quadratic's coefficients and, in the same sentence, for the parts of
   a complex number.
8. poly-02 points 33s and 35s readers at "the expression in fn-02's TABLE section", which they never
   saw: it is in fn-02's STU section.
9. exp-01 splits 0.5^2.5 as 0.5² × √0.5, a rule (multiply powers by adding exponents) taught only for
   powers of ten (num-04).
10. exp-04 asserts that a line meets a curve bending one way at most twice, without a picture or an
    argument a learner can follow.
11. The 036b note's "(or a line's three digits)" names a way to use XEQ and GTO that no lesson teaches
    (accurate, abacus #4744; it may simply go).
12. poly-01 is the first program entered after fn-03 leaves S stopped; fn-03's last answer says to
    press GTO . . first, and poly-01 does not repeat it.
