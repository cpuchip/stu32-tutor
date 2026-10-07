# rpn-03 evidence

## Expected values (2026-10-06)

Python's decimal module at 34 digits, rounding half even (the core's precision), independently of
the core:

| Vector | Computation | Exact at 34 digits |
|---|---|---|
| P01, P02, P04 | 2 / 3 | 0.6666666666666666666666666666666667 |
| P03 | (2 / 3) x 3 | 2.000000000000000000000000000000000 = 2 |
| P05 | 23456 | 23456 |
| P06 | 1 / 80000 | 0.0000125 |
| P07 | 4.5 x 10^9 | 4500000000 |
| P08 | 1 / 8 | 0.125 |
| E01 | 22 / 7 | 3.142857142857142857142857142857143 |
| E02A | 7 / 9 | 0.7777777777777777777777777777777778 |
| E02 | (7 / 9) x 9 | 7.000000000000000000000000000000000 = 7 |

The ENG example uses 23456, not 12345: 12345 at ENG 3 sits on a rounding tie (1234|5), where half
up and half even disagree, which would distract from the lesson.

Displays (fmt-vectors.txt), each at the setting its example ends in, all as predicted before the
run: 0.6667 (FIX 4), 0.67 and 2.00 (FIX 2), 6.667E-1 (SCI 3), 23.46E3 (ENG 3), 1.2500E-5 (FIX 4),
4.50E9 (SCI 2), 0.125 (ALL), 3.143 (FIX 3), 0.78 and 7.00 (FIX 2). Each also matches the device's
X line after the printed keys.

## Probes (on the core at 867ddd5)

- SHOW is not in the core (no op, no key); abacus queued it as unit 030 (abacus-firmware c904cb3).
  The lesson carries a `SHOW:` note where its section goes.
- Two thirds at ALL: the display runner at its default width (22) gives 0.66666666666666666667;
  the device's X line (screen_lines) gives 0.6666666666666666667. The two widths differ, so the
  lesson does not quote it; it says only that such a number fills the line. Reported to abacus.

## Non-author read (2026-10-06)

Eight findings, all taken. The two that mattered:

- **ENG's digit was explained wrongly:** "like SCI" with "places after the point" makes a reader
  expect 23.456E3; the screen shows 23.46E3, because ENG's digit counts significant digits after
  the first. Rewritten, with the four-significant-digit reading.
- **The lesson broke for a student working in order:** after P05 the display is still ENG 3, so
  P06 would not show what the text said. The lesson now says a setting stays until changed, and
  P06 sets FIX 4 again (in its keys and its vector).

Also: the digit after FIX's digit (it starts a new number and pushes X up; P03 backs it); "two
thirds times three is 2" made precise (34-digit rounding, exactly 2 per P03's X=2); the E key
located (ENTER row, between +/- and <-) and E-notation taught both ways; "very large numbers
switch the same way" cut as unshown; ALL's limit stated; "the same setup as before" corrected to
rpn-01's.

The self-audit before the run found an unbacked "the display showed 0.78" (now E02A with a quoted
display) and a gap in check.py's screen-word list ("showed" was missing; added, with a control).

## Checks

`make check` at 867ddd5: 11/11 vectors in 33s and 35s, from a fresh and a used core; 12 keys
blocks, 11 of 11 vectors shown, pressed in both modes; 11 displays quoted, each verified at its
example's final setting and on the device's X line. Controls: rpn-03 2/2 red, 1/1 green (rpn-01
30/30 and 4/4, rpn-02 5/5 and 1/1).
