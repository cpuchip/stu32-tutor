---
id: angle-01
title: Points, lines and angles
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation column-subtraction long-division
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael; Gullhaven and its names are stand-ins, lore/WORLD.md)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
cast: Corwen
---

# Points, lines and angles

Long after Thornwick's market days, its people have reached the sea. Gullhaven is a harbour town on
a wide bay, and Corwen is making the first true map of it. A map has to say where the lighthouse is,
and where the church tower is, from one place everyone can find: the end of the harbour wall. The
distance is one half of the answer. The other half is the direction, and a direction is measured
as an angle. This lesson is about angles: what they are, how to measure them, and what kinds there
are.

## Before you start

The setup from start-01. You also need paper, a sharp pencil, a ruler and a protractor. Geometry is
done on paper first, and the calculator does the arithmetic.

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## Points and lines

A point marks a place and has no size. On paper it is a dot, named with a capital letter: the point
A. A line is straight and goes on forever both ways; a drawing shows only part of it. The part of a
line between two points A and B is the segment AB, and it has a length you can measure with a
ruler. A ray starts at a point and goes on forever one way only, like the beam of the lighthouse.

## Angles

Two rays that start at the same point make an angle. The point is the angle's vertex, and the rays
are its arms. Here the vertex is B, and the arms go through A and through C:

```
          C
         /
        /
       /
      B---------A
```

The angle is written ∠ABC, with the vertex in the middle; ∠CBA is the same angle. When there is no
doubt which angle is meant, it can be named by its vertex alone, ∠B, or by a small letter written
inside it, as the next lessons do. Its size is how far one arm is turned from the other. Drawing the
arms longer does not change it.

## Degrees

Angles are measured in degrees, written °. A full turn, all the way round to where you started, is
360°. Half a turn is 180°, and a quarter turn is 90°, the corner of a sheet of paper. A full turn was
cut into 360 a very long time ago, and it is a handy number: 360 divides evenly by 2, 3, 4, 5, 6, 8,
9, 10 and 12, though not by 7.

Corwen's sighting board is a disc marked all the way round. If it is cut into 8 equal parts, each
part is 360 ÷ 8:

```keys K01 entry=alg
360 ÷ 8 ENTER
```

```keys K01 entry=rpn
360 ENTER 8 ÷
```

The screen shows <disp v="K01">45.0000</disp>: each eighth of a turn is 45°.

## A protractor

A protractor is a half circle marked from 0 to 180, usually twice: one scale runs from 0 at the
right to 180 at the left, and the other from 0 at the left to 180 at the right. To measure an angle:

1. Put the protractor's centre mark exactly on the vertex.
2. Turn it so its 0 line, the straight line through the centre mark, lies along one arm. On most
   protractors that line is a little above the bottom edge, so line up the line, not the edge.
3. Find the scale that reads 0 on that arm, and follow that scale round to the other arm.

If an arm is too short to reach the scale, make it longer with your ruler first.

Step 3 is where the usual mistake happens: reading the other scale. The two scales always add to
180, so an angle of 50° read on the wrong scale shows 180 − 50:

```keys P01 entry=alg
180 − 50 ENTER
```

```keys P01 entry=rpn
180 ENTER 50 −
```

The screen shows <disp v="P01">130.0000</disp>. The check is to look before you read: an angle
narrower than the corner of a page is less than 90°, so it cannot be 130°.

**Draw it.** Draw a ray from a point B. Put the protractor's centre on B with its 0 line along the
ray, find 50 on the scale that starts at 0 on your ray, and mark a dot there. Join B to the dot.
Then check it: put the protractor's 0 line along your new arm instead, and read the angle again from
the scale that starts at 0 there. It should still be 50°.

## Kinds of angle

- An **acute** angle is less than 90°.
- A **right** angle is exactly 90°. A small square drawn in the corner marks one.
- An **obtuse** angle is more than 90° and less than 180°.
- A **straight** angle is exactly 180°: the two arms make one straight line.
- A **reflex** angle is more than 180° and less than 360°.

Two rays from one point make two angles, one each way round. If the turn one way is 50°, the turn
the other way round is the rest of the full turn, 360 − 50:

```keys R01 entry=alg
360 − 50 ENTER
```

```keys R01 entry=rpn
360 ENTER 50 −
```

The screen shows <disp v="R01">310.0000</disp>, a reflex angle. When nobody says which, "the angle"
means the one not more than 180°.

## Back to the bay

Corwen stands at the end of the harbour wall and sights along it. Turning from the wall, the
lighthouse is at 35°, and the church tower is at 110°, both measured from the same arm, the wall,
turning the same way.
The angle between the lighthouse and the tower, as seen from there, is 110 − 35:

```keys B01 entry=alg
110 − 35 ENTER
```

```keys B01 entry=rpn
110 ENTER 35 −
```

The screen shows <disp v="B01">75.0000</disp>. Taking one from the other works only because both
angles were measured from the same arm, turning the same way.

## Exercises

Draw first, then check.

1. Draw an angle of 60°. What is the reflex angle the other way round it?
2. What kind of angle is 135°? If it were read on the wrong scale of a protractor, what would it
   show?
3. How many degrees is a third of a full turn?
4. From the end of the wall, turning the same way from it, a boat is at 140° and the lighthouse at
   35°. What is the angle between them?

## Answers

1. A full turn is 360°, so the other way round is 360 − 60 = 300°.

   ```keys E01 entry=alg
   360 − 60 ENTER
   ```

   ```keys E01 entry=rpn
   360 ENTER 60 −
   ```

   The screen shows <disp v="E01">300.0000</disp>.

2. More than 90° and less than 180°: obtuse. The other scale shows 180 − 135 = 45.

   ```keys E02 entry=alg
   180 − 135 ENTER
   ```

   ```keys E02 entry=rpn
   180 ENTER 135 −
   ```

   The screen shows <disp v="E02">45.0000</disp>. 45° would be acute, but an angle of 135° is
   plainly wider than the corner of a page, so looking before reading catches the slip.

3. 360 ÷ 3 = 120°.

   ```keys E03 entry=alg
   360 ÷ 3 ENTER
   ```

   ```keys E03 entry=rpn
   360 ENTER 3 ÷
   ```

   The screen shows <disp v="E03">120.0000</disp>.

4. Both are measured from the wall, turning the same way, so 140 − 35 = 105°.

   ```keys E04 entry=alg
   140 − 35 ENTER
   ```

   ```keys E04 entry=rpn
   140 ENTER 35 −
   ```

   The screen shows <disp v="E04">105.0000</disp>.
