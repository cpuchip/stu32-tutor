---
id: trig-04
title: Polar and rectangular
requires: setup shift-keys soft-keys enter-copies swap-roll change-sign angle-unit sin-key trig-ratios inverse-trig pythagoras unit-circle pythagorean-identity full-turn trig-mirror
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
display: FIX 4
---

# Polar and rectangular

A point on a plane can be named two ways. Rectangular coordinates say how far across and how far up:
(x, y), the across and up of trig-03. Polar coordinates say how far the point is from O, where the
axes cross, and in which direction: a distance r and an angle θ, measured anticlockwise from the
positive x axis as in trig-03. A point in polar form is written (r, θ).

```
            y
            |
            |         * (x, y), or (r, θ)
            |        /|
            |     r / |
            |      /  | y
            |     /   |
            |    / θ  |
   ---------O---------+------ x
            |    x
```

The point lies on the arm from trig-03, r times as far out as the point P on the unit circle. Every length
is stretched by r and the angle stays the same, as with the scaled triangles of trig-02, so

x = r cos θ, y = r sin θ, and r = √(x² + y²)

by Pythagoras' rule, squaring removing any signs (trig-03). The point (3, 4) is 5 from O, since
3² + 4² = 5², at an angle of about 53 degrees. This lesson converts between the two forms. Both
conversions use the angle unit that is set, so check it first (trig-01); here it is degrees.

## Before you start

The setup from trig-01: the mode you chose, FIX 4, and degrees. Every example starts fresh, except
where one says it carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
```

## Rectangular to polar

The ANGLE menu, blue above SIN, has →POL. It takes y in Y and x in X, so type y first, then ENTER,
then x, and gives back r in X and the angle in Y. For (3, 4):

```keys P01
4 ENTER 3 BLUE ANGLE →POL
```

X shows <disp v="P01">5.0000</disp>: r. The angle is in Y; x↔y brings it down:

```keys P02 after=P01
x↔y
```

X shows <disp v="P02">53.1301</disp> degrees. So (3, 4) is (5, 53.1301°) in polar form.

The angle follows the point all the way round, which ATAN alone cannot. For (−3, 4), up and to the
left:

```keys Q01
4 ENTER 3 +/− BLUE ANGLE →POL x↔y
```

X shows <disp v="Q01">126.8699</disp> degrees, past 90, where the point is. ATAN of the ratio 4 ÷ −3
gives a different answer:

```keys Q02
4 ENTER 3 +/− ÷ GOLD ATAN
```

X shows <disp v="Q02">-53.1301</disp>. Like ASIN in trig-03, ATAN answers only between −90 and 90
degrees, and a ratio cannot tell (−3, 4) from (3, −4): 4 ÷ −3 and −4 ÷ 3 are the same number. So
ATAN's −53.1301 points at (3, −4), down and to the right; for a point on the left you would have to
add 180 yourself. →POL knows the signs of both coordinates, so it puts the angle on the correct side
without that. Its angles run from just above −180 up to and including 180 degrees (a point straight
left gets 180, never −180): a point below the x axis gets a negative angle, and adding 360 gives
the same direction between 0 and 360 (trig-03).

## Polar to rectangular

→REC goes the other way: it takes the angle in Y and r in X, and gives x in X and y in Y, by
x = r cos θ and y = r sin θ. A point 10 from O at 30 degrees:

```keys R01
30 ENTER 10 BLUE ANGLE →REC
```

X shows <disp v="R01">8.6603</disp>: x, which is 10 cos 30°. Bring y down:

```keys R02 after=R01
x↔y
```

X shows <disp v="R02">5.0000</disp>: y, 10 sin 30°.

## Exercises

1. Write the point (−5, −12) in polar form. What would ATAN of −12 ÷ −5 give instead?
2. Write the polar point (2, 135°) in rectangular form.

## Answers

1. y first:

   ```keys E01
   12 +/− ENTER 5 +/− BLUE ANGLE →POL
   ```

   X shows <disp v="E01">13.0000</disp>: r = √(25 + 144). Then the angle:

   ```keys E01B after=E01
   x↔y
   ```

   X shows <disp v="E01B">-112.6199</disp> degrees: down and to the left, so (−5, −12) is
   (13, −112.6199°), the same direction as 247.3801° (add 360). ATAN of −12 ÷ −5 = 2.4 would give
   about 67.38 degrees, up and to the right: the opposite direction.

2. The angle first, then r:

   ```keys E02
   135 ENTER 2 BLUE ANGLE →REC
   ```

   X shows <disp v="E02">-1.4142</disp>: x, to the left. Then y:

   ```keys E02B after=E02
   x↔y
   ```

   X shows <disp v="E02B">1.4142</disp>, above: the point is up and to the left, at 135 degrees.

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP7A
prompt: A right triangle's two shorter sides are 5 and 12. How long is its hypotenuse?
topics: pythagoras
answer: type
calculator: no
slip: CP7A1 | added the sides | Square each side, add, then take the square root: 25 + 144 = 169.
slip: CP7A2 | stopped at the square | That is the hypotenuse squared; take its square root.
```

```item CP7B
prompt: In a right triangle, the hypotenuse is 10 and the side opposite angle A is 6. What is sin A?
topics: trig-ratios pythagoras
answer: type
calculator: no
slip: CP7B1 | the cosine | That is the adjacent side over the hypotenuse, the cosine. The sine is the opposite side over the hypotenuse: 6 ÷ 10.
slip: CP7B2 | the tangent | That is the opposite side over the adjacent side, the tangent. The sine divides by the hypotenuse.
```

```item CP7C
prompt: A point is at r = 2 and angle 90°. What is its x?
topics: to-rect
answer: type
calculator: no
slip: CP7C1 | r itself | At 90° the point is straight up, on the y axis, so x = r × cos 90° = 0.
```
