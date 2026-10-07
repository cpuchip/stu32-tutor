---
id: num-02
title: Fractions
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# Fractions

Measurements and recipes come in fractions: 3/8 of an inch, 2/3 of a cup. The STU-32 lets you type
them as fractions and can show its answers as fractions. Underneath, every number is still a
decimal with 34 significant digits, and this lesson is about both sides of that.

## Before you start

The setup from rpn-01: 33s mode and FIX 4. Work the examples in order: several of them carry on
from the one before, and the text says when.

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

## Typing a fraction

While you are typing a number, a second press of the point key starts the bottom of a fraction.
Digits before the first point are the whole part, digits between the points are the top, and
digits after the second point are the bottom. So 3/8, with no whole part, is point, 3, point, 8:

```keys G01
.3.8 ENTER
```

X shows <disp v="G01">0.3750</disp>, the same number as a decimal. A mixed number has its whole part
in front: 2 3/8 is 2, point, 3, point, 8.

```keys G02
2.3.8 ENTER
```

X holds 2.375.

## Showing fractions

Fraction display is →FRAC, printed in blue above the point key. (The FRAC printed in blue above E is
a menu, and something else.) Press blue, then the point key:

```keys G03
2.3.8 ENTER BLUE →FRAC
```

X shows <disp v="G03">2 3/8</disp>. A fraction with no whole part shows a 0 in front, and a whole
number shows on its own, with no fraction after it.

Fraction display stays on until you press →FRAC again or choose another display setting. Press it
again now, and the display goes back to the setting it had before, here FIX 4:

```keys G07 after=G03
BLUE →FRAC
```

X shows <disp v="G07">2.3750</disp>.

## Adding and multiplying

Fractions work with the same keys as any other numbers. Measuring a board that is 5 3/8 inches
and another that is 2 7/16, with fraction display turned on for the answer:

```keys G05
5.3.8 ENTER 2.7.16 + BLUE →FRAC
```

X shows <disp v="G05">7 13/16</disp>. You never needed a common denominator: the calculator added
the two numbers and found the fraction afterwards.

Fraction display is still on. A recipe calls for 2/3 of a cup, and you are making 3/4 of the
recipe:

```keys G06 after=G05
.3.4 ENTER .2.3 ×
```

X shows <disp v="G06">0 1/2</disp>: half a cup. The 2/3 you typed was stored to 34 digits, a hair
above two thirds, but three quarters of that hair is too small to survive the rounding, so the
answer is exactly 1/2.

## When the answer is not exact

Fraction display shows the closest fraction whose bottom number is at most 4095, the calculator's
limit unless you change it. When the answer is not exactly that fraction, a small arrow in the
status band says so. The status band is the line at the top of the screen; it also shows the mode,
33. With fraction display still on, add 1/2 and 1/3:

```keys G04 after=G06
.1.2 ENTER .1.3 +
```

X shows <disp v="G04">0 5/6</disp>, and the status band shows <disp v="G04" kind="status">▼</disp>.
The 1/3 was stored as 0.3333... to 34 digits, a hair less than a third, so the sum is a hair less
than 5/6. The ▼ says the number is below the fraction shown; a ▲ would say it is above. Either way
the difference is in the 34th digit, far too small to matter in a measurement.

Turn fraction display off again before the exercises:

```keys G08 after=G04
BLUE →FRAC
```

X shows <disp v="G08">0.8333</disp>.

## Exercises

1. Work out 2/3 + 1/6 as a fraction. Which arrow does the status band show, and what does it mean?
2. Leaving fraction display on, work out 1 1/2 × 2 2/3.

## Answers

1. The keys:

   ```keys E01
   .2.3 ENTER .1.6 + BLUE →FRAC
   ```

   X shows <disp v="E01">0 5/6</disp>, and the status band shows <disp v="E01" kind="status">▲</disp>.
   This time both parts were stored a hair above their true values, so the sum is a hair above
   5/6: the same fraction as before, with the other arrow.

2. With fraction display still on from exercise 1:

   ```keys E02 after=E01
   1.1.2 ENTER 2.2.3 ×
   ```

   X shows <disp v="E02">4</disp>, with no arrow. The stored 2 2/3 is a hair above its true value,
   but times 1 1/2 the extra is too small to survive the rounding to 34 digits, so the product is
   exactly 4.
