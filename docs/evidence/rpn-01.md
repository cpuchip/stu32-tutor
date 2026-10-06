# rpn-01 evidence

## Expected values (2026-10-06)

Recomputed with Python's `fractions.Fraction` (exact rationals), independently of the core:

| Vector | Computation | Exact |
|---|---|---|
| S01 | 7 + 5 | 12 |
| S02 | 7 - 5 | 2 |
| S03 | 20 / 8 | 5/2 = 2.5 |
| S04 | ENTER copies | X = Y = 6 |
| S05 | 6 x 6 | 36 |
| S06 | (3 + 4) x 5 | 35 |
| S07 | 4 + 6, with 2 + 3 waiting | X = 10, Y = 5 |
| S08 | (2 + 3) x (4 + 6) | 50 |
| S09 | 20 / 5 | 4 |
| S10 | 1 2 3 4 entered, R-down | X 3, Y 2, Z 1, T 4 |
| S11 | 12 / 4, then LAST x | X = 4, Y = 3 |
| S12 | 12 / 4 x 4 | 12 |
| S13 | -5 - 3 | -8 |
| S14 | 1.05^4 | 194481/160000 = 1.21550625 |

## Runs

`make check` at core f839cb9 (2026-10-06, gcc:14 container on fermion): 14/14 vectors and 20/20
expectations in 33s mode and in 35s mode; 4/4 display vectors; 14 of 14 vectors shown by their
printed keys, each the same ops and the same core state; 4 displays quoted.

`make controls`, first version: 17/17 planted faults turn the check red, each for its own reason. The first run
was 14/17: three controls were anchored on `| X=12`, which two vectors end with, so their faults
did not apply and the suite said so instead of counting them.

## Outside review (2026-10-06)

A read-only reviewer that did not write the checker read it looking for wrong lessons that pass,
and reported nine. Fixed, each with a control that turns red (29/29 at core f839cb9):

- the quoted displays' setting was not tied to the setting pressed, and display options were not
  inspected (two controls);
- a quoted display could be of an error or of a number still being typed: now compared with the
  device's own X line (`screen_lines`);
- a quoted display could sit under another example; near-miss fences and other `<disp` forms were
  invisible;
- an example could lean on an empty stack: the vectors also run from a used core;
- an empty `modes:` line, or `modes: 33s 35s`, skipped the 35s run; a second MODE33 inside a
  vector escaped the 35s rewrite;
- keys ending with a shift armed (or a menu or prompt open, or a device setting changed) passed;
- the em-dash check missed HTML entities and the front matter;
- an open menu's label that is also a printed legend is now refused as ambiguous (no control for this one yet);
- more than 64 expectations (the runner keeps 64) is refused.

Not fixed, and listed in lesson-format.md: inline-code keys and plain prose numbers, core entry
points beyond the three traced, and the screen's fitting of long lines. After the fixes the clean
pilot passes: 14/14 vectors and 20/20 expectations in each mode, from a fresh core and a used one;
14 of 14 vectors shown, the keys pressed in 33s and 35s; 4 displays quoted, each matching the
device's X line.

## Exercises (added with the prose, 2026-10-06)

Recomputed with Python fractions: E01 (8 - 3) x (2 + 4) = 30; E02 100 / (4 x 5) = 5; E03 2^5 = 32
(a stack of 2s, four presses of x, T copying down); E04 (-3) x (-4) = 12.

## Sources for the prose

- The name: "Polish" refers to Jan Łukasiewicz's nationality; his notation (1924) puts operators
  before operands, and RPN after them. Wikipedia, "Reverse Polish notation" and "Polish notation",
  read 2026-10-06. The lesson paraphrases; it quotes nothing.
- Key positions and colours: abacus layout/stu32-v0.json (not ruled): MODE blue on ENTER, LASTx
  gold on ENTER, DISP gold on 2. keyrun resolves every printed key from the firmware keymap, so a
  wrong name or colour fails the check.

## Teaching checks (the teaching agent's three, 2026-10-06)

- **Binding question:** how does the STU-32 hold your numbers while you work, and how do you move
  them? **Ring:** each section answers a part of it (ENTER separates and copies; a result stays in
  X; the stack replaces parentheses; x<>y and R-down move it; LAST x recovers; T copies down). The
  exercises use only what the sections teach.
- **Posture:** written to a person holding the calculator; no claims about our system or about
  RPN being better than other entry methods.
- **Ben Test:** the lesson makes no claim about our practice. Its claims about the calculator are
  each backed by a vector or by the layout; one unbacked sentence (R-down four times restores the
  stack) was cut rather than claimed.
- **The honest moment:** the minus-for-negative mistake gives a wrong answer with no error.
- **Backing for the pitfall:** S02 shows − on two numbers returns a number with no error.
- **Voice:** 0 em-dashes, 0 en-dashes; no antithesis or significance markers found by grep. The
  short "X holds 35." lines after examples are result lines, kept for Michael's call.

## Non-author read (2026-10-06)

A reader that did not write the lesson read it as a newcomer, with only the lesson and the layout,
and reported eleven findings about the lesson. All taken:

- **Wrong explanation of right keys (the serious one):** the draft said each x in S14 used the
  1.05 that T copied down. After 1.05 ENTER ENTER ENTER all four levels hold their own 1.05, so
  three presses never reach a copy. S14 now presses x five times (1.05 to the 6th =
  85766121/64000000 = 1.340095640625, FIX 4 1.3401) and says the 4th and 5th use copies; E03's
  answer says the same of its 4th press. Every check passed on the wrong text: the numbers were
  right and the words were not.
- The typing rule (after ENTER a new number replaces X; after + - x / it pushes X up) was shown and
  never stated; ENTER was first said to "move" and then to "copy"; S07 said the 5 waited in Y while
  it was in Z (new vector S07A: X 6, Y 4, Z 5 before the second +); shift keys and soft keys were
  used and never taught; S08 repeated S07's keys as "one more key"; no word on typos or on what is
  left on the stack (new vector S01A: 7 ENTER 56 <- + = 12; and the used-core run backs "no example
  depends on what is already on the stack"); "minus 5, minus 3" was ambiguous; "the 20 goes back
  up"; LAST x vs LASTx; "shows" vs "holds".

Two of my own claims were then narrowed before the run: face legends are not said to be white
(the layout does not say), and the typing rule names + - x / only (S06 backs it; keys such as the
clearing ones behave like ENTER). An untagged "12.0000" in the setup was cut, and check.py now
fails a FIX-form number outside a tag (its first version missed one followed by a full stop; the
control caught it).

After all of it: 20/20 vectors and 28/28 expectations in each mode, from a fresh and a used core;
21 keys blocks, 20 of 20 vectors shown, pressed in 33s and 35s; 4 displays quoted, each on the
device's X line; 30/30 controls red, 3/3 harmless changes green.

## Abacus's accuracy read (#4228, 2026-10-06)

Passed by hand, independently of check.py: S01A, S07A, S14 as rewritten, E01-E04, and the three
unbacked claims (key positions in layout v0; arithmetic leaves stack lift enabled, 33s appendix B;
the Łukasiewicz history). One fix: "every number shows four decimal places" is false at the
extremes (abacus probed 1E20 and 0.00001 in FIX 4). The setup now says very large or very small
numbers switch to scientific form, backed by display vectors F01 (1E20 -> 1.0000E20) and F02
(0.00001 -> 1.0000E-5), both passing; neither is quoted. Abacus's optional sentence crediting RPN
to Hamblin was left out: the Wikipedia article read this session credits the postfix scheme to
Burks, Warren and Wright (1954), reinvented by Bauer and Dijkstra, so a single inventor is not
settled by it. Two controls anchored on the changed sentence stopped applying and the suite said
so; re-anchored, 30/30 red and 3/3 green.
