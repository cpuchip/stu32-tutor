---
id: int-01
title: Area under a curve
requires: setup shift-keys rpn-arithmetic stack-lift swap-roll x-squared power change-sign fix sto rcl sto-arithmetic letter-keys display-rounds eqn-typing times-matters equation-list eqn-last-viewed eqn-power expression solve solve-prompts program-entry xeq-program stopped-program loop summing-loop limit limit-by-approach
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Area under a curve

How much area lies under the curve y = x², above the x axis, from x = 0 to x = 3? The region has a
curved top, so no formula for a rectangle or a triangle fits it. But rectangles can come close: cut the
region into thin strips, treat each strip as a rectangle, and add up their areas, height times width.
For a curve like this one, the thinner the strips, the closer the sum comes to the area. As the strips
get thinner without end, the sums have a limit (lim-01, here with the number of strips growing rather
than x approaching a number), and that limit is called the integral. When the curve stays above the
axis, as this one does, the integral is the area. This lesson adds up rectangles with a program, then
lets the calculator's built-in integral do the work.

## From before

Two from before, by hand: a sum from seq-01, and squares from unit 1. This lesson adds squares up.

```item IN1F1
prompt: Add 1 + 2 + 3 + … + 10.
topics: arithmetic-sum
answer: type
calculator: no
slip: IN1F1A | forgot to halve | Pair the first and last: 10 pairs of 11 counts each number twice, so halve 110.
```

```item IN1F2
prompt: Work out 1² + 2² + 3².
topics: x-squared
answer: type
calculator: no
slip: IN1F2A | squared the sum | Square each first: 1 + 4 + 9. (1 + 2 + 3)² is another number.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. The program's examples are one chain, each
carrying on from the one before; the others start fresh, except where one says it carries on.

<mode m="35s,STU">In this mode XEQ and GTO wait, after the label's letter, for ENTER; the keys below
show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Adding up rectangles

Cut the stretch from 0 to 3 into n strips of equal width, 3 ÷ n. Strip number k ends at x = 3k ÷ n, and
a rectangle as tall as the curve there is (3k ÷ n)² tall, so its area is (3k ÷ n)² × (3 ÷ n). Add those
for k = 1 to n.

Program A does the adding, with a loop as in fn-02 and a total as in seq-01. Give it n, a whole number
from 1 to 999, in X. It keeps n in N, and builds the counter in I: 1 + n ÷ 1000, which is 1 followed by n
written in three digits, so n = 30 gives 1.030, counting from 1 up to 30. It sets the total T to 0. Its
loop, B, takes k from the counter's whole part, works out strip k's area, and adds it to T with STO +;
ISG counts on and GTO goes back to B until the count passes n. Then RCL T brings the total to X. First
GOLD GTO . . (fn-03) goes to the top of program memory, so that A cannot land inside a program left
stopped. A is on √x, B on eˣ, N on x↔y, I on R↓ and T on 8:

```keys P01A
GOLD GTO . . GOLD PRGM PRGM GOLD LBL A STO N 1000 ÷ 1 + STO I 0 STO T GOLD LBL B RCL I BLUE POW IP 3 × RCL N ÷ GOLD x² 3 × RCL N ÷ STO + T BLUE ISG I GOLD GTO B RCL T BLUE RTN
```
```keys P01A mode=35s,STU
GOLD GTO . . GOLD PRGM PRGM GOLD LBL A STO N 1000 ÷ 1 + STO I 0 STO T GOLD LBL B RCL I BLUE POW IP 3 × RCL N ÷ GOLD x² 3 × RCL N ÷ STO + T BLUE ISG I GOLD GTO B ENTER RCL T BLUE RTN
```

The X line shows <disp v="P01A" kind="program">B017 RTN</disp>: B's lines, from LBL B to RTN, number 17.
Another number means a key in B was missed or doubled. A slip in A's first nine lines does not change
it, so check the totals below against the ones shown. Carrying on, turn program entry off:

```keys P01 after=P01A
GOLD PRGM PRGM
```

Carrying on, 3 strips, each 1 wide:

```keys A01 after=P01
3 XEQ A
```
```keys A01 after=P01 mode=35s,STU
3 XEQ A ENTER
```

X shows <disp v="A01">14.0000</disp>: 1 + 4 + 9, the three rectangles of heights 1², 2² and 3². x² rises
from 0 to 3, so each rectangle, as tall as the curve at its right end, sticks out above the curve, and
14 is too much. Carrying on, 30 strips:

```keys A02 after=A01
30 XEQ A
```
```keys A02 after=A01 mode=35s,STU
30 XEQ A ENTER
```

X shows <disp v="A02">9.4550</disp>, and carrying on, 300:

```keys A03 after=A02
300 XEQ A
```
```keys A03 after=A02 mode=35s,STU
300 XEQ A ENTER
```

<disp v="A03">9.0451</disp>. The sums seem to close in on 9 as the strips thin out, and the next section
confirms it: the area under y = x² from 0 to 3 is 9.

## The built-in integral

The calculator can estimate the integral itself. ∫, gold above 8, finds the integral of the expression
showing in Equation mode between two ends on the stack: the lower end in Y and the upper in X. (These
ends are also called the integral's limits, a second meaning of the word.) Type x² as an expression,
with no = sign (poly-02):

```keys I01
GOLD EQN RCL X yˣ 2 ENTER
```

The screen shows <disp v="I01" kind="eqn">X^2</disp>. Carrying on, turn Equation mode off with EQN, since
in Equation mode digits type into an equation (eq-01); put 0 and 3 on the stack; show the expression
again with EQN; and press ∫. Like SOLVE (eq-02), it asks which variable to integrate over; answer X:

```keys I01B after=I01
GOLD EQN 0 ENTER 3 GOLD EQN GOLD ∫ X
```

The X line shows <disp v="I01B" kind="view">∫=9.0000</disp>. The calculator adds up many slices, chosen
more cleverly than the program's equal ones, until its answer is good enough for the places on the
screen. It also leaves in Y its own cautious figure for how far off the answer might be. Carrying on, C
leaves the view and x↔y brings that figure down:

```keys I01C after=I01B
C x↔y
```

X shows <disp v="I01C">0.0003</disp>. That is a cautious estimate, meant to be on the safe side, not the
actual error: the true error is usually far smaller, and here the 9 is exactly right. With more places showing, run ∫ again and the figure shrinks:
at FIX 8 it is three hundred-millionths.

## Area below the axis

Where the curve is below the x axis, its rectangles have negative heights, so height × width is
negative, and the integral counts that area as negative. y = x from −1 to 1 has a triangle below the
axis from −1 to 0 and a mirror image of it, of the same size, above the axis from 0 to 1. Type x as an
expression, put −1 and 1 on the stack, and integrate:

```keys S01
GOLD EQN RCL X ENTER GOLD EQN 1 +/− ENTER 1 GOLD EQN GOLD ∫ X
```

The X line shows <disp v="S01" kind="view">∫=0.0000</disp>. The two triangles are each 0.5 in area, so
the region between the line and the axis has area 1; but the integral is the area above the axis minus
the area below it, 0.5 − 0.5, which is 0.

## Exercises

1. What is the area under y = 3x² from x = 0 to x = 2?
2. Work out the integral of y = x from x = −2 to x = 1. What is the area between the line and the axis
   over that stretch?

## Answers

1. 8. 3x² stays above the axis, so its integral is the area. Type it (with the ×, as eq-01
   said), put 0 and 2 on the stack, and integrate:

   ```keys E01
   GOLD EQN 3 × RCL X yˣ 2 ENTER GOLD EQN 0 ENTER 2 GOLD EQN GOLD ∫ X
   ```

   The X line shows <disp v="E01" kind="view">∫=8.0000</disp>.

2. The integral is −1.5 and the area is 2.5. From −2 to 0 the line is below the axis, a triangle of
   area 2 × 2 ÷ 2 = 2; from 0 to 1 it is above, a triangle of area 1 × 1 ÷ 2 = 0.5. The integral is
   0.5 − 2:

   ```keys E02
   GOLD EQN RCL X ENTER GOLD EQN 2 +/− ENTER 1 GOLD EQN GOLD ∫ X
   ```

   The X line shows <disp v="E02" kind="view">∫=-1.5000</disp>, and the area is 2 + 0.5.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item IN1M1
prompt: Two strips of width 1 stand under y = x², with heights taken at x = 1 and x = 2. What is their total area?
topics: riemann-sum
answer: type
calculator: no
slip: IN1M1A | squared the sum | Each strip is its own height times its width, 1: 1² + 2².
```

```item IN1M2
prompt: What does (x² − 36) ÷ (x − 6) close in on as x approaches 6?
topics: limit
answer: type
calculator: no
slip: IN1M2A | 0 ÷ 0 read as 0 | Near 6 the fraction is x + 6, which closes in on 12.
```

```item IN1M3
prompt: y = −3 from x = 0 to x = 2: what does that stretch count for in the integral?
topics: signed-area
answer: type
calculator: no
slip: IN1M3A | counted it as positive | Area below the axis counts negative: −3 × 2.
```

```item IN1M4
prompt: The sequence 5, 8, 11, … goes on the same way. What is its 8th term?
topics: arithmetic-sequence
answer: type
calculator: no
slip: IN1M4A | eight steps, not seven | The 8th term is 7 steps after the first: 5 + 7 × 3.
```

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP12A
prompt: What is the area under y = 2x from x = 0 to x = 3?
topics: integral riemann-sum
answer: type
calculator: no
slip: CP12A1 | the whole rectangle | The area is a triangle, half the 3 by 6 rectangle.
slip: CP12A2 | the slope times the width | The height at x = 3 is 6: the triangle is ½ × 3 × 6.
```

```item CP12B
prompt: What is the integral of y = x − 2 from x = 0 to x = 2?
topics: integral signed-area
answer: type
calculator: no
slip: CP12B1 | the area, not the integral | The line is below the x axis there, so the integral counts that area as negative.
slip: CP12B2 | the rectangle | It is a triangle, ½ × 2 × 2, below the axis.
```
