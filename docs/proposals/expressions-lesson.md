# Proposal: a short lesson on expressions (▸, →X, →EQN), STU only

**Status:** a draft, held. Asked for by Michael's ruling on the learn-082-140 card (via abacus #11861):
publish 082, plus a short lesson on expressions. The keys wait for his answer on the eqn-screen card (abacus #11864),
whose recommended option makes →X leave the list. So nothing below presses a key after →X that depends on where →X
leaves you; those places are marked **HELD**. No vectors exist yet, and the lesson folder is made only once they can
(section 3).

**Measured on:** the core at CORE_PIN 52134a4 (firmware 0.82, Casimir 1.4.0), with keyrun --sequence from
`BLUE MODE STU GOLD DISP FIX 4`, 2026-10-31. The screens quoted below are keyrun's report lines from those runs,
not yet checked by vectors.

## 1. The lesson

- **id:** expr-01, **title:** An equation you can hold. **modes:** STU, with `modes_reason:` saying that →X and →EQN
  are STU mode's keys alone (firmware 082: in 33s and 35s modes the list keeps EXIT and has no EQN MORE).
- **Place:** the algebra-to-calculus course, after eq-01 (the equation list) and before der-01, which can then point
  back to it.
- **requires:** setup shift-keys soft-keys stack-levels sto rcl swap-roll clear-message eqn-typing equation-list
- **Teaches (new TOPICS rows):** expression-value (an expression in X, and how T, Z and Y write one), eqn-more (the
  list's ▸ and EQN MORE), eq-drop (→X), eq-store (→EQN), not-a-number (NOT A NUMBER, and why).

### Draft prose

**An equation you can hold.** In eq-01 an equation lived in the list: you typed it, and XEQ or SOLVE worked with it
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

**HELD (eqn-screen):** what the screen shows right after →X, and the keys that take you to the stack. At 52134a4
the list stays on the screen with nothing changed (abacus's walk, item 2), and C then leaves it.

**What X shows.** X draws the expression as the list did, 3X² − 4. In Y, Z or T the same expression is written on
one line, in quotes: `'3×X^2-4'` (measured). The quotes say "this is a rule, not a number", so `'2'` can never be
mistaken for 2.

**It isn't a number.** Type 2 and press ×. The screen says NOT A NUMBER, and nothing else changes: the 2 is still in
X and the expression still in Y (measured). An expression has no value until you give X one, which is what XEQ does in
the list (eq-01). ← clears the message.

**Keeping it in a letter.** STO A stores an expression just as it stores a number, and RCL A brings it back
(measured: X `'3×X^2-4'` after RCL A).

**Back into the list.** With the expression in X, open the list and press ▸ then →EQN. The expression goes into the
list just after the equation that was showing, and becomes the one showing. X keeps its copy. ▲ shows the equation it
came from (measured: two `3×X^2-4` entries, then EQN LIST TOP). With a number in X, →EQN refuses: INVALID DATA, and the
list is unchanged (measured, with 2 in X).

**HELD (eqn-screen): a warning about C.** At 52134a4, C after →X leaves the list and a second C clears X, so the
expression is gone unless it was stored (measured). Whether the warning is needed, and its keys, depend on the card.

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

- **G1, the eqn-screen card:** the keys after →X.
- **G2, firmware vectors (tests/vectors.c at 52134a4):** no token for →X or →EQN (the CAS ops have `CASD:` and the
  like), and no expectation for an expression in X or Y (`X=` compares a number). The lesson format requires vectors
  before prose, so the lesson needs both. That is the firmware's tool, not tutor's.
- **G3, tutor's tools:** keyrun's VAL line prints an empty field for an expression (measured), so check.py's VAL
  comparison needs a rule for it. X's expression is quoted with kind="drawn" (the DRAWN line), and Y's one-line text
  with the line kinds; both exist.
