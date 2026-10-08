---
id: lim-01
title: Approaching a limit
requires: setup shift-keys rpn-arithmetic enter-copies stack-lift swap-roll x-squared power reciprocal fix display-rounds type-e neg-e fraction-bar change-sign abs program-entry xeq-program stopped-program function divide-by-zero angle-unit sin-key radian ln
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Approaching a limit

Some functions have no value at a point, yet settle on a number as x comes close to it. f(x) =
(x² − 1) ÷ (x − 1) has no value at x = 1: the top and the bottom of the fraction are both 0 there,
and 0 ÷ 0 has no answer. fn-03 showed why 1 ÷ 0 has none: no number times 0 gives 1. 0 ÷ 0 fails the
other way: every number times 0 gives 0, so no one number is the answer. But near x = 1, f has values.
If they can be made as near to one number as you like by taking x near enough to 1, from either side,
that number is the limit of f(x) as x approaches 1. This lesson finds limits by coming close, and
shows two that do not exist.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. In each section the examples carry on from one
another, and the text says so; each section starts fresh.

<mode m="35s,STU">In this mode XEQ waits, after the label's letter, for ENTER; the keys below show the
ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Coming close

f goes in as a program, as in fn-01, so it can be run at many values of x. First GOLD GTO . . (fn-03)
moves to the top of program memory, so that L cannot land inside a program left stopped. Then, with x
in X: ENTER puts a copy of x in Y; x² squares the x in X, and 1 − takes 1 from that; x↔y brings the x in
Y back down, and 1 − makes x − 1; and ÷ divides x² − 1, now in Y, by x − 1. The label is L, on the TAN
key:

```keys P01A
GOLD GTO . . GOLD PRGM PRGM GOLD LBL L ENTER GOLD x² 1 − x↔y 1 − ÷ BLUE RTN
```

The X line shows <disp v="P01A" kind="program">L010 RTN</disp>, L's tenth line; another number means a
key was missed or doubled (fn-01 showed how to fix a line). Carrying on, turn program entry off:

```keys P01 after=P01A
GOLD PRGM PRGM
```

Now run L at values of x closer and closer to 1, from above. Carrying on:

```keys L01 after=P01
1.1 XEQ L
```
```keys L01 after=P01 mode=35s,STU
1.1 XEQ L ENTER
```

X shows <disp v="L01">2.1000</disp>.

```keys L02 after=L01
1.01 XEQ L
```
```keys L02 after=L01 mode=35s,STU
1.01 XEQ L ENTER
```

X shows <disp v="L02">2.0100</disp>.

```keys L03 after=L02
1.001 XEQ L
```
```keys L03 after=L02 mode=35s,STU
1.001 XEQ L ENTER
```

X shows <disp v="L03">2.0010</disp>. And from below:

```keys L04 after=L03
0.9 XEQ L
```
```keys L04 after=L03 mode=35s,STU
0.9 XEQ L ENTER
```

X shows <disp v="L04">1.9000</disp>,

```keys L05 after=L04
0.99 XEQ L
```
```keys L05 after=L04 mode=35s,STU
0.99 XEQ L ENTER
```

<disp v="L05">1.9900</disp>, and

```keys L06 after=L05
0.999 XEQ L
```
```keys L06 after=L05 mode=35s,STU
0.999 XEQ L ENTER
```

<disp v="L06">1.9990</disp>. From both sides the values close in on 2. (At 1 itself, L would stop on its
÷ with a division by 0; if you try it, C clears the message and GOLD GTO . . frees the program, as in
fn-03.)

A few values only suggest a limit; they cannot show that the values come as near to 2 as you like.
Here the algebra settles it. (x − 1) × (x + 1) is x² + x − x − 1, which is x² − 1. So wherever x is not
1, f(x) is (x − 1) × (x + 1) divided by x − 1, which is x + 1. Near 1, x + 1 is as near to 2 as you like.
f is x + 1 with one point missing, and the limit fills the gap.

Coming close also has a floor on any calculator. The STU-32 keeps 34 digits (rpn-03), so a number
closer to 1 than the 34th digit is just 1. 1 plus 10⁻³⁴, minus 1:

```keys Z01
1 E 34 +/− ENTER 1 + 1 −
```

X shows <disp v="Z01">0.0000</disp>, not 10⁻³⁴: the sum rounded to 1. At an x that close, L's x − 1
would be 0 too, and it would divide by 0. Close enough to see the limit, not so close that the digits
run out.

## A limit no algebra here can do

sin(x) ÷ x, with x in radians, has no value at x = 0, and nothing this lesson's algebra can do
simplifies it; coming close is how to see its limit. Set the unit to radians (trig-01), and show nine
places so the closing in can be seen. With x in X, ENTER puts a copy in Y, SIN takes the sine of the x in
X, and x↔y and ÷ divide that sine by x:

```keys S01
BLUE ∡MODE RAD GOLD DISP FIX 9 0.1 ENTER SIN x↔y ÷
```

X shows <disp v="S01">0.998334166</disp>. Carrying on, closer to 0:

```keys S02 after=S01
0.01 ENTER SIN x↔y ÷
```

X shows <disp v="S02">0.999983333</disp>, and carrying on,

```keys S03 after=S02
0.001 ENTER SIN x↔y ÷
```

<disp v="S03">0.999999833</disp>. And from below, carrying on:

```keys S03B after=S03
0.001 +/− ENTER SIN x↔y ÷
```

X shows <disp v="S03B">0.999999833</disp>, the same: the sine of −x is minus the sine of x, so the
fraction is the same on both sides. The values close in on 1, and the limit of sin(x) ÷ x as x
approaches 0 is 1, which a geometry proof in calculus confirms. At FIX 4 the last values would all have
rounded to 1 at four places, which hides how they close in; that is why the section showed nine.
Carrying on, set FIX 4 again:

```keys S04 after=S03B
GOLD DISP FIX 4
```

## Limits that do not exist

1/x near 0 settles on nothing. Close to 0 from above it is large:

```keys N01
0.01 1/x
```

X shows <disp v="N01">100.0000</disp>. Carrying on, nearer:

```keys N01B after=N01
0.001 1/x
```

X shows <disp v="N01B">1,000.0000</disp>: the nearer x is to 0, the larger 1/x grows, without end. And
carrying on, from below:

```keys N02 after=N01B
0.001 +/− 1/x
```

X shows <disp v="N02">-1,000.0000</disp>. The values close in on no number, from either side.

The two sides can also disagree. x ÷ |x|, x divided by its absolute value (eq-03), is 1 for every
positive x and −1 for every negative one. With x in X, ENTER copies it, ABS (gold, above +/−) makes the
x in X positive, and ÷ divides:

```keys N03
0.01 ENTER GOLD ABS ÷
```

X shows <disp v="N03">1.0000</disp>. Carrying on, from below:

```keys N04 after=N03
0.01 +/− ENTER GOLD ABS ÷
```

X shows <disp v="N04">-1.0000</disp>. From above the values are 1, from below −1, however near to 0:
two different numbers, so there is no limit. This is why a limit is checked from both sides.

## Exercises

1. Work out (x² − 4) ÷ (x − 2) at x = 2.01 and at x = 1.99. What is its limit as x approaches 2, and
   why?
2. Work out (2ˣ − 1) ÷ x at x = 0.001 and at x = 0.0001. Its limit as x approaches 0 is a number you have
   met in exp-03: which?

## Answers

1. 4. The top of the fraction first, then the bottom, then divide:

   ```keys E01
   2.01 GOLD x² 4 − 2.01 ENTER 2 − ÷
   ```

   X shows <disp v="E01">4.0100</disp>. Carrying on, from below:

   ```keys E01B after=E01
   1.99 GOLD x² 4 − 1.99 ENTER 2 − ÷
   ```

   X shows <disp v="E01B">3.9900</disp>. (x − 2) × (x + 2) is x² + 2x − 2x − 4, which is x² − 4, so away
   from 2 the function is x + 2, and near 2 that is near 4.

2. ln 2. At 0.001:

   ```keys E02
   2 ENTER 0.001 yˣ 1 − 0.001 ÷
   ```

   X shows <disp v="E02">0.6934</disp>. Carrying on, closer:

   ```keys E02B after=E02
   2 ENTER 0.0001 yˣ 1 − 0.0001 ÷
   ```

   X shows <disp v="E02B">0.6932</disp>. And carrying on, ln 2 (exp-03):

   ```keys E02C after=E02B
   2 LN
   ```

   X shows <disp v="E02C">0.6931</disp>: the values close in on it.
