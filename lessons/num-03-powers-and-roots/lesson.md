---
id: num-03
title: Powers and roots
requires: setup shift-keys rpn-arithmetic stack-lift change-sign type-fraction minus-and-power
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Powers and roots

A power is repeated multiplication: 2⁵ is 2 × 2 × 2 × 2 × 2. A root undoes a power: the cube root
of 8 is 2, because 2³ is 8. The STU-32 has keys for the common cases and one key, yˣ, for the
rest. This lesson is about those keys, and about the order of the two numbers they use.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Work the examples in order; when one carries on from the
example before it, the text says so.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Squares and square roots

Squaring is x² (gold, above √x), which you met in num-01. The square root is √x itself:

```keys R01
3 GOLD x²
```

X holds 9.

```keys R02
49 √x
```

X holds 7. Both work on X alone, so they need no ENTER.

## Any power: yˣ

The yˣ key is the fourth key in the top row, under the soft keys. It takes two numbers: it raises
Y to the power X. So the number being raised goes in first, and the power second. For 2¹⁰:

```keys R03
2 ENTER 10 yˣ
```

X shows <disp v="R03">1,024.0000</disp>. The comma groups the thousands, so 1,024 is one thousand and
twenty-four. Swap them, 10 first and 2 second, and you get 10², which is 100:

```keys R04
10 ENTER 2 yˣ
```

X holds 100.

## Roots of any order

The root that undoes yˣ is ˣ√y (gold, above yˣ). It takes the X-th root of Y, again with the
number first and the root's order second. The cube root of 27:

```keys R05
27 ENTER 3 GOLD ˣ√y
```

X holds 3.

## Negative and fractional powers

A negative power means one over the positive power: 2⁻³ is 1/2³, which is 1/8. Make the power
negative with +/− before you press yˣ:

```keys R06
2 ENTER 3 +/− yˣ
```

X shows <disp v="R06">0.1250</disp>, which is 1/8.

A power of one half is a square root: 16 to the 1/2 is the square root of 16. You can type the half
as .5:

```keys R07
16 ENTER .5 yˣ
```

X holds 4, the same as 16 √x would give.

A third has no exact decimal, but you can type it as a fraction, the way num-02 showed. The cube
root of 27 as a power:

```keys R07B
27 ENTER .1.3 yˣ
```

X holds 3, the same as the ˣ√y example.

There is one thing ˣ√y can do that yˣ cannot: take an odd root of a negative number. The cube root
of −8 is −2, because (−2)³ is −8:

```keys R07C
8 +/− ENTER 3 GOLD ˣ√y
```

X holds −2. Try the same thing as a power of one third:

```keys R07D
8 +/− ENTER .1.3 yˣ
```

The screen shows <disp v="R07D" kind="message">INVALID yˣ</disp>: yˣ refuses a negative number raised
to a fractional power. Nothing was lost. Press C, the bottom left key, to clear the message:

```keys R07E after=R07D
C
```

X shows <disp v="R07E">0.3333</disp>, the third you typed, and Y still holds −8, just as they were
before the yˣ.

## The order of two powers

Powers stacked in a tower, a 2 with a 3 raised above it and a 2 raised above that, are read from the
top down: the top power first. So that tower means 2 to the power 3², which is 2⁹. With
parentheses, (2³)² means something else: cube the 2, then square the result. Cube first, then
square:

```keys R08
2 ENTER 3 yˣ 2 yˣ
```

X holds 64. For the tower, 2 to the power 3², work out 3² first, then raise 2 to that. Type all
three numbers and stop:

```keys R09A
2 ENTER 3 ENTER 2
```

The first 2 waits in Z, the 3 in Y and the second 2 in X. Press yˣ once:

```keys R09B after=R09A
yˣ
```

It worked 3² from Y and X, so X holds 9, and the stack dropped, bringing the first 2 back down to
Y. Press yˣ again for 2⁹:

```keys R09 after=R09B
yˣ
```

X shows <disp v="R09">512.0000</disp>. You still need the top-down rule to read a tower, but you
need no parentheses to work it: in RPN the order you press the keys in is the order the powers are
worked.

## Two shortcuts

Powers of ten have their own key, 10ˣ (gold, above eˣ; eˣ itself comes in a later lesson). It
works on X alone. A thousand is 10³:

```keys R10
3 GOLD 10ˣ
```

X shows <disp v="R10">1,000.0000</disp>. And 1/x, the key beside yˣ, gives one over X, the power
−1, also in one key:

```keys R11
8 1/x
```

X shows <disp v="R11">0.1250</disp>.

## Exercises

1. Work out 5⁴.
2. Work out the fourth root of 81.
3. Work out (−2)⁴.
4. Work out −2⁴, and compare it with exercise 3.

## Answers

1. 625. The 5 first, then the power:

   ```keys E01
   5 ENTER 4 yˣ
   ```

2. 3. The 81 first, then the root's order:

   ```keys E02
   81 ENTER 4 GOLD ˣ√y
   ```

3. 16. The minus belongs to the 2, so change its sign before the power:

   ```keys E03
   2 +/− ENTER 4 yˣ
   ```

   X shows <disp v="E03">16.0000</disp>.

4. −16. The power comes before the minus sign (num-01), so raise 2 to the 4th, then change the sign:

   ```keys E04
   2 ENTER 4 yˣ +/−
   ```

   X shows <disp v="E04">-16.0000</disp>. An even power makes the two readings differ in sign.
