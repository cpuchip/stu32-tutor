# num-02 evidence

## Expected values (2026-10-06)

Python's decimal module at 34 digits, half even, with Python fractions to judge exactness:

| Vector | Computation | 34 digits | Against the fraction |
|---|---|---|---|
| G01 | 3/8 | 0.375 | exact |
| G02, G03, G07 | 2 3/8 | 2.375 | exact |
| G05 | 5 3/8 + 2 7/16 | 7.8125 | exact (7 13/16) |
| G06 | 3/4 x 2/3 (2/3 stored ...67) | 0.5000000000000000000000000000000000 | exact (1/2) |
| G04, G08 | 1/2 + 1/3 (1/3 stored ...33) | 0.8333333333333333333333333333333333 | below 5/6 |
| E01 | 2/3 + 1/6 (both stored ...67) | 0.8333333333333333333333333333333334 | above 5/6 |
| E02 | 1 1/2 x 2 2/3 (2 2/3 stored ...67) | 4.000000000000000000000000000000000 | exact (a tie, half even) |

The non-author reader re-derived every above/below claim by hand and agreed.

## Sources and probes (core 867ddd5)

- Fraction entry, Fraction display, the default maximum denominator 4095 and FIX turning
  Fraction display off: abacus-firmware work/007-fractions.md and its vectors (M13, M22, M23).
- The device's X line shows the fraction without its indicator ("0 5/6"); the indicator is drawn in
  the status band as ▼ or ▲ (firmware/screen.c, status text). The display runner's text carries it
  as " v" or " ^". check.py now ties the two.
- The status band also showed "--:--" (the clock, unset) and "33" (the mode) in every probe.
- →FRAC is blue above the point key; FRAC (a menu) is blue above E (layout v0, keymap).

## Non-author read (2026-10-06)

Eight findings, all taken. The biggest: Fraction display is a toggle, so a student working
straight through got wrong screens from G05 on (G03 left it on; each later →FRAC turned it off).
The lesson now turns it on once, keeps it on through continuation blocks, turns it off before the
exercises, and says so; the new student run in check.py confirms what that student sees. Also:
G06's exact 1/2 explained; "closest fraction" given its limit (bottom at most 4095); →FRAC told
apart from the FRAC menu; the typing rule for the digits between the points; "Back to decimals"
moved up beside the toggle; a whole number's display (4); the status band introduced.

## Checks

`make check` at 867ddd5: 10/10 vectors in 33s and 35s, from a fresh and a used core; 11 keys
blocks; 11 quotes (9 displays, 2 status arrows), each on the device, and all again for a student
working through in order. Controls: 4/4 red, 1/1 green.

## Abacus's accuracy read (#4301, 2026-10-06)

Values right, and the arrows' meaning and the 4095 default match the 33s guide (p.5-3 and p.5-2; the FIX/SCI/ENG/ALL sentence is p.5-1,
per abacus). Two fixes, taken. E02's reason was wrong: 1.5 x 2.666...667 is 4.000...0005, exactly
half a unit, a tie that half-even rounds to 4; "too small to survive the rounding" was G06's case,
not this one. The prose now says the product lands exactly halfway and the calculator rounds a tie
to the even digit. And "choose another display setting" turns Fraction display off had no example:
G09 (continuing G07: on again, then FIX 4) now shows 2.3750 on the device's X line, which backs it
on the real path (the runner has no Fraction-display expectation to probe it).
