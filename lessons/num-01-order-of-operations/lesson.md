---
id: num-01
title: Order of operations
requires: setup shift-keys rpn-arithmetic enter-copies stack-lift stack-levels swap-roll t-copies-down
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Order of operations

When an expression mixes operations, mathematics has an agreed order for them: what is inside
parentheses first, then powers, then multiplication and division, then addition and subtraction.
Multiplication and division share a rank and are done left to right, and so are addition and
subtraction. A minus sign in front of a number is applied after powers: −3² is the negative of 3².
So 3 + 4 × 5 is 23: the multiplication comes first. On the STU-32 you do the operations yourself,
one key at a time, so you choose the order. This lesson is about choosing it.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each example below is written out in full from it.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

Squaring is x² (gold, above √x).

## Multiplication before addition

For 3 + 4 × 5 the multiplication comes first. Type the 3 and let it wait on the stack, then type
the 4 and the 5, and stop before the × to look at the stack:

```keys N01A
3 ENTER 4 ENTER 5
```

X holds 5, Y holds 4 and Z holds 3. Now press × and then +:

```keys N01 after=N01A
× +
```

X shows <disp v="N01">23.0000</disp>. The × used the 4 and the 5 while the 3 waited in Z. When ×
finished, the stack dropped and the 3 came down to Y for the +.

You can also start with the multiplication and bring the 3 in last:

```keys N01B
4 ENTER 5 × 3 +
```

X holds 23 again. This second way, working from the inside out, comes back at the end of the
lesson.

## Parentheses first

Parentheses tell you to do their inside before anything else. For (6 + 2) ÷ 4, add first:

```keys N02
6 ENTER 2 + 4 ÷
```

X holds 2.

## Powers before multiplication

In 2 × 3², the power belongs to the 3 alone, so square the 3 before multiplying:

```keys N03
2 ENTER 3 GOLD x² ×
```

X holds 18. If the whole product is squared, written (2 × 3)², multiply first and then square:

```keys N04
2 ENTER 3 × GOLD x²
```

X holds 36. The numbers and the operations are the same as before; only their order differs.

## A fraction: top, bottom, then divide

A fraction bar works like a pair of parentheses around the top and another around the bottom. For
(12 − 4) ÷ (5 − 3), work out the top, then type the bottom's two numbers, and stop:

```keys N05A
12 ENTER 4 − 5 ENTER 3
```

X holds 3, Y holds 5 and Z holds the 8 from the top. Now press − to finish the bottom, and ÷:

```keys N05 after=N05A
− ÷
```

X holds 4. When − finished the bottom, the stack dropped and the 8 came back down to Y for the ÷.

## A minus sign and a power

The expression −3² means the negative of 3², which is −9: the power comes before the minus sign.
Square first, then change the sign. The +/− key changes the sign of a finished result in X as well
as of a number you are typing:

```keys N06
3 GOLD x² +/−
```

X shows <disp v="N06">-9.0000</disp>. If the minus belongs to the 3, the expression is written
(−3)², and the answer is 9. Change the sign first, then square:

```keys N07
3 +/− GOLD x²
```

X shows <disp v="N07">9.0000</disp>. The same two operations, in the other order, give the other
reading.

## Two ways through a longer one

Take 2 + 3 × (4 + 1)². You can type the numbers from left to right and let them wait, as long as
they fit in the four levels:

```keys N08
2 ENTER 3 ENTER 4 ENTER 1 + GOLD x² × +
```

X shows <disp v="N08">77.0000</disp>. Stop after typing the 1, and all four levels are full:

```keys N08S
2 ENTER 3 ENTER 4 ENTER 1
```

T holds 2, Z holds 3, Y holds 4 and X holds 1. Each two-number operation (+ and ×) uses X and Y
and drops the stack, so the 2 moves down one level each time, from T to Z to Y, while T keeps a
copy; x² uses X alone and moves nothing. Carry on, and stop again just before the last +:

```keys N08T after=N08S
+ GOLD x² ×
```

X holds 75 and Y holds 2, ready for the +.

Four levels is the limit. If you press ENTER after the 1, the stack pushes up once more and the 2
falls off the top:

```keys N08B
2 ENTER 3 ENTER 4 ENTER 1 ENTER
```

X and Y hold 1, Z holds 4 and T holds 3. The 2 is gone. Carry on with the rest of the keys as if
nothing had happened:

```keys N08C after=N08B
+ GOLD x² × +
```

X shows <disp v="N08C">19.0000</disp>. The last + found a leftover 3 where the 2 should have been,
and gave a wrong answer with no error to warn you.

The other way is to start from the inside, the (4 + 1), and work outward. It never needs more than
two levels:

```keys N09
4 ENTER 1 + GOLD x² 3 × 2 +
```

X holds 77 again. Working from the inside out does not depend on how many numbers the stack can
hold, so it is the habit to build.

It has one catch. With + and × the order of the two numbers does not matter, but with − and ÷ it
does. Take 20 − 3 × 4 from the inside out: work out 3 × 4, then type the 20.

```keys N10S
3 ENTER 4 × 20
```

Now the 20 is in X and the 12 in Y, the wrong way round for 20 − 12. Carry on: press x↔y to put
them right, then −:

```keys N10 after=N10S
x↔y −
```

X holds 8. Without the x↔y, the − works Y minus X, which is 12 − 20:

```keys N10A
3 ENTER 4 × 20 −
```

X shows <disp v="N10A">-8.0000</disp>, with no error to warn you.

## Exercises

1. Work out 5 + 6 × 2.
2. Work out (9 − 3)² ÷ 4.
3. Work out 4 × 3² − 10.
4. Work out 50 − 2 × 3² from the inside out.

## Answers

1. 17. The 6 × 2 first, with the 5 waiting:

   ```keys E01
   5 ENTER 6 ENTER 2 × +
   ```

2. 9. The parentheses, then the square, then the division:

   ```keys E02
   9 ENTER 3 − GOLD x² 4 ÷
   ```

3. 26. The square, then the multiplication, then the subtraction:

   ```keys E03
   4 ENTER 3 GOLD x² × 10 −
   ```

4. 32. The square, then the multiplication, then the 50 and x↔y, then the subtraction:

   ```keys E04
   3 GOLD x² 2 × 50 x↔y −
   ```
