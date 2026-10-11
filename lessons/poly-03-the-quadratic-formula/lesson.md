---
id: poly-03
title: The quadratic formula
requires: setup shift-keys change-sign sto rcl minus-and-power square-root clear-message sqrt-negative polynomial root sign-change root-count
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The quadratic formula

A polynomial of degree 2, $ax^{2} + bx + c$ with a not 0, is called a quadratic. Its roots do not need
SOLVE's search: there is a formula for them,

$x = (−b ± \sqrt{b^{2} − 4ac}) ÷ (2a)$,

where ± means the formula gives two answers, one with + and one with −, and $2a$ is $2 × a$. The part
under the square root, $b^{2} − 4ac$, is called the discriminant. It decides how many real roots there
are, before you work out any of them. The calculator works the formula on the stack, with $a$, $b$ and $c$ kept
in variables.

## From before

```item PL3F1
prompt: Work out $−5^{2} + 30$.
topics: minus-and-power
answer: type
calculator: no
slip: PL3F1A | squared −5 | $−5^{2}$ is the negative of $5^{2}$, so −25. Only $(−5)^{2}$ is 25.
```

```item PL3F2
prompt: For $\sqrt{3 − 7}$, what is the number under the root?
topics: sqrt-negative
answer: type
calculator: no
slip: PL3F2A | took 3 from 7 | It is $3 − 7$, which is −4: a negative number, with no real square root.
```

## Before you start

Each section's examples are one chain; each section and
the exercise start fresh. A, B, C and D are on the top row, each printed small at the lower right
of its key as rpn-02 showed: A on √x, B on eˣ, C on LN, D on yˣ.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Two roots

Take $q(x) = x^{2} − 4x + 3$ from fn-02. Here $a = 1$, $b = −4$ and $c = 3$. Store them:

```keys Q01
1 STO A 4 +/− STO B 3 STO C
```

X shows <disp v="Q01">3.0000</disp>, the $c$ just stored. Now the discriminant, $b^{2} − 4ac$. x² is gold
above √x, as in num-01. On the stack: $b$, then square it; then 4, then $a$:

```keys Q02A after=Q01
RCL B GOLD x² 4 RCL A
```

X shows <disp v="Q02A">1.0000</disp>, the $a$. Typing 4 lifted $b^{2}$ to Y, and RCL A lifted it again,
so now $a$ is in X, 4 in Y, and $b^{2}$, 16, in Z. × makes $4a$ and drops $b^{2}$ back to Y; RCL C lifts it to Z
once more, and the second × makes $4ac$ and drops it back to Y; − then takes $4ac$ from $b^{2}$. Keep the
result in $D$:

```keys Q02 after=Q02A
× RCL C × − STO D
```

X shows <disp v="Q02">4.0000</disp>: $16 − 12$. Now the root with +: $−b$, plus the square root of $D$,
all divided by $2a$. After RCL D, the √x key means the square root again, not the letter A: only the
key right after STO or RCL means a letter. $−b + \sqrt{D}$ waits in Y while 2 RCL A × builds $2a$ in
X, then ÷ divides Y by X.

```keys Q03 after=Q02
RCL B +/− RCL D √x + 2 RCL A × ÷
```

X shows <disp v="Q03">3.0000</disp>: $(4 + 2) ÷ 2$. The same keys with − in place of + give the
other root:

```keys Q04 after=Q03
RCL B +/− RCL D √x − 2 RCL A × ÷
```

X shows <disp v="Q04">1.0000</disp>: $(4 − 2) ÷ 2$. The roots are 1 and 3, the two zeros in q's
table.

```why
ask: Why are the two roots, 1 and 3, the same distance either side of 2?
because: The formula gives $−b ÷ 2a$ plus or minus $\sqrt{D} ÷ 2a$, so both roots sit the same distance from the middle, $−b ÷ 2a$, which here is $4 ÷ 2$.
```

## One root

$x^{2} − 6x + 9$ has $a = 1$, $b = −6$ and $c = 9$. Its discriminant:

```keys Z01
1 STO A 6 +/− STO B 9 STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X shows <disp v="Z01">0.0000</disp>. With a discriminant of 0, adding or subtracting its square root
changes nothing, so both of the formula's answers are the same:

```keys Z02 after=Z01
RCL B +/− RCL D √x + 2 RCL A × ÷
```

X shows <disp v="Z02">3.0000</disp>, the same root twice, called a double root: $x^{2} − 6x + 9$ is
$(x − 3)^{2}$, with the factor $x − 3$ twice. It is the kind of root poly-02 warned about: the graph touches the axis at 3 without crossing it, so no sign change would have shown it.
The formula finds it anyway.

## No real root

$x^{2} + 2x + 5$ has $a = 1$, $b = 2$ and $c = 5$:

```keys N01
1 STO A 2 STO B 5 STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X shows <disp v="N01">-16.0000</disp>: a negative discriminant. Its square root is refused, as in
fn-03:

```keys N02 after=N01
RCL B +/− RCL D √x
```

The screen shows <disp v="N02" kind="message">SQRT(NEG)</disp>. Clear it with C:

```keys N03 after=N02
C
```

X shows <disp v="N03">-16.0000</disp>, the discriminant the square root refused. A negative
discriminant means no real root: the graph never reaches the $x$ axis. So the discriminant sorts
every quadratic before any root is worked out: positive, two real roots; zero, one double root;
negative, none among the real numbers. The roots of $x^{2} + 2x + 5$ are complex numbers, which poly-04
works out with the same formula.

```why
ask: Why does a negative discriminant mean the graph never reaches the $x$ axis?
because: Every root the formula gives needs $\sqrt{D}$, and no real number squares to a negative, so there is no real $x$ where the value is zero.
```

Now $x^{2} + 6x + 10$, with $a = 1$, $b = 6$ and $c = 10$. Store them, and work out its discriminant the
same way.

```keys N01T twin=N01
1 STO A 6 STO B 10 STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X holds −4: negative again, so $x^{2} + 6x + 10$ has no real root.

## Exercise

Find the roots of $2x^{2} + 3x − 2$. Work out the discriminant first: how many roots will there be?

## Answer

$a = 2$, $b = 3$ and $c = −2$:

```keys E01
2 STO A 3 STO B 2 +/− STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X shows <disp v="E01">25.0000</disp>: positive, so two roots. With +:

```keys E01B after=E01
RCL B +/− RCL D √x + 2 RCL A × ÷
```

X shows <disp v="E01B">0.5000</disp>: $(−3 + 5) ÷ 4$. With −:

```keys E01C after=E01B
RCL B +/− RCL D √x − 2 RCL A × ÷
```

X shows <disp v="E01C">-2.0000</disp>: $(−3 − 5) ÷ 4$.

## Mixed review

```item PL3M1
prompt: What is the discriminant $b^{2} − 4ac$ of $x^{2} − 6x + 9$?
operands: 2, 6, 9
topics: discriminant
answer: type
calculator: no
slip: PL3M1A | added the 4ac | It is $b^{2}$ minus $4ac$: $36 − 36$.
```

```item PL3M2
prompt: Work out $4 × 2^{3} − 10$.
topics: powers-first
answer: type
calculator: no
slip: PL3M2A | cubed 4 × 2 | The power belongs to the 2 alone: $2^{3}$ is 8, then $4 × 8 − 10$.
```

```item PL3M3
prompt: A quadratic's discriminant is −20. How many real roots does it have?
topics: negative-discriminant
answer: type
calculator: no
working: none
slip: PL3M3A | two, as the ± suggests | A negative number has no real square root, so neither sign gives a real root.
```

```item PL3M4
prompt: At most how many roots can $x^{5} − x$ have?
topics: root-count
answer: type
calculator: no
working: none
slip: PL3M4A | the power of the last term | The degree is the highest power, 5: at most 5 roots.
```
