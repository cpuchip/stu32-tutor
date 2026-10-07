---
id: num-01
title: Order of operations
status: draft prose (not yet read by a non-author, abacus or Michael)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# Order of operations

When an expression mixes operations, mathematics has an agreed order for them: what is inside
parentheses first, then powers, then multiplication and division, then addition and subtraction.
Multiplication and division share a rank and are done left to right, and so are addition and
subtraction. A minus sign in front of a number counts as a subtraction, so it comes after powers.
So 3 + 4 × 5 is 23: the multiplication comes first. On the STU-32 you do the operations yourself,
one key at a time, so you choose the order. This lesson is about choosing it.

## Before you start

The setup from rpn-01: 33s mode and FIX 4. Each example below is written out in full from it.

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

Squaring is x² (gold, above √x).

## Multiplication before addition

For 3 + 4 × 5 the multiplication comes first. Type the 3 and let it wait on the stack, then do 4 ×
5, and add last:

```keys N01
3 ENTER 4 ENTER 5 × +
```

X shows <disp v="N01">23.0000</disp>. Stop just before the × and look at the stack:

```keys N01A
3 ENTER 4 ENTER 5
```

X holds 5, Y holds 4 and Z holds 3. The × uses the 4 and the 5 while the 3 waits in Z. When ×
finishes, the stack drops and the 3 comes down to Y for the +.

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
(12 − 4) ÷ (5 − 3), work out the top, then the bottom, then divide:

```keys N05
12 ENTER 4 − 5 ENTER 3 − ÷
```

X holds 4. Just before the bottom's −, the stack holds the 8 from the top in Z:

```keys N05A
12 ENTER 4 − 5 ENTER 3
```

X holds 3, Y holds 5 and Z holds 8. When − finishes the bottom, the stack drops and the 8 comes
back down to Y for the ÷.

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

X shows <disp v="N08">77.0000</disp>. When you typed the 1, all four levels were full: 2 in T, 3 in
Z, 4 in Y and 1 in X. Each two-number operation (+ and ×) used X and Y and dropped the stack, so
the 2 moved down one level each time, from T to Z to Y, while T kept a copy; x² used X alone and
moved nothing. That is why the 2 is in Y for the last +.

Four levels is the limit. If you press ENTER after the 1, the stack pushes up once more and the 2
falls off the top:

```keys N08B
2 ENTER 3 ENTER 4 ENTER 1 ENTER
```

X and Y hold 1, Z holds 4 and T holds 3. The 2 is gone, and the + at the end would have nothing to
add it to.

The other way is to start from the inside, the (4 + 1), and work outward. It never needs more than
two levels:

```keys N09
4 ENTER 1 + GOLD x² 3 × 2 +
```

X holds 77 again. Working from the inside out does not depend on how many numbers the stack can
hold, so it is the habit to build.

It has one catch. With + and × the order of the two numbers does not matter, but with − and ÷ it
does. Take 20 − 3 × 4 from the inside out: work out 3 × 4, then type the 20. Now the 20 is in X
and the 12 in Y, the wrong way round for 20 − 12. Press x↔y before the − to put them right:

```keys N10
3 ENTER 4 × 20 x↔y −
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
