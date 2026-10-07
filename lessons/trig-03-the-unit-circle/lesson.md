---
id: trig-03
title: The unit circle
status: draft prose (non-author read taken; accepted for accuracy by abacus #4683; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
display: FIX 4
---

# The unit circle

trig-02 defined sine and cosine with a right triangle, whose other angles are less than 90 degrees.
But SIN and COS take any angle: 120, 200, 390, or −30. They come from a circle.

## Before you start

The setup from trig-01: the mode you chose, FIX 4, and degrees. Every example starts fresh.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
```

## Sine and cosine on a circle

Draw axes, as in fn-02, and a circle of radius 1 centred where they cross, at O: the unit circle.
An angle, written θ (the Greek letter theta, often used for angles), starts along the positive x axis
and its moving side, its arm, turns anticlockwise (counterclockwise). The arm meets the circle at a
point P, and P's coordinates are the cosine and the sine of the angle: across = cos θ, up = sin θ.
"Across" and "up" are coordinates, so they carry a sign: negative to the left of the y axis, and
negative below the x axis.

```
                        y
                        |
                 .  '   +   '  .
              '         |    P     '
            .           |   /|       .
           '            |  / |        '
          .             | /  | sin θ   .
          .             |/ θ |         .
   - -1 --+-------------O----+---------+-- 1 -- x
          .             |cos θ         .
          .             |              .
           '            |             '
            .           |            .
              '         |          '
                 '  .   +   .  '
                        |
```

For an angle between 0 and 90 degrees this is trig-02's triangle: O, P, and the point below P on the x
axis make a right triangle whose hypotenuse is the arm, of length 1, so sin θ = up ÷ 1 and
cos θ = across ÷ 1. Beyond 90 degrees there is no right triangle with that angle, but P still has
coordinates, and those are the sine and cosine.

At 120 degrees the arm has turned past the y axis, to the left:

```keys U01
120 COS
```

X shows <disp v="U01">-0.5000</disp>: P is half a unit left of the y axis.

```keys U02
120 SIN
```

X shows <disp v="U02">0.8660</disp>: still above the x axis. At 200 degrees the arm is past 180, below
and to the left:

```keys U03
200 COS
```

X shows <disp v="U03">-0.9397</disp>.

```keys U04
200 SIN
```

X shows <disp v="U04">-0.3420</disp>: both negative. Left of the y axis cosine is negative; below the
x axis sine is negative.

## cos²θ + sin²θ = 1

For any angle, O, P and the point on the x axis straight below or above P make a right triangle,
whatever side of the axes P is on. Its sides are as long as the across and the up, without their
signs, and its hypotenuse is the arm, 1. Pythagoras' rule (trig-02 used it the other way round) says
that in a right triangle the two shorter sides squared add up to the longest squared. So, writing
sin²θ for (sin θ)², cos²θ + sin²θ = 1, for every angle: squaring removes the signs. Check it at 200
degrees, with x² (gold above √x) squaring each:

```keys U05
200 SIN GOLD x² 200 COS GOLD x² +
```

X shows <disp v="U05">1.0000</disp>.

## Around again

A full turn of 360 degrees brings the arm back where it started, so 390 degrees is the same point as
30:

```keys U08
390 SIN
```

X shows <disp v="U08">0.5000</disp>, the sine of 30 degrees. A negative angle turns clockwise
instead:

```keys U09
30 +/− SIN
```

X shows <disp v="U09">-0.5000</disp>: the arm is 30 degrees below the x axis, and P is half a unit
below it. −30 degrees is the same point as 360 − 30 = 330 degrees.

## One sine, two angles

The point at 150 degrees is the mirror image of the point at 30 degrees, across the y axis: turning
30 short of 180 lands at the same height as turning 30 past 0, on the other side.

```keys U06
150 SIN
```

X shows <disp v="U06">0.5000</disp>, the same as sin 30°. So a sine of 0.5 belongs to two angles
between 0 and 360. ASIN can give only one:

```keys U07
0.5 GOLD ASIN
```

X shows <disp v="U07">30.0000</disp>. ASIN always answers between −90 and 90 degrees, and the other
angle with the same sine is 180 minus that one, here 150. (Only at the very top and bottom, sin θ = 1
or −1, is there one angle and no mirror.) This is what trig-02 promised: for a right triangle the
answer between 0 and 90 is the one meant, but in general it is one of two.

Cosine has its own mirror: across the x axis. The point at −θ, or 360 − θ, is straight below the
point at θ, the same distance across. So the other angle with the same cosine is 360 minus the one
ACOS gives, and ACOS always answers between 0 and 180. (At cos θ = 1 or −1, at 0 and 180 degrees,
the point is on the x axis and is its own mirror.) The "180 minus" rule is sine's only.

## Exercise

Find both angles between 0 and 360 degrees whose cosine is −0.5.

## Answer

ACOS gives one:

```keys E01
0.5 +/− GOLD ACOS
```

X shows <disp v="E01">120.0000</disp>. The other is cosine's mirror, 360 − 120 = 240. Check:

```keys E02
240 COS
```

X shows <disp v="E02">-0.5000</disp>. The two angles are 120 and 240 degrees. (180 − 120 = 60 would be
sine's mirror, and cos 60° is +0.5, not −0.5.)
