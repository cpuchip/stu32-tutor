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
