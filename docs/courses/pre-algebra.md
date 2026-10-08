# Pre-algebra with the STU-32 (PROPOSED syllabus)

**Status:** a proposal for Michael to push against (abacus decision 60, 2026-10-07: "pre-algebra and
geometry", for a first learner in pre-algebra). Not ruled.

**Scope source, scope and order only (no text, figure or problem taken):** the chapter list of
OpenStax Prealgebra 2e (books/openstax/prealgebra-2e, CC BY-NC-SA 4.0, fetched 2026-10-07). Its
order is the usual one: whole numbers, the language of algebra, integers, fractions, decimals,
percent, the properties of numbers, linear equations, measurement and geometry, polynomials, graphs.

## The shape

- **Hand first, calculator second.** At this level the arithmetic is the lesson. Each idea is done
  by hand, then the STU-32 checks it, and then the calculator does what hand work cannot do quickly
  (a long division's remainder, a prime test by a program, a fraction to 34 digits). The calculator
  never stands in for a skill the lesson is teaching.
- **Stories for the simpler topics** (decision 60). Each unit runs inside one small story with
  invented characters, a place and a problem the mathematics solves (a bakery's orders, a ship's
  stores, a garden's plots). No real person is named or described, the learners least of all. The
  story carries the examples; the vectors are still written first, and every number in the story
  is one the calculator computes.
- **Real-world examples throughout**, adults included: prices, recipes, distances, time.
- **The graph links back.** Each lesson's `requires:` names what it leans on, so a learner who
  missed a topic is linked to the section that taught it, in this track or the algebra course.
  Where an algebra-course lesson already teaches a key (rpn-01's ENTER, num-02's fraction keys,
  num-04's %), the pre-algebra lesson requires it rather than teaching the key twice; where the
  algebra course assumed something (adding fractions by hand, negative numbers), this track teaches
  it, and the algebra lesson's `requires:` gains the link.
- Lessons of 10 to 15 minutes, shorter than the algebra course's 15 to 25.

## Units

| # | Unit | The mathematics | On the STU-32 |
|---|---|---|---|
| P1 | Whole numbers | place value; adding, subtracting, multiplying, dividing; estimating to check an answer | rpn-01's stack (required, not retaught); INT÷ and Rmdr for a quotient and remainder |
| P2 | The language of algebra | a variable; an expression; evaluating; an equation solved by undoing | a variable as STO and RCL (rpn-02); checking a solution by putting it in |
| P3 | Factors and multiples | divisibility; primes; prime factorization; greatest common factor; least common multiple | Rmdr as a divisibility test; a small program that looks for factors (a first loop) |
| P4 | Integers | the number line; adding and subtracting negatives; signs in multiplying and dividing | +/− (rpn-01); the calculator agreeing with the sign rules |
| P5 | Fractions | what a fraction is (parts of a whole, a point on a line); equivalent fractions and simplest form; the four operations; mixed numbers | num-02's fraction keys, after the hand work; →FRAC to check |
| P6 | Decimals, ratio and rate | decimals and fractions as one number; rounding; ratio, rate and unit rate; the mean | the stack for unit rates; Σ+ and x̄ for an average |
| P7 | Percent and proportion | percent as per hundred; percent of, percent change; proportions | num-04's % and %CHG; a proportion as an equation |
| P8 | The properties of numbers | commutative, associative, distributive; identity and inverse; rational and irrational | why the stack order matters for − and ÷; √2 to 34 digits never ending |
| P9 | Linear equations | one and two steps; variables on both sides; fractions and decimals in an equation | the check by putting the answer in, then eq-01's SOLVE as a bridge to the algebra course |
| P10 | The coordinate plane | points, axes, plotting from a table | a table from a rule (by hand, then fn-02's loop or STU's TABLE) |

Keys named here that no lesson uses yet (INT÷ and Rmdr, x̄, STU's algebraic entry) come from the
layout (abacus layout/stu32-v0.json) and the firmware's unit list; each is probed on the pinned
core before a lesson leans on it, and the plan changes if one is not there.

About 30 lessons. P1 to P5 are what a pre-algebra year mostly is; P6 to P10 lead into the algebra
course (num-01 onward), whose lessons then require P-topics where they assumed them.

## Before writing: one pilot

As with rpn-01, one pilot lesson first, for Michael's reaction to the story voice and the hand-then-
calculator rhythm before thirty are written. Proposed: P5's first lesson (equivalent fractions), since
fractions are where a pre-algebra year spends most of its time and where the calculator's →FRAC
can check hand work exactly.

Written 2026-10-08: lessons/frac-01-equivalent-fractions (docs/evidence/frac-01.md), the first lesson
to offer entries, algebraic first with RPN offered, in STU mode. The bakery in it is a placeholder
until question 4 is answered.

## Questions for Michael (through abacus)

1. Where is the pre-algebra learner now, and what book or program do they use (for the entry point
   and the order; read for scope only)?
2. Hand first, calculator second: right for them? ANSWERED yes (decision 63, abacus #5022).
3. RPN or algebraic entry for a young learner? The algebra course is RPN first (decision 7). If STU
   mode's algebraic entry (firmware unit 029) is on the calculator they use, a pre-algebra track
   could start there and meet the stack later. ANSWERED (decision 63): algebraic by default, RPN
   offered; built as the entry axis (docs/lesson-format.md, `entries:`).
4. The story: one world shared by both tracks, or one per track? Any setting they would enjoy?
