# der-01 evidence: the derivative

abacus #5263 (Michael away; unit 11 waits on nothing of his): propose unit 11's lessons and draft the
first. The plan is in docs/courses/algebra-to-calculus.md's units table:
- **der-01, the derivative as a function:** this lesson.
- **der-02, the power rule by hand:** (a + h)ⁿ expanded for n = 2 and 3, the pattern n·aⁿ⁻¹, sums and
  constants term by term. Checked numerically by a difference quotient in every mode, and by D/DX in
  STU, whose -1÷X^2 for 1/x shows the rule reaching past whole powers.
- **der-03, using the derivative:** the tangent line y = f(a) + f′(a)(x − a); highest and lowest points
  where f′ = 0, found by SOLVE on the derivative in every mode; STU's GRAPH SLOPE and EXTR (unit 040)
  as the numeric d/dx beside them.

## What the core does (probed 2026-10-08, core c7ab388; build/proto/der_probe.sh)

- **D/DX** is CAS 004: EQN LIST's fifth soft key, CAS, then D/DX. It prompts for the variable as
  SOLVE does and is answered by the letter key; STU only. The printed keys
  `GOLD EQN 2 × RCL T yˣ 2 ENTER CAS D/DX T` issue the same ops as the vector `EQN … CASD:T`.
- **Casimir's texts:**

  | Input | D/DX |
  |---|---|
  | 2T² in T | 4×T |
  | X³ − 4X + 1 | 3×X^2-4 |
  | 5 | 0 |
  | X⁵ | 5×X^4 |
  | 1/X | -1÷X^2 |

  The result is a new equation after the original, which is kept.
- **XEQ on the result,** with 3 at the T prompt and R/S, gives 12.
- **Equation mode stays on after D/DX.** The student run caught it: exercise 3's first digits started
  a new equation. Fixed with a block that turns it off, and a control plants the fault.

## Expected values

Oracle: build/proto/der01.py, modelling the keys.
- **Program V,** (d(a + h) − d(a)) ÷ h for d(t) = 2t², each operation rounded once. Every value is the
  exact 4a + 2h:

  | Vector | a, h | Value |
  |---|---|---|
  | D01 | 3, 0.001 | 12.002 |
  | D02 | 3, −0.001 | 11.998 |
  | D02B | 3, 0.0001 | 12.0002 |
  | D03 | 0.5, 0.001 | 2.002 |

- **The algebra the prose states** (2(a + h)² − 2a² = 4ah + 2h², ÷ h = 4a + 2h) is asserted in exact
  fractions at several a and h.
- **The exercises,** typed directly: (2 × 5.001² − 50) ÷ 0.001 = 20.002; (3.001² − 9) ÷ 0.001 = 6.001;
  (2 × 3.001² − 18) ÷ 0.001 = 12.002.
- **Casimir's 4×T and 2×X** are the core's own texts, checked by the vectors.

13 vectors, 8 display vectors.

## Checks

**`make check`:**
- 33s and 35s: 9/9 vectors.
- STU: 13/13. The D/DX section is STU-only (mode= blocks, @STU vectors); the 33s and 35s readings say
  their modes have no such key and the algebra plus program V is the method there.
- Each mode worked through in order.

**Controls (6), all red:**
- d(a) not doubled in V;
- the speed at 3 quoted as exactly 12;
- h from below keyed with − instead of +/−;
- D/DX answered with X instead of T;
- Casimir's 4×T misquoted;
- Equation mode left on before exercise 3.

## Non-author read (2026-10-08)

The arithmetic is all correct (the expansion, V's 15 lines, every value). Taken:
- **The tangent line.** "Turns until it only touches the curve" made the secant reach the tangent,
  the limit error this unit exists to prevent, and "only touches" is the wrong test besides (a vertical
  line meets a parabola once). Now the lines close in on one line, as the averages close in on a
  number, and no line through two points ever is the tangent.
- **"Checks" overstated what averages do.** Now they agree with the rule and do not prove it; the
  algebra proves it. An h = 0.0001 run (D02B) was added, so closing in is seen, not asserted.
- **Exercise 3.** At 8 metres the speed was 8, so the answer could not show which number it came from.
  Now 18 metres: t = 3, speed 12, with "not d′(18), which is 72: d′ takes a time".
- **The limit's why.** 2h shrinks to 0, and h = 0 could not go into the first fraction (0 ÷ 0). The
  doubling step is written out.
- **The letters:**
  - a renamed t in so many words;
  - d′ named as the function and d′(t) as its value;
  - why the program is V (lim-02's D may still be in memory);
  - the d's in D/DX are not the ball's d.
- **The STU reading:** "type the expression 2t²" (the keys type no d(t) =). The 35s/STU ENTER note now
  says it is for running a program; XEQ on an equation takes none.
- **The 33s and 35s readings:** "in these modes", and Casimir is no longer named to a learner who
  cannot use it.

Not taken: "(eq-01, fn-02)" was read as pointing at a lesson not yet done. fn-02 is unit 3 of this
course, long before; the brief to the reader listed only some earlier lessons.
