# lim-01 evidence: approaching a limit

## Expected values (2026-10-07, core c7ab388)

Oracle: build/proto/lim01.py, modelling the keys (each operation rounded once to 34 digits, half even);
SIN in radians correctly rounded (firmware 044) by dmath; 2ˣ by Decimal's power at 80 digits, rounded
once. 24/24 vectors, 21/21 display vectors (the sine section at FIX 9). The core agreed with the oracle on
every value at the first run, including 2^0.001 and 2^0.0001 (yˣ correctly rounded here).

| Vector | What | Value (shown) |
|---|---|---|
| P01A, P01 | program L, 10 lines, from GTO . . | L010 RTN |
| L01..L06 | f at 1.1, 1.01, 1.001; 0.9, 0.99, 0.999 | 2.1, 2.01, 2.001; 1.9, 1.99, 1.999 |
| Z01 | 1 + 10⁻³⁴, then − 1 | 0 (the sum rounds to 1) |
| S01..S03B | sin(x)/x at 0.1, 0.01, 0.001, −0.001 (RAD, FIX 9) | 0.998334166, 0.999983333, 0.999999833, 0.999999833 |
| N01, N01B, N02 | 1/x at 0.01, 0.001, −0.001 | 100, 1,000, −1,000 |
| N03, N04 | x/abs(x) at 0.01, −0.01 | 1, −1 |
| E01, E01B | (x² − 4)/(x − 2) at 2.01, 1.99 | 4.01, 3.99 |
| E02..E02C | (2ˣ − 1)/x at 0.001, 0.0001; 2 LN | 0.6934, 0.6932; 0.6931 |

## Sources and probes

- Program L, not an equation: the equation editor's "( )" soft key is only on the bar while an equation
  is being typed, so an expression cannot start with a bracket from EQN LIST TOP (probed); a program, as
  in fn-01, keys the same in every mode.
- No other lesson's vectors use the label L (every LBL: in them is F, G, H, K, N, P, Q, R, S, T, U, W or Z).

## Non-author read (2026-10-07)

No wrong value; every display and stack trace came out right. Taken:
- 0 ÷ 0 leaned on fn-03's reason for 1 ÷ 0, which fails for 0 ÷ 0 (every number times 0 is 0): both
  reasons now said.
- "As near as you like" came after the definition, and a table cannot show it: the definition now
  states it; the lesson says a few values only suggest a limit, and the algebra settles this one.
- Coming too close breaks on a 34-digit calculator: Z01 shows 1 + 10⁻³⁴ rounding to 1.
- The factoring x² − 1 = (x − 1)(x + 1) was untaught: shown by multiplying out (and x² − 4 in the answer).
- sin(x)/x was checked from one side only, after "from both sides": S03B at −0.001, with why the sides
  agree; "no tidy algebra" became "nothing this lesson's algebra can do", with the geometry proof named.
- The only "does not exist" was 1/x: x/abs(x) added, two sides that disagree, which is why both sides
  are checked; 1/x at 0.001 shown, not only said.
- "ENTER makes a copy; x² squares the copy" contradicted fn-01: the copy goes to Y, x² squares the x in X.
- "the top, now in Y" in a stack lesson: "x² − 1, now in Y"; "the top of the fraction".
- The program pointer: GOLD GTO . . before entering L (fn-03 can leave a program stopped); a checkpoint,
  L010 RTN; what to do if L is tried at 1.
- "carrying on" said on every continuing block; exercise 1 at 1.99 too, without a needless ENTER;
  exercise 2 at 0.0001 and 2 LN shown; requires gained fraction-bar, display-rounds, type-e, neg-e, abs,
  stopped-program; "rounded to 1 at four places".

## Checks

`make check`: 24/24 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (4): program L without x↔y, sin(x)/x quoted at FIX 4, the limit from below
quoted as from above, two sides that disagree quoted as agreeing; all red.

## Abacus's accuracy read (#4983, 2026-10-07)

Accepted at b51615a, every value rechecked (sin x/x 0.998334166468…, 0.999983333417…, 0.999999833333…;
(2ˣ − 1)/x 0.693387…, 0.693171…; ln 2 0.693147…). One change, made: the spacing of 34-digit numbers is
not the same on both sides of 1 (the 34th digit is the 10⁻³³ place above 1 and 10⁻³⁴ below), so "a number
closer to 1 than the 34th digit is just 1" was false from below (1 − 10⁻³⁴ is 0.999…9, 34 nines, probed by
abacus); now "1 + 10⁻³⁴ would need a 35th digit, and it is just 1". The "( )" question: not intended;
EQN LIST's bar is full, and abacus is giving soroban a unit to let an equation start with a bracket.
