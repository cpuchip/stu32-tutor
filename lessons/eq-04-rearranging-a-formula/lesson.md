---
id: eq-04
title: Rearranging a formula
modes: STU
modes_reason: Casimir, the algebra system that rearranges a formula, is STU mode's alone (CAS 004, 038)
requires: setup shift-keys soft-keys sto rcl clear-message eqn-typing xeq-check equation-list eqn-last-viewed solve solve-any-letter mult-before-add fraction-bar
status: draft prose (accuracy: not yet in lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Rearranging a formula

In eq-02, Solving a formula for any letter, SOLVE asked for every other letter and gave back one number.
Ask again with other values and it works the whole thing out again. Rearranging a formula does the work
once. It writes the letter you want in terms of the others, and that rule answers for every value at once.
In an electric circuit, $V = I × R$ ties the voltage, $V$, to the current, $I$, and the resistance, $R$.
Rearranged for $R$, it says how to find the resistance from any voltage and any current.

## From before

```item EQ4F1
prompt: A rectangle has $A = L × W$, with an area of 36 and a length of 4. What is its width?
operands: 36, 4
topics: solve-any-letter
answer: type
calculator: no
slip: EQ4F1A | multiplied | The formula says 4 times the width is 36, so the width is $36 ÷ 4$.
```

```item EQ4F2
prompt: Work out $(35 − 5) ÷ 6$: the whole top over the bottom.
operands: 35, 5, 6
topics: fraction-bar
answer: type
calculator: no
slip: EQ4F2A | divided only the 5 by the 6 | The bracket comes first: $35 − 5$ is 30, and $30 ÷ 6$.
```

## Before you start

Every example carries on from the one before, on one calculator, from the setup. Some sections start a
new equation, and the text says so.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## By hand

$V = I × R$ says that $R$ is multiplied by $I$. To get $R$ on its own, undo the times $I$, and do it
to both sides so that they stay equal: divide both sides by $I$. That leaves
$V ÷ I = R$, which is the same as $R = V ÷ I$.

Check it by putting numbers back. Take $V = 12$ and $I = 3$. The rule gives $R = 12 ÷ 3 = 4$, and
$I × R = 3 × 4 = 12$, which is $V$. This works on any calculator, or with none: the same step on both sides,
until the letter you want is on its own.

## With Casimir

Casimir, STU mode's algebra system, can do the rearranging. Type the formula. RCL and a letter's key give the
letter, as before:

```keys C01
GOLD EQN RCL V = RCL I × RCL R ENTER CAS ▸ SOLVE R
```

With an equation showing, the list's fifth soft key, CAS, opens Casimir's menu. Its last key, ▸, opens a
second row of keys, which starts with SOLVE. SOLVE asks which letter, and R answers. Casimir's SOLVE asks
for no values. It answers with a report, one row at a time, and the first row says how it went:
<disp v="C01" kind="message">SOLVED</disp>. ▼ moves down a row:

```keys C02 after=C01
▼
```

The screen shows <disp v="C02" kind="message">R=V÷I</disp>, the rule found by hand. One more row:

```keys C03 after=C02
▼
```

The screen shows <disp v="C03" kind="message">I≠0</disp>: $I$ is not 0. The answer holds only where that is
true. Each row after the answer is a condition like this one.

## Checking the rule

The report's answer can check itself. C closes the report, and C again closes the list. Store the
numbers from before:

```keys K01 after=C03
C C 12 STO V 3 STO I
```

GOLD EQN shows the formula again. Solve it once more, move down to the answer, and press EVAL, the
report's third soft key:

```keys K02 after=K01
GOLD EQN CAS ▸ SOLVE R ▼ EVAL
```

EVAL on the answer's row works it out with the values the letters hold, and X shows <disp v="K02">4.0000</disp>:
$12 ÷ 3$, the resistance found by hand. ENTER on that row does something else: it copies the rule
itself, $V ÷ I$, into X.

## Why the row is there

Now store 0 in $I$ and try the same thing:

```keys K03 after=K02
0 STO I GOLD EQN CAS ▸ SOLVE R ▼ EVAL
```

This time the screen shows <disp v="K03" kind="message">CONDITION FAILS</disp>, and nothing goes into X. C
clears the message, and the report shows the row that failed:

```keys K04 after=K03
C
```

The screen shows <disp v="K04" kind="message">I≠0</disp>. Here is why. At $I = 0$, $I × R$ is 0 for every
$R$. So $V = I × R$ holds for every $R$ when $V = 0$, and for none when $V ≠ 0$. Either way there is no one
answer, and $V ÷ 0$ is no number at all. The rule $R = V ÷ I$ is right everywhere else. C twice more closes
the report and the list:

```keys K05 after=K04
C C
```

```why
ask: With $I = 0$ and $V = 0$, why is every $R$ an answer?
because: $I × R$ is $0 × R$, which is 0 whatever $R$ is, and $V$ is 0 too, so the two sides are equal for every $R$.
```

## A formula with no row

A circle's circumference is $C = 2 × π × R$, where $R$ is its radius. This example starts a new
equation, and π is GOLD π.

```keys N01
GOLD EQN RCL C = 2 × GOLD π × RCL R ENTER CAS ▸ SOLVE R
```

The report starts with <disp v="N01" kind="message">SOLVED</disp>. Down a row:

```keys N02 after=N01
▼
```

The screen shows <disp v="N02" kind="message">R=C÷2÷π</disp>: $C$ divided by 2, then by π. Down again:

```keys N03 after=N02
▼
```

The report is back at <disp v="N03" kind="message">SOLVED</disp>. There was no row after the answer,
because this rule has nothing to fail: it divides by 2 and by π, and neither is ever 0.

## The same answer, another form

To turn degrees Celsius into degrees Fahrenheit, Solving a formula for any letter used
$F = 1.8 × C + 32$. Rearrange it by hand for $C$. Take 32 from both sides, $F − 32 = 1.8 × C$, then
divide both sides by 1.8: $C = (F − 32) ÷ 1.8$. Now ask Casimir. C twice closes the report and the list,
and 212 goes into $F$ for a check:

```keys F01 after=N03
C C 212 STO F
```

Then the formula, with SOLVE for $C$, and down to the answer:

```keys F02 after=F01
GOLD EQN RCL F = 1.8 × RCL C + 32 ENTER CAS ▸ SOLVE C ▼
```

The screen shows <disp v="F02" kind="message">C=5×F÷9-160÷9</disp>. That does not look like
$(F − 32) ÷ 1.8$, but it is the same rule. Dividing by 1.8 is the same as multiplying by 5 and dividing by 9,
because $1.8 = 9 ÷ 5$. So $(F − 32) ÷ 1.8$ is $5 × F ÷ 9 − 5 × 32 ÷ 9$, and $5 × 32 = 160$. EVAL puts in
the 212 held in $F$:

```keys F03 after=F02
EVAL
```

X shows <disp v="F03">100.0000</disp>. By hand, $(212 − 32) ÷ 1.8 = 180 ÷ 1.8 = 100$: the boiling point of
water, both ways. Two answers that look different can be one rule. Putting the same numbers into both is a
quick way to see it.

## When Casimir says no

Casimir rearranges a formula only when the letter you want is to the first power: no square, and nothing
like SIN around it. This starts a new equation, $x^{2} = A$, solved for $x$:

```keys W01 after=F03
GOLD EQN RCL X yˣ 2 = RCL A ENTER CAS ▸ SOLVE X
```

The screen shows <disp v="W01" kind="message">COEF NOT NUMERIC</disp>: with a square, Casimir needs numbers
beside $x$, not letters. By hand there are two answers, $\sqrt{A}$ and $−\sqrt{A}$, for an $A$ above 0.
When it says no, rearrange by hand, or give the other letters numbers and use SOLVE as in Solving a
formula for any letter. C twice clears the message and closes the list:

```keys W02 after=W01
C C
```

## Exercises

1. Distance is rate times time, $D = R × T$. Rearrange it for $T$ by hand, then with Casimir. What row
   comes after the answer, and why?
2. A rectangle's area is $A = L × W$. Rearrange it for $W$ with Casimir. Then check the rule with the
   rectangle from Solving a formula for any letter, an area of 42 and a length of 12.

## Answers

1. By hand, divide both sides by $R$: $T = D ÷ R$. Then with Casimir:

   ```keys E01 after=W02
   GOLD EQN RCL D = RCL R × RCL T ENTER CAS ▸ SOLVE T ▼
   ```

   The screen shows <disp v="E01" kind="message">T=D÷R</disp>. One row down:

   ```keys E01B after=E01
   ▼
   ```

   The screen shows <disp v="E01B" kind="message">R≠0</disp>: a rate of 0 covers no distance in any time,
   so there is no one time to find.

2. The same steps for $W$, after C twice to close the report and the list:

   ```keys E02 after=E01B
   C C GOLD EQN RCL A = RCL L × RCL W ENTER CAS ▸ SOLVE W ▼
   ```

   The screen shows <disp v="E02" kind="message">W=A÷L</disp>, and its row is $L ≠ 0$. To check, close
   the report and the list, store 42 in $A$ and 12 in $L$, and EVAL on the answer:

   ```keys E02B after=E02
   C C 42 STO A 12 STO L GOLD EQN CAS ▸ SOLVE W ▼ EVAL
   ```

   X shows <disp v="E02B">3.5000</disp>, the width SOLVE found there.

## Mixed review

```item EQ4M1
prompt: In $V = I × R$, take $I = 0$ and $V = 5$, and try $R = 7$. What is $I × R$?
operands: 0, 5, 7
topics: solve-rows
answer: type
calculator: no
slip: EQ4M1A | multiplied V by R | It is $I$ times $R$, and $I$ is 0: $0 × 7$. That is not 5, so $R = 7$ fails, and so does every $R$.
```

```item EQ4M2
prompt: Work out $3 + 4 × 5$.
topics: mult-before-add
answer: type
calculator: no
slip: EQ4M2A | added first | Multiplication comes before addition: $4 × 5$ is 20, then $3 + 20$.
```

```item EQ4M3
prompt: A square's perimeter is $P = 4 × S$. Rearrange it for $S$, then find $S$ when $P = 26$.
operands: 4, 26
topics: rearrange-by-hand
answer: type
calculator: no
slip: EQ4M3A | multiplied | $S$ is multiplied by 4, so undo it by dividing: $26 ÷ 4$.
```

```item EQ4M4
prompt: For $5x − 7 = 8$, what is left minus right at $x = 3$?
operands: 5, 7, 8, 3
topics: xeq-check
answer: type
calculator: no
slip: EQ4M4A | the left side alone | Left minus right: $5 × 3 − 7$ is 8, and $8 − 8$.
```
