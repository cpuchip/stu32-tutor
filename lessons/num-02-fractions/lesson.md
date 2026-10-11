---
id: num-02
title: Fractions
requires: setup shift-keys rpn-arithmetic display-rounds
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Fractions

Measurements and recipes come in fractions: $\frac{3}{8}$ of an inch, $\frac{2}{3}$ of a cup. The STU-32 lets you type
them as fractions and can show its answers as fractions. Underneath, every number is still a
decimal with 34 significant digits, and that decimal decides which fraction you see.

## Before you start

Work the examples in order: several of them carry on
from the one before, and the text says when.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Typing a fraction

While you are typing a number, a second press of the point key starts the bottom of a fraction.
Digits before the first point are the whole part, digits between the points are the top, and
digits after the second point are the bottom. So $\frac{3}{8}$, with no whole part, is point, 3, point, 8:

```keys G01
.3.8 ENTER
```

X shows <disp v="G01">0.3750</disp>, the same number as a decimal. A mixed number has its whole part
in front: $2 \frac{3}{8}$ is 2, point, 3, point, 8.

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

X shows <disp v="G07">2.3750</disp>. Choosing a setting from the DISP menu turns fraction display
off as well. Turn it on again, then choose FIX 4:

```keys G09 after=G07
BLUE →FRAC GOLD DISP FIX 4
```

X shows <disp v="G09">2.3750</disp>, a decimal again.

## Adding and multiplying

Fractions work with the same keys as any other numbers. Measuring a board that is $5 \frac{3}{8}$ inches
and another that is $2 \frac{7}{16}$, with fraction display turned on for the answer:

```keys G05
5.3.8 ENTER 2.7.16 + BLUE →FRAC
```

X shows <disp v="G05">7 13/16</disp>. You never needed a common denominator: the calculator added
the two numbers and found the fraction afterwards.

```why
ask: Why is the answer in sixteenths, when one board was measured in eighths?
because: An eighth is two sixteenths, so the exact sum is a number of sixteenths. Its top, 13, is odd, so it cannot be halved back into eighths.
```

```item G5T1
prompt: Add $3 \frac{3}{4} + 1 \frac{5}{8}$ by hand. Written as a mixed number in eighths, what is the top of its fraction part?
twin: G05
topics: fraction-arithmetic
answer: type
calculator: no
slip: G5T1A | the whole not carried | $\frac{6}{8} + \frac{5}{8} = \frac{11}{8}$, which is more than 1: carry the 1 whole, leaving $\frac{3}{8}$.
slip: G5T1B | the tops added as they are | Quarters and eighths are different sizes: $\frac{3}{4}$ is $\frac{6}{8}$ before the tops add.
```

Fraction display is still on. A recipe calls for $\frac{2}{3}$ of a cup, and you are making $\frac{3}{4}$ of the
recipe:

```keys G06 after=G05
.3.4 ENTER .2.3 ×
```

X shows <disp v="G06">0 1/2</disp>: half a cup. The $\frac{2}{3}$ you typed was stored to 34 digits, a hair
above two thirds, but three quarters of that hair is too small to survive the rounding, so the
answer is exactly $\frac{1}{2}$.

```why
ask: Why is $\frac{3}{4}$ of $\frac{2}{3}$ exactly a half?
because: Multiply the tops and the bottoms: the three on top of one fraction cancels the three below in the other. That leaves two quarters, and two quarters is a half.
```

## When the answer is not exact

Fraction display shows the closest fraction whose bottom number is at most 4095, the calculator's
limit unless you change it. When the answer is not exactly that fraction, a small arrow in the
status band says so. The status band is the line at the top of the screen. With fraction display
still on, add $\frac{1}{2}$ and $\frac{1}{3}$:

```keys G04 after=G06
.1.2 ENTER .1.3 +
```

X shows <disp v="G04">0 5/6</disp>, and the status band shows <disp v="G04" kind="status">▼</disp>.
The $\frac{1}{3}$ was stored as 0.3333... to 34 digits, a hair less than a third, so the sum is a hair less
than $\frac{5}{6}$. The ▼ says the number is below the fraction shown; a ▲ would say it is above. Either way
the difference is in the 34th digit, far too small to matter in a measurement.

Turn fraction display off again before the exercises:

```keys G08 after=G04
BLUE →FRAC
```

X shows <disp v="G08">0.8333</disp>, five sixths as a decimal.

## Exercises

1. Work out $\frac{2}{3} + \frac{1}{6}$ as a fraction. Which arrow does the status band show, and what does it mean?
2. Leaving fraction display on, work out $1 \frac{1}{2} × 2 \frac{2}{3}$.

## Answers

1. Two thirds plus one sixth, then →FRAC:

   ```keys E01
   .2.3 ENTER .1.6 + BLUE →FRAC
   ```

   X shows <disp v="E01">0 5/6</disp>, and the status band shows <disp v="E01" kind="status">▲</disp>.
   This time both parts were stored a hair above their true values, so the sum is a hair above
   $\frac{5}{6}$: the same fraction as before, with the other arrow.

2. With fraction display still on from exercise 1:

   ```keys E02 after=E01
   1.1.2 ENTER 2.2.3 ×
   ```

   X shows <disp v="E02">4</disp>, with no arrow. The stored $2 \frac{2}{3}$ is a hair above its true value,
   and times $1 \frac{1}{2}$ the product lands exactly halfway between two 34-digit numbers. The calculator
   rounds a tie like that to the one ending in an even digit, which here is exactly 4.
