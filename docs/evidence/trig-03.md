# trig-03 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/trig03.py with dmath.py (80 digits, rounded once). Every value matched the
core exactly on the first run; the degree trig is correctly rounded (034's exact reduction), and the
oracle asserts cos 120° = −0.5, sin 150° = sin 390° = 0.5 and cos²200° + sin²200° = 1 exactly as keyed.

| Vector | What | FIX 4 |
|---|---|---|
| U01, U02 | cos 120°, sin 120° | -0.5000, 0.8660 |
| U03, U04 | cos 200°, sin 200° | -0.9397, -0.3420 |
| U05 | sin² 200° + cos² 200° | 1.0000 (exactly 1) |
| U06, U07 | sin 150°; ASIN 0.5 | 0.5000; 30.0000 |
| U08, U09 | sin 390°; sin(−30°) | 0.5000; -0.5000 |
| E01, E02 | ACOS(−0.5); cos 240° | 120.0000; -0.5000 |

## Sources and probes

- The promise from trig-02 (abacus #4679): a sine belongs to more than one angle (U06, U07).
- x² gold above √x (num-01).

## Non-author read (2026-10-07)

Nine findings, eight to act on (one confirmed the signs), all taken. The three of substance: cos²θ +
sin²θ = 1 leaned on a triangle the lesson had just said was not there (now: O, P and the point below P
make a right triangle with sides the unsigned across and up, for any angle, and Pythagoras' rule is
stated the way it is used, trig-02 having given its converse); the exercise's answer used cosine's
mirror, 360 − θ, which was never taught, so a learner with only "180 minus" would get 60 (now each
function's mirror is taught with its reason, and the answer says why 60 is wrong); ASIN's range used
negative angles before they were introduced (the section on full turns and negative angles now comes
first, and the one-angle case at ±1 is named). Also: the picture made symmetric and marked with
across = cos θ and up = sin θ; "across" said to carry a sign; U09 read as the arm 30 degrees below and
P half a unit below; "arm", θ and counterclockwise defined; why 150 mirrors 30.

## Checks

`make check`: 11/11 vectors in 33s, 35s and STU, from a fresh and a used core; 12 keys blocks.
Controls: cos 120 quoted positive, ASIN 0.5 quoted as 150, a negative angle keyed without its sign;
all red.
