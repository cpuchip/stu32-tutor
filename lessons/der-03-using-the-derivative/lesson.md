---
id: der-03
title: Using the derivative
requires: setup shift-keys rpn-arithmetic enter-copies stack-lift swap-roll x-squared power change-sign linear-function slope intercept function derivative-function tangent-line power-rule sum-multiple-rules constant-derivative eqn-typing solve equation-list
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Using the derivative

A derivative is a function that gives a curve's slope at each point. This lesson puts that to work
twice: to find the straight line that best fits a curve near a point, and to find where a curve turns,
from falling to rising or back. The examples use the function from fn-02, q(x) = x² − 4x + 3, whose graph you drew by hand, and
by the rules of der-02, q′(x) = 2x − 4.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each example starts fresh, except where one says
it carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## The tangent line

der-01 called the tangent line at a the line through (a, f(a)) with slope f′(a). That line is
y = f(a) + f′(a)(x − a). At x = a it gives f(a), and each 1 added to x adds f′(a) to y, so it is the line
through that point with that slope (the slope of lin-01). At x = 3,
q(3) = 9 − 12 + 3 = 0 and q′(3) = 2 × 3 − 4 = 2, so the tangent line is y = 0 + 2(x − 3), or y = 2x − 6.

Near the point, the tangent line and the curve are very close. At x = 3.1, q is worked out on the
stack as fn-02 did: 3.1 ENTER keeps a copy in Y for the 4 ×, after x² has squared the one in X.

```keys T01
3.1 ENTER GOLD x² x↔y 4 × − 3 +
```

X shows <disp v="T01">0.2100</disp>. And the line at 3.1, 2 × 3.1 − 6:

```keys T02
3.1 ENTER 2 × 6 −
```

X shows <disp v="T02">0.2000</disp>. They differ by 0.01, which is 0.1². Here the difference between q
and its tangent line is exactly (x − 3)², since x² − 4x + 3 − (2x − 6) = x² − 6x + 9. Halve the distance
from 3, to 3.05:

```keys T03
3.05 ENTER GOLD x² x↔y 4 × − 3 +
```

X shows <disp v="T03">0.1025</disp>. The line there is 2 × 3.05 − 6 = 0.1, so the gap is 0.0025, a
quarter of 0.01. Halving the distance quartered the gap.

Any line through (3, 0) is close to q near 3, so compare another: y = 3x − 9. At 3.1 it gives 0.3, a gap
of 0.09; at 3.05 it gives 0.15, a gap of 0.0475, only about half. Its gap is (x − 3)(x − 4), which
shrinks only as fast as the distance itself; the tangent's, (x − 3)², shrinks as fast as the distance
squared. Of all the lines through the point, only the tangent's gap shrinks that fast, which is what
makes it the best straight-line stand-in for the curve near the point.

## Lowest and highest points

On the graph of q from fn-02, the curve falls, turns at its lowest point, and rises. Where it falls, its
slope is negative; where it rises, positive. At the turn the tangent line is flat: the slope is 0. So
where a smooth curve turns, its derivative is 0, and the turns are among the places where f′ = 0.

Two warnings. Not every place where f′ = 0 is a turn: x³ has derivative 3x², which is 0 at x = 0, but
x³ rises on both sides of 0 and only flattens there for a moment. And on a limited stretch of a curve,
its lowest or highest point can be at an end of the stretch, where the slope need not be 0. So each
place where f′ = 0 is a candidate, and the slope's sign either side decides it: negative then positive
is a turn up, a lowest point nearby; positive then negative a turn down, a highest point nearby; the
same sign both sides, no turn. Test either side at points with no other zero of f′ between them and
the candidate.

For q, 2x − 4 = 0 at x = 2. By hand that is one step; SOLVE (eq-01) does the same for an equation
typed with no = sign, where it finds a value that makes the expression 0. (SOLVE finds one such value,
near its starting guess; where there are two, as for 3x² − 3, it finds only one, so the algebra comes
first.)

```keys S01
GOLD EQN 2 × RCL X − 4 ENTER GOLD SOLVE X
```

The X line shows <disp v="S01" kind="view">X=2.0000</disp>. The slope's sign either side: q′(1) = −2,
falling, and q′(3) = 2, rising, so x = 2 is a turn up. In fact q′(x) = 2x − 4 is negative for every x below
2 and positive for every x above, so q falls all the way to 2 and rises all the way after: x = 2 is
q's lowest point anywhere, not only nearby. Its height, q(2):

```keys S02
2 ENTER GOLD x² x↔y 4 × − 3 +
```

X shows <disp v="S02">-1.0000</disp>. The lowest point of q is (2, −1), the turn the drawing in fn-02 showed.

A curve can have more than one. f(x) = x³ − 3x has f′(x) = 3x² − 3, which is 0 when x² = 1: at x = 1 and
x = −1. The slope's sign tells which is which. f′(−2) = 9 is positive, f′(0) = −3 negative, and
f′(2) = 9 positive again. So f rises, turns down at x = −1, falls, and turns up at x = 1. The heights,
f(−1) on the stack (yˣ uses the copy in Y as its base, and the last copy waits for 3 ×, as in der-02):

```keys C01
1 +/− ENTER ENTER 3 yˣ x↔y 3 × −
```

X shows <disp v="C01">2.0000</disp>. And f(1):

```keys C02
1 ENTER ENTER 3 yˣ x↔y 3 × −
```

X shows <disp v="C02">-2.0000</disp>. (−1, 2) is a high point and (1, −2) a low one, but only nearby:
f(3) = 18 is higher, and f(−3) = −18 lower, and f keeps rising to the right and falling to the left, so
it has no highest or lowest point at all. A point higher than everything near it is called a local
maximum, and one lower than everything near it a local minimum.<mode m="33s,35s"> The 33s and 35s
modes have no graph, so the derivative, worked by hand and solved as above, is how to find these
points in this mode.</mode>

<mode m="STU">

## On the graph

STU mode's GRAPH (fn-02) has tools that find these points from the picture. Type q, turn Equation
mode off, and set the window from fn-02, XMIN −2 and XMAX 5.98: its 400 columns are 0.02 apart, so column 200,
where the trace starts, is x = 2 (fn-02).</mode>

```keys G01 mode=STU
GOLD EQN RCL X yˣ 2 − 4 × RCL X + 3 ENTER GOLD EQN 2 +/− BLUE GRAPH XMIN 5.98 BLUE GRAPH XMAX
```

<mode m="STU">X shows <disp v="G01">5.9800</disp>. Carrying on, GO draws the curve, and the digit 6
moves the trace one column right; five of them move it off the bottom, to x = 2.1:</mode>

```keys G02 after=G01 mode=STU
BLUE GRAPH GO 6 6 6 6 6
```

<mode m="STU">The readout shows <disp v="G02" kind="readout">x=2.1000 y=-0.9900</disp>. The open graph's
soft keys come in three pages: the first has ◀ and ▶, TRACE, (X,Y) and MARK; the second, ZOOM, the
zooms; the third, FCN, the tools. ▸, the last soft key, moves to the next page, and from FCN back to
the first. EXTR searches near the trace for a lowest or highest point, by the same kind of search as
SOLVE, so it too is a very close number, not a rule:</mode>

```keys G03 after=G02 mode=STU
▸ ▸ EXTR
```

<mode m="STU">The readout shows <disp v="G03" kind="readout">EXTRM: 2.0000</disp>, and the trace has moved
to it. Carrying on, SLOPE gives the slope at the trace. It works it out from the heights just either
side, the way program V's averages did, so in general it too is a very close number. (On a parabola
the average from the two sides is exactly the slope, so here it is exact.)</mode>

```keys G04 after=G03 mode=STU
SLOPE
```

<mode m="STU">The readout shows <disp v="G04" kind="readout">SLOPE: 0.0000</disp>, flat at the bottom.
Carrying on, TANL, gold on the same page, draws the tangent line and gives it as y = mx + b:</mode>

```keys G05 after=G04 mode=STU
GOLD TANL
```

<mode m="STU">The readout shows <disp v="G05" kind="readout">Y=0.0000·X-1.0000</disp>: the flat line
y = −1, touching the curve at its lowest point. Carrying on, C leaves the graph:</mode>

```keys G06 after=G05 mode=STU
C
```

## Exercises

1. Write down the tangent line to y = x² at x = 1. Compare it with the curve at x = 1.1.
2. Find the lowest point of g(x) = x² + 6x + 5.
3. Find the local maximum and minimum of k(x) = x³ − 12x.
4. h(x) = x³ has h′(0) = 0. Does h turn at 0?

## Answers

1. At 1, y = 1 and y′ = 2x = 2, so the tangent line is y = 1 + 2(x − 1), or y = 2x − 1. The curve at
   1.1:

   ```keys E01
   1.1 GOLD x²
   ```

   X shows <disp v="E01">1.2100</disp>, and the line:

   ```keys E01B
   1.1 ENTER 2 × 1 −
   ```

   X shows <disp v="E01B">1.2000</disp>: 0.1² apart, as for q.

2. g′(x) = 2x + 6, which is 0 at x = −3, its only zero. Either side, g′(−4) = −2 and g′(−2) = 2: a turn
   up. Its height, g(−3):

   ```keys E02
   3 +/− ENTER GOLD x² x↔y 6 × + 5 +
   ```

   X shows <disp v="E02">-4.0000</disp>. The lowest point is (−3, −4).

3. k′(x) = 3x² − 12, which is 0 when x² = 4: at x = 2 and x = −2. k′(−3) = 15 and k′(3) = 15 are
   positive and k′(0) = −12 is negative, so k rises, turns down at −2, and turns up at 2. The heights:

   ```keys E03
   2 ENTER ENTER 3 yˣ x↔y 12 × −
   ```

   X shows <disp v="E03">-16.0000</disp>, and

   ```keys E03B
   2 +/− ENTER ENTER 3 yˣ x↔y 12 × −
   ```

   X shows <disp v="E03B">16.0000</disp>. The local maximum is (−2, 16) and the local minimum (2, −16).

4. No. h′(x) = 3x² is positive on both sides of 0: h′(−1) = 3 and h′(1) = 3. So h rises, flattens for a
   moment at 0, and keeps rising. Just either side, h(−0.1) is below h(0) = 0 and h(0.1) above:

   ```keys E04
   0.1 ENTER 3 yˣ
   ```

   X shows <disp v="E04">0.0010</disp>, and h(−0.1) is −0.001: a slope of 0 with no turn.

## Checkpoint

Three questions on the whole unit. Work each by hand first, then give your answer; the calculator
checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item K01
prompt: f(x) = x³ − 2x. What is f′(2)?
topics: power-rule sum-multiple-rules
answer: type
calculator: no
slip: K01A | the −2x term dropped | Every term has a derivative: −2x gives −2.
slip: K01B | f(2), not f′(2) | That is the height at 2. Take the derivative first, then put in 2.
```

```item K02
prompt: The ball from lim-02 has gone d(t) = 2t² metres after t seconds. How fast is it going when it has rolled 32 metres?
topics: derivative-function
answer: type
calculator: no
slip: K02A | d′ of the distance | d′ takes a time. First find when it has rolled 32 metres.
slip: K02B | the time, not the speed | That is when. Now find d′ at that time.
```

```item K03
prompt: g(x) = x² − 6x + 10. How low does g go?
topics: extremes
answer: work
calculator: yes
keys: 3 ENTER GOLD x² x↔y 6 × − 10 +
slip: K03A | the x, not the height | That is where g is lowest. How low is g there?
slip: K03B | g(0) | Find where g′ is 0 first; 0 is only where the graph crosses the y axis.
```
