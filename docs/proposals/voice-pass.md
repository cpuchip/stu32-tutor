# A voice pass over the lessons, and back-references linked once (DONE)

**Status:** DONE 2026-10-11 (decision 82; approved abacus #6736). Every lesson of the three courses went through
the pass a unit at a time, each accepted by abacus. The link rule is graph.py's check_links (a2b82bc), and its
pending list is empty since the setup sweep (b0b9d8d, accepted #7103): every lesson links each other lesson once,
and a lesson that leans on another keeps one link to it or has it in its "Before this lesson" box. The setup
sentence went to primer's setup card (abacus ruled setup-line yes, #6900). Kept on purpose, as 3b says:
pre-algebra's "The check:", and "By hand" where the line is the hand working itself. Not done, by design: the
bare "X shows N." sentences were joined to their meaning only where that read better, and rpn-01's "X shows
12.0000." waits until its controls are re-anchored. The maths markup is separate, in docs/proposals/maths-markup.md.

Michael read the live lessons on his phone: "The learn site is a little repetitive I think, a lot of by hand over
and over again." Asked what he meant, he said: "I meant there are a lot of repeated phrases like, by hand first.
We should apply my voicing rules or something? To the prose." On back-references, he said: "names it once then
stops relinking. Unless we're building from a new previous work then that warrants a fresh link since it's
different." His screenshots were der-01, whose prose names lim-02 ("Rates of change" on the page) six times.

**The binding question:** which phrases does a learner meet again and again, which of Michael's voice rules does
each break, and what does each lesson say once in their place?

## 1. What was measured

All 55 lessons at stu32-tutor 0b5f51b, read-only. Prose is what a learner reads in the default voice: outside
every fence (at any indent), front matter and headings, with each `<disp>` quote counted as a number and tags
removed. A lesson's own id is not counted. Two throwaway scripts did the counting, not committed. Two figures
were checked another way: der-01 names lim-02 six times, by both the script and a grep of the source; and the
"by hand" sections below add up to the total.

Michael's voice rules are in two places: the external-voice skill, for writing that goes out under his name, and
principles.md's "Voice Discipline". The ones that apply to prose are:
- cut stock and presenter phrases;
- concrete, direct, unadorned, with no narration of the document's own structure;
- let a fact land in the sentence that earns it, not in a short line of its own;
- state the positive alone, not "not X, it's Y";
- earn significance instead of announcing it;
- em-dashes: zero in the skill, "1-2 per document" in principles.md. The lessons have none, so the difference does
  not arise.

## 2. The counts, by the rule each breaks

| Rule | Phrase | Pre-algebra | Algebra to calculus | Geometry | All | Lessons |
|---|---|---|---|---|---|---|
| stock | "by hand" (any case) | 55 | 88 | 4 | 147 | 50 |
| stock | "The setup from \<id\>" | 10 | 36 | 3 | 49 | 49 |
| stock | "as \<id\> showed / found", "as in \<id\>" | 4 | 50 | 2 | 56 | 31 |
| stock | "Four from this lesson and the ones before it, in no order." | 8 | 33 | 0 | 41 | 41 |
| stock | "Work each by hand unless it says to use the calculator." | 8 | 33 | 0 | 41 | 41 |
| stock | "Two from before" / "Two from unit N" / "Two from pre-algebra" | 6 | 31 | 3 | 40 | 40 |
| stock | "Work each by hand first (a few offer the calculator) …" | 0 | 12 | 1 | 13 | 13 |
| stock | "A wrong answer that comes from a common slip gets a hint that names the step." | 0 | 12 | 1 | 13 | 13 |
| stock | "starts fresh" / "carrying on" / "one chain" | 5 | 90 | 0 | 95 | 39 |
| stock | "Now check it" / "Now the check" / "The check:" | 15 | 0 | 0 | 15 | 7 |
| meta-narration | "This lesson …" (in 39 lessons' opening paragraph) | 17 | 84 | 3 | 104 | 53 |
| meta-narration | "the next section", "the keys below", "as above" | 2 | 29 | 0 | 31 | 22 |
| unadorned | "just" / "simply" / "really" | 5 | 24 | 2 | 31 | 23 |
| antithesis | ", not …" / "not X but Y" (candidates: most are maths, "not negative") | 5 | 28 | 6 | 39 | 26 |
| short line | a one-sentence paragraph of 8 words or fewer (candidates) | 16 | 5 | 4 | 25 | |
| significance | "Notice" / "Note that" / "Remember" / "important" | 0 | 1 | 0 | 1 | 1 |

**The display sentences** are the most repeated of all: "X shows N." 164 times in 37 lessons, "The screen shows N."
102 in 29, and "The X line shows N." 35 in 12, so 301 in all. Each holds a `<disp>` quote that the harness checks
against the device, therefore the quote stays. What breaks the voice is the bare sentence: a quote on its own, then
its meaning in the next sentence. lin-01 already does the other thing: "X shows 0.9615: nearly a metre up for every
metre along."

### "By hand" on the page

A learner meets "by hand" **439 times**, because the page adds 292 of them: it tags every item that is
`calculator: no` with "By hand", and that is 292 of the 300 items. One page shows it 8 times at the median and 14
at most (der-03). The 147 in prose sit here:

| Section | Count |
|---|---|
| From before, the opening line ("Two from before, by hand: …") | 46 |
| Mixed review ("Work each by hand unless …") | 41 |
| The teaching, mostly pre-algebra's worked examples ("By hand, 7 + 5 = 12.") | 32 |
| Checkpoint ("Work each by hand first …") | 13 |
| Exercises ("Do each by hand first, then check.") | 11 |
| Answers (start-01, whole-01) | 4 |

### Back-references

Prose names another lesson **345 times**, and the page links every one. **160 repeat** a lesson already linked in
the same lesson. **43 of the 55 lessons** link one lesson twice or more: 33 of 40 in algebra to calculus, 8 of 12 in
pre-algebra and 2 of 3 in geometry. The most:

| Lesson | Mentions | Repeats | Most |
|---|---|---|---|
| sys-02 | 21 | 17 | sys-01, 14 times |
| der-03 | 15 | 9 | fn-02, 8 |
| der-01 | 15 | 8 | lim-02, 6 |
| exp-03 | 11 | 7 | exp-01, 4 |
| exp-04 | 12 | 7 | exp-03, 4 |
| trig-04 | 10 | 7 | trig-03, 7 |

## 3. The proposal

### 3a. Back-references: each other lesson linked once (Michael's rule)

**The rule:** a lesson links each other lesson once, at its first mention. A different lesson gets its own first
link. After that the prose refers without the id: "the ball from before", "the table", or the fact itself. "As
lim-02 found" becomes "as before", or goes.

**The check, in graph.py:** a second mention of the same lesson id in one lesson's prose is refused. It is counted
in each voice's reading, since a learner reads one: an id once in the story span and once in the plain span is one
link per reading. The check needs these controls:
- a planted repeat (abacus's): refused;
- two different lessons, each named once: green;
- the same id once in each voice: green;
- a repeat inside one voice span: refused.

Ids in item and why fields (4 today) are counted with the prose if the page links them there. primer to say.

**Whether a "Builds on" note is still needed: I think not.** Of the 185 lessons named (each counted once per
lesson):
- **160 are already in the "Before this lesson" box,** by title, which the page builds from `requires:`;
- **6 are forward pointers** ("the next lesson"), which a Builds-on note would not hold;
- **19 are lessons whose objects the prose reuses** without needing their topic, such as der-01's drawing from
  fn-02. Their first mention links them in the sentence that uses them.

A note under the heading would be a third place naming the same lessons, beside the box and the first links, which
is the repetition being cut. The one thing it would add is visibility: the box is folded shut. If Michael wants
the sources visible, the better place is the box's own summary line, "Before this lesson: Rates of change and 9
more", which is primer's to change.

### 3b. The voice pass, a course at a time

**What the pass changes, phrase by phrase:**
- **Mixed review:** both stock sentences go (82). The heading says what the section is, and the page's tag says
  which items allow the calculator.
- **Checkpoint:** "Work each by hand first …" (13) and the slip-hint sentence (13) go. "Questions on the whole
  unit." stays where the heading does not already say it.
- **From before:** "Two from before, by hand: X from lesson, and one from unit N" (40) goes, or keeps only what it
  says about its items that the items do not.
- **The setup sentence** (49) keeps only what is particular to the lesson ("the examples are one chain"). That
  depends on primer's setup card saying the rest (3c).
- **"starts fresh" / "carrying on"** (95): one statement per lesson of how its examples run, in the setup
  paragraph. In an example it stays only where it tells a learner with a real calculator what to clear.
- **The openings:** 39 open with "This lesson …". They start with the problem instead: the ball has a speed at
  every moment, and that speed is a new function.
- **The display sentences** (301): each bare "X shows N." takes its meaning in the same sentence, case by case. The
  quotes themselves are not touched.
- **"just" / "simply" / "really"** (31) and the 39 antithesis candidates are each read and kept or cut. Most of the
  candidates are mathematical and stay.
- **Kept on purpose:** pre-algebra's "By hand, … The check:" in the teaching (32 and 15). That is the course's
  method, in start-01's words "you work each idea out by hand first, and then the STU-32 checks your answer", and
  for a young reader a fixed cue before each check is a signpost. I would drop the "By hand" label where the
  working itself shows it and keep "The check:". **That is Michael's call:** his complaint names "by hand first",
  and in pre-algebra it is teaching rather than stock.

**The oracle for each lesson**, so that a wording pass cannot change what is taught:
- **its skeleton is unchanged:** keys blocks, items, why blocks, `<disp>` quotes and sections, read the way
  check_voices compares two voices;
- **its prose numbers are unchanged, in order,** except those in the stock sentences it removes, which are listed.
  This is the external-voice skill's "ordered numeric comparison";
- **check.py, graph.py and controls.py are green,** and the lesson is held by accepted.py for abacus's read, as any
  edit is.

**Kept from coming back:** check.py refuses the removed stock sentences and an em-dash in prose, with a control
each. The census can be rerun at each course's end.

**The order:** algebra to calculus first, unit by unit as with the why blocks: it has 294 of the 345 lesson mentions
and 33 of the 43 lessons that link one lesson twice, and it is what Michael read. Then pre-algebra, then geometry. Each unit goes to abacus for a read. The maths conversion
touches the same prose; it is done by a script with its own exact check, so it can run before or after a course's
pass, but not in the middle of one.

### 3c. Two changes on the page (primer's)

- **The item tag:** "By hand" on 292 items becomes no tag. "The calculator may help" and "Work it on the
  calculator" are kept, and each course states the default once where it starts (start-01 already does). This
  removes 292 of the 439.
- **The setup card:** if it says "Your mode and FIX 4, as in every lesson", the 49 setup sentences drop that part.

Both are primer's to build. Neither depends on the other, and neither needs a lesson to change first.

## 4. The tension

Michael's voice rules were written for text that goes out under his name: PR bodies, posts, docs. The lessons'
readers are learners, some young. Some repetition there is a signpost, such as the same cue before every check,
or the same frame around every display quote. The pass keeps a fixed phrase only where it signals the same act
each time, and 3b lists which ones, so Michael can strike any of them.
