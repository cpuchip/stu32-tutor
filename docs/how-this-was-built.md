# How this was built

Michael Stufflebeam owns this curriculum and rules on it. The lessons and their checker were written by a team of AI
agents, each a Claude Code session with its own charter, working with him. The commit messages and documents name
these agents (the "seats") and the messages between them. They stay in the history on purpose, so anyone can see how
the work was done and try it themselves.

## The seats

- **tutor** writes the lessons (`lessons/`), their key vectors and quoted displays, the prerequisite graph
  (`lessons/TOPICS`), the courses (`courses/`), and the checker (`tools/`).
- **abacus** reads every lesson and every change to one, and accepts it or sends it back. `lessons/ACCEPTED` is the
  record of what abacus has accepted, and only an accepted lesson is published.
- **primer** builds the learning site from the accepted lessons, with the calculator's own core running in the page,
  and checks every page against that core in a real browser.
- **soroban** writes the STU-32's core and firmware, which the lessons are checked on (`CORE_PIN` in the Makefile).
- **casim** writes Casimir, the computer algebra the STU-mode sections use.
- **basecamp** coordinates the seats and relays Michael's rulings.

## The numbers

A `#NNNN` in a commit or a document (for example "abacus #6736") is a message in our internal message log: the
request, ruling or review that a change answers. The log itself is not public. The number shows which conversation a
line came from and in what order.

Decisions are numbered too ("decision 82"): those are Michael's rulings, recorded by abacus.

## How a lesson gets made

1. **tutor writes it.** Every lesson is written fresh. Textbooks set the scope and order of a course and nothing
   more: no text, figure or problem is copied from a book or from any calculator's manual. The one exception is a
   word-problems lesson's "From the books" set, which quotes public-domain and CC BY-SA problems, each marked with
   its source (Michael's choice, 2026-10-15).
2. **The calculator checks the maths.** Each worked example is a key vector, and `make check` runs every vector on
   the pinned core, in each mode the lesson offers. It then presses the keys the lesson prints, through the
   firmware's own key layer, and they must give the same result. Every display the prose quotes must match the
   device's screen, and every number a "Why?" answer gives must be one its example shows.
3. **The checks are checked.** `make controls` plants a fault in a copy of a lesson, a wrong key, a wrong display or
   a number no example shows, and the check must refuse each one. `tools/graph.py --selftest` does the same for the
   prerequisite graph, the review sections, and the rule that a lesson links each other lesson once.
4. **abacus reads it.** A lesson is published only after abacus accepts it. `tools/accepted.py` holds back any lesson
   changed since abacus last saw it, so a later edit cannot slip through on an old acceptance.
5. **Michael reads it.** Each lesson's `status:` line says whether he has. His reading on his phone (decision 82)
   started a pass over every lesson's prose, a unit at a time, with a check that every number and example stayed
   the same.

## The rules the work kept

- **Original work:** the README says it plainly, and it holds for every lesson and problem here.
- **Oracle first:** a lesson's expected values are computed on the calculator's core before its prose is trusted,
  and `docs/evidence/` recomputes them independently.
- **A check that has never been seen to fail is not evidence:** every check has planted faults it must refuse.
- **Nothing about learners is collected:** the site has no accounts, and progress stays in the learner's own
  browser.
