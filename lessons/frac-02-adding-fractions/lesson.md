---
id: frac-02
title: Adding and subtracting fractions
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation calc-frac-display fraction-is-division equivalent-fractions simplest-form lcm multiply-first
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
display: FIX 4
cast: Maren
voices: story plain
---

# Adding and subtracting fractions

<voice v="story">Maren's recipe for a small batch of buns needs 1/4 cup of sugar for the dough and 3/8 cup for the
glaze.</voice><voice v="plain">A recipe for a small batch of buns needs 1/4 cup of sugar for the dough and 3/8 cup for the
glaze.</voice> How much sugar is that in all? Adding fractions takes one idea first: fractions can only be
added when their pieces are the same size. This lesson makes them the same size by hand, then
checks with fraction display.

## From before

Two from before, by hand: a least common multiple from factor-02, and fractions from frac-01.

```item FR2F1
prompt: What is the least common multiple of 4 and 6?
topics: lcm
answer: type
calculator: no
slip: FR2F1A | multiplied them | 4 × 6 is a common multiple, but not the least: 4 = 2 × 2 and 6 = 2 × 3 need only 2 × 2 × 3.
```

```item FR2F2
prompt: Write 3/4 with a bottom of 12. What is the top?
topics: equivalent-fractions
answer: type
calculator: no
slip: FR2F2A | added instead of multiplying | Top and bottom are multiplied alike: 4 × 3 is 12, so the top is 3 × 3.
```

## Before you start

The setup from start-01, with →FRAC at the end to turn on fraction display, as in frac-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
```

## A common bottom

1/4 is one piece of a cup cut into 4; 3/8 is three pieces of a cup cut into 8. Quarters and eighths
are different sizes, so 1 + 3 would be 4 pieces, but 4 pieces of what size? Cut the pieces smaller
until they match. Cutting every piece into the same number of smaller pieces multiplies the bottom
(frac-01), so a common bottom has to be a multiple of both bottoms: a common multiple. Any common
multiple works (32 would), but the smallest keeps the numbers small and leaves less to simplify: the
least common multiple of the bottoms (factor-02). LCM(4, 8) = 8.

- 1/4 = 2/8, multiplying top and bottom by 2 (frac-01).
- Now both are eighths: 2/8 + 3/8 = 5/8. Add the tops; the bottom stays 8, because the pieces are
  still eighths.

<voice v="story">So Maren needs 5/8 cup.</voice><voice v="plain">So the recipe needs 5/8 cup.</voice> The method: a common bottom, add the tops, keep the bottom, and simplify at
the end if you can. On the calculator, each fraction is a division (frac-01):
<entry e="alg">type the sum as written; the line divides before it adds (expr-01), so each fraction is
worked out before the +:</entry><entry e="rpn">each fraction, then +:</entry>

```keys A01 entry=alg
1 ÷ 4 + 3 ÷ 8 ENTER
```

```keys A01 entry=rpn
1 ENTER 4 ÷ 3 ENTER 8 ÷ +
```

The screen shows <disp v="A01">0 5/8</disp>, the hand work's answer.

A common slip is to add the tops and add the bottoms: (1 + 3)/(4 + 8) = 4/12 = 1/3. That cannot be
right: 1/3 is less than the 3/8 cup of glaze alone, and adding more sugar cannot give less.

## Another pair

2/5 + 1/2: LCM(5, 2) = 10. 2/5 = 4/10 (top and bottom times 2) and 1/2 = 5/10 (times 5), so the sum is
9/10.

```keys A02 entry=alg
2 ÷ 5 + 1 ÷ 2 ENTER
```

```keys A02 entry=rpn
2 ENTER 5 ÷ 1 ENTER 2 ÷ +
```

The screen shows <disp v="A02">0 9/10</disp>.

The LCM earns its keep when neither bottom divides the other. 1/4 + 1/6: multiplying the bottoms gives
24, but the LCM is 12 (4 = 2 × 2 and 6 = 2 × 3, so two 2s and a 3). 1/4 = 3/12 and 1/6 = 2/12, so the
sum is 5/12. (Over 24 it would be 6/24 + 4/24 = 10/24, which then simplifies to 5/12: the same answer,
with more work.) 5/12 does not come out as an ending decimal (it is 0.41666…), so this one stays a hand
example.

## Taking away

Taking away works the same way: a common bottom, then take away the tops. 7/8 − 1/4: 1/4 = 2/8, so
7/8 − 2/8 = 5/8.

```keys S01 entry=alg
7 ÷ 8 − 1 ÷ 4 ENTER
```

```keys S01 entry=rpn
7 ENTER 8 ÷ 1 ENTER 4 ÷ −
```

The screen shows <disp v="S01">0 5/8</disp>.

## Over a whole

3/4 + 1/2 = 3/4 + 2/4 = 5/4: five quarters. Four of the quarters make one whole, and one quarter is
left: 1 1/4. A fraction whose top is bigger than its bottom is more than 1, and fraction display
shows the whole number first:

```keys A03 entry=alg
3 ÷ 4 + 1 ÷ 2 ENTER
```

```keys A03 entry=rpn
3 ENTER 4 ÷ 1 ENTER 2 ÷ +
```

The screen shows <disp v="A03">1 1/4</disp>.

## Exercises

By hand first, with a common bottom, then check.

1. 1/2 + 1/8.
2. 3/5 − 1/10.
3. 3/8 + 3/4.

## Answers

1. LCM(2, 8) = 8: 1/2 = 4/8, and 4/8 + 1/8 = 5/8.

   ```keys E01 entry=alg
   1 ÷ 2 + 1 ÷ 8 ENTER
   ```

   ```keys E01 entry=rpn
   1 ENTER 2 ÷ 1 ENTER 8 ÷ +
   ```

   The screen shows <disp v="E01">0 5/8</disp>.

2. LCM(5, 10) = 10: 3/5 = 6/10, and 6/10 − 1/10 = 5/10, which in simplest form is 1/2.

   ```keys E02 entry=alg
   3 ÷ 5 − 1 ÷ 10 ENTER
   ```

   ```keys E02 entry=rpn
   3 ENTER 5 ÷ 1 ENTER 10 ÷ −
   ```

   The screen shows <disp v="E02">0 1/2</disp>.

3. LCM(8, 4) = 8: 3/4 = 6/8, and 3/8 + 6/8 = 9/8, which is 1 1/8.

   ```keys E03 entry=alg
   3 ÷ 8 + 3 ÷ 4 ENTER
   ```

   ```keys E03 entry=rpn
   3 ENTER 8 ÷ 3 ENTER 4 ÷ +
   ```

   The screen shows <disp v="E03">1 1/8</disp>.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item FR2M1
prompt: Work out 1/4 + 1/8, as a decimal.
topics: common-bottom
answer: type
calculator: no
slip: FR2M1A | added the tops over the larger bottom | Give them one bottom first: 1/4 is 2/8, and 2/8 + 1/8 is 3/8.
```

```item FR2M2
prompt: What is the greatest common factor of 12 and 20?
topics: gcf
answer: type
calculator: no
slip: FR2M2A | the LCM, not the GCF | 12 = 2 × 2 × 3 and 20 = 2 × 2 × 5 share 2 × 2. 60 is their least common multiple.
```

```item FR2M3
prompt: Work out 7/8 − 1/4, as a decimal.
topics: subtract-fractions
answer: type
calculator: no
slip: FR2M3A | took tops from tops and bottoms from bottoms | Give them one bottom: 1/4 is 2/8, and 7/8 − 2/8 is 5/8.
```

```item FR2M4
prompt: Put 15/25 in simplest form. What is its bottom?
topics: simplest-form
answer: type
calculator: no
slip: FR2M4A | the top, not the bottom | Divide top and bottom by 5: 3 over 5. The bottom is 5.
```
