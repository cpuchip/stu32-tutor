---
id: eq-03
title: Two answers, and inequalities
requires: setup shift-keys change-sign sto eqn-typing xeq-check solve
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Two answers, and inequalities

The equations in eq-01 and eq-02 each had one answer. Some have more than one, and SOLVE finds only
one at a time. This lesson shows how to point SOLVE at each answer, and then how the check from
eq-01 answers a second question: which side of an answer a value is on.

## From before

Two from unit 1, by hand.

```item EQ3F1
prompt: Work out 7² − 4².
topics: x-squared
answer: type
calculator: no
slip: EQ3F1A | squared the difference | Square each first: 49 − 16. (7 − 4)² is another number.
```

```item EQ3F2
prompt: Work out 3/4 − 1/2, as a decimal.
topics: fraction-arithmetic
answer: type
calculator: no
slip: EQ3F2A | took tops from tops and bottoms from bottoms | Give them one bottom: 3/4 − 2/4 is 1/4.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Work the examples in order: each one either carries on
from the one before or starts fresh, and the text says which.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## An equation with two answers

The absolute value of a number, written |x|, is its distance from zero: |5| and |−5| are both 5.
So |x − 3| = 5 says that x − 3 is 5 or −5, which makes x either 8 or −2.

Absolute value is ABS (gold, above +/−). In an equation it types ABS with its opening bracket; ▶, the second key on the equation bar, steps out of the bracket
when you are done inside it. Type |x − 3| = 5:

```keys A01
GOLD EQN GOLD ABS RCL X − 3 ▶ = 5 ENTER
```

The screen shows <disp v="A01" kind="eqn">ABS(X-3)=5</disp>. Check the first answer, 8, with XEQ:

```keys A02 after=A01
XEQ 8 R/S
```

X shows <disp v="A02">0.0000</disp>, so 8 is a solution.

## Pointing SOLVE at an answer

SOLVE starts its search from two guesses: the value stored in the variable you solve for, and the
number on the X line when you press SOLVE. It finds one solution, usually the one nearest its
guesses, and stops. It does not tell you whether there is another.

To find the larger answer, use guesses 10 and 20: store 10 in X, type 20 so it is on the X line,
and solve. XEQ has already left Equation mode, so STO stores the 10.

```keys A03 after=A02
10 STO X 20 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="A03" kind="view">X=8.0000</disp>. SOLVE leaves Equation mode too, so STO works straight away.
Now guesses on the other side, 0 and −10:

```keys A04 after=A03
0 STO X 10 +/− GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="A04" kind="view">X=-2.0000</disp>. Both answers, found by giving SOLVE guesses near each one. When
you expect more than one answer, work out roughly where they are first, by reasoning as above or by
checking values with XEQ and watching where left minus right changes sign, then guess near each.

One more thing about guesses. Right after you type an equation and press ENTER, Equation mode is
still on, and digits you type start a new equation instead of setting a guess. So press EQN once
to leave Equation mode, set the guesses, then press EQN again to show the equation for SOLVE.
SOLVE and XEQ need the equation showing; STO and the guesses need Equation mode off.

## Inequalities

An inequality says one side is less than or greater than the other: 2x + 3 < 11. The x where the
two sides are equal is the boundary; eq-01 found it: 2x + 3 = 11 at x = 4. This equation has one
answer, so the x that make the inequality true lie all on one side of 4. (An inequality whose
equation has two answers, like |x − 3| < 5, is true between them, from −2 to 8.)

The check from eq-01 tells you which side a value is on. XEQ works out left minus right, and if that
is negative, the left side is smaller. This example starts fresh. Type the boundary equation and
test 0:

```keys B01
GOLD EQN 2 × RCL X + 3 = 11 ENTER XEQ 0 R/S
```

X shows <disp v="B01">-8.0000</disp>: negative, so at x = 0 the left side is less than the right, and
0 makes 2x + 3 < 11 true. Test 5, on the other side of 4:

```keys B02 after=B01
GOLD EQN XEQ 5 R/S
```

X shows <disp v="B02">2.0000</disp>: positive, so 5 does not. The inequality is true for every x less
than 4: x < 4. At 4 itself the two sides are equal (eq-01 showed 0 there), so 4 is not less: it
would count only for ≤, "less than or equal to".

## Exercises

1. Find both answers to |x + 1| = 4.
2. For which x is 3x − 6 > 0? Find the boundary with SOLVE, then test a value.

## Answers

1. The answers are 3 and −5. Press EQN once after ENTER to leave Equation mode, then guesses 0 and
   10 for the first answer:

   ```keys E01
   GOLD EQN GOLD ABS RCL X + 1 ▶ = 4 ENTER GOLD EQN 0 STO X 10 GOLD EQN GOLD SOLVE X
   ```

   The X line shows <disp v="E01" kind="view">X=3.0000</disp>. Then guesses 0 and −10 for the second:

   ```keys E01B after=E01
   0 STO X 10 +/− GOLD EQN GOLD SOLVE X
   ```

   The X line shows <disp v="E01B" kind="view">X=-5.0000</disp>.

2. The boundary is where 3x − 6 = 0. Right after ENTER the equation is still showing, so SOLVE can
   follow at once:

   ```keys E02
   GOLD EQN 3 × RCL X − 6 = 0 ENTER GOLD SOLVE X
   ```

   The X line shows <disp v="E02" kind="view">X=2.0000</disp>. Test 4, above the boundary:

   ```keys E02B after=E02
   GOLD EQN XEQ 4 R/S
   ```

   X shows <disp v="E02B">6.0000</disp>: positive, so the left side, 3x − 6, is more than 0 at 4. The
   inequality is true for every x greater than 2: x > 2.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item EQ3M1
prompt: x × x = 9 has two answers. Which does SOLVE find from guesses 1 and 5?
topics: solve-guesses
answer: type
calculator: yes
slip: EQ3M1A | the other answer | SOLVE finds the answer near its guesses, and 1 and 5 are both positive.
```

```item EQ3M2
prompt: Work out (15 − 3) ÷ 4 + 2.
topics: mult-before-add
answer: type
calculator: no
slip: EQ3M2A | added before dividing | Division comes before the addition: 12 ÷ 4 is 3, then + 2.
```

```item EQ3M3
prompt: The boundary of 2x − 4 > 10 is where 2x − 4 = 10. What x is that?
topics: inequalities
answer: type
calculator: no
slip: EQ3M3A | took the 4 away instead of adding it | Undo the − 4 by adding 4: 10 + 4 is 14, then ÷ 2.
```

```item EQ3M4
prompt: Work out 10² × 10³ as one number.
topics: power
answer: type
calculator: no
slip: EQ3M4A | multiplied the powers | 10² × 10³ is 100 × 1000: the powers add, to 10⁵.
```

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP2A
prompt: Solve 4x − 7 = 13. What is x?
topics: xeq-check
answer: type
calculator: no
slip: CP2A1 | took the 7 away instead of adding it | Undo the − 7 by adding 7: 13 + 7 = 20, then ÷ 4.
slip: CP2A2 | undid the × 4 first | Undo in the opposite order: the − 7 first, then the × 4.
```

```item CP2B
prompt: |x − 2| = 5 has two answers. What is the larger one?
topics: abs
answer: type
calculator: no
slip: CP2B1 | took the 2 away instead of adding it | If x − 2 = 5, then x is 2 more than 5.
slip: CP2B2 | the smaller answer | That is the other answer, from x − 2 = −5. The larger comes from x − 2 = 5.
```

```item CP2C
prompt: What is the largest whole number x with 2x + 1 < 9?
topics: inequalities
answer: type
calculator: no
slip: CP2C1 | the edge itself | The inequality 2x + 1 < 9 means x < 4, and 4 itself is not less than 4.
slip: CP2C2 | added the 1 | Undo the + 1 by taking it away: 9 − 1 = 8.
```
