---
id: sky-02
title: Angles with your hand
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: degrees angle-kinds partial-products long-division
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
display: FIX 4
---

# Angles with your hand

How far apart are two stars? Not in kilometers: from the ground there is no way to tell how far away either one
is. But you can say how far apart they look, as an angle, the turn your eye makes from one to the other, in degrees
(angle-01). Astronomers measure those angles with fine instruments. You can measure them, roughly, with your hand.
How?

## From before

```item SK2F1
prompt: How many degrees is a right angle?
topics: angle-kinds
answer: type
calculator: no
slip: SK2F1A | took a straight angle | A straight angle is 180°; a right angle is half of it, a square corner.
```

```item SK2F2
prompt: How many degrees is half a turn?
topics: degrees
answer: type
calculator: no
slip: SK2F2A | took a quarter turn | A full turn is 360°, and half of it is $360 ÷ 2$.
```

## Your hand as a ruler

Hold your arm out straight and look past your hand at the sky. NASA's skywatching answers give three marks: your
little finger is about 1 degree wide, your three middle fingers together about 5 degrees, and your fist about 10
degrees (the Chandra X-ray Observatory's guide gives the same finger and fist). Keep your arm straight every time,
or the marks change.

From the horizon straight up to the point overhead is a right angle, 90 degrees. A fist is 10 degrees, so that is
$90 ÷ 10 = 9$ fists, one on top of the other.

A star sits two fists and three little fingers above the horizon. The two fists are $2 × 10 = 20$ degrees, and the
three little fingers a degree each, so the star is about $20 + 3 = 23$ degrees up.

## Checking the hand on the stars

A hand is a rough ruler, and the stars can check it. The two stars at the end of the Big Dipper's bowl, Dubhe and
Merak, are called the Pointers. Below, the two stars are drawn from their places in the Yale Bright Star
Catalogue, with three middle fingers laid from Dubhe toward Merak at the same scale. The drawing has north at the
top. In the sky the Big Dipper circles round the North Star through the night, so the Pointers lean a different way
as the hours go by, but the gap between them stays the same. Read the separation, and how many hands the gap
spans, under the drawing. Then switch to a little finger or a fist to compare, and come back to three middle
fingers.

```widget W01 hand-ruler
from: 4301
to: 4295
hand: three
epoch: J2000
shows: sep | 5.37°
shows: spans | 1.1
shows: off | +0.37°
```

The readout gives the Pointers <disp v="W01" kind="widget" k="sep">5.37°</disp> apart, and the gap is
<disp v="W01" kind="widget" k="spans">1.1</disp> three-finger widths, a little more than one. How far off is the
hand? $5.37 − 5 = 0.37$ degrees, less than half a little finger. The readout's
<disp v="W01" kind="widget" k="off">+0.37°</disp> is the same figure: the gap is that much wider than the hand.
Good enough to find your way, and a reason astronomers use instruments when they need more.

## Exercises

1. Castor and Pollux, the two bright stars of Gemini, are 4.5 degrees apart. By how many degrees is that less
   than three middle fingers?
2. A star is four fists and two little fingers above the horizon. About how many degrees up is it?

## Answers

1. Three middle fingers are 5 degrees, and 5 is more than 4.5: $5 − 4.5 = 0.5$, half a degree, half a little
   finger.
2. Four fists are $4 × 10 = 40$ degrees, and two little fingers more make $40 + 2 = 42$: about 42 degrees up.

## Mixed review

```item SK2M1
prompt: Two stars are three fists apart, with your arm held straight. About how many degrees apart are they?
topics: hand-ruler
answer: type
calculator: no
slip: SK2M1A | counted fingers, not fists | A fist is about 10 degrees: $3 × 10$.
```

```item SK2M2
prompt: How many degrees is a full turn?
topics: degrees
answer: type
calculator: no
slip: SK2M2A | took half a turn | Half a turn is 180°; all the way round is twice that.
```

```item SK2M3
prompt: The Pointers are 5.37 degrees apart, and your three middle fingers cover 5. By how many degrees is your hand short?
topics: sky-separation
answer: type
calculator: no
slip: SK2M3A | added instead | Short by the difference: $5.37 − 5$.
```

```item SK2M4
prompt: Work out $360 ÷ 10$. (That many fists go all the way round the horizon.)
topics: long-division
answer: type
calculator: no
slip: SK2M4A | divided by 100, not 10 | $360 ÷ 10$ takes off one zero: 36, not 3.6.
```
