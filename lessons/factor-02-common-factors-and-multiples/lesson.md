---
id: factor-02
title: Common factors and multiples
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation quotient-remainder divides prime prime-factorization
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Maren, Tobin
---

# Common factors and multiples

Maren has 84 apple tarts and 90 cherry tarts to pack. Every box must hold the same number of tarts,
all of one kind, with none left over. What is the biggest box that works for both? And Tobin delivers
to the mill every 12 days and to the inn every 18 days: if he goes to both today, when will he next
go to both on the same day? Common means shared: the first is a factor both numbers share, and the
second a multiple both share. Both come from the prime factorizations of factor-01.

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## The greatest common factor

A box size works when it divides both 84 and 90. The biggest such number is their greatest common
factor (GCF). Find it from the prime factorizations:

- 84 = 2 × 2 × 3 × 7 (factor-01).
- 90 = 2 × 3 × 3 × 5 (90 = 2 × 45, 45 = 3 × 15, 15 = 3 × 5).

The primes both have are one 2 and one 3. For each prime, take it the smaller number of times it
appears: 84 has two 2s and 90 has one, so one 2; each has a 3 (90 has two), so one 3; 5 and 7 are not
in both. So the GCF is 2 × 3 = 6, and 6 sits inside both: 84 = (2 × 3) × (2 × 7) and
90 = (2 × 3) × (3 × 5). Boxes of 6. Check that 6 divides each:

```keys G01 entry=alg
BLUE Rmdr 84 GOLD , 6 ▶ ENTER
```

```keys G01 entry=rpn
84 ENTER 6 BLUE Rmdr
```

The screen shows <disp v="G01">0.0000</disp>, and for 90:

```keys G02 entry=alg
BLUE Rmdr 90 GOLD , 6 ▶ ENTER
```

```keys G02 entry=rpn
90 ENTER 6 BLUE Rmdr
```

The screen shows <disp v="G02">0.0000</disp>. How many boxes of each?

```keys G03 entry=alg
GOLD INT÷ 84 GOLD , 6 ▶ ENTER
```

```keys G03 entry=rpn
84 ENTER 6 GOLD INT÷
```

The screen shows <disp v="G03">14.0000</disp> boxes of apple, and

```keys G04 entry=alg
GOLD INT÷ 90 GOLD , 6 ▶ ENTER
```

```keys G04 entry=rpn
90 ENTER 6 GOLD INT÷
```

<disp v="G04">15.0000</disp> of cherry. To check by hand that 6 really is the greatest, list the factors
of each (by their pairs, as in factor-01). 84: 1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84. 90: 1, 2, 3, 5,
6, 9, 10, 15, 18, 30, 45, 90. The ones in both lists are 1, 2, 3 and 6, and the greatest is 6.

## The least common multiple

The multiples of 12 are 12 × 1, 12 × 2, 12 × 3 and so on: 12, 24, 36, 48. Call today day 0. Tobin
goes to the mill on day 12, 24, 36, and to the inn on day 18, 36, 54. The first day on both lists is
36: the least common multiple (LCM) of 12 and 18. From the prime factorizations:

- 12 = 2 × 2 × 3.
- 18 = 2 × 3 × 3.

A multiple of 12 needs two 2s and a 3; a multiple of 18 needs a 2 and two 3s. For the LCM, take each
prime the larger number of times it appears (the GCF took the smaller): two 2s and two 3s:

```keys M01 entry=alg
2 × 2 × 3 × 3 ENTER
```

```keys M01 entry=rpn
2 ENTER 2 × 3 × 3 ×
```

The screen shows <disp v="M01">36.0000</disp>. Check that 12 and 18 both divide it:

```keys M02 entry=alg
BLUE Rmdr 36 GOLD , 12 ▶ ENTER
```

```keys M02 entry=rpn
36 ENTER 12 BLUE Rmdr
```

The screen shows <disp v="M02">0.0000</disp>, and

```keys M03 entry=alg
BLUE Rmdr 36 GOLD , 18 ▶ ENTER
```

```keys M03 entry=rpn
36 ENTER 18 BLUE Rmdr
```

shows <disp v="M03">0.0000</disp>. Tobin's two rounds meet again 36 days from today.

## Exercises

1. Find the GCF of 24 and 36, and check that it divides both.
2. Find the LCM of 4 and 10, and check it by listing multiples.
3. Find the LCM of 6 and 8, and check it by listing multiples.
4. Find the GCF and the LCM of 8 and 15.

## Answers

1. 24 = 2 × 2 × 2 × 3 and 36 = 2 × 2 × 3 × 3. Both have two 2s and one 3: GCF = 2 × 2 × 3 = 12. The
   check:

   ```keys E01 entry=alg
   BLUE Rmdr 36 GOLD , 12 ▶ ENTER
   ```

   ```keys E01 entry=rpn
   36 ENTER 12 BLUE Rmdr
   ```

   The screen shows <disp v="E01">0.0000</disp>, and for 24:

   ```keys E01B entry=alg
   BLUE Rmdr 24 GOLD , 12 ▶ ENTER
   ```

   ```keys E01B entry=rpn
   24 ENTER 12 BLUE Rmdr
   ```

   shows <disp v="E01B">0.0000</disp>.

2. 4 = 2 × 2 and 10 = 2 × 5. The LCM takes two 2s and a 5. Listing: 4, 8, 12, 16, 20 and 10, 20 meet
   first at 20:

   ```keys E02 entry=alg
   2 × 2 × 5 ENTER
   ```

   ```keys E02 entry=rpn
   2 ENTER 2 × 5 ×
   ```

   The screen shows <disp v="E02">20.0000</disp>.

3. 6 = 2 × 3 and 8 = 2 × 2 × 2. The LCM takes three 2s and a 3. Listing: 6, 12, 18, 24 and 8, 16, 24
   meet first at 24:

   ```keys E03 entry=alg
   2 × 2 × 2 × 3 ENTER
   ```

   ```keys E03 entry=rpn
   2 ENTER 2 × 2 × 3 ×
   ```

   The screen shows <disp v="E03">24.0000</disp>.

4. 8 = 2 × 2 × 2 and 15 = 3 × 5 have no prime in common, so their GCF is 1: they share no factor but 1.
   The LCM takes every prime of both: 2 × 2 × 2 × 3 × 5, which is 8 × 15:

   ```keys E04 entry=alg
   8 × 15 ENTER
   ```

   ```keys E04 entry=rpn
   8 ENTER 15 ×
   ```

   The screen shows <disp v="E04">120.0000</disp>.
