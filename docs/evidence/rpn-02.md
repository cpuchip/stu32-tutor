# rpn-02 evidence

## Expected values (2026-10-06)

Recomputed with Python's `fractions.Fraction`, independently of the core:

| Vector | Computation | Exact |
|---|---|---|
| V01 | store 0.0825 | A = X = 0.0825 |
| V02 | 40 x 0.0825 | 33/10 = 3.3 |
| V03 | 40 x 0.0825 by RCL x, Y keeps the 0.0825 lifted by typing 40 | X 3.3, Y 0.0825 |
| V04 | 9 stored, 1 + 2 on the stack, then RCL C | X 9, Y 3, C 9 |
| V05 | 0 + 12.5 + 7.25 + 30 | 199/4 = 49.75 |
| V06 | as V05, then VIEW | X 30, B 49.75 |
| V03A | 25 - 10 by RCL - | 15 |
| V06B | as V06, then 5 | X 5, Y 30 |
| V07 | 3.5 x 12 | 42 |
| V08 | 2 x (12 + 3.5) | 31 |
| E01 | 250 x 1.08^2 | 1458/5 = 291.6 |
| E02 | 100 - 23.4 - 9.6 | 67 |

Displays at FIX 2 (fmt-vectors.txt): 0.0825 -> 0.08, 3.3 -> 3.30, 9 -> 9.00, 42 -> 42.00,
291.6 -> 291.60. VIEW B's line, B=49.75 (kind view), is checked on the device's X line.

## Sources

- Letters printed at each key's lower right: abacus decision 25 and layout/stu32-v0.json's
  comment; keyrun resolves every letter through the firmware's letter layer (km_letter_of).
- STO + and RCL x as two-key sequences: the firmware's km_arith_op (keymap.h), pressed through
  app.c by keyrun.

## Probes (2026-10-06, on the core at f839cb9, not lesson vectors)

Before the prose claimed them: after VIEW the next key acts, in 33s and in 35s mode (V06B now
backs it); RCL - works X minus A (V03A backs it); RCL / works X divided by A (2 STO A, 10 RCL / A
gives 5; the prose states it, no lesson vector shows it). Letter keys from layout v0: A on the
square-root key, B on e^x, C on LN, D on y^x, G on STO, L on TAN, W on 5.

## Non-author read (2026-10-06)

A reader that did not write the lesson walked every example as a newcomer who had done rpn-01,
tracking the stack and the variables, and found every answer right and ten problems in how the
lesson explained them. All taken:

- **The screen contradicted the text:** at FIX 2, storing 0.0825 shows 0.08 while the prose said X
  holds it. Now quoted (D-V01) and explained.
- Letters on keys that do something else (W on 5, L on TAN, G on STO: STO G is STO twice): named.
- **A claim that discriminated nothing:** "Y still holds 0.0825" was offered to show RCL x does
  not push the stack, but plain RCL then x leaves the same X and Y. Cut; the gain stated is one
  key fewer.
- What typing does after STO, and the order of RCL - and RCL /, were never stated: stated, with
  V03A.
- VIEW's screen and what the next key does: quoted (kind view) and backed by V06B.
- V07's "in the order you think it" was weak: the section now reuses W and L for the perimeter
  (V08). The answers quote the display (291.60) instead of a bare value.
- Also: "until you store something else" ignored STO +; the prompt's screen was not described
  (left in words: "the calculator waits for a variable").

One antithesis ("changes what you see, never what is stored") was cut in the voice pass.

## Checks

`make check` at core f839cb9: 12/12 vectors and 29/29 expectations in 33s and in 35s, from a
fresh core and from a used one (every variable A-Z holding 7, so no example leans on an empty
variable); 13 keys blocks, 12 of 12 vectors shown, pressed in both modes; 6 displays quoted, each
on the device's X line. `make controls`: rpn-01 30/30 red and 4/4 green; rpn-02 5/5 red and 1/1
green.
