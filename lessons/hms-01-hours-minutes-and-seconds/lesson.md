---
id: hms-01
title: Hours, minutes and seconds
requires: calc-setup|setup calc-first-calculation|rpn-arithmetic fraction-is-division|fraction-bar degrees|full-turn
entries: alg rpn
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
---

# Hours, minutes and seconds

Vega, one of the brightest stars in the northern summer sky, has its place in a star catalog written as 18h 36m 56.3s and
+38° 47′ 01″. The first is a time: 18 hours, 36 minutes and 56.3 seconds. The second is an angle: 38 degrees, 47
arcminutes and 1 arcsecond. Both count in sixties, the way a clock does, and neither is a number the calculator can
add or multiply as it stands. How many hours is 18h 36m 56.3s, as one number?

## From before

```item HM1F1
prompt: What part of an hour is 15 minutes? Give it as a decimal.
topics: fraction-is-division fraction-bar
answer: type
calculator: no
slip: HM1F1A | counted the minutes as hundredths | An hour is 60 minutes, not 100: $15 ÷ 60$.
```

```item HM1F2
prompt: How many degrees is a quarter of a full turn?
topics: degrees full-turn
answer: type
calculator: no
slip: HM1F2A | took half a turn | A full turn is 360°: a quarter of it is $360 ÷ 4$.
```

## Before you start

The setup turns the calculator on in your mode and shows four places after the point.
<entry e="alg">In the algebraic entry the keys below type a function first, then its number, then ▶ to close the
bracket and ENTER, which works as = here.</entry><entry e="rpn">In RPN the number goes first, then the function.</entry>

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Sixty, not ten

An hour has 60 minutes, and a minute has 60 seconds, so an hour has $60 × 60 = 3600$ seconds. Half an hour is 30
minutes, so 1 hour 30 minutes is 1.5 hours, not 1.30: the digits after a decimal point count tenths and hundredths,
and minutes count sixtieths. To turn minutes into part of an hour, divide by 60; seconds, divide by 3600. So 2
hours, 30 minutes and 45 seconds is $2 + 30 ÷ 60 + 45 ÷ 3600 = 2 + 0.5 + 0.0125 = 2.5125$ hours.

## Into hours

The calculator holds hours, minutes and seconds in one number: the hours, a point, two digits of minutes, then the
seconds. So 2 hours, 30 minutes and 45 seconds is typed 2.3045. HMS→, in the ANGLE menu (blue above SIN), turns that
into hours:

```keys H01 entry=alg
BLUE ANGLE HMS→ 2.3045 ▶ ENTER
```

```keys H01
2.3045 BLUE ANGLE HMS→
```

The screen shows <disp v="H01">2.5125</disp>, the hours worked out by hand above.

```why
ask: Why does HMS→ turn 2.3045 into 2.5125?
because: In 2.3045 the 30 minutes and 45 seconds count sixtieths, not tenths and hundredths; HMS→ turns them into a part of an hour, and 2.5125 is the whole time in hours.
```

Now Vega's 18h 36m 56.3s. The seconds have a tenth, so it is typed 18.36563:

```keys H02 entry=alg
BLUE ANGLE HMS→ 18.36563 ▶ ENTER
```

```keys H02
18.36563 BLUE ANGLE HMS→
```

The screen shows <disp v="H02">18.6156</disp>: Vega's place is about 18.6 hours around the sky.

## Back to hours and minutes

→HMS, beside HMS→ in the same menu, goes the other way: from hours to hours, minutes and seconds.

```keys H03 entry=alg
BLUE ANGLE →HMS 1.5 ▶ ENTER
```

```keys H03
1.5 BLUE ANGLE →HMS
```

The screen shows <disp v="H03">1.3000</disp>: 1 hour, 30 minutes and 0 seconds.

Measured against the stars, the Earth turns once in 86164.0989 seconds: the US Naval Observatory's Circular 179
gives it as the Earth's rotation period. (The sidereal day, timed from the equinox instead of from a star, is
shorter by about 0.008 seconds, the same Circular says.) Divide by 3600 for hours, and →HMS shows how long a turn
takes:

```keys H04 entry=alg
BLUE ANGLE →HMS 86164.0989 ÷ 3600 ▶ ENTER
```

```keys H04
86164.0989 ENTER 3600 ÷ BLUE ANGLE →HMS
```

The screen shows <disp v="H04">23.5604</disp>: 23 hours, 56 minutes and 4 seconds, about 4 minutes short of a day.
That is why a star rises about 4 minutes earlier each night.

## Degrees, arcminutes and arcseconds

Angles on the sky are counted the same way. A degree has 60 arcminutes, written ′, and an arcminute has 60
arcseconds, written ″. The same two keys work on angles: type degrees, a point, two digits of arcminutes, then the
arcseconds. Vega's +38° 47′ 01″ is typed 38.4701:

```keys H05 entry=alg
BLUE ANGLE HMS→ 38.4701 ▶ ENTER
```

```keys H05
38.4701 BLUE ANGLE HMS→
```

The screen shows <disp v="H05">38.7836</disp>: the catalog's 38° 47′ 01″, the same angle in degrees.

## Exercises

1. Turn 3 hours 45 minutes into hours.
2. Write 2.75 hours in hours and minutes.
3. The best measurements before telescopes were good to about an arcminute. What is 1 arcminute in degrees?

## Answers

1. 45 minutes is $45 ÷ 60 = 0.75$ of an hour, so 3.75 hours. On the calculator it is typed 3.45:

   ```keys E01 entry=alg
   BLUE ANGLE HMS→ 3.45 ▶ ENTER
   ```

   ```keys E01
   3.45 BLUE ANGLE HMS→
   ```

   The screen shows <disp v="E01">3.7500</disp>.

2. 0.75 of an hour is $0.75 × 60 = 45$ minutes, so 2 hours 45 minutes:

   ```keys E02 entry=alg
   BLUE ANGLE →HMS 2.75 ▶ ENTER
   ```

   ```keys E02
   2.75 BLUE ANGLE →HMS
   ```

   The screen shows <disp v="E02">2.4500</disp>.

3. $1 ÷ 60$ of a degree. 0 degrees and 1 arcminute is typed 0.01:

   ```keys E03 entry=alg
   BLUE ANGLE HMS→ 0.01 ▶ ENTER
   ```

   ```keys E03
   0.01 BLUE ANGLE HMS→
   ```

   The screen shows <disp v="E03">0.0167</disp> degrees.

## Mixed review

```item HM1M1
prompt: How many minutes are in 2.5 hours?
topics: sexagesimal
answer: type
calculator: no
slip: HM1M1A | read .5 as 50 minutes | 0.5 of an hour is half of 60 minutes: $2.5 × 60$.
```

```item HM1M2
prompt: How many degrees is a third of a full turn?
topics: degrees full-turn
answer: type
calculator: no
slip: HM1M2A | a third of half a turn | A full turn is 360°, not 180°: $360 ÷ 3$.
```

```item HM1M3
prompt: Write 1.75 hours in hours and minutes. How many minutes past the hour is it?
topics: hours-to-hms
answer: type
calculator: no
slip: HM1M3A | read the decimal as minutes | 0.75 of an hour is $0.75 × 60$ minutes.
```

```item HM1M4
prompt: What part of an hour is 12 minutes? Give it as a decimal.
topics: fraction-is-division fraction-bar
answer: type
calculator: no
slip: HM1M4A | counted the minutes as hundredths | An hour is 60 minutes: $12 ÷ 60$.
```
