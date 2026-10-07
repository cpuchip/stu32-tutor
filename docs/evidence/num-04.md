# num-04 evidence

## Expected values (2026-10-06)

Exact fractions in Python, independently of the core:

| Vector | Computation | Exact |
|---|---|---|
| C01 | 15/100 x 80, Y kept | X 12, Y 80 |
| C02 | 80 + 12 | 92 |
| C03 | 60 - 25/100 x 60 | 45 |
| C04 | (65 - 50) / 50 x 100 | 30 |
| C05 | (60 - 80) / 80 x 100 | -25 |
| C06 | 4 x 10^-3 | 0.004 |
| C07 | 6 x 10^5 x 4 x 10^-3 | 2400 |
| C09 | 9 x 10^-6 / (3 x 10^2) | 3 x 10^-8 |
| C08, C08B | 3.2 x 10^12 x 2.5 x 10^9 | 8 x 10^21 |
| E01 | 12/100 x 250 | 30 |
| E02 | (46 - 40) / 40 x 100 | 15 |
| E03 | 2.5 x 10^6 x 4 x 10^-2 | 100000 |

Displays, each at the setting its example ends in, all as predicted before the run: 92.00, 30.00,
-25.00, 4.00E-3 (FIX 2 switching to scientific form for 0.004), 2,400.00, 3.00E-8, 8.00E21 (SCI 2),
30.00, 100,000.00.

## The core's behaviour this lesson relies on (867ddd5, all vectors)

- % gives X percent of Y and keeps Y (C01: Y 80), so + or - next applies it (C02, C03).
- %CHG gives the change from Y to X as a percent of Y, signed (C04 +30, C05 -25).
- +/- pressed after E while typing changes the exponent's sign (C06: 4 E 3 +/- is 0.004).
- Key positions (layout v0): % gold and %CHG blue on the 1/x key.

## Student run

~~C08 sets SCI 2 for its answer; C08B (a continuation) sets FIX 2 again, so the exercises' quoted
displays hold for a student working in order.~~ (Superseded by the non-author read below: FIX 2
already shows 8 x 10^21 in scientific form, so C08's SCI 2 and C08B were cut.) The hypothetical "0.004 would show as 0.00" was
flagged by the untagged-display check and reworded.

## Non-author read (2026-10-06)

Every answer and key legend checked by the reader. Findings, each probed on the core before the
prose changed (867ddd5):

- % keeping Y was mentioned in passing though every earlier lesson taught that a two-number
  operation drops the stack. Probed: % leaves Y, Z and T where they were (C00: X 12, Y 80, Z 2,
  T 1), and so does %CHG (C04 now checks Y 50). Both now said; C02 continues C00 and checks the
  drop (Y 2).
- %CHG had no formula; now (X - Y) / Y x 100, worked. The asymmetry the reader suggested is
  exercise 5: 60 to 80 is +33.33% (34 digits: 33.33333333333333333333333333333333) where 80 to 60
  was -25%.
- **"SCI is the clearer display" had nothing behind it:** probed, FIX 2 already shows 8 x 10^21 as
  8.00E21. The SCI example and its FIX 2 hand-back were cut; C08 now shows the switch at FIX 2.
- +/- before E: probed, 4 +/- E 3 is -4000 (C06B, shown as the slip it is).
- A way to check powers of ten in the head (multiply the fronts, add the powers; divide and
  subtract), used in C07, C09, C08 and exercise 3. "A tiny number divided by a large one" (300)
  became "a bigger one". Exercise 4 practises the discount; answers 2 and 3 now say enough.
- Prose: "more than any others" and "everyday work" dropped; "works with money" scoped to the
  percents; the percent keys located on the 1/x key, fifth in the top row.

## Checks

`make check` at 867ddd5: 16/16 vectors and 22/22 expectations in 33s and 35s, from a fresh and a
used core; 17 keys blocks, 16 of 16 shown, pressed in both modes; 13 displays quoted; worked
through in order.

## Abacus's accuracy read (#4323, 2026-10-06)

All values right; key positions match keymap.c. One fix: C08's reason. FIX falls back to
scientific form when the text will not fit the X line's 21 characters (screen.c FMT_WIDTH), not
because of its two places; 8 x 10^21 written out at FIX 2 is 32 characters. The prose now says so.
Abacus confirmed % and %CHG preserve Y per the 33s manual (p.4-6) and the %CHG formula. Unit 1
complete.
