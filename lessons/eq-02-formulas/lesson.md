---
id: eq-02
title: Solving a formula for any letter
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# Solving a formula for any letter

A formula ties several quantities together. The area of a rectangle is its length times its width:
A = L × W. Usually a formula is written to give one of them, here A. But if you know the area and
the length, the same formula tells you the width. With SOLVE you type a formula once and solve it
for whichever letter you need.

## Before you start

The setup from rpn-01: 33s mode and FIX 4. Work the examples in order: each one either carries on
from the one before or starts fresh, and the text says which. eq-01 showed how to type an equation,
check it with XEQ, and solve it with SOLVE; this lesson uses all three.

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

## One unknown, the others asked for

Type the area formula. Each letter is RCL and its letter key: A is on the √x key, L on TAN, W on 5.
Then ask SOLVE for W:

```keys S01A
GOLD EQN RCL A = RCL L × RCL W ENTER GOLD SOLVE W
```

SOLVE needs the values of the other two letters, so it asks for them one at a time. The line above
X shows <disp v="S01A" kind="prompt">A?</disp>. A rectangle with an area of 42: type 42 and press
R/S.

```keys S01B after=S01A
42 R/S
```

Now it shows <disp v="S01B" kind="prompt">L?</disp>. Its length is 12:

```keys S01 after=S01B
12 R/S
```

The X line shows <disp v="S01" kind="view">W=3.5000</disp>: the width is 3.5, which is 42 ÷ 12. SOLVE stored it in the
variable W. Each value you typed at a prompt was stored too; VIEW (from rpn-02) shows that A holds
the 42:

```keys S01V after=S01
GOLD VIEW A
```

The screen shows <disp v="S01V" kind="view">A=42.0000</disp>.

## The same formula, another letter

The formula is still in the calculator, and A, L and W still hold 42, 12 and 3.5. Show it again with
EQN, and this time ask SOLVE for L:

```keys S02A after=S01V
GOLD EQN GOLD SOLVE L
```

It asks <disp v="S02A" kind="prompt">A?</disp>, and X shows <disp v="S02A">42.0000</disp>, the value
A holds now. R/S keeps it:

```keys S02B after=S02A
R/S
```

Now it asks <disp v="S02B" kind="prompt">W?</disp>, with the 3.5 showing. R/S keeps that too:

```keys S02 after=S02B
R/S
```

The X line shows <disp v="S02" kind="view">L=12.0000</disp>, the length you started from. One formula, typed once, answered
for two different letters.

## A formula with more in it

To turn a temperature in degrees Celsius, C, into degrees Fahrenheit, F, multiply by 1.8 and add
32: F = 1.8 × C + 32. This example starts fresh. F is on the Σ+ key and C on LN. Typing while an
equation is showing starts a new one, and the area formula stays in the calculator's list. Type the
temperature formula and ask SOLVE for C:

```keys T01A
GOLD EQN RCL F = 1.8 × RCL C + 32 ENTER GOLD SOLVE C
```

There is only one other letter, so it asks only <disp v="T01A" kind="prompt">F?</disp>. Body
temperature is about 98.6 degrees Fahrenheit:

```keys T01 after=T01A
98.6 R/S
```

The X line shows <disp v="T01" kind="view">C=37.0000</disp>. Now the other way: how many degrees Fahrenheit is 100 degrees
Celsius? EQN shows the last equation you viewed, here the temperature formula, so solve it for F:

```keys T02 after=T01
GOLD EQN GOLD SOLVE F 100 R/S
```

The X line shows <disp v="T02" kind="view">F=212.0000</disp>.

## Exercises

1. Distance is rate times time, D = R × T. A car covers 150 kilometres at 60 kilometres an hour.
   Type the formula and solve it for T. Answer each prompt with the value of the letter it names.
2. At one temperature the Celsius and Fahrenheit numbers are the same. Type F = 1.8 × C + 32 again,
   solve it for C when F is −40, and see.

## Answers

1. D is on the yˣ key, R on XEQ, T on 8. SOLVE asks D? first, then R?:

   ```keys E01
   GOLD EQN RCL D = RCL R × RCL T ENTER GOLD SOLVE T 150 R/S 60 R/S
   ```

   The X line shows <disp v="E01" kind="view">T=2.5000</disp>: two and a half hours.

2. The keys:

   ```keys E02
   GOLD EQN RCL F = 1.8 × RCL C + 32 ENTER GOLD SOLVE C 40 +/− R/S
   ```

   The X line shows <disp v="E02" kind="view">C=-40.0000</disp>: −40 degrees is the same in both scales.
