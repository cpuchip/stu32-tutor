---
id: poly-02
title: Roots with SOLVE
requires: setup shift-keys display-rounds power clear-message eqn-typing xeq-check solve solve-guesses graph-by-hand polynomial
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Roots with SOLVE

A root of a polynomial, also called a zero, is a value of x where the polynomial is 0. On its graph,
it is where the curve meets the x axis. This lesson finds the roots of

c(x) = x³ − 6x² + 11x − 6

with SOLVE from eq-01. SOLVE finds one root at a time, usually the one near the two guesses you give
it (eq-03). So the work is in deciding where to look, and in knowing when you have found them all.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. The examples about c are one chain, each carrying on from
the one before; the one about x² + 1 starts fresh, and so does the exercise.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Typing c

Equation mode, as in eq-01, with yˣ for the powers. c has no = sign, as the expression in fn-02's
TABLE section had none: SOLVE treats an expression on its own as equal to 0, and XEQ gives its
value.

```keys R01
GOLD EQN RCL X yˣ 3 − 6 × RCL X yˣ 2 + 11 × RCL X − 6 ENTER
```

The screen shows <disp v="R01" kind="eqn">X^3-6×X^2+11×X-6</disp>.

## Where to look

Work out c at a few values of x with XEQ, as in eq-01, and watch the sign. At 0:

```keys R02 after=R01
XEQ 0 R/S
```

X shows <disp v="R02">-6.0000</disp>. XEQ leaves Equation mode, so show the equation again each time.
At 1.5:

```keys R03 after=R02
GOLD EQN XEQ 1.5 R/S
```

X shows <disp v="R03">0.3750</disp>. At 2.5:

```keys R04 after=R03
GOLD EQN XEQ 2.5 R/S
```

X shows <disp v="R04">-0.3750</disp>. At 4:

```keys R05 after=R04
GOLD EQN XEQ 4 R/S
```

X shows <disp v="R05">6.0000</disp>.

| x | 0 | 1.5 | 2.5 | 4 |
|---|---|---|---|---|
| c(x) | −6 | 0.375 | −0.375 | 6 |

The sign changes three times: from 0 to 1.5, from 1.5 to 2.5, and from 2.5 to 4. A polynomial's
graph is one unbroken curve, so to get from below the x axis to above it, it must cross the axis
somewhere in between. Each change of sign marks at least one root inside that gap.

How many roots can there be? Each root r goes with a factor x − r: if c(r) = 0, then c(x) can be
written as (x − r) times a polynomial of one degree less. Three roots would use up all three
degrees of c, so a polynomial of degree 3 has at most three roots, and in general a polynomial of
degree n has at most n. c has three gaps with a root in each, so those are all of its roots.

The other way round is not true: no sign change does not mean no root. (x − 2)² is 0 at x = 2 but
positive on both sides of it; its graph touches the axis there without crossing. A gap can also hide
two roots, the curve crossing down and back up between two values where the sign is the same. Try
more values when the count does not add up.

## One root in each gap

Give SOLVE the two ends of a gap as its guesses: the first stored in X, the second on the X line,
as eq-03 does. XEQ has left Equation mode, so STO works straight away. The first gap:

```keys S01 after=R05
0 STO X 1.5 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="S01" kind="view">X=1.0000</disp>. The second gap:

```keys S02 after=S01
1.5 STO X 2.5 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="S02" kind="view">X=2.0000</disp>. The third:

```keys S03 after=S02
2.5 STO X 4 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="S03" kind="view">X=3.0000</disp>. The roots are 1, 2 and 3, and indeed
c(x) = (x − 1)(x − 2)(x − 3): multiply it out to check.

SOLVE works by trying values of x and narrowing in on the root, and it stops when it is close
enough. So a root it finds can be off in its last digit. The calculator keeps 34 significant digits
(rpn-03), and the third root here is 3.000…0003: every one of those digits is right except the
34th, which is 3 where the exact root has 0. FIX 4 shows only the first few digits, all of them
right. It is a reminder that SOLVE's answers come from searching, not from a formula.

## A polynomial with no real root

Not every polynomial crosses the x axis. x² + 1 is never less than 1, since x² is never negative,
so it is never 0. Ask SOLVE anyway:

```keys N01
GOLD EQN RCL X yˣ 2 + 1 ENTER GOLD SOLVE X
```

The screen shows <disp v="N01" kind="message">NO ROOT FND</disp>: SOLVE searched and found no root.
None exists among the real numbers, the only numbers these lessons have used so far. x² + 1 does
have roots, but they are complex numbers, which poly-04 meets. Clear the message with C before you
go on<mode m="35s,STU">: in this mode a key pressed while a message shows only clears it, so the
next example's first key would be lost</mode>.

```keys N02 after=N01
C
```

## Exercise

Find all the roots of d(x) = x³ − 3x + 1. Start by working out d at the whole numbers from −2 to 2,
find where the sign changes, and use SOLVE in each gap. d has no x² term: type only the terms it
has.

## Answer

Type d:

```keys E01
GOLD EQN RCL X yˣ 3 − 3 × RCL X + 1 ENTER
```

Then its values at −2, −1, 0, 1 and 2:

```keys E01A after=E01
XEQ 2 +/− R/S
```

X shows <disp v="E01A">-1.0000</disp>.

```keys E01B after=E01A
GOLD EQN XEQ 1 +/− R/S
```

X shows <disp v="E01B">3.0000</disp>.

```keys E01C after=E01B
GOLD EQN XEQ 0 R/S
```

X shows <disp v="E01C">1.0000</disp>.

```keys E01D after=E01C
GOLD EQN XEQ 1 R/S
```

X shows <disp v="E01D">-1.0000</disp>.

```keys E01E after=E01D
GOLD EQN XEQ 2 R/S
```

X shows <disp v="E01E">3.0000</disp>. The sign changes from −2 to −1, from 0 to 1, and from 1 to 2:
three gaps, and d has degree 3, so one root in each and no more. Between −1 and 0 the sign stays
positive, and the count of three is already reached, so nothing hides there. One SOLVE in each gap:

```keys E02 after=E01E
2 +/− STO X 1 +/− GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="E02" kind="view">X=-1.8794</disp>.

```keys E03 after=E02
0 STO X 1 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="E03" kind="view">X=0.3473</disp>.

```keys E04 after=E03
1 STO X 2 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="E04" kind="view">X=1.5321</disp>. None of d's roots is a whole number or a
simple fraction, which is why trying whole numbers found only the gaps, and SOLVE found the roots.
