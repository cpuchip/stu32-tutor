---
id: rpn-03
title: The display
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The display

The STU-32 keeps 34 significant digits of every number. The screen shows far fewer, and the
display setting decides which ones. This lesson is about that setting: what each kind shows, and
why changing it leaves the number underneath as it was.

## Before you start

The setup is the one from rpn-01: the mode you chose and FIX 4.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

The display settings live in the DISP menu (gold, then 2). Its soft keys are FIX, SCI, ENG and
ALL. FIX, SCI and ENG each take one digit next.

Changing the setting does not touch the stack. A number you type next behaves just as it would
have without the change: after ENTER, it still replaces the copy in X.

```keys P00
1 ENTER 2 ENTER GOLD DISP FIX 2 7
```

X shows <disp v="P00" kind="entry">7_</disp>, the 7 still being typed, with Y holding 2 and Z
holding 1: the same as 1 ENTER 2 ENTER 7 would leave them.

A display setting stays until you change it. Each example below is written out in full from the
setup, so if you have just changed the setting, an example that needs FIX 4 sets it again.

<!-- SHOW: unit 030 (abacus-firmware c904cb3) adds SHOW, to see all of X's digits when the format
hides them (abacus decision 46). How it is pressed and dismissed comes from the unit, not from
here. When it lands, a short section goes after "FIX: a fixed number of decimal places", on two
thirds. -->

## FIX: a fixed number of decimal places

Two divided by three never ends: 0.666... with sixes forever. The calculator keeps it to 34
digits, and FIX 4 shows four decimal places, rounded. Set FIX 4 again (the last example left FIX
2), then divide:

```keys P01
GOLD DISP FIX 4 2 ENTER 3 ÷
```

X shows <disp v="P01">0.6667</disp>. Here is the same number at FIX 2:

```keys P02
2 ENTER 3 ÷ GOLD DISP FIX 2
```

X shows <disp v="P02">0.67</disp>.

The display rounded; the number kept its 34 digits. Multiply it by 3:

```keys P03
2 ENTER 3 ÷ GOLD DISP FIX 2 3 ×
```

X shows <disp v="P03">2.00</disp>, and the number underneath is exactly 2. The stored two thirds
was rounded at its 34th digit, and three times it rounds back to 2. If the calculator had kept
only the 0.67 you could see, the answer would have been 2.01.

## Reading a power of ten

The next two settings write a number with E and a power of ten after it. E means "times ten to
the". A positive power moves the point that many places to the right: 4.5E9 is 4.5 with the point
moved nine places right, 4500000000. A negative power moves it to the left: 1.25E-5 is 0.0000125.

## SCI: scientific notation

SCI shows one digit before the point, then the number of places you chose, then E and the power.
With SCI 3, two thirds becomes:

```keys P04
2 ENTER 3 ÷ GOLD DISP SCI 3
```

X shows <disp v="P04">6.667E-1</disp>, which is 6.667 with the point moved one place left.

## ENG: engineering notation

ENG keeps the power of ten to a multiple of three (thousands, millions, thousandths), and moves
the point to suit. Its digit counts significant digits after the first one, so ENG 3 always shows
four significant digits, wherever the point lands. 23456 at ENG 3:

```keys P05
23456 GOLD DISP ENG 3
```

X shows <disp v="P05">23.46E3</disp>: 23.46 thousand, four significant digits with two of them
after the point.

## When FIX runs out of room

At FIX 4, a number like 0.0000125 has no digit but zero in its first four places. So for a number
that small the calculator switches to scientific form on its own, still with four places. One divided by
80000, with FIX 4 set again after the last example:

```keys P06
GOLD DISP FIX 4 1 ENTER 80000 ÷
```

X shows <disp v="P06">1.2500E-5</disp>: four places, now in scientific form.

## Typing a power of ten

The E key, in the ENTER row between +/− and ←, types the power of ten for you. To enter 4.5
billion, type 4.5, press E, and type 9. Shown at SCI 2:

```keys P07
4.5 E 9 GOLD DISP SCI 2
```

X shows <disp v="P07">4.50E9</disp>.

## ALL: no padding

ALL shows a number without padding it to a fixed number of places. One eighth is exactly 0.125:

```keys P08
1 ENTER 8 ÷ GOLD DISP ALL
```

X shows <disp v="P08">0.125</disp>. ALL is still limited by the width of the screen. A number that
never ends, like two thirds, fills the line with as many digits as fit:

```keys P08B
2 ENTER 3 ÷ GOLD DISP ALL
```

X shows <disp v="P08B">0.6666666666666666667</disp>, which is 19 of the 34 digits the
calculator keeps, the last one rounded.

## Exercises

1. Work out 22 divided by 7, shown at FIX 3.
2. Work out 7 divided by 9 and show it at FIX 2. Then multiply by 9. What does the display show,
   and why is it not 7.02?

## Answers

1. The keys:

   ```keys E01
   22 ENTER 7 ÷ GOLD DISP FIX 3
   ```

   X shows <disp v="E01">3.143</disp>.

2. Seven ninths at FIX 2:

   ```keys E02A
   7 ENTER 9 ÷ GOLD DISP FIX 2
   ```

   X shows <disp v="E02A">0.78</disp>. Then times 9 (the whole sequence again):

   ```keys E02
   7 ENTER 9 ÷ GOLD DISP FIX 2 9 ×
   ```

   X shows <disp v="E02">7.00</disp>. The calculator multiplied all 34 digits of seven ninths by 9,
   and the result rounds to exactly 7. Nine times the 0.78 you could see would have been 7.02.
