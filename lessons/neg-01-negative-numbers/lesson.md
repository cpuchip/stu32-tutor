---
id: neg-01
title: Negative numbers
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation column-subtraction
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Hesk
voices: story plain
---

# Negative numbers

<voice v="story">In winter, Hesk keeps a thermometer by the mill pond.</voice><voice v="plain">In winter, a thermometer hangs by a pond.</voice> At dawn the air is 5 degrees Celsius; by night
it is 8 degrees colder. How cold is it tonight? Water freezes at 0 degrees Celsius, and tonight the air
is colder than that, so the pond will freeze over, and the answer needs a number below zero. This lesson is about those numbers: what
they mean, how they line up, and how to add and take them away.

## From before

Two from whole-01, by hand.

```item NG1F1
prompt: Work out 803 − 467.
topics: column-subtraction
answer: type
calculator: no
slip: NG1F1A | took the smaller digit from the larger | 3 − 7 needs a borrow, and the tens are 0, so borrow from the hundreds.
```

```item NG1F2
prompt: Round 4762 to the nearest hundred.
topics: estimating
answer: type
calculator: no
working: none
slip: NG1F2A | rounded down | The tens digit is 6, which is 5 or more, so it rounds up.
```

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Below zero

A number below zero is negative, written with a minus sign in front: −3 is "three below zero". The
whole numbers and their negatives together are the integers. Picture them on a line, zero in the
middle, the positive numbers to the right and the negatives to the left:

```
  −8  −7  −6  −5  −4  −3  −2  −1   0   1   2   3   4   5
```

Further right is bigger. So 5 is bigger than −3, and −3 is bigger than −8, even though 8 is bigger
than 3: −8 is further below zero. <voice v="story">On Hesk's thermometer, −3 degrees is warmer than −8.</voice><voice v="plain">On a thermometer, −3 degrees is warmer than −8.</voice>

The sign − now has two jobs. Between two numbers it means take away, as in 5 − 8. In front of one
number it means below zero, as in −8. When a negative number follows an operation, brackets keep the
two jobs apart: 5 + (−8) is "5 plus negative 8".

## Adding a negative

Adding a positive number moves right along the line; adding a negative moves left. The air at 5
degrees, 8 degrees colder: 5 + (−8). Start at 5 and move 8 to the left: 5 steps reach 0, and 3 more
reach −3. So 5 + (−8) = −3, the same as 5 − 8. Tonight the air is 3 degrees below zero, and the pond's top
freezes.

On the calculator, the − key takes away, and +/− flips the sign of the number being typed: 8 becomes
−8 (and −8 would become 8 again).
<entry e="alg">On the algebraic line, +/− can come before or after the digits; either way the line
shows a minus sign in front of the number:</entry><entry e="rpn">Type the number, then +/−, then
ENTER or an operation key to finish it:</entry>

```keys A01 entry=alg
5 + 8 +/− ENTER
```

```keys A01 entry=rpn
5 ENTER 8 +/− +
```

The screen shows <disp v="A01">-3.0000</disp>. The calculator writes the minus sign as a short dash.
<entry e="alg">The line reads <disp v="A01" kind="line">5+-8</disp>: 5 plus negative 8.</entry>

A mistake to watch for: +/− works on the number being typed, and digits typed after it keep going
into that same number. Here is the mistake, typing 8, +/−, then 5:

```keys S01
8 +/− 5 ENTER
```

The screen shows <disp v="S01">-85.0000</disp>: not −8 and 5, but one number, −85. To get −8 and then 5,
finish the −8 first, with an operation key (as in the example above) or, in RPN, with ENTER.

A negative plus a negative goes further left: −3 + (−5). Start at −3 and move 5 to the left: −8.

```keys A04 entry=alg
3 +/− + 5 +/− ENTER
```

```keys A04 entry=rpn
3 +/− ENTER 5 +/− +
```

The screen shows <disp v="A04">-8.0000</disp>.

## Taking away a negative

Taking away is the opposite of adding, so taking away a negative moves the other way: right. One way to
picture it: in the morning the air is −4 degrees, and the sun takes away 6 degrees of cold:
−4 − (−6). Start at −4 and move 6 to the right: 4 steps reach 0, and 2 more reach 2. So
−4 − (−6) = 2, the same as −4 + 6. Taking away a negative is adding the positive: − (−6) is + 6.

```keys A02 entry=alg
4 +/− − 6 +/− ENTER
```

```keys A02 entry=rpn
4 +/− ENTER 6 +/− −
```

The screen shows <disp v="A02">2.0000</disp>.

Taking away a positive from a negative goes further left: −3 − 5. Start at −3 and move 5 to the left:
−8.

```keys A03 entry=alg
3 +/− − 5 ENTER
```

```keys A03 entry=rpn
3 +/− ENTER 5 −
```

The screen shows <disp v="A03">-8.0000</disp>.

## Exercises

Use the number line by hand first, then check.

1. −7 + 10.
2. 2 − 9.
3. −5 − (−2).
4. Put −2, 5, −7 and 0 in order, smallest first.

## Answers

1. Start at −7 and move 10 right: 7 steps reach 0, 3 more reach 3.

   ```keys E01 entry=alg
   7 +/− + 10 ENTER
   ```

   ```keys E01 entry=rpn
   7 +/− ENTER 10 +
   ```

   The screen shows <disp v="E01">3.0000</disp>.

2. Start at 2 and move 9 left: 2 steps reach 0, 7 more reach −7.

   ```keys E02 entry=alg
   2 − 9 ENTER
   ```

   ```keys E02 entry=rpn
   2 ENTER 9 −
   ```

   The screen shows <disp v="E02">-7.0000</disp>.

3. Taking away −2 is adding 2: −5 + 2. Start at −5 and move 2 right: −3.

   ```keys E03 entry=alg
   5 +/− − 2 +/− ENTER
   ```

   ```keys E03 entry=rpn
   5 +/− ENTER 2 +/− −
   ```

   The screen shows <disp v="E03">-3.0000</disp>.

4. Left to right on the number line: −7, −2, 0, 5.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item NG1M1
prompt: Work out −6 + 9.
topics: add-negatives
answer: type
calculator: no
slip: NG1M1A | added the sizes and kept the minus | Start at −6 and go 9 to the right: past 0, to 3.
```

```item NG1M2
prompt: Work out 1468 + 2579.
topics: column-addition
answer: type
calculator: no
slip: NG1M2A | every carry left out | 8 + 9 is 17: write 7 and carry 1 to the tens, and so on.
```

```item NG1M3
prompt: Work out 4 − (−5).
topics: subtract-negatives
answer: type
calculator: no
slip: NG1M3A | took away 5, not −5 | Taking away a negative adds it: 4 − (−5) is 4 + 5.
```

```item NG1M4
prompt: What is the 7 in 3742 worth?
topics: place-value
answer: type
calculator: no
working: none
slip: NG1M4A | the digit, not its worth | The 7 sits in the hundreds column: 7 hundreds, 700.
```
