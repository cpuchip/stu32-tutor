# angle-02 evidence: angle pairs (geometry unit 1)

## The core (2d08baf)

As angle-01: subtraction in both entries, including a chain (360-120-95 on the line; 360 ENTER 120
− 95 − on the stack).

## Expected values

Oracle: build/proto/g1.py. On a straight line (180 − 70), in a right angle (90 − 35), round a point
(360 − 120 − 95), the two steps of the vertically opposite reason (180 − 70, then 180 − 110, asserted
equal to the first angle), and the exercises (180 − 128, 90 − 62, 360 − 90 − 150, 180 − 41). 9
examples in both entries.

## Sources

Written fresh. The vertically opposite argument is the standard one (each angle is 180° less the
same angle); the course's first general reason, as the plan has it (reasons from G2, a first one
here).

## Non-author read (2026-10-09)

All values and the crossing's labels correct, and the vertically opposite reason valid. Taken: the
yard's path runs out from the corner (one crossing it would make a triangle, which is unit 2), with
a figure; "vertically" explained as at the vertex; the worked example starts from b, the narrow
angle the figure shows, not a; "three streets leave" the cross (roads through it would make six
angles); the opening's "fixed rules" (opposite angles are equal, not a total); "at least one" wrong;
capitalised bullets; exercise 3 reworded.

## Checks

make check at 2d08baf, both entries, the student run in order. Controls (4): the opposite angle
quoted as the one beside it; a chained take-away typed as an add; RPN's 180 and 70 swapped; the
angle beside 41 quoted as 41. All red.
