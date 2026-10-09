# neg-01 evidence: negative numbers (pre-algebra unit 4)

## The core (be3617e; probed 2026-10-09, build/proto/p4_probe.sh)

+/− flips the sign of the number being typed, before or after its digits on the algebraic line (the
line shows `5+-8`). In both entries, digits typed after +/− keep going into the same number: `8 +/−
5` is −85 (measured on the line and on the stack); the lesson shows it as a mistake, with the fix.

## Expected values

Oracle: build/proto/neg01.py: 5 + (−8), the −85 slip, −3 + (−5), −4 − (−6), −3 − 5, and the exercises
(−7 + 10, 2 − 9, −5 − (−2), and an ordering by hand). 8 examples in both entries.

## Non-author read (2026-10-09)

All values correct. Taken: "the line" read as the number line (now "the algebraic line"); +/− flips
the sign rather than makes negative; −'s two jobs and why 5 + (−8) has brackets; the slip labelled a
mistake with the right way beside it, and shown in both entries (the reader asked whether the line
does it too: it does); RPN finishes a number with ENTER or an operation; degrees Celsius, and the
opening asks its question; "adding the positive"; −3 warmer than −8; a negative plus a negative; an
ordering exercise.

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): −3 quoted without its
sign; the slip's keys changed; taking away −6 typed as 6; the line quoted as written on paper. All red.
