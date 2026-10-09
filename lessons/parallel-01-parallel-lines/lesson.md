---
id: parallel-01
title: Parallel lines and a line across them
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation column-subtraction angle degrees angle-kinds straight-line-angles vertical-angles
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Gullhaven and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Corwen
---

# Parallel lines and a line across them

Gullhaven's newest streets were laid out side by side down the hill to the harbour, and the coast
road cuts across all of them on a slant. Corwen measures the angle at one crossing, and wants to know
whether that tells her the angles at all the others.

## Before you start

The setup from start-01, and paper, a pencil, a ruler and a protractor, as in angle-01.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Parallel lines

Two straight lines on a flat page that never meet, however far they go, are parallel. **Draw it.**
Lay your ruler down and draw along both of its edges: the two lines are parallel, and they stay the
same distance apart all the way along the ruler.

## A line across

A line that crosses two other lines is called a transversal. The coast road is one: it crosses
Harbour Street and Market Street, which are parallel. So in this lesson the road is the transversal,
and the streets are the parallel lines. At each crossing it makes four angles, so eight
in all:

```
                     /
                 p  / q
   -----------------+-----------------  Harbour Street
                 s  / r
                   /
               t  / u
   --------------+-------------------  Market Street
              w  / v
                /
```

At the Harbour Street crossing the angles are p, q, r and s, going round; at the Market Street
crossing, t, u, v and w, in the same places.

**Draw it.** Draw two parallel lines with your ruler, then a line across them on a slant. Measure the
four angles at each crossing. What do you find?

## Corresponding angles

The angles in the same place at the two crossings are called corresponding: p and t, q and u, r and
v, s and w. Measured, they come out equal. For parallel lines this is the starting fact that the rest
of this lesson builds on, and it is taken as given, not shown. Euclid, too, took a statement about
parallel lines as given without proof, usually called his fifth postulate (some editions call it his
twelfth axiom), and this is one form of it. His own form says: if a line crosses two lines and the
two angles between them on one side add to less than 180°, those two lines meet on that side. From
it he proved that corresponding angles are equal (his Book I, proposition 29).
Corresponding angles are equal when the lines are parallel.

So at every crossing on the coast road the angles are the same. The road meets Harbour Street at
q = 65°, so u = 65° too. The angle beside q on the straight street, p, is 180 − 65:

```keys A01 entry=alg
180 − 65 ENTER
```

```keys A01 entry=rpn
180 ENTER 65 −
```

The screen shows <disp v="A01">115.0000</disp>. With vertically opposite angles (angle-02), every
angle is now known: q, s, u and w are 65°, and p, r, t and v are 115°.

It works the other way too: if corresponding angles are equal, the lines are parallel. Euclid did not
need to take this one as given; he proved it from earlier steps (his Book I, propositions 27 and 28).
That is how Corwen checks a new street. If the coast road meets it at 65°, in the same place as q,
the new street is parallel to Harbour Street. If it meets it at 68° there, it cannot be parallel,
since parallel streets would make the same angle, and the two streets will meet somewhere.

## Alternate angles

The angles between the two streets, on opposite sides of the road, are called alternate: s and u,
and r and t. They are equal too, and now there is a reason, made of two steps already known:
- First, s = q, because they are vertically opposite.
- Then q = u, because they are corresponding.
- So s = u. In the same way, r = t.

## Co-interior angles

The angles between the two streets on the same side of the road are called co-interior: r and u,
and s and t. They add to 180°, and so are usually not equal (both are 90° only when the road
crosses at a right angle). The reason:
- First, u = q, because they are corresponding.
- Then q and r lie together on the straight line of the road, so q + r = 180°.
- So u + r = 180° as well.

On Corwen's map, r = 115° and u = 65°:

```keys I01 entry=alg
65 + 115 ENTER
```

```keys I01 entry=rpn
65 ENTER 115 +
```

The screen shows <disp v="I01">180.0000</disp>.

## Exercises

Draw first, then check.

1. A road crosses two parallel streets, and one co-interior angle is 58°. What is the other?
2. In the same drawing, what is the angle alternate to the 58° one?
3. A road crosses two parallel streets. At the first crossing, one of the four angles is 104°. What
   are the eight angles?

## Answers

1. Co-interior angles add to 180°: 180 − 58 = 122°.

   ```keys E01 entry=alg
   180 − 58 ENTER
   ```

   ```keys E01 entry=rpn
   180 ENTER 58 −
   ```

   The screen shows <disp v="E01">122.0000</disp>.

2. Alternate angles are equal: 58°.

3. At the first crossing, the angle opposite 104° is 104°, and the two beside it are 180 − 104:

   ```keys E03 entry=alg
   180 − 104 ENTER
   ```

   ```keys E03 entry=rpn
   180 ENTER 104 −
   ```

   The screen shows <disp v="E03">76.0000</disp>. The second crossing has the same four angles in the
   same places, since corresponding angles are equal: four angles of 104° and four of 76°.

## Checkpoint

Questions on the whole unit. Work each by hand first, then give your answer; the page checks it. A
wrong answer that comes from a common slip gets a hint that names the step.

```item CPG1A
prompt: Two angles lie together on a straight line. One is 47°. What is the other, in degrees?
topics: straight-line-angles
answer: type
calculator: no
slip: CPG1A1 | a right angle, not a straight line | Angles on a straight line add to 180°, not 90°.
slip: CPG1A2 | a full turn, not a straight line | A straight line is half a turn, 180°, not a full turn.
```

```item CPG1B
prompt: Two straight lines cross. One of the four angles is 38°. What is the angle opposite it, in degrees?
topics: vertical-angles
answer: type
calculator: no
slip: CPG1B1 | the angle beside it | That is the angle beside it, on the same straight line. The opposite angle is equal to the given one.
```

```item CPG1C
prompt: Three angles make a full turn round a point. Two of them are 100° and 145°. What is the third, in degrees?
topics: angles-at-a-point
answer: type
calculator: no
slip: CPG1C1 | added the two, and stopped | That is the two given angles together. Take them from the full turn, 360°.
slip: CPG1C2 | left the 145° out | Take both given angles from 360°, not only the 100°.
slip: CPG1C3 | left the 100° out | Take both given angles from 360°, not only the 145°.
```

```item CPG1D
prompt: A line crosses two parallel lines. One co-interior angle is 70°. What is the other, in degrees?
topics: co-interior
answer: type
calculator: no
slip: CPG1D1 | taken as alternate | Alternate angles are equal, but co-interior angles add to 180°.
```

```item CPG1E
prompt: A right angle is cut into two angles. One is 23°. What is the other, in degrees?
topics: complementary
answer: type
calculator: no
slip: CPG1E1 | a straight line, not a right angle | A right angle is 90°, not 180°.
```

```item CPG1F
prompt: Two rays from a point make an angle of 130°. What is the reflex angle, the other way round, in degrees?
topics: angle-kinds degrees
answer: type
calculator: no
slip: CPG1F1 | a straight line, not a full turn | The two angles, one each way round, make a full turn, 360°, not a straight line.
```

```item CPG1G
prompt: A line crosses two parallel lines. One of the angles between the parallel lines is 72°. What is the angle alternate to it, in degrees?
topics: alternate-angles
answer: type
calculator: no
slip: CPG1G1 | taken as co-interior | Co-interior angles add to 180°, but alternate angles are equal.
```

```item CPG1H
prompt: A line crosses two parallel lines. At the first crossing, one of the four angles is 58°. What is the angle in the same place at the second crossing, in degrees?
topics: corresponding-angles
answer: type
calculator: no
slip: CPG1H1 | the angle beside it | That is the angle beside it on a straight line. Corresponding angles, in the same place at each crossing, are equal.
```

```item CPG1I
prompt: An angle is plainly narrower than the corner of a page. Read on one scale of a protractor, it shows 140. What is the angle, in degrees?
topics: protractor angle-kinds
answer: type
calculator: no
slip: CPG1I1 | read on the wrong scale | An angle narrower than a page corner is less than 90°, so 140 is the other scale's reading. The two scales add to 180.
```
