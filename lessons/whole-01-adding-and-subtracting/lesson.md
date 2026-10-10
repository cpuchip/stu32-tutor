---
id: whole-01
title: Adding and subtracting
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Hesk, Tobin
voices: story plain
---

# Adding and subtracting

<voice v="story">In Thornwick, Hesk runs the mill on the river, and Tobin carries the bakery's orders around town.
Both of them add and take away large numbers every day: sacks of grain, loaves delivered, loaves
still to go. This lesson does it by hand, the way they would, then checks it on the calculator.</voice><voice v="plain">A mill and a bakery add and take away large numbers every day: sacks of grain, loaves delivered,
loaves still to go. This lesson does it by hand, then checks it on the calculator.</voice>

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Place value

In 3452 each digit means something different because of where it sits. Reading from the right: 2
ones, 5 tens, 4 hundreds and 3 thousands. So 3452 = 3000 + 400 + 50 + 2. To add two numbers, add the
ones to the ones, the tens to the tens, and so on: like with like, one column at a time. And one of
any place is worth ten of the place to its right: 1 thousand is 10 hundreds, 1 hundred is 10 tens, 1
ten is 10 ones. So ten in any column can be traded for one in the next column left, and one can be
traded for ten in the next column right. That trade is what carrying and borrowing are.

## Adding, column by column

<voice v="story">Hesk's mill ground 3452 kilograms of grain in the summer and 1879 in the autumn.</voice><voice v="plain">A mill grinds 3452 kilograms of grain in the summer and 1879 in the autumn.</voice> How much in all?
Write the numbers one above the other, ones under ones, and add each column from the right.

- Ones: 2 + 9 = 11 ones. That is 1 ten and 1 one: write the 1 in the ones, and carry the ten to the
  tens column, where it is written as 1, because there it counts tens.
- Tens: 5 + 7 + 1 carried = 13 tens. Write the 3, carry 1 to the hundreds.
- Hundreds: 4 + 8 + 1 = 13 hundreds. Write the 3, carry 1 to the thousands.
- Thousands: 3 + 1 + 1 = 5.

By hand, 3452 + 1879 = 5331. Now the check:
<entry e="alg">type it as written, then ENTER:</entry><entry e="rpn">the first number, ENTER, the second, then +.
In RPN, − works the same way, and takes the second number away from the first:</entry>

```keys A01 entry=alg
3452 + 1879 ENTER
```

```keys A01 entry=rpn
3452 ENTER 1879 +
```

The screen shows <disp v="A01">5,331.0000</disp>, the same as the hand work. The calculator puts a
comma every three digits to the left of the point, to make a long number easier to read.

## Taking away, column by column

Taking away also goes column by column from the right. <voice v="story">Tobin had 742 loaves in the store and sent out
368.</voice><voice v="plain">A store holds 742 loaves, and 368 are sent out.</voice> How many are left?

- Ones: 2 is less than 8, so borrow. Trade 1 of the 4 tens for 10 ones: 12 ones, and 3 tens left.
  12 − 8 = 4.
- Tens: 3 is less than 6, so borrow again. Trade 1 of the 7 hundreds for 10 tens: 13 tens, and 6
  hundreds left. 13 − 6 = 7.
- Hundreds: 6 − 3 = 3.

By hand, 742 − 368 = 374. The check:

```keys B01 entry=alg
742 − 368 ENTER
```

```keys B01 entry=rpn
742 ENTER 368 −
```

The screen shows <disp v="B01">374.0000</disp>.

Zeros make borrowing take longer. <voice v="story">Tobin had 5000 loaves to deliver this season and has delivered 2768.</voice><voice v="plain">5000 loaves are to be delivered this season, and 2768 have been.</voice>
The ones column has 0 to take 8 from, and there are no tens or hundreds to borrow from either. So
trade down a step at a time. 1 of the 5 thousands becomes 10 hundreds, leaving 4 thousands. Keep 9 of
those hundreds, and trade the last one for 10 tens. Keep 9 tens, and trade the last one for 10 ones.
Now 5000 is 4 thousands, 9 hundreds, 9 tens and 10 ones, still 5000, and every column has enough:

- Ones: 10 − 8 = 2.
- Tens: 9 − 6 = 3.
- Hundreds: 9 − 7 = 2.
- Thousands: 4 − 2 = 2.

By hand, 5000 − 2768 = 2232. The check:

```keys A02 entry=alg
5000 − 2768 ENTER
```

```keys A02 entry=rpn
5000 ENTER 2768 −
```

The screen shows <disp v="A02">2,232.0000</disp>. Order matters in taking away: 2768 − 5000 would be a
different question, a number below zero, which unit 4 is about.

## Estimating, to catch a slip

A calculator does exactly what it is told, so a key missed in typing gives a wrong answer that looks
just as sure as a right one. An estimate catches that. Round each number to the nearest hundred and
add those instead. To round to the nearest hundred, look at the tens digit: 5 or more rounds up, less
than 5 rounds down. 3452 has 5 tens, so it rounds up to 3500; 1879 has 7 tens, so it rounds up to 1900, so the sum should be near 3500 + 1900 =
5400. 5331 is near 5400, so it is believable.

Now suppose the 1 of 1879 was missed in typing:

```keys A03 entry=alg
3452 + 879 ENTER
```

```keys A03 entry=rpn
3452 ENTER 879 +
```

The screen shows <disp v="A03">4,331.0000</disp>, more than a thousand away from the estimate of 5400.
Something went wrong, and the estimate said so before anyone believed it.

## Exercises

Do each by hand first, estimate, then check.

1. The mill had 607 sacks in the store and 2598 more came in. How many now?
2. <voice v="story">Tobin had 4003 loaves to deliver and has delivered 1756.</voice><voice v="plain">4003 loaves are to be delivered, and 1756 of them have been.</voice> How many are left?
3. Estimate 6120 − 2890 to the nearest hundred, then work it out exactly.

## Answers

1. The estimate: 600 + 2600 = 3200. By hand: ones 7 + 8 = 15, write 5, carry 1. Tens: 0 + 9 + 1 = 10,
   write 0, carry 1. Hundreds: 6 + 5 + 1 = 12, write 2, carry 1. Thousands: 2 + 1 = 3. So 3205, near
   the estimate. The check:

   ```keys E01 entry=alg
   607 + 2598 ENTER
   ```

   ```keys E01 entry=rpn
   607 ENTER 2598 +
   ```

   The screen shows <disp v="E01">3,205.0000</disp>.

2. The estimate: 4000 − 1800 = 2200. By hand, trade down from the thousands as for 5000: 4003 is 3
   thousands, 9 hundreds, 9 tens and 10 + 3 = 13 ones. Then 13 − 6 = 7, 9 − 5 = 4, 9 − 7 = 2 and
   3 − 1 = 2: 2247, near the estimate. The check:

   ```keys E02 entry=alg
   4003 − 1756 ENTER
   ```

   ```keys E02 entry=rpn
   4003 ENTER 1756 −
   ```

   The screen shows <disp v="E02">2,247.0000</disp>.

3. To the nearest hundred, 6100 − 2900 = 3200. Exactly, column by column: ones 0 − 0 = 0. Tens: 2 is
   less than 9, so trade 1 hundred for 10 tens: 12 − 9 = 3. Hundreds: now 0, less than 8, so trade 1
   thousand: 10 − 8 = 2. Thousands: now 5, and 5 − 2 = 3. So 3230, near the estimate:

   ```keys E03 entry=alg
   6120 − 2890 ENTER
   ```

   ```keys E03 entry=rpn
   6120 ENTER 2890 −
   ```

   The screen shows <disp v="E03">3,230.0000</disp>.
