---
id: angle-02
title: Angle pairs
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation column-subtraction angle degrees protractor angle-kinds
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Gullhaven and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Corwen
---

# Angle pairs

In Gullhaven, Corwen is mapping the streets now, not just the bay. Where roads meet, the angles
between them come in pairs and groups that follow fixed rules, so measuring one angle tells you
others. That saves measuring, and it is a check on the ones you do measure.

## Before you start

The setup from start-01, and paper, a pencil, a ruler and a protractor, as in angle-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## On a straight line

The coast road is straight, and a lane leaves it at 70°. The two angles the lane makes with the road,
one on each side of it, together make the straight angle of the road: 180°. So the other one is
180 − 70:

```keys S01 entry=alg
180 − 70 ENTER
```

```keys S01 entry=rpn
180 ENTER 70 −
```

The screen shows <disp v="S01">110.0000</disp>. Two angles that add to 180° are called
supplementary.

```
                 lane
                /
               /
       110°   /  70°
   ----------+----------  coast road
```

## In a right angle

The harbour master's yard has a square corner, 90°. A path runs out from the corner across the
yard, between the two walls, at 35° to one wall:

```
   |
   |  55°    /  path
   |       /
   |     /
   |   /   35°
   | /
   +-------------- wall
```

Its angle to the other wall is what is left of the right angle, 90 − 35:

```keys C01 entry=alg
90 − 35 ENTER
```

```keys C01 entry=rpn
90 ENTER 35 −
```

The screen shows <disp v="C01">55.0000</disp>. Two angles that add to 90° are called complementary.

## Round a point

Three streets leave the market cross, each in its own direction. Going round the cross, the angles
between them are 120°, 95° and a third. Together they make a full turn, 360°, so the third is 360 − 120 − 95:

```keys P01 entry=alg
360 − 120 − 95 ENTER
```

```keys P01 entry=rpn
360 ENTER 120 − 95 −
```

The screen shows <disp v="P01">145.0000</disp>. This is a good check on a survey: measure all three,
and if they do not add to 360°, at least one of them is wrong.

## Where two lines cross

The coast road and the hill road are both straight, and they cross. That makes four angles. Here
they are named a, b, c and d, going round:

```
      \     /
       \ b /
        \ /
     a   X   c
        / \
       / d \
      /     \
```

**Draw it.** Draw two straight lines that cross, not at a right angle, and measure all four angles.
Two pairs of them face each other across the crossing, a with c and b with d. Each pair is called
vertically opposite. The name comes from the vertex, not from up and down: the two angles are
opposite each other at the vertex they share. What do you find?

They come out equal: a = c and b = d. A measurement shows it for one drawing, though. Here is why it
must be so for every crossing:
- Angles a and b lie together on one straight line, so a + b = 180°.
- Angles b and c lie together on the other straight line, so b + c = 180°.
- Both a and c are what is left when b is taken from 180°, so a and c are the same.

Say b is 70°. Then a, beside it on a straight line, is 180 − 70:

```keys V01 entry=alg
180 − 70 ENTER
```

```keys V01 entry=rpn
180 ENTER 70 −
```

The screen shows <disp v="V01">110.0000</disp>. And d, beside a on the other straight line, is
180 − 110:

```keys V02 entry=alg
180 − 110 ENTER
```

```keys V02 entry=rpn
180 ENTER 110 −
```

The screen shows <disp v="V02">70.0000</disp>, the same as b, the angle opposite it, as the reason
said it must be. This is
the first thing in the course shown to be true for every drawing, not just measured on one.

## Exercises

Draw first, then check.

1. One angle on a straight line is 128°. What is the other?
2. A right angle is cut into two; one part is 62°. What is the other?
3. Three angles make a full turn round a point. Two are 90° and 150°. What is the third?
4. Two lines cross, and one angle is 41°. What are the other three?

## Answers

1. 180 − 128 = 52°.

   ```keys E01 entry=alg
   180 − 128 ENTER
   ```

   ```keys E01 entry=rpn
   180 ENTER 128 −
   ```

   The screen shows <disp v="E01">52.0000</disp>.

2. 90 − 62 = 28°.

   ```keys E02 entry=alg
   90 − 62 ENTER
   ```

   ```keys E02 entry=rpn
   90 ENTER 62 −
   ```

   The screen shows <disp v="E02">28.0000</disp>.

3. 360 − 90 − 150 = 120°.

   ```keys E03 entry=alg
   360 − 90 − 150 ENTER
   ```

   ```keys E03 entry=rpn
   360 ENTER 90 − 150 −
   ```

   The screen shows <disp v="E03">120.0000</disp>.

4. The angle opposite 41° is also 41°. The two beside it are each 180 − 41:

   ```keys E04 entry=alg
   180 − 41 ENTER
   ```

   ```keys E04 entry=rpn
   180 ENTER 41 −
   ```

   The screen shows <disp v="E04">139.0000</disp>. So the four angles are 41°, 139°, 41° and 139°,
   and they add to 360°, as angles round a point must.
