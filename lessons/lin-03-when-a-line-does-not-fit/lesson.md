---
id: lin-03
title: When a line does not fit
status: draft prose (non-author read taken; accepted for accuracy by abacus #4460; not yet read by Michael)
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
right model; the shape of the points decides. Doubling has its own kind of function, which unit 6
meets.
