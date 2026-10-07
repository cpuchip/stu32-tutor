---
id: poly-03
title: The quadratic formula
status: draft prose (non-author read taken; accepted for accuracy by abacus #4503; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The quadratic formula

A polynomial of degree 2, ax² + bx + c with a not 0, is called a quadratic. Its roots do not need
SOLVE's search: there is a formula for them,

x = (−b ± √(b² − 4ac)) ÷ (2a),

where ± means the formula gives two answers, one with + and one with −, and 2a is 2 × a. The part
under the square root, b² − 4ac, is called the discriminant. It decides how many real roots there
are, before you work out any of them. This lesson uses the formula on the stack, with a, b and c kept in variables.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each section's examples are one chain; each section and
the exercise start fresh. A, B, C and D are on the top row, each printed small at the lower right
of its key as rpn-02 showed: A on √x, B on eˣ, C on LN, D on yˣ.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Two roots

Take q(x) = x² − 4x + 3 from fn-02. Here a = 1, b = −4 and c = 3. Store them:

```keys Q01
1 STO A 4 +/− STO B 3 STO C
```

X shows <disp v="Q01">3.0000</disp>, the c just stored. Now the discriminant, b² − 4ac. x² is gold
above √x, as in num-01. On the stack: b, then square it; then 4, then a:

```keys Q02A after=Q01
RCL B GOLD x² 4 RCL A
```

X shows <disp v="Q02A">1.0000</disp>, the a. Typing 4 lifted b² to Y, and RCL A lifted it again,
so now a is in X, 4 in Y, and b², 16, in Z. × makes 4a and drops b² back to Y; RCL C lifts it to Z
once more, and the second × makes 4ac and drops it back to Y; − then takes 4ac from b². Keep the
result in D:

```keys Q02 after=Q02A
× RCL C × − STO D
```

X shows <disp v="Q02">4.0000</disp>: 16 − 12. Now the root with +: −b, plus the square root of D,
all divided by 2a. After RCL D, the √x key means the square root again, not the letter A: only the
key right after STO or RCL means a letter (rpn-02). −b + √D waits in Y while 2 RCL A × builds 2a in
X, then ÷ divides Y by X.

```keys Q03 after=Q02
RCL B +/− RCL D √x + 2 RCL A × ÷
```

X shows <disp v="Q03">3.0000</disp>: (4 + 2) ÷ 2. The same keys with − in place of + give the
other root:

```keys Q04 after=Q03
RCL B +/− RCL D √x − 2 RCL A × ÷
```

X shows <disp v="Q04">1.0000</disp>: (4 − 2) ÷ 2. The roots are 1 and 3, the two zeros in fn-02's
table.

## One root

x² − 6x + 9 has a = 1, b = −6 and c = 9. Its discriminant:

```keys Z01
1 STO A 6 +/− STO B 9 STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X shows <disp v="Z01">0.0000</disp>. With a discriminant of 0, adding or subtracting its square root
changes nothing, so both of the formula's answers are the same:

```keys Z02 after=Z01
RCL B +/− RCL D √x + 2 RCL A × ÷
```

X shows <disp v="Z02">3.0000</disp>, the same root twice, called a double root: x² − 6x + 9 is
(x − 3)², with the factor x − 3 twice. It is the kind of root poly-02 warned about: the graph touches the axis at 3 without crossing it, so no sign change would have shown it.
The formula finds it anyway.

## No real root

x² + 2x + 5 has a = 1, b = 2 and c = 5:

```keys N01
1 STO A 2 STO B 5 STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X shows <disp v="N01">-16.0000</disp>: a negative discriminant. Its square root is refused, as in
fn-03:

```keys N02 after=N01
RCL B +/− RCL D √x
```

The screen shows <disp v="N02" kind="message">SQRT(NEG)</disp>. Clear it with C, as in fn-03:

```keys N03 after=N02
C
```

X shows <disp v="N03">-16.0000</disp>, the discriminant the square root refused. A negative
discriminant means no real root: the graph never reaches the x axis. So the discriminant sorts
every quadratic before any root is worked out: positive, two real roots; zero, one double root;
negative, none among the real numbers. The roots of x² + 2x + 5 are complex numbers, which poly-04
works out with the same formula.

## Exercise

Find the roots of 2x² + 3x − 2. Work out the discriminant first: how many roots will there be?

## Answer

a = 2, b = 3 and c = −2:

```keys E01
2 STO A 3 STO B 2 +/− STO C RCL B GOLD x² 4 RCL A × RCL C × − STO D
```

X shows <disp v="E01">25.0000</disp>: positive, so two roots. With +:

```keys E01B after=E01
RCL B +/− RCL D √x + 2 RCL A × ÷
```

X shows <disp v="E01B">0.5000</disp>: (−3 + 5) ÷ 4. With −:

```keys E01C after=E01B
RCL B +/− RCL D √x − 2 RCL A × ÷
```

X shows <disp v="E01C">-2.0000</disp>: (−3 − 5) ÷ 4.
