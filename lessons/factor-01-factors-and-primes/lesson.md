---
id: factor-01
title: Factors and primes
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation quotient-remainder long-division
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Maren
---

# Factors and primes

Maren has 84 pastries to set out in equal rows. 84 in rows of 2 works, and so do rows of 3; rows of 5
leave some over. The numbers that make equal rows of 84 are its factors. This lesson finds factors by
hand, checks them with Rmdr (whole-02), and meets the primes: the numbers with exactly two different
factors, 1 and themselves.

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Divides, and factors

A number divides another when it goes into it with nothing left over: the remainder is 0. Then it is a
factor of the other number. Three quick tests, done in your head. Each works both ways: if the test
passes, the number divides, and if it fails, it does not.

- **2** divides a whole number exactly when its last digit is even: 0, 2, 4, 6 or 8. (A number that
  ends in 1, 3, 5, 7 or 9 is odd.)
- **5** divides it exactly when its last digit is 0 or 5.
- **3** divides it exactly when its digits add up to a number 3 divides.

84 ends in 4, which is even, so 2 divides 84. Its digits add to 8 + 4 = 12, which 3 divides, so 3
divides 84. It ends in 4, not 0 or 5, so 5 does not. Rmdr checks each one:

```keys R01 entry=alg
BLUE Rmdr 84 GOLD , 2 ▶ ENTER
```

```keys R01 entry=rpn
84 ENTER 2 BLUE Rmdr
```

The screen shows <disp v="R01">0.0000</disp>: no remainder, so 2 is a factor.

```keys R02 entry=alg
BLUE Rmdr 84 GOLD , 3 ▶ ENTER
```

```keys R02 entry=rpn
84 ENTER 3 BLUE Rmdr
```

The screen shows <disp v="R02">0.0000</disp>, and for 5:

```keys R03 entry=alg
BLUE Rmdr 84 GOLD , 5 ▶ ENTER
```

```keys R03 entry=rpn
84 ENTER 5 BLUE Rmdr
```

The screen shows <disp v="R03">4.0000</disp>: 4 over, so 5 is not a factor of 84.

Factors come in pairs that multiply to the number. Testing 1, 2, 3 and so on, 84's pairs are 1 × 84,
2 × 42, 3 × 28, 4 × 21, 6 × 14 and 7 × 12. So Maren can set out 84 pastries in rows of 1, 2, 3, 4, 6,
7, 12, 14, 21, 28, 42 or 84.

## Primes

A prime is a whole number with exactly two different factors, 1 and itself: 2, 3, 5, 7, 11, 13 and so
on. 1 is not a prime, because it has only one factor, itself. Some numbers look prime and are not. 91
is odd; its digits add to 10, which 3 does not divide; and it does not end in 0 or 5. So 2, 3 and 5 do
not divide it. But 7 does:

```keys R04 entry=alg
BLUE Rmdr 91 GOLD , 7 ▶ ENTER
```

```keys R04 entry=rpn
91 ENTER 7 BLUE Rmdr
```

The screen shows <disp v="R04">0.0000</disp>: 91 = 7 × 13, not a prime.

How far must you try? Take a number from 10 to 99, and any of its factor pairs other than 1 and the
number itself, like 7 and 13 for 91. If both of the pair were 10 or more, they would multiply to at
least 10 × 10 = 100, which is too big. So one of them is below 10, and it is enough to try 2, 3, 5 and
7, the primes below 10. 4, 6, 8 and 9 need not be tried: 4 and 8 are made of 2s, 9 of 3s, and 6 of a 2
and a 3, so if 2 and 3 do not divide the number, none of them can. (This is for numbers from 10 up. A
prime below 10, like 7, divides itself: Rmdr of 7 and 7 is 0, and that does not make 7 not prime.)

For 97: it is odd; its digits add to 16, which 3 does not divide; it does not end in 0 or 5. And 7, by
hand (whole-02): 7 goes into 9 once with 2 over, and 27 holds three 7s (21) with 6 over: 13, with 6
over. The check:

```keys R05 entry=alg
BLUE Rmdr 97 GOLD , 7 ▶ ENTER
```

```keys R05 entry=rpn
97 ENTER 7 BLUE Rmdr
```

The screen shows <disp v="R05">6.0000</disp>. None of 2, 3, 5 and 7 divides 97, so 97 is prime.

## Breaking a number into primes

Every whole number above 1 that is not prime can be broken into primes multiplied together, its prime
factorization. Split it into two factors, neither of them 1, then split those, until every piece is
prime. Drawn as a tree, each number splits into two branches:

```
        84
       /  \
      2    42
          /  \
         2    21
             /  \
            3    7
```

- 84 = 2 × 42.
- 42 = 2 × 21, so 84 = 2 × 2 × 21.
- 21 = 3 × 7, so 84 = 2 × 2 × 3 × 7, and 2, 3 and 7 are all prime.

Any first split ends at the same primes: 84 = 4 × 21, and 4 = 2 × 2 and 21 = 3 × 7, so again
2 × 2 × 3 × 7.

Multiply the pieces back together to check:

```keys F01 entry=alg
2 × 2 × 3 × 7 ENTER
```

```keys F01 entry=rpn
2 ENTER 2 × 3 × 7 ×
```

The screen shows <disp v="F01">84.0000</disp>.

## Exercises

1. Does 3 divide 117? Use the test, then check with Rmdr.
2. Find the prime factorization of 60, and check it.
3. Is 89 prime?

## Answers

1. 1 + 1 + 7 = 9, which 3 divides, so yes:

   ```keys E01 entry=alg
   BLUE Rmdr 117 GOLD , 3 ▶ ENTER
   ```

   ```keys E01 entry=rpn
   117 ENTER 3 BLUE Rmdr
   ```

   The screen shows <disp v="E01">0.0000</disp>.

2. 60 = 2 × 30, 30 = 2 × 15, 15 = 3 × 5: 60 = 2 × 2 × 3 × 5. The check:

   ```keys E02 entry=alg
   2 × 2 × 3 × 5 ENTER
   ```

   ```keys E02 entry=rpn
   2 ENTER 2 × 3 × 5 ×
   ```

   The screen shows <disp v="E02">60.0000</disp>.

3. 89 is below 100, so try 2, 3, 5 and 7. It is odd; its digits add to 17, which 3 does not divide; it
   does not end in 0 or 5; and for 7:

   ```keys E03 entry=alg
   BLUE Rmdr 89 GOLD , 7 ▶ ENTER
   ```

   ```keys E03 entry=rpn
   89 ENTER 7 BLUE Rmdr
   ```

   The screen shows <disp v="E03">5.0000</disp>. So 89 is prime.
