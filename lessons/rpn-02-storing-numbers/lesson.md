---
id: rpn-02
title: Storing numbers
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 2
display: FIX 2
---

# Storing numbers

The stack holds four numbers, and they move every time you calculate. A number you want to keep
for later, like a tax rate or a measurement, goes in a variable instead. The STU-32 has 26 of
them, named A to Z, and a variable keeps its number until you change it.

## Before you start

This lesson works in money, so set the display to two decimal places: blue, then ENTER (MODE), the
soft key under your mode, then gold, 2 (DISP), the soft key under FIX, and 2.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 2
```

Each variable's letter is printed small at the lower right of a key. After STO, RCL or VIEW, the
calculator waits for a variable, and the next key you press means only its letter. Some letters
sit on keys that usually do something else: W is on the 5 key, L on TAN, and G on STO itself. So
STO G is STO pressed twice.

## STO puts a number away

A sales tax of 8.25% is 0.0825 as a decimal. Type it and press STO. The calculator waits for a
variable; press A (the √x key).

```keys V01
0.0825 STO A
```

X shows <disp v="V01">0.08</disp>. The display rounds to two places, but A and X both keep all of
0.0825. STO keeps a copy and takes nothing off the stack, and after STO a number you type pushes X up, as it does after + or ×.

## RCL brings it back

RCL (recall) copies a variable into X and pushes the stack up, the way a typed number does. The
tax on a 40 dollar purchase is 40 times the rate:

```keys V02
0.0825 STO A 40 RCL A ×
```

X shows <disp v="V02">3.30</disp>. A still holds 0.0825: recalling a number does not use it up.

RCL can also do the arithmetic. Press RCL, then ×, then A, and X is multiplied by A in one step:

```keys V03
0.0825 STO A 40 RCL × A
```

The answer is the same. RCL with − or ÷ works X minus A, or X divided by A. Here it takes 10 from
25:

```keys V03A
10 STO A 25 RCL − A
```

X holds 15. And here it divides 10 by 4:

```keys V03B
4 STO A 10 RCL ÷ A
```

X holds 2.5.

## Variables are not on the stack

Whatever you do on the stack, a variable keeps its number. Store 9 in C (the LN key), do some
arithmetic, then recall C:

```keys V04
9 STO C 1 ENTER 2 + RCL C
```

X shows <disp v="V04">9.00</disp>, and the 3 from the arithmetic has moved up to Y.

## A running total

STO can also change a variable. Press STO, then +, then the letter, and X is added to what the
variable holds; STO − takes X away from it. To total three purchases (12.50, 7.25 and 30), start
B (the eˣ key) at 0 and add each one:

```keys V05
0 STO B 12.5 STO + B 7.25 STO + B 30 STO + B
```

B now holds 49.75. Starting at 0 matters: STO + adds to whatever B held before, and a calculator
that has been used may have left anything there.

To look at a variable without disturbing the stack, use VIEW (gold, above STO):

```keys V06
0 STO B 12.5 STO + B 7.25 STO + B 30 STO + B GOLD VIEW B
```

The screen shows <disp v="V06" kind="view">B=49.75</disp> on the X line. X itself still holds 30,
the last purchase. The view stays until your next key, and that key also does its own job: typing
5 puts the 5 in X and lifts the 30 into Y.

```keys V06B
0 STO B 12.5 STO + B 7.25 STO + B 30 STO + B GOLD VIEW B 5
```

The two exceptions are ← and C, which only clear the view and change nothing else:

```keys V06C
0 STO B 12.5 STO + B 7.25 STO + B 30 STO + B GOLD VIEW B ←
```

X still holds 30.

## Using stored numbers more than once

A number you have stored can be used as many times as you like, without typing it again. Store the
width and length of a rectangle, 3.5 in W and 12 in L, and find its area:

```keys V07
3.5 STO W 12 STO L RCL L RCL W ×
```

X shows <disp v="V07">42.00</disp>. The same two variables give its perimeter, 2 × (L + W):

```keys V08
3.5 STO W 12 STO L RCL L RCL W + 2 ×
```

X holds 31.

## Exercises

1. A price of 250 grows by 8% a year. Store 1.08 in G, then use recall arithmetic to work out the
   price after two years.
2. Put 100 in D (the yˣ key). Then spend 23.40 and 9.60, taking each one out of D with STO −.
   What does D hold?

## Answers

1. Each RCL × G multiplies X by 1.08:

   ```keys E01
   1.08 STO G 250 RCL × G RCL × G
   ```

   X shows <disp v="E01">291.60</disp>.

2. D holds 67. STO − takes X away from the variable, so D goes from 100 to 76.6 to 67:

   ```keys E02
   100 STO D 23.4 STO − D 9.6 STO − D
   ```
