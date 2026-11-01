---
id: par-01
title: Parallax: a distance from an angle
requires: setup shift-keys enter-copies reciprocal type-e angle-unit trig-ratios dms
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
display: FIX 4
---

# Parallax: a distance from an angle

Hold a finger up at arm's length and look at it with one eye, then the other. The finger jumps against the wall
behind it, and the nearer the finger, the bigger the jump. The Earth does the same thing to the stars. In six
months it moves to the other side of its orbit around the Sun, and a near star shifts a little against the far
ones behind it. In 1838 Friedrich Bessel measured that shift for the star 61 Cygni. He took its parallax, half the
yearly shift, as 0.3136 arcseconds, and from it he found the star to be 657,700 times as far from the Sun as the Earth is, so far that light
takes 10.3 years to cross the distance (his report, as Shapley and Howarth's Source Book in Astronomy of 1929 prints
it). How does an angle that small give a distance?

## From before

```item PX1F1
prompt: A right triangle has sides 3 and 4 around its right angle, and its longest side is 5. The side opposite one angle is 3, and the side next to it is 4. What is that angle's tangent?
topics: trig-ratios
answer: type
calculator: no
slip: PX1F1A | used the longest side | The tangent is opposite over next to: $3 ÷ 4$. Opposite over the longest side is the sine.
```

```item PX1F2
prompt: How many arcseconds are there in one degree?
topics: dms
answer: type
calculator: no
slip: PX1F2A | counted the arcminutes only | A degree is 60 arcminutes, and each of those is 60 arcseconds: $60 × 60$.
```

## Before you start

The setup turns the calculator on in your mode, shows four places after the point, and sets the angle unit to
degrees (∡MODE, from trig-01), since the angles below are turned into degrees before TAN.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
```

## The triangle

Draw the Sun, the Earth, and the star far off to one side. From one side of the Earth's orbit to the other is 2
astronomical units (AU), twice the Earth's distance from the Sun. Half of the six-month shift, the angle p, belongs
to half of that: 1 AU. So the Sun, the Earth and the star make a right triangle at the Sun, with 1 AU opposite the
angle p at the star and the star's distance d next to it. The tangent is opposite over next to, so $\tan p = 1 ÷ d$,
and $d = 1 ÷ \tan p$, counted in AU.

Bessel's angle is 0.3136 arcseconds. An arcsecond is $1 ÷ 3600$ of a degree (hms-01), so divide by 3600 for degrees,
press TAN and then 1/x:

```keys P01
0.3136 ENTER 3600 ÷ TAN 1/x
```

The X line shows <disp v="P01">657,732.1628</disp> AU, which Bessel gave as 657,700.

```why
ask: Why divide by 3600 before pressing TAN?
because: TAN takes the angle in the angle unit, degrees here, and 0.3136 is in arcseconds; an arcsecond is a 3600th of a degree.
```

## The parsec

An angle of exactly 1 arcsecond gives a distance worth a name of its own:

```keys P02
1 ENTER 3600 ÷ TAN 1/x
```

The X line shows <disp v="P02">206,264.8062</disp> AU. That distance is a parsec, from parallax and arcsecond, and
the International Astronomical Union's education glossary gives it as 206,264.8 AU. For angles this small the
tangent grows in step with the angle: half the angle, twice the distance. So the distance in parsecs is just $1 ÷ p$,
with p in arcseconds and p half the six-month shift. For Bessel's star:

```keys P03
0.3136 1/x
```

The X line shows <disp v="P03">3.1888</disp> parsecs. That many parsecs of 206,264.8 AU each make Bessel's
657,700 AU again.

## Parsecs and light-years

A light-year is the distance light travels in a year. The year is the Julian year, 365.25 days of 86,400 seconds
(the basis NIST's Guide for the Use of the International System of Units, 2008, gives for the light-year), and light
travels 299,792.458 kilometers a second, the speed the SI fixes exactly. The glossary rounds the light-year to 9.46
trillion kilometers. The astronomical unit is 149,597,870,700 meters exactly (the International Astronomical Union,
2012), which is 149,597,870.7 kilometers. So a parsec in kilometers, divided by a light-year in kilometers, is a
parsec in light-years:

```keys P04
206264.8 ENTER 149597870.7 × 299792.458 ENTER 86400 × 365.25 × ÷
```

The X line shows <disp v="P04">3.2616</disp>: a parsec is about 3.26 light-years, as the glossary says. Carrying on,
Bessel's star in light-years is its parsecs times that, with the 3.2616 still in X:

```keys P05 after=P04
0.3136 1/x ×
```

The X line shows <disp v="P05">10.4004</disp> light-years. Bessel wrote 10.3.

## How sure?

A measurement comes with its uncertainty, and so does the distance worked out from it. The Hipparcos Catalogue
(1997) gives Alpha Centauri A a parallax of 742.12 ± 1.40 milliarcseconds: thousandths of an arcsecond, so 0.74212
± 0.00140 arcseconds. The distance first:

```keys U01
0.74212 1/x
```

The X line shows <disp v="U01">1.3475</disp> parsecs. The parallax could be as large as
$0.74212 + 0.00140 = 0.74352$:

```keys U02
0.74352 1/x
```

The X line shows <disp v="U02">1.3450</disp>. Or as small as $0.74212 − 0.00140 = 0.74072$:

```keys U03
0.74072 1/x
```

The X line shows <disp v="U03">1.3500</disp>. So the star is between 1.345 and 1.350 parsecs away.

```why
ask: Why does the smallest parallax in the range give the largest distance?
because: The distance is one divided by p, and one divided by a smaller number is larger: 0.74072 gives 1.3500.
```

## Exercises

1. The Hipparcos Catalogue gives Sirius a parallax of 379.21 ± 1.58 milliarcseconds. How far away is Sirius in
   parsecs, and between what distances does the uncertainty put it?
2. How many light-years away is Alpha Centauri A? Use 1.3475 parsecs and 3.2616 light-years to a parsec.

## Answers

1. 379.21 milliarcseconds is 0.37921 arcseconds:

   ```keys E01
   0.37921 1/x
   ```

   The X line shows <disp v="E01">2.6371</disp> parsecs. The ends of the range are $0.37921 + 0.00158 = 0.38079$
   and $0.37921 − 0.00158 = 0.37763$:

   ```keys E01B
   0.38079 1/x
   ```

   The X line shows <disp v="E01B">2.6261</disp>, and for the other end:

   ```keys E01C
   0.37763 1/x
   ```

   The X line shows <disp v="E01C">2.6481</disp>. Sirius is between 2.626 and 2.648 parsecs away.

2. Parsecs times light-years to a parsec:

   ```keys E02
   1.3475 ENTER 3.2616 ×
   ```

   The X line shows <disp v="E02">4.3950</disp>, about 4.4 light-years.

## Mixed review

```item PX1M1
prompt: A star's parallax is 0.5 arcseconds. How far away is it, in parsecs?
topics: parsec
answer: type
calculator: no
slip: PX1M1A | took the parallax as the distance | The distance is 1 ÷ p: $1 ÷ 0.5$.
```

```item PX1M2
prompt: In a right triangle, an angle's tangent is 0.5 and the side next to the angle is 10. How long is the side opposite it?
topics: trig-ratios
answer: type
calculator: no
slip: PX1M2A | divided by the tangent | Opposite is next to times the tangent: $10 × 0.5$.
```

```item PX1M3
prompt: A star is 10 parsecs away. Using 3.26 light-years to a parsec, how many light-years is that?
topics: light-year
answer: type
calculator: no
slip: PX1M3A | added the factor | Each parsec is 3.26 light-years, so multiply: $10 × 3.26$.
```

```item PX1M4
prompt: How many arcseconds is 0.01 of a degree?
topics: dms
answer: type
calculator: no
slip: PX1M4A | counted arcminutes | A degree is 3600 arcseconds: $0.01 × 3600$.
```
