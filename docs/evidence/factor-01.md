# factor-01 evidence: factors and primes (pre-algebra unit 3)

## Expected values

Oracle: build/proto/factor01.py. Asserted: the tests for 2, 3 and 5 against true remainders for every
n below 2000, both ways; 84's full factor list and its pairs; 91 = 7 × 13; the "try 2, 3, 5, 7" rule
against trial division for every n from 10 to 99; that 4, 8, 9 and 6 add nothing once 2 and 3 fail;
97 ÷ 7 by hand (13 r 6); both factor trees of 84 to the same primes; the exercises (117 by 3, 60's
factorization, 89 prime). 9 examples in both entries, 9 display vectors.

## Non-author read (2026-10-09)

All arithmetic correct. Taken: "try 2, 3, 5 and 7" would call 7 itself not prime (Rmdr 7, 7 is 0):
now for numbers from 10 to 99, and the number itself not tried; the pair 1 × n excluded from the
argument; 4, 6, 8 and 9 explained (made of 2s and 3s); the tests stated "exactly when", since the
lesson uses them both ways; 84's factors listed, answering the opening; a prime has exactly two
different factors, so 1 is not one; a factor tree splits off no 1, is drawn, and any start ends at the
same primes; 97 ÷ 7 by hand before Rmdr; each digit-sum test carried to its conclusion; "odd"
defined; "and so on".

## Checks

make check at be3617e, both entries, the student run in order. Controls (4): a remainder misquoted as
0; Rmdr without its blue shift; a factor left out of the check; RPN's Rmdr with the numbers swapped.
All red.
