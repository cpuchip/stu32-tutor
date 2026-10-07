---
id: exp-01
title: Growth and decay
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Growth and decay

A linear function (unit 4) adds the same amount at every step. An exponential function multiplies
by the same factor at every step. After n steps from a starting amount a, with a factor b each
step, the amount is

a × bⁿ.

A factor above 1 makes growth, and a factor between 0 and 1 makes decay. lin-03's doubling data was
exponential, with a factor of 2, which is why a line described it so badly. This lesson works with
exponential growth and decay, using yˣ from num-03.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Every example starts fresh, except where one says it
carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Growth

Growth of 4% a year means each year's amount is the last year's plus 4% of it: 1.04 times it. So the
factor is 1 + 0.04 = 1.04. Start with 500 and grow 4% a year for 10 years: 500 × 1.04¹⁰. yˣ raises
Y to the power in X. Type 500, ENTER, 1.04, ENTER, 10: the 500 waits in Z. yˣ uses Y and X and the
stack drops, bringing the 500 down to Y, so a last × multiplies by it:

```keys G01
500 ENTER 1.04 ENTER 10 yˣ ×
```

X shows <disp v="G01">740.1221</disp>. Compare adding a fixed 4% of the first 500, that is 20, every
year:

```keys G02
500 ENTER 20 ENTER 10 × +
```

X shows <disp v="G02">700.0000</disp>. The exponential is ahead, because each year's 4% is taken
from a bigger amount than the year before, so each year's increase is bigger than the last. The
fixed 20 never grows. That is why exponential growth is fast in the end, however slow it starts.

## Decay

Decay works the same way with a factor below 1. Losing r% each step leaves 100 − r of every 100, so
the factor is 1 − r ÷ 100: losing 15% is a factor of 0.85, and losing half is a factor of 0.5.

A medicine whose amount in the body halves every 6 hours has a factor of 0.5 for every 6 hours. The
time it takes to halve is called its half-life. Start with 80 mg. The amount does not drop in jumps
at each halving; it falls smoothly all the time, so a × bⁿ holds for part of a step too, with n a
fraction. After 15 hours, 15 ÷ 6 = 2.5 half-lives have passed, so 80 × 0.5^2.5 remain. A power of
2.5 is a power of 2 and a power of one half together: 0.5^2.5 = 0.5² × √0.5, as num-03's powers of
one half were square roots. yˣ takes any power. First the 2.5:

```keys D01A
80 ENTER 0.5 ENTER 15 ENTER 6 ÷
```

X shows <disp v="D01A">2.5000</disp>. Before ÷ the stack was full: 80 in T, 0.5 in Z, 15 in Y and 6
in X. ÷ dropped it, leaving 0.5 in Y and 80 in Z, with T copying its 80 down (rpn-01). One more
number typed before ÷ would have pushed the 80 off the top, so this is as many as the stack can
hold. Now yˣ, then ×:

```keys D01 after=D01A
yˣ ×
```

X shows <disp v="D01">14.1421</disp> mg. After 12 hours, two half-lives, there would be 20; after
18, three, 10. Fifteen hours is halfway between 12 and 18 in time, but 14.1421 is below 15, the
halfway amount: the drop is faster early in those six hours, 20 to 14.1421 in the first three and
14.1421 to 10 in the next three, because there is more to lose at the start.

## Finding the factor

If an amount went from 1200 to 1452 in two years, growing by the same factor b each year, then
1200 × b × b = 1452, so b × b = 1452 ÷ 1200 and b is its square root. Over n years it would be the
n-th root, ˣ√y from num-03 (gold above yˣ):

```keys R01
1452 ENTER 1200 ÷ 2 GOLD ˣ√y
```

X shows <disp v="R01">1.1000</disp>: a factor of 1.1, growth of 10% a year. The whole rise is 21%
(%CHG from num-04 would say so), and it would be wrong to halve it to 10.5% a year: the second year
grows from a bigger amount than the first, so 10% a year is enough, 1200 to 1320 to 1452.

## Exercises

1. 2000 is saved at 3% a year. How much is there after 25 years?
2. A car worth 18000 loses 15% of its value every year. What is it worth after 4 years?
3. A town grew from 8000 to 9261 people in 3 years, by the same factor each year. What was the
   yearly factor, and the yearly growth in percent?

## Answers

1. The factor is 1.03:

   ```keys E01
   2000 ENTER 1.03 ENTER 25 yˣ ×
   ```

   X shows <disp v="E01">4,187.5559</disp>: more than double.

2. Losing 15% leaves 85%, so the factor is 0.85:

   ```keys E02
   18000 ENTER 0.85 ENTER 4 yˣ ×
   ```

   X shows <disp v="E02">9,396.1125</disp>.

3. The factor is the cube root of 9261 ÷ 8000:

   ```keys E03
   9261 ENTER 8000 ÷ 3 GOLD ˣ√y
   ```

   X shows <disp v="E03">1.0500</disp>: 5% a year.
