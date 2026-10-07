---
id: exp-02
title: The number e
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# The number e

exp-01 grew an amount by a factor once a year. Growth can also be added more often: interest of 6%
a year paid as 0.5% every month, or as a tiny share every day. The more often, the more the amount
grows, but by less and less: the total gets closer and closer to a value it never passes, called
its limit. That limit brings in a number as important as π: e, about 2.7183. The eˣ key raises e to
a power.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Every example starts fresh.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Compounding more often

Paying interest on interest already paid is called compounding. 1000 at 6% a year, paid once at
the end of the year:

```keys C01
1000 ENTER 1.06 ×
```

X shows <disp v="C01">1,060.0000</disp>. Paid monthly instead, each month adds 6% ÷ 12 = 0.5% of
what is there, twelve times: the year's factor is (1 + 0.06 ÷ 12)¹². On the stack: 1000, then 0.06
divided by 12, plus 1, to the power 12. The 1000 waits in Z most of the way; yˣ drops it to Y, and
the last × multiplies by it, as in exp-01:

```keys C02
1000 ENTER 0.06 ENTER 12 ÷ 1 + 12 yˣ ×
```

X shows <disp v="C02">1,061.6778</disp>: more than 1060, because each month's interest earns
interest in the months after it. Daily, 365 times:

```keys C03
1000 ENTER 0.06 ENTER 365 ÷ 1 + 365 yˣ ×
```

X shows <disp v="C03">1,061.8313</disp>. About thirty times as many payments added only 0.15.
Paying ever more often keeps adding, but less each time, towards a limit.

## The number e

Take the simplest case: an amount of 1, and growth of 100% shared out n times, so each share adds
1/n and the factor for the whole is (1 + 1/n)ⁿ. Here the keys put the 1 first and then add 1/n to
it; adding in either order gives the same. For n = 12, with 1/x (the fifth key of the top row) for
one twelfth:

```keys L01
1 ENTER 12 1/x + 12 yˣ
```

X shows <disp v="L01">2.6130</disp>. For n = 365:

```keys L02
1 ENTER 365 1/x + 365 yˣ
```

X shows <disp v="L02">2.7146</disp>. For a million:

```keys L03
1 ENTER 1000000 1/x + 1000000 yˣ
```

X shows <disp v="L03">2.7183</disp>. The limit as n grows without end is the number called e. eˣ,
the second key of the top row, raises e to the power in X; e itself is e to the power 1:

```keys L04
1 eˣ
```

X shows <disp v="L04">2.7183</disp>. A million shares agree with e in every place FIX 4 shows; the
calculator keeps 34 digits (ALL, from rpn-03, shows more of them), and the two first differ in the
sixth decimal place. Like π, e never ends and never repeats.

## Continuous growth

Growth shared out without end, every instant, is called continuous. For a rate r, written as a
decimal (0.06 for 6%, not 6), the factor for a year is the limit of (1 + r/n)ⁿ, and that limit is
eʳ. A million shares of 6% come close:

```keys L05
1 ENTER 0.06 ENTER 1000000 ÷ + 1000000 yˣ
```

X shows <disp v="L05">1.0618</disp>, and e to the 0.06:

```keys L06
0.06 eˣ
```

X shows <disp v="L06">1.0618</disp>. So 1000 at 6% a year, continuously:

```keys G01
1000 ENTER 0.06 eˣ ×
```

X shows <disp v="G01">1,061.8365</disp>: just above the daily 1061.8313, and above every way of
paying 6% a fixed number of times. Over t years the factor is eʳ multiplied by itself t times,
(eʳ)ᵗ, and a power of a power multiplies the powers, as (2³)² = 2⁶ = 64: so the factor is e^(r × t),
and continuous growth from an amount a is a × e^(r × t).

## Exercises

1. 2500 grows at 4% a year, continuously, for 10 years. How much is there?
2. The same 2500 at 4% paid once a year for 10 years, as in exp-01. How much less is it?
3. The same 2500 at 4% a year paid monthly for 10 years: 120 payments of 4% ÷ 12 each.

## Answers

1. The power is r × t = 0.04 × 10: work it out, then eˣ. The × that makes 0.4 drops the 2500 from
   Z to Y, where the last × finds it:

   ```keys E01
   2500 ENTER 0.04 ENTER 10 × eˣ ×
   ```

   X shows <disp v="E01">3,729.5617</disp>.

2. The factor is 1.04, ten times:

   ```keys E02
   2500 ENTER 1.04 ENTER 10 yˣ ×
   ```

   X shows <disp v="E02">3,700.6107</disp>: about 28.95 less than continuous growth gives.

3. The factor is (1 + 0.04 ÷ 12)¹²⁰:

   ```keys E03
   2500 ENTER 0.04 ENTER 12 ÷ 1 + 120 yˣ ×
   ```

   X shows <disp v="E03">3,727.0817</disp>: between the yearly and the continuous amounts, and much
   nearer the continuous one.
