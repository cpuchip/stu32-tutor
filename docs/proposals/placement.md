# Placement: finding a learner's course and unit (PROPOSAL, for Michael)

**Status:** a proposal against the roadmap's placement card (abacus #5211). Nothing is built until he
says go. If he does, tutor writes the questions and the rules, and primer builds the page.

**His words** (basecamp #5210): "I was wondering for one of them if we could create a pre-assesment
that helps find the right course for a student."

## What it is

- **A short check on the learning page:** 6 to 12 questions, about ten minutes. It ends in one
  answer: "start at Pre-algebra, unit 4", with a link there.
- **It runs in the browser and sends nothing.** No account, no score stored anywhere but the
  learner's own browser (if at all), and no analytics. That is the curriculum's standing rule: no
  student data collected.
- **The result is a suggestion,** never a gate. Every lesson stays open, and a learner can start
  anywhere.

## Built from the prerequisite graph

The graph already knows what each unit leans on. Every topic has a lesson and a section, every lesson
has a course and a unit, and a lesson's `requires:` names the topics it needs.

- **A unit's gateway** is the set of topics its lessons require from earlier units. Knowing them is
  what it takes to start there. graph.py can compute it, and `--json` would carry it per unit.
- **Placement asks about gateways.** For each course, a few questions per unit gateway, each tagged
  with the topics it probes.
- **The search runs down the course like a binary search.** Ask about the middle unit's gateway: two
  right moves the check later, a miss moves it earlier. Pre-algebra's 11 units take about 4 steps,
  8 questions. Passing the last unit's gateway moves the check to the next course on the ladder.
- **What it reports:** the unit to start, and for each question missed, the topic it probed, linked
  to the section that teaches it. That is the link the page already makes for a lesson's
  `requires:`, so a learner placed at unit 6 who missed one fractions question is sent back to that
  section, not to unit 1.

## The questions

- **Done by hand.** The courses are hand first, so placement measures the mathematics, not the
  calculator. Calculator-only skills, such as the setup and the keys, are taught in each course's
  first unit and are not placed.
- **Written fresh, like everything else.** None is copied from a test or a book.
- **Exact answers:** a number, a fraction or a short list, typed in and compared exactly. Multiple
  choice only where a typed answer would test typing.
- **A file, `placement/<course>.items`:** `ID | unit | topics | question | answer`. Each answer is
  computed by an oracle in exact rationals, as the lessons' are.
- **Checked by `make check`:**
  - every item's topics exist and belong to its unit's gateway;
  - every unit with lessons has at least two items;
  - every answer matches its oracle.
- **Controls:** a wrong answer, an unknown topic, and a unit with no items. Each must turn the check
  red.
- **A non-author read of the items, for the young end.** A placement question that misleads costs a
  learner a whole course.

## Limits

- **It places by unit,** not by lesson. A course whose units hold one lesson each places as finely
  as its lessons.
- **The questions sample a gateway; they do not cover it.** A learner can pass the check and still
  miss a topic. The topic links in each lesson are the safety net, as they are now.
- **Courses with few lessons place poorly.** Pre-algebra and geometry have 2 and 0 lessons today, so
  placement means most where the lessons exist: the algebra course, now. It grows as the young courses
  do.
- **Unit 0 is not placed.** Every course's unit 0 (start-01; rpn-01's start for the algebra course)
  teaches the calculator, which every learner needs. Placement suggests it alongside the result.

## For him to choose

1. **Go or not.** If go, start with the algebra course, which has lessons to place into, and add
   pre-algebra as it fills.
2. **By hand only,** as proposed, or a calculator allowed for the later courses?
3. **Remember the result in the browser** (a convenience, never sent), or forget it when the page
   closes?
