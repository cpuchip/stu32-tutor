# factor-02 evidence: common factors and multiples (pre-algebra unit 3)

## Expected values

Oracle: build/proto/factor02.py, against math.gcd and math.lcm. Asserted: 84 and 90's factorizations
and GCF 6, with 84 = (2 × 3)(2 × 7) and 90 = (2 × 3)(3 × 5); both factor lists and their common factors
1, 2, 3, 6; 12 and 18's LCM 36, and nothing smaller a multiple of both; the exercises GCF(24, 36) =
12, LCM(4, 10) = 20 and LCM(6, 8) = 24 with their listing checks, and GCF(8, 15) = 1 with LCM 120.
12 examples in both entries, 12 display vectors.

## Non-author read (2026-10-09)

All values correct. Taken: "14 and 15 share no prime, so 6 really is the greatest" did not prove it
(it rules out only multiples of 6): now a cross-check by listing both numbers' factors; "as many times
as both have them" was ambiguous: now the smaller count for the GCF and the larger for the LCM, the
rule the exercises need; "today" given a day number (day 0); multiples as 12 × 1, 12 × 2; "common"
defined; exercise 1 checks both numbers, the LCM answers check by listing, and a GCF of 1 case added.
Raised to abacus, not changed here: lesson ids like "(whole-02)" in a young reader's text.

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): the LCM one 3 short; the
box count misquoted; INT÷ for Rmdr; RPN's LCM missing a factor. All red.
