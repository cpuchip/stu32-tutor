---
id: lin-01
title: Slope and intercept
status: draft prose (non-author read taken; accepted for accuracy by abacus #4443; not yet read by Michael)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# Slope and intercept

A linear function has the form y = mx + b. Its graph, drawn on axes as in fn-02, is a straight
line, and the two numbers say everything about it. m, the slope, is how far the line rises for each
step of 1 to the right. b, the intercept, is the value of y at x = 0, where the line crosses the
vertical axis. f(x) = 2x + 3 from fn-01 is one, with slope 2 and intercept 3. This lesson finds m and
b from two points on a line.

## Before you start

The setup from rpn-01: 33s mode and FIX 4. The examples in the first two sections are one chain,
each carrying on from the one before. In the third, each slope starts fresh. Two variables hold the
answers, as in rpn-02: M for the slope and B for the intercept. M is on the ENTER key and B on the eˣ
key; after STO, the next key means only its letter, so STO M is STO then ENTER.

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

## The slope from two points

Between two points on a line, the rise is how much y changes and the run is how much x changes.
Work both out from the same point, in the same order: the second point's y minus the first's, and
the second point's x minus the first's. The slope is the rise divided by the run, and on a straight
line it is the same whichever two points you pick. Take the points (3, 9) and (5, 13). The rise is
13 − 9 and the run is 5 − 3, so the slope is (13 − 9) ÷ (5 − 3). On the stack, work out the rise,
then the run, then divide:

```keys L01
13 ENTER 9 − 5 ENTER 3 − ÷
```

X shows <disp v="L01">2.0000</disp>: a rise of 4 over a run of 2. Each step of 1 to the right, the
line rises 2. Keep it in M:

```keys L02 after=L01
STO M
```

## The intercept

Any point on the line makes y = mx + b true. Take mx from both sides of that, and it gives
the intercept: b = y − mx. With the point (3, 9) and the slope in M, that is b = 9 − m × 3. Start it:

```keys L03A after=L02
9 RCL M 3
```

The stack now holds three numbers. The 9 lifted when RCL M brought m into X, and lifted again when
you started typing 3: 9 is in Z, m in Y, and X shows <disp v="L03A" kind="entry">3_</disp>. Now ×
multiplies m by 3, and the stack drops, so 9 comes down to Y. − then takes m × 3 from 9. Keep the
result in B:

```keys L03 after=L03A
× − STO B
```

X shows <disp v="L03">3.0000</disp>: b = 9 − 6. The line is y = 2x + 3, fn-01's f.

Check it with the other point. At x = 5 the line should give 13:

```keys L04 after=L03
5 RCL M × RCL B +
```

X shows <disp v="L04">13.0000</disp>. Both points are on the line.

## Lines that fall, lines that are flat

A line that falls to the right has a negative slope. Through (0, 10) and (5, 0), the rise is 0 − 10
and the run is 5 − 0:

```keys L05
0 ENTER 10 − 5 ENTER 0 − ÷
```

X shows <disp v="L05">-2.0000</disp>: each step to the right, the line drops 2. Through (1, 4) and
(3, 4), both points have the same y, so there is no rise:

```keys L06
4 ENTER 4 − 3 ENTER 1 − ÷
```

X shows <disp v="L06">0.0000</disp>. A slope of 0 is a flat line, y = 4 for every x.

A line straight up and down has no slope at all. Through (3, 1) and (3, 5), the run is 3 − 3:

```keys L07
5 ENTER 1 − 3 ENTER 3 − ÷
```

The screen shows <disp v="L07" kind="message">DIVIDE BY 0</disp>, as in fn-03: the rise of 4 would
be divided by a run of 0. Press C to clear the message:

```keys L07B after=L07
C
```

X shows <disp v="L07B">0.0000</disp>, the run. The rise is still in Y; x↔y brings it down to see:

```keys L07C after=L07B
x↔y
```

X shows <disp v="L07C">4.0000</disp>. Such a line is not y = mx + b for any m. It is the line x = 3,
and it is not a function of x: a function gives one output for each input, and here the input 3
would need every y as its output.

## Exercises

1. Find the slope and the intercept of the line through (−1, 5) and (3, 13).
2. Find the slope of the line through (0, 1) and (4, 4). What is its intercept, without any keys?

## Answers

1. The rise is 13 − 5 and the run is 3 − (−1):

   ```keys E01
   13 ENTER 5 − 3 ENTER 1 +/− − ÷
   ```

   X shows <disp v="E01">2.0000</disp>. Then b = 5 − m × (−1), with the slope kept in M:

   ```keys E01B after=E01
   STO M 5 RCL M 1 +/− × −
   ```

   X shows <disp v="E01B">7.0000</disp>. The line is y = 2x + 7.

2. The keys:

   ```keys E02
   4 ENTER 1 − 4 ENTER 0 − ÷
   ```

   X shows <disp v="E02">0.7500</disp>: three quarters. The point (0, 1) has x = 0, so it is where the
   line crosses the vertical axis: the intercept is 1, and the line is y = 0.75x + 1.
