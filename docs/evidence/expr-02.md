# expr-02 evidence: solving by undoing (pre-algebra unit 2)

## Expected values

Oracle: build/proto/expr02.py: 3n + 5 = 20 undone (15, then 5) and checked; the wrong order shown
(20 ÷ 3 − 5 = 5/3); n ÷ 4 − 2 = 3 undone (5, then 20) and checked; the exercises 2a + 7 = 31, 5b − 3
= 32, c ÷ 3 + 4 = 10, and Tobin's 41-coin bill (12 pies), each undone and each checked, one by the
stored letter. 17 examples in both entries, 17 display vectors.

## Non-author read (2026-10-09)

All values and both stories checked. Taken: the opposite-order rule had no picture and no counter-
example (now socks and shoes, and the wrong order worked on the calculator: 1.6667, no whole pies); n
in an equation is one unknown number, not a variable that can be anything, said; an equation has an
= between its sides; ÷ before − in n ÷ 4 − 2 now follows expr-01's widened rule; one check uses STO
and RCL; a word problem among the exercises; exercise letters a, b, c, not x.

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): the × 3 undone before the
+ 5; the answer misquoted; the check adding before multiplying; the ÷ 4 undone by dividing. All red.

## Covering a part (2026-10-21, sense-making section 5, abacus #9439)

A second way to read an equation: cover the part with the letter in it and ask what it must be. The new section
retells 3n + 5 = 20 (3n covered: 15, so n = 5; prose only) and works 3 × (n + 2) − 5 = 25 with keys: the covered
part 25 + 5 = 30 (K01), the bracket 30 ÷ 3 = 10 (K02), n = 10 − 2 = 8 (K03), and the check (8 + 2) × 3 − 5 = 25
(C03), the bracket typed first since the () key comes in frac-03 (unit 5). The limit is said: the letter must
appear once (5n = 2n + 9 is the example of one it doesn't fit).

**The twin, CV1T1:** 2 × (n + 4) − 3 = 17, so the covered part is 20, the bracket 10, and n = 6. Slip A takes the
3 away: (17 − 3) ÷ 2 − 4 = 3. Slip B stops at the bracket: 10. The IDs began as K1T1, which graph.py refused because
angle-01 already has it.

**Oracle:** exact arithmetic, asserted before any vector was written (scratchpad sense_vectors.py, with the
lesson's own build/proto/pa_lib.py formatting the rows): 3 × (8 + 2) − 5 = 25, 25 + 5 = 30, 30/3 = 10, 10 − 2 = 8;
2 × (6 + 4) − 3 = 17, 20/2 − 4 = 6, (17 − 3)/2 − 4 = 3, 20/2 = 10. 4 new examples in both entries (8 vectors),
4 display vectors, and the twin's 4 in both entries (8). abacus checked the arithmetic independently (#9439).

**abacus's conditions (#9439):** brackets are written 3 × (n + 2), as expr-01 writes 3 × (4 + 5), not 3(n + 2);
the braces picture is left out until it has a generator and a check; the limit is in the lesson's text.

**Checks:** First run (all 56): red, 54/56, on three of my own faults: a why block naming 78, which P03 does not show; the twin CV1T1 naming K01 with K02 and K03 between them (it now names K03); a why block after C03 naming 20 and 30. All three fixed. Rerun at 6e51b56 on expr-02 and whole-02: make check 2/2, make controls rc 0. Three planted faults in copies under build/plant, each red for its own reason: P01 quoted 14.0000 (prose against display vector and device), CV1T1A expecting 4 (the core gave 3), and C03's RPN keys with 5 + for 5 − (keys against vector). The other 54 were green on the first run, and only these two lessons and TOPICS changed after it; graph.py passed on all 55. Then two prose fixes ("30 divided by 3"; CV1T1B's hint), and make check on the two lessons again: 2/2.
