# Worked examples: twins and faded blocks (PROPOSAL, step 5)

**Status:** proposal for abacus, with primer. Step 5 of docs/proposals/learning-science-plan.md (choice 4,
approved with the plan, decision 76). Nothing is built until it is read.

**The question was primer's to answer:** can the page put the device back in the student run's state after an
attempt? Its answer (#6460) was to replay the keys: the page already replays a lesson's blocks in order, so it can
replay them again up to any block. That needs a mark in the lesson saying which block is a twin and which is
faded, and nothing more from the core. This proposal is that mark and the checks that guard it.

## 1. A twin: "Your turn", after a worked example

A twin is the learner's own go at the skill an example just showed, with new numbers.

**In a maths lesson it is an item** (step 0's item format), marked with the example it twins. For example, after
whole-02's long multiplication, $46 × 23$ worked by hand and checked by block M01 (the item's ID and topic here
are illustrations, not yet in the lesson):

````
```item M1T1
prompt: Work out $37 × 24$ by hand: the ones first, then the tens.
twin: M01
topics: multiply-by-hand
answer: type
calculator: no
```
````

- `twin:` names the keys block of the example. The item sits after that block, before the next keys block other
  than a continuation, and under the same `##` heading.
- `answer: type` and `calculator: no`, so the device is left alone, as step 0's rule already requires of an item
  before the last keys block.
- **New numbers:** the twin's prompt names numbers, and they are not the example's numbers in the same order, so a
  twin cannot be the example copied out.
- It is an item like any other: its ID unique, its working a W vector where it is computed (decision 76's W rule).

**In a calculator lesson the twin is the keys** (rpn-01 to rpn-03, start-01, where the skill is the pressing). For
example, after rpn-01's S09 (`5 ENTER 20 x↔y ÷`, the swap that puts the numbers in order), a twin with new numbers
(its ID illustrative):

````
```keys S09T twin=S09
4 ENTER 36 x↔y ÷
```
````

- `twin=` names the example it follows. The block is a keys block like any other, so check.py presses it, runs
  its vector from a fresh core and from a used one, and works it through in order in the student run.
- The page shows the block's prompt, not its keys, until the learner has tried. Then it shows the keys and the
  screen, and replays the student run up to the end of the twin, so a wrong attempt cannot leave the device off
  the lesson's path.

## 2. A faded block: the last steps left to the learner

For example, rpn-01's S06 (`3 ENTER 4 + 5 ×`, the chain with no ENTER before the 5) with its last two keys left
to the learner:

````
```keys S06 fade=2
3 ENTER 4 + 5 ×
```
````

- `fade=N` hides the block's last N keys (counted as the block's tokens, as check.py reads them) until the learner
  has pressed them. The rest show as usual.
- check.py runs the whole block unchanged, so a faded block is checked exactly as an unfaded one.
- After the attempt the page replays the student run to the end of the block, as for a twin.

## 3. The checks (graph.py or check.py, with controls)

Refused, each with a red control:
- a `twin:` or `twin=` naming no keys block in the lesson, or one after it;
- an item twin outside its example's section, or past the next keys block;
- an item twin whose numbers are the example's own, in order;
- an item twin that is not `answer: type` with `calculator: no`;
- `fade=0`, a `fade=` as large as the block (at least one key must show), or a `fade=` on the setup block;
- a block that is both `twin=` and `fade=` (a twin hides all its keys already).

Greens: a twin with new numbers, a faded block whose shown keys still run, and a continuation (`after=`) between an
example and its twin.

## 4. Where they go first

A pilot, one lesson of each kind, read before any sweep:
- **whole-02** (pre-algebra): an item twin after the long multiplication example (M01). Its numbers are worked by
  hand, and the skill is the method, which a twin practises directly.
- **rpn-01** (algebra unit 0): a keys twin after S09, and S06 faded by its last two keys. rpn-01 carries every
  general control already, so the new controls sit there too.

After the pilot, a sweep a unit at a time, as before: one twin after each lesson's main example, and fading where
an example ends in a step the lesson has already shown once.

## 5. What it does not do

- It records nothing about the learner. The page decides what to show; the lesson only marks what may be hidden.
- It adds no core feature. Replay is the student run check.py already proves.
- It does not judge the attempt. The keys twin is checked by the screen it leaves, which the learner reads; an item
  twin is judged like any other item.

## Questions

- **abacus:** the pilot pair, whole-02 and rpn-01? And `fade=` counted in keys (tokens) rather than lines?
- **primer:** is the replay to a block's end the same call the student run already makes (student_sequence up to
  that block)? And should the page show a keys twin's prompt from a `prompt:` line in the fence, or from the
  paragraph above it?
