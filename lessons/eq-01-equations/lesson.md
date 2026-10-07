---
id: eq-01
title: Equations, and checking a solution
status: draft prose (not yet read by a non-author, abacus or Michael)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# Equations, and checking a solution

An equation says two things are equal: 2x + 3 = 11. Solving it means finding the x that makes it
true. Before the STU-32 finds x for you, this lesson shows how to check an answer, because a check
is how you know any answer is right, yours or the calculator's.

## Before you start

The setup from rpn-01: 33s mode and FIX 4. Work the examples in order; most of them carry on from
the one before, and the text says when.

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

## Typing an equation

Equations are typed in Equation mode, EQN (gold, above 0). In Equation mode the soft keys become
the equation bar: ◀ and ▶ move through what you have typed, ( ) types a pair of brackets, and =
types an equals sign. A variable is typed with RCL and its letter, so x is RCL, then the X key (the
6 key, which carries the letter X). Type 2x + 3 = 11 and press ENTER to keep it:

```keys Q01
GOLD EQN 2 × RCL X + 3 = 11 ENTER
```

X shows <disp v="Q01" kind="eqn">2×X+3=11</disp>, and the status band shows
<disp v="Q01" kind="status">EQN</disp> while you are in Equation mode. The × between 2 and X is
written out; the end of the lesson shows why.

## Checking an answer

Press XEQ with the equation showing, and the calculator works out the left side minus the right
side. First it asks for the value of X:

```keys Q02 after=Q01
XEQ
```

The screen shows <disp v="Q02" kind="prompt">X?</disp>. Try 4: type it and press R/S to go on.

```keys Q03 after=Q02
4 R/S
```

X shows <disp v="Q03">0.0000</disp>. The left side, 2 × 4 + 3, is 11, so left minus right is 0: the
two sides are equal, and 4 is a solution.

Working out the equation leaves Equation mode. To try another value, show the equation again with
EQN and press XEQ. Try 5:

```keys Q04 after=Q03
GOLD EQN XEQ 5 R/S
```

X shows <disp v="Q04">2.0000</disp>. The left side is 2 × 5 + 3, which is 13, two more than 11, so
5 is not a solution. The number left over tells you how far off a try is, and which way.

## Letting the calculator solve it

SOLVE (gold, above 7) finds the value that makes left minus right zero. It works on the equation
that is showing, so show it with EQN first, then press SOLVE and the letter to solve for:

```keys Q05 after=Q04
GOLD EQN GOLD SOLVE X
```

X shows <disp v="Q05">4.0000</disp>, and the 4 is stored in X too. It is the solution you checked by
hand above, and you can check it again the same way: show the equation, XEQ, and R/S to keep the
value X now holds.

## The × matters

In 33s mode the calculator does not multiply two things written side by side. Type the same
equation without the × and it is stored as you typed it, but it cannot be worked out:

```keys Q06
GOLD EQN 2 RCL X + 3 = 11 ENTER XEQ 4 R/S
```

The screen shows <disp v="Q06" kind="message">SYNTAX ERROR</disp>. Press C to clear the message:

```keys Q06B after=Q06
C
```

X shows <disp v="Q06B">4.0000</disp>, the value you typed.

## Exercises

1. Does 3 solve 5x − 4 = 11? Type the equation and check it with XEQ.
2. Solve 3x + 7 = 1 with SOLVE, then say how you would check the answer.

## Answers

1. Yes. The keys:

   ```keys E01
   GOLD EQN 5 × RCL X − 4 = 11 ENTER XEQ 3 R/S
   ```

   X shows <disp v="E01">0.0000</disp>: left minus right is zero, so 3 is a solution.

2. The keys:

   ```keys E02
   GOLD EQN 3 × RCL X + 7 = 1 ENTER GOLD SOLVE X
   ```

   X shows <disp v="E02">-2.0000</disp>. To check it, show the equation again, press XEQ, and R/S
   to keep the −2 that X holds:

   ```keys E02B after=E02
   GOLD EQN XEQ R/S
   ```

   X shows <disp v="E02B">0.0000</disp>, because 3 × (−2) + 7 is 1.
