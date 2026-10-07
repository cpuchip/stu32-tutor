# num-03 evidence

## Expected values (2026-10-06)

Exact integers and fractions in Python, independently of the core:

| Vector | Computation | Exact |
|---|---|---|
| R01 | 3^2 | 9 |
| R02 | sqrt(49) | 7 |
| R03 | 2^10 | 1024 |
| R04 | 10^2 | 100 |
| R05 | 27^(1/3) | 3 (3^3 = 27) |
| R06 | 2^-3 | 1/8 = 0.125 |
| R07 | 16^(1/2) | 4 |
| R08 | (2^3)^2 | 64 |
| R09A | 2 ENTER 3 ENTER 2 | X 2, Y 3, Z 2 |
| R09B | 3^2, the first 2 dropped back | X 9, Y 2 |
| R09 | 2^(3^2) = 2^9 | 512 |
| R10 | 10^3 | 1000 |
| R11 | 1/8 | 0.125 |
| E01 | 5^4 | 625 |
| E02 | 81^(1/4) | 3 (3^4 = 81) |
| E03 | (-2)^3 | -8 |

Every one is exact on the core at 867ddd5 (the cube root of 27, the fourth root of 81 and a
negative base to an integer power included; unit 028 made y^x correctly rounded everywhere).
Displays at FIX 4, grouping on (the device's default): 1,024.0000, 0.1250, 512.0000, 1,000.0000,
-8.0000.

## Sources

- Key positions (layout v0): y^x on its own key with the x-th root in gold above it; 10^x gold above
  e^x; x^2 gold above the square root; 1/x on its own key.
- "In RPN there is no rule for which power comes first": in STU's algebraic line, powers group right
  to left (abacus decision 53, unit 031), so the sentence is limited to RPN.

## Self-audit before the non-author read

R09's draft narrated the stack between its two y^x presses ("9 in X with the 2 back in Y") with no
stopping point; it is now a chain R09A (stop), R09B (after the first y^x: X 9, Y 2), R09 (512).

## Non-author read (2026-10-06)

Every answer and key position checked by the reader; eight findings about claims and teaching, all
taken. The power tower's top-down rule was never stated, and "in RPN there is no rule" overstated it
(the student still needs the rule to read a tower; RPN needs no parentheses to work it); "2 cubed
squared means two things" was wrong in words. Exercise 3, (-2)^3, could not tell the two readings
apart (-2^3 is -8 too), so it is now (-2)^4 = 16 beside a new exercise 4, -2^4 = -16. Also: y^x's
and 1/x's positions given (fourth and fifth in the top row, layout v0); "for any power at all"
dropped (the reader says a negative number to a fractional power is out of y^x's reach; not probed here, and the lesson makes no claim about it); the sentence after R03
made exact; e^x deferred by name; R11 quoted as a display.

Its seventh finding asked for "a third cannot be typed exactly, which is why the x-th root exists".
Probed first: 27 to the power .1.3 (a third typed as a fraction) gives exactly 3 on the core at
867ddd5, as does 27 to 1/3 by 1/x. So the lesson shows the typed third working (R07B) and says only
that the root key states the intent more directly; the probe kept a false reason out of the prose.

## Checks

`make check` at 867ddd5: 18/18 vectors and 21/21 expectations in 33s and 35s, from a fresh and a
used core; 19 keys blocks, 18 of 18 shown, pressed in both modes; 7 displays quoted; worked
through in order.

## After acceptance: the reason x-root exists (abacus #4306)

Abacus probed what the lesson had left open: on 867ddd5, in 33s and 35s mode, -8 ENTER .1.3 y^x is
an error (X left at the exponent), while -8 ENTER 3 x-root gives -2. That is a true reason for the
x-root key, so the lesson now teaches it with vectors: R07C (-2), R07D (the error; the device's X
line shows the message INVALID y^x, quoted as kind message), R07E (continuing: C clears it, X 1/3
and Y -8 as they were). The 35s run first failed on R07E: on the 35s the app layer takes a key
pressed over a message and clears the message itself, with no op, while the runner sends the C and
the core applies the same rule. keyrun now logs such a key as its op when a 35s message was showing
and no op went out, and the state image then confirms the two agree (control: KEYRUN_FAULT=
no-m35-rule turns R07E red again).
