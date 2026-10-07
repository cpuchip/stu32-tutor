---
id: trig-01
title: Degrees and radians
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
display: FIX 4
---

# Degrees and radians

Angles are measured in two units. Degrees divide a full turn into 360. Radians measure an angle by
the arc it cuts from a circle centred on the angle's corner: one radian is the angle whose arc is
as long as the circle's radius. A full circle's edge is 2π times its radius, so the radius fits
around the edge 2π times, and a full turn is 2π radians; half a turn, 180 degrees, is π radians.
The calculator's sine and the other angle functions read angles in whichever unit is set, and a
wrong unit gives a wrong answer with no warning. This lesson sets the unit, sees what it changes,
and converts between the two.

## Before you start

The setup from rpn-01, the mode you chose and FIX 4, and one thing more: the angle unit. ∡MODE is
blue above 2 (DISP is gold above the same key), and its soft keys are DEG, RAD and GRAD. GRAD is a
third unit, with 400 in a turn, that these lessons do not use. The setup chooses DEG:

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
```

Every example is written from that setup, in degrees, except where one says it carries on. If you
work through in order, some examples switch to radians and your calculator stays there; that does
not change the conversions (they ignore the unit), and the one example that needs degrees sets
them again.

## The same keys, two answers

SIN, the fourth key of the second row (after STO, RCL and R↓), gives the sine of the angle in X.
What a sine is comes in trig-02, with right triangles; here it is only a way to see the unit
matter. The sine of an angle x is written sin x, so the sine of 30 degrees is sin 30°. In degrees:

```keys A01
30 SIN
```

X shows <disp v="A01">0.5000</disp>: the sine of 30 degrees is one half. Now switch to radians and
press the same keys:

```keys A02 after=A01
BLUE ∡MODE RAD 30 SIN
```

X shows <disp v="A02">-0.9880</disp>, the sine of 30 radians, an angle of almost five full turns.
There is no error message, because 30 radians is a real angle; it is just not the one meant. The
only sign is the status band, which now shows <disp v="A02" kind="status">RAD</disp>. In degrees it
shows no unit at all. Look at the status band before any calculation with angles.

## Converting

The unit changes how SIN and the other angle functions read X; it does not convert anything.
Setting RAD does not turn 60 into radians. To convert a number, use →RAD and →DEG, which work the
same whatever the unit. →RAD, blue above COS (the key after SIN), turns degrees in X into radians.
Half a turn:

```keys C01
180 BLUE →RAD
```

X shows <disp v="C01">3.1416</disp>: π. →DEG, blue above TAN (the key after COS), goes the other
way. One radian in degrees:

```keys C02
1 BLUE →DEG
```

X shows <disp v="C02">57.2958</disp>: a radian is a little over 57 degrees.

## π in radians

In radians, the angles that come up most are fractions of π. 30 degrees is a twelfth of a turn
(360 ÷ 30 = 12), and a turn is 2π radians, so 30 degrees is 2π ÷ 12 = π ÷ 6. π has a key of its
own, gold above E (the E key of rpn-03):

```keys R01
BLUE ∡MODE RAD GOLD π 6 ÷ SIN
```

X shows <disp v="R01">0.5000</disp>, as sin 30° did in degrees: the same angle, in the other unit.

## Arc length

Radians make the length of an arc simple: on a circle of radius r, an angle of θ radians cuts an
arc of length r × θ. That is the definition of a radian, stretched: one radian cuts one radius, so
θ radians cut θ radii. An angle of 60 degrees on a circle of radius 10, converted first:

```keys S01
60 BLUE →RAD 10 ×
```

X shows <disp v="S01">10.4720</disp>: a little more than the radius, as 60 degrees is a little more
than one radian.

## Exercises

1. What is 45 degrees in radians?
2. What is 2 radians in degrees?
3. What is the sine of 45 degrees? If your calculator is still in radians from an earlier example,
   set degrees first.

## Answers

1. The keys:

   ```keys E01
   45 BLUE →RAD
   ```

   X shows <disp v="E01">0.7854</disp>: π ÷ 4, an eighth of a turn.

2. The keys:

   ```keys E02
   2 BLUE →DEG
   ```

   X shows <disp v="E02">114.5916</disp>.

3. Set degrees, then SIN:

   ```keys E03
   BLUE ∡MODE DEG 45 SIN
   ```

   X shows <disp v="E03">0.7071</disp>.
