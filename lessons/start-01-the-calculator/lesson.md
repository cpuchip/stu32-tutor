---
id: start-01
title: Getting started with the calculator
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires:
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; the bakery is a placeholder world)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
---

# Getting started with the calculator

In this course you work each idea out by hand first, and then the STU-32 checks your answer. This
lesson shows how to set the calculator up, how to type a calculation, how to use the last answer,
and how to make the calculator show fractions. The examples come from a bakery.

## Before you start

Some keys have two more jobs, printed above them in gold and in blue. To use a gold one, press the
gold key first and then the key it is printed above; blue works the same way. So BLUE MODE means: the
blue key, then the key with MODE printed above it in blue (that is ENTER).

Some keys open a menu. Its choices appear along the bottom of the screen, and the six blank keys
just under the screen pick them. These are called soft keys, because what each one does depends on
the menu that is open.

The setup is three choices, each made with a soft key. First the mode: STU, the STU-32's own way of
working (the other two modes copy two older calculators). Then how you type:
<entry e="alg">ALG, short for algebraic, which lets you type a calculation the way it is written.</entry>
<entry e="rpn">RPN, short for Reverse Polish Notation, which keeps numbers in a stack, like a pile:
each number you type goes on top, and an operation works on the top two.</entry>
Last, the display: DISP is gold above the 2 key, and FIX 4 shows four digits after the decimal point.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

<entry e="rpn">The screen shows four lines, named T, Z, Y and X from top to bottom. X, at the bottom,
is the top of the pile: the number you just typed, and where every answer lands. Y is the number
under it.</entry>

## A first calculation

The bakery bakes 7 apple pies and 5 cherry pies. By hand, 7 + 5 = 12. Now check it.
<entry e="alg">Type it the way it is written. ENTER works as the = key:</entry>
<entry e="rpn">Type 7, then ENTER, then 5, then +. ENTER finishes the 7, so the 5 you type next is a
new number and not 75. The operation always comes last:</entry>

```keys C01 entry=alg
7 + 5 ENTER
```

```keys C01 entry=rpn
7 ENTER 5 +
```

The screen shows <disp v="C01">12.0000</disp>: 12 pies, with four digits after the decimal point
because of FIX 4.
<entry e="alg">The line you typed stays on the screen above the answer: <disp v="C01" kind="line">7+5</disp>.</entry>
<entry e="rpn">It is in X, at the bottom of the screen.</entry>

## Using the answer

Tomorrow the bakery bakes twice as many: by hand, 12 × 2 = 24. The answer is still there, so carry
on from it.
<entry e="alg">When you press an operation key straight after an answer, the calculator starts the
new line with ANS, short for the last answer:</entry>
<entry e="rpn">The 12 is already finished, so it needs no ENTER: type 2, and the × works on the 12
and the 2:</entry>

```keys C02 entry=alg after=C01
× 2 ENTER
```

```keys C02 entry=rpn after=C01
2 ×
```

The screen shows <disp v="C02">24.0000</disp>.
<entry e="alg">The line reads <disp v="C02" kind="line">ANS×2</disp>.</entry>

The bakery has 100 boxes, and each of the 24 pies takes one. How many boxes are left? By hand,
100 − 24 = 76. This time the last answer comes second.
<entry e="alg">Pressing − first would start the line with ANS and work out 24 − 100. Instead type 100,
then −, then ANS. In ALG, the key with LASTx printed in gold above ENTER types ANS:</entry>
<entry e="rpn">Type 100. Now 100 is in X and 24 is in Y. − takes X away from Y, which would work out
24 − 100, so first the x↔y key swaps X and Y:</entry>

```keys C03 entry=alg after=C02
100 − GOLD LASTx ENTER
```

```keys C03 entry=rpn after=C02
100 x↔y −
```

The screen shows <disp v="C03">76.0000</disp>: 76 boxes left.
<entry e="alg">The line reads <disp v="C03" kind="line">100-ANS</disp>.</entry>

## Fractions on the screen

The bakery shares 20 cups of flour equally among 8 batches of dough. By hand: 8 goes into 20 twice,
which uses 16 cups, and 4 cups are left. Those 4 cups shared among 8 batches is half a cup each, so
each batch gets 2 and a half cups. Now check it:

```keys F01 entry=alg
20 ÷ 8 ENTER
```

```keys F01 entry=rpn
20 ENTER 8 ÷
```

The screen shows <disp v="F01">2.5000</disp>: 2 and 5 tenths, the same as 2 and a half. To see it as
a fraction, turn on fraction display with BLUE →FRAC. →FRAC is printed in blue above the decimal
point key. (Careful: another FRAC is printed above the E key. That one opens a menu.)

```keys F02 after=F01
BLUE →FRAC
```

The screen shows <disp v="F02">2 1/2</disp>: a whole number, a space, and then the fraction. The
fraction is always in its simplest form, the smallest numbers that name it: 4/8 shows as 1/2.
Fraction display stays on until you press BLUE →FRAC again.

Now share 1 pie equally among 3 people:

```keys F03 entry=alg after=F02
1 ÷ 3 ENTER
```

```keys F03 entry=rpn after=F02
1 ENTER 3 ÷
```

The screen shows <disp v="F03">0 1/3</disp>: no whole pies, and 1/3 of a pie each. Look at the top
line of the screen, the status band. It has a small <disp v="F03" kind="status">▼</disp>. 1 ÷ 3 is
0.333... and the 3s never end, but the calculator keeps only 34 digits. So its number is a tiny bit
less than 1/3, and the ▼ says so. When there is no arrow, the fraction shown is exactly the
calculator's number.

Press BLUE →FRAC again to turn fraction display off:

```keys F04 after=F03
BLUE →FRAC
```

The screen shows <disp v="F04">0.3333</disp>: the same number, rounded to four digits after the
decimal point.

## Exercises

Work each one out by hand first, then check it on the calculator. If the two answers differ, look
for the slip in each: either one can be the wrong one.

1. The bakery sells 45 loaves in the morning and 38 in the afternoon. How many in all?
2. 9 cups of sugar are shared equally among 4 cakes. How much does each cake get, as a whole number
   and a fraction? Turn fraction display on first, and off again after.

## Answers

1. By hand: the tens, 40 + 30 = 70, and the ones, 5 + 8 = 13, so 70 + 13 = 83. The check:

   ```keys E01 entry=alg
   45 + 38 ENTER
   ```

   ```keys E01 entry=rpn
   45 ENTER 38 +
   ```

   The screen shows <disp v="E01">83.0000</disp>.

2. By hand: 4 goes into 9 twice, which uses 8 cups, and 1 cup is left. That 1 cup shared among 4
   cakes is 1/4 cup each, so each cake gets 2 1/4 cups. The check, with fraction display turned on
   first:

   ```keys E02 entry=alg
   BLUE →FRAC 9 ÷ 4 ENTER
   ```

   ```keys E02 entry=rpn
   BLUE →FRAC 9 ENTER 4 ÷
   ```

   The screen shows <disp v="E02">2 1/4</disp>. And off again:

   ```keys E03 after=E02
   BLUE →FRAC
   ```

   The screen shows <disp v="E03">2.2500</disp>.
