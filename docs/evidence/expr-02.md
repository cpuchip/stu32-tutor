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
