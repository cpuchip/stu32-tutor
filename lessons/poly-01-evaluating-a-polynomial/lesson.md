---
id: poly-01
title: Evaluating a polynomial
requires: setup shift-keys enter-copies stack-lift t-copies-down change-sign stack-full function program-entry xeq-program stopped-program
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Evaluating a polynomial

A polynomial adds up terms, each a number times a power of x: x, x², x³ and so on, plus a term with
no x at all, the constant term. The numbers are its coefficients. p(x) = 2x³ − 3x² + 4x − 5 has the
coefficients 2, −3 and 4, and the constant term −5. Its degree is the highest power with a
coefficient that is not 0, here 3. q(x) = x² − 4x + 3 from fn-02 has degree 2, and the lines of
lin-01 to lin-03 are polynomials of degree 1 (or 0, for a flat line). This lesson works out a
polynomial's value with very few keys, by a method that uses the stack the way rpn-01 taught it.

## From before

Two from before, by hand: one from unit 1, and one function from fn-01.

```item PL1F1
prompt: Work out 2 × 3³.
topics: powers-first
answer: type
calculator: no
slip: PL1F1A | cubed 2 × 3 | The power belongs to the 3 alone: 3³ is 27, then 2 × 27.
```

```item PL1F2
prompt: h(x) = 3 − x². What is h(2)?
topics: function
answer: type
calculator: no
slip: PL1F2A | took 2 from 3, then squared | Square first: 2² is 4, then 3 − 4.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. The worked example in "On the stack" is one chain, each
step carrying on from the one before, and so is the program and its runs. Everything else starts
fresh. If a program is still stopped from fn-03, press GOLD GTO . . before you key in P, as the last answer
in fn-03 says.

<mode m="35s,STU">In this mode XEQ and GTO wait, after the label's letter, for ENTER; the keys
below show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Nesting

Working out 2x³, 3x² and 4x one at a time takes many keys and a place to keep each term. There is a
shorter way. Each of the first three terms has at least one x in it, so x can be taken out of them
as a common factor:

p(x) = (2x² − 3x + 4)x − 5.

The first two terms inside the parentheses still have an x each, so take it out again:

p(x) = ((2x − 3)x + 4)x − 5.

Multiply the parentheses out again (2x − 3 times x is 2x² − 3x, and so on) and the first form comes
back. Now read the nested form from the inside: start with the first coefficient, 2; times x, then
add the next coefficient, −3, which is the same as subtracting 3; times x, add 4; times x, add −5.
Every step is "times x, then add the next coefficient". Working a polynomial out this way, from the
inside of its nested form, is called Horner's method. It needs x again and again, and the stack can
supply it.

## On the stack

rpn-01 showed that when the stack drops, T keeps its number and copies it down. So fill the stack
with x, and every × finds a copy of x waiting in Y. Work out p(4). Fill the stack with 4, then type
the first coefficient:

```keys H01A
4 ENTER ENTER ENTER 2
```

X shows <disp v="H01A" kind="entry">2_</disp>, and Y, Z and T each hold 4: the third ENTER left a
copy of 4 in X, and the 2 you typed replaced it. Now × gives 2 × 4, and the stack drops, T copying
its 4 down, so Y, Z and T hold 4 again. Then type the next coefficient, 3:

```keys H01C after=H01A
× 3
```

X shows <disp v="H01C" kind="entry">3_</disp>. Typing 3 lifted the stack: the 8 went up to Y, one 4
went up to T, and the 4 that was in T fell off the top, as in num-01. Only Z and T hold 4 now. Then −
takes the 3 from the 8, and the stack drops, T copying its 4 down once more:

```keys H01B after=H01C
−
```

X shows <disp v="H01B">5.0000</disp>, which is 2 × 4 − 3, and 4 is in Y, Z and T again. The first
coefficient only replaced the copy ENTER left in X; each later coefficient you type pushes one 4 off
the top, and the drop that follows has T copy one back, so the supply of 4s never runs out. The rest goes the same way: times x, add 4; times x, take away 5.

```keys H01 after=H01B
× 4 + × 5 −
```

X shows <disp v="H01">91.0000</disp>: 5 × 4 + 4 is 24, and 24 × 4 − 5 is 91. Check it the long way if
you like: 2 × 64 − 3 × 16 + 4 × 4 − 5 = 128 − 48 + 16 − 5 = 91.

The same keys work for any x. p(2), all at once:

```keys H02
2 ENTER ENTER ENTER 2 × 3 − × 4 + × 5 −
```

X shows <disp v="H02">7.0000</disp>: 16 − 12 + 8 − 5.

## As a program

The keys after the number never change, so they make a program, as in fn-01. You start a program
with x in X, so its three ENTERs fill the stack with x the same way. P is on the E key:

```keys P01A
GOLD PRGM PRGM GOLD LBL P ENTER ENTER ENTER 2 × 3 − × 4 + × 5 − BLUE RTN
```

The X line shows <disp v="P01A" kind="program">P015 RTN</disp>: fifteen lines. Turn program entry
off:

```keys P01 after=P01A
GOLD PRGM PRGM
```

Now any value is a number and XEQ P. p(1.5):

```keys P02 after=P01
1.5 XEQ P
```
```keys P02 after=P01 mode=35s,STU
1.5 XEQ P ENTER
```

X shows <disp v="P02">1.0000</disp>: 2 × 3.375 − 3 × 2.25 + 4 × 1.5 − 5 is 6.75 − 6.75 + 6 − 5. And
p(−1):

```keys P03 after=P02
1 +/− XEQ P
```
```keys P03 after=P02 mode=35s,STU
1 +/− XEQ P ENTER
```

X shows <disp v="P03">-14.0000</disp>: −2 − 3 − 4 − 5.

## Exercises

r(x) = x³ − 2x + 1 has no x² term. In the nested form a missing power has the coefficient 0, so the
coefficients in order are 1, 0, −2 and 1, and r(x) = ((1x + 0)x − 2)x + 1.

1. Work out r(2) on the stack, keying every coefficient in order, the 1 and the 0 too.
2. Write r as a program N (N is on the x↔y key; your calculator may still hold other lessons'
   programs, and N is a letter none of them used). Then work out r(0.5) with it.

## Answers

1. Fill the stack with 2, and start with the coefficient 1:

   ```keys E01
   2 ENTER ENTER ENTER 1 × 0 + × 2 − × 1 +
   ```

   X shows <disp v="E01">5.0000</disp>: 8 − 4 + 1. The 1 × and the 0 + change nothing, and you could
   skip them, but keying every coefficient in order is what keeps a longer polynomial from going
   wrong.

2. The program:

   ```keys E02A
   GOLD PRGM PRGM GOLD LBL N ENTER ENTER ENTER 1 × 0 + × 2 − × 1 + BLUE RTN
   ```

   The X line shows <disp v="E02A" kind="program">N015 RTN</disp>. Then:

   ```keys E02 after=E02A
   GOLD PRGM PRGM 0.5 XEQ N
   ```
   ```keys E02 after=E02A mode=35s,STU
   GOLD PRGM PRGM 0.5 XEQ N ENTER
   ```

   X shows <disp v="E02">0.1250</disp>: 0.125 − 1 + 1.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item PL1M1
prompt: What is the constant term of 5x³ − x + 8?
topics: polynomial
answer: type
calculator: no
working: none
slip: PL1M1A | the first coefficient | The constant term is the one with no x: the 8.
```

```item PL1M2
prompt: Work out √(2 × 18).
topics: square-root
answer: type
calculator: no
slip: PL1M2A | halved instead of taking the root | 2 × 18 is 36, and √36 is 6, since 6 × 6 is 36.
```

```item PL1M3
prompt: 2x² − x + 4 nested is (2x − 1)x + 4. Work it out at x = 3, from the inside.
topics: horner
answer: type
calculator: no
slip: PL1M3A | dropped the brackets | From the inside: 2 × 3 − 1 is 5, then 5 × 3 + 4.
```

```item PL1M4
prompt: 5x − 15 < 0 has its boundary where 5x − 15 = 0. What x is that?
topics: inequalities
answer: type
calculator: no
slip: PL1M4A | kept the minus sign | Undo the − 15 by adding 15: 5x = 15, then ÷ 5.
```
