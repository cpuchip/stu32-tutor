---
id: frac-03
title: Multiplying and dividing fractions
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation calc-frac-display fraction-is-division equivalent-fractions simplest-form
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
display: FIX 4
cast: Maren
---

# Multiplying and dividing fractions

On Monday, Maren has 3/4 of a pan of fudge left, and a customer buys half of it. What fraction of the
pan is that? On Tuesday, with 3/4 of another pan, she cuts pieces of 3/8 pan each: how many pieces?
The first is multiplying fractions, the second dividing them. Neither needs a common bottom, though one
can help to picture dividing.

## Before you start

The setup from start-01, with →FRAC at the end, as in frac-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
```

## Multiplying

With whole numbers, half of 6 is 3, and 1/2 × 6 = 3: taking a fraction "of" something is multiplying
by it. So half of 3/4 is 1/2 × 3/4. Picture the pan cut into quarters, with 3 quarters left. Halve each
quarter: the 4 quarters, each cut in 2, make 2 × 4 = 8 pieces in the pan, eighths. Half of the fudge
is one piece from each of the 3 quarters: 1 × 3 = 3 of those eighths. So 1/2 × 3/4 = 3/8. That is the
rule: multiply the tops, and multiply the bottoms. 1/2 × 3/4 = (1 × 3)/(2 × 4) = 3/8. The answer is
smaller than 3/4, as half of anything is: multiplying by a fraction less than 1 makes a number
smaller.

```keys M01 entry=alg
1 ÷ 2 × 3 ÷ 4 ENTER
```

```keys M01 entry=rpn
1 ENTER 2 ÷ 3 ENTER 4 ÷ ×
```

The screen shows <disp v="M01">0 3/8</disp>.
<entry e="alg">The line reads <disp v="M01" kind="line">1÷2×3÷4</disp>. × and ÷ are worked left to right:
(1 ÷ 2) × 3, then ÷ 4. Times 3 and then divided by 4 is the same as times 3/4, so no brackets are
needed here.</entry>

Another: 5/8 × 4/5 = (5 × 4)/(8 × 5) = 20/40, which in simplest form is 1/2.

```keys M02 entry=alg
5 ÷ 8 × 4 ÷ 5 ENTER
```

```keys M02 entry=rpn
5 ENTER 8 ÷ 4 ENTER 5 ÷ ×
```

The screen shows <disp v="M02">0 1/2</disp>.

## Dividing

3/4 ÷ 3/8 asks how many pieces of 3/8 fit in 3/4. In eighths, 3/4 is 6/8, and 6 eighths hold two
pieces of 3 eighths: 2. There is a shortcut that always works: dividing by a fraction is multiplying
by it flipped, its top and bottom swapped. 3/4 ÷ 3/8 = 3/4 × 8/3 = 24/12 = 2. Why: a whole pan is 8
eighths, and each piece is 3 eighths, so a whole pan holds 8 ÷ 3 = 8/3 pieces (2 2/3). 3/4 of a pan
holds 3/4 of that many, and "of" is times: 3/4 × 8/3.

On the calculator the second fraction must be kept together:
<entry e="alg">the soft key () types a pair of brackets (also called parentheses), and ▶ steps out of
them:</entry><entry e="rpn">each fraction is worked out first, then ÷ divides them:</entry>

```keys D01 entry=alg
3 ÷ 4 ÷ () 3 ÷ 8 ▶ ENTER
```

```keys D01 entry=rpn
3 ENTER 4 ÷ 3 ENTER 8 ÷ ÷
```

The screen shows <disp v="D01">2</disp>: two pieces.
<entry e="alg">The line reads <disp v="D01" kind="line">3÷4÷(3÷8)</disp>. Without the brackets, the line
would work left to right, 3 ÷ 4, then ÷ 3, then ÷ 8. Dividing by 3 and then by 8 is dividing by 24,
when it should have been times 8 and divided by 3:</entry><entry e="rpn">In RPN there is no bracket to
forget, but dividing step by step, by 3 and then by 8, is the same mistake as on a line without
brackets: it divides by 24, when it should have been times 8 and divided by 3:</entry>

```keys D02 entry=alg
3 ÷ 4 ÷ 3 ÷ 8 ENTER
```

```keys D02 entry=rpn
3 ENTER 4 ÷ 3 ÷ 8 ÷
```

<entry e="alg">The screen shows <disp v="D02">0 1/32</disp>, a different question's answer.</entry><entry e="rpn">The
screen shows <disp v="D02">0 1/32</disp>: dividing by 3 and then by 8 is a different question.</entry>

## Exercises

By hand first, then check.

1. 2/5 × 1/4.
2. 7/8 ÷ 1/4.
3. How many pieces of 1/8 are in 1/2?

## Answers

1. (2 × 1)/(5 × 4) = 2/20, which in simplest form is 1/10.

   ```keys E01 entry=alg
   2 ÷ 5 × 1 ÷ 4 ENTER
   ```

   ```keys E01 entry=rpn
   2 ENTER 5 ÷ 1 ENTER 4 ÷ ×
   ```

   The screen shows <disp v="E01">0 1/10</disp>.

2. Flip 1/4 to 4/1, which is 4: 7/8 × 4 = 28/8. 8 goes into 28 three times with 4 left over, so
   28/8 = 3 4/8 = 3 1/2.

   ```keys E02 entry=alg
   7 ÷ 8 ÷ () 1 ÷ 4 ▶ ENTER
   ```

   ```keys E02 entry=rpn
   7 ENTER 8 ÷ 1 ENTER 4 ÷ ÷
   ```

   The screen shows <disp v="E02">3 1/2</disp>.

3. 1/2 ÷ 1/8 = 1/2 × 8 = 4: four eighths in a half.

   ```keys E03 entry=alg
   1 ÷ 2 ÷ () 1 ÷ 8 ▶ ENTER
   ```

   ```keys E03 entry=rpn
   1 ENTER 2 ÷ 1 ENTER 8 ÷ ÷
   ```

   The screen shows <disp v="E03">4</disp>.
