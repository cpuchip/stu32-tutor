---
id: poly-04
title: Complex roots
requires: setup shift-keys soft-keys enter-copies stack-levels x-squared square-root clear-message root-count horner horner-stack quadratic quadratic-formula discriminant double-root negative-discriminant
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Complex roots

poly-03 left x² + 2x + 5 with a discriminant of −16 and no real root, because no real number squares
to a negative. This lesson brings in a new number that does, and with it finds the two roots the
quadratic formula was pointing at.

## From before

Two from before, by hand: a discriminant from poly-03, and one from unit 1.

```item PL4F1
prompt: What is the discriminant b² − 4ac of x² + 2x + 2?
topics: discriminant
answer: type
calculator: no
slip: PL4F1A | added the 4ac | It is b² minus 4ac: 4 − 8.
```

```item PL4F2
prompt: Work out √16 ÷ 2.
topics: square-root
answer: type
calculator: no
slip: PL4F2A | halved instead of taking the root | √16 is 4, since 4 × 4 is 16. Then 4 ÷ 2.
```

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

<mode m="35s,STU">The calculator keeps both parts of a complex number in one stack level. To type one,
type the real part, then press CMPLX (blue above +/−), which opens a menu like MODE in rpn-01, and
press the soft key under i; then type the imaginary part. (This is the HP 35s's way, and STU mode's.
An HP 33s keeps the two parts as a pair of numbers on the stack instead, and so does 33s mode.) i
itself is 0 + 1i:</mode><mode m="33s">In this mode, as on an HP 33s, a complex number is a pair of
numbers on the stack: its imaginary part in Y and its real part in X. To type one, type the imaginary
part, press ENTER, then type the real part. Two complex numbers fill the four levels:

    T: the first one's imaginary part     Z: the first one's real part
    Y: the second one's imaginary part    X: the second one's real part

To work on them, press CMPLX (blue above +/−) just before the operation: CMPLX + adds the two, CMPLX ×
multiplies them, and CMPLX ÷ divides the first complex number typed by the second, as ÷ divides Y by X.
The answer is left as a pair, real part in X and imaginary part in Y, with the first number kept in Z
and T. (The HP 35s, and 35s and STU mode, keep a complex number in one stack level instead.) i itself
is 0 + 1i, so its pair is 1 ENTER 0:</mode>

```keys C01A
0 BLUE CMPLX i 1
```
```keys C01A mode=33s
1 ENTER 0
```

<mode m="35s,STU">X shows <disp v="C01A" kind="entry">0i1_</disp>. Read it carefully: the calculator
puts its i between the two parts, so the number before the i is the real part and the number after it
is the imaginary part. 0i1 means 0 + 1i, and −1.0000i2.0000 would mean −1 + 2i, not "−1i, then 2". Now
square i. x² and √x do not take a complex number (more on that below), so multiply it by itself with
ENTER ×:</mode><mode m="33s">X shows <disp v="C01A" kind="entry">0_</disp>, the real part being typed,
with the imaginary part, 1, in Y. Now square i: ENTER and i's pair again, which puts the two pairs in
the four levels, i in Z and T and i in Y and X; then CMPLX ×:</mode>

```keys C01 after=C01A
ENTER ×
```
```keys C01 after=C01A mode=33s
ENTER 1 ENTER 0 BLUE CMPLX ×
```

X shows <disp v="C01" m="35s,STU">-1.0000i0.0000</disp><disp v="C01" m="33s">-1.0000</disp><mode m="33s">,
the real part, and Y holds 0, the imaginary part</mode>: −1 + 0i, which is −1. Now 4i times 4i:

```keys C02
0 BLUE CMPLX i 4 ENTER ×
```
```keys C02 mode=33s
4 ENTER 0 ENTER 4 ENTER 0 BLUE CMPLX ×
```

X shows <disp v="C02" m="35s,STU">-16.0000i0.0000</disp><disp v="C02" m="33s">-16.0000</disp><mode m="33s">,
and Y holds 0 (4i's pair is 4 ENTER 0, typed twice with ENTER between)</mode>. So 4i is a square root of −16, and so is −4i, since (−4i)² is 16 × i × i too. The
same works for any negative number: for d greater than 0, (√d × i)² = d × i × i = −d. So −d has the
two square roots √d × i and −√d × i, and √(−d) is taken to mean the first, √d × i, as √ of a positive
number means the positive root. √(−16) = 4i, √(−20) = √20 × i, and so on.

<mode m="35s,STU">The calculator will not take that square root for you. √x on a complex number:

```keys V01
16 +/− BLUE CMPLX i 0 √x
```

The screen shows <disp v="V01" kind="message">INVALID DATA</disp>. Clear it with C before you go on (in
this mode a key pressed over a message only clears it):

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

</mode><mode m="33s">√x and x² work on the number in X alone, a real number, and there is no complex
square root key, so the calculator will not take that square root for you.</mode> So work out
√(−d) as √d × i yourself, and type it as a complex number.

## The roots of x² + 2x + 5

The formula gives (−b ± √D) ÷ (2a), with a = 1, b = 2 and D = −16 from poly-03. With 4i for √D, the
roots are (−2 + 4i) ÷ 2 and (−2 − 4i) ÷ 2. <mode m="35s,STU">On the stack: −2, ENTER, then 4i typed as
0 i 4, then add (a real plus a complex number is complex), then divide by 2:</mode><mode m="33s">Type
−2 + 4i as its pair, 4 ENTER 2 +/−; then ENTER, and 2 as the pair 0 ENTER 2 (2 + 0i); then CMPLX ÷
divides the first by the second:</mode>

```keys R01
2 +/− ENTER 0 BLUE CMPLX i 4 + 2 ÷
```
```keys R01 mode=33s
4 ENTER 2 +/− ENTER 0 ENTER 2 BLUE CMPLX ÷
```

X shows <disp v="R01" m="35s,STU">-1.0000i2.0000</disp><disp v="R01" m="33s">-1.0000</disp><mode m="33s">
and Y holds 2</mode>: −1 + 2i. And <mode m="35s,STU">with − for the other</mode><mode m="33s">with −4 for
the imaginary part, the other</mode>:

```keys R02
2 +/− ENTER 0 BLUE CMPLX i 4 − 2 ÷
```
```keys R02 mode=33s
4 +/− ENTER 2 +/− ENTER 0 ENTER 2 BLUE CMPLX ÷
```

X shows <disp v="R02" m="35s,STU">-1.0000i-2.0000</disp><disp v="R02" m="33s">-1.0000</disp><mode m="33s">
and Y holds −2</mode>: −1 − 2i.

The two roots differ only in the sign of their imaginary part. Such a pair is called a complex
conjugate pair. For a quadratic with real coefficients and a negative discriminant this always
happens: −b ÷ (2a) is real, √D is a real number times i, and the ± adds and subtracts it, giving
a pair of the form p + qi and p − qi. (The complex roots of any polynomial with real coefficients come in conjugate
pairs; that needs more than the formula to show.)

## Checking a root

A root makes the polynomial 0. <mode m="35s,STU">Put −1 + 2i into x² + 2x + 5 with the Horner
keys of poly-01: fill the stack with it, then 1 ×, 2 +, ×, 5 +. The stack holds a complex number in each level
just as it holds a real one, so the same keys work. Here +/− comes before the i, so it makes the real
part negative:</mode><mode m="33s">Put −1 + 2i into x² + 2x + 5. Horner's keys need a complex number in
every stack level, and here a pair takes two levels, so work it out term by term instead. x² is z × z:
the pair 2 ENTER 1 +/−, ENTER, the pair again, and CMPLX ×. Then add 2z: twice each part, worked out in
your head, is −2 + 4i, typed as 4 ENTER 2 +/−. A result moves up when you type the next number
(rpn-01), and a pair is two numbers, so typing it pushes the square up two levels, into Z and T, with
no ENTER needed first; CMPLX + then adds the two. Then add 5, typed as the pair 0 ENTER 5:</mode>

```keys H01
1 +/− BLUE CMPLX i 2 ENTER ENTER ENTER 1 × 2 + × 5 +
```
```keys H01 mode=33s
2 ENTER 1 +/− ENTER 2 ENTER 1 +/− BLUE CMPLX × 4 ENTER 2 +/− BLUE CMPLX + 0 ENTER 5 BLUE CMPLX +
```

X shows <disp v="H01" m="35s,STU">0.0000i0.0000</disp><disp v="H01" m="33s">0.0000</disp><mode m="33s">
and Y holds 0</mode>: 0, so −1 + 2i is a root. <mode m="35s,STU">For the other root both parts are
negative: +/− before the i for the real part, and +/− after the 2 for the imaginary part:</mode><mode m="33s">
For the other root, −1 − 2i, both parts of the pair are negative:</mode>

```keys H02A
1 +/− BLUE CMPLX i 2 +/−
```
```keys H02A mode=33s
2 +/− ENTER 1 +/−
```

X shows <disp v="H02A" kind="entry" m="35s,STU">-1i-2_</disp><disp v="H02A" kind="entry" m="33s">-1_</disp><mode m="33s">,
the real part being typed, and Y holds −2</mode>: −1 − 2i. Now <mode m="35s,STU">the same Horner keys</mode><mode m="33s">ENTER, the pair again, and the
same terms: z × z, then 2z, which is −2 − 4i, then 5</mode>:

```keys H02 after=H02A
ENTER ENTER ENTER 1 × 2 + × 5 +
```
```keys H02 after=H02A mode=33s
ENTER 2 +/− ENTER 1 +/− BLUE CMPLX × 4 +/− ENTER 2 +/− BLUE CMPLX + 0 ENTER 5 BLUE CMPLX +
```

X shows <disp v="H02" m="35s,STU">0.0000i0.0000</disp><disp v="H02" m="33s">0.0000</disp><mode m="33s">
and Y holds 0</mode>. Both roots check. Counted with complex numbers, a polynomial of degree n, for n of
1 or more, always has exactly n roots, when a root that repeats is counted as many times as it
repeats: a double root twice, a triple root three times. Among the real numbers it can have fewer, as
x² + 2x + 5 has none.

## Exercise

x² − 4x + 13 has a = 1, b = −4 and c = 13. Work out its discriminant by hand, find its two complex
roots with the formula, and check one of them <mode m="35s,STU">with Horner's keys</mode><mode m="33s">term
by term</mode>.

## Answer

The discriminant is 16 − 52 = −36, so √D = √36 × i = 6i. The roots are (4 ± 6i) ÷ 2:

```keys E01
4 ENTER 0 BLUE CMPLX i 6 + 2 ÷
```
```keys E01 mode=33s
6 ENTER 4 ENTER 0 ENTER 2 BLUE CMPLX ÷
```

X shows <disp v="E01" m="35s,STU">2.0000i3.0000</disp><disp v="E01" m="33s">2.0000</disp><mode m="33s">
and Y holds 3</mode>: 2 + 3i.

```keys E02
4 ENTER 0 BLUE CMPLX i 6 − 2 ÷
```
```keys E02 mode=33s
6 +/− ENTER 4 ENTER 0 ENTER 2 BLUE CMPLX ÷
```

X shows <disp v="E02" m="35s,STU">2.0000i-3.0000</disp><disp v="E02" m="33s">2.0000</disp><mode m="33s">
and Y holds −3</mode>: 2 − 3i. Check 2 + 3i<mode m="35s,STU">, with 1 ×, then −4 as 4 −, then 13
+</mode><mode m="33s">: z × z, then −4z, which is −8 − 12i (worked out in your head), then 13</mode>:

```keys E03
2 BLUE CMPLX i 3 ENTER ENTER ENTER 1 × 4 − × 13 +
```
```keys E03 mode=33s
3 ENTER 2 ENTER 3 ENTER 2 BLUE CMPLX × 12 +/− ENTER 8 +/− BLUE CMPLX + 0 ENTER 13 BLUE CMPLX +
```

X shows <disp v="E03" m="35s,STU">0.0000i0.0000</disp><disp v="E03" m="33s">0.0000</disp><mode m="33s">
and Y holds 0</mode>.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item PL4M1
prompt: i × i is what real number?
topics: complex
answer: type
calculator: no
working: none
slip: PL4M1A | lost the sign | i is defined by one rule: i × i = −1.
```

```item PL4M2
prompt: Work out (−2 + 6) ÷ 2.
topics: fraction-bar
answer: type
calculator: no
slip: PL4M2A | divided only the 6 | The bracket comes first: −2 + 6 is 4, then ÷ 2.
```

```item PL4M3
prompt: What is the real part of the roots of x² − 4x + 13?
topics: complex-roots
answer: type
calculator: no
slip: PL4M3A | the sign of −b | The real part is −b ÷ 2a, and −b is −(−4), which is 4.
```

```item PL4M4
prompt: x² − 10x + 25 has one root. What is it?
topics: double-root
answer: type
calculator: no
slip: PL4M4A | the sign of −b | The root is −b ÷ 2a, and −b is −(−10), which is 10.
```

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP5A
prompt: What is the discriminant b² − 4ac of x² + 4x + 13?
topics: discriminant
answer: type
calculator: no
slip: CP5A1 | added the 4ac | It is b² minus 4ac: 16 − 52.
slip: CP5A2 | the order turned round | The b² comes first: 16 − 52, not 52 − 16.
```

```item CP5B
prompt: What is the larger root of x² − 7x + 10?
topics: root quadratic-formula
answer: type
calculator: no
slip: CP5B1 | the smaller root | That is the other root. (7 ± √(49 − 40)) ÷ 2 gives 5 and 2; the larger is 5.
slip: CP5B2 | the sign of −b | In the formula −b is −(−7) = 7, so the roots are (7 ± 3) ÷ 2, both positive.
```

```item CP5C
prompt: Evaluate 2x³ − x + 1 at x = 2.
topics: polynomial
answer: type
calculator: no
slip: CP5C1 | cubed the 2x | The 2x³ is 2 times x³: cube x first, 2³ = 8, then double it.
slip: CP5C2 | took the 1 away | It is plus 1 at the end.
```
