---
id: expr-02
title: Solving by undoing
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation calc-ans variable algebraic-expression evaluating multiply-first store-letter
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Thornwick and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Maren, Tobin
voices: story plain
---

# Solving by undoing

<voice v="story">Tobin's bill for an order of $n$ of the bakery's small pies is $3n + 5$ coins: 3 for each pie, and 5 for
carrying (expr-01). A customer paid 20 coins. How many pies did she order?</voice><voice v="plain">The bill for an order of $n$ small pies is $3n + 5$ coins: 3 for each pie, and 5 for
carrying (expr-01). A bill came to 20 coins. How many pies were ordered?</voice> Now the total is known and
the number of pies is not. To find it, undo what the rule did, step by step.

## From before

```item EP2F1
prompt: Evaluate $3n + 5$ when $n = 6$.
operands: 3, 5, 6
topics: evaluating
answer: type
calculator: no
slip: EP2F1A | added before multiplying | $3n$ means 3 times $n$: $3 × 6$ is 18, then + 5.
```

```item EP2F2
prompt: Work out $25 × 14$ by parts: $25 × 10$, then $25 × 4$.
operands: 25, 14
topics: partial-products
answer: type
calculator: no
slip: EP2F2A | added the 4 | The second part is $25 × 4$, which is 100, not 4.
```

## Before you start

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## An equation

$3n + 5 = 20$ says that the rule's answer is 20. A statement that two things are equal, with an = sign
between them, is an equation. Here $n$ is not a number that can be anything: it is one number we do not
know yet, an unknown. Solving the equation means finding it.

Look at what the rule does to $n$, in order: first it multiplies by 3, then it adds 5. To get back to $n$
from 20, undo those steps in the opposite order, the way you take off shoes before socks: socks went
on first and shoes last, so shoes come off first. The last thing done was "add 5", so undo it first:
take 5 away. Then undo "multiply by 3": divide by 3. Each undo is the opposite operation, the one that
takes you back: taking away undoes adding, and dividing undoes multiplying.

By hand: $20 − 5 = 15$, then $15 ÷ 3 = 5$. So $n = 5$. On the calculator, take 5 away from 20:

```keys U01 entry=alg
20 − 5 ENTER
```

```keys U01 entry=rpn
20 ENTER 5 −
```

The screen shows <disp v="U01">15.0000</disp>. Carrying on, divide what is there by 3:
<entry e="alg">an operation key straight after an answer starts the line with ANS:</entry><entry e="rpn">the 15 is on the stack, so type the 3 and ÷:</entry>

```keys U02 entry=alg after=U01
÷ 3 ENTER
```

```keys U02 entry=rpn after=U01
3 ÷
```

The screen shows <disp v="U02">5.0000</disp>: she ordered 5 pies.

```item U1T1
prompt: Solve $4n + 9 = 41$ by undoing the steps in the opposite order.
twin: U01
topics: undoing
answer: type
calculator: no
slip: U1T1A | divided first | The 9 was added last, so take it away first: $41 − 9 = 32$, then $32 ÷ 4$.
slip: U1T1B | stopped after one undo | $41 − 9 = 32$ undoes the + 9; the × 4 still has to be undone: $32 ÷ 4$.
```

Undo the two steps in the other order, the × 3 first and then the + 5, and see what happens:

```keys W01 entry=alg
20 ÷ 3 − 5 ENTER
```

```keys W01 entry=rpn
20 ENTER 3 ÷ 5 −
```

The screen shows <disp v="W01">1.6667</disp>: not even a whole number of pies. Undoing in the wrong order
does not take you back.

```why
ask: Why does undoing in the wrong order fail?
because: The rule multiplied by 3 and then added 5, so the 5 came last. Undoing has to take it away first, before the ÷ 3.
```

## Check by putting it back

An answer to an equation can always be checked: put it back into the rule and see whether it gives the
known total. $3 × 5 + 5$ should be 20:

```keys C01 entry=alg
3 × 5 + 5 ENTER
```

```keys C01 entry=rpn
3 ENTER 5 × 5 +
```

The screen shows <disp v="C01">20.0000</disp>. It does, so $n = 5$ is right.

## Another order of steps

<voice v="story">Maren shares a batch of $n$ rolls equally among 4 shelves, and then takes 2 rolls off one shelf for a
customer.</voice><voice v="plain">A batch of $n$ rolls is shared equally among 4 shelves, and then 2 rolls are taken off one shelf for a
customer.</voice> That shelf has 3 left: $n ÷ 4 − 2 = 3$. The rule divided by 4, then took 2 away. Undo in the
opposite order: first add the 2 back, then multiply by 4. By hand: $3 + 2 = 5$, then $5 × 4 = 20$.

```keys U03 entry=alg
3 + 2 ENTER
```

```keys U03 entry=rpn
3 ENTER 2 +
```

The screen shows <disp v="U03">5.0000</disp>. Carrying on, multiply by 4:

```keys U04 entry=alg after=U03
× 4 ENTER
```

```keys U04 entry=rpn after=U03
4 ×
```

The screen shows <disp v="U04">20.0000</disp>: the batch was 20 rolls. The check, $20 ÷ 4 − 2$:

```keys C02 entry=alg
20 ÷ 4 − 2 ENTER
```

```keys C02 entry=rpn
20 ENTER 4 ÷ 2 −
```

The screen shows <disp v="C02">3.0000</disp>, as it should.

```why
ask: Why put the answer back into the rule?
because: If 20 rolls shared among 4 shelves, less 2, leave 3, then 20 is right: the check runs the rule forward.
```

## Covering a part

There is a second way to look at an equation. Go back to $3n + 5 = 20$ and cover the $3n$ with a finger. What is
left reads: something plus 5 is 20. The something has to be 15, since $15 + 5 = 20$. So $3n$ is 15, and 3 times
what is 15? 5, the answer undoing gave.

Covering works on longer equations too. In $3 × (n + 2) − 5 = 25$, cover the part with the letter in it,
$3 × (n + 2)$. Something take away 5 is 25, so the something is 5 more than 25:

```keys K01 entry=alg
25 + 5 ENTER
```

```keys K01 entry=rpn
25 ENTER 5 +
```

The screen shows <disp v="K01">30.0000</disp>.

```why
ask: Why add the 5 to the 25, when the equation takes 5 away?
because: The covered part had 5 taken away and left 25, so before that it was 5 more than 25.
```

Now uncover one layer: $3 × (n + 2)$ is 30, so 3 times the bracket is 30, so the bracket is 30 divided by 3:

```keys K02 entry=alg after=K01
÷ 3 ENTER
```

```keys K02 entry=rpn after=K01
3 ÷
```

The screen shows <disp v="K02">10.0000</disp>. Inside the bracket, $n + 2$ is 10, so $n$ is 2 less than 10:

```keys K03 entry=alg after=K02
− 2 ENTER
```

```keys K03 entry=rpn after=K02
2 −
```

The screen shows <disp v="K03">8.0000</disp>: $n = 8$. Covering takes the same steps as undoing, from the outside
in, and each step answers one question: what must the covered part be?

The check for $n = 8$ puts it back, the bracket first, then × 3 and − 5:

```keys C03 entry=alg
8 + 2 ENTER × 3 − 5 ENTER
```

```keys C03 entry=rpn
8 ENTER 2 + 3 × 5 −
```

The screen shows <disp v="C03">25.0000</disp>, the equation's right side.

```item CV1T1
prompt: Solve $2 × (n + 4) − 3 = 17$ by covering: first the part with $n$ in it, then the bracket.
operands: 2, 4, 3, 17
twin: C03
topics: covering
answer: type
calculator: no
slip: CV1T1A | took the 3 away | The covered part had 3 taken away and left 17, so it is $17 + 3 = 20$, not $17 − 3$.
slip: CV1T1B | stopped at the bracket | 10 is $n + 4$, not $n$. Take the 4 away as well: $n = 10 − 4$.
```

Covering needs the letter to appear once, so that one part holds it. In $5n = 2n + 9$ the letter is on both sides,
there is no single part to cover, and neither covering nor undoing solves it as it stands. A later unit shows how.

## Exercises

Solve each by undoing, by hand first, then check by putting the answer back.

1. $2a + 7 = 31$.
2. $5b − 3 = 32$.
3. $c ÷ 3 + 4 = 10$.
4. <voice v="story">Tobin's bill for an order of the small pies was 41 coins</voice><voice v="plain">An order of the small pies cost 41 coins</voice> ($3n + 5$, as above). How many pies?

## Answers

1. The rule multiplied by 2, then added 7. Undo: $31 − 7 = 24$, then $24 ÷ 2 = 12$. Check: $2 × 12 + 7 = 31$.

   ```keys E01 entry=alg
   31 − 7 ENTER
   ```

   ```keys E01 entry=rpn
   31 ENTER 7 −
   ```

   The screen shows <disp v="E01">24.0000</disp>, and carrying on:

   ```keys E01B entry=alg after=E01
   ÷ 2 ENTER
   ```

   ```keys E01B entry=rpn after=E01
   2 ÷
   ```

   shows <disp v="E01B">12.0000</disp>. To check it with the calculator holding the answer,
   store 12 under A and work out $2a + 7$:

   ```keys E01C
   12 STO A
   ```

   ```keys E01D entry=alg after=E01C
   2 × RCL A + 7 ENTER
   ```

   ```keys E01D entry=rpn after=E01C
   2 ENTER RCL A × 7 +
   ```

   The screen shows <disp v="E01D">31.0000</disp>, the equation's right side.

2. The rule multiplied by 5, then took 3 away. Undo: add the 3 back, $32 + 3 = 35$, then $35 ÷ 5 = 7$.
   Check: $5 × 7 − 3 = 32$.

   ```keys E02 entry=alg
   32 + 3 ENTER
   ```

   ```keys E02 entry=rpn
   32 ENTER 3 +
   ```

   The screen shows <disp v="E02">35.0000</disp>, and carrying on:

   ```keys E02B entry=alg after=E02
   ÷ 5 ENTER
   ```

   ```keys E02B entry=rpn after=E02
   5 ÷
   ```

   shows <disp v="E02B">7.0000</disp>.

3. The rule divided by 3, then added 4. Undo: $10 − 4 = 6$, then $6 × 3 = 18$. Check: $18 ÷ 3 + 4 = 10$.

   ```keys E03 entry=alg
   10 − 4 ENTER
   ```

   ```keys E03 entry=rpn
   10 ENTER 4 −
   ```

   The screen shows <disp v="E03">6.0000</disp>, and carrying on:

   ```keys E03B entry=alg after=E03
   × 3 ENTER
   ```

   ```keys E03B entry=rpn after=E03
   3 ×
   ```

   shows <disp v="E03B">18.0000</disp>.

4. $3n + 5 = 41$. Undo the + 5, then the × 3: $41 − 5 = 36$, and $36 ÷ 3 = 12$ pies. Check: $3 × 12 + 5 = 41$.

   ```keys E04 entry=alg
   41 − 5 ENTER
   ```

   ```keys E04 entry=rpn
   41 ENTER 5 −
   ```

   The screen shows <disp v="E04">36.0000</disp>, and carrying on:

   ```keys E04B entry=alg after=E04
   ÷ 3 ENTER
   ```

   ```keys E04B entry=rpn after=E04
   3 ÷
   ```

   shows <disp v="E04B">12.0000</disp>: 12 pies.

## Mixed review

```item EP2M1
prompt: Solve $4x + 6 = 30$ by undoing.
topics: undoing
answer: type
calculator: no
slip: EP2M1A | undid in the wrong order | The rule multiplied by 4, then added 6: undo the + 6 first, then ÷ 4.
```

```item EP2M2
prompt: Work out $20 − 3 × 4$.
topics: multiply-first
answer: type
calculator: no
slip: EP2M2A | took away first | Multiplying comes before taking away: $3 × 4$ is 12, then $20 − 12$.
```

```item EP2M3
prompt: Is $n = 7$ a solution of $3n − 2 = 19$? Put it back: what is $3 × 7 − 2$?
operands: 7, 3, 2, 19
topics: check-by-putting-back
answer: type
calculator: no
slip: EP2M3A | added the 2 | It is $3 × 7$ minus 2: $21 − 2$.
```

```item EP2M4
prompt: 100 rolls go 8 to a box. How many full boxes?
topics: quotient-remainder
answer: type
calculator: no
slip: EP2M4A | the rolls left over, not the boxes | 12 boxes of 8 hold 96, with 4 left over: 12 full boxes.
```

## Checkpoint

Questions on the whole unit.

```item CPP2A
prompt: Work out $5n + 3$ when $n$ is 8.
topics: evaluating
answer: type
calculator: no
slip: CPP2A1 | read 5n as 5 + n | $5n$ means 5 times $n$: $5 × 8$ first, then add 3.
slip: CPP2A2 | added before multiplying | Multiply before you add: $5 × 8$ is 40, then $40 + 3$. Brackets would be needed to add first.
```

```item CPP2B
prompt: Solve $6x − 9 = 33$ by undoing.
topics: undoing
answer: type
calculator: no
slip: CPP2B1 | took the 9 away instead of adding it | The rule took 9 away, so undo it by adding 9: $33 + 9$, then ÷ 6.
slip: CPP2B2 | undid the × 6 first | Undo in the opposite order: the − 9 was done last, so undo it first.
```

```item CPP2C
prompt: Solve $n ÷ 3 + 5 = 12$ by undoing.
topics: undoing
answer: type
calculator: no
slip: CPP2C1 | undid in the wrong order | The + 5 was done last, so undo it first: $12 − 5$, then × 3.
slip: CPP2C2 | added the 5 instead of taking it away | The rule added 5, so undo it by taking 5 away: $12 − 5$ is 7.
```
