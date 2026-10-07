---
id: fn-03
title: Domain
status: draft prose (non-author read taken; accepted for accuracy by abacus #4415; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Domain

A function's domain is the set of inputs it can take. Many rules take any number: f(x) = 2x + 3 from
fn-01 has a value for every x, and so does x/2. But a rule that divides by something that can be 0,
or takes the square root of something that can be negative, has inputs it cannot take, and those
inputs are left out of its domain. This lesson writes two such functions as programs, gives each an
input it cannot take, and reads what the calculator says.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. This lesson is one chain: each example carries on from
the one before. It enters two programs, R and S, with the program entry, labels, XEQ and RTN of
fn-01. R is on the XEQ key and S is on 7; neither letter is used in fn-01 or fn-02.

<mode m="35s,STU">In this mode XEQ and GTO wait, after the label's letter, for ENTER (or a line's
three digits); the keys below show the ENTER.</mode>

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Two functions

The first is r(x) = 1/x, one over x. The second is s(x) = √(x − 2), the square root of x − 2. Both
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

X shows <disp v="D01">0.2500</disp>: r(4) = 1/4. Now try it on 0:

```keys D02 after=D01
0 XEQ R
```
```keys D02 after=D01 mode=35s,STU
0 XEQ R ENTER
```

The screen shows <disp v="D02" kind="message">DIVIDE BY 0</disp>. One over zero has no value: a
quotient a/b is the number that gives a when it is multiplied by b, and no number gives 1 when it
is multiplied by 0. So 0 is not in the domain of r. Every other number is, so the domain of r is
all numbers except 0.

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

X shows <disp v="S01">2.0000</disp>: s(6) = √4. Now 2:

```keys S02 after=S01
2 XEQ S
```
```keys S02 after=S01 mode=35s,STU
2 XEQ S ENTER
```

X shows <disp v="S02">0.0000</disp>: s(2) = √0 = 0. Now 1:

```keys S03 after=S02
1 XEQ S
```
```keys S03 after=S02 mode=35s,STU
1 XEQ S ENTER
```

The screen shows <disp v="S03" kind="message">SQRT(NEG)</disp>: the square root of a negative
number. A square is never negative: a positive number times itself is positive, a negative number
times itself is positive too, and 0 × 0 is 0. So no number squares to a negative, and a negative
number has no square root among the numbers these lessons use (the real numbers).

Press C to clear the message:

```keys S04 after=S03
C
```

X shows <disp v="S04">-1.0000</disp>. That is not the input, 1. R refused its input at its first
step, but S had already done its 2 and its − when the √x refused, so X holds 1 − 2. Open program
entry to see where S stopped:

```keys S05 after=S04
GOLD PRGM PRGM
```

The X line shows <disp v="S05" kind="program">S004 √x</disp>, S's square root. Turn program entry
off:

```keys S06 after=S05
GOLD PRGM PRGM
```

So the domain of s is the inputs x for which x − 2 is not negative: x − 2 ≥ 0, which is x ≥ 2.
2 itself is in it, as s(2) = 0 showed. It is the edge of the domain: every number above it is in,
every number below it is out, however close.

The domain comes from the rule, worked out as above; the calculator's message confirms it. A
calculator can refuse for other reasons too, so a message alone does not tell you the domain.

## A stopped program

While a program is stopped at a line, program entry opens at that line, as you saw twice. Anything
you key in then goes in after the line showing, as in fn-01, so it lands inside that program. That
is why both programs went in at the start: if S had been keyed in after R stopped, its lines would
have gone into R, after the 1/x.

GTO . . clears that: it moves the pointer to the top of program memory, without running anything.
GTO is gold above 4, as in fn-02, and the two dots are the . key pressed twice:

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
its end does the same, as fn-01 showed: the pointer goes back to the top when a program finishes.)

## Exercises

1. Is −2 in the domain of r? Work out r(−2) with R.
2. Is 2.25 in the domain of s? Work out s(2.25) with S.
3. Is 1.99 in the domain of s? Try it with S, and read X after you clear the message.

## Answers

1. Yes: only 0 is left out of r's domain. The keys:

   ```keys E01 after=S09
   2 +/− XEQ R
   ```
   ```keys E01 after=S09 mode=35s,STU
   2 +/− XEQ R ENTER
   ```

   X shows <disp v="E01">-0.5000</disp>: r(−2) = 1/(−2).

2. Yes: 2.25 ≥ 2. The keys:

   ```keys E02 after=E01
   2.25 XEQ S
   ```
   ```keys E02 after=E01 mode=35s,STU
   2.25 XEQ S ENTER
   ```

   X shows <disp v="E02">0.5000</disp>: s(2.25) = √0.25, and 0.5 × 0.5 = 0.25.

3. No: 1.99 is below 2, however little. The keys:

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

   X shows <disp v="E03B">-0.0100</disp>: 1.99 − 2, the negative number the square root refused. S
   is stopped at its √x again, so press GOLD GTO . . before you key in a new program.
