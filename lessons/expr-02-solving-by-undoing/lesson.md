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
---

# Solving by undoing

Tobin's bill for an order of n of the bakery's small pies is 3n + 5 coins: 3 for each pie, and 5 for
carrying (expr-01). A customer paid 20 coins. How many pies did she order? Now the total is known and
the number of pies is not. This lesson finds it by undoing, step by step, what the rule did.

## Before you start

The setup from start-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## An equation

3n + 5 = 20 says that the rule's answer is 20. A statement that two things are equal, with an = sign
between them, is an equation. Here n is not a number that can be anything: it is one number we do not
know yet, an unknown. Solving the equation means finding it.

Look at what the rule does to n, in order: first it multiplies by 3, then it adds 5. To get back to n
from 20, undo those steps in the opposite order, the way you take off shoes before socks: socks went
on first and shoes last, so shoes come off first. The last thing done was "add 5", so undo it first:
take 5 away. Then undo "multiply by 3": divide by 3. Each undo is the opposite operation, the one that
takes you back: taking away undoes adding, and dividing undoes multiplying.

By hand: 20 − 5 = 15, then 15 ÷ 3 = 5. So n = 5. On the calculator, take 5 away from 20:

```keys U01 entry=alg
20 − 5 ENTER
```

```keys U01 entry=rpn
20 ENTER 5 −
```

The screen shows <disp v="U01">15.0000</disp>. Carrying on, divide what is there by 3:
<entry e="alg">an operation key straight after an answer starts the line with ANS (start-01):</entry><entry e="rpn">the 15 is on the stack, so type the 3 and ÷:</entry>

```keys U02 entry=alg after=U01
÷ 3 ENTER
```

```keys U02 entry=rpn after=U01
3 ÷
```

The screen shows <disp v="U02">5.0000</disp>: she ordered 5 pies. Found.

The order matters. Undo the × 3 first, and then the + 5, and see what happens:

```keys W01 entry=alg
20 ÷ 3 − 5 ENTER
```

```keys W01 entry=rpn
20 ENTER 3 ÷ 5 −
```

The screen shows <disp v="W01">1.6667</disp>: not even a whole number of pies. Undoing in the wrong order
does not take you back.

## Check by putting it back

An answer to an equation can always be checked: put it back into the rule and see whether it gives the
known total. 3 × 5 + 5 should be 20:

```keys C01 entry=alg
3 × 5 + 5 ENTER
```

```keys C01 entry=rpn
3 ENTER 5 × 5 +
```

The screen shows <disp v="C01">20.0000</disp>. It does, so n = 5 is right.

## Another order of steps

Maren shares a batch of n rolls equally among 4 shelves, and then takes 2 rolls off one shelf for a
customer. That shelf has 3 left: n ÷ 4 − 2 = 3. The rule divided by 4, then took 2 away. Undo in the
opposite order: first add the 2 back, then multiply by 4. By hand: 3 + 2 = 5, then 5 × 4 = 20.

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

The screen shows <disp v="U04">20.0000</disp>: the batch was 20 rolls. The check, 20 ÷ 4 − 2:

```keys C02 entry=alg
20 ÷ 4 − 2 ENTER
```

```keys C02 entry=rpn
20 ENTER 4 ÷ 2 −
```

The screen shows <disp v="C02">3.0000</disp>, as it should.

## Exercises

Solve each by undoing, by hand first, then check by putting the answer back.

1. 2a + 7 = 31.
2. 5b − 3 = 32.
3. c ÷ 3 + 4 = 10.
4. Tobin's bill for an order of the small pies was 41 coins (3n + 5, as above). How many pies?

## Answers

1. The rule multiplied by 2, then added 7. Undo: 31 − 7 = 24, then 24 ÷ 2 = 12. Check: 2 × 12 + 7 = 31.

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

   shows <disp v="E01B">12.0000</disp>. To check it with the calculator holding the answer (expr-01),
   store 12 under A and work out 2a + 7:

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

2. The rule multiplied by 5, then took 3 away. Undo: add the 3 back, 32 + 3 = 35, then 35 ÷ 5 = 7.
   Check: 5 × 7 − 3 = 32.

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

3. The rule divided by 3, then added 4. Undo: 10 − 4 = 6, then 6 × 3 = 18. Check: 18 ÷ 3 + 4 = 10.

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

4. 3n + 5 = 41. Undo the + 5, then the × 3: 41 − 5 = 36, and 36 ÷ 3 = 12 pies. Check: 3 × 12 + 5 = 41.

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
