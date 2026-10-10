---
id: lin-03
title: When a line does not fit
requires: setup shift-keys clear-message slope intercept falling-flat sigma-plus regression y-hat correlation
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# When a line does not fit

The calculator finds the best line for any data you give it, even data no line suits. r, from
lin-02, measures one thing only: how well a sloping line fits. This lesson gives the line some
points that follow a rule exactly, the table of q from fn-02, and watches r find no sloping line in
them. Then it tries points on one sloping line, points on a flat line, and points a line fits well
by r but describes badly.

A model is a rule chosen to describe data. A line is one kind of model; the lesson is about when it
is the wrong kind.

## From before

Two from before, by hand: one from unit 1, and an estimate from lin-02.

```item LN3F1
prompt: Work out 3² + 4².
topics: x-squared
answer: type
calculator: no
slip: LN3F1A | squared the sum | Square each first: 9 + 16. (3 + 4)² is another number.
```

```item LN3F2
prompt: The line y = 2x − 1 estimates y at x = 7. What is the estimate?
topics: estimate
answer: type
calculator: no
slip: LN3F2A | took 1 from x first | Multiply first: 2 × 7 is 14, then take away 1.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. The examples in each section are one chain; each section
and the exercise start fresh, with the sums cleared.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## A curve

In fn-02, q(x) = x² − 4x + 3 gave this table:

| x | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| q(x) | 3 | 0 | −1 | 0 | 3 |

Enter the five points as lin-02 does, y first. The −1 is 1 +/−:

```keys Q01
GOLD CLEAR Σ 3 ENTER 0 Σ+ 0 ENTER 1 Σ+ 1 +/− ENTER 2 Σ+ 0 ENTER 3 Σ+ 3 ENTER 4 Σ+
```

X shows <disp v="Q01">5.0000</disp>, five points. Now r:

```keys Q02 after=Q01
BLUE L.R. r
```

X shows <disp v="Q02">0.0000</disp>. By r, no sloping line follows these points at all, and yet
each one follows q's rule exactly. The slope:

```keys Q03 after=Q02
BLUE L.R. m
```

X shows <disp v="Q03">0.0000</disp>, and the intercept:

```keys Q04 after=Q03
BLUE L.R. b
```

X shows <disp v="Q04">1.0000</disp>. The best line is flat, y = 1, and 1 is the average of the five
values: (3 + 0 − 1 + 0 + 3) ÷ 5. The points mirror each other about x = 2: the left half falls just
as the right half rises. Tilting the line up would bring it nearer the right half exactly as much as
it took it away from the left half, and tilting it down the same the other way, so the best line
does not tilt. It lies flat, and fits neither half. Ask it for x = 2:

```keys Q05 after=Q04
2 BLUE L.R. ŷ
```

X shows <disp v="Q05">1.0000</disp>, but q(2) is −1. The line misses the lowest point by 2.

So r near 0 does not mean x and y are unrelated. It means no sloping line describes them. Look at
the points first, in a table or on a graph as in fn-02, and use a line only when they lie roughly
along one.

## A perfect fit

The other end of the scale. f(x) = 2x + 3 from fn-01 gives 3, 5, 7, 9 and 11 at x = 0 to 4, all on
one line:

```keys P01
GOLD CLEAR Σ 3 ENTER 0 Σ+ 5 ENTER 1 Σ+ 7 ENTER 2 Σ+ 9 ENTER 3 Σ+ 11 ENTER 4 Σ+ BLUE L.R. r
```

X shows <disp v="P01">1.0000</disp>, exactly. r is 1 or −1 only when every point is on one sloping
line. The slope and intercept are f's own:

```keys P02 after=P01
BLUE L.R. m
```

X shows <disp v="P02">2.0000</disp>.

```keys P03 after=P02
BLUE L.R. b
```

X shows <disp v="P03">3.0000</disp>.

## A flat line

Points all on a flat line, y = 4 at x = 1, 2 and 3, fit a line perfectly too, yet they have no r:

```keys F01
GOLD CLEAR Σ 4 ENTER 1 Σ+ 4 ENTER 2 Σ+ 4 ENTER 3 Σ+ BLUE L.R. r
```

The screen shows <disp v="F01" kind="message">STAT ERROR</disp>. r compares how y moves with how x
moves, and here y does not move at all, so the comparison would divide by zero. Clear the message:

```keys F02 after=F01
C
```

X shows <disp v="F02">3.0000</disp>, the count Σ+ left. The line itself is still there:

```keys F03 after=F02
BLUE L.R. m
```

X shows <disp v="F03">0.0000</disp>, and

```keys F04 after=F03
BLUE L.R. b
```

X shows <disp v="F04">4.0000</disp>: the line y = 4, through every point.

## Exercise

Something that doubles each step: 2, 4, 8, 16 and 32 at x = 1 to 5. Look at the points first: how
much does each step add? Then find r, and use the line at x = 1, at x = 3 and at x = 6. Is a line a
good model?

## Answer

Each step adds more than the one before: 2, then 4, 8 and 16. Points that rise faster and faster lie
on a curve, not a line. r:

```keys E01
GOLD CLEAR Σ 2 ENTER 1 Σ+ 4 ENTER 2 Σ+ 8 ENTER 3 Σ+ 16 ENTER 4 Σ+ 32 ENTER 5 Σ+ BLUE L.R. r
```

X shows <disp v="E01">0.9333</disp>, high: by r alone, a line looks good. The line at x = 1:

```keys E01B after=E01
1 BLUE L.R. ŷ
```

X shows <disp v="E01B">-2.0000</disp>, below zero, for something that starts at 2 and only grows.
At x = 3:

```keys E01C after=E01B
3 BLUE L.R. ŷ
```

X shows <disp v="E01C">12.4000</disp>, where the data says 8. Inside the data the line runs too low at
the ends and too high in the middle: the mark of points on a curve. Past the data it is worse:

```keys E01D after=E01C
6 BLUE L.R. ŷ
```

X shows <disp v="E01D">34.0000</disp>, and the next doubling is 64. A high r does not make a line the
right model; the shape of the points decides. Doubling has its own kind of function, which exp-01
meets.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item LN3M1
prompt: The points (0, 1), (1, 3) and (2, 5) all lie on one rising line. What is their r?
topics: perfect-fit
answer: type
calculator: no
working: none
slip: LN3M1A | gave the slope | r measures the fit, not the slope: points exactly on a rising line have r = 1.
```

```item LN3M2
prompt: What is the slope of the line through (0, 3) and (2, −1)?
topics: slope
answer: type
calculator: no
slip: LN3M2A | lost the sign | The rise is −1 − 3, which is −4: the line falls.
```

```item LN3M3
prompt: Five points all have y = 4. What is the slope of the best line through them?
topics: flat-no-r
answer: type
calculator: no
working: none
slip: LN3M3A | gave the height | Every point is at the same height, so the line is flat: it rises 0.
```

```item LN3M4
prompt: f(x) = x² − 1. What is f(−2)?
topics: function
answer: type
calculator: no
slip: LN3M4A | squared 2, then made it negative | f(−2) puts −2 in for x: (−2)² is 4, then 4 − 1.
```

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP4A
prompt: What is the slope of the line through (2, 5) and (6, 13)?
topics: slope
answer: type
calculator: no
slip: CP4A1 | run over rise | Rise over run: the change in y on top, (13 − 5) ÷ (6 − 2).
slip: CP4A2 | the points in different orders | Take the points in the same order, top and bottom: (13 − 5) ÷ (6 − 2).
```

```item CP4B
prompt: The line y = 2x + b goes through (1, 7). What is b?
topics: intercept
answer: type
calculator: no
slip: CP4B1 | added the 2 | Put x = 1 and y = 7 in: 7 = 2 + b, so b = 7 − 2.
slip: CP4B2 | divided by 2 | The b is added to 2x, not multiplied: 7 = 2 × 1 + b, so b = 7 − 2.
```

```item CP4C
prompt: For y = 3x − 4, what is y when x = 10?
topics: linear-function
answer: type
calculator: no
slip: CP4C1 | added the 4 | It is minus 4: 30 − 4.
slip: CP4C2 | took 4 from x first | Multiply first: 3 × 10, then take away 4.
```
