---
id: lin-02
title: Lines through data
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Lines through data

Measurements rarely sit exactly on a line. A seedling measured at the end of each of five weeks
might be 3, 5, 6, 8 and 11 centimetres tall: rising steadily, but not by the same amount each week.
No straight line passes through all five points, but one passes closest to them, and the calculator
can find it. Its slope and intercept summarise the data, and the line can then estimate a value you
did not measure. This lesson finds that line for the seedling.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. All the examples in the lesson are one chain, each
carrying on from the one before; each exercise starts fresh.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Entering the data

The calculator keeps running sums of the points you give it: of the x values, of the y values, and
a few more the line needs. Σ, the Greek capital S, stands for sum. Σ+ adds a point to the sums and
Σ− takes one out; the sums stay until you clear them. Clear them first, so no earlier data mixes in:
CLEAR is gold above ←, and its Σ soft key clears the sums.

Σ+, the last key of the top row, reads x from X and y from Y. So give each point y first, then
ENTER, which pushes the y up to Y, then x, then Σ+. That is the opposite of the (x, y) order points
are written in, so it is worth saying to yourself as you go: y, ENTER, x, Σ+. The first point is
week 1, 3 centimetres:

```keys D01
GOLD CLEAR Σ 3 ENTER 1 Σ+
```

X shows <disp v="D01">1.0000</disp>: Σ+ answers with how many points the sums hold. The other four:

```keys D02 after=D01
5 ENTER 2 Σ+ 6 ENTER 3 Σ+ 8 ENTER 4 Σ+ 11 ENTER 5 Σ+
```

X shows <disp v="D02">5.0000</disp>: five points.

## The line

L.R., blue above +, opens the menu for the line. L.R. stands for linear regression, the name of
this way of fitting a line to data. m gives its slope:

```keys D03 after=D02
BLUE L.R. m
```

X shows <disp v="D03">1.9000</disp>: the seedling grows about 1.9 centimetres a week. b gives the
intercept:

```keys D04 after=D03
BLUE L.R. b
```

X shows <disp v="D04">0.9000</disp>. The line is y = 1.9x + 0.9. Its intercept is the line's value
at week 0, a week before the first measurement. No height was measured there; it is where the line
crosses the vertical axis, not a fact about the seedling.

ŷ gives the line's y for the x in X. The hat marks a value read from the line, not from the data.
At week 3:

```keys D04B after=D04
3 BLUE L.R. ŷ
```

X shows <disp v="D04B">6.6000</disp>, and the measurement at week 3 was 6: that point is 0.6 below
the line. Closest means this: take each point's distance above or below the line, square it, and
add the squares. Squaring makes every distance count as positive, so points above and below cannot
cancel out. The line the calculator finds makes that total as small as any line can, which is why
it is also called the least-squares line.

## How well a line fits

r says how well a sloping line fits the points:

```keys D05 after=D04B
BLUE L.R. r
```

X shows <disp v="D05">0.9851</disp>. r is always between −1 and 1, and it has the same sign as the
slope. Near 1, the points lie close to a rising line; near −1, close to a falling one. Near 0, they
show no rise or fall a line can follow: they may be scattered, or spread along a flat line, or on
a curve that rises and falls (lin-03 has one). Points exactly on a flat line have no r at all, as
lin-03 shows. 0.9851 says the seedling's points lie very close to their
rising line.

## Estimating

The line can estimate what was not measured. The height at week 6:

```keys D06 after=D05
6 BLUE L.R. ŷ
```

X shows <disp v="D06">12.3000</disp>, which is 1.9 × 6 + 0.9. x̂ goes the other way: the x for the
y in X. When does the line reach 15 centimetres?

```keys D07 after=D06
15 BLUE L.R. x̂
```

X shows <disp v="D07">7.4211</disp>: a little under seven and a half weeks. Both answers lie beyond
the measured weeks, and the line can only assume that the pattern carries on. Estimates between
the measured weeks are the safest; the further past them, the less a line can be trusted. Week 50
would give 95.9 centimetres, and no seedling promised that. This one grew 2, 1, 2 and then 3
centimetres from week to week, faster at the end, so its real height at week 6 may well be above
the line's.

## Fixing a mistake

Say the last point went in twice:

```keys W01A after=D07
11 ENTER 5 Σ+
```

X shows <disp v="W01A">6.0000</disp>: six points, one too many. The line has moved:

```keys W01 after=W01A
BLUE L.R. m
```

X shows <disp v="W01">1.9750</disp>. Σ−, gold above Σ+, takes a point out of the sums. Give it
exactly the y and x that went in:

```keys W02A after=W01
11 ENTER 5 GOLD Σ−
```

X shows <disp v="W02A">5.0000</disp>, five points again, and the slope is back:

```keys W02 after=W02A
BLUE L.R. m
```

X shows <disp v="W02">1.9000</disp>. Σ− cannot check that the point was ever entered: given a y and
x that never went in, it takes them out of the sums all the same, and the line is quietly wrong.
Watch the count, and type the point exactly.

## Exercises

1. A second seedling measured 4, 6, 7, 10 and 13 centimetres at the end of weeks 1 to 5. Find the
   line's slope and intercept, and its estimate for week 6.
2. A leaking tank is measured at hours 1, 2, 3 and 4: it holds 10, 8, 7 and 4 litres. Find r, then
   m. What do their signs say?

## Answers

1. Clear the sums, enter the five points, and ask for m:

   ```keys E01
   GOLD CLEAR Σ 4 ENTER 1 Σ+ 6 ENTER 2 Σ+ 7 ENTER 3 Σ+ 10 ENTER 4 Σ+ 13 ENTER 5 Σ+ BLUE L.R. m
   ```

   X shows <disp v="E01">2.2000</disp>. Then b:

   ```keys E01B after=E01
   BLUE L.R. b
   ```

   X shows <disp v="E01B">1.4000</disp>, and week 6:

   ```keys E01C after=E01B
   6 BLUE L.R. ŷ
   ```

   X shows <disp v="E01C">14.6000</disp>: 2.2 × 6 + 1.4.

2. The keys:

   ```keys E02
   GOLD CLEAR Σ 10 ENTER 1 Σ+ 8 ENTER 2 Σ+ 7 ENTER 3 Σ+ 4 ENTER 4 Σ+ BLUE L.R. r
   ```

   X shows <disp v="E02">-0.9812</disp>, close to −1: the points lie close to a falling line. Then m:

   ```keys E02B after=E02
   BLUE L.R. m
   ```

   X shows <disp v="E02B">-1.9000</disp>: the tank loses about 1.9 litres an hour. Both are
   negative, as r and m always share a sign: the water goes down as the hours go up.
