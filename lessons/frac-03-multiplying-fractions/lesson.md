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
voices: story plain
---

# Multiplying and dividing fractions

<voice v="story">On Monday, Maren has $\frac{3}{4}$ of a pan of fudge left, and a customer from across Thornwick buys half of it. What fraction of the
pan is that? On Tuesday, with $\frac{3}{4}$ of another pan, she cuts pieces of $\frac{3}{8}$ pan each: how many pieces?</voice><voice v="plain">$\frac{3}{4}$ of a pan of fudge is left, and a customer buys half of it. What fraction of the
pan is that? From $\frac{3}{4}$ of another pan, pieces of $\frac{3}{8}$ pan each are cut: how many pieces?</voice>
The first is multiplying fractions, the second dividing them. Neither needs a common bottom, though one
can help to picture dividing.

## From before

```item FR3F1
prompt: Write $\frac{3}{8}$ as a decimal.
topics: fraction-is-division
answer: type
calculator: no
slip: FR3F1A | wrote the digits, not the division | $\frac{3}{8}$ is $3 ÷ 8$.
```

```item FR3F2
prompt: Write $\frac{2}{5}$ with a bottom of 15. What is the top?
topics: equivalent-fractions
answer: type
calculator: no
slip: FR3F2A | added instead of multiplying | Top and bottom are multiplied alike: $5 × 3$ is 15, so the top is $2 × 3$.
```

## Before you start

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC
```

## Multiplying

With whole numbers, half of 6 is 3, and $\frac{1}{2} × 6 = 3$: taking a fraction "of" something is multiplying
by it. So half of $\frac{3}{4}$ is $\frac{1}{2} × \frac{3}{4}$. Picture the pan cut into quarters, with 3 quarters left. Halve each
quarter: the 4 quarters, each cut in 2, make $2 × 4 = 8$ pieces in the pan, eighths. Half of the fudge
is one piece from each of the 3 quarters: $1 × 3 = 3$ of those eighths. So $\frac{1}{2} × \frac{3}{4} = \frac{3}{8}$. That is the
rule: multiply the tops, and multiply the bottoms. $\frac{1}{2} × \frac{3}{4} = \frac{1 × 3}{2 × 4} = \frac{3}{8}$. The answer is
smaller than $\frac{3}{4}$, as half of any amount is: multiplying a positive number by a fraction less than 1
makes it smaller.

```keys M01 entry=alg
1 ÷ 2 × 3 ÷ 4 ENTER
```

```keys M01 entry=rpn
1 ENTER 2 ÷ 3 ENTER 4 ÷ ×
```

The screen shows <disp v="M01">0 3/8</disp>.
<entry e="alg">The line reads <disp v="M01" kind="line">1÷2×3÷4</disp>. × and ÷ are worked left to right:
$(1 ÷ 2) × 3$, then ÷ 4. Times 3 and then divided by 4 is the same as times $\frac{3}{4}$, so no brackets are
needed here.</entry>

Another: $\frac{5}{8} × \frac{4}{5} = \frac{5 × 4}{8 × 5} = \frac{20}{40}$, which in simplest form is $\frac{1}{2}$.

```keys M02 entry=alg
5 ÷ 8 × 4 ÷ 5 ENTER
```

```keys M02 entry=rpn
5 ENTER 8 ÷ 4 ENTER 5 ÷ ×
```

The screen shows <disp v="M02">0 1/2</disp>.

## Dividing

$\frac{3}{4} ÷ \frac{3}{8}$ asks how many pieces of $\frac{3}{8}$ fit in $\frac{3}{4}$. In eighths, $\frac{3}{4}$ is $\frac{6}{8}$, and 6 eighths hold two
pieces of 3 eighths: 2. There is a shortcut that works for dividing by any fraction but 0 (you can't divide by 0): dividing by
a fraction is multiplying by it flipped, its top and bottom swapped. $\frac{3}{4} ÷ \frac{3}{8} = \frac{3}{4} × \frac{8}{3} = \frac{24}{12} = 2$. Why: a whole pan is 8
eighths, and each piece is 3 eighths, so a whole pan holds $8 ÷ 3 = \frac{8}{3}$ pieces ($2 \frac{2}{3}$). $\frac{3}{4}$ of a pan
holds $\frac{3}{4}$ of that many, and "of" is times: $\frac{3}{4} × \frac{8}{3}$.

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

```why
ask: Why does $\frac{3}{4} ÷ \frac{3}{8}$ give 2?
because: $\frac{3}{4}$ is twice $\frac{3}{8}$: two pieces of $\frac{3}{8}$ make $\frac{3}{4}$.
```

<entry e="alg">The line reads <disp v="D01" kind="line">3÷4÷(3÷8)</disp>. Without the brackets, the line
would work left to right, $3 ÷ 4$, then ÷ 3, then ÷ 8. Dividing by 3 and then by 8 is dividing by 24,
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

1. $\frac{2}{5} × \frac{1}{4}$.
2. $\frac{7}{8} ÷ \frac{1}{4}$.
3. How many pieces of $\frac{1}{8}$ are in $\frac{1}{2}$?

## Answers

1. $\frac{2 × 1}{5 × 4} = \frac{2}{20}$, which in simplest form is $\frac{1}{10}$.

   ```keys E01 entry=alg
   2 ÷ 5 × 1 ÷ 4 ENTER
   ```

   ```keys E01 entry=rpn
   2 ENTER 5 ÷ 1 ENTER 4 ÷ ×
   ```

   The screen shows <disp v="E01">0 1/10</disp>.

2. Flip $\frac{1}{4}$ to $\frac{4}{1}$, which is 4: $\frac{7}{8} × 4 = \frac{28}{8}$. 8 goes into 28 three times with 4 left over, so
   $\frac{28}{8} = 3 \frac{4}{8} = 3 \frac{1}{2}$.

   ```keys E02 entry=alg
   7 ÷ 8 ÷ () 1 ÷ 4 ▶ ENTER
   ```

   ```keys E02 entry=rpn
   7 ENTER 8 ÷ 1 ENTER 4 ÷ ÷
   ```

   The screen shows <disp v="E02">3 1/2</disp>.

3. $\frac{1}{2} ÷ \frac{1}{8} = \frac{1}{2} × 8 = 4$: four eighths in a half.

   ```keys E03 entry=alg
   1 ÷ 2 ÷ () 1 ÷ 8 ▶ ENTER
   ```

   ```keys E03 entry=rpn
   1 ENTER 2 ÷ 1 ENTER 8 ÷ ÷
   ```

   The screen shows <disp v="E03">4</disp>.

## Mixed review

```item FR3M1
prompt: Work out $\frac{3}{4} × \frac{2}{3}$, as a decimal.
topics: multiply-fractions
answer: type
calculator: no
slip: FR3M1A | multiplied crosswise | Multiply straight across: tops times tops and bottoms times bottoms: $\frac{6}{12}$, which is $\frac{1}{2}$.
```

```item FR3M2
prompt: Put $\frac{12}{16}$ in simplest form. What is its top?
topics: simplest-form
answer: type
calculator: no
slip: FR3M2A | stopped too soon | $\frac{6}{8}$ still shares a 2: divide top and bottom by 4, to $\frac{3}{4}$.
```

```item FR3M3
prompt: How many pieces of $\frac{1}{4}$ are in 3?
topics: divide-fractions
answer: type
calculator: no
slip: FR3M3A | multiplied by 1/4 | Dividing by $\frac{1}{4}$ asks how many quarters fit: 4 in each whole, so $3 × 4$.
```

```item FR3M4
prompt: A bar is cut into 8 equal pieces and 3 are eaten. What fraction is left, as a decimal?
topics: fraction-parts
answer: type
calculator: no
slip: FR3M4A | the part eaten, not the part left | $8 − 3$ is 5 pieces left: $\frac{5}{8}$.
```

## Checkpoint

Questions on the whole unit.

```item CPP5A
prompt: Put $\frac{18}{24}$ in simplest form. What is its bottom number?
topics: simplest-form
answer: type
calculator: no
slip: CPP5A1 | divided by 2 only | $\frac{9}{12}$ is simpler, but 9 and 12 still share a 3. Divide top and bottom by the greatest common factor, 6.
slip: CPP5A2 | divided by 3 only | $\frac{6}{8}$ is simpler, but 6 and 8 still share a 2. Divide top and bottom by the greatest common factor, 6.
```

```item CPP5B
prompt: Work out $\frac{2}{3} + \frac{1}{4}$. Written with a bottom number of 12, what is its top?
topics: common-bottom
answer: type
calculator: no
slip: CPP5B1 | added the tops and the bottoms | Fractions add only when their pieces are the same size: make both twelfths first, $\frac{2}{3} = \frac{8}{12}$ and $\frac{1}{4} = \frac{3}{12}$.
slip: CPP5B2 | changed only one top | $\frac{1}{4}$ as twelfths is $\frac{3}{12}$: multiply its top by 3 as well as its bottom.
```

```item CPP5C
prompt: How many pieces of $\frac{3}{8}$ are in $\frac{3}{4}$?
topics: divide-fractions
answer: type
calculator: no
slip: CPP5C1 | multiplied instead of dividing | "How many fit" is a division: $\frac{3}{4} ÷ \frac{3}{8}$, which is $\frac{3}{4} × \frac{8}{3}$.
slip: CPP5C2 | flipped the wrong fraction | Keep the first fraction and flip the one you divide by: $\frac{3}{4} × \frac{8}{3}$.
```
