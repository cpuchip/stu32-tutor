# Decisions

Michael's rulings for the curriculum, in his words, and what follows from each. A proposal stays
marked as one until he rules on it.

## 2026-10-06 (relayed by workspace-basecamp, #4255)

His words: "CC BY-SA, learn.stuffleberry.com, algebra to calculus first", then minutes later:
"though let's use cpuchip.net for the domain for now I don't have stuffleberry setup yet."

1. **Licence: CC BY-SA** for the curriculum. The repo stays private until he sets the licence text
   itself; no LICENSE file is written before then.
   - The program listings and the vectors under MIT: RULED yes later the same day (relayed by
     basecamp #4267, his words: "yes MIT for the programs and vectors, go ahead with rpn-03").
   - The LICENSE text is drafted for his read (LICENSE, LICENSE-MIT copied from his other repos'
     MIT text with his usual copyright line, LICENSE-CC-BY-SA-4.0 fetched from
     creativecommons.org). The version, 4.0 (the current one), is my choice, for him to confirm.
     The repo stays private until he says otherwise.
2. **Site home: cpuchip.net for now**, learn.stuffleberry.com once that domain is set up. Nothing is
   built or deployed for the site yet; any framework beyond what cpuchip.net already runs is his
   call first.
3. **First course: Algebra to Calculus.** Proposed syllabus: docs/courses/algebra-to-calculus.md.
4. **First learner: open.** Asked through basecamp when it starts to matter.

## 2026-10-06 (Michael, relayed by abacus #4334: abacus decision 54, abacus 4f9d2d2)

A full learning platform: logins, progress, quizzes, and lessons with animations and graphics,
built by a new seat that basecamp launches. The lesson files here stay the single source; the
platform renders them, with the real core compiled to WebAssembly in the page, animations driven by
the core's traced states (tools/trace.c is the seed), and quizzes judged by the core. Learners are
13 and over (this answers decision 4's question in part: the age, not yet the level). The order:
the live calculator first, then animations and quizzes, then accounts. Nothing changes in how
lessons are written; the new seat will ask about the format (keys blocks, `<disp>` tags,
continuations), which docs/lesson-format.md is written to answer.

## 2026-10-06 (abacus, #4218 and #4224)

- Every lesson sets its mode and display in its first keys; vectors pass in 33s and 35s modes.
- Prose keys are checked against the vectors through the firmware's keymap (tools/keyrun.c).
- Accepted on abacus's review: every vector also runs from a used core, and a quoted display must
  match the device's X line (screen_lines).
