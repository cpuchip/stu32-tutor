---
id: exp-04
title: Exponential equations
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Exponential equations

exp-03 solved 1.04ⁿ = 2 with logarithms, because the unknown sat alone in the power. Many equations
are not so tidy. In eˣ = 3x the unknown is both in a power and outside it: taking logarithms gives
x = ln(3x), with x still on both sides, and no rearranging with the functions on the calculator
gets it out. SOLVE, from poly-02, does not need it out: it searches for the x that makes the two
sides equal. This lesson uses it on exponential equations.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. The examples about eˣ = 3x are one chain, each
carrying on from the one before; the others start fresh.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Typing it

In Equation mode, eˣ types EXP with its opening bracket, as ABS did in eq-03, and ▶ steps out of
the bracket when you are done inside it. Type the power, X, then ▶:

```keys Q01
GOLD EQN eˣ RCL X ▶ = 3 × RCL X ENTER
```

The screen shows <disp v="Q01" kind="eqn">EXP(X)=3×X</disp>.

## Where to look

XEQ gives left minus right (eq-01): where it changes sign, the two sides cross. At 0:

```keys Q02 after=Q01
XEQ 0 R/S
```

X shows <disp v="Q02">1.0000</disp>: e⁰ − 0. At 1:

```keys Q03 after=Q02
GOLD EQN XEQ 1 R/S
```

X shows <disp v="Q03">-0.2817</disp>: e − 3. At 2:

```keys Q04 after=Q03
GOLD EQN XEQ 2 R/S
```

X shows <disp v="Q04">1.3891</disp>: e² − 6. The sign changes from 0 to 1 and again from 1 to 2, so
eˣ and 3x cross at least once in each gap. A sign change says nothing more than "at least once",
and unlike poly-02 there is no degree to cap the count. What caps it here is the shape of the two
sides: 3x is a straight line, and the graph of eˣ bends upward everywhere, getting steeper as it
goes. A straight line can cross a curve that bends one way like that at most twice: once going in
and once coming out. So two crossings is all there are, one in each gap.

## One root in each gap

As in poly-02, give SOLVE the ends of a gap: the first stored in X, the second on the X line.

```keys S01 after=Q04
0 STO X 1 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="S01" kind="view">X=0.6191</disp>.

```keys S02 after=S01
1 STO X 2 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="S02" kind="view">X=1.5121</disp>. So eˣ = 3x at x = 0.6191 and at
x = 1.5121, to four places. Each root comes to 34 digits, but only the latest is kept: the 1 typed
for S02's guesses replaced the first root in X. Store a root in a variable (STO) if you need it
later.

## SOLVE agrees with the logarithms

SOLVE works on the tidy equations too. 500 grows at 4% a year; when does it reach 1000? Type
500 × 1.04ᵀ = 1000, with yˣ for the power and T (on the 8 key) for the time. Then turn Equation mode
off with EQN (eq-01), store a guess of 10 years in T, and put 30 on the X line:

```keys T01
GOLD EQN 500 × 1.04 yˣ RCL T = 1000 ENTER GOLD EQN 10 STO T 30 GOLD EQN GOLD SOLVE T
```

The X line shows <disp v="T01" kind="view">T=17.6730</disp>. Dividing both sides by 500 gives
1.04ᵀ = 2, the equation exp-03 solved with logarithms, and this is its answer, found by searching
instead. (As exp-03 showed, growth paid once a year first reaches double at the 18th payment;
SOLVE answers the equation as written.) Where logarithms can untangle an equation they
give the answer at once; where they cannot, SOLVE still can.

## Exercise

2ˣ = x + 3. Type it (yˣ for the power), work out left minus right at −3, 0 and 3, and find every
solution with SOLVE.

## Answer

```keys E01
GOLD EQN 2 yˣ RCL X = RCL X + 3 ENTER
```

The screen shows <disp v="E01" kind="eqn">2^X=X+3</disp>. At −3:

```keys E01A after=E01
XEQ 3 +/− R/S
```

X shows <disp v="E01A">0.1250</disp>.

```keys E01B after=E01A
GOLD EQN XEQ 0 R/S
```

X shows <disp v="E01B">-2.0000</disp>.

```keys E01C after=E01B
GOLD EQN XEQ 3 R/S
```

X shows <disp v="E01C">2.0000</disp>. Two sign changes, so at least one solution in each gap.
And no more: x + 3 is a straight line, and 2ˣ bends upward everywhere as eˣ does, so they cross at
most twice. The two gaps hold one each:

```keys E02 after=E01C
3 +/− STO X 0 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="E02" kind="view">X=-2.8625</disp>.

```keys E03 after=E02
0 STO X 3 GOLD EQN GOLD SOLVE X
```

The X line shows <disp v="E03" kind="view">X=2.4449</disp>.
