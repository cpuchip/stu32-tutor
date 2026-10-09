# der-03 evidence: using the derivative

Unit 11's third lesson, as planned (abacus #5263, #5276). It covers:
- the tangent line's equation, y = f(a) + f′(a)(x − a);
- lowest and highest points where f′ = 0, with the slope's sign either side;
- local maximum and minimum;
- in STU, GRAPH's FCN tools (unit 040): EXTR, SLOPE and TANL as numeric checks.

## What the core does (probed 2026-10-08, core c7ab388; build/proto/der3_probe*.sh)

- **The window.** It opens at −10 to 10 with the trace at column 200 (x ≈ 0.0251). With fn-02's window
  (XMIN −2, XMAX 5.98) column 200 falls on x = 2, as fn-02 found.
- **The open graph's soft keys.** They are three pages (BAR, ZOOM, FCN), cycled by ▸ (abacus-firmware
  8510989). FCN holds ROOT, SLOPE, EXTR, AREA and F(X); its gold bank holds TANL and ISECT.
- **The readouts** on q at x = 2:

  | Keys | Readout | Note |
  |---|---|---|
  | `▸ ▸ EXTR` | `EXTRM: 2.0000` | |
  | `SLOPE` | `SLOPE: 0.0000` | |
  | `GOLD TANL` | `Y=0.0000·X-1.0000` | |
  | `F(X)` | `F(X): -1.0000` | |
  | `EXTR` then `ENTER` | — | puts 2 in X and leaves the graph |

- **The tools are numeric.** EXTR uses SOLVE's engine on the slope; SLOPE is a 5-point central
  difference with h = 10⁻⁷·max(1, |x|) (040's vectors' header). So their vectors carry a tolerance
  (1E-15). The lesson calls SLOPE "a very close number, not a rule".
- **x³ − 3x's EXTR from the default open cursor finds 1.** Moving the cursor ten pixels by printed keys
  (`GOLD 4`) did not resolve, so the lesson finds the cubic's points by hand, not on the graph.
- **The digit 6 moves the trace one column right** (GMOVE:6). Five of them take it from x = 2 to 2.1,
  so EXTR has something to find.
- **The graph left open:** the exercises' digits move the cursor. G06 (C) leaves the graph, and a
  control removes it.

## Expected values

Oracle: build/proto/der03.py. Every hand claim is asserted in exact fractions:
- q(3) = 0 and q′(3) = 2, so q − (2x − 6) = (x − 3)² at several x;
- q′(2) = 0 with q′(1) = −2 and q′(3) = 2, and q > −1 everywhere else on a grid from −2 to 6;
- for x³ − 3x, f′(±1) = 0, and f′(−2), f′(0), f′(2) have the signs stated; f(±1) = ∓2 and f(±3) = ±18;
- the exercises: y = 2x − 1, 1.21 against 1.2; g′(−3) = 0 and g(−3) = −4; k′(±2) = 0 and
  k(±2) = ∓16, with the signs of k′ at −3, 0 and 3.

| Vector | What | Value |
|---|---|---|
| T01, T02, T03 | q(3.1), the tangent at 3.1, q(3.05) | 0.21, 0.2, 0.1025 |
| S01 | SOLVE of 2X − 4 | 2 |
| S02 | q(2) | −1 |
| C01, C02 | f(−1), f(1) | 2, −2 |
| G01 | the window set (STU) | 5.98 |
| G02 | five columns right (STU) | x = 2.1, y = −0.99, column 205 |
| G03, G04, G05 | EXTR, SLOPE, TANL (STU) | 2 (the trace moved to column 200); 0; m = 0, b = −1, each within 1E-15 |
| E01, E01B, E02, E03, E03B, E04 | the exercises | 1.21, 1.2, −4, −16, 16, 0.001 |

19 vectors, 13 display vectors.

## Checks

**`make check`:**
- 33s and 35s: 13/13 vectors.
- STU: 19/19.
- Each mode worked through in order, the SOLVE view and the graph included.

**Controls (7), all red:**
- the tangent's value quoted as the curve's;
- SOLVE answered with Y;
- f(−1) without its +/−;
- EXTR's readout misquoted;
- TANL without its gold shift;
- the trace left at x = 2, so EXTR has nothing to find;
- the graph left open before the exercises.

## Non-author read (2026-10-08)

Every value and all six stack walkthroughs checked correct. Taken:
- **"A smooth curve's lowest and highest points are among the places where its derivative is 0" was
  false as written.** An end of a limited stretch can be lowest or highest, and x³ − 3x has neither
  overall. Nothing warned that f′ = 0 can come with no turn (x³ at 0). Now the turns are among the
  places where f′ = 0, with both warnings. The sign test is stated, with its rule (no other zero of f′
  between the test point and the candidate), and exercise 4 asks whether x³ turns at 0.
- **"The best straight-line stand-in" did not follow.** Any line through (3, 0) is close near 3. Now:
  - q at 3.05 is computed (T03), so halving the distance is seen to quarter the gap;
  - y = 3x − 9 is compared, whose gap only halves;
  - the reason is given: q − m(x − 3) = (x − 3)(x − 1 − m), whose gap shrinks like (x − 3)² only for
    m = 2.
- **q's lowest point is now said to be overall** (q′ < 0 for every x below 2 and > 0 above), and the
  cubic's to be only local.
- **The tangent line's form is explained** (at a it gives f(a); each 1 added to x adds f′(a)).
- **EXTR is called a numeric search,** like SOLVE. It started on the answer, so it visibly did nothing;
  now the trace moves to 2.1 first. SLOPE's exact 0 is explained: on a parabola the central average is
  exact.
- **The pages are named,** and ▸ cycles back. Why the trace starts at 2 is said: 400 columns, 0.02
  apart.
- **The 33s reading no longer gets an "On the graph" heading with no graph.** The heading is in the
  STU span, and the 33s sentence closes the section before.
- **SOLVE finds one root near its guess:** said, with 3x² − 3 as the case.
- **Exercise 2 uses the lesson's own test,** g′(−4) and g′(−2).
- **The opening:** the derivative is a function that gives the slope at each point.
