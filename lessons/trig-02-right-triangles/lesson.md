---
id: trig-02
title: Right triangles
status: draft prose (non-author read taken; not yet read by abacus or Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
display: FIX 4
---

# Right triangles

A right triangle has one square corner, a right angle of 90 degrees. Its longest side, across from
the right angle, is the hypotenuse. Pick one of the other two angles and call it A. The side across
from A is the opposite side, and the side beside A that is not the hypotenuse is the adjacent side.
In this picture the right angle is the square corner at the bottom left:

```
                 B
                 |\
                 | \
    opposite     |  \   hypotenuse
    (across      |   \
     from A)     |    \
                 |_    \
                 |_|____\ A
                 adjacent (beside A)
```

The sine, cosine and tangent of A are ratios of these sides:

sin A = opposite ÷ hypotenuse,  cos A = adjacent ÷ hypotenuse,  tan A = opposite ÷ adjacent.

They depend only on the angle, not on the size of the triangle. A triangle's three angles add up to
180 degrees, so two right triangles that share the angle A share all three angles, and one is a
scaled copy of the other: every side twice as long, say, and each ratio the same. So the calculator
can work them out for any angle, on SIN, COS and TAN, and give any side from one other side and an
angle, or an angle from two sides.

## Before you start

The setup from trig-01: the mode you chose, FIX 4, and degrees. Every example starts fresh, except
where one says it carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4 BLUE ∡MODE DEG
```

## A side from an angle

A 5 m ladder leans against a wall, at 70 degrees to the ground. The ladder is the hypotenuse; the
height it reaches up the wall is the side opposite the 70 degrees. sin 70° = height ÷ 5, and
multiplying both sides by 5 gives the height: 5 × sin 70°. On the stack, SIN works on X alone, so
the 5 waits in Y while 70 becomes sin 70°, and × multiplies them:

```keys L01
5 ENTER 70 SIN ×
```

X shows <disp v="L01">4.6985</disp> m. The adjacent side is the ground between the ladder's foot and
the wall, so that distance is 5 × cos 70°:

```keys L02
5 ENTER 70 COS ×
```

X shows <disp v="L02">1.7101</disp> m.

Tangent uses the two shorter sides. Standing 12 m from a tree, you look up 35 degrees to its top.
The triangle has its corner at your eye: the 12 m level with your eye is adjacent to the angle, and
the side opposite runs up from eye level to the top of the tree. So tan 35° = that height ÷ 12,
and it is 12 × tan 35°:

```keys T01
12 ENTER 35 TAN ×
```

X shows <disp v="T01">8.4025</disp> m above your eye level; add the height of your eyes for the
whole tree.

## An angle from two sides

The other way round: given two sides, find the angle. That needs the inverse functions, which take a
ratio and give back the angle: ASIN, ACOS and ATAN, gold above SIN, COS and TAN (books write them
sin⁻¹, cos⁻¹ and tan⁻¹). For a right triangle's angles, all between 0 and 90 degrees, they give the
angle meant; trig-03 shows that a sine belongs to more than one angle in general. A triangle with
sides 3, 4 and 5 is a right triangle: Pythagoras' rule says a triangle whose sides fit
a² + b² = c², with c the longest, has a right angle, and 3² + 4² = 9 + 16 = 25 = 5². The angle A
opposite the 3 has sin A = 3 ÷ 5:

```keys A01
3 ENTER 5 ÷ GOLD ASIN
```

X shows <disp v="A01">36.8699</disp> degrees. The same angle has the 4 beside it, so cos A = 4 ÷ 5:

```keys A02
4 ENTER 5 ÷ GOLD ACOS
```

X shows <disp v="A02">36.8699</disp> again. And tan A = 3 ÷ 4:

```keys A03
3 ENTER 4 ÷ GOLD ATAN
```

X shows <disp v="A03">36.8699</disp>. Any two sides give the angle, through whichever ratio uses
those two.

## Exercises

1. A ramp rises 1 m over 12 m measured along the ground. At what angle does it rise?
2. A 2.5 m ladder stands with its foot 0.7 m from a wall. What angle does it make with the ground,
   and how high up the wall does it reach?

## Answers

1. The rise is opposite the angle and the 12 m adjacent to it, so tan A = 1 ÷ 12:

   ```keys E01
   1 ENTER 12 ÷ GOLD ATAN
   ```

   X shows <disp v="E01">4.7636</disp> degrees.

2. The 0.7 m is adjacent to the angle and the ladder is the hypotenuse, so cos A = 0.7 ÷ 2.5:

   ```keys E02
   0.7 ENTER 2.5 ÷ GOLD ACOS
   ```

   X shows <disp v="E02">73.7398</disp> degrees. The height is sin A × 2.5, with A still in X: SIN,
   then typing 2.5 pushes sin A up to Y (as typing after any function does, exp-03), and × in
   either order gives the same:

   ```keys E02B after=E02
   SIN 2.5 ×
   ```

   X shows <disp v="E02B">2.4000</disp> m. (Check with 0.7² + 2.4² = 2.5².)
