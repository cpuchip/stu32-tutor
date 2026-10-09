---
id: lim-02
title: Rates of change
requires: setup shift-keys rpn-arithmetic enter-copies stack-lift x-squared power powers-first fraction-bar change-sign sto rcl letter-keys type-e neg-e display-rounds slope function program-entry xeq-program stopped-program limit limit-by-approach digits-floor
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Rates of change

A ball rolls down a ramp, and after t seconds it has gone d(t) = 2t² metres. It speeds up as it goes:
in the first second it covers 2 metres, and by the end of the third it has covered 18 metres. How fast
is it going at one moment, at t = 1 exactly? A speed is distance over time, but at one moment no time
passes. This lesson answers the question with a limit (lim-01), and finds where the calculator's 34
digits stop helping.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. From the program on, the examples are one chain
through the next two sections and the first exercise, each carrying on from the one before; the other
examples start fresh.

<mode m="35s,STU">In this mode XEQ waits, after the label's letter, for ENTER; the keys below show the
ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## The average rate

Over a stretch of time, the ball's average speed is the distance it covers divided by the time it
takes. From t = 1 to t = 3 it goes from d(1) = 2 × 1² = 2 metres to d(3) = 2 × 3² = 18 metres, so its
average speed is (18 − 2) ÷ (3 − 1). A function has such an average rate of change between any two
different points where it has values: (f(b) − f(a)) ÷ (b − a), how much f changed over how much x
changed. On a graph it is the slope (lin-01) of the straight line through the two points. Work out the
top of the fraction, then the bottom, then divide:

```keys A01
2 ENTER 3 GOLD x² × 2 ENTER 1 GOLD x² × − 3 ENTER 1 − ÷
```

X shows <disp v="A01">8.0000</disp> metres a second, on average. But the ball went slower than that near
t = 1 and faster near t = 3.

## The rate at an instant

To find the speed at t = 1, take the average over a short time h around it, from t = 1 to t = 1 + h:
(d(1 + h) − d(1)) ÷ h. Then make h smaller and smaller, from both sides, as a limit is checked (lim-01),
and see what number the averages close in on. That limit is the rate of change at an instant, or at a
point when x is not a time: here, the ball's speed at that moment.

Program D works the average out for any h. With h in X, it keeps h in H, adds 1, squares, doubles to get
d(1 + h) = 2(1 + h)², takes away d(1) = 2, recalls h and divides. First GOLD GTO . . (fn-03) moves to the
top of program memory, so that D cannot land inside a program left stopped. D is on the yˣ key and H on
RCL. (If you have entered D before, the calculator refuses a second LBL D, as fn-01 showed; it is
already there.)

```keys P01A
GOLD GTO . . GOLD PRGM PRGM GOLD LBL D STO H 1 + GOLD x² 2 × 2 − RCL H ÷ BLUE RTN
```

The X line shows <disp v="P01A" kind="program">D012 RTN</disp>: D's twelfth line. Another number means a
key was missed or doubled (fn-01 showed how to fix a line). Carrying on, turn program entry off:

```keys P01 after=P01A
GOLD PRGM PRGM
```

Carrying on, h = 0.1:

```keys D01 after=P01
0.1 XEQ D
```
```keys D01 after=P01 mode=35s,STU
0.1 XEQ D ENTER
```

X shows <disp v="D01">4.2000</disp>. Carrying on, h = 0.01:

```keys D02 after=D01
0.01 XEQ D
```
```keys D02 after=D01 mode=35s,STU
0.01 XEQ D ENTER
```

X shows <disp v="D02">4.0200</disp>, and carrying on, h = 0.001:

```keys D03 after=D02
0.001 XEQ D
```
```keys D03 after=D02 mode=35s,STU
0.001 XEQ D ENTER
```

<disp v="D03">4.0020</disp>. And carrying on, from below, h = −0.001:

```keys D03B after=D03
0.001 +/− XEQ D
```
```keys D03B after=D03 mode=35s,STU
0.001 +/− XEQ D ENTER
```

X shows <disp v="D03B">3.9980</disp>. From both sides the averages close in on 4. The algebra says why.
(1 + h)² is 1 + 2h + h², so 2(1 + h)² is 2 + 4h + 2h², and d(1 + h) − d(1) is 4h + 2h². Divided by h,
for any h that is not 0, that is 4 + 2h, and as h shrinks from either side, 4 + 2h comes as near to 4 as
you like. So at t = 1 the ball is going 4 metres a second. This rate at an instant is called the
derivative of d at t = 1; finding derivatives is a large part of calculus.

## Where the digits run out

The calculator keeps 34 digits, so smaller h should be better, up to a point. Carrying on, h = 10⁻²⁰,
typed with E and +/− (rpn-03, num-04):

```keys D04 after=D03B
1 E 20 +/− XEQ D
```
```keys D04 after=D03B mode=35s,STU
1 E 20 +/− XEQ D ENTER
```

X shows <disp v="D04">4.0000</disp>. The true average is 4 + 2 × 10⁻²⁰, but the calculator gives exactly
4: the 2h² in d(1 + h), 2 × 10⁻⁴⁰, is below its 34th digit and is rounded away when 1 + h is squared.
The digits have started to run out, too far down to see. Carrying on, h = 10⁻³⁴:

```keys D05 after=D04
1 E 34 +/− XEQ D
```
```keys D05 after=D04 mode=35s,STU
1 E 34 +/− XEQ D ENTER
```

X shows <disp v="D05">0.0000</disp>. Near 1, 34 digits step by 10⁻³³, and a sum that falls between two
steps is rounded to the nearer one. 1 + 10⁻³⁴ is less than halfway to the next step, so it rounds to
1 (lim-01); d(1 + h) is then exactly d(1), and their difference is 0. Carrying on, h = 6 × 10⁻³⁴:

```keys D06 after=D05
6 E 34 +/− XEQ D
```
```keys D06 after=D05 mode=35s,STU
6 E 34 +/− XEQ D ENTER
```

X shows <disp v="D06">6.6667</disp>, far from 4. 1 + 6 × 10⁻³⁴ is more than halfway to the next step, so
it rounds up to 1 + 10⁻³³: the h that went into d is not the h it is divided by. From there nothing
else matters: d(1 + 10⁻³³) − d(1) is 4 × 10⁻³³ (the square drops only 10⁻⁶⁶, far below), and
4 × 10⁻³³ ÷ (6 × 10⁻³⁴) is 40 ÷ 6. The
subtraction lost nothing itself; what it did was leave only the one digit in which the two values
differ, so the small rounding of 1 + h became the whole answer. A subtraction of two nearly equal
numbers, which leaves only the digits where they differ so that any earlier rounding becomes all of the
result, is called cancellation. The lesson for the calculator: make h small enough to see the limit, and
no smaller. Here 0.001 already suggested 4.

## Exercises

1. Carrying on, what does D give for h = 10⁻⁴⁰? Why?
2. f(x) = x³. Work out its average rate of change from x = 2 to x = 2.001, and then to x = 2.0001. What is
   its rate of change at x = 2?
3. What is the average rate of change of f(x) = 2ˣ from x = 0 to x = 3?

## Answers

1. 0. 1 + 10⁻⁴⁰ is far less than halfway to the next step after 1, so it rounds to 1, and d(1 + h) − d(1)
   is 0, as for h = 10⁻³⁴:

   ```keys E01 after=D06
   1 E 40 +/− XEQ D
   ```
   ```keys E01 after=D06 mode=35s,STU
   1 E 40 +/− XEQ D ENTER
   ```

   X shows <disp v="E01">0.0000</disp>.

2. 12. The average is (2.001³ − 2³) ÷ 0.001, with 2³ = 8:

   ```keys E02
   2.001 ENTER 3 yˣ 8 − 0.001 ÷
   ```

   X shows <disp v="E02">12.0060</disp>. Carrying on, with h = 0.0001:

   ```keys E02B after=E02
   2.0001 ENTER 3 yˣ 8 − 0.0001 ÷
   ```

   X shows <disp v="E02B">12.0006</disp>. The algebra: (2 + h)³ is 8 + 12h + 6h² + h³, so the average is
   12 + 6h + h², which comes as near to 12 as you like as h shrinks.

3. 2ˣ is 2⁰ = 1 at 0 and 2³ at 3, so the average rate is (2³ − 1) ÷ (3 − 0):

   ```keys E03
   2 ENTER 3 yˣ 1 − 3 ÷
   ```

   X shows <disp v="E03">2.3333</disp>.

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP10A
prompt: What is the average rate of change of x² from x = 2 to x = 4?
topics: average-rate
answer: type
calculator: no
slip: CP10A1 | forgot to divide | Divide the change in x² by the change in x, 4 − 2.
slip: CP10A2 | divided by 4 | The change in x is 4 − 2 = 2, not 4.
```

```item CP10B
prompt: What does (x² − 9) ÷ (x − 3) close in on as x approaches 3?
topics: limit limit-by-approach
answer: type
calculator: no
slip: CP10B1 | 0 ÷ 0 read as 0 | At 3 it is 0 ÷ 0, which tells nothing; near 3 it equals x + 3.
slip: CP10B2 | x itself | Near 3 it equals x + 3, so it closes in on 3 + 3.
```
