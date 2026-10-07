---
id: fn-02
title: A table of values
status: draft prose (accepted for accuracy by abacus #4399; the TABLE section added since, at abacus; not yet read by Michael)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# A table of values

A table of values lists a function's outputs for a run of inputs, side by side. It is the first
picture of a function: from it you can see where the function is zero, where it is smallest, and
how it rises and falls. This lesson builds one with a short program that loops, builds the same
one again with the calculator's TABLE, and then draws the graph from it by hand.

## Before you start

The setup from rpn-01: 33s mode and FIX 4. This lesson is one chain: each example carries on from
the one before. It uses the program entry, labels, XEQ and RTN of fn-01. It enters two programs, Q
and T, and T has a second label inside it, U, for its loop to jump back to. None of these letters
is used in fn-01.

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

## The function

The function for this lesson is q(x) = x² − 4x + 3. As a program it needs x more than once. It
starts with two ENTERs, which leave copies of x in Y and Z. Then x² squares the one in X, x↔y brings
a copy of x back to X, 4 × makes 4x, − leaves x² − 4x, and 3 + finishes. Q is on the ← key:

```keys Q01A
GOLD PRGM PRGM GOLD LBL Q ENTER ENTER GOLD x² x↔y 4 × − 3 + BLUE RTN
```

The X line shows <disp v="Q01A" kind="program">Q011 RTN</disp>: eleven lines, from LBL Q to RTN. If
the number differs, a key went in twice or not at all; step back with ← and fix it, as in fn-01.
Turn program entry off:

```keys Q01 after=Q01A
GOLD PRGM PRGM
```

Try it on 2:

```keys Q02 after=Q01
2 XEQ Q
```

X shows <disp v="Q02">-1.0000</disp>: q(2) = 4 − 8 + 3. And Y holds 2, the input: one of the copies
the two ENTERs made is left over. So when Q finishes, the input sits in Y beside the output in X,
which is just what a table needs.

## A loop

A table needs Q run for x = 0, 1, 2, 3 and 4. A second program, T, does that with a loop: a run of
lines that repeats, here once for each x.

The loop needs a counter, and a counter on the STU-32 packs its numbers into one value. In 0.004,
the whole part, 0, is the count. The three digits after the point, 004, are where to stop, and the
count runs up to and including that number; the stop value always takes exactly three digits, so 4
is written 004. Two more digits after those could set the step; left off, the step is 1.

Program T starts by storing that counter in I (I is on the R↓ key; T is on 8):

```keys T01A after=Q02
GOLD PRGM PRGM GOLD LBL T 0.004 STO I
```

The loop itself gets its own label, U (on the 9 key), so the program can jump back to it. Each time
round it:

- recalls I and keeps its whole part with IP (in the POW menu, blue above yˣ): that is x;
- runs Q. Inside a program, XEQ Q runs Q, and Q's RTN comes back to the line after XEQ Q, so T
  carries on;
- stops with R/S, so you can read the row: x in Y, q(x) in X. Recorded in a program, R/S makes it
  stop; pressed by you, it carries on from the stop;
- adds 1 to the count with ISG (blue, above 4; its name means "increment, skip if greater"). Like
  STO, it waits for a variable, here I. Once the count passes the stop value, ISG skips the next
  line;
- otherwise goes back to U with GTO (gold, above 4), which waits for a label the way XEQ does.

After the loop, RTN ends T:

```keys T01B after=T01A
GOLD LBL U RCL I BLUE POW IP XEQ Q R/S BLUE ISG I GOLD GTO U BLUE RTN
```

The X line shows <disp v="T01B" kind="program">U008 RTN</disp>: lines after a label are numbered from
that label, so the loop and its RTN are U's lines 1 to 8. Turn program entry off:

```keys T01 after=T01B
GOLD PRGM PRGM
```

## Reading the table

Run T. It stops at the first row:

```keys T02 after=T01
XEQ T
```

X shows <disp v="T02">3.0000</disp> and Y holds 0: q(0) = 3. Press R/S for each next row:

```keys T03 after=T02
R/S
```

X shows <disp v="T03">0.0000</disp>, with 1 in Y.

```keys T04 after=T03
R/S
```

X shows <disp v="T04">-1.0000</disp>, with 2 in Y.

```keys T05 after=T04
R/S
```

X shows <disp v="T05">0.0000</disp>, with 3 in Y.

```keys T06 after=T05
R/S
```

X shows <disp v="T06">3.0000</disp>, with 4 in Y. One more R/S: ISG counts to 5, past the stop value,
skips the GTO, and RTN ends the program.

```keys T07 after=T06
R/S
```

The last row stays showing: X shows <disp v="T07">3.0000</disp>. The whole table:

| x | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| q(x) | 3 | 0 | −1 | 0 | 3 |

## The same table from TABLE

The mode menu you used in the setup has three modes. 33s and 35s mode behave like two older
calculators, the HP 33s and the HP 35s. STU mode is the STU-32's own, with features those two never
had. One of them is TABLE, which makes a table like the one program T printed, from an expression,
with no program. Switch to STU mode: press blue, then ENTER for the mode menu, then the soft key
under STU:

```keys B01 after=T07
BLUE MODE STU
```

The status band shows <disp v="B01" kind="status">STU</disp>. TABLE works on the equation list of
eq-01, and an entry there may be an expression with no = sign. Type x² − 4x + 3 that way, with yˣ
for the power and no =:

```keys B02 after=B01
GOLD EQN RCL X yˣ 2 − 4 × RCL X + 3 ENTER
```

The screen shows <disp v="B02" kind="eqn">X^2-4×X+3</disp>; ^ means "to the power of". With no =,
TABLE gives the expression's value. (With an =, it would give left minus right, as XEQ does.)

TABLE, blue above 8, opens a menu: VAR picks the variable, START and STEP each take the number in X,
as STO does, and GO shows the table. TABLE uses the equation last shown, even after Equation mode
is off, and its first variable unless you pick another: here X, the only one. The step is 1 unless
it has been set to something else, so only the start needs setting. Turn Equation mode off first,
because a digit typed while the equation shows starts a new equation (eq-01). Then start at 0.
START closes the menu:

```keys B03 after=B02
GOLD EQN 0 BLUE TABLE START
```

Open it again for GO:

```keys B04 after=B03
BLUE TABLE GO
```

The X line shows the row for x = 0: <disp v="B04" kind="row">0.0000 3.0000</disp>, x on the left
and q(x) on the right. The row on the X line is the selected one, and the status band shows
<disp v="B04" kind="status">TABLE</disp>. The table does not stop at the start: the three lines
above hold the rows before it, x = −3, −2 and −1, so four rows show at once, and the one just above
reads −1 and 8. ▼ moves down a row:

```keys B05 after=B04
▼
```

The X line shows <disp v="B05" kind="row">1.0000 0.0000</disp>. Three more:

```keys B06 after=B05
▼ ▼ ▼
```

The X line shows <disp v="B06" kind="row">4.0000 3.0000</disp>, the last row of T's table; ▲ moves
back up. ENTER copies the selected row's q(x) to X and leaves the table; C leaves it without
copying. Take the 3. The rest of this lesson, like the lessons before it, is written for 33s mode,
so switch back:

```keys B07 after=B06
ENTER BLUE MODE 33s
```

X shows <disp v="B07">3.0000</disp>. The two ways give the same table. T is still worth having:
TABLE needs STU mode, and a program is something you can change to do more at each row.

## Drawing the graph

<!-- GRAPH: firmware unit 033 (abacus #4315) will plot the equation shown against TABLE's variable,
with X from −10 to 10 and Y fitted to the curve, and a trace whose ENTER copies the traced value to
X. STU mode only. When it lands, this section gains the same curve on the screen, kept beside the
drawing by hand, and the TABLE section's switch back to 33s mode moves to after the graph (both
need STU; a non-author read, 2026-10-06). -->

On squared paper, draw an x axis across and a q axis up, and mark each row as a point: (0, 3),
(1, 0), (2, −1), (3, 0) and (4, 3). The curve comes down from 3, crosses the x axis at x = 1, is
lowest in the table at x = 2, crosses the x axis again at x = 3, and rises back to 3.

A table shows only its rows, so check what happens between two of them before joining the points.
Halfway on each side of 2:

```keys G01 after=B07
1.5 XEQ Q
```

X shows <disp v="G01">-0.7500</disp>.

```keys G02 after=G01
2.5 XEQ Q
```

X shows <disp v="G02">-0.7500</disp> too. Both are above −1 and below 0, and equal, so the curve is
rounded at the bottom, and its two sides mirror each other about the vertical line x = 2. Join the
points with a smooth curve, not straight lines. The graph of any function of the form ax² + bx + c,
with a not zero, has this shape, which is called a parabola.

## Exercises

1. Where is q(x) zero? Read it from the table, then check one of the answers with Q.
2. Is q(5) above q(4)? Work it out with Q.
3. Make the table run from x = 2 to x = 6 without changing program T: store a new counter in I and
   start the program at U instead of T.

## Answers

1. At x = 1 and x = 3. Check 1:

   ```keys E01 after=G02
   1 XEQ Q
   ```

   X shows <disp v="E01">0.0000</disp>.

2. The keys:

   ```keys E02 after=E01
   5 XEQ Q
   ```

   X shows <disp v="E02">8.0000</disp>: q(5) = 25 − 20 + 3, above q(4) = 3, so the curve is still
   rising at 5.

3. The counter is 2.006: count from 2, stop at 6. XEQ U starts at the loop, skipping T's own STO:

   ```keys E03 after=E02
   2.006 STO I XEQ U
   ```

   X shows <disp v="E03">-1.0000</disp> with 2 in Y, the row for x = 2. Four more R/S:

   ```keys E03B after=E03
   R/S R/S R/S R/S
   ```

   X shows <disp v="E03B">15.0000</disp> with 6 in Y: q(6) = 36 − 24 + 3. One more R/S ends it.
