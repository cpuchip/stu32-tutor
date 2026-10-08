---
id: poly-04
title: Complex roots
requires: setup shift-keys soft-keys x-squared square-root clear-message root-count horner horner-stack quadratic quadratic-formula discriminant double-root negative-discriminant
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
modes: 35s STU
modes_reason: In 33s mode, as on an HP 33s, CMPLX does not type a complex number with i (firmware 041); a 33s version, with the 33s's pairs of numbers, is to come.
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Complex roots

poly-03 left x² + 2x + 5 with a discriminant of −16 and no real root, because no real number squares
to a negative. This lesson brings in a new number that does, and with it finds the two roots the
quadratic formula was pointing at.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Most examples start fresh; where one carries on from the
one before, it says so.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## A number whose square is −1

The new number is called i, and it is defined by one rule: i × i = −1. A complex number is a real
number plus a real number times i, written a + bi. a is its real part and b its imaginary part (the
"i part"): −1 + 2i, for example, or 4i, which is 0 + 4i. The real numbers are the complex numbers
whose imaginary part is 0.

The calculator keeps both parts of a complex number in one stack level. To type one, type the real
part, then press CMPLX (blue above +/−), which opens a menu like MODE in rpn-01, and press the soft
key under i; then type the imaginary part. (Typing a complex number with i like this is the HP
35s's way, and STU mode's. An HP 33s keeps the two parts as a pair of numbers on the stack instead,
and so does 33s mode, which is why this lesson is offered in 35s and STU mode.) i itself is 0 + 1i:

```keys C01A
0 BLUE CMPLX i 1
```

X shows <disp v="C01A" kind="entry">0i1_</disp>. Read it carefully: the calculator puts its i
between the two parts, so the number before the i is the real part and the number after it is the
imaginary part. 0i1 means 0 + 1i, and −1.0000i2.0000 would mean −1 + 2i, not "−1i, then 2". Now
square i. x² and √x do not take a complex number (more on that below), so multiply it by itself
with ENTER ×:

```keys C01 after=C01A
ENTER ×
```

X shows <disp v="C01">-1.0000i0.0000</disp>: −1 + 0i, which is −1. Now 4i times 4i:

```keys C02
0 BLUE CMPLX i 4 ENTER ×
```

X shows <disp v="C02">-16.0000i0.0000</disp>. So 4i is a square root of −16, and so is −4i, since
(−4i)² is 16 × i × i too. The same works for any negative number: for d greater than 0,
(√d × i)² = d × i × i = −d, so √(−d) = √d × i. √(−16) = 4i, √(−20) = √20 × i, and so on.

The calculator will not take that square root for you. √x on a complex number:

```keys V01
16 +/− BLUE CMPLX i 0 √x
```

The screen shows <disp v="V01" kind="message">INVALID DATA</disp>. Clear it with C before you go
on<mode m="35s,STU"> (in this mode a key pressed over a message only clears it)</mode>:

```keys V01B after=V01
C
```

x² refuses a complex number the same way:

```keys V02
0 BLUE CMPLX i 1 GOLD x²
```

The screen shows <disp v="V02" kind="message">INVALID DATA</disp>. Clear it too:

```keys V02B after=V02
C
```

So work out √(−d) as √d × i yourself, and type it as a complex number.

## The roots of x² + 2x + 5

The formula gives (−b ± √D) ÷ (2a), with a = 1, b = 2 and D = −16 from poly-03. With 4i for √D, the
roots are (−2 + 4i) ÷ 2 and (−2 − 4i) ÷ 2. On the stack: −2, ENTER, then 4i typed as 0 i 4, then
add (a real plus a complex number is complex), then divide by 2:

```keys R01
2 +/− ENTER 0 BLUE CMPLX i 4 + 2 ÷
```

X shows <disp v="R01">-1.0000i2.0000</disp>: −1 + 2i. And with − for the other:

```keys R02
2 +/− ENTER 0 BLUE CMPLX i 4 − 2 ÷
```

X shows <disp v="R02">-1.0000i-2.0000</disp>: −1 − 2i.

The two roots differ only in the sign of their imaginary part. Such a pair is called a complex
conjugate pair. For a quadratic with real coefficients and a negative discriminant this always
happens: −b ÷ (2a) is real, √D is a real number times i, and the ± adds and subtracts it, giving
a pair of the form p + qi and p − qi. (The complex roots of any polynomial with real coefficients come in conjugate
pairs; that needs more than the formula to show.)

## Checking a root

A root makes the polynomial 0. Put −1 + 2i into x² + 2x + 5 with poly-01's Horner keys: fill the
stack with it, then 1 ×, 2 +, ×, 5 +. The stack holds a complex number in each level just as it holds
a real one, so the same keys work. Here +/− comes before the i, so it makes the real part negative:

```keys H01
1 +/− BLUE CMPLX i 2 ENTER ENTER ENTER 1 × 2 + × 5 +
```

X shows <disp v="H01">0.0000i0.0000</disp>: 0, so −1 + 2i is a root. For the other root both parts are
negative: +/− before the i for the real part, and +/− after the 2 for the imaginary part:

```keys H02A
1 +/− BLUE CMPLX i 2 +/−
```

X shows <disp v="H02A" kind="entry">-1i-2_</disp>: −1 − 2i. Now the same Horner keys:

```keys H02 after=H02A
ENTER ENTER ENTER 1 × 2 + × 5 +
```

X shows <disp v="H02">0.0000i0.0000</disp>. Both roots check. Counted with complex numbers, a
polynomial of degree n always has exactly n roots, a double root counted twice and a triple root
three times. Among the real numbers it can have fewer, as x² + 2x + 5 has none.

## Exercise

x² − 4x + 13 has a = 1, b = −4 and c = 13. Work out its discriminant by hand, find its two complex
roots with the formula, and check one of them with Horner's keys.

## Answer

The discriminant is 16 − 52 = −36, so √D = √36 × i = 6i. The roots are (4 ± 6i) ÷ 2:

```keys E01
4 ENTER 0 BLUE CMPLX i 6 + 2 ÷
```

X shows <disp v="E01">2.0000i3.0000</disp>: 2 + 3i.

```keys E02
4 ENTER 0 BLUE CMPLX i 6 − 2 ÷
```

X shows <disp v="E02">2.0000i-3.0000</disp>: 2 − 3i. Check 2 + 3i, with 1 ×, then −4 as 4 −, then
13 +:

```keys E03
2 BLUE CMPLX i 3 ENTER ENTER ENTER 1 × 4 − × 13 +
```

X shows <disp v="E03">0.0000i0.0000</disp>.
