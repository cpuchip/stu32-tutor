---
id: sky-02
title: Angles with your hand
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation degrees angle-kinds partial-products long-division
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
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

## Before you start

The setup turns the calculator on and shows four places after the point.
<entry e="alg">Type each calculation the way it is written, then press ENTER, which works as = here.</entry><entry e="rpn">In
RPN, type the first number, ENTER, the second, then the operation.</entry>

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Your hand as a ruler

Hold your arm out straight and look past your hand at the sky. NASA's skywatching answers give three marks: your
little finger is about 1 degree wide, your three middle fingers together about 5 degrees, and your fist about 10
degrees (the Chandra X-ray Observatory's guide gives the same finger and fist). Keep your arm straight every time,
or the marks change.

From the horizon straight up to the point overhead is a right angle, 90 degrees. How many fists is that?

```keys H01 entry=alg
90 ÷ 10 ENTER
```

```keys H01 entry=rpn
90 ENTER 10 ÷
```

The screen shows <disp v="H01">9.0000</disp>: nine fists, one on top of the other, from the horizon to overhead.

A star sits two fists and three little fingers above the horizon. The two fists first:

```keys H02 entry=alg
2 × 10 ENTER
```

```keys H02 entry=rpn
2 ENTER 10 ×
```

The screen shows <disp v="H02">20.0000</disp>. Then the three little fingers, a degree each:

```keys H03 entry=alg
20 + 3 ENTER
```

```keys H03 entry=rpn
20 ENTER 3 +
```

The screen shows <disp v="H03">23.0000</disp>: the star is about 23 degrees up.

## Checking the hand on the stars

A hand is a rough ruler, and the stars can check it. The two stars at the end of the Big Dipper's bowl, Dubhe and
Merak, are called the Pointers. By the positions in the Yale Bright Star Catalogue they are 5.37 degrees apart.
Three middle fingers should just cover the gap. How far off is the hand?

```keys S01 entry=alg
5.37 − 5 ENTER
```

```keys S01 entry=rpn
5.37 ENTER 5 −
```

The screen shows <disp v="S01">0.3700</disp>: less than half a little finger. Good enough to find your way, and a
reason astronomers use instruments when they need more.

## Exercises

1. Castor and Pollux, the two bright stars of Gemini, are 4.5 degrees apart. How far is that from three middle
   fingers?
2. A star is four fists and two little fingers above the horizon. About how many degrees up is it?

## Answers

1. Three middle fingers are 5 degrees, and 5 is more than 4.5:

   ```keys E01 entry=alg
   5 − 4.5 ENTER
   ```

   ```keys E01 entry=rpn
   5 ENTER 4.5 −
   ```

   The screen shows <disp v="E01">0.5000</disp>: half a degree, half a little finger.

2. Four fists first:

   ```keys E02 entry=alg
   4 × 10 ENTER
   ```

   ```keys E02 entry=rpn
   4 ENTER 10 ×
   ```

   The screen shows <disp v="E02">40.0000</disp>, and two little fingers more:

   ```keys E02B entry=alg
   40 + 2 ENTER
   ```

   ```keys E02B entry=rpn
   40 ENTER 2 +
   ```

   The screen shows <disp v="E02B">42.0000</disp>: about 42 degrees up.

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
slip: SK2M4A | took off a zero too many | $360 ÷ 10$ takes off one zero: 36, not 3.6.
```
