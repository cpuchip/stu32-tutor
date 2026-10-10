# Learning science: the plan (decision 76)

**Status:** a plan, sent to abacus before anything is built (abacus #6408). Nothing is built.

**The ruling:** Michael took all six choices in [learning-science.md](learning-science.md): "These all sound good"
(decision 76, relayed by abacus #6408). Productive failure is built only after its study is read. Order and scope
are tutor's.

**The binding question:** in what order can the six go in so that each is checked by a machine before it reaches a
lesson, the accepted lessons stay on the site while the work goes on, and abacus's reading load stays even?

## What was measured for this plan (graph.py --json at 518630b, 2026-10-10)

- **55 lessons** in three courses:
  - algebra-to-calculus: units 0 to 12;
  - pre-algebra: units 0 to 5 written;
  - geometry: unit 1 written.
- **46 lessons can carry a "From before" set.** Each requires a topic taught outside unit 0. The other nine require
  only the calculator's own lessons, or nothing: rpn-01, rpn-02, rpn-03, start-01, num-01, num-02, num-04, frac-01
  and whole-01.
- **42 lessons are in unit 2 or later,** where a mixed review has earlier lessons to draw on: 33 in algebra and 9
  in pre-algebra.
- **65 items today, with 65 distinct IDs.** No ID is used in two lessons, but nothing checks that.
- **The student run** (lesson-format.md, check 5) presses every block of a lesson in order on one device, "with
  nothing reset between them". The format therefore puts items at a lesson's end: "a learner's own answer leaves
  the device in a state no lesson can know".

  That rule decides most of the order below. An item placed before an example must not touch the calculator.

## The order

| Step | What | Who | Waits on |
|---|---|---|---|
| 0 | The format and its checks for "From before" and "Mixed review", with controls | tutor | nothing |
| 1 | One pilot lesson with both sections | tutor; abacus reads | step 0 |
| 2 | New lessons written with both from the start | tutor | step 1's read |
| 3 | The sweep: algebra unit by unit, then pre-algebra with the voices pass | tutor; abacus reads | step 1's read |
| 4 | "Why?" blocks: the format, its check, then added in the sweep | tutor | step 0 |
| 5 | Worked examples: twins, faded blocks, problems first | tutor, primer | primer's answer (below) |
| 6 | The review queue in the browser | primer; tutor's ID check | steps 0 to 2 |
| 7 | Productive failure: one trial lesson, designed as a proposal | tutor; Michael | the study (read; below) |

## Step 0: the format and its checks (before any lesson changes)

**`## From before`** comes after a lesson's opening and before its first keys block.
- It holds two items on topics from earlier lessons.
- Each item is `answer: type` and `calculator: no`, so it leaves the student run's device alone.
- Each item is worked by hand, as every item already is (decision 63).

**`## Mixed review`** comes after `## Exercises`, and before `## Checkpoint` where there is one.
- It holds four items. At least two are on topics from earlier lessons.
- These items come at the lesson's end, so they may use the calculator.
- Each has its answer and working, plus slips where a likely one exists. This is the corrective feedback the 2019
  trial's fourth caveat names.

**The checks** (built in graph.py, stu32-tutor after d4a5f08). This plan first split them between check.py and
graph.py. None of them needs the core, so all of them went into graph.py, whose selftest runs with no core or
Docker:
- an item followed by a keys block must sit in `## From before`, and be `type` and `calculator: no`;
- `## From before` comes before the first keys block, the setup included, and holds two items or more;
- every topic of a From-before item is taught by one of the lesson's prerequisites, taken transitively, outside
  unit 0, and is not taught here;
- `## Mixed review` holds four items or more, at least two of them on earlier lessons' topics. No two
  consecutive items share a topic, and the section comes before any `## Checkpoint`;
- each section appears at most once;
- item IDs are unique across lessons and placement. The review queue (step 6) keys on them.

**Controls:** 14 planted faults, each refused for its own reason. Two harmless twins pass: both sections as
planned, and the same with each section reordered with no repeat. A separate run of 12 mutants weakens one rule
each, and every one turns the selftest red.

**Spacing, as an authoring rule:** where the course has one, at least one From-before item comes from an earlier
unit, not the lesson just before. Section 3 of the proposal gives the reason: the longer the gap, the longer it
lasts. This is a rule for the writer, read by abacus, not a check.

## Step 1: the pilot

**poly-02** (algebra unit 5). It requires topics from units 1 to 3 (power, solve, graph-by-hand), so its
From-before set can space by two units or more. It is plain-voiced, so it does not wait on the voices work.

The pilot measures:
- what one lesson costs: items, vectors, slips and the check's time;
- whether two and four items are the right sizes.

abacus reads it before steps 2 and 3.

## Steps 2 and 3: new lessons, then the sweep

**New lessons** get both sections when they are written: pre-algebra units 6 to 10, and geometry units 2 to 9.

**The sweep's cost,** at two plus four items: 46 × 2 + 42 × 4 = 260 new items, each with its vectors in every mode
and entry the lesson offers. That is four times today's 65, so it goes unit by unit.

**The site stays whole.** A swept lesson leaves the publishable list until abacus re-reads it, because its
lesson.md differs from its accepted commit (tools/accepted.py). primer publishes from a pinned commit, so it keeps
its pin until a unit's batch is accepted. No lesson leaves the site.

**The order of the sweep:**
1. **Algebra**, unit by unit from unit 2. It is plain-voiced (decision 71).
2. **Pre-algebra**, together with its voices pass (voices.md: `<voice>` spans). One edit per lesson means one
   re-read for abacus.
3. **Geometry unit 1:** From-before sets only, from pre-algebra. No geometry unit comes before it.

## Step 4: "Why?" blocks (choice 5, as prose)

A fenced block under a main example:

````
```why
ask: Why does the 180 come in here?
because: The angles of a triangle add to 180°, so the third is what is left.
```
````

The page shows `ask:`, and reveals `because:` when the learner asks for it. The words are read, not judged; the
non-author read checks them, as it does all prose.

**check.py:**
- a why block sits directly under a keys block;
- every number in it appears in that example's keys or displays, so the prose carries no number the core has not
  made.

**Controls:** a why block with a number its example lacks, and a why block with no example above it.

**The other option,** a reason item judged by the page, is not planned. The judge (tools/judge.c) compares numbers,
so reasons would need a new answer kind. I would bring it back only if the prose prompts are found too easy to
skip. Then it is Michael's word again.

## Step 5: worked examples (choice 4), with primer

- **A "Your turn" twin** follows a main example: an item on the same skill with new numbers.
  - In a maths lesson it is `type` with `calculator: no`. It is worked by hand and leaves the device alone, so step
    0's rule covers it. That rule widens to cover any item before the last keys block, not only the first.
  - In a calculator lesson (rpn-01 to rpn-03, start-01) the twin is the keys themselves, so it needs the calculator
    mid-lesson.
- **A faded block** is a keys block whose last steps the page hides until the learner has pressed them.
  - check.py runs the whole block unchanged, so it stays verified.
  - A learner who presses wrong keys leaves the device off the student run.
- **The question for primer:** both of the calculator cases need the page to put the device back in the student
  run's state after the attempt. check.py already knows that state after every block (check 5). Can the page load
  it? Until primer answers, twins are written for maths lessons only and no block is faded.
- **Problems first for placed learners** is the page's: a learner placed past a unit opens its lessons at the
  checkpoint, with the examples a link away. The lessons need nothing new. primer to say whether it fits the map
  (adventure.md section 3).

## Step 6: the review queue (choice 3)

The queue is primer's, in the browser only.
- It holds the IDs of checkpoint and Mixed-review items passed, and the date of each.
- An item comes back after several weeks (IES Recommendation 1: "at least several weeks").
- It stores no name, no answer text and nothing sent anywhere, like the stored mode and entry.

**tutor's part:**
- step 0's check that IDs are unique;
- a format rule: an item whose question changes gets a new ID, so the queue never returns a different question
  under an old one.

## Step 7: productive failure (choice 6)

**The study is now read.** Sinha & Kapur's 2021 meta-analysis was refused by the publisher on the first try. A copy posted at
janfasen.nl was opened on 2026-10-10 (`build/learning-science/`, local), and section 8 of the proposal is
updated from it.

**What it found:**
- "a meta-analysis of 53 studies with 166 comparisons that compared PS-I with I-PS design". PS-I is problem
  solving followed by instruction; I-PS is instruction first.
- "a significant, moderate effect in favor of PS-I (Hedge's g 0.36 [95% confidence interval 0.20; 0.51])" for
  conceptual knowledge and transfer.
- For procedures, "a nonsignificant effect (Hedge's g) of -0.03". It "does not hurt or compromise on students'
  knowledge of procedures".
- **Publication bias:** after allowing for it, the authors' estimate is larger. "Overall, an estimation of true
  effect sizes after accounting for publication bias suggested a strong effect size favoring PS-I (Hedge's g
  0.87)." The card should carry both 0.36 and 0.87.

**What bounds it here:**
- **Age, and the kind of skill.** "Contrasting trends were, however, observed for younger age learners (second to
  fifth graders) and for the learning of domain-general skills, for which effect sizes favored I-PS." For the
  young, the pooled estimate "was negative, and these estimates increased (or became more positive) with the age
  range".

  Their example of a domain-general skill is the "control of variable strategy". A maths concept is
  domain-specific, where they found "moderate effect sizes in favor of PS-I". So the trial stays on one maths
  concept, and off the calculator's own lessons, whose keystroke skills are not concepts either.
- **The four strongest predictors** were "instruction building on student solutions, group work as the
  participation structure in the problem-solving phase, evidence for multiple RSM generation in the article, and
  dialogue-dominant social surround facilitation in the instruction phase". A static page has no group and no
  dialogue. It can build only on the solutions a learner is likely to try, which is what our slips already are.
- **The authors' own advice:** "Rather than forcing the implementation of all seven PF design fidelity criteria, it
  is important to consider what is feasible within the cultural context and the available time and resources."
- **Short lessons.** For short interventions, "affective draw of the problem may be critical", and "designing the
  problem-solving phase to accommodate individual work yields a better predictive estimate". A lesson is short and
  worked alone, and decision 71's stories are an affective draw.
- **Narrow evidence.** "nearly 75% of all included comparisons ... targeted learning concepts of math and physics".
- **The printed tables.** In Tables 4 and 5 several intervals do not contain their own estimates as printed (for
  grades 2 to 5, "-0.09 [-0.92, -0.16]"). This plan leans on the text, not those intervals.

**What it means for us:**
1. **One trial lesson, conceptual, in algebra** (the paper's 6th-to-10th band), never in the young courses.
2. **The opener** is a story problem with more than one way in, worked alone. It is an item, so the core judges it.
3. **The likely attempts are its slips,** each made by its own keys in the core. Each hint tells the learner
   that the lesson builds on that attempt.
4. **The lesson's teaching walks through those attempts** and compares each with the method it then teaches.
5. **It meets three of the seven criteria:**
   - problems with several ways in;
   - affective draw;
   - instruction building on solutions, the anticipated ones.

   It cannot meet group work or either social-surround criterion.
6. **Candidates:** lin-01 (slope) or der-01 (rate of change). I would write the design as a proposal first.

**The tension for Michael's card:** a trial needs a measure, and this curriculum collects nothing about learners.
The lesson can be judged only by reading it, and perhaps by a parent watching one learner. Whether a trial nobody
can measure is worth a lesson is his call. I would still write the design, because it costs one proposal.

## Questions this plan raises

- **primer:**
  - Can the page load the student run's state after a block, for twins and faded blocks?
  - Can a From-before set render at a lesson's top, ahead of the examples?
  - Does problems-first fit the map?
- **abacus:**
  - Are two From-before and four Mixed-review items the right sizes to pilot?
  - Is a unit's batch the right reading size for the sweep?
- **Michael, through abacus:** an unmeasured productive-failure trial, or none (step 7).
