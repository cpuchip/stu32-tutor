# parallel-01 evidence: parallel lines and a line across them (geometry unit 1)

## The core (2d08baf)

As angle-01. The checkpoint's answers are typed numbers, finished with ENTER in both entries (N= on
the line, X= on the stack), the first items in an algebraic-first course.

## Expected values

Oracle: build/proto/g1.py. The angle beside 65 (180 − 65), co-interior 65 + 115, the exercises
(180 − 58; 180 − 104). The unit's checkpoint, seven items, each slip its own working:
- CPG1A: on a straight line with 47 is 133; slips 90 − 47 = 43, 360 − 47 = 313.
- CPG1B: opposite 38 is 38; slip 180 − 38 = 142.
- CPG1C: round a point with 100 and 145 is 115; slips 100 + 145 = 245, 360 − 100 = 260, 360 − 145 = 215.
- CPG1D: co-interior with 70 is 110; slip 70 (taken as alternate).
- CPG1E: in a right angle with 23 is 67; slip 180 − 23 = 157.
- CPG1F: the reflex angle of 130 is 230; slip 180 − 130 = 50.
- CPG1G: alternate to 72 is 72; slip 180 − 72 = 108.

## Sources

Written fresh. Corresponding angles for parallel lines are taken as given, and said to be one form
of the parallel statement Euclid took without proof, usually called his fifth postulate: it is
Postulate 5 in the usual modern numbering, and Axiom xii in Casey's 1885 edition (books/Euclid,
read 2026-10-09: two lines meeting a third with the interior angles on one side less than two right
angles meet on that side). Euclid's own I.29 derives the equal angles from it; the lesson does not
quote him. Alternate and co-interior angles are then reasoned from it, with
vertically opposite angles (angle-02) and angles on a straight line.

## Non-author read (2026-10-09)

All answers and the eight-angle labels correct, and the reasons valid. Taken: the converse no longer
illustrated by the first fact's contrapositive (a 65° street shown parallel, a 68° one not), and said
to be proved by Euclid (I.27, I.28, read in Casey), not assumed; Euclid's own form of the postulate in
plain words, and its other name; co-interior angles "usually" unequal (both 90° for a right-angle
crossing); the ruler's two edges as the drawn sense of "the same distance apart"; the road named as
the transversal; r = t beside s = u; capitalised bullets. Checkpoint: CPG1B1's hint no longer gives
the answer; CPG1C's other left-out angle (215) as its own slip; a reflex item (CPG1F, for angle-01)
and an alternate-angle item (CPG1G), so the checkpoint covers the unit; slip names and vector notes
aligned.

## Checks

make check at 2d08baf, both entries, the student run in order. Controls (4): the angle beside q
quoted as equal to it; co-interior typed as equal; RPN adding where it should take away; a slip that
is the answer itself. All red.
