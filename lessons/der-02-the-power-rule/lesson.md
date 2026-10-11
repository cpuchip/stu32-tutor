---
id: der-02
title: The power rule
requires: setup shift-keys rpn-arithmetic enter-copies stack-lift swap-roll x-squared power reciprocal change-sign polynomial instant-rate derivative-function eqn-typing xeq-check equation-list
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The power rule

der-01 found two derivatives by algebra: $d(t) = 2t^{2}$ has $d'(t) = 4t$, and $f(x) = x^{2}$ has $f'(x) = 2x$. Each
took an expansion, a division by $h$ and a limit. Doing that for every function would be slow. Powers
of $x$ follow one pattern, and two rules build every polynomial's derivative from it, so any
polynomial's derivative can be written down at once.

## From before

```item DR2F1
prompt: $d(t) = 2t^{2}$ has $d'(t) = 4t$. What is $d'(5)$?
operands: 2, 2, 5
topics: derivative-function
answer: type
calculator: no
slip: DR2F1A | d(5), not d′(5) | $d'(5)$ is the speed at 5: $4 × 5$. $d(5)$ is the distance.
```

```item DR2F2
prompt: Nested, $x^{2} + 3x + 2$ is $(x + 3)x + 2$. Work it out at $x = 4$, from the inside.
operands: 2, 3, 2, 4
topics: horner
answer: type
calculator: no
slip: DR2F2A | dropped the brackets | From the inside: $4 + 3$ is 7, then $7 × 4 + 2$.
```

## Before you start

Each example starts fresh, except where one says
it carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Powers of x

Do the same algebra for $x^{3}$. $(a + h)^{3}$ is $(a + h)^{2} × (a + h)$, which is $(a^{2} + 2ah + h^{2})(a + h)$. Multiplied
out, that is $a^{3} + a^{2}h + 2a^{2}h + 2ah^{2} + ah^{2} + h^{3}$, and collecting like terms, $a^{3} + 3a^{2}h + 3ah^{2} + h^{3}$. Take
away $a^{3}$ and divide by $h$: the average rate is $3a^{2} + 3ah + h^{2}$, for any $h$ that
is not 0. As $h$ shrinks, $3ah$ and $h^{2}$ shrink to 0, and the average closes in on $3a^{2}$. So the derivative of
$x^{3}$ is $3x^{2}$.

The same work for the smaller powers:

| $f(x)$ | the average from $a$ to $a + h$ | $f'(x)$ |
|---|---|---|
| $x$ | $((a + h) − a) ÷ h = 1$ | 1 |
| $x^{2}$ | $2a + h$ | $2x$ |
| $x^{3}$ | $3a^{2} + 3ah + h^{2}$ | $3x^{2}$ |

The pattern: the power comes down in front, and the new power is one less. For $n = 1$, 2, 3 and on,
the derivative of $x^{n}$ is $n·x^{n-1}$. This is the power rule. (For $n = 1$ it gives $1·x^{0}$, and $x^{0}$ is 1, so the
$x$ row fits.)

Why $n$ in front, for every $n$? $(a + h)^{n}$ is $n$ brackets of ($a + h$) multiplied together. Multiplying out
takes one letter from each bracket. Taking $a$ from every bracket gives $a^{n}$. A term with exactly one $h$
takes $h$ from one bracket and $a$ from the other $n − 1$, and there are $n$ brackets the $h$ could come from,
so together those terms are $n·a^{n-1}h$. Every other term has two or more h's. So $(a + h)^{n} − a^{n}$, divided
by $h$, is $n·a^{n-1}$ plus terms that each still have an $h$, and as $h$ shrinks they shrink to 0.

A constant, like $f(x) = 7$, never changes: $(7 − 7) ÷ h = 0$, so its derivative is 0. On a graph it is a
flat line, with slope 0.

## Sums and multiples

Two more rules come straight from the averages.
- A number times a function. $(2(a + h)^{2} − 2a^{2}) ÷ h$ is $2 × ((a + h)^{2} − a^{2}) ÷ h$: twice the average of
  $t^{2}$. Whatever that average closes in on, twice it closes in on twice as much. So the derivative of
  k times a function is k times its derivative: for $2t^{2}$, $2 × 2t = 4t$, which is the answer found before.
- A sum. For $f + g$, the change from $a$ to $a + h$ is f's change plus g's change, so the average of the
  sum is f's average plus g's average. If those close in on $f'(a)$ and $g'(a)$, their sum closes in on
  $f'(a) + g'(a)$: the derivative of a sum is the sum of the derivatives. A difference is a sum with a
  multiple of −1, so it works the same way.

With these and the power rule, any polynomial's derivative is written term by term. For
$f(x) = x^{3} − 4x + 1$: $x^{3}$ gives $3x^{2}$, $−4x$ is −4 times $x$ and gives $−4 × 1 = −4$, and the constant 1 gives 0, so
$f'(x) = 3x^{2} − 4$. At $x = 2$,
$f'(2) = 3 × 4 − 4 = 8$.

## Checking the rule

As before, one average over a small $h$ should land near the rule's answer. $f(2) = 8 − 8 + 1 = 1$, so
work out $f(2.001)$, take away 1, and divide by 0.001. On the stack, 2.001 ENTER ENTER leaves 2.001 in X, Y
and Z. Typing 3 replaces the 2.001 in X, and yˣ uses the copy in Y as its base: $2.001^{3}$. The last copy
drops down to Y, and x↔y brings it back to X for 4 ×. Then − takes $4x$ away from $x^{3}$, and 1 + finishes
$f(2.001)$. The 1 − after it is taking $f(2) = 1$ away; + 1 and − 1 cancel, but the keys follow the
method.

```keys P01
2.001 ENTER ENTER 3 yˣ x↔y 4 × − 1 + 1 − 0.001 ÷
```

X shows <disp v="P01">8.0060</disp>, near 8. It agrees with the rule; the algebra above is what proves it.

```why
ask: Why does the average land a little above 8?
because: The average is $3a^{2} + 3ah + h^{2} − 4$. At $a = 2$, the $3ah$ adds $3 × 2 × 0.001$ to the rule's 8, and the $h^{2}$ adds far less.
```

```item DR2T1
prompt: For $g(x) = x^{4} − 5x$, what is $g'(2)$? Work it out by hand.
operands: 4, 5, 2
twin: P01
topics: power-rule
answer: type
calculator: no
slip: DR2T1A | the power not brought down | $x^{4}$ gives $4x^{3}$: the 4 comes down in front of $2^{3}$.
slip: DR2T1B | −5x kept as it is | $−5x$ is −5 times $x$, and its derivative is −5, not $−5x$.
```

<mode m="STU">

STU mode's D/DX gives the rule itself, as before: type the expression in the equation list, then
CAS, D/DX, and the variable.</mode>

```keys B01 mode=STU
GOLD EQN RCL X yˣ 3 − 4 × RCL X + 1 ENTER CAS D/DX X
```

<mode m="STU">The screen shows <disp v="B01" kind="eqn">3×X^2-4</disp>, the rule's $3x^{2} − 4$. Carrying on,
XEQ works it out at $x = 2$:</mode>

```keys B02 after=B01 mode=STU
XEQ 2 R/S
```

<mode m="STU">X shows <disp v="B02">8.0000</disp>. XEQ also leaves Equation mode, so the next number
typed is a number again.</mode>

## Beyond whole powers

The power rule reaches further than $n = 1$, 2, 3. $\frac{1}{x}$ is $x^{-1}$, and if the rule holds for $n = −1$, its
derivative is $−1 × x^{-2}$, which is $−1 ÷ x^{2}$. At $x = 2$ that is $−\frac{1}{4}$, or −0.25. One average over 0.001, with
1/x, takes $\frac{1}{2} = 0.5$ away from $\frac{1}{2.001}$ and divides by 0.001:

```keys R01
2.001 1/x 0.5 − 0.001 ÷
```

X shows <disp v="R01">-0.2499</disp>, near −0.25. The algebra proves it. $\frac{1}{a + h} − \frac{1}{a}$, over the common
bottom $a(a + h)$, is $(a − (a + h)) ÷ (a(a + h))$, which is $−h ÷ (a(a + h))$. Divided by $h$, the average is
$−1 ÷ (a(a + h))$, and as $h$ shrinks it closes in on $−1 ÷ a^{2}$. So the rule holds for $n = −1$, at every a
but 0, where $\frac{1}{x}$ has no value. A later course proves the rule for other powers, such as fractions.

```why
ask: Why is the average −0.2499, a little above −0.25?
because: The average is $−1 ÷ (a(a + h))$. With $h$ above 0, $a + h$ is a little more than $a$, so −1 is divided by a little more than 4, which lands a little nearer 0 than $−1 ÷ 4$.
```

<mode m="STU">

STU mode's D/DX agrees:</mode>

```keys R02 mode=STU
GOLD EQN 1 ÷ RCL X ENTER CAS D/DX X
```

<mode m="STU">The screen shows <disp v="R02" kind="eqn">-1÷X^2</disp>. Carrying on, Equation mode off:</mode>

```keys R03 after=R02 mode=STU
GOLD EQN
```

## Exercises

1. Write down the derivative of $5x^{4}$. What is it at $x = 1$? Check with one average over $h = 0.001$.
2. Write down the derivative of $x^{2} + 3x$. What is it at $x = 1$? Check with one average over $h = 0.001$.
   <mode m="STU">Then check the rule with D/DX.</mode>
3. What is the derivative of $g(x) = 7$, and what does it say about g's graph?

## Answers

1. 5 times the derivative of $x^{4}$: $5 × 4x^{3} = 20x^{3}$, which is 20 at $x = 1$. The average from 1 to 1.001,
   $(5 × 1.001^{4} − 5) ÷ 0.001$:

   ```keys E01
   1.001 ENTER 4 yˣ 5 × 5 − 0.001 ÷
   ```

   X shows <disp v="E01">20.0300</disp>.

2. $2x + 3$, which is 5 at $x = 1$. $f(1) = 1 + 3 = 4$, so the average from 1 to 1.001 is
   $(1.001^{2} + 3 × 1.001 − 4) ÷ 0.001$. On the stack, one ENTER is enough this time: x² uses only X, so the
   copy in Y waits, and x↔y brings it back for 3 ×. (yˣ, above, used the copy in Y as its base, which
   is why that example needed two.)

   ```keys E02
   1.001 ENTER GOLD x² x↔y 3 × + 4 − 0.001 ÷
   ```

   X shows <disp v="E02">5.0010</disp>.<mode m="STU"> And D/DX:</mode>

   ```keys E02B mode=STU
   GOLD EQN RCL X yˣ 2 + 3 × RCL X ENTER CAS D/DX X
   ```

   <mode m="STU">The screen shows <disp v="E02B" kind="eqn">2×X+3</disp>. Carrying on, Equation mode
   off:</mode>

   ```keys E02C after=E02B mode=STU
   GOLD EQN
   ```

3. 0, at every $x$: $g$ never changes, so its graph is a flat line, with slope 0 everywhere.
   <mode m="STU">D/DX agrees:</mode>

   ```keys E03 mode=STU
   GOLD EQN 7 ENTER CAS D/DX X
   ```

   <mode m="STU">The screen shows <disp v="E03" kind="eqn">0</disp>.</mode>

## Mixed review

```item DR2M1
prompt: What is the derivative of $x^{5}$ at $x = 2$?
operands: 5, 2
topics: power-rule
answer: type
calculator: no
slip: DR2M1A | the function, not its derivative | The derivative of $x^{5}$ is $5x^{4}$: $5 × 2^{4}$.
```

```item DR2M2
prompt: Work out $(5^{2} − 1) ÷ (5 − 1)$.
topics: fraction-bar
answer: type
calculator: no
slip: DR2M2A | divided only the 1 | The whole top over the whole bottom: $24 ÷ 4$.
```

```item DR2M3
prompt: What is the derivative of the constant 7?
topics: constant-derivative
answer: type
calculator: no
working: none
slip: DR2M3A | the constant itself | A constant does not change, so its rate of change is 0.
```

```item DR2M4
prompt: What is the average rate of change of $x^{3}$ from $x = 1$ to $x = 3$?
operands: 3, 1, 3
topics: average-rate
answer: type
calculator: no
slip: DR2M4A | forgot to divide | The change in $x^{3}$ is $27 − 1$, over the change in $x$, 2.
```
