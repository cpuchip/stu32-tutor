---
id: der-01
title: The derivative
requires: setup shift-keys rpn-arithmetic x-squared change-sign sto rcl letter-keys function slope program-entry xeq-program stopped-program limit average-rate instant-rate derivative eqn-typing xeq-check equation-list power
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The derivative

lim-02's ball rolls down a ramp, and after t seconds it has gone d(t) = 2t² metres. At t = 1 it is going
4 metres a second: the averages over shorter and shorter times close in on 4. But the ball has a speed
at every moment, not only at t = 1. This lesson finds them all at once, as a new function, and tries
it on the calculator.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. The program and the examples after it are one
chain, each carrying on from the one before; the exercises start fresh.

<mode m="35s,STU">In this mode XEQ, when it runs a program, waits after the label's letter for ENTER;
the keys below show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## The speed at every moment

lim-02 worked at t = 1. Do the same algebra at any time a. Over the short time from a to a + h, the
ball goes d(a + h) − d(a) = 2(a + h)² − 2a². Since (a + h)² = a² + 2ah + h², the first part is
2(a² + 2ah + h²) = 2a² + 4ah + 2h², and taking away 2a² leaves 4ah + 2h². Divided by the time h, the
average speed is 4a + 2h, for any h that is not 0. As h shrinks from either side, 4a + 2h closes in on
4a, because 2h shrinks to 0. h = 0 could not go into the first fraction (it would be 0 ÷ 0), but
4a + 2h has no division left in it.

So at time a the ball is going 4a metres a second: 4 at t = 1, as lim-02 found, and 12 at t = 3. a was
any time, so call it t again: one rule gives the speed at every moment, and the speed is itself a
function of t. It is called the derivative of d, and written d′, read "d prime". Its value at t is
d′(t), and here d′(t) = 4t.

## Checking it

Program V works out lim-02's average for any time, not only t = 1. (lim-02's program D may still be in
memory, so this one is V, for velocity.) The time a waits in A; with h in X,
V keeps h in H, adds a, squares, doubles to get d(a + h), then takes away d(a) = 2a², worked out the
same way, and divides by h. First GOLD GTO . . (fn-03) moves to the top of program memory. (If you
have entered V before, the calculator refuses a second LBL V, as fn-01 showed; it is already there.)

```keys V01A
GOLD GTO . . GOLD PRGM PRGM GOLD LBL V STO H RCL A + GOLD x² 2 × RCL A GOLD x² 2 × − RCL H ÷ BLUE RTN
```

The X line shows <disp v="V01A" kind="program">V015 RTN</disp>: V's fifteenth line. Another number
means a key was missed or doubled (fn-01 showed how to fix a line). Carrying on, turn program entry
off:

```keys V01 after=V01A
GOLD PRGM PRGM
```

Carrying on, the speed at t = 3: store 3 in A, then run V with h = 0.001.

```keys D01 after=V01
3 STO A 0.001 XEQ V
```
```keys D01 after=V01 mode=35s,STU
3 STO A 0.001 XEQ V ENTER
```

X shows <disp v="D01">12.0020</disp>, which is 4a + 2h for a = 3 and h = 0.001, just as the algebra
said. Carrying on, from below:

```keys D02 after=D01
0.001 +/− XEQ V
```
```keys D02 after=D01 mode=35s,STU
0.001 +/− XEQ V ENTER
```

X shows <disp v="D02">11.9980</disp>, 2h below 12 this time. Carrying on, a ten times smaller h:

```keys D02B after=D02
0.0001 XEQ V
```
```keys D02B after=D02 mode=35s,STU
0.0001 XEQ V ENTER
```

X shows <disp v="D02B">12.0002</disp>: nearer still. The averages close in on 12, which is d′(3) = 4 × 3,
as the rule said. Carrying on, at half a second, where d′ says 2:

```keys D03 after=D02B
0.5 STO A 0.001 XEQ V
```
```keys D03 after=D02B mode=35s,STU
0.5 STO A 0.001 XEQ V ENTER
```

X shows <disp v="D03">2.0020</disp>: close to 2, off by 2h, as at t = 3. Program V only ever gives
averages. At each time you try, they land within 2h of the rule, which agrees with it but does not
prove it; the algebra is what proves the rule for every t.

## A picture: the tangent line

On a graph of d, the average speed from a to a + h is the slope (lin-01) of the straight line through
the two points (a, d(a)) and (a + h, d(a + h)). As h shrinks, the second point slides along the curve
toward the first, and the lines through them close in on one line through (a, d(a)), as the averages
close in on a number. That line is the tangent line at a, and its slope is the number the averages
close in on, d′(a). No line through two points ever is the tangent, since h is never 0; the tangent is
their limit. So the derivative is two things at once: the rate of change at a moment, and the slope of
the curve at a point.

## The derivative on the calculator

<mode m="33s,35s">The 33s and 35s modes have no key that finds a derivative as a rule. In these
modes the algebra above is how a derivative is found, and a program like V tries it.</mode><mode m="STU">STU mode's algebra system, Casimir, finds the
derivative as a rule. Type the expression 2t² in the equation list (eq-01, fn-02), with T for t and yˣ
for the power. With the equation showing, the list's fifth soft key, CAS, opens Casimir's menu; D/DX
asks which variable, as SOLVE does, and T answers. (The d's in D/DX, short for d/dx, mean "a small
change in", as in a small change in d over a small change in t; they are not the ball's d.)</mode>

```keys B01 mode=STU
GOLD EQN 2 × RCL T yˣ 2 ENTER CAS D/DX T
```

<mode m="STU">The screen shows <disp v="B01" kind="eqn">4×T</disp>: d′(t) = 4t, the rule the algebra
found. Casimir puts the derivative in the list as a new equation, after the one it came from, which is
kept. A derivative found this way is an equation like any other, so XEQ works it out at a time
(eq-01): it asks for T, and 3 then R/S answers:</mode>

```keys B02 after=B01 mode=STU
XEQ 3 R/S
```

<mode m="STU">X shows <disp v="B02">12.0000</disp>: d′(3), the speed the program closed in on.</mode>

## Exercises

1. How fast is the ball going at t = 5? Use d′, then check with one average over h = 0.001, typed
   directly: (d(5.001) − d(5)) ÷ 0.001.
2. f(x) = x². Find f′(x) by the algebra above, with (a + h)² − a² in place of the ball's. Check it at
   x = 3 with one average over h = 0.001.<mode m="STU"> Then check the rule with D/DX.</mode>
3. How fast is the ball going when it has rolled 18 metres?

## Answers

1. d′(5) = 4 × 5 = 20 metres a second. The average from 5 to 5.001 is (2 × 5.001² − 50) ÷ 0.001:

   ```keys E01
   5.001 GOLD x² 2 × 50 − 0.001 ÷
   ```

   X shows <disp v="E01">20.0020</disp>: 20 + 2h, close to 20.

2. (a + h)² − a² = 2ah + h², and divided by h that is 2a + h, which closes in on 2a. So f′(x) = 2x, and
   f′(3) = 6. The average from 3 to 3.001:

   ```keys E02
   3.001 GOLD x² 9 − 0.001 ÷
   ```

   X shows <disp v="E02">6.0010</disp>.<mode m="STU"> And D/DX, on x² typed with X:</mode>

   ```keys E02B mode=STU
   GOLD EQN RCL X yˣ 2 ENTER CAS D/DX X
   ```

   <mode m="STU">The screen shows <disp v="E02B" kind="eqn">2×X</disp>. Turn Equation mode off before
   the next exercise, since a digit typed while an equation shows starts a new equation (eq-01):</mode>

   ```keys E02C after=E02B mode=STU
   GOLD EQN
   ```

3. First when: 2t² = 18, so t² = 9, and t = 3 (a time after the start, so not −3). Then
   d′(3) = 4 × 3 = 12 metres a second. Not d′(18), which is 72: d′ takes a time, not a distance, and
   d′(18) is the speed 18 seconds in. The check, from 3 to 3.001:

   ```keys E03
   3.001 GOLD x² 2 × 18 − 0.001 ÷
   ```

   X shows <disp v="E03">12.0020</disp>.
