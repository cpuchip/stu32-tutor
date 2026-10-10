---
id: whole-02
title: Multiplying and dividing
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation place-value column-addition
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Maren, Tobin
voices: story plain
---

# Multiplying and dividing

<voice v="story">Thornwick's bakery works in batches and boxes. Maren bakes trays of rolls by the dozen, and Tobin
packs them into boxes to carry.</voice><voice v="plain">A bakery works in batches and boxes: trays of rolls baked by the dozen, packed into boxes to carry.</voice> Finding how many rolls are in all the trays is multiplying; finding
how many boxes they fill, and how many are left over, is dividing. This lesson does both by hand, then checks them on the
calculator, which has a key for each part of a division.

## From before

Two from whole-01, by hand.

```item WH2F1
prompt: Work out 2478 + 1365.
topics: column-addition
answer: type
calculator: no
slip: WH2F1A | every carry left out | Each column that makes ten or more carries one to the next: 8 + 5 is 13, so write 3 and carry 1.
```

```item WH2F2
prompt: Work out 6004 − 2357.
topics: column-subtraction
answer: type
calculator: no
slip: WH2F2A | took the smaller digit from the larger | When the top digit is smaller, borrow from the next column; 4 − 7 is not 3.
```

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Multiplying in parts

<voice v="story">Maren bakes 23 trays of 46 rolls each.</voice><voice v="plain">A bakery makes 23 trays of 46 rolls each.</voice> How many rolls? Split the 23 into 20 and 3, by place value
(whole-01), and multiply 46 by each part:

- 46 × 3: the ones first, 6 × 3 = 18, write 8 and carry 1 ten; then the tens, 4 × 3 = 12, and 1
  carried makes 13. So 138.
- 46 × 20: 20 is 2 tens, and 46 × 2 = 92, so 46 × 2 tens = 92 tens = 920.
- Add the parts: 138 + 920 = 1058.

The parts add up to the whole because 23 trays are 20 trays and 3 trays. The check:
<entry e="alg">× is the multiplication key:</entry><entry e="rpn">the first number, ENTER, the second, then ×:</entry>

```keys M01 entry=alg
46 × 23 ENTER
```

```keys M01 entry=rpn
46 ENTER 23 ×
```

The screen shows <disp v="M01">1,058.0000</disp>.

## Dividing, and what is left over

<voice v="story">Tobin has 59 rolls to pack, 9 to a box.</voice><voice v="plain">59 rolls are to be packed, 9 to a box.</voice> How many full boxes, and how many rolls over? The number you
divide by, here 9, is the divisor. By hand: how many 9s are in 59? 6 × 9 = 54, and 7 × 9 = 63 is too
many, so 6 boxes. 59 − 54 = 5 rolls are left over. The 6 is the quotient and the 5 is the remainder.
Check it: 6 × 9 + 5 = 59.

The ÷ key does not give that answer:

```keys D01 entry=alg
59 ÷ 9 ENTER
```

```keys D01 entry=rpn
59 ENTER 9 ÷
```

The screen shows <disp v="D01">6.5556</disp>: 6 boxes and a part of a box, as a decimal. The digits after
the point are not the remainder: 0.5556 is a part of one box, rounded, and its 5s really go on for
ever. <voice v="story">Tobin cannot carry part of a box.</voice><voice v="plain">Only full boxes count here.</voice> Two keys give the whole number of boxes and the remainder,
both printed on the ÷ key. INT÷, in gold, gives the quotient:
<entry e="alg">on the algebraic line it types IDIV(, short for whole-number divide, and waits for two
numbers: the number to divide first, then a comma (gold, above the point key), then the divisor. ▶
closes the bracket:</entry><entry e="rpn">the number to divide, ENTER, the divisor, then GOLD INT÷:</entry>

```keys D02 entry=alg
GOLD INT÷ 59 GOLD , 9 ▶ ENTER
```

```keys D02 entry=rpn
59 ENTER 9 GOLD INT÷
```

The screen shows <disp v="D02">6.0000</disp>: 6 full boxes.
<entry e="alg">The line reads <disp v="D02" kind="line">IDIV(59,9)</disp>.</entry>
Rmdr, in blue on the same ÷ key, gives the remainder.<entry e="alg"> It types RMDR(, and takes its two
numbers the same way.</entry>

```keys D03 entry=alg
BLUE Rmdr 59 GOLD , 9 ▶ ENTER
```

```keys D03 entry=rpn
59 ENTER 9 BLUE Rmdr
```

The screen shows <disp v="D03">5.0000</disp>: 5 rolls over, as the hand work said.

## Long division

A big division by hand goes one digit at a time from the left. <voice v="story">Tobin has 1000 rolls in boxes of 7.</voice><voice v="plain">1000 rolls go into boxes of 7.</voice>
Write the 1000, and write each digit of the answer above the digit it finishes. "Holds" means how
many whole 7s fit.

- The first digit, 1, is less than 7, so take the first two digits together: 10. 10 holds one 7, with
  3 over. Write 1 above the second digit.
- The 3 left over is 3 hundreds, which is 30 tens. Bring down the next digit, a 0 tens, beside it:
  30. 30 holds four 7s (28), with 2 over. Write 4.
- The 2 left over is 2 tens, or 20 ones. Bring down the last 0 beside it: 20. 20 holds two 7s (14),
  with 6 over. Write 2.

So 1000 ÷ 7 is 142, with 6 over. Check: 7 × 142 + 6 = 994 + 6 = 1000. On the calculator:

```keys D04 entry=alg
GOLD INT÷ 1000 GOLD , 7 ▶ ENTER
```

```keys D04 entry=rpn
1000 ENTER 7 GOLD INT÷
```

The screen shows <disp v="D04">142.0000</disp>, and the remainder:

```keys D05 entry=alg
BLUE Rmdr 1000 GOLD , 7 ▶ ENTER
```

```keys D05 entry=rpn
1000 ENTER 7 BLUE Rmdr
```

The screen shows <disp v="D05">6.0000</disp>.

## Exercises

Do each by hand first, then check.

1. 15 trays of 37 rolls. How many rolls?
2. 100 loaves go into crates of 12. How many full crates, and how many loaves over?
3. A year of 365 days is how many full weeks, and how many days more?

## Answers

1. 37 × 15 is 37 × 5 + 37 × 10. 37 × 5: 7 × 5 = 35, write 5 and carry 3; 3 × 5 = 15, and 3 carried
   makes 18: 185. 37 × 10 = 370. Then 185 + 370 = 555. The check:

   ```keys E01 entry=alg
   37 × 15 ENTER
   ```

   ```keys E01 entry=rpn
   37 ENTER 15 ×
   ```

   The screen shows <disp v="E01">555.0000</disp>.

2. 8 × 12 = 96, and 9 × 12 = 108 is too many: 8 crates, and 100 − 96 = 4 loaves over. The checks:

   ```keys E02 entry=alg
   GOLD INT÷ 100 GOLD , 12 ▶ ENTER
   ```

   ```keys E02 entry=rpn
   100 ENTER 12 GOLD INT÷
   ```

   The screen shows <disp v="E02">8.0000</disp>, and

   ```keys E02B entry=alg
   BLUE Rmdr 100 GOLD , 12 ▶ ENTER
   ```

   ```keys E02B entry=rpn
   100 ENTER 12 BLUE Rmdr
   ```

   shows <disp v="E02B">4.0000</disp>.

3. Long division by 7: 3 is less than 7, so start with 36. 36 holds five 7s (35), 1 over; bring down
   the 5: 15 holds two 7s (14), 1 over. So 52 weeks and 1 day. Check: 7 × 52 + 1 = 364 + 1 = 365. On the
   calculator:

   ```keys E03 entry=alg
   GOLD INT÷ 365 GOLD , 7 ▶ ENTER
   ```

   ```keys E03 entry=rpn
   365 ENTER 7 GOLD INT÷
   ```

   The screen shows <disp v="E03">52.0000</disp>, and

   ```keys E03B entry=alg
   BLUE Rmdr 365 GOLD , 7 ▶ ENTER
   ```

   ```keys E03B entry=rpn
   365 ENTER 7 BLUE Rmdr
   ```

   shows <disp v="E03B">1.0000</disp>.
