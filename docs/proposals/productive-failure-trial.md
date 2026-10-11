# A productive-failure trial: lin-01, slope (PROPOSAL, for Michael)

**Status:** BUILT in lin-01 (decision 81, Michael: "Build it on lin-01, judged by reading"; "Let's try it"). It
began as a proposal (decision 76's sixth choice, step 7 of docs/proposals/learning-science-plan.md), which abacus
asked for so Michael could judge a concrete lesson (#6425). The build differs from the design below in two places:
- slip C (5 ÷ 3) is left out, as its value is not exact, so the item has three slips, A, B and D (LN1T1A to C);
- "rise per metre across" is taught the other way round, as 3 m along for each metre up (6 ÷ 2 × 5). It is the
  same idea, and the core gives exactly 15, where 5 ÷ (2 ÷ 6) is off in the 34th digit.

lin-01's front matter says it is a trial and names the study it follows.

**The binding question:** can one lesson open with a problem learners have not been taught to solve, and then teach
from the ways they are likely to try it, within what a static page can do and what the evidence supports?

## What the study supports, and what it does not

Sinha & Kapur (2021) is summarized, with its quotes, in the plan's step 7 and the proposal's section 8. In short:
- a moderate effect for problem solving first on conceptual knowledge and transfer (g 0.36, 0.87 after the
  authors' publication-bias estimate);
- none either way for procedures;
- instruction first was better for second to fifth graders, and for domain-general skills.

Of the seven "fidelity" criteria, this design can meet these:
- **a problem with several ways in;** this one has at least four;
- **an affective draw:** a concrete situation in place of a bare ratio. The algebra course stays plain (decision
  71), so there is no cast, but there is a real thing to picture;
- **teaching that builds on the learner's attempts:** on the attempts a learner is likely to make, since the page
  cannot see the learner's own;
- **individual work,** which the study found suits short interventions;
- **part of the "social surround":** the page can say plainly that not finding the answer yet is expected.

It cannot meet group work or teacher dialogue. Those are two of the study's four strongest predictors, and they
need people.

**Why lin-01:**
- slope is a concept, not a procedure;
- the algebra course sits in the study's sixth-to-tenth-grade band;
- the wrong ways in are well known and computable.

## The design

### 1. "Try it first", before anything is taught

A new section, `## Try it first`. It comes after From before and before the setup, and holds one item:

> Ramp A rises 3 m over a run of 12 m along the ground. Ramp B rises 2 m over a run of 6 m. A third ramp must
> rise 5 m and be exactly as steep as ramp B. How far along the ground must it run?

- **The answer is 15:** B rises 1 m for every 3 m across, so 5 m of rise needs 15 m of run.
- **The item is hand-worked:** `type`, `calculator: no`.
- **The prose before it says what is expected:** "Nothing in this lesson has shown how yet. Try any way you can
  think of, a drawing, a table, a rule of your own, and give a number. The lesson starts from what you tried."
  That is the safe-space part of the study's social surround, in the only voice the page has.

### 2. The likely attempts are its slips, each made by the core

| Slip | The attempt | Value | How it is made |
|---|---|---|---|
| A | the same difference: B's run is 4 more than its rise, so 5 + 4 | 9 | `6 − 2 + 5` |
| B | used ramp A instead of B | 20 | `12 ÷ 3 × 5` |
| C | found B's 3 m of run per metre of rise, then divided by it: 5 ÷ 3 | 1.6667 | not exact: left out, or the item takes a tolerance |
| D | scaled the wrong way: 6 ÷ 5 × 2 | 2.4 | `6 ÷ 5 × 2` |

Each hint does not say "wrong". It says what the attempt kept the same, and points to the next section:
- slip A: "You kept the difference between run and rise the same. The next section tests whether that keeps the
  steepness the same."
- slip B: "That keeps ramp A's steepness. The question asks for B's."

### 3. "Four ways people answer it": the teaching, built on those attempts

A section after the item, prose with keys blocks. It works through the attempts in turn, with the core computing
each.
- **The same difference (9).** Test it on an extreme: a ramp rising 100 m over 104 m has B's difference, but it is
  almost a wall. Keeping the difference does not keep the steepness.
- **Scaling (15).** 5 is 2.5 times B's rise, so the run must be 2.5 times B's run: 2.5 × 6.
- **Rise per metre across (15).** B rises 2 over 6, which is 1/3 m per metre. 5 m of rise needs 5 ÷ (1/3) = 15.
- **A drawing.** B's triangle, enlarged until it is 5 tall, is 15 long. It is the same shape, so it is the same
  steepness.

The last two are the same idea. **This is where the lesson names slope:** rise ÷ run, the same number for every
ramp of the same steepness. From there the existing lesson goes on unchanged: two points, the intercept, flat and
falling lines.

### 4. The rest of lin-01 is unchanged

- the From before, the examples, the exercises and the Mixed review stay as abacus accepted them;
- the new item's vectors and its section's keys blocks follow the lesson format, as every example's do.

## What it would change in the format

- **A new section kind, `## Try it first`:** at most one per lesson, before the first keys block, holding items that
  are `type` and `calculator: no`.
- **graph.py's rule:** today an item before a keys block must sit in From before. It would widen to "in From before
  or Try it first".
- **A new rule:** a Try-it-first item tests a topic the lesson itself teaches, which is the point, and is the
  opposite of From before.
- **Controls:** a Try-it-first item on the calculator; a second Try-it-first section; one on a topic from another
  lesson.
- **The page:** primer's page renders items above the setup already (#6460). Nothing new is needed except the
  section's heading.

## The tension for Michael's card

**A trial needs a measure, and this curriculum collects nothing about learners.**
- No accounts, no analytics: the page cannot know whether learners who saw the Try-it-first section understood slope
  better.
- The study's effects were measured with post-tests against control groups, which a static page has neither of.
- The lesson can be judged only by reading it, and perhaps by a parent watching one learner work through both
  orders.

**What there is to choose:**
1. **Build it as one lesson's design**, judged by reading, and keep it if readers think it teaches slope better.
   That costs one lesson's revision: one item, four slips, one section.
2. **Build it as optional:** a "Try it first" the learner can skip, with the lesson reading the same either way.
   This also costs nothing in data. It does weaken the design, though, because a skippable problem is easy to skip.
3. **Don't build it now,** and keep the evidence on file for a time when a measure exists.

My recommendation is 1. The cost is one lesson, the evidence for conceptual topics in this age band is moderate,
and the design never collects anything about a learner.
