---
id: fn-03
title: Domain
requires: setup shift-keys rpn-arithmetic stack-lift change-sign clear-message inequalities function program-entry xeq-program program-pointer program-edit loop
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Domain

A function's domain is the set of inputs it can take. Many rules take any number: $f(x) = 2x + 3$ from
fn-01 has a value for every $x$, and so does $\frac{x}{2}$. But a rule that divides by something that can be 0,
or takes the square root of something that can be negative, has inputs it cannot take, and those
inputs are left out of its domain. Written as programs, two such functions each meet an input they
cannot take, and the calculator says so.

## From before

```item FN3F1
prompt: Work out $1 ÷ 0.25$.
topics: reciprocal
answer: type
calculator: no
slip: FN3F1A | multiplied instead | Dividing by a quarter asks how many quarters make 1: four.
```

```item FN3F2
prompt: $2x − 8 ≥ 0$ has its boundary where $2x − 8 = 0$. What $x$ is that?
operands: 2, 8, 0
topics: inequalities
answer: type
calculator: no
slip: FN3F2A | kept the minus sign | Undo the − 8 by adding 8: $2x = 8$, then ÷ 2.
```

## Before you start

The examples are one chain: each carries on from
the one before. Two programs go in, R and S, with the program entry, labels, XEQ and RTN you know.
R is on the XEQ key and S is on 7; the programs of the last two lessons use neither letter.

<mode m="35s,STU">In this mode XEQ and GTO wait, after the label's letter, for ENTER; the keys
below show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Two functions

The first is $r(x) = \frac{1}{x}$, one over $x$. The second is $s(x) = \sqrt{x − 2}$, the square root of $x − 2$. Both
programs go in now, one after the other. R's whole rule is one key, 1/x, the fifth key of the top
row:

```keys P01A
GOLD PRGM PRGM GOLD LBL R 1/x BLUE RTN
```

The X line shows <disp v="P01A" kind="program">R003 RTN</disp>. R's RTN ends R, so a new label keyed
in after it starts a program of its own. Carry straight on with S, which subtracts 2 and takes the
square root with √x, the first key of the top row:

```keys P01B after=P01A
GOLD LBL S 2 − √x BLUE RTN
```

The X line shows <disp v="P01B" kind="program">S005 RTN</disp>: S's lines are numbered from its own
label, as U's were in fn-02. Turn program entry off:

```keys P01 after=P01B
GOLD PRGM PRGM
```

## Dividing by zero

Try R on 4:

```keys D01 after=P01
4 XEQ R
```
```keys D01 after=P01 mode=35s,STU
4 XEQ R ENTER
```

X shows <disp v="D01">0.2500</disp>: $r(4) = \frac{1}{4}$. Now try it on 0:

```keys D02 after=D01
0 XEQ R
```
```keys D02 after=D01 mode=35s,STU
0 XEQ R ENTER
```

The screen shows <disp v="D02" kind="message">DIVIDE BY 0</disp>. One over zero has no value: a
quotient $\frac{a}{b}$ is the number that gives $a$ when it is multiplied by $b$, and no number gives 1 when it
is multiplied by 0. So 0 is not in the domain of $r$. Every other number is, so the domain of $r$ is
all numbers except 0.

```why
ask: Why can no number stand for $1 ÷ 0$, not even a very large one?
because: A very large number times 0 is still 0, never 1. And 1 divided by numbers closer and closer to 0 grows without end, so there is no number for it to settle on.
```

Press C to clear the message:

```keys D03 after=D02
C
```

X shows <disp v="D03">0.0000</disp>, the input that was refused.

A program that meets an input it cannot use stops at the line that refused it. Open program entry
to see where R stopped:

```keys D04 after=D03
GOLD PRGM PRGM
```

The X line shows <disp v="D04" kind="program">R002 1/x</disp>: line 2 of R, the 1/x. In a longer
program this is how you find which step failed. Turn program entry off:

```keys D05 after=D04
GOLD PRGM PRGM
```

## The square root of a negative number

Try S on 6:

```keys S01 after=D05
6 XEQ S
```
```keys S01 after=D05 mode=35s,STU
6 XEQ S ENTER
```

X shows <disp v="S01">2.0000</disp>: $s(6) = \sqrt{4}$.

```item SQ1T1
prompt: Work out $s(51)$ by hand, for the same $s(x) = \sqrt{x − 2}$.
operands: 51, 2
twin: S01
topics: function
answer: type
calculator: no
slip: SQ1T1A | the root first | S takes the 2 away first and then the root: $\sqrt{49}$, not $\sqrt{51} − 2$.
slip: SQ1T1B | no root | $51 − 2$ is 49, and the root of 49 is 7.
```

Now 2:

```keys S02 after=S01
2 XEQ S
```
```keys S02 after=S01 mode=35s,STU
2 XEQ S ENTER
```

X shows <disp v="S02">0.0000</disp>: $s(2) = \sqrt{0} = 0$. Now 1:

```keys S03 after=S02
1 XEQ S
```
```keys S03 after=S02 mode=35s,STU
1 XEQ S ENTER
```

The screen shows <disp v="S03" kind="message">SQRT(NEG)</disp>: the square root of a negative
number. A square is never negative: a positive number times itself is positive, a negative number
times itself is positive too, and $0 × 0$ is 0. So no number squares to a negative, and a negative
number has no square root among the numbers these lessons use (the real numbers).

Press C to clear the message:

```keys S04 after=S03
C
```

X shows <disp v="S04">-1.0000</disp>. That is not the input, 1. R refused its input at its first
step, but S had already done its 2 and its − when the √x refused, so X holds $1 − 2$. Open program
entry to see where S stopped:

```keys S05 after=S04
GOLD PRGM PRGM
```

The X line shows <disp v="S05" kind="program">S004 √x</disp>, S's square root. Turn program entry
off:

```keys S06 after=S05
GOLD PRGM PRGM
```

So the domain of $s$ is the inputs $x$ for which $x − 2$ is not negative: $x − 2 ≥ 0$, which is $x ≥ 2$.
2 itself is in it, as $s(2) = 0$ showed. It is the edge of the domain: every number above it is in,
every number below it is out, however close.

```why
ask: Why is 2 the edge of s's domain, and not 0, the edge of √x's own?
because: S takes 2 away before the root, so the root sees $x − 2$. That is 0 when $x$ is 2, and negative for any $x$ below it.
```

The domain comes from the rule, worked out as above; the calculator's message confirms it. A
calculator can refuse for other reasons too, so a message alone does not tell you the domain.

## A stopped program

While a program is stopped at a line, program entry opens at that line, as you saw twice. Anything
you key in then goes in after the line showing, as before, so it lands inside that program. That
is why both programs went in at the start: if S had been keyed in after R stopped, its lines would
have gone into R, after the 1/x.

GTO . . clears that: it moves the pointer to the top of program memory, without running anything.
GTO is gold above 4, as in T's loop, and the two dots are the . key pressed twice:

```keys S07 after=S06
GOLD GTO . .
```

Nothing ran: X still shows <disp v="S07">-1.0000</disp>. But program entry now opens at the top:

```keys S08 after=S07
GOLD PRGM PRGM
```

The X line shows <disp v="S08" kind="program">PRGM TOP</disp>. Turn program entry off:

```keys S09 after=S08
GOLD PRGM PRGM
```

So before you key in a new program after an error, press GOLD GTO . . first. (Running any program to
its end does the same: the pointer goes back to the top when a program finishes.)

## Exercises

1. Is −2 in the domain of $r$? Work out $r(−2)$ with R.
2. Is 2.25 in the domain of $s$? Work out $s(2.25)$ with S.
3. Is 1.99 in the domain of $s$? Try it with S, and read X after you clear the message.

## Answers

1. Yes: only 0 is left out of r's domain.

   ```keys E01 after=S09
   2 +/− XEQ R
   ```
   ```keys E01 after=S09 mode=35s,STU
   2 +/− XEQ R ENTER
   ```

   X shows <disp v="E01">-0.5000</disp>: $r(−2) = \frac{1}{−2}$.

2. Yes, since $2.25 ≥ 2$:

   ```keys E02 after=E01
   2.25 XEQ S
   ```
   ```keys E02 after=E01 mode=35s,STU
   2.25 XEQ S ENTER
   ```

   X shows <disp v="E02">0.5000</disp>: $s(2.25) = \sqrt{0.25}$, and $0.5 × 0.5 = 0.25$.

3. No: 1.99 is below 2, however little.

   ```keys E03 after=E02
   1.99 XEQ S
   ```
   ```keys E03 after=E02 mode=35s,STU
   1.99 XEQ S ENTER
   ```

   The screen shows <disp v="E03" kind="message">SQRT(NEG)</disp>. Clear it:

   ```keys E03B after=E03
   C
   ```

   X shows <disp v="E03B">-0.0100</disp>: $1.99 − 2$, the negative number the square root refused. S
   is stopped at its √x again, so press GOLD GTO . . before you key in a new program.

## Mixed review

```item FN3M1
prompt: For $\sqrt{x − 1}$ at $x = 0.75$, what is the number under the root?
operands: 1, 0.75
topics: sqrt-negative
answer: type
calculator: no
slip: FN3M1A | took x from 1 | It is $x − 1$: $0.75 − 1$, below zero. That is why the root is refused.
```

```item FN3M2
prompt: Work out $2^{-1} + 2^{0}$.
topics: neg-frac-powers
answer: type
calculator: no
slip: FN3M2A | read the powers as numbers to add | $2^{-1}$ is $1 ÷ 2$, and any number to the power 0 is 1.
```

```item FN3M3
prompt: For which $x$ is $6 ÷ (2x − 4)$ not defined?
topics: divide-by-zero
answer: type
calculator: no
slip: FN3M3A | the sign turned | The bottom is 0 when $2x − 4 = 0$: $2x = 4$.
```

```item FN3M4
prompt: For $2x + 1 = 7$, what is left minus right at $x = 2$?
operands: 2, 1, 7, 2
topics: xeq-check
answer: type
calculator: no
slip: FN3M4A | the left side alone | Left minus right: $2 × 2 + 1$ is 5, and $5 − 7$.
```

## Checkpoint

Questions on the whole unit.

```item CP3A
prompt: $f(x) = x^{2} − 2x$. What is $f(3)$?
operands: 2, 2, 3
topics: function
answer: type
calculator: no
slip: CP3A1 | 2x read as 2 | The $2x$ means 2 times $x$: take away $2 × 3$.
slip: CP3A2 | added the 2x | It is minus $2x$: $9 − 6$.
```

```item CP3B
prompt: For which $x$ is $1 ÷ (x − 5)$ not defined?
topics: domain divide-by-zero
answer: type
calculator: no
slip: CP3B1 | the sign turned | The bottom is 0 when $x − 5 = 0$, so $x = 5$.
slip: CP3B2 | x = 0 | At $x = 0$ the bottom is −5, which is fine; find where it is 0.
```

```item CP3C
prompt: What is the smallest $x$ for which $\sqrt{x − 4}$ is defined?
topics: domain sqrt-negative
answer: type
calculator: no
slip: CP3C1 | x = 0 | The number under the root, $x − 4$, must not be negative, so $x$ is at least 4.
slip: CP3C2 | more than 0, not 0 or more | The square root of 0 is 0, which is defined, so $x − 4$ can be 0: $x = 4$.
```
