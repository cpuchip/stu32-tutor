---
id: seq-01
title: Sequences and sums
requires: setup shift-keys rpn-arithmetic stack-lift mult-before-add fraction-bar stack-full power sto rcl sto-arithmetic letter-keys program-entry xeq-program loop growth
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Sequences and sums

A sequence is a list of numbers in order: a first term, a second, a third, and so on. Many follow a
rule. In 20, 22, 24, 26, … each term is the one before plus 2; in 3, 6, 12, 24, … each term is the one
before times 2. This lesson finds any term of such a sequence without writing out all the terms
before it, and adds up many terms at once.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each example starts fresh, except where one says
it carries on. The last section enters a program, as in fn-01, with a loop as in fn-02.

<mode m="35s,STU">In this mode XEQ and GTO wait, after the label's letter, for ENTER; the keys below
show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Arithmetic sequences

A sequence that adds the same number at every step is arithmetic, and the number it adds is its
common difference, d. A theatre has 20 seats in its first row and 2 more in each row behind. Row 2
has 20 + 2, row 3 has 20 + 2 + 2, and row n has 20 plus n − 1 steps of 2: the first term plus
(n − 1) times d. Row 15 has 20 + 14 × 2:

```keys A01
20 ENTER 14 ENTER 2 × +
```

X shows <disp v="A01">48.0000</disp> seats.

How many seats in all 15 rows? Write the sum forwards and backwards, one under the other:

    20 + 22 + 24 + … + 44 + 46 + 48
    48 + 46 + 44 + … + 24 + 22 + 20

Each column adds to 68, the first term plus the last, and there are 15 columns. So the two lines
together are 15 × 68, and the sum is half of that: 15 × (20 + 48) ÷ 2. In general, the sum of the
first n terms of an arithmetic sequence is n times (the first term plus the last), divided by 2:

```keys A02
15 ENTER 20 ENTER 48 + × 2 ÷
```

X shows <disp v="A02">510.0000</disp> seats.

## Geometric sequences

A sequence that multiplies by the same number at every step is geometric, and the number is its
common ratio, r: exp-01's growth by a factor is a geometric sequence. A colony of cells starts with 3
and doubles every hour: 3, 6, 12, 24, …. The nth term is n − 1 steps after the first, so it is the
first term multiplied by r once for each of those steps: 3 × 2ⁿ⁻¹. (exp-01 counted its steps from the
start, a × bⁿ after n steps; here the first term is the start, so the nth is n − 1 steps on.) The 10th:

```keys G01
3 ENTER 2 ENTER 9 yˣ ×
```

X shows <disp v="G01">1,536.0000</disp>.

The sum of the first n terms of a geometric sequence has a trick of its own. Call the sum of the
first 10 terms S: S = 3 + 6 + 12 + … + 1536. Twice S is 6 + 12 + … + 1536 + 3072: each term of S
doubled is the term after it, so it is the same list without the first term and with one more at the
end. So 2S − S takes away every term the two share, leaving 3072 − 3, and 3072 is 3 × 2¹⁰, so
S = 3 × (2¹⁰ − 1). With any ratio r, the same steps take rS − S, which is (r − 1)S, so dividing by
r − 1: the sum of the first n terms is the first term times (rⁿ − 1), divided by r − 1. That needs r
not to be 1; with r = 1 every term is the same, and the sum is n times the first. Here r − 1 is 1:

```keys G02
3 ENTER 2 ENTER 10 yˣ 1 − × 2 ENTER 1 − ÷
```

X shows <disp v="G02">3,069.0000</disp>.

## Checking a sum with a loop

A formula is quicker, but adding the terms one by one is a check that needs no sum formula. Program Z
adds the theatre's 15 rows. It keeps the total in the variable T (on 8), and a counter in I (on R↓)
as fn-02's loop kept its counter: 1.015 counts from 1 up to and including 15. Z is on the 2 key and
its loop label, W, on 5:

```keys P01A
GOLD PRGM PRGM GOLD LBL Z 0 STO T 1.015 STO I
```

Each time round, the loop takes the row number k from the counter's whole part and works out row k's
seats. The rule from above, 20 + (k − 1) × 2, is 20 + 2k − 2, which is 18 + 2k, fewer keys. It adds
them to T with STO + (rpn-02). Then ISG counts on and GTO goes back to W; once the count passes 15,
ISG skips the GTO, as in fn-02, and RCL T brings the total to X:

```keys P01B after=P01A
GOLD LBL W RCL I BLUE POW IP 2 × 18 + STO + T BLUE ISG I GOLD GTO W RCL T BLUE RTN
```
```keys P01B after=P01A mode=35s,STU
GOLD LBL W RCL I BLUE POW IP 2 × 18 + STO + T BLUE ISG I GOLD GTO W ENTER RCL T BLUE RTN
```

The X line shows <disp v="P01B" kind="program">W012 RTN</disp>: W's twelfth line. If it shows another
number, a key was missed or doubled; fn-01 showed how to step back and fix a line. Turn program entry
off and run it:

```keys P01 after=P01B
GOLD PRGM PRGM
```

```keys P02 after=P01
XEQ Z
```
```keys P02 after=P01 mode=35s,STU
XEQ Z ENTER
```

X shows <disp v="P02">510.0000</disp>, the sum the formula gave.

## Exercises

1. The sequence 7, 11, 15, 19, … goes on adding 4. Find its 30th term, then the sum of its first 30
   terms.
2. A ball dropped from 2 metres bounces back to three quarters of the height it fell from. How high
   does it rise after the 5th bounce?
3. One grain of rice on the first square of a board, 2 on the second, 4 on the third, doubling each
   time. How many grains on the first 10 squares together?

## Answers

1. 123, and 1950. The 30th term is 7 + 29 × 4:

   ```keys E01
   7 ENTER 29 ENTER 4 × +
   ```

   X shows <disp v="E01">123.0000</disp>. Carrying on, with the last term in X, the sum is
   (123 + 7) × 30 ÷ 2:

   ```keys E01B after=E01
   7 + 30 × 2 ÷
   ```

   X shows <disp v="E01B">1,950.0000</disp>.

2. About 0.47 metres. The heights the ball rises to are geometric: the first term is the first
   bounce's, 2 × 0.75 = 1.5, and r = 0.75. The 5th term is 1.5 × 0.75⁴, which is 2 × 0.75 × 0.75⁴,
   that is 2 × 0.75⁵. (Start from the 2 metres, and the 5th bounce is 5 steps on, not 4.)

   ```keys E02
   2 ENTER 0.75 ENTER 5 yˣ ×
   ```

   X shows <disp v="E02">0.4746</disp>.

3. 1023 grains. The first term is 1 and r = 2, so the sum is 1 × (2¹⁰ − 1) ÷ (2 − 1), which is
   2¹⁰ − 1:

   ```keys E03
   2 ENTER 10 yˣ 1 −
   ```

   X shows <disp v="E03">1,023.0000</disp>.
