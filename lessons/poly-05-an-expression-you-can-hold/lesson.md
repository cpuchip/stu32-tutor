---
id: poly-05
title: An expression you can hold
modes: STU
modes_reason: →X and →EQN are STU mode's alone (firmware 082: in 33s and 35s modes EQN LIST has no EQN MORE)
requires: setup shift-keys soft-keys stack-levels enter-copies swap-roll sto rcl clear-message eqn-typing xeq-check equation-list eqn-last-viewed polynomial expression eqn-power
status: draft prose (accuracy: not yet in lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# An expression you can hold

In poly-02 an expression lived in the equation list: you typed it there, and XEQ and SOLVE worked with it in
place. STU mode can also hand you a copy of it, to keep on the stack like a number, to store in a letter, and
to put back into the list. A copy held this way is still a rule, not a number: it has no value until $x$ has
one.

## From before

```item PL5F1
prompt: Work out $3x^{2} − 4$ at $x = 2$.
operands: 3, 2, 4, 2
topics: polynomial
answer: type
calculator: no
slip: PL5F1A | squared the 3x | $3x^{2}$ is 3 times $x^{2}$: square the 2 first, then times 3.
```

```item PL5F2
prompt: XEQ shows left minus right. For $4x − 1 = 9$ at $x = 3$, what does it show?
operands: 4, 1, 9, 3
topics: xeq-check
answer: type
calculator: no
slip: PL5F2A | right minus left | It is the left side minus the right side: $11 − 9$.
```

## Before you start

Every example carries on from the one before, on one calculator, from the setup:

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Onto the stack

Type an expression, with no = sign:

```keys B01
GOLD EQN 3 × RCL X yˣ 2 − 4 ENTER
```

The screen shows <disp v="B01" kind="drawn">3X^2-4</disp>. EQN LIST's last soft key, ▸, opens a second row of
keys for the list, EQN MORE. Its first key, →X, copies the expression shown into X:

```keys B02 after=B01
▸ →X
```

Equation mode closes, and the expression lands in X. X draws it as the list did:
<disp v="B02" kind="drawn">3X^2-4</disp>. The stack is back on the screen, and the list still holds its own copy.
→X takes one copy each time the list is open; for another, GOLD EQN opens the list again at the same entry.

## On one line in Y

ENTER copies X into Y, an expression as well as a number:

```keys B03 after=B02
ENTER
```

Only X is drawn. Y, Z and T write an expression on one line, in quotes, with every × shown: Y shows
<disp v="B03" kind="y">'3×X^2-4'</disp>. The quotes mark it as a rule, not a number.

## Not a number

Now type 2 and press ×, as if to double it:

```keys N01 after=B03
2 ×
```

The screen says <disp v="N01" kind="message">NOT A NUMBER</disp>, and nothing changes: X holds 2 and the
expression is still in Y. × needs two numbers, and the expression has no value until $x$ has one, which is what
XEQ gives it in the list (eq-01). C clears the message:

```keys N02 after=N01
C
```

## Keeping it in a letter

x↔y brings the expression down into X, and STO A stores it, just as it stores a number:

```keys K01 after=N02
x↔y STO A
```

C clears X. RCL A brings the expression back:

```keys K02 after=K01
C RCL A
```

X shows <disp v="K02" kind="drawn">3X^2-4</disp> again.

## Back into the list

Type a second expression into the list, $x + 1$:

```keys L01 after=K02
GOLD EQN RCL X + 1 ENTER
```

The list shows <disp v="L01" kind="drawn">X+1</disp>, and X still holds the expression from A. EQN MORE's second
key, →EQN, puts X's expression into the list just after the entry showing:

```keys L02 after=L01
▸ →EQN
```

The list shows <disp v="L02" kind="drawn">3X^2-4</disp>, its new third entry, and X keeps its copy. ▲ steps back to
the one before:

```keys L03 after=L02
▲
```

The list shows <disp v="L03" kind="drawn">X+1</disp>. C leaves Equation mode:

```keys L04 after=L03
C
```

X shows <disp v="L04" kind="drawn">3X^2-4</disp>, the copy it kept.

## Exercises

1. Type $2x + 5 = 11$, take it onto the stack with →X, and store it in B.
2. With that equation in X, type 7 and press ×. What does the screen say?
3. Recall B, type $x + 1$ into the list, and put B's equation in just after it.

## Answers

1. An equation can be held as well as an expression:

   ```keys E01
   GOLD EQN 2 × RCL X + 5 = 11 ENTER ▸ →X STO B
   ```

   X shows <disp v="E01" kind="drawn">2X+5=11</disp>.

2. The 7 lifts the equation into Y, and × cannot multiply a rule:

   ```keys E02 after=E01
   7 ×
   ```

   The screen says <disp v="E02" kind="message">NOT A NUMBER</disp>. C clears it:

   ```keys E02B after=E02
   C
   ```

3. Recall B before opening the list: in Equation mode, RCL types a letter into the equation. The new entry goes in
   after the one showing, and →EQN then puts B's equation after the new one:

   ```keys E03 after=E02B
   RCL B GOLD EQN RCL X + 1 ENTER ▸ →EQN
   ```

   The list shows <disp v="E03" kind="drawn">2X+5=11</disp>, after $x + 1$.

## Mixed review

```item PL5M1
prompt: Type $x^{2} − 2x$ into the list and XEQ it at $x = 5$. What does X show?
operands: 2, 2, 5
topics: expression
answer: type
calculator: yes
slip: PL5M1A | took 2 away, not 2x | The second term is $2x$: at $x = 5$ it is 10, so $25 − 10$.
```

```item PL5M2
prompt: Work out $\sqrt{81} − 4$.
topics: square-root
answer: type
calculator: no
slip: PL5M2A | halved 81 instead of its root | $\sqrt{81}$ asks which number times itself is 81: 9, then $9 − 4$.
```

```item PL5M3
prompt: Type $3x^{2} − 4$, take it onto the stack with →X, put it back with →EQN, and XEQ the copy at $x = 3$. What does X show?
operands: 3, 2, 4, 3
topics: eq-store
answer: type
calculator: yes
slip: PL5M3A | squared the 3x | $3x^{2}$ is 3 times $x^{2}$: $3 × 9$, then take away 4.
```

```item PL5M4
prompt: Work out $2^{5} − 3$.
topics: power
answer: type
calculator: no
slip: PL5M4A | multiplied instead of raising | $2^{5}$ is five 2s multiplied: 32.
```
