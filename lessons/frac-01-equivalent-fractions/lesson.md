---
id: frac-01
title: Equivalent fractions
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation calc-frac-display calc-frac-arrows
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
cast: Maren
voices: story plain
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
display: FIX 4
---

# Equivalent fractions

<voice v="story">In Thornwick's market, two pies come out of the oven at Maren's bakery, the same size. Maren cuts the
first into 4 equal pieces and the second into 2 equal pieces.</voice><voice v="plain">Two pies of the same size come out of an oven. The first is cut
into 4 equal pieces and the second into 2 equal pieces.</voice> One customer buys 2 pieces of the first
pie. Another buys 1 piece of the second. Who got more pie?

Work it out by hand first. Draw two circles the same size. Cut the first into 4 equal parts and
shade 2 of them: that is 2/4 of a pie. Cut the second into 2 equal parts and shade 1: that is 1/2 of
a pie. The shaded parts are the same size, so the two customers got the same amount. 2/4 and 1/2 are
two names for one amount. Fractions like that are called equivalent fractions.

## Before you start

Set the calculator up as in start-01: the mode, how you type
<entry e="alg">(ALG)</entry><entry e="rpn">(RPN)</entry>, and the display. Then press BLUE →FRAC to
turn on fraction display, so the calculator shows its answers as fractions. It stays on for the whole
lesson.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
```

## Making equivalent fractions by hand

The bottom number of a fraction counts the equal pieces in a whole. The top number counts the pieces
taken. Now cut every piece of the second pie in half. There are 2 × 2 = 4 pieces in the pie, and the
customer's piece is now 1 × 2 = 2 of them. The amount of pie has not changed: 1/2 = 2/4. Cut every
piece into 3 instead, and there are 2 × 3 = 6 pieces, with the customer's piece now 1 × 3 = 3 of
them: 1/2 = 3/6.

That is the rule. Multiply the top and the bottom by the same whole number (any but 0), and the new
fraction names the same amount. By 4, 1/2 becomes 4/8. So 1/2, 2/4, 3/6 and 4/8 are all equivalent.

The rule can aim at a bottom number you want. To write 1/2 with a bottom number of 8: 8 is 2 × 4, so
multiply the top by 4 as well, and 1/2 = 4/8.

## Simplest form

The rule works the other way too. A number divides another when it goes into it evenly, with nothing
left over: 2 divides 6, because 6 ÷ 2 = 3 exactly. Divide the top and the bottom by a number that
divides both, and the fraction still names the same amount. 2 divides both 6 and 8, so 6/8 = 3/4.
Nothing but 1 divides both 3 and 4, so 3/4 cannot be written with smaller numbers. It is in simplest
form: the same amount, in the smallest numbers that can name it.

Sometimes it takes more than one step. 12/16: divide by 2 to get 6/8, then by 2 again to get 3/4. Or
divide by 4 at once. Either way ends at 3/4.

## A fraction is a division

Share 2 pies equally among 4 people, and each person gets 2/4 of a pie. Sharing is dividing: 2 ÷ 4 is
2/4. So on the calculator, a fraction is typed as a division.
<entry e="alg">Type it the way it is written, then press ENTER, which works as = here:</entry>
<entry e="rpn">In RPN, type the top, ENTER, the bottom, then ÷:</entry>

```keys Q01 entry=alg
2 ÷ 4 ENTER
```

```keys Q01 entry=rpn
2 ENTER 4 ÷
```

The screen shows <disp v="Q01">0 1/2</disp>.
<entry e="alg">The line you typed stays on the screen above the answer: <disp v="Q01" kind="line">2÷4</disp>.</entry>
The 0 in front means no whole pies, and then 1/2. Fraction display shows a fraction in simplest form
(when it is exact, with no arrow in the status band: start-01), so 2/4 comes out as 1/2. Now type 1/2 itself:

```keys Q02 entry=alg
1 ÷ 2 ENTER
```

```keys Q02 entry=rpn
1 ENTER 2 ÷
```

The screen shows <disp v="Q02">0 1/2</disp>: the same number. Two fractions are equivalent when they
are the same number, and the calculator agrees with the drawing.

## Checking your hand work

By hand, 6/8 was 3/4. The calculator can check it:

```keys Q03 entry=alg
6 ÷ 8 ENTER
```

```keys Q03 entry=rpn
6 ENTER 8 ÷
```

The screen shows <disp v="Q03">0 3/4</disp>. The calculator does not show how to get there. That is
the hand work's job; the calculator checks the answer.

## When hand work is slow

Last month the bakery sold 296 pies, and 111 of them were apple. What fraction were apple, in
simplest form? By hand, that means finding a number that divides both 111 and 296. 2 does not divide
111. 3 divides 111 (111 = 3 × 37), but not 296. It could take a long time to find one. So here, for
once, the calculator goes first:

```keys Q04 entry=alg
111 ÷ 296 ENTER
```

```keys Q04 entry=rpn
111 ENTER 296 ÷
```

The screen shows <disp v="Q04">0 3/8</disp>. So 111/296 = 3/8: exactly 3 pies in every 8 were apple.

Now the hand work can find the number that divides both 111 and 296. Since 111/296 is 3/8, some
number goes into 111 exactly 3 times and into 296 exactly 8 times, so 3 times it is 111. And
111 = 3 × 37, so the number is 37. If that is right, 8 times 37 is 296. Work out
8 × 37 by hand: 8 × 30 = 240 and 8 × 7 = 56, and 240 + 56 = 296. Then check it:

```keys Q05 entry=alg
8 × 37 ENTER
```

```keys Q05 entry=rpn
8 ENTER 37 ×
```

The screen shows <disp v="Q05">296</disp>. Both 111 and 296 divide by 37, and dividing both by it
leaves 3/8. The hand work and the calculator agree.

## Exercises

Do each one by hand first, then check it on the calculator.

1. Write 3/5 as a fraction with a bottom number of 20.
2. Put 18/24 in simplest form.
3. Are 6/15 and 8/20 equivalent? Put each in simplest form to find out.

## Answers

1. 20 is 5 × 4, so multiply the top by 4 as well: 3/5 = 12/20. To check, type your answer. The
   screen shows the fraction in simplest form, so if your answer is right it shows the fraction you
   started with:

   ```keys E01 entry=alg
   12 ÷ 20 ENTER
   ```

   ```keys E01 entry=rpn
   12 ENTER 20 ÷
   ```

   The screen shows <disp v="E01">0 3/5</disp>.

2. Divide the top and the bottom by 6, or by 2 and then by 3: 18/24 = 3/4. The check:

   ```keys E02 entry=alg
   18 ÷ 24 ENTER
   ```

   ```keys E02 entry=rpn
   18 ENTER 24 ÷
   ```

   The screen shows <disp v="E02">0 3/4</disp>.

3. 6/15: divide by 3 to get 2/5. 8/20: divide by 4 to get 2/5. They are equivalent. The checks:

   ```keys E03 entry=alg
   6 ÷ 15 ENTER
   ```

   ```keys E03 entry=rpn
   6 ENTER 15 ÷
   ```

   The screen shows <disp v="E03">0 2/5</disp>, and

   ```keys E03B entry=alg
   8 ÷ 20 ENTER
   ```

   ```keys E03B entry=rpn
   8 ENTER 20 ÷
   ```

   The screen shows <disp v="E03B">0 2/5</disp>: the same.
