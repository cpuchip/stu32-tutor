# Algebra to Calculus with the STU-32 (PROPOSED syllabus)

**Status:** a proposal for Michael to push against (decision 3, 2026-10-06). Not ruled. The title
is abacus's suggestion.

**Scope sources, scope and order only (no text, figure or problem taken):** the chapter lists of
OpenStax College Algebra 2e, Precalculus 2e and Calculus Volume 1, read from openstax.org's book
pages on 2026-10-06. None of the three is on this box (books/openstax holds physics, chemistry
and astronomy); whether to add them is a question for Michael.

## The shape

Each unit teaches the mathematics, the calculator keys that do it, and one small program, so the
programming thread runs through the course instead of sitting at the end. Every example and
exercise is a vector before it is prose (docs/lesson-format.md). Lessons run 15 to 25 minutes.

The calculator decides some of the order. Today the core has no graphing or tables (the GRAPH,
TABLE and TUTOR menus are not defined at abacus-firmware 153d606) and no derivative key (Casimir's
d/dx is accepted on its own but not yet in the core). So graphs are drawn by hand from values the
calculator computes, and derivatives arrive at the end, as Casimir lands.

## Units

| # | Unit | The mathematics | On the STU-32 | Ready? |
|---|---|---|---|---|
| 0 | The calculator | the stack and ENTER; storing and recalling; the display | ENTER, x<>y, R-down, LAST x; STO/RCL/VIEW; FIX/SCI/ENG | rpn-01 drafted; rest now |
| 1 | Numbers | order of operations as the stack does it; fractions; powers and roots; scientific notation; percent | FRAC, y^x, x-root, %, %CHG, E | now |
| 2 | Equations and inequalities | linear equations; rearranging formulas; absolute value; checking a solution | the equation editor; SOLVE as a checker first, then as a solver | now |
| 3 | Functions | a function as a rule; evaluating; domain; a table of values by hand | a function as a labelled program (LBL ... RTN, XEQ); a loop that prints a table (ISG, VIEW) | now; a TABLE key later would shorten it |
| 4 | Linear functions | slope and intercept; lines through data | linear regression (slope, intercept, r, predicted x and y) | now |
| 5 | Polynomials and rational functions | evaluation, roots, the quadratic formula, complex roots (SOLVE finds one root near its guesses, not all: say so, abacus #4340) | Horner's method as a 4-level-stack program; SOLVE; CMPLX | now |
| 6 | Exponentials and logarithms | growth and decay; logs; solving exponential equations | e^x, 10^x, LN, LOG; SOLVE | now |
| 7 | Trigonometry | angles in degrees and radians; right triangles; the unit circle; inverse functions; polar and rectangular | DEG/RAD; SIN COS TAN and inverses; ->P ->R; vectors | now |
| 8 | Systems of equations | two and three equations in two and three unknowns | the built-in exact 2x2 and 3x3 solvers; when there is no solution or many | now |
| 9 | Sequences, counting and probability | sequences and sums; factorials, combinations, permutations | n!, nCr, nPr; a summing loop; RAND | now |
| 10 | Toward calculus: limits and rates | a limit by approaching; average and instantaneous rate; where 34 digits help and where cancellation still bites | difference quotients as a program; the stack and LAST x | now |
| 11 | The derivative | the derivative as a limit, then by rules; checking a derivative by value | numeric first; Casimir's d/dx when it is in the core | waits on Casimir in the core |
| 12 | The integral | area by sums; the integral; the fundamental theorem checked numerically | a Riemann-sum program; the built-in integral | now (the theorem's symbolic side waits on Casimir) |

About 40 lessons in all. Unit 0 needs perhaps 6 more; units 1 to 12 three or four each.

**Settled with abacus (#4263, 2026-10-06):** GRAPH and TABLE do not come before units 3 to 7
(the accepted order is unit 029 STU's ALG, then the 35s's and 33s's ALG and the stack depth;
"TABLE next, after 029?" is on the roadmap as Michael's call). So units 3 to 7 use the
program-loop table (ISG, VIEW) and hand-drawn graphs, and each place a TABLE key would replace the
loop carries a `TABLE:` note in the lesson source, so the later edit is small. The d/dx key has no
plan yet (Casimir is at CAS 003; the core integration unit is not written); abacus will say when.

**Ruled by Michael (abacus decisions 52-53, #4294 and #4297, 2026-10-06):** TABLE next, GRAPH
after (firmware units 032 TABLE, then GRAPH; 030 SHOW and 031 first). Both are STU-mode features,
so the units that use them run in STU mode (setup `BLUE MODE STU`), and check.py will need STU
support then. Units 3 to 7 keep `TABLE:` notes and gain `GRAPH:` notes where a graph is drawn by
hand, to swap in when those units land. STU's parser (031): powers right to left (2^3^2 = 512;
33s and 35s keep 64), and implied multiplication (2A, 2(3)) ranked as a typed x, so 1/2A is A/2
and 1/(2A) needs brackets. Lessons in 33s mode are unaffected. With implied multiplication the longest known name wins (ALOG( is 10^x, not A x LOG(; ASIN( is the arcsine); a number never follows implicitly (A2 is a syntax error); no implied x across a space (abacus #4321). STU lessons write x wherever a name could hide a product. A tower typed as an equation reads left to right in 33s and 35s mode (2^3^2 = 64), confirmed on Michael's own 33s and 35s (field check 7, abacus #4387).

What GRAPH will do (abacus-firmware work/033-graph.md at efaf424, per abacus #4315; describe in
`GRAPH:` notes, quote no screen until it lands): it plots the equation shown in Equation mode
against TABLE's variable (Y=expr plots expr); the default X window is -10 to 10 with Y fitted to the
curve; the arrow keys trace along it, and ENTER copies the traced value to X; 1/X draws no wall at
its asymptote. STU only, like TABLE (032), whose rows are start + k x step, with ENTER copying a
row's value to X.

**Repin watches (firmware units that will change quoted screens):** 035 (SOLVE ends by viewing the
root, W=3.5000, with no stale prompt) FIRED at the repin to 25dca53, as predicted: the 13 SOLVE
quotes in eq-01..03 failed until they became kind="view", and nothing else moved.
036 (GTO . . to PRGM TOP) landed at the repin to 7c96617: fn-03 teaches it as the way out of a
stopped program. 036b (in 35s and STU mode XEQ and GTO take a letter then ENTER) landed at the
repin to d75fc75: fn-01..03 and poly-01 carry 35s,STU variants with the ENTER, and say so.
034 (→POL's θ correctly rounded) landed there too: trig-04's (3, 4) angle is exact, unpinned.
Re-run fn-03's side vector W01 (docs/evidence/fn-03.md) at every repin: make check does not.
042 (SOLVE with both guesses on one side of a root, abacus #4683) is not in d75fc75: re-run
eq-03's A03 (guesses 10 and 20, root 8) at the next repin.
Field check 8 (abacus #4764): typed entry counts leading zeros toward the 34 digits (0.0000 then
34 digits keeps 29), while rpn-03's "keeps 34 significant digits of every number" is true of
results. If the field check leaves it so, a later lesson on typing long numbers says it.
041 (decision 58, abacus #4645): 33s mode hides what the HP 33s lacked (CMPLX i, vectors, the
linear solvers, LOGIC, CLEAR's STK, →km/→mile, REG/ARG in equations) and adds the 33s's own (x³/∛x,
the ENG shifts, MEM, FN=, HYP as a prefix, its equation syntax and 40 constants). Of the lessons,
only poly-04 uses a hidden feature (CMPLX i): at that repin it offers 35s and STU with a
modes_reason until 039's CMPLX pairs give it a 33s variant.
The single-input hp Ziv unit (after 041, abacus #4666/#4667) makes radian trig, →RAD/→DEG and the
inverse trig functions correctly rounded (today within 8 units): repin trig-01's A02 and E01 and
trig-02's E02, pinned within 1-2 units now, to exact values then. The 33s equation syntax may change
equation quotes in eq-01..03, exp-04 and poly-02; the 33s pass will say.

## What this asks of others

- **abacus:** each lesson's accuracy read, as for rpn-01. Whether GRAPH/TABLE are planned before
  units 3 to 7 are written, since a table key changes how unit 3 teaches.
- **casim, through abacus:** when d/dx reaches the core's keys (unit 11), and what form its output
  takes on the screen.
- **soroban, through abacus:** a web build of the core for the site, when the site starts.
- **ALG mode (unit 029, in progress):** the course stays RPN (decision 7, "RPN first"). If the
  free app's students start in ALG, a short bridge lesson could carry them across.

## Open to Michael

1. Push against the unit order and the scope (anything missing, anything to cut).
2. Whether the OpenStax algebra, precalculus and calculus books should be added to the box for
   scope (read for scope only like the others, under whatever terms each book carries, to be read
   from the book itself), or the public chapter lists suffice.
3. The first learner (decision 4), which sets the pace and the examples' settings.
