# Proposal: a short lesson on expressions (▸, →X, →EQN), STU only

**Status:** accepted by Michael on the poly-05-lesson card (2026-11-01: "Publish both; the checkpoint stays in
poly-04.", via abacus #12143), after abacus walked poly-05's keys on primer's preview at 1a12ecf. The lesson is
lessons/poly-05-an-expression-you-can-hold, with int-01's sentence, merged to main from lesson-poly-05.

**To revisit if symbolic stack arithmetic lands:** Michael's note on the card asks for 50g-style arithmetic on
expressions, so that 2 × with an expression in Y multiplies the whole expression. It is not decided or built
(soroban has the blueprint ask, abacus #12143). If it lands, poly-05's "Not a number" section (N01, N02) and
exercise 2 (E02, E02B) change, along with the not-a-number topic in lessons/TOPICS and the control that misquotes
NOT A NUMBER in tools/controls.py.

The rest of this status is as it stood before the card. Unit 083 was accepted at stu32-firmware 0acbbdc (abacus #12011), and main's CORE_PIN is 0acbbdc (64fa4cc). The
branch passes make check (57/57) and make controls (405/405 red over 65 folders, 27/27 harmless green) there. The draft
below is kept as it was written; the lesson folder supersedes its prose.

Asked for by Michael's ruling on the learn-082-140 card (via abacus #11861): publish 082, plus a short lesson on
expressions. He answered the eqn-screen card on 31 October with option 1 (abacus #11975): Equation mode gets its own
screen in every mode, and STU's →X leaves Equation mode. The firmware built it as unit 083 (blueprint at
stu32-firmware 81442f7, work/blueprint/083-eqn-screen.md; abacus #11987).
- **Placement (abacus #12018):** unit 5's checkpoint stays in poly-04, so no existing text moves, and poly-05 comes
  after it. Michael kept it there, and docs/lesson-format.md now says a checkpoint may sit before a one-mode last
  lesson.

**Measured on:** the core at CORE_PIN 52134a4 (firmware 0.82, Casimir 1.4.0), with keyrun --sequence from
`BLUE MODE STU GOLD DISP FIX 4`, 2026-10-31. The screens quoted below are keyrun's report lines from those runs,
not yet checked by vectors.

## 1. The lesson

- **id:** poly-05, **title:** An expression you can hold. **modes:** STU, with `modes_reason:` saying that →X and →EQN
  are STU mode's keys alone (firmware 082: in 33s and 35s modes the list keeps EXIT and has no EQN MORE).
  (This draft first said expr-01, but that id is taken: lessons/expr-01-letters-for-numbers, "Letters for numbers".)
- **Place:** the algebra-to-calculus course, unit 5 (Polynomials), after poly-04. Its example, 3X² − 4, is an
  expression without =, which the course teaches in poly-02 ("Typing c", topic `expression`). Placed in unit 2, as this
  draft first had it, it would lean on a topic taught three units later, which the course file forbids. der-01 can
  still point back to it.
- **requires:** setup shift-keys soft-keys stack-levels sto rcl swap-roll clear-message eqn-typing equation-list
  expression
- **Teaches (new TOPICS rows):** expression-value (an expression in X, and how T, Z and Y write one), eqn-more (the
  list's ▸ and EQN MORE), eq-drop (→X), eq-store (→EQN), not-a-number (NOT A NUMBER, and why).

### Draft prose

**An expression you can hold.** In eq-01 an equation lived in the list: you typed it, and XEQ or SOLVE worked with it
there. STU mode can also hand you a copy of it, to keep on the stack like a number. A copy held this way is called an
*expression*: the rule itself, with no value yet.

Type an equation to work with:

```keys B01 mode=STU
GOLD EQN 3 × RCL X yˣ 2 − 4 ENTER
```

The screen shows it as a textbook writes it, 3X² − 4 (measured: drawn `3X^2-4`). The list's last soft key, ▸,
opens a second row of keys for the list, EQN MORE. Its first key, →X, copies the equation into X:

```keys B02 after=B01 mode=STU
▸ →X
```

**HELD (083):** what the screen shows right after →X. At 52134a4 the list stays on the screen (abacus's walk, item 2),
and C then leaves it. At 083 (§2) →X leaves Equation mode, so the expression lands in X and no key is needed to reach
the stack. It is one →X per visit: GOLD EQN reopens the list at the same entry, for another.

**What X shows.** X draws the expression as the list did, 3X² − 4. In Y, Z or T the same expression is written on
one line, in quotes: `'3×X^2-4'` (measured). The quotes say "this is a rule, not a number", so `'2'` can never be
mistaken for 2.

**It isn't a number.** Type 2 and press ×. The screen says NOT A NUMBER, and nothing else changes: the 2 is still in
X and the expression still in Y (measured). An expression has no value until you give X one, which is what XEQ does in
the list (eq-01). ← clears the message.

**Keeping it in a letter.** STO A stores an expression just as it stores a number, and RCL A brings it back
(measured: X `'3×X^2-4'` after RCL A).

**Back into the list.** With the expression in X, open the list with GOLD EQN and press ▸ then →EQN. (At 083, →EQN
outside the list is NO EQN, so the GOLD EQN is needed.) The expression goes into the
list just after the equation that was showing, and becomes the one showing. X keeps its copy. ▲ shows the equation it
came from (measured: two `3×X^2-4` entries, then EQN LIST TOP). With a number in X, →EQN refuses: INVALID DATA, and the
list is unchanged (measured, with 2 in X).

**A warning about C, probably not needed.** At 52134a4, C after →X leaves the list and a second C clears X, so the
expression is gone unless it was stored (measured). At 083 →X has already left the list, so one C clears X, as it
clears any number, and only by choice (083's new vector X10 proves it). Decided at the build.

### Exercises (outline)
1. Type 2X + 5 = 11, take it onto the stack, and store it in B. (HELD at the →X step.)
2. With 7 in X and an expression in Y, predict what × shows, then check. (Needs only x↔y and ×.)
3. Put an expression from a letter back into the list after a given equation, and find it with ▲ and ▼.

## 2. What the measurements showed (for abacus's walk and the card)

- **C twice loses the expression silently.** After ▸ →X, the first C leaves the list (X shows `'3×X^2-4'`); a second C
  clears X. A learner who presses C twice to "get out" loses what →X gave. Related to the card's question of where →X
  leaves you.
- **→EQN puts in a duplicate** when X holds the shown equation's own copy: the list then has the same text twice. As
  082 specifies (after the shown entry); worth one sentence in the lesson.
- **keyrun's DRAWN line also names EQN LIST TOP and a built-in's entry** (`2*2 lin. solve`) as drawn text. No lesson
  quotes either today. check.py's strict rule fails an eqn quote wherever something is drawn, so a future lesson quoting
  EQN LIST TOP as kind="eqn" would fail, and the rule may need to treat those as not drawn.

## 3. What the check needs before the lesson folder exists

- **G1, the eqn-screen card:** answered (option 1). The keys after →X follow unit 083 once it is built and accepted;
  then the pin moves to its head.
- **G2, firmware vectors:** done at stu32-firmware 67db051. It adds the tokens EQDROP and EQSTORE, and the expectations
  %XEXPR, %YEXPR and %XDRAWN (tests/082-soroban.txt X1-X9). 083 moves X1-X5, X7 and X8 with its §2, and soroban
  carries them.
- **G3, tutor's tools:** done. keyrun prints an EXPR line (X Y Z T as STU's text, none for a number) whenever the
  stack holds an expression. The walk-through checks a vector's %XEXPR and %YEXPR against what the student's device
  holds, and %XDRAWN against the DRAWN line. check.py reads a key vector's expectations as the rest of the line, as
  the firmware does, since a drawn text may hold |; a | anywhere else still miscounts the fields. A plain quote of X
  where the glass draws is refused with that reason. (It was already refused before, but only because it had no
  display vector.) Falsified with a throwaway STU lesson at firmware 9df97a8: the lesson passed; a planted %YEXPR
  fault went red for its own reason; and two mutants of the new comparison each went red.

## 4. What 083's screen moves in the published lessons (abacus #11987)

Measured at 52134a4 by walking every lesson and the placement file in each of its modes, as the learning page presses
them (check.py's student_sequence through keyrun --sequence), and listing every block that ends with EQN in the status
band.
- **33s and 35s, a block that ends on the list with Y in view** (083 hides T, Z and Y), in 6 lessons:
  - eq-01: Q01, Q06A;
  - eq-03: A01;
  - exp-04: Q01, E01;
  - int-01: I01;
  - poly-02: R01, E01;
  - sys-02, 35s only: T01Z, T01A, F01A, M01A, N01A, N02A.
- **STU:** every block that ends in Equation mode ends on the list, which 080 already draws clean. None ends while an
  equation is being typed. Typing shows only between a block's keys, in the 11 lessons that press EQN: der-01, der-02,
  der-03, eq-01, eq-02, eq-03, exp-04, fn-02, int-01, poly-02, sys-02.
- **One block 083's blueprint doesn't name:** eq-01 Q05A, SOLVE's variable prompt (`SOLVE _`). It has EQN in the
  status band and Y in view (5.0000) in all three modes. It is neither the list nor the editor.
- **Quotes:** none of these blocks quotes T, Z or Y. Their quotes are kind eqn, drawn or prompt, all on X's line. So
  the check should not move, though the pictures do. One passage reads differently once the stack is hidden: int-01's
  "The built-in integral" puts the two ends on the stack, then shows the expression again with EQN. At 083 the ends are
  out of view while the list shows. A sentence saying they are still there would help (lesson text, so on a card).
  On branch lesson-poly-05, the sentence is in the lesson, in every mode (STU's list has hidden the stack since 080).
  It sits right after the I01B block, so "answer X:" still leads into its keys, and so it is in the past tense:

  > While the expression showed, the two ends were out of sight, but they were still in Y and X: Equation mode
  > gives the screen to the equation, and the stack comes back when it closes.

  abacus (#11999): this sentence and poly-05 ride one card with 083's learn update, once 083 is accepted.
