# Decisions

Michael's rulings for the curriculum, in his words, and what follows from each. A proposal stays
marked as one until he rules on it.

## 2026-10-06 (relayed by workspace-basecamp, #4255)

His words: "CC BY-SA, learn.stuffleberry.com, algebra to calculus first", then minutes later:
"though let's use cpuchip.net for the domain for now I don't have stuffleberry setup yet."

1. **Licence: CC BY-SA** for the curriculum. The repo stays private until he sets the licence text
   itself; no LICENSE file is written before then.
   - PROPOSED, not ruled: the program listings and the vectors under MIT, as the firmware is. His
     words named only CC BY-SA. To confirm when he sets the text.
2. **Site home: cpuchip.net for now**, learn.stuffleberry.com once that domain is set up. Nothing is
   built or deployed for the site yet; any framework beyond what cpuchip.net already runs is his
   call first.
3. **First course: Algebra to Calculus.** Proposed syllabus: docs/courses/algebra-to-calculus.md.
4. **First learner: open.** Asked through basecamp when it starts to matter.

## 2026-10-06 (abacus, #4218 and #4224)

- Every lesson sets its mode and display in its first keys; vectors pass in 33s and 35s modes.
- Prose keys are checked against the vectors through the firmware's keymap (tools/keyrun.c).
- Accepted on abacus's review: every vector also runs from a used core, and a quoted display must
  match the device's X line (screen_lines).
