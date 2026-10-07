# lin-02 evidence

## Expected values (2026-10-06, core 25dca53)

Data (ours): a seedling at the end of weeks 1-5, 3 5 6 8 11 cm. The oracle is build/proto/lin02.py:
exact fractions for m, b, ŷ and x̂ (rounded once to 34 digits), and r as the square root of the
exact r² at 60 digits, rounded to 34. Every value below matched the core to all 34 digits.

| Vector | What | Exact |
|---|---|---|
| D01, D02 | Σ+ of the five points | n 1, then 5 |
| D03 | m | 19/10 = 1.9 |
| D04 | b | 9/10 = 0.9 |
| D04B | ŷ at week 3 (measured 6) | 6.6 |
| D05 | r | 0.9851041099939040049432289779635516 |
| D06 | ŷ at week 6 | 12.3 |
| D07 | x̂ at 15 cm | 141/19 = 7.421052631578947368421052631578947 |
| W01A, W01 | the last point twice: n 6, m | 1.975 |
| W02A, W02 | Σ− of the copy: n 5, m | 1.9 |
| E01-E01C | 4 6 7 10 13: m, b, ŷ(6) | 2.2, 1.4, 14.6 |
| E02, E02B | a tank 10 8 7 4 over hours 1-4: r, m | -0.9811557810392122775787472346115412, -1.9 |

## Sources and probes

- Keys (keymap.c, keys numbered row x 6 + column): Σ+ is key 11, the last of the top row, Σ− gold
  above it; CLEAR is gold above ← and its Σ soft key is CLΣ; L.R. is blue above + (x̂ ŷ r m b).
- The L.R. labels are y and x with a combining circumflex (U+0302); a lesson must print them so or
  resolve refuses the name (told to abacus #4442, passed to primer).
- Σ+ reads x from X and y from Y, and answers with n (D01, W01A); Σ− answers with n (W02A).
- Σ− of a point never entered (the lesson's warning): probed with the vector runner at 25dca53,
  CLΣ, (1, 3) and (2, 5) in, then Σ− of (7, 99): n is 1 and Σy is -91 (2/2). Kept in
  build/proto/sigminus.txt; not in the lesson's vectors, since a student should not do it.
- A first-draft mistake caught by the oracle's eye: a wrong point at x = 3, the mean of the x
  values, leaves the slope unchanged (1.9), so it showed nothing; the mistake became the last point
  entered twice.

## Non-author read (2026-10-06)

Eleven findings, all taken. The largest: "near 0, no line describes them well" was wrong (a tight
band on a flat line, or a U-shaped curve, gives r near 0); r is now "how well a sloping line fits",
with the flat and curved cases named (lin-03 shows the curve). The intercept read as week 0, which
is outside the data and was called "the day the measuring began"; x̂ at 15 cm is outside it too,
and the lesson now says estimates between the measured weeks are safest. "Closest" is shown with
one point's distance (D04B: the line 6.6, the measurement 6) and why squares are used. Σ and the hat
defined; L.R. named as linear regression and the least-squares line; Σ− warned (the probe above)
with the count shown after Σ+ and Σ−; r and m sharing a sign said; the y-first order explained;
the chain sentence made exact; the seedling's speeding growth noted.

## Checks

`make check`: 17/17 vectors in 33s and 35s, from a fresh and a used core; 18 keys blocks; 17
quotes, each on the device and again in the in-order run. Controls: a point entered x first, the
sums not cleared first, r quoted with the falling set's sign, Σ− without the point's values; all red.

## Abacus's accuracy read (#4446, 2026-10-06)

Every value recomputed in exact fractions and matched (the doubled point's m is 79/40). One fix:
"near 0 ... or lie on a flat line" was wrong, since points exactly on a flat line have no r (0 ÷ 0;
STAT ERROR, probed by abacus and by me on 25dca53; the 33s guide's STAT ERROR entry is p.F-4). Our
own lin-03 read had found the same. Now "spread along a flat line" for near 0, and a sentence that
exactly flat points have no r, which lin-03 shows with a vector (F01). Statements (1)-(5) otherwise
confirmed; the sums also survive power-off, and CLEAR ALL clears them (not claimed).
