---
id: num-04
title: Percent and powers of ten
requires: setup shift-keys rpn-arithmetic stack-lift stack-levels change-sign fix read-e type-e fix-overflow
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 2
display: FIX 2
---

# Percent and powers of ten

Two kinds of number come up often: percents, in prices and changes, and very large or very small
numbers, written with powers of ten. This lesson finishes the unit on numbers with both.

## Before you start

The percents here are prices, so set two decimal places: the mode you chose and FIX 2. Work the examples in
order; when one carries on from the example before it, the text says so.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 2
```

The two percent keys are on the 1/x key, fifth in the top row: % in gold above it, %CHG in blue.

## A percent of a number

Percent means "per hundred", so 15% of 80 is 15/100 × 80. The % key works it from the stack: X
percent of Y. Type the number first, then the percent:

```keys C01
80 ENTER 15 GOLD %
```

X holds 12, and Y still holds the 80. That is different from + and ×, which use up Y and drop the
stack: % leaves Y where it was, and Z and T too. Here it is with two more numbers above:

```keys C00
1 ENTER 2 ENTER 80 ENTER 15 GOLD %
```

X holds 12, Y 80, Z 2 and T 1. Keeping the 80 makes the next step one key. To add 15% to 80, carry
on and press +:

```keys C02 after=C00
+
```

X shows <disp v="C02">92.00</disp>, and the stack has dropped, bringing the 2 down to Y. For a discount, subtract instead. Twenty-five percent off 60:

```keys C03
60 ENTER 25 GOLD % −
```

X holds 45.

## Percent change

The %CHG key works how much Y changed to become X, as a percent of Y: (X − Y) ÷ Y × 100. A price
that went from 50 to 65 changed by (65 − 50) ÷ 50 × 100:

```keys C04
50 ENTER 65 BLUE %CHG
```

X shows <disp v="C04">30.00</disp>: it went up 30%. Like %, %CHG leaves the 50 in Y. A fall gives a
negative change. From 80 down to 60:

```keys C05
80 ENTER 60 BLUE %CHG
```

X shows <disp v="C05">-25.00</disp>: down 25%. The starting value goes in first: it is the number
the change is measured from.

## Negative powers of ten

rpn-03 showed how E types a power of ten. For a negative power, press +/− after E, while you are
typing the power. So 4 × 10⁻³, which is 0.004, is 4, E, 3, +/−:

```keys C06
4 E 3 +/− ENTER
```

X shows <disp v="C06">4.00E-3</disp>. The number 0.004 has no digit but zero in its first two
places, so at FIX 2 the calculator switches to scientific form on its own, as rpn-03 showed for
FIX 4.

Where you press +/− matters. Pressed before E, it changes the sign of the front number instead:

```keys C06B
4 +/− E 3 ENTER
```

X shows <disp v="C06B">-4,000.00</disp>, which is −4 × 10³.

## Calculating with powers of ten

Numbers typed with E work like any others. To check an answer in your head, multiply the front
numbers and add the powers. Six hundred thousand times four thousandths is 6 × 10⁵ times 4 × 10⁻³;
6 × 4 is 24, and 5 + (−3) is 2, so the answer is 24 × 10², or 2,400:

```keys C07
6 E 5 ENTER 4 E 3 +/− ×
```

X shows <disp v="C07">2,400.00</disp>. For division, divide the front numbers and subtract the
powers. A tiny number divided by a bigger one, 9 × 10⁻⁶ divided by 3 × 10²: 9 ÷ 3 is 3, and −6 − 2
is −8:

```keys C09
9 E 6 +/− ENTER 3 E 2 ÷
```

X shows <disp v="C09">3.00E-8</disp>, which is 3 × 10⁻⁸. A very large answer switches to scientific
form the same way. Two large numbers, 3.2 × 10¹² and 2.5 × 10⁹; 3.2 × 2.5 is 8, and 12 + 9 is 21:

```keys C08
3.2 E 12 ENTER 2.5 E 9 ×
```

X shows <disp v="C08">8.00E21</disp>, which is 8 × 10²¹. Written out at FIX 2 it would need more
than 30 characters, too long to fit the line, so the calculator shows it in scientific form.

## Exercises

1. Work out 12% of 250.
2. A price went from 40 to 46. By what percent did it change?
3. Work out 2.5 × 10⁶ times 4 × 10⁻², and check it in your head.
4. An item costs 60 and is 20% off. What does it cost?
5. A price falls from 80 to 60, a 25% fall, then rises from 60 back to 80. By what percent did it
   rise?

## Answers

1. The 250 first, then the percent:

   ```keys E01
   250 ENTER 12 GOLD %
   ```

   X shows <disp v="E01">30.00</disp>.

2. Up 15%. The starting price first:

   ```keys E02
   40 ENTER 46 BLUE %CHG
   ```

   X shows <disp v="E02">15.00</disp>.

3. In your head: 2.5 × 4 is 10, and 6 + (−2) is 4, so the answer is 10 × 10⁴, which is 10⁵:

   ```keys E03
   2.5 E 6 ENTER 4 E 2 +/− ×
   ```

   X shows <disp v="E03">100,000.00</disp>.

4. The discount, then subtract it:

   ```keys E04
   60 ENTER 20 GOLD % −
   ```

   X shows <disp v="E04">48.00</disp>.

5. The starting price is now 60:

   ```keys E05
   60 ENTER 80 BLUE %CHG
   ```

   X shows <disp v="E05">33.33</disp>: a rise of about 33%, where the fall was 25%. The same 20 is
   a bigger part of 60 than of 80, so going back up takes a bigger percent than coming down.
