# cnt-01 evidence: counting

## Expected values (2026-10-07, core c7ab388)

Oracle: build/proto/cnt01.py, Python's exact factorial, comb and perm; 52! (68 digits) rounded once to
34 digits, half even. 13/13 vectors, 11/11 display vectors. n!, Cn,r and Pn,r give the same in 33s,
35s and STU mode (probed).

| Vector | What | Value |
|---|---|---|
| M01 | 3 × 4 × 2 outfits | 24 |
| F01, F02, F03 | 5!, 52!, 0! | 120; 8.065817517094387857166063685640377E+67 (shown 8.0658E67); 1 |
| P01 | P(10, 3) = 10 × 9 × 8 | 720 |
| C01, C02 | C(10, 3) = 720 ÷ 3!; C(52, 5) | 120; 2,598,960 |
| C03, C03B | C(2, 5): INVALID DATA; C leaves 5 in X, 2 in Y | message; 5, 2 |
| E01..E04 | 10⁴; 6!; C(8, 3); P(12, 3) | 10,000; 720; 56; 1,320 |

The first oracle asserted a 52! digit string written from memory; it was wrong in its last digit
(…376 for …377) and the assert stopped it. It now asserts only what it computes: 68 digits, exponent
67, 34 kept, within half a unit of the exact integer, and the core's value is compared with that.

## Sources and probes

- n! gold above ×; the PROB menu blue above ×, its soft keys Cn,r Pn,r n! RAND SEED (firmware
  keymap.c "PROB"); n in Y, r in X; r > n gives INVALID DATA (probed in all three modes).

## Non-author read (2026-10-07)

All 13 vectors agreed with the quotes; 52!'s rounding checked by hand. Taken:
- The multiplying rule's condition "the choices do not limit each other" is broken by the very next
  section (the 4 left): now "each step has the same number of choices whatever was picked before".
- P and C assume nothing is picked twice: said.
- "No way to choose 5 from 2" means 0 ways, but the calculator refuses: both said.
- 0! = 1 "keeps the rules working" leaned on n! ÷ (n − r)!, never stated: P(n, r) = n! ÷ (n − r)! is now
  derived from 10! = 10 × 9 × 8 × 7!, and 0! = 1 follows from P(n, n) = n!.
- Exercise 1's trap: the summary's two questions lead to P(10, 4) = 5040 for a code whose digits repeat;
  the summary now starts with "can a choice repeat? multiply", and the exercise says digits may repeat.
- "three rules" against "two questions" against four tools: made one account.
- The too-big case of scientific form is rpn-01's sentence as well as rpn-03's section: both cited;
  `display-rounds` added to requires.
- PROB said to be short for probability, and Cn,r and Pn,r tied to C(n, r) and P(n, r); "again"
  dropped from C03B (5.0000 was never shown before); "3 chosen from 10, in order"; "too long for the
  screen at FIX 4"; exercise 3's "different three-topping pizzas"; 1,320 with its comma.

## Checks

`make check`: 13/13 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (3): a team counted with Pn,r, n and r reversed, 52! quoted with one power
of ten too many; all red.
