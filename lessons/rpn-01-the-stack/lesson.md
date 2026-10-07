---
id: rpn-01
title: The stack and ENTER
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The stack and ENTER

The STU-32 has no equals key. You give it the numbers first and the operation last, and it works
each step the moment you press it. This is RPN, Reverse Polish Notation. The "Polish" is for Jan
Łukasiewicz, a Polish logician whose notation put the operation before the numbers; RPN puts it
after. While you type, the numbers wait on a stack, so this lesson is about the stack: where your
numbers go, and how to move them.

## Before you start

Most keys do three things. The legend on the key itself is what it does when you press it alone. The gold and blue legends printed above it are its shifted functions: press the plain gold
key (at the left edge, beside 4) or the plain blue key (beside 1), let go, then press the key under
the legend. In the examples, `GOLD LASTx` means the gold key, then the key with LASTx printed in
gold above it.

Some functions open a menu. Its choices appear as labels along the bottom of the screen, and the
six blank keys just under the screen choose them. These are the soft keys.

The STU-32 has three modes. 33s and 35s mode behave like two older calculators, the HP 33s and the
HP 35s; STU mode is the STU-32's own, with features those two never had. Choose one on this page,
and every lesson shows the keys for it. Where the modes differ, the lessons say so.

Put the calculator in your mode and show four decimal places. Press blue, then ENTER (MODE is
printed in blue above it), and the mode menu opens; press the soft key under your mode. Then
press gold and 2 (DISP, in gold), the soft key under FIX, and 4.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

The screen shows four lines, labelled T, Z, Y and X from top to bottom. X, at the bottom, is the
number you are looking at, and it is where every answer lands. With FIX 4, numbers show four
decimal places, and very large or very small ones switch to scientific form.

You only do this setup once. The examples below are meant to be worked in order. Most start
fresh and don't depend on what is already on the stack; when one carries on from the example
before it, the text says so and its keys are only what you press next.

## Two numbers, one operation

To add 7 and 5, type 7, press ENTER, type 5, and press +.

```keys S01
7 ENTER 5 +
```

X shows <disp v="S01">12.0000</disp>.

ENTER copies the 7 up into Y. The 5 you type next replaces the copy left in X, so Y holds 7 and X
holds 5. The + key then adds Y and X and puts the sum in X.

If you type a wrong digit, the ← key (backspace) takes it back. Here 56 was typed in place of 5,
and ← removes the 6 before the +:

```keys S01A
7 ENTER 56 ← +
```

X holds 12, as before.

Subtraction and division need the numbers in the order you would say them. The first number goes
in Y, the second in X, and the operation works Y minus X, or Y divided by X. So 7 minus 5 is:

```keys S02
7 ENTER 5 −
```

and X holds 2. Twenty divided by eight is:

```keys S03
20 ENTER 8 ÷
```

X shows <disp v="S03">2.5000</disp>.

## ENTER copies

Because ENTER copies, a number you type and ENTER is in both X and Y. Type 6 and press ENTER:

```keys S04
6 ENTER
```

Both X and Y hold 6. Therefore ENTER followed by × multiplies a number by itself. This gives 36:

```keys S05
6 ENTER ×
```

The rule for typing is worth knowing exactly. Right after ENTER, the next number you type replaces
the copy in X. After an operation such as + − × or ÷, the next number you type pushes X up into Y
first.

## A result is a number you can keep using

By that rule, an answer in X is kept when you start typing the next number: it moves up to Y.
For (3 + 4) × 5, add first, then type 5 and multiply, with no ENTER before the 5:

```keys S06
3 ENTER 4 + 5 ×
```

X holds 35.

The stack is what lets you skip parentheses. For (2 + 3) × (4 + 6), work out the first sum, then
start the second one. The 5 from the first sum stays on the stack while you work. Typing 4 pushes
it up to Y, ENTER pushes it again to Z, and 6 replaces the copy of 4 in X:

```keys S07A
2 ENTER 3 + 4 ENTER 6
```

Now Z holds 5, Y holds 4 and X holds 6. Carry on from there and press +. It adds Y and X, and
everything above drops down a level, so the 5 comes back down to Y:

```keys S07 after=S07A
+
```

X holds 10 and Y holds 5. Press × to finish:

```keys S08 after=S07
×
```

X holds 50. You never had to tell the calculator where the parentheses were, because you did the
inside of each one first.

## Moving the stack

Sometimes the numbers are in the wrong order. Say you typed 5 and then 20, but you want 20 divided
by 5. The x↔y key swaps X and Y, so the 20 goes up to Y and the 5 comes down to X:

```keys S09
5 ENTER 20 x↔y ÷
```

X holds 4.

The stack has four levels, and R↓ (roll down) turns all four. Type 1, 2, 3 and 4 with ENTER
between them, so T holds 1, Z holds 2, Y holds 3 and X holds 4. Then press R↓:

```keys S10
1 ENTER 2 ENTER 3 ENTER 4 R↓
```

Every number moves down one level, and the 4 that was in X wraps around to T. Now X holds 3, Y
holds 2, Z holds 1 and T holds 4.

## LAST x

The calculator remembers the number that was in X just before the last operation. LAST x (printed
LASTx, in gold above ENTER) brings it back. Divide 12 by 4, then press LAST x:

```keys S11
12 ENTER 4 ÷ GOLD LASTx
```

The 4 comes back into X, and the answer of the division, 3, moves up to Y. This is useful when you
divide by the wrong number: multiply by LAST x and you are back where you started.

```keys S12
12 ENTER 4 ÷ GOLD LASTx ×
```

X holds 12 again.

## Negative numbers

The − key subtracts, so it cannot also make a number negative. For that there is +/−, which
changes the sign of the number you are typing. Here is −5 minus 3:

```keys S13
5 +/− ENTER 3 −
```

X shows <disp v="S13">-8.0000</disp>.

If you press − in place of +/−, the calculator subtracts your 5 from whatever is in Y. That gives a
wrong answer and no error message, so watch for it.

## T copies down

When an operation uses X and Y, everything above drops down a level. T has nothing above it, so it
keeps its number and also copies it down into Z. Therefore a stack filled with one number keeps
handing you that number, as many times as you ask.

A price that grows 5% a year is multiplied by 1.05 each year. Type 1.05 and press ENTER three
times, so all four levels hold 1.05, then press × five times:

```keys S14
1.05 ENTER ENTER ENTER × × × × ×
```

X shows <disp v="S14">1.3401</disp>. That is 1.05 to the sixth power: over six years the price grows
by about 34%. The first three presses of × use the four 1.05s you filled in. From the fourth press
on, each × uses a copy that T dropped down.

## Exercises

1. Work out (8 − 3) × (2 + 4).
2. Work out 100 divided by (4 × 5), typing 100 first.
3. Fill the stack with 2s and multiply until X holds 2 to the fifth power. How many times do you
   press ×?
4. Work out −3 × −4.

## Answers

1. 30:

   ```keys E01
   8 ENTER 3 − 2 ENTER 4 + ×
   ```

2. 5. The 100 goes up to Z while you multiply 4 by 5, and comes back down to Y for the ÷:

   ```keys E02
   100 ENTER 4 ENTER 5 × ÷
   ```

3. 32, after four presses of ×. The first three use the four 2s you filled in, and the fourth uses
   a copy that T dropped:

   ```keys E03
   2 ENTER ENTER ENTER × × × ×
   ```

4. 12:

   ```keys E04
   3 +/− ENTER 4 +/− ×
   ```
