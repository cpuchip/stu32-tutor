---
id: fn-01
title: Functions as programs
requires: setup shift-keys soft-keys rpn-arithmetic stack-lift swap-roll change-sign stack-full x-squared status-band clear-message
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Functions as programs

A function is a rule that turns an input into an output. The rule f(x) = 2x + 3 turns 5 into 13 and
1.5 into 6. Written down, a function is a formula; on the STU-32 it can be a short program: you
record the keys of the rule once and give them a letter, and then a number in X goes through the
rule with XEQ and that letter. The program uses the stack like any other calculation.

## From before

Two from unit 1, by hand. A function's rule is arithmetic like this, done in the right order.

```item FN1F1
prompt: Work out 3 + 4 × 5 − 2.
topics: mult-before-add
answer: type
calculator: no
slip: FN1F1A | worked left to right | Multiplication comes first: 4 × 5 is 20, then 3 + 20 − 2.
```

```item FN1F2
prompt: Work out 6² − 2 × 6.
topics: x-squared
answer: type
calculator: no
slip: FN1F2A | doubled 6 instead of squaring it | 6² is 6 × 6, which is 36, not 6 × 2.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. This whole lesson is one chain: each example carries on
from the one before, because a program is entered once and then used.

<mode m="35s,STU">In this mode XEQ and GTO wait, after the label's letter, for ENTER; the keys
below show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Entering a program

Programs live in the PRGM menu (gold, above 9). Its first soft key, also called PRGM, turns program
entry on and off. Turn it on:

```keys F01A
GOLD PRGM PRGM
```

The X line shows <disp v="F01A" kind="program">PRGM TOP</disp>, the top of program memory, and the
status band shows <disp v="F01A" kind="status">PRGM</disp>. In program entry, keys are recorded as
numbered lines instead of being worked out.

A program starts with a label, a letter that names it. LBL is gold, above XEQ:

```keys F01L after=F01A
GOLD LBL
```

The X line shows <disp v="F01L" kind="prompt">LBL _</disp>: like STO, LBL waits for a letter. F is on
the Σ+ key:

```keys F01B after=F01L
F
```

The X line shows <disp v="F01B" kind="program" m="33s">F001 LBL F ·33</disp><disp v="F01B" kind="program" m="35s">F001 LBL F ·35</disp><disp v="F01B" kind="program" m="STU">F001 LBL F ·STU</disp>: line 1 of program F. The mark after the
label is the mode it was written in<mode m="33s">, 33s</mode><mode m="35s">, 35s</mode><mode m="STU">, STU</mode>;
the program will run in that mode even if you change the mode later.

Now the rule itself. The program will find x in X when it starts, so the rule is the keys you would
press with x already there: multiply by 2, add 3.

```keys F01C after=F01B
2 × 3 +
```

The X line shows <disp v="F01C" kind="program">F005 +</disp>: lines 2 to 5 hold 2, ×, 3 and +. End
the program with RTN (blue, above XEQ):

```keys F01R after=F01C
BLUE RTN
```

The X line shows <disp v="F01R" kind="program">F006 RTN</disp>. Turn program entry off:

```keys F01 after=F01R
GOLD PRGM PRGM
```

PRGM leaves the status band and the X line shows a number again: keys are worked out as usual.

## Using the function

XEQ runs a program. With no equation showing, it waits for a label. Type the input, then XEQ:

```keys F02A after=F01
5 XEQ
```

The X line shows <disp v="F02A" kind="prompt">XEQ _</disp>. Press F<mode m="35s,STU">, then ENTER</mode>:

```keys F02 after=F02A
F
```
```keys F02 after=F02A mode=35s,STU
F ENTER
```

X shows <disp v="F02">13.0000</disp>: f(5) = 13. Any input works the same way:

```keys F03 after=F02
1.5 XEQ F
```
```keys F03 after=F02 mode=35s,STU
1.5 XEQ F ENTER
```

X shows <disp v="F03">6.0000</disp>, and a negative one:

```keys F04 after=F03
4 +/− XEQ F
```
```keys F04 after=F03 mode=35s,STU
4 +/− XEQ F ENTER
```

X shows <disp v="F04">-5.0000</disp>: f(−4) = 2 × (−4) + 3 = −5.

## A second program

The rule g(x) = x² + x needs x twice. In RPN, ENTER makes the copy: with x in X, ENTER puts a copy
in Y, x² squares the one in X, and + adds the two. Turn program entry on again:

```keys G01A after=F04
GOLD PRGM PRGM
```

The X line shows <disp v="G01A" kind="program">PRGM TOP</disp>. Program entry opens where the
program pointer is, and after a program has run, that is the top. A new label there starts a new
program, and F is left as it was. G is on the STO key:

```keys G01B after=G01A
GOLD LBL G
```

The X line shows <disp v="G01B" kind="program" m="33s">G001 LBL G ·33</disp><disp v="G01B" kind="program" m="35s">G001 LBL G ·35</disp><disp v="G01B" kind="program" m="STU">G001 LBL G ·STU</disp>. Record the rule, end it, and
turn program entry off:

```keys G01 after=G01B
ENTER GOLD x² + BLUE RTN GOLD PRGM PRGM
```

Then g(3):

```keys G02 after=G01
3 XEQ G
```
```keys G02 after=G01 mode=35s,STU
3 XEQ G ENTER
```

X shows <disp v="G02">12.0000</disp>: 3² + 3 = 9 + 3.

## Fixing a mistake

In program entry, ← deletes the line showing. Say you meant k(x) = 2x − 3 but pressed + at the end.
K is on the COS key:

```keys M01 after=G02
GOLD PRGM PRGM GOLD LBL K 2 × 3 +
```

The X line shows <disp v="M01" kind="program">K005 +</disp>, the wrong line. Press ←:

```keys M02 after=M01
←
```

The + is gone, and the X line shows the line before it, <disp v="M02" kind="program">K004 3</disp>.
Press − in its place, finish the program, and try it:

```keys M03 after=M02
− BLUE RTN GOLD PRGM PRGM 10 XEQ K
```
```keys M03 after=M02 mode=35s,STU
− BLUE RTN GOLD PRGM PRGM 10 XEQ K ENTER
```

X shows <disp v="M03">17.0000</disp>: k(10) = 20 − 3.

Each label names one program, and the calculator refuses a label that is already used. Try to start
another program F:

```keys D01 after=M03
GOLD PRGM PRGM GOLD LBL F
```

The screen shows <disp v="D01" kind="message">DUPLICAT.LBL</disp>. Press C to clear the message, and
turn program entry off; F is unchanged:

```keys D02 after=D01
C GOLD PRGM PRGM 5 XEQ F
```
```keys D02 after=D01 mode=35s,STU
C GOLD PRGM PRGM 5 XEQ F ENTER
```

X shows <disp v="D02">13.0000</disp>, f(5) as before. Programs stay in the calculator until you
clear them, so for each new function, pick a letter no program uses yet.

## Exercises

1. Enter h(x) = 5 − 2x as program H (H is on the RCL key), and work out h(4). Hint: work out 2x
   first, then bring in the 5; x↔y puts the two in the right order for the subtraction, as in
   num-01.
2. Work out g(−2) with the program G you already have.

## Answers

1. After 2 ×, X holds 2x; typing 5 puts it in X with 2x in Y, and x↔y swaps them so − works 5 − 2x:

   ```keys E01 after=D02
   GOLD PRGM PRGM GOLD LBL H 2 × 5 x↔y − BLUE RTN GOLD PRGM PRGM 4 XEQ H
   ```
   ```keys E01 after=D02 mode=35s,STU
   GOLD PRGM PRGM GOLD LBL H 2 × 5 x↔y − BLUE RTN GOLD PRGM PRGM 4 XEQ H ENTER
   ```

   X shows <disp v="E01">-3.0000</disp>: h(4) = 5 − 8.

2. G is still in the calculator:

   ```keys E02 after=E01
   2 +/− XEQ G
   ```
   ```keys E02 after=E01 mode=35s,STU
   2 +/− XEQ G ENTER
   ```

   X shows <disp v="E02">2.0000</disp>: (−2)² + (−2) = 4 − 2.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item FN1M1
prompt: f(x) = 3x − 4. What is f(5)?
topics: function
answer: type
calculator: no
slip: FN1M1A | read 3x as 3 + x | 3x means 3 times x: 3 × 5 is 15, then take away 4.
```

```item FN1M2
prompt: Work out (10 − 4) ÷ (1 + 2).
topics: fraction-bar
answer: type
calculator: no
slip: FN1M2A | divided only the 4 | The brackets come first: 6 ÷ 3.
```

```item FN1M3
prompt: g(x) = x² + x. What is g(−3)?
topics: function
answer: type
calculator: no
slip: FN1M3A | squared 3, then made it negative | g(−3) puts −3 in for x: (−3)² is 9, then 9 + (−3).
```

```item FN1M4
prompt: Work out √(5² − 4²).
topics: square-root
answer: type
calculator: no
slip: FN1M4A | took the root of each square | Work out under the root first: 25 − 16 is 9, and √9 is 3.
```
