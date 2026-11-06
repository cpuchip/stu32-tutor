---
id: hms-01
title: Hours, minutes and seconds
requires: calc-setup|setup calc-first-calculation|rpn-arithmetic fraction-is-division|fraction-bar degrees|full-turn
entries: alg rpn
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
calculator_reason: the section for a calculator without HMS→ does its work with + − × ÷, carrying every digit of 18.6156… from step to step
---

# Hours, minutes and seconds

Vega, one of the brightest stars in the northern summer sky, has its place in a star catalog written as 18h 36m 56.3s
and +38° 47′ 01″. The first is a time: 18 hours, 36 minutes and 56.3 seconds. The second is an angle: 38 degrees, 47
arcminutes (an arcminute is a sixtieth of a degree) and 1 arcsecond (a sixtieth of an arcminute). Both count in
sixties, the way a clock does, and neither is a number the calculator can add or multiply as it stands. How many hours
is 18h 36m 56.3s, as one number?

## From before

```item HM1F1
prompt: What part of an hour is 15 minutes? Give it as a decimal.
topics: fraction-is-division fraction-bar
answer: type
calculator: no
slip: HM1F1A | counted the minutes as hundredths | An hour is 60 minutes, not 100: $15 ÷ 60$.
```

```item HM1F2
prompt: How many degrees is a quarter of a full turn? (Type just the number.)
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

## Vega on the sky

The sphere below is the sky over New York, with the grid astronomers use to say where a star is. The lines from pole
to pole are right ascension, counted in hours around the sky; the circles are declination, counted in degrees north
or south of the sky's equator. Vega is marked. Turn the sphere, and follow its lines to where they cross.

```widget W01 sky-sphere
lat: 40.7
lst: 18.6
star: 7001
grids: radec
epoch: J2000
shows: ra | 18h 37m
shows: dec | +39°
```

The readout puts Vega at <disp v="W01" kind="widget" k="ra">18h 37m</disp> and
<disp v="W01" kind="widget" k="dec">+39°</disp>, which is as close as a grid can be read. The catalog's 18h 36m 56.3s
and +38° 47′ 01″ are the same place, measured with instruments and given to the nearest tenth of a second of time
and the nearest arcsecond. Both are on the lines of the year 2000, the catalog's own (J2000), which the grid draws
too.

## Sixty, not ten

An hour has 60 minutes, and a minute has 60 seconds, so an hour has $60 × 60 = 3600$ seconds. Half an hour is 30
minutes, so 1 hour 30 minutes is 1.5 hours, not 1.30: the digits after a decimal point count tenths and hundredths,
and minutes count sixtieths. To turn minutes into part of an hour, divide by 60; seconds, divide by 3600. So 2
hours, 30 minutes and 45 seconds is $2 + 30 ÷ 60 + 45 ÷ 3600 = 2 + 0.5 + 0.0125 = 2.5125$ hours.

## Into hours

The calculator holds hours, minutes and seconds in one number: the hours, a point, two digits of minutes, then two
digits of seconds and any tenths after them. So 2 hours, 30 minutes and 45 seconds is typed 2.3045. That number is a
code for HMS→ to read, not a time in hours: its 30 and 45 still count sixtieths. HMS→, in the ANGLE menu (blue above
SIN), turns that into hours:

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

The screen shows <disp v="H03">1.3000</disp>: the code for 1 hour, 30 minutes and 0 seconds, not 1.3 hours.

Measured against the stars, the Earth turns once in 86164.0989 seconds: the US Naval Observatory's Circular 179
gives it as the Earth's rotation period. Divide by 3600 for hours, and →HMS shows how long a turn
takes:

```keys H04 entry=alg
BLUE ANGLE →HMS 86164.0989 ÷ 3600 ▶ ENTER
```

```keys H04
86164.0989 ENTER 3600 ÷ BLUE ANGLE →HMS
```

The screen shows <disp v="H04">23.5604</disp>: 23 hours, 56 minutes and 4 seconds, about 4 minutes short of a day.
That is why a star rises about 4 minutes earlier each night.

## On a calculator without these keys

If your calculator has no HMS→ or →HMS, you can do the same work with + − × ÷, one sixty at a time. Seconds divided by
60 are minutes: 18h 36m 56.3s is 18 hours and 36 minutes, and $56.3 ÷ 60$ of a minute more. Minutes divided by 60 are
hours. So start from the seconds: divide by 60, add the minutes, divide by 60 again, and add the hours. The seconds
are divided by 60 twice, which is dividing by 3600, so this is the sum from "Sixty, not ten", worked from the seconds
out, and in this order it needs no brackets. <entry e="alg">On your calculator, press = wherever the keys below show
ENTER, after each step, and the answer is the same on a calculator that works from left to right and on one that does
× and ÷ before + and −. Each step after the first starts with a key, and carries on from the answer. If yours does not
carry on from the answer when a key follows =, type the answer back in first, with every digit your own screen shows,
not the four printed here.</entry><entry e="rpn">In RPN the steps go in the order they are said, each number before
its key.</entry> The screens below show four places after the point; yours may show more.

```keys M01 entry=alg
56.3 ÷ 60 ENTER + 36 ENTER ÷ 60 ENTER + 18 ENTER
```

```keys M01
56.3 ENTER 60 ÷ 36 + 60 ÷ 18 +
```

The screen shows <disp v="M01">18.6156</disp>, the hours HMS→ gave.

To go back, take away the whole hours and multiply what is left by 60. That gives the minutes:

```keys M02 entry=alg after=M01
− 18 ENTER × 60 ENTER
```

```keys M02 after=M01
18 − 60 ×
```

The screen shows <disp v="M02">36.9383</disp>: 36 whole minutes. Take them away and multiply by 60 again for the
seconds:

```keys M03 entry=alg after=M02
− 36 ENTER × 60 ENTER
```

```keys M03 after=M02
36 − 60 ×
```

The screen shows <disp v="M03">56.3000</disp>: 56.3 seconds, and the time is 18h 36m 56.3s again. A calculator that
keeps fewer digits may end a little either side of 56.3, the difference lost in its last digits.

## Degrees, arcminutes and arcseconds

Angles on the sky are counted the same way. A degree has 60 arcminutes, written ′, and an arcminute has 60 arcseconds,
written ″. The same two keys work on angles: type degrees, a point, two digits of arcminutes, then two digits of
arcseconds. Vega's +38° 47′ 01″ is typed 38.4701:

```keys H05 entry=alg
BLUE ANGLE HMS→ 38.4701 ▶ ENTER
```

```keys H05
38.4701 BLUE ANGLE HMS→
```

The screen shows <disp v="H05">38.7836</disp>: the catalog's 38° 47′ 01″, the same angle in degrees. The steps
for a calculator without these keys work on an angle too: divide the arcseconds by 60, add the arcminutes, divide
by 60 again, and add the degrees. For a negative angle, south of the sky's equator, work without the minus sign
and put it on the whole answer at the end, not on the degrees alone.

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
prompt: How many degrees is a third of a full turn? (Type just the number.)
topics: degrees full-turn
answer: type
calculator: no
slip: HM1M2A | a third of half a turn | A full turn is 360°, not 180°: $360 ÷ 3$.
```

```item HM1M3
prompt: 1.75 hours is 1 hour and how many minutes?
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
