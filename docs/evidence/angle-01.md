# angle-01 evidence: points, lines and angles (geometry unit 1)

## The core (2d08baf)

Nothing new is asked of the core: whole-number subtraction and division in both entries, as in
whole-01 and whole-02, with the line written as the core writes it (360÷8, 180-50).

## Expected values

Oracle: build/proto/g1.py. A full turn in 8 parts (45); the wrong protractor scale (180 − 50); the
reflex angle (360 − 50); the angle between two sightings from one arm (110 − 35); the exercises
(360 − 60, 180 − 135, 360 ÷ 3, 140 − 35). 360's divisors (2, 3, 4, 5, 6, 8, 9, 10, 12, not 7) are
asserted. 8 examples in both entries.

## Sources

Scope and order only, from the course plan (docs/courses/geometry.md); the definitions are written
fresh. Nothing is taken from a geometry textbook.

## Non-author read (2026-10-09)

All values correct. Taken: the protractor's 0 line, not its edge (on most protractors they differ),
and lengthening a short arm; the check step re-measured from the new arm; two sightings from one
arm must turn the same way; ∠CBA, ∠B and a small letter as names; answer 2's look-first check
reworded; two awkward sentences.

## Checks

make check at 2d08baf, both entries, the student run in order. Controls (4): the wrong scale's
reading quoted as the angle; a turn cut into 6; RPN's reflex angle the wrong way round; the
sightings added. All red.
