---
id: sys-02
title: The built-in solvers
requires: setup shift-keys soft-keys stack-levels change-sign rcl letter-keys view clear-message equation-list eqn-last-viewed solve-prompts system check-pair elimination no-or-every-solution
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
modes: 35s STU
modes_reason: In 33s mode, as on an HP 33s, the equation list has no built-in solvers (firmware 041).
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The built-in solvers

sys-01 solved two equations in two unknowns by elimination. For two equations in two unknowns, or
three in three, the calculator has solvers of its own. They work on linear equations: each unknown is
only multiplied by a number, never squared, divided into or multiplied by another unknown ("lin." on
the screen is short for linear). And they take each equation in one form: the unknowns on the left,
in the order x, y, z, each times a number, and a number on the right. Two equations are
Ax + By = C and Dx + Ey = F, and the solver asks for the six numbers A to F. Three are
Ax + By + Cz = D, Ex + Fy + Gz = H and Ix + Jy + Kz = L, twelve numbers, A to L. The letters are
variables, so C in Ax + By = C is not the C key, and it means a different number in the 3×3 form.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. This lesson is offered in 35s and STU mode: in
33s mode, as on an HP 33s, the solvers are not there, so if you chose 33s, choose 35s or STU in the
setup for this lesson. The whole lesson is one chain: each example carries on from the one before,
because the equation list remembers where you left it. "X shows" means the bottom line of the screen,
and "the variable X" means the letter, as in sys-01. The solvers keep the numbers you give them in the
variables A to L, and the answers in X, Y and Z, so they replace whatever those variables held.

In the equation list, the first two soft keys are ▲ and ▼, which step up and down the list. The list
holds two entries of its own besides your equations. Going down from EQN LIST TOP, it has your
equations, then the 2×2 solver, then the 3×3 solver, and then the top again: the list goes round. The
screen writes 2×2 as 2*2, with * for ×.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## The 2×2 solver

Open the list. It may open at one of your equations, so press NEW, the fourth soft key, which goes to
EQN LIST TOP wherever the list opened, and keeps your equations:

```keys T01Z
GOLD EQN NEW
```

From the top, ▲ goes up to the 3×3 solver and ▲ again to the 2×2, however many equations you have:

```keys T01A after=T01Z
▲ ▲
```

The X line shows <disp v="T01A" kind="eqn">2*2 lin. solve</disp>. SOLVE runs it. Unlike eq-02's SOLVE
W, you press no letter after it: it asks for the six numbers in turn, A first.

```keys T01B after=T01A
GOLD SOLVE
```

The line above X asks <disp v="T01B" kind="prompt">A?</disp>, and X shows the number the variable A
holds now. Type each number and press R/S. The tickets of sys-01, 2x + 3y = 37 and x + y = 15, give
A = 2, B = 3, C = 37, D = 1, E = 1 and F = 15:

```keys T01 after=T01B
2 R/S 3 R/S 37 R/S 1 R/S 1 R/S 15 R/S
```

The X line shows <disp v="T01" kind="view">X=8.0000</disp>: x = 8. The answers are shown one at a
time, and ▼ steps to the next:

```keys T02 after=T01
▼
```

The X line shows <disp v="T02" kind="view">Y=7.0000</disp>, the answer sys-01 found by elimination.
C leaves the view, as it leaves VIEW's (rpn-02):

```keys T03 after=T02
C
```

X shows <disp v="T03">8.0000</disp>. The answers are on the stack, x in X and y in Y (rpn-01's levels),
and in the variables X and Y. So sys-01's check works straight away, 2x + 3y:

```keys T04 after=T03
2 RCL X × 3 RCL Y × +
```

X shows <disp v="T04">37.0000</disp>, the first equation's right side.

## Keeping a number

sys-01's fruit stall: 0.75x + 1.25y = 6.5 and x + y = 6. EQN opens at the last entry you viewed
(eq-02), which is the 2×2 solver:

```keys F01A after=T04
GOLD EQN
```

The X line shows <disp v="F01A" kind="eqn">2*2 lin. solve</disp>. SOLVE:

```keys F01B after=F01A
GOLD SOLVE
```

It asks <disp v="F01B" kind="prompt">A?</disp>, and X shows <disp v="F01B">2.0000</disp>, the A of
the tickets. R/S on its own keeps the number shown, as SOLVE's prompts did in eq-02. Here D and E are
1 and 1, as the tickets' were, so R/S alone keeps them:

```keys F01 after=F01B
0.75 R/S 1.25 R/S 6.5 R/S R/S R/S 6 R/S
```

The X line shows <disp v="F01" kind="view">X=2.0000</disp>, two apples; the stack's Y and the variable
Y hold 4, four pears.

## Into the solver's form

An equation that is not in the solver's form is rearranged first, as sys-01 rearranged equations into
y = mx + b, only the other way. Take y = 2x + 1 and x + y = 7. Take 2x from both sides of the first:
−2x + y = 1. Now A = −2, B = 1 and C = 1, and the second is already D = 1, E = 1, F = 7. A negative
number is typed with +/−, and D and E are 1 and 1 still, so R/S keeps them:

```keys R01 after=F01
C GOLD EQN GOLD SOLVE 2 +/− R/S 1 R/S 1 R/S R/S R/S 7 R/S
```

The X line shows <disp v="R01" kind="view">X=2.0000</disp>, and y is 5: 2 × 2 + 1 is 5, and 2 + 5 is 7.
An unknown that an equation does not have is there times 0, so its number is typed as 0.

## Three equations

At a market, three shoppers buy apples by the kilo, loaves of bread and cheeses. The first pays 9.50
dollars for 2 kilos of apples, a loaf and a cheese; the second pays 10 dollars for a kilo of apples, 2
loaves and a cheese; the third pays 12.50 dollars for a kilo of apples, a loaf and 2 cheeses. With x,
y and z the three prices: 2x + y + z = 9.5, x + 2y + z = 10 and x + y + 2z = 12.5.

C leaves the view, and EQN opens at the 2×2 solver again. The 3×3 solver is the next entry down:

```keys M01A after=R01
C GOLD EQN ▼
```

The X line shows <disp v="M01A" kind="eqn">3*3 lin. solve</disp>. SOLVE asks for A to L, a row of
four numbers for each equation:

```keys M01 after=M01A
GOLD SOLVE 2 R/S 1 R/S 1 R/S 9.5 R/S 1 R/S 2 R/S 1 R/S 10 R/S 1 R/S 1 R/S 2 R/S 12.5 R/S
```

The X line shows <disp v="M01" kind="view">X=1.5000</disp>. Then

```keys M02 after=M01
▼
```

shows <disp v="M02" kind="view">Y=2.0000</disp>, and

```keys M03 after=M02
▼
```

<disp v="M03" kind="view">Z=4.5000</disp>. Apples are 1.50 dollars a kilo, a loaf 2.00 and a cheese
4.50. Check the first shopper in your head: 2 × 1.50 + 2.00 + 4.50 is 9.50.

## No solution, or every solution

sys-01's two awkward cases go to the 2×2 solver too. EQN now opens at the 3×3 solver, and ▲ goes up
to the 2×2:

```keys N01A after=M03
C GOLD EQN ▲
```

The X line shows <disp v="N01A" kind="eqn">2*2 lin. solve</disp>. The parallel lines x + y = 3 and
x + y = 5:

```keys N01 after=N01A
GOLD SOLVE 1 R/S 1 R/S 3 R/S 1 R/S 1 R/S 5 R/S
```

The screen shows <disp v="N01" kind="message">NO SOLUTION</disp>. Clear it with C. Now the same line
twice, x + y = 3 and 2x + 2y = 6. Its first equation is the one just typed, so R/S keeps A, B and C:

```keys N02A after=N01
C GOLD EQN
```

```keys N02 after=N02A
GOLD SOLVE R/S R/S R/S 2 R/S 2 R/S 6 R/S
```

The screen shows <disp v="N02" kind="message">MULT SOLUTION</disp>: many solutions, endlessly many,
every point of one line, as in sys-01. Here the line is the first equation, x + y = 3.

## Exercises

1. Solve 3x + 2y = 16 and x + y = 6 with the 2×2 solver (sys-01's first exercise, by hand there).
   Watch what the prompts show before you keep a number.
2. Solve x + y + z = 6, 2x − y + z = 3 and x + 2y − z = 2 with the 3×3 solver.
3. What does the 2×2 solver say about 2x − y = 1 and 4x − 2y = 5 (sys-01's second exercise)?
4. Solve x + y = 5, y + z = 7 and x + z = 6 with the 3×3 solver.

## Answers

1. x = 4 and y = 2. C clears the last message, and EQN opens at the 2×2 solver. D? and E? show 2, the
   2x + 2y of the last example, so type 1 and 1; F? shows 6, which is right, so R/S keeps it:

   ```keys E01 after=N02
   C GOLD EQN GOLD SOLVE 3 R/S 2 R/S 16 R/S 1 R/S 1 R/S R/S
   ```

   The X line shows <disp v="E01" kind="view">X=4.0000</disp>, and y is 2, as sys-01 found.

2. x = 1, y = 2 and z = 3. The 3×3 solver is one ▼ from the 2×2, and a −1 is typed 1 +/−:

   ```keys E02 after=E01
   C GOLD EQN ▼ GOLD SOLVE 1 R/S 1 R/S 1 R/S 6 R/S 2 R/S 1 +/− R/S 1 R/S 3 R/S 1 R/S 2 R/S 1 +/− R/S 2 R/S
   ```

   The X line shows <disp v="E02" kind="view">X=1.0000</disp>, and y and z are 2 and 3. Check the
   second equation: 2 × 1 − 2 + 3 = 3.

3. No solution. One ▲ from the 3×3 solver is the 2×2:

   ```keys E03 after=E02
   C GOLD EQN ▲ GOLD SOLVE 2 R/S 1 +/− R/S 1 R/S 4 R/S 2 +/− R/S 5 R/S
   ```

   The screen shows <disp v="E03" kind="message">NO SOLUTION</disp>: the lines are parallel, as sys-01
   showed by elimination.

4. x = 2, y = 3 and z = 4. Each equation lacks one unknown, which is there times 0: x + y + 0z = 5,
   0x + y + z = 7 and x + 0y + z = 6.

   ```keys E04 after=E03
   C GOLD EQN ▼ GOLD SOLVE 1 R/S 1 R/S 0 R/S 5 R/S 0 R/S 1 R/S 1 R/S 7 R/S 1 R/S 0 R/S 1 R/S 6 R/S
   ```

   The X line shows <disp v="E04" kind="view">X=2.0000</disp>, and y and z are 3 and 4: 2 + 3 is 5,
   3 + 4 is 7, and 2 + 4 is 6.
