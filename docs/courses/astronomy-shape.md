# Astronomy: the shape of a unit (PROPOSED)

**Status:** a skeleton, by tutor with astrometrics (the sky, the tools and the measurement) and primer (the widgets),
for abacus's review (#12366) before any unit 2 is written. If it changes the courses' character, it goes back to
Michael as a card. The courses themselves are docs/courses/astronomy.md; their four pilots are on main at e54be97.

**Why:** Michael's note on the astronomy-courses card (2026-11-01, via abacus #12366), verbatim: "This is good! And
ive looked at the demo I likr it. I think i do want the lessons to be more interactive, we have the star data and
charts and can walk through each lesson with animations and tools to help. I worry a bit that we are teaching to the
calculator though."

## The flow of a unit: sky → tool → measurement → calculator → check

1. **The sky.** A real question about a real object, with the star data behind it (astrometrics).
   <!-- astrometrics: what a unit opens with, and how the story links come in. -->
2. **The tool.** The learner does something: turns the sphere, lays a ruler across the sky, puts markers on a plate,
   reads a light curve. It is a widget in the lesson (primer's `widget` block, docs/courses/astronomy.md's site
   section) or one of astrometrics's tools, linked.
   <!-- astrometrics: which tools a lesson can open (the hand ruler, grids, eyepiece, lab finder, light curves, the
   3D distance map). primer: which become widgets, and how each one's oracle works. -->
3. **The measurement.** A number the learner takes from the tool, with how sure it is: an angle, a time, a
   brightness. The lesson gives the tool's starting state, so the number it quotes is one the checks can reproduce.
4. **The calculator.** The STU-32 does the work a measurement needs and a head cannot: a tangent, a logarithm, a
   power, a root, hours and minutes, a long chain carried without rounding. That is the test for a keys block (below).
5. **The check.** The answer against a catalog or a published figure, and the items: a learner who measured
   it and worked it out compares with what astronomers found.

## Where the calculator earns its place

A keys block belongs in an astronomy lesson when the step needs one of:
- a function the learner cannot do in their head: TAN, LOG, yˣ, ˣ√y, HMS→, 1/x of a small number;
- a constant or a chain too long to carry by hand without rounding (a parsec in light-years, from c and a Julian year);
- a number the tool measured, whose consequence is the point (Bessel's 0.3136 arcseconds to 657,732 AU).

It does not belong where the step is arithmetic a learner at that course's level does in their head (40 + 25, 7 − 2,
2 × 10). There, the lesson says the sum in prose and moves on. A B lesson may therefore have few keys blocks, or one,
and B's calculator work gathers where the measurements need it: hours and minutes (hms-01), a period from timed minima
(B5), degrees per year of precession (B3).
<!-- abacus: is this the rule you want checked, or a guide? A check could refuse a keys block whose only keys are
digits and + − × ÷ in a lesson of the astronomy courses; that is a format change of mine, and I would plant it. -->

## What the format needs

- **The widget block** (proposed in astronomy.md, primer #12155): `widget <name>` with `key: value` parameters. A
  lesson quotes what the widget shows only from the starting state its parameters set, so check.py and primer's
  oracle agree on the number.
- **A measurement that feeds a keys block:** the lesson names the measured number in prose (from the widget's
  starting state) and the keys block types it. Nothing new is needed in the format for that.
- **A lesson with no keys block but its setup:** today a lesson needs examples to be checked in order. Whether an
  observing lesson with none is allowed, and how it is "done" (graph.py's `no_items`, the last keys block tried), is
  a question for abacus and primer before sky-01 is rewritten.

## The four pilots, and how each changes

- **hms-01 (both courses).** Keeps its conversions: HMS→ and →HMS are real calculator work. Gains a first step on the
  sphere: Vega's place read off the grid as 18h 36m 56.3s and +38° 47′ 01″, then turned into hours and degrees.
- **par-01 (A1).** Keeps Bessel and the triangle: TAN and 1/x are the point. Gains a plate lab before them: two
  plates six months apart, the near star's shift measured with markers, half of it the parallax (astrometrics's D
  Calc station, #12367).
- **sky-01 (B unit 1).** Loses its keys blocks: the 40 + 25 and 7 − 2 are exactly the worry. Leads with the limit
  tool (the faintest magnitude, city against a dark sky) and the dark-adaptation timeline. Its items stay (the
  calculation is the learner's own, by head), and safety stays first.
- **sky-02 (B unit 2).** Loses the fist arithmetic on the calculator. Leads with the hand ruler on the sphere: measure
  the Pointers with three fingers, then read the catalog's 5.37 and see how far off the hand was.

## Questions

1. (abacus) The calculator test above: a guide for writers, or a check that refuses a plain-arithmetic keys block?
2. (abacus, primer) A lesson with no keys block beyond its setup: allowed, and done when?
3. (Michael, only if abacus judges it a change of character) B, the practice course, with little calculator work.
