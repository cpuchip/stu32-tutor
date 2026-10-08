# sys-02 evidence: the built-in solvers

## Expected values (2026-10-07, core 7776c7c)

Oracle: build/proto/sys02.py, Gauss-Jordan on exact fractions; it also reports "none" and "many".
Every answer is a short decimal, which the solvers' 34-digit elimination must give exactly; they do
(23/23 vectors, 61/61 expectations, in 35s and STU mode).

| Vector | System | Answer |
|---|---|---|
| T01..T04 | 2x + 3y = 37, x + y = 15 (sys-01's tickets); the check 2x + 3y | 8, 7; 37 |
| F01 | 0.75x + 1.25y = 6.5, x + y = 6 (D and E kept with R/S) | 2, 4 |
| R01 | y = 2x + 1 as −2x + y = 1, x + y = 7 | 2, 5 |
| M01..M03 | 2x + y + z = 9.5, x + 2y + z = 10, x + y + 2z = 12.5 | 1.5, 2, 4.5 |
| N01 | x + y = 3, x + y = 5 | NO SOLUTION |
| N02 | x + y = 3, 2x + 2y = 6 | MULT SOLUTION |
| E01 | 3x + 2y = 16, x + y = 6 | 4, 2 |
| E02 | x + y + z = 6, 2x − y + z = 3, x + 2y − z = 2 | 1, 2, 3 |
| E03 | 2x − y = 1, 4x − 2y = 5 | NO SOLUTION |
| E04 | x + y = 5, y + z = 7, x + z = 6 | 2, 3, 4 |

## Sources and probes (keyrun --sequence, the device's key path, 7776c7c)

- The solvers are list entries, 2*2 lin. solve and 3*3 lin. solve. In 33s mode they are not in the
  list (firmware 041; decision 58), hence `modes: 35s STU`.
- SOLVE on a solver entry asks A? at once (firmware 043, from tutor #4778: at d75fc75 the keys stopped
  at SOLVE _ and took a typed coefficient as a letter). The prompt is on the line above X; X shows the
  variable's value, and R/S alone keeps it.
- The answers: an X= view, ▼ to Y= (and Z=), wrapping; C leaves the view; the answers stay on the stack
  (x in X, y in Y, z in Z) and in the variables X, Y, Z. The inputs stay in A to F (A to L).
- No solution and one line twice: the messages NO SOLUTION and MULT SOLUTION.
- The list is a ring. Going down from EQN LIST TOP: the learner's equations, then 2*2, then 3*3, then
  the top (probed with two equations of the learner's own). EQN opens at the last entry viewed. So
  from the top ▲ ▲ is the 2×2 solver, from it ▼ is the 3×3, and from that ▲ is the 2×2, whatever the
  learner's equations. The list's soft keys are ▲ ▼ EDIT NEW CAS EXIT (firmware/keymap.c, "EQN LIST");
  NEW goes to EQN LIST TOP from anywhere (probed). The vector runner has no token for NEW, so the
  lesson's keys open the list with EQN alone (the top on a fresh list) and the prose tells a learner
  whose list opens elsewhere to press NEW.
- An earlier draft went one ▼ from the top to the 2×2 solver: true on a fresh list, and the check's
  fresh student run passed it, but wrong for any learner with equations (▼ from the top is their first
  equation). Found by the self-audit against the firmware's own vector M26, then probed.

## Non-author read (2026-10-07)

Every keys block matched its vector and every quoted value. The findings, all taken:
- The solvers' real demand, putting an equation into Ax + By = C form (and 0 for a missing unknown),
  was never shown: a section "Into the solver's form" (y = 2x + 1 as −2x + y = 1) and exercise 4
  (each equation lacks an unknown). "Linear" and "lin." said; the order x, y, z said.
- Opening the list assumed a fresh list, but every learner here has eq-01's and eq-02's equations: the
  keys now open with EQN alone, and NEW (the fourth soft key) is the way to the top for anyone else.
- ▲ and ▼ never located: the first two soft keys of the list, said in "Before you start".
- "Needs no letter" assumed eq-02's SOLVE W was remembered: said outright.
- MULT SOLUTION's "multiple" read as two or three: "endlessly many, every point of one line"; and the
  line is the first equation, not something elimination finds.
- Exercise 1's trap: after N02, D? and E? show 2, not 1, so keeping them gives a wrong answer; the
  exercise says to watch the prompts and the answer types 1 and 1 (and keeps F, which is right).
- The exercises did not test the cases or the form: exercise 3 (NO SOLUTION) and exercise 4 (zeros)
  added.
- "Y holds 4" ambiguous between the stack and the variable: both named, or "y is".
- Wording: "sys-01's fruit stall"; the verbless no-solution sentence, with why A, B and C are kept;
  the letter C against the C key, and C's two meanings in the two forms; * for ×; what a 33s learner
  does (choose 35s or STU); the market's dollars; "EQN now opens at the 3×3 solver".
- `requires:` dropped eqn-typing and sto (not used), added view and stack-levels.

## Checks

`make check`: 23/23 vectors in 35s and STU, from a fresh and a used core, and the student run in order
in each mode. Controls (3): A and B typed the wrong way round, y quoted as x's value, one line twice
quoted as no solution; all red.
