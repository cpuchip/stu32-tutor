---
id: neg-02
title: Multiplying and dividing negatives
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation negative-number add-negatives quotient-remainder
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Hesk
voices: story plain
---

# Multiplying and dividing negatives

<voice v="story">On a winter night the air by Hesk's mill pond cools by 4 degrees every hour.</voice><voice v="plain">On a winter night the air by a pond cools by 4 degrees every hour.</voice> Write a change of 4 degrees colder as −4.
After 3 hours the change is −4 three times over: 3 × (−4). What does a negative times a number give,
and what about a negative times a negative? This lesson finds the rules, says why they hold, and
checks them on the calculator.

## From before

Two from before, by hand: a negative from neg-01, and one from whole-02.

```item NG2F1
prompt: Work out −8 + 3.
topics: add-negatives
answer: type
calculator: no
slip: NG2F1A | added the sizes and kept the minus | Start at −8 and go 3 to the right: to −5.
```

```item NG2F2
prompt: Work out 18 × 21 by parts: 18 × 20, then 18 × 1.
topics: partial-products
answer: type
calculator: no
slip: NG2F2A | added the 1 | The second part is 18 × 1, which is 18, not 1.
```

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## A positive times a negative

3 × (−4) is −4 added three times: −4 + (−4) + (−4). On the number line (neg-01), that is three moves of 4
to the left from 0: −12.

```keys M01 entry=alg
3 × 4 +/− ENTER
```

```keys M01 entry=rpn
3 ENTER 4 +/− ×
```

The screen shows <disp v="M01">-12.0000</disp>. After 3 hours the air is 12 degrees colder. A positive
times a negative is negative. And the order of multiplying does not matter (3 × 4 and 4 × 3 are the
same rows turned around), so a negative times a positive, like (−4) × 3, is negative too.

## A negative times a negative

Watch a pattern, multiplying −4 by 3, then 2, then 1, then 0:

- 3 × (−4) = −12
- 2 × (−4) = −8
- 1 × (−4) = −4
- 0 × (−4) = 0

Each time the first number goes down by 1, there is one −4 fewer, so the answer is the last one with a
−4 taken away. Taking away −4 adds 4 (neg-01). So going on below zero, each step still adds 4:
(−1) × (−4) = 0 + 4 = 4, (−2) × (−4) = 8, (−3) × (−4) = 12. A negative times a negative is positive.
On the thermometer: if the air cools 4 degrees an hour, then 3 hours ago, which is −3 hours, it was 12 degrees
warmer.

```keys M02 entry=alg
3 +/− × 4 +/− ENTER
```

```keys M02 entry=rpn
3 +/− ENTER 4 +/− ×
```

The screen shows <disp v="M02">12.0000</disp>. So for multiplying: the same signs give a positive
answer, and different signs give a negative one.

## Dividing

Dividing undoes multiplying (expr-02), so each division is a multiplication question, and that is why
the same sign rule comes out. −12 ÷ 4 asks "4 times what is −12?", and 4 × (−3) = −12, so the answer is
−3:

```keys D01 entry=alg
12 +/− ÷ 4 ENTER
```

```keys D01 entry=rpn
12 +/− ENTER 4 ÷
```

The screen shows <disp v="D01">-3.0000</disp>. And −12 ÷ (−4) asks "−4 times what is −12?": 3, since
(−4) × 3 = −12.

```keys D02 entry=alg
12 +/− ÷ 4 +/− ENTER
```

```keys D02 entry=rpn
12 +/− ENTER 4 +/− ÷
```

The screen shows <disp v="D02">3.0000</disp>. The same signs, positive; different signs, negative.

## INT÷ and Rmdr with a negative

−7 ÷ 2 is −3.5. INT÷ (whole-02) gives an integer. This calculator always takes the integer at or below
the answer: the nearest one at or to its left on the number line. (For 84 ÷ 6, which is exactly 14, that is
14 itself.) The integer below −3.5 is −4, not −3:

```keys F01 entry=alg
GOLD INT÷ 7 +/− GOLD , 2 ▶ ENTER
```

```keys F01 entry=rpn
7 +/− ENTER 2 GOLD INT÷
```

The screen shows <disp v="F01">-4.0000</disp>. On the number line, 2 × (−4) = −8 is the multiple of 2
at or to the left of −7, and the remainder is the step from −8 up to −7: 1. So the remainder is
positive:

```keys F02 entry=alg
BLUE Rmdr 7 +/− GOLD , 2 ▶ ENTER
```

```keys F02 entry=rpn
7 +/− ENTER 2 BLUE Rmdr
```

The screen shows <disp v="F02">1.0000</disp>. Check: 2 × (−4) + 1:

```keys C01 entry=alg
2 × 4 +/− + 1 ENTER
```

```keys C01 entry=rpn
2 ENTER 4 +/− × 1 +
```

The screen shows <disp v="C01">-7.0000</disp>. When the number you divide by is positive, the multiple
is always at or left of the number, so this calculator's remainder is never negative. (Some other
calculators and computer languages chop −3.5 to −3 instead, with remainder −1: −7 = 2 × (−3) + (−1).
Neither is wrong; they follow different rules. So check which one a calculator follows before
trusting it with negatives.)

## Exercises

Work out the sign first, then the size (the number without its sign), then check.

1. (−6) × 5.
2. (−8) × (−3).
3. (−20) ÷ (−5).
4. INT÷ and Rmdr of −10 and 3.
5. 15 ÷ (−3).

## Answers

1. Different signs: negative. 6 × 5 = 30, so −30.

   ```keys E01 entry=alg
   6 +/− × 5 ENTER
   ```

   ```keys E01 entry=rpn
   6 +/− ENTER 5 ×
   ```

   The screen shows <disp v="E01">-30.0000</disp>.

2. The same signs: positive. 8 × 3 = 24.

   ```keys E02 entry=alg
   8 +/− × 3 +/− ENTER
   ```

   ```keys E02 entry=rpn
   8 +/− ENTER 3 +/− ×
   ```

   The screen shows <disp v="E02">24.0000</disp>.

3. The same signs: positive. 20 ÷ 5 = 4.

   ```keys E03 entry=alg
   20 +/− ÷ 5 +/− ENTER
   ```

   ```keys E03 entry=rpn
   20 +/− ENTER 5 +/− ÷
   ```

   The screen shows <disp v="E03">4.0000</disp>.

4. −10 ÷ 3 is −3.33…, so the integer at or below is −4. Then 3 × (−4) = −12, and from −12 up to −10 is
   2, the remainder. Check: 3 × (−4) + 2 = −10.

   ```keys E04 entry=alg
   GOLD INT÷ 10 +/− GOLD , 3 ▶ ENTER
   ```

   ```keys E04 entry=rpn
   10 +/− ENTER 3 GOLD INT÷
   ```

   The screen shows <disp v="E04">-4.0000</disp>, and

   ```keys E04B entry=alg
   BLUE Rmdr 10 +/− GOLD , 3 ▶ ENTER
   ```

   ```keys E04B entry=rpn
   10 +/− ENTER 3 BLUE Rmdr
   ```

   shows <disp v="E04B">2.0000</disp>.

5. Different signs: negative. 15 ÷ 3 = 5, so −5.

   ```keys E05 entry=alg
   15 ÷ 3 +/− ENTER
   ```

   ```keys E05 entry=rpn
   15 ENTER 3 +/− ÷
   ```

   The screen shows <disp v="E05">-5.0000</disp>.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item NG2M1
prompt: Work out (−7) × (−6).
topics: sign-rules
answer: type
calculator: no
slip: NG2M1A | kept the minus | A negative times a negative is positive.
```

```item NG2M2
prompt: Work out −3 − (−10).
topics: subtract-negatives
answer: type
calculator: no
slip: NG2M2A | took away 10, not −10 | Taking away a negative adds it: −3 + 10.
```

```item NG2M3
prompt: Work out 36 ÷ (−4).
topics: divide-negatives
answer: type
calculator: no
slip: NG2M3A | dropped the minus | A positive divided by a negative is negative.
```

```item NG2M4
prompt: Work out 504 ÷ 7 by long division.
topics: long-division
answer: type
calculator: no
slip: NG2M4A | stopped before the last digit | Bring down every digit: after 50 comes the 4.
```
