---
id: sys-01
title: Two equations at once
requires: setup rpn-arithmetic stack-lift mult-before-add fraction-bar stack-full sto rcl letter-keys linear-function slope intercept falling-flat
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Two equations at once

At a school play, two adult tickets and three child tickets cost 37 dollars, and one adult ticket
with one child ticket costs 15. What does each kind of ticket cost? Call an adult's ticket x and a
child's y. Then 2x + 3y = 37 and x + y = 15. Two equations that must hold at the same time are a
system of equations, and a solution of the system is a pair of numbers, one for x and one for y,
that makes both true. This lesson finds such pairs, and shows when there is none, or endlessly many.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Work the examples in order; when one carries on
from the one before, the text says so. The pair goes in two variables, X for x and Y for y. X is on
the 6 key and Y on the 1 key; after STO or RCL, the next key means only its letter (rpn-02). The
bottom line of the screen is also called X. In this lesson, "X shows" always means that bottom line,
and "the variable X" means the letter.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Checking a pair

Try a guess: an adult's ticket 5 and a child's 10. Store the pair in the variables X and Y, then work
out the left side of the first equation, 2x + 3y:

```keys C01
5 STO X 10 STO Y 2 RCL X × 3 RCL Y × +
```

X shows <disp v="C01">40.0000</disp>, not 37. The second equation's left side, x + y:

```keys C02 after=C01
RCL X RCL Y +
```

X shows <disp v="C02">15.0000</disp>. This pair fits the second equation and not the first, so it is
not a solution: a solution has to fit both. Many pairs add to 15; the system asks for a pair among
them that also makes 2x + 3y come to 37. Try 8 and 7:

```keys C03
8 STO X 7 STO Y 2 RCL X × 3 RCL Y × +
```

X shows <disp v="C03">37.0000</disp>, and, carrying on,

```keys C04 after=C03
RCL X RCL Y +
```

X shows <disp v="C04">15.0000</disp>. The pair (8, 7) fits both: an adult's ticket is 8 dollars and a
child's 7. But guessing is slow. The next section finds the pair without guessing.

## Elimination

An equation still holds when both its sides are multiplied by the same number, or divided by the same
number that is not 0. And when two equations hold, taking one from the other, left side from left side
and right side from right side, gives an equation that holds too: equals taken from equals leave
equals.

Multiply the second equation by 2: 2x + 2y = 30. Now both equations have 2x. Take the new one from the
first: the 2x's cancel, and what is left is 3y − 2y = 37 − 30, that is, y = 37 − 2 × 15. Taking one
equation from another to get rid of an unknown is called elimination. Either unknown can be
eliminated; pick the one whose numbers make it easiest. On the stack, the 37 waits while 2 × 15 is
worked out, as in num-01:

```keys L01
37 ENTER 2 ENTER 15 × −
```

X shows <disp v="L01">7.0000</disp>: y = 7. Store it in the variable Y, and put it into the second
equation, which says x = 15 − y:

```keys L02 after=L01
STO Y 15 RCL Y −
```

X shows <disp v="L02">8.0000</disp>: x = 8, the pair that the checks found.

The calculator earns its keep when the numbers are less tidy. At a fruit stall, apples are 0.75
dollars and pears 1.25. Six pieces of fruit cost 6.50. How many of each? With x apples and y pears,
0.75x + 1.25y = 6.5 and x + y = 6. Multiply the second by 0.75 and take it from the first: the x's
cancel, leaving (1.25 − 0.75)y = 6.5 − 0.75 × 6. Divide both sides by 1.25 − 0.75, and
y = (6.5 − 0.75 × 6) ÷ (1.25 − 0.75). Work out the top, then the bottom, then divide, as in num-01:

```keys F01
6.5 ENTER 0.75 ENTER 6 × − 1.25 ENTER 0.75 − ÷
```

X shows <disp v="F01">4.0000</disp>: four pears. Carrying on, x = 6 − y:

```keys F02 after=F01
STO Y 6 RCL Y −
```

X shows <disp v="F02">2.0000</disp>: two apples. Check it in your head: 2 × 0.75 + 4 × 1.25 is 1.50 +
5.00, which is 6.50.

## No solution, or every solution

The graph of each equation in these systems is a line. To see its slope and intercept (lin-01),
rewrite it as y = mx + b. x + y = 15: take x from both sides, and y = −x + 15, slope −1 and intercept
15. 2x + 3y = 37: take 2x from both sides, 3y = −2x + 37, and divide both sides by 3: y = −(2/3)x +
37/3, slope −2/3. A solution is a point on both lines, where they cross. Two different lines with
different slopes cross at exactly one point, and these slopes, −1 and −2/3, differ: that is why the
tickets had one answer.

Lines with the same slope and different intercepts never meet, however far they go: they are called
parallel. Take x + y = 3 and x + y = 5, which are y = −x + 3 and y = −x + 5. Taking the first from
the second leaves 0 = 5 − 3:

```keys P01
5 ENTER 3 −
```

X shows <disp v="P01">2.0000</disp>. This is not a value of x or y: both unknowns have gone, and the
2 is what is left on the right side. Elimination has left 0 = 2, which is never true, so no pair fits
both: the system has no solution, as parallel lines have no point in common.

Now x + y = 3 and 2x + 2y = 6. Twice the first, taken from the second, leaves 0 = 6 − 2 × 3:

```keys P02
6 ENTER 2 ENTER 3 × −
```

X shows <disp v="P02">0.0000</disp>. Elimination has left 0 = 0, which is always true. The second
equation is the first one doubled, so both are the same line, and every point on it is a solution:
(0, 3), (1, 2), (2.5, 0.5), and endlessly many more.

So when elimination takes away both unknowns at once, what is left decides it. If it is 0 = 0, every
point of the line is a solution. If it is 0 = a number that is not 0, there is no solution.

## Exercises

1. Solve 3x + 2y = 16 and x + y = 6 by elimination, then check the pair in the first equation.
2. Show that 2x − y = 1 and 4x − 2y = 5 have no solution.
3. A jar holds 40 coins, each a 5-cent or a 10-cent coin, worth 2.75 dollars in all. How many of each?
4. What are the solutions of 3x − y = 2 and 6x − 2y = 4?

## Answers

1. x = 4 and y = 2. Twice the second is 2x + 2y = 12, with the same 2y as the first, so taking it
   from the first eliminates y and leaves x = 16 − 2 × 6:

   ```keys E01
   16 ENTER 2 ENTER 6 × −
   ```

   X shows <disp v="E01">4.0000</disp>. Carrying on, store it in the variable X; y = 6 − x:

   ```keys E01B after=E01
   STO X 6 RCL X −
   ```

   X shows <disp v="E01B">2.0000</disp>. Carrying on, store it in the variable Y and check 3x + 2y:

   ```keys E01C after=E01B
   STO Y 3 RCL X × 2 RCL Y × +
   ```

   X shows <disp v="E01C">16.0000</disp>, the first equation's right side.

2. Twice the first is 4x − 2y = 2. Taken from the second, it leaves 0 = 5 − 2 × 1:

   ```keys E02
   5 ENTER 2 ENTER 1 × −
   ```

   X shows <disp v="E02">3.0000</disp>. Elimination has left 0 = 3, which is false, so there is no
   solution. Written as y = mx + b, the lines are y = 2x − 1 and y = 2x − 2.5: the same slope and
   different intercepts, so they are parallel.

3. 25 five-cent coins and 15 ten-cent coins. In dollars, a 5-cent coin is 0.05 and a 10-cent coin
   0.10. With x five-cent and y ten-cent coins, x + y = 40 and 0.05x + 0.10y = 2.75. Take 0.05 times
   the first from the second: (0.10 − 0.05)y = 2.75 − 0.05 × 40, so
   y = (2.75 − 0.05 × 40) ÷ (0.10 − 0.05):

   ```keys E03
   2.75 ENTER 0.05 ENTER 40 × − 0.10 ENTER 0.05 − ÷
   ```

   X shows <disp v="E03">15.0000</disp>: y = 15. Carrying on, x = 40 − y:

   ```keys E03B after=E03
   STO Y 40 RCL Y −
   ```

   X shows <disp v="E03B">25.0000</disp>. Check: 25 × 0.05 + 15 × 0.10 is 1.25 + 1.50, which is 2.75.

4. Every point of one line. Twice the first is 6x − 2y = 4; taken from the second, it leaves
   0 = 4 − 2 × 2:

   ```keys E04
   4 ENTER 2 ENTER 2 × −
   ```

   X shows <disp v="E04">0.0000</disp>: 0 = 0, always true. The second equation is the first doubled,
   so they are one line, y = 3x − 2, and every point on it is a solution: (0, −2), (1, 1), (2, 4),
   and endlessly many more.
