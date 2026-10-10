---
id: expr-01
title: Letters for numbers
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation partial-products
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Maren, Tobin
voices: story plain
---

# Letters for numbers

<voice v="story">Maren sells pies at 7 coins each.</voice><voice v="plain">Pies sell at 7 coins each.</voice> Two pies cost 7 × 2 = 14 coins, and ten cost 7 × 10 = 70. Each
time the rule is the same: 7 times the number of pies. Algebra writes a rule like that once, with a
letter standing for the number that changes: if n is the number of pies, they cost 7 × n coins. This
lesson is about letters like n: what they mean, and how to work out what a rule gives for a number.

## From before

Two from unit 1, by hand.

```item EP1F1
prompt: Work out 34 × 12 by parts: 34 × 10, then 34 × 2.
topics: partial-products
answer: type
calculator: no
slip: EP1F1A | added the 2 | The second part is 34 × 2, which is 68, not 2.
```

```item EP1F2
prompt: Work out 1000 − 364.
topics: column-subtraction
answer: type
calculator: no
slip: EP1F2A | took the smaller digit from the larger | 0 − 4 needs a borrow, all the way from the thousands.
```

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## A letter stands for a number

A letter that stands for a number is called a variable, because the number it stands for can vary:
one customer buys 2 pies, the next 12. A rule made of numbers, letters and operations, like 7 × n, is
an expression. An expression has no = sign; it is something to work out. Algebra usually leaves out
the × between a number and a letter: 7n means 7 × n.

To find what 12 pies cost, put 12 in for n: 7 × 12 = 84. Putting in a number for the letter and
working out the result is called evaluating the expression. By hand, 7 × 12 is 7 × 10 + 7 × 2 =
70 + 14 = 84 (whole-02). The check:

```keys P01 entry=alg
7 × 12 ENTER
```

```keys P01 entry=rpn
7 ENTER 12 ×
```

The screen shows <disp v="P01">84.0000</disp>: 84 coins.

## Multiply before you add

<voice v="story">Tobin carries orders for 5 coins. For the bakery's small pies, at 3 coins each, an order of n pies
costs 3n + 5: 3 for each pie, and 5 for carrying.</voice><voice v="plain">Carrying an order costs 5 coins. For small pies at 3 coins each, an order of n pies
costs 3n + 5: 3 for each pie, and 5 for carrying.</voice> For 4 pies, is that 3 × 4 + 5 = 12 + 5 = 17, or
3 × (4 + 5) = 27? Everyone who writes mathematics agrees to read it the first way, so that a line of
mathematics means the same thing to everyone: multiplying and dividing come before adding and taking
away, unless brackets say otherwise. So 3n + 5 means 3 times n first, then 5 more. By hand,
3 × 4 + 5 = 17.

## Letting the calculator hold the number

The calculator can keep a number under a letter. STO stores the number showing, and RCL recalls it.
After STO or RCL the calculator waits for a letter, and the next key you press means only the letter
printed small at its lower right. N is on the x↔y key. The calculator's letters do not have to match
the ones on paper, but matching them is easier to follow.

Store 4 under N:

```keys V01
4 STO N
```

The screen shows <disp v="V01">4.0000</disp>. Carrying on, type the expression with RCL N where the
letter goes:
<entry e="alg">the line multiplies before it adds, as the rule does.</entry><entry e="rpn">on the stack,
the order of the keys does it: 3 times N first, then 5 added. RCL puts a finished number on the stack,
so no ENTER is needed after it.</entry>

```keys V02 entry=alg after=V01
3 × RCL N + 5 ENTER
```

```keys V02 entry=rpn after=V01
3 ENTER RCL N × 5 +
```

The screen shows <disp v="V02">17.0000</disp>, the hand work's answer.
<entry e="alg">The line reads <disp v="V02" kind="line">3×N+5</disp>: the letter is in the line, and the
calculator used the number stored under it.</entry>

The point of a letter is that the number can change and the rule stays. Carrying on, an order of 10
pies:

```keys V03 after=V02
10 STO N
```

The screen shows <disp v="V03">10.0000</disp>. Carrying on, the same expression again:

```keys V04 entry=alg after=V03
3 × RCL N + 5 ENTER
```

```keys V04 entry=rpn after=V03
3 ENTER RCL N × 5 +
```

The screen shows <disp v="V04">35.0000</disp>: 3 × 10 + 5.

## Exercises

Work each out by hand first, then check it with the number stored under its letter.

1. Evaluate 2a + 9 when a = 6. (A is on the √x key.)
2. Loaves cost 3 coins each and the box costs 2. Write the cost of n loaves in a box, then find it
   for n = 15.
3. Evaluate a times a, take away a, when a = 5.

## Answers

1. 2 × 6 + 9 = 12 + 9 = 21. Store 6 under A, then the expression:

   ```keys E01
   6 STO A
   ```

   ```keys E01B entry=alg after=E01
   2 × RCL A + 9 ENTER
   ```

   ```keys E01B entry=rpn after=E01
   2 ENTER RCL A × 9 +
   ```

   The screen shows <disp v="E01B">21.0000</disp>.

2. 3n + 2. For n = 15, 3 × 15 + 2 = 45 + 2 = 47:

   ```keys E02
   15 STO N
   ```

   ```keys E02B entry=alg after=E02
   3 × RCL N + 2 ENTER
   ```

   ```keys E02B entry=rpn after=E02
   3 ENTER RCL N × 2 +
   ```

   The screen shows <disp v="E02B">47.0000</disp>.

3. 5 × 5 − 5 = 25 − 5 = 20:

   ```keys E03
   5 STO A
   ```

   ```keys E03B entry=alg after=E03
   RCL A × RCL A − RCL A ENTER
   ```

   ```keys E03B entry=rpn after=E03
   RCL A RCL A × RCL A −
   ```

   The screen shows <disp v="E03B">20.0000</disp>.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item EP1M1
prompt: Evaluate 4n + 3 when n = 5.
topics: evaluating
answer: type
calculator: no
slip: EP1M1A | added before multiplying | 4n means 4 times n: 4 × 5 is 20, then + 3.
```

```item EP1M2
prompt: 57 eggs go into boxes of 6. How many eggs are left over?
topics: quotient-remainder
answer: type
calculator: no
slip: EP1M2A | the full boxes, not what is left | 9 full boxes hold 54, and 57 − 54 are left over.
```

```item EP1M3
prompt: Work out 2 + 5 × 6.
topics: multiply-first
answer: type
calculator: no
slip: EP1M3A | added first | Multiplying comes before adding: 5 × 6 is 30, then 2 + 30.
```

```item EP1M4
prompt: Work out 589 + 237.
topics: column-addition
answer: type
calculator: no
slip: EP1M4A | every carry left out | 9 + 7 is 16: write 6 and carry 1 to the tens, and so on.
```
