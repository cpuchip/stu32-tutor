---
id: exp-03
title: Logarithms
status: draft prose (non-author read taken; accepted for accuracy by abacus #4646; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Logarithms

exp-01 and exp-02 worked out an amount after a given time. The opposite question is just as
common: how long until an amount doubles, or halves? The time is the power in a × bⁿ, so the
question is "what power?", and the answer is a logarithm.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Most examples start fresh; where one carries
on from the one before, it says so.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## What power?

A logarithm is a power. The logarithm of a number to the base 10 is the power 10 must be raised to
to give that number: 10³ = 1000, so the logarithm of 1000, base 10, is 3, written log 1000 = 3. LOG
is gold above LN, the third key of the top row:

```keys L01
1000 GOLD LOG
```

X shows <disp v="L01">3.0000</disp>. Most numbers are not whole powers of 10. The logarithm of 2:

```keys L02
2 GOLD LOG
```

X shows <disp v="L02">0.3010</disp>, rounded to four places: 10 to the power 0.30102999…, all 34
digits of it, is 2. 10ˣ from num-03 (gold above eˣ) raises 10 to the power in X, so it undoes LOG.
Carry on, with the full value still in X:

```keys L03 after=L02
GOLD 10ˣ
```

X shows <disp v="L03">2.0000</disp>, the 2 back again. Typing the rounded 0.3010 instead would give
a little less than 2: the four places shown are not the whole number.

LN is the logarithm to the base e: the natural logarithm, the power of e that gives a number. eˣ
undoes it:

```keys N01
2 LN
```

X shows <disp v="N01">0.6931</disp>: e to the power 0.69314…, in full, is 2. Carry on:

```keys N02 after=N01
eˣ
```

X shows <disp v="N02">2.0000</disp>.

## Solving for the power

How long does an amount take to double at 4% a year? That is the n with 1.04ⁿ = 2. Take the
logarithm of both sides. 1.04 is 10 to the power log 1.04, so

1.04ⁿ = (10^(log 1.04))ⁿ = 10^(n × log 1.04),

since a power of a power multiplies the powers (exp-02). So the logarithm of 1.04ⁿ is n × log 1.04.
A logarithm turns a power into a multiplication, and then

n × log 1.04 = log 2, and n = log 2 ÷ log 1.04.

On the stack: 2, LOG, then 1.04 and LOG. Typing a number after a function like LOG pushes its
result up to Y, as after + or × (rpn-01), so log 2 waits in Y while log 1.04 is worked out in X,
and ÷ divides them:

```keys S01
2 GOLD LOG 1.04 GOLD LOG ÷
```

X shows <disp v="S01">17.6730</disp>. Check it: 1.04 to that power. The 1.04 goes in first and waits
in Z while the power is worked out; ÷ drops it to Y, and yˣ uses it:

```keys S02
1.04 ENTER 2 GOLD LOG 1.04 GOLD LOG ÷ yˣ
```

X shows <disp v="S02">2.0000</disp>. With growth paid once a year, though, the amount grows only at
each payment, so 17.67 years means it doubles at the 18th payment. After 17:

```keys Y17
1.04 ENTER 17 yˣ
```

X shows <disp v="Y17">1.9479</disp>, not yet double. After 18:

```keys Y18
1.04 ENTER 18 yˣ
```

X shows <disp v="Y18">2.0258</disp>. So: 18 years. A fraction of a year counts only for growth that
goes on smoothly, as continuous growth does (below) and decay did in exp-01.

The same argument with e in place of 10 gives n × ln 1.04 = ln 2, so natural logarithms give the
same n:

```keys S03
2 LN 1.04 LN ÷
```

X shows <disp v="S03">17.6730</disp>. Use whichever is nearer to hand; LN saves the gold key.

## Halving, and numbers with no logarithm

Something that keeps 90% of itself each hour, decaying smoothly, has a factor of 0.9 an hour, and
it is half gone when 0.9ⁿ = 0.5:

```keys H01
0.5 LN 0.9 LN ÷
```

X shows <disp v="H01">6.5788</disp> hours: its half-life. Both logarithms are negative here. A number
between 0 and 1 is e (or 10) to a negative power, since a negative power is one over the positive
power (num-03); the quotient of two negatives is positive.

0 and the negative numbers have no logarithm: no power of 10 or of e is 0 or below. The calculator
refuses them:

```keys V01
0 GOLD LOG
```

The screen shows <disp v="V01" kind="message">LOG(0)</disp> (and LN of a negative number shows
LOG(NEG)). Clear it:

```keys V01B after=V01
C
```

## Continuous growth

For continuous growth (exp-02), e^(r × t) = 2 means r × t = ln 2, because LN undoes eˣ. So the time
to double at a rate r is ln 2 ÷ r. At 6%:

```keys C01
2 LN 0.06 ÷
```

X shows <disp v="C01">11.5525</disp> years. Here the fraction counts: continuous growth reaches double
partway through the twelfth year.

## Exercises

1. How long does an amount take to triple at 4% paid once a year? Find n with logarithms, then
   check the whole years on either side of it.
2. Something loses 20% of itself each day, smoothly. What is its half-life?
3. How long does an amount take to double at 3% a year, continuously?

## Answers

1. 1.04ⁿ = 3, so n = ln 3 ÷ ln 1.04:

   ```keys E01
   3 LN 1.04 LN ÷
   ```

   X shows <disp v="E01">28.0110</disp>, just over 28. After 28 payments:

   ```keys E01B after=E01
   1.04 ENTER 28 yˣ
   ```

   X shows <disp v="E01B">2.9987</disp>, not quite triple; after 29:

   ```keys E01C after=E01B
   1.04 ENTER 29 yˣ
   ```

   X shows <disp v="E01C">3.1187</disp>. So 29 years.

2. Losing 20% leaves a factor of 0.8 (exp-01), so 0.8ⁿ = 0.5:

   ```keys E02
   0.5 LN 0.8 LN ÷
   ```

   X shows <disp v="E02">3.1063</disp> days.

3. ln 2 ÷ 0.03:

   ```keys E03
   2 LN 0.03 ÷
   ```

   X shows <disp v="E03">23.1049</disp> years.
