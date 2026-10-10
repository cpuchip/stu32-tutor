---
id: eq-01
title: Equations, and checking a solution
requires: setup shift-keys soft-keys status-band sto clear-message
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Equations, and checking a solution

An equation says two things are equal: 2x + 3 = 11. Solving it means finding the x that makes it
true. Before the STU-32 finds x for you, this lesson shows how to check an answer, because a check
is how you know any answer is right, yours or the calculator's.

## From before

Two from unit 1, by hand, before the calculator comes out. Solving an equation is undoing
arithmetic like this, so it needs to be sure.

```item EQ1F1
prompt: Work out 2 × (3 + 4).
topics: parentheses
answer: type
calculator: no
slip: EQ1F1A | multiplied before the brackets | The brackets come first: 3 + 4 is 7, then 2 × 7.
```

```item EQ1F2
prompt: Work out 10³ ÷ 4.
topics: power
answer: type
calculator: no
slip: EQ1F2A | 10 × 3, not 10³ | 10³ is 10 × 10 × 10, which is 1000. Then 1000 ÷ 4.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Work the examples in order; most of them carry on from
the one before, and the text says when.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

A word about names. The unknown in an equation is usually called x, and on the calculator it is
the variable X, the same kind of variable as A to Z in rpn-02. The bottom line of the screen is
also called X. In this lesson, "X shows" always means that bottom line, and "the variable X" means
the stored value.

## Typing an equation

Equation mode is EQN, gold above 0. It works like a switch: press it once to turn Equation mode
on, again to turn it off. In Equation mode the keys type into an equation instead of calculating:
2 types a 2, and × types a times sign. The equals sign has no key
of its own; while you type, the soft keys under the screen become the equation bar, and = is the
fourth of them. A variable is typed with RCL and then its letter, so x is RCL, then the 6 key,
which carries the letter X. ENTER keeps the equation and leaves it showing.

Type 2x + 3 = 11:

```keys Q01
GOLD EQN 2 × RCL X + 3 = 11 ENTER
```

The screen shows the equation, <disp v="Q01" kind="eqn">2×X+3=11</disp>, and the status band shows
<disp v="Q01" kind="status">EQN</disp> while Equation mode is on.

## Checking an answer

XEQ is the first key in the row with 7, 8 and 9. Press it with an equation showing, and the
calculator works out the left side minus the right side. First it asks what X should be:

```keys Q02 after=Q01
XEQ
```

The line above X shows <disp v="Q02" kind="prompt">X?</disp>, and X shows the value the variable X
holds now. Type a new value, or leave it, and press R/S (on the bottom row, fourth key) to go on.
Whichever value you give is stored in the variable X. Try 4:

```keys Q03 after=Q02
4 R/S
```

X shows <disp v="Q03">0.0000</disp>. The left side, 2 × 4 + 3, is 11, so left minus right is 0: the
two sides are equal, and 4 is a solution.

Working the equation out turns Equation mode off. To try another value, press EQN to show the
equation again, and XEQ. Try 5:

```keys Q04 after=Q03
GOLD EQN XEQ 5 R/S
```

X shows <disp v="Q04">2.0000</disp>. The left side is 2 × 5 + 3, which is 13, two more than 11, so
5 is not a solution. The number left over tells you how far off a try is, and which way.

## Letting the calculator solve it

SOLVE (gold, above 7) searches for a value of X that makes left minus right zero, and reports the
value it finds. It works on the equation that is showing, so show it first, then press SOLVE:

```keys Q05A after=Q04
GOLD EQN GOLD SOLVE
```

X shows <disp v="Q05A" kind="prompt">SOLVE _</disp>. Like STO and RCL, SOLVE waits for a
variable's letter, so the 6 key now means X:

```keys Q05 after=Q05A
X
```

The X line shows <disp v="Q05" kind="view">X=4.0000</disp>: SOLVE ends by showing the
variable it solved for, as VIEW does in rpn-02. The 4 is in X, and it is stored in the variable
X too: the solution you checked by hand above. The next key clears the view: ← and C only clear
it, and any other key clears it and then does its own job. Press ←:

```keys Q05C after=Q05
←
```

X shows <disp v="Q05C">4.0000</disp>: the view is gone, and the 4 is still in X. To check the
solution again, show the equation, press XEQ, and press R/S at X? to keep the 4.

## The × matters

<mode m="33s,35s">
In this mode the calculator does not multiply two things written side by side in an equation, as
the HP 33s and 35s did not.
</mode>
<mode m="STU">
In STU mode the calculator does multiply two things written side by side, as algebra does: 2X
means 2 × X. The 33s and 35s modes do not, so this section differs there.
</mode>

Type the same equation without the ×. Typing while an equation is showing starts a new one, and
the first stays in the calculator's list:

```keys Q06A
GOLD EQN 2 RCL X + 3 = 11 ENTER
```

<mode m="33s,35s">
The screen shows <disp v="Q06A" kind="eqn">2X+3=11</disp>. It is stored as typed, but it cannot be
worked out. The trouble shows only when the calculator tries, after R/S:
</mode>
<mode m="STU">
The screen shows <disp v="Q06A" kind="eqn">2×X+3=11</disp>: the calculator put the × in for you.
Work it out at 4, after R/S:
</mode>

```keys Q06 after=Q06A
XEQ 4 R/S
```

<mode m="33s,35s">
The screen shows <disp v="Q06" kind="message">SYNTAX ERROR</disp>. Press C to clear the message:
</mode>

```keys Q06B after=Q06 mode=33s,35s
C
```

<mode m="33s,35s">
X shows <disp v="Q06B">4.0000</disp>. That is the 4 you typed at X?, left on the X line; it is not an
answer.
</mode>
<mode m="STU">
X shows <disp v="Q06">0.0000</disp>: left minus right is zero, so 4 is a solution, as it was with
the ×. In the 33s and 35s modes the same keys end in SYNTAX ERROR, so a lesson written for them
always types the ×. Typing it in STU mode does no harm.
</mode>

## Exercises

1. Does 3 solve 5x − 4 = 11? Type the equation, with x as RCL X, and check it with XEQ.
2. Solve 3x + 7 = 1 with SOLVE, then check the answer.

## Answers

1. Yes. The keys:

   ```keys E01
   GOLD EQN 5 × RCL X − 4 = 11 ENTER XEQ 3 R/S
   ```

   X shows <disp v="E01">0.0000</disp>: left minus right is zero, so 3 is a solution.

2. After ENTER the equation is still showing, so SOLVE can follow straight away:

   ```keys E02
   GOLD EQN 3 × RCL X + 7 = 1 ENTER GOLD SOLVE X
   ```

   The X line shows <disp v="E02" kind="view">X=-2.0000</disp>. To check it, show the equation again, press XEQ, and R/S to
   keep the −2 the variable X holds:

   ```keys E02B after=E02
   GOLD EQN XEQ R/S
   ```

   X shows <disp v="E02B">0.0000</disp>, because 3 × (−2) + 7 is 1.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item EQ1M1
prompt: Type 3x − 5 = 13 and XEQ it at x = 6. What does X show? Does 6 solve it?
topics: xeq-check
answer: type
calculator: yes
slip: EQ1M1A | the left side alone | XEQ gives the left side minus the right side: 13 − 13.
```

```item EQ1M2
prompt: Work out 4 + 6 × 2.
topics: mult-before-add
answer: type
calculator: no
slip: EQ1M2A | added first | Multiplication comes before addition: 6 × 2 is 12, then 4 + 12.
```

```item EQ1M3
prompt: Solve 5x + 8 = 3 with SOLVE. What is x?
topics: solve
answer: type
calculator: yes
slip: EQ1M3A | added the 8 instead of taking it away | Undo the + 8 by taking 8 away: 3 − 8 is −5, then ÷ 5.
```

```item EQ1M4
prompt: Work out √36 × 5.
topics: square-root
answer: type
calculator: no
slip: EQ1M4A | halved 36 instead of its root | √36 asks which number times itself is 36: 6, then 6 × 5.
```
