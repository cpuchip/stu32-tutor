# Lesson format

A lesson is a folder `lessons/<id>/` with three files. The examples exist as vectors before any
prose is written around them, and `make check` (or `scripts/check-docker.sh`, in a container) runs every
one of them on the STU-32's own core at `CORE_PIN`.

## vectors.txt: the maths

The firmware's key-vector format (`abacus-firmware/tests/vectors.c`): `ID | note | keys |
expectations`, one example per line. Rules (abacus, 2026-10-06):

- Every vector's keys begin `MODE33` and a display setting (`FIX4`, `SCI2`, `ALL`...), so nothing
  depends on how the core started (`ab_init` gives ALL, MEMORY CLEAR gives FIX 4).
- Modes (decision 56): a lesson is checked in each mode it offers, 33s, 35s and STU unless its front
  matter says otherwise. In each mode, a vector's first token, `MODE33`, is set to that mode's
  (`MODE35`, `STU`); no other mode token may follow it. A vector whose ID carries `@` and a list of
  modes (`Q06@STU`, `Q06B@33s,35s`) applies in those modes only, and replaces the shared vector of
  the same ID there: where a mode's maths or keys differ (decision 53's implied multiplication, an
  STU-only TABLE), and where a block exists in some modes only. The differences between the modes
  are abacus decisions 22, 45, 46, 52, 53 and 56.
- Entries (decision 63; agreed with primer #5027): a lesson that offers entries (front matter
  `entries:`) is also checked in each entry, and the entry's token (`RPN`, `ALG`) is put right after
  the mode's. A vector's `@` list may name entries as well as modes (`Q01@alg`, `Q01@STU,rpn`); the
  narrowest vector that fits a mode and entry serves, and two that fit equally narrowly are refused.
  On the algebraic line a result is ANS, shown in X's place, and the stack is left alone (firmware
  029 rule 6), so an `alg` vector expects `N=` (and `%LINE=`, the line as typed) where an RPN vector
  expects `X=`.
- Avoid E with no mantissa and the first key after an error, unless that is the lesson.
- Every vector has at least one expectation, and every expected value is recomputed independently
  (exact rationals, mpmath or SymPy) with the computation kept in `docs/evidence/`.
- Every physical constant names its CODATA year in the note. Every example is ours: nothing is
  copied from a textbook or from any calculator's manual.

## fmt-vectors.txt: the displays

The firmware's display-vector format (`tests/fmt_vectors.c`): `ID | note | value | setting |
options | text`. `D-Snn` is what X shows after key vector `Snn`. The prose may quote only a display
a display vector has verified, at the lesson's display setting.

## lesson.md: the prose

Front matter:

```
---
id: rpn-01
title: The stack and ENTER
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---
```

- `requires:` lists the topics (lessons/TOPICS slugs) the lesson leans on and does not teach, on one
  line, space-separated; empty for a first lesson. A topic is required when a learner who skipped
  the lesson that teaches it would be lost or misled; a key named only as a landmark, or an idea
  re-taught in place, is not. TOPICS gives each topic its lesson and section (- for the opening);
  `tools/graph.py` (in `make check`) refuses an unknown slug, a lesson requiring its own topic, a
  heading not in its lesson, and a cycle. A new lesson adds its topics to TOPICS.
- `status:` is `draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)` until Michael's
  read; the learning page marks a draft. Acceptance is never written here: lessons/ACCEPTED is the
  one record of what abacus has accepted, the list the site publishes from, checked by
  `tools/accepted.py` (a lesson changed since abacus last saw it is held back). The front matter's
  `status:`, `requires:` and `tools:` lines are bookkeeping and may change without holding it; any
  other change does (`accepted.py --selftest`, in `make controls`, plants both kinds).
- `modes:` lists the modes the lesson offers, by the MODE menu's labels (`33s 35s STU`, the
  default). A lesson that offers fewer says why in `modes_reason:`. The page opens in the link's
  mode, else the reader's remembered one, else STU, else `default:`, else the first offered
  (docs/proposals/mode-variants.md).
- `entries:` lists the entries the lesson offers, `rpn` and `alg`, the default first (`entries: alg
  rpn` for the young courses, decision 63). A lesson with no `entries:` is RPN only, as every lesson
  of the algebra course is, and nothing about it changes. Algebraic entry is STU mode's alone
  (firmware 029 rule 2: the 33s and 35s modes refuse ALG), so a lesson offering `alg` gives
  `modes: STU` and a `modes_reason:`.

- `setup` is the keys the student presses once, with `{mode}` for MODE's soft key; the checker
  presses them, the mode filled in, before every example. The lesson prints them, `{mode}` and all,
  in a ```` ```keys setup ```` block, which must match (the page fills in the mode). A lesson that
  offers entries presses `{entry}` too, right after the mode with the same keys (`BLUE MODE {mode}
  BLUE MODE {entry}`), because its vectors set the entry right after the mode; the page fills in
  `RPN` or `ALG`, the MODE menu's labels.
- Each example is a ```` ```keys Snn ```` block: the keys the student presses, by the legends
  printed on the STU-32 (abacus `layout/stu32-v0.json`). A shifted function is `GOLD` or `BLUE` and
  then the legend printed in that colour (`GOLD LASTx`, never `LASTx` alone). A number is its
  digits (`1.05`). A soft key is the label its menu shows (`FIX`, `33s`). A variable is its letter
  (`STO A`).
- A block that carries on from the one just before it is ```` ```keys Snn after=Smm ````, and holds
  only the keys pressed next. Its vector holds the full sequence (Smm's keys, then these). Use it
  wherever the text says "now press", and always after a stopping point: a stopping point leaves a
  number half typed, and a fresh example after it would type into that number.
- A block with no `mode=` is shared: it is printed and checked in every offered mode. Where a mode
  needs other keys, a variant follows it at once with the same ID, ```` ```keys Snn mode=35s,STU ````,
  and replaces it in the modes it names; a block may also have variants only (an STU-only example).
  A variant may carry its own `after=`; otherwise it continues what its shared block continues.
- Prose that differs by mode goes in `<mode m="35s,STU">...</mode>` spans, inline or around whole
  paragraphs; a quote for one mode is `<disp v="Snn" m="STU">...</disp>`, and a quote inside a span
  holds in the span's modes. No span inside a span. A value quoted differently by mode (33s's real
  part of a pair against 35s's a i b, poly-04) has its own display vector, `D-Snn@33s`, which that
  mode's quote uses before `D-Snn`.
- Entries are built the same way: a variant ```` ```keys Snn entry=alg ```` (which may also carry
  `mode=`), prose in `<entry e="alg">...</entry>` spans, a quote `<disp v="Snn" e="alg">`, and a
  display vector `D-Snn@alg`. A `<mode>` span may hold an `<entry>` span and the reverse; neither
  holds one of its own kind. On the algebraic line, `ENTER` is the = key (there is no `=` legend),
  a bracket pair is the soft key `()` with `▶` to step out, and a fraction is typed as a division.
  ANS is `GOLD LASTx` (LASTx's key types ANS on the line, firmware 029's answers); its vector token
  is `LASTX`, not `ANS`, which is another op (measured 2026-10-08: the printed key and an `ANS`
  vector disagree, and a `LASTX` vector gives the same line and result).
- A quoted display is `<disp v="Snn">text</disp>`. Other screen lines take a kind: `eqn` (an equation shown on X), `prompt` (a prompt
  on X, like `SOLVE _`, or on the line above, like XEQ's `X?`), `message`, `entry`, `view`, and
  `status` (a token of the status band). A block may stop at a prompt only when the block right
  after it continues it (`after=`) and answers it. An annunciator in the status band (the fraction
  indicator ▼ or ▲, RAD) is `<disp v="Snn" kind="status">▼</disp>`. A screen line that is not a value (a VIEW's
  `B=49.75`) is `<disp v="Snn" kind="view">text</disp>`, checked against the device's X line
  (text and kind) since no display vector covers it. The kinds are view, prompt, message, entry
  (a number still being typed shows with its cursor: 7_) and row (TABLE's selected row on the X
  line, the variable's value then the equation's, written with one space between:
  `<disp v="B04" kind="row">0.0000 3.0000</disp>`; the device spaces them to the line's width),
  and line (the algebraic line as typed, shown in Y's place above the result: `<disp v="Q01"
  kind="line" e="alg">2÷4</disp>`).
  A quoted value's display vector may carry
  `w=21`, the device's X-line width (firmware/screen.c FMT_WIDTH); the runner's default of 22
  agrees with the device only for short values.
- No em-dashes (the house voice, external-voice skill). No child is ever named.
- Each other lesson is linked once (decision 82). The page shows a lesson id as that lesson's title, linked, in the
  prose, an item's prompt and a why block's ask and because (a slip's hint shows the title unlinked, primer #6738).
  So a lesson names each other lesson's id once, at its first mention, and then refers to it without the id ("the
  ball from before"); a different lesson gets its own first link. graph.py (in `make check`) refuses a second
  mention of one id in any reading a learner can have (voice × mode × entry, check.py's views), except in a lesson
  on its LINKS_PENDING list, which the voice pass (docs/proposals/voice-pass.md) has not reached: there the repeats
  are counted, and a listed lesson that links each lesson once is refused until it comes off. `graph.py
  --selftest` plants a repeat, a repeat inside one voice, mode or entry, and one between the prose and a prompt or a
  why block, and accepts one id once in each voice, mode and entry, and an id in a slip's hint.

## Items: quizzes and checkpoints

An item asks a question the learner works by hand and then answers; the page judges the answer with
the core. Michael ruled them in (decision 67: "hints tied to slips", the calculator offered where an
item justifies it). An item is a fenced block in lesson.md, its fields one a line:

````
```item K01
prompt: f(x) = x³ − 2x. What is f′(2)?
topics: power-rule sum-multiple-rules
answer: type
calculator: no
slip: K01A | the −2x term dropped | Every term has a derivative: −2x gives −2.
slip: K01B | f(2), not f′(2) | That is the height at 2. Take the derivative first, then put in 2.
```
````

- `prompt:` the question, as the page shows it.
- `topics:` the TOPICS slugs it tests; a miss links back to the section that teaches each.
- `answer:` `type` (the learner types the number; the hand work is the skill) or `work` (the learner
  works it on the calculator; the keys are part of the skill).
- `calculator:` `yes` or `no`: whether the page offers its calculator while the item is open.
- `keys:` the working, as printed keys, shown after the attempt. Needed for `work`.
- `working: none`, on a `type` item only: its answer is counted or recalled, not computed (how many
  roots at most; how many prompts). The same goes when a working would only retype the answer through one
  identity step (0 + 5 for x − 5 = 0; abacus #6465). Leave it out for a computed answer.
- `slip: VID | name | hint`, any number: a wrong answer a learner is likely to give, the slip that
  gives it, and the hint the page shows when the learner's answer is that slip's value.
- The answer is vector `ID` in vectors.txt, and each slip is vector `VID`, written and run like every
  example, in every mode and entry the lesson offers. A slip's keys are the slip's own working (the
  −2x dropped: `2 x² 3 ×`), so its wrong value is made by the core, not typed in. A `type` item's
  vector is the answer typed (`10`).
- The answer is the vector's last `X=` (`N=` on the algebraic line), or its `X#c,t` for a numeric
  answer. Each slip needs an exact value, and it must not be the answer (or, with a tolerance,
  within it).
- **A computed typed answer has its working on the core** (abacus #6439). The vector `IDW` beside it
  works the answer out, and its answer must be the typed one. Otherwise a wrong typed answer would pass
  every check, with only a reader to catch it.
  - A `calculator: yes` item's working uses the keys its prompt names (XEQ, SOLVE).
  - A hand item's working is the arithmetic of the hand method.
  - check.py refuses:
    - a computed answer with no working;
    - a working that gives another value;
    - `working: none` beside a working vector;
    - any other `working:` value.
  - Files whose items predate the rule are listed in check.py's WORKING_PENDING. Each comes off when its unit's
    batch gives every computed item its working, and a listed file with nothing left to give is refused.
- Nothing before an item may show its answer or a slip: no keys block and no `<disp>` of their IDs.
  The item's own vectors need no keys block; the page reveals them after the attempt.
- Items are not part of the student run (check 5): a learner's own answer leaves the device in a
  state no lesson can know, so items come at the end of a lesson (a unit's checkpoint is a
  `## Checkpoint` section in its last lesson). The one exception is a From-before set (below), whose
  items leave the device alone.
- An item's ID is its own across every lesson and placement file: the browser's review queue keys on
  it, so an item whose question changes takes a new ID.

### Why? blocks

A "Why?" prompt under a worked example (decision 76, step 4; the proposal's section 5, self-explanation):

````
```why
ask: Why does Y hold 7 when + is pressed?
because: ENTER copied the 7 up into Y, and the 5 replaced the copy in X, so + gives 12.
```
````

The page shows `ask:` and reveals `because:` when the learner asks for it. The words are read, not judged; the
non-author read checks them, as it does all prose.

check.py refuses:
- a why block without exactly one `ask:` and one `because:` line, or with any other line;
- a why block with no worked example above it (the nearest keys block other than the setup);
- a why block with a `##` heading between it and that example;
- a why block naming a number its example doesn't show. Numbers are compared by value, so 12 and 12.0000 are one
  number, and an example's numbers are those in its keys, its prose and its quoted displays. The digits of an ID
  (the 1 of `keys S01` or of `<disp v="S01">`, or of a lesson id such as rpn-01, which the page shows as its
  title) are not among them, and a lesson id in a why block is not a number it names.

The example's region also takes in its lead-in, the prose paragraph directly above its first keys block (abacus
#6632). An example given in several entry variants (`mode=` or `entry=` blocks one after another) is one example, so
its lead-in is the paragraph above the first variant. A paragraph that is a `##` heading or ends in another fence is
no lead-in, and one further up doesn't count. The lead-in rule holds from the algebra course on; pre-algebra's why
blocks were accepted before it and are left as they are.

A why block is part of the skeleton every voice shares, so it never sits inside a voice span. The controls are in
rpn-01's set (a number the example doesn't show, no `because:`, no example above, a heading between, a number from
two paragraphs above, a number from above a heading when the example has no lead-in, a number found only in the
example's ID, a number found only in a lesson id, and as greens a good one, a why block naming a lesson id, and a
number from the lead-in) and whole-01's (a why block inside a voice span, and as a green a number from the lead-in
above the first of an example's entry variants).

### Voices: story and plain

A lesson may offer two readings of the same skeleton (decision 71: story first for the young courses, the algebra
course plain; docs/proposals/voices.md).
- **Front matter:** `voices: story plain`, the default first. A lesson with no `voices:` line has one voice.
- **Spans:** prose that belongs to one voice goes in `<voice v="story">…</voice>` or `<voice v="plain">…</voice>`.
  Everything outside the spans is shared.
- **A span holds prose only:** no keys block, no item, no `<disp>`, no `<mode>` or `<entry>` span, no other
  `<voice>` span, and no `##` heading. So every voice has the same examples, quotes, items and sections.
- **Numbers:** the problems are the same problems in every voice. A voice changes the words that set a problem up,
  never its numbers. Every reading's numerals in prose (outside its keys blocks, items, quotes and headings) are the
  default's, the same values in the same order, in a worked example's setup as in the exercises (abacus #6550). A
  number that belongs to one voice only, such as a character's age, is spelled out in words, or abacus rules on
  it.
- **The cast** (`cast:` and `walk-ons:`, lore/) belongs to the story voice. The plain reading names no one.

check.py refuses:
- a span that breaks those rules;
- a span in a lesson with no `voices:` line;
- a span for a voice the lesson doesn't offer;
- an offered voice with no span of its own;
- a reading whose keys blocks, items, quotes or `##` headings differ from the default's, in order (a second proof
  under the span rules);
- a reading whose numerals in prose differ from the default's.

Every other check then runs on the default reading. graph.py refuses a plain reading that names a cast member or a
walk-on.

The controls are in whole-01's set:
- a plain exercise with another number, and a plain worked-example setup with another number;
- a quote, a keys block and a heading, each inside a voice span;
- a span with no `voices:` line;
- a span in a voice the lesson doesn't offer;
- and, as greens, a plain sentence and a story sentence reworded with the same numbers. whole-01 is told in both
  voices, so its spans are the plants' anchors.

graph.py's selftest plants a plain voice that names its cast.

### Maths: `$…$` and ```` ```math ````

The page typesets maths with KaTeX (docs/proposals/maths-markup.md: TeX inside, with primer; everything typeset,
arithmetic too, Michael via abacus #6967). The lesson says where the maths is:
- **Inline:** `$…$`. A span opens at a `$` and closes at the next `$` on the same line. It is never empty, never
  starts or ends with a space, and never crosses a line. A `$` that is not maths is written `\$`.
- **Display:** a ```` ```math ```` fence holding one equation on one line, with no `$`.
- **Where it may go:** prose, an item's `prompt:` and `slip:` lines, and a why block's `ask:` and `because:`. It may
  not go in a heading, a keys block, a `<disp>` quote, a tag, or an item's other fields.
- **It may not cross a tag.** A span lies wholly inside one `<voice>` span or outside them all.
- **A key's name stays plain:** "the x² key", never a span before the word "key".
- **Inside a span, TeX** over a closed list: `^2` or `^{…}`, `\frac{a}{b}`, `\sqrt{…}`, `'` and `''`, and `\times
  \div \le \ge \pm \neq \cdot \pi \theta \infty \, \left \right \% \angle` (the last two by abacus #7218), and
  `\operatorname{LCM}` and `\operatorname{GCF}`, so those names set upright (abacus #7227), and `\sin \cos \tan
  \log \ln` (abacus #7263), whose following space the reader keeps ("sin x"); a thousands comma is `10{,}000`; a
  sum's ellipsis is `\dots` (its following space kept too: "1 + 2 + \dots + 10"); ½ ¼ ¾ are `\dfrac{1}{2}` and the
  like (KaTeX refuses the characters). The
  calculator's key names (SIN, COS, TAN, LOG, LN, ABS) are refused inside a span: a key is plain. Any
  other character is taken as written, so − × ÷ ≤ ≥ ° π may be written as they are. A bare `%` is refused: TeX
  takes it as a comment and drops the rest of the span.
- **What is a span** (the conversion's rules, docs/proposals/maths-markup.md §6): an expression or relation,
  arithmetic too, and a power, root, prime or function on its own (LCM(4, 8) = 8 included); a variable named in
  words. Every fraction is stacked, a bracket over a bracket too (`\frac{1 + 3}{4 + 8}`), and a mixed number is one
  span (`1 \frac{1}{8}`). A lone number, a register (X Y Z T), a memory letter, a key's name (INT÷, Rmdr), a point,
  a lone ∠ name and a lone LCM or GCF stay plain; a word unit and an aside's brackets stay outside the span. In
  geometry a capital is a point (plain) and a small letter is an angle (a span: "the angles $p$, $q$, $r$ and $s$").
  Decided by hand, never by the converter: a lone a, A or I in a sentence with a one-letter span, a lone capital
  that is also a memory letter ("3.5 in $W$", a variable; "W is on the 5 key", the calculator's letter), and a
  register letter in an expression ("$D = R × T$" is time; "2 × X" is the register), a lone product of letters
  ("Take $mx$ from both sides"), and a formula an operator joins to a word ("sin A = opposite ÷ hypotenuse",
  plain as a whole so no half of it is typeset). A letter used as a function counts as the lesson's ("the domain
  of $r$"), and a product of letters is read where an operator touches it ($y = mx + b$). Each decision is a line of
  tools/maths_hand.txt, which the converter reads, so a regeneration reproduces every accepted lesson.
- **No half-spans** (abacus #7274): check.py refuses an operator in the prose touching a span ("eˣ = $3x$") and a
  span glued to a raised letter, a word character or a bracket ("$500 × 1.04$ᵀ", "($2x − 3$)$x$"): the whole
  expression goes in the span. A plural s is English ("how many $\frac{2}{10}$s"). A raised letter (ˣ ʳ ᵗ ᵀ …) is
  `^{x}`, and a formula in words writes its words as `\text{…}` (letters and spaces only, and only in a span with a
  function, operator or relation): `$\sin A = \text{opposite} ÷ \text{hypotenuse}$`.
- **An absolute value** is `$|x − 3|$`, the bars with no space inside (a table row is never read as bars), and a
  **factorial** is `$5!$`, the `!` after a digit or a bracket only. A `|` may not sit in a span on a slip line,
  where `|` separates the fields: check.py refuses it. tools/maths_convert.py applies them a course at a time.

check.py reads every span back to the plain text the lessons wrote before the markup (`maths_text`: `^2` as ²,
`^{r × t}` as ^(r × t), `^{2.5}` as ^2.5, `\frac{1}{4}` as 1/4, `\sqrt{x + 1}` as √(x + 1), `'` as ′), and every
other check reads that text. So the why rule and the voices rule count a span's numbers as written (1/4 names 1
and 4; a superscript is not a numeral), and seen() lifts a span out before it strips tags and lesson ids, so
"x < 2 … >" and "x-10" are read whole.

check.py refuses:
- a `$` with no closing `$` on its line;
- an empty span, or one that starts or ends with a space;
- a span in a place maths may not go, or across a tag;
- a span written before the word "key";
- a ```` ```math ```` fence that is not one line of TeX;
- a command off the list, a bare brace, or a command missing its argument.

The controls are in rpn-01's set: a span across a line, in a heading, in a keys block, with a command off the list,
and before "key"; a why number the example's maths does not show; and, as greens, a why number shown only inside
maths, and maths with `<` and `x-10` read whole. whole-01's set adds a span across a voice tag and voices whose
maths differ in a number, with the same maths in both voices as a green.

### Twins and faded blocks (step 5)

docs/proposals/worked-examples.md, approved by abacus (#7299) with primer's page answers (#7300).
- **An item twin**, after a worked example: an item with `twin: <block ID>`, `answer: type` and `calculator: no`,
  right after the example's blocks (a continuation of the example may come between) and under the same `##`
  heading. Its operands are not the example's own, in any order: $24 × 37$ is not a twin of $37 × 24$. Nor are they
  any problem's in its unit, an item's (the checkpoint, From before, Mixed review) or an exercise's, or the twin
  would hand the learner that answer (abacus #7310). A prompt's operands are its problem's, its first maths span, so
  "Work out $37 × 24$ in parts: $37 × 4$, ..." is [24, 37] (its first span holding a number). A power's raised
  number counts: $2^{5}$ is [2, 5] and $(−2)^{4}$ is [2, 4], where a reading without powers gives [2] for both. Nor
  are its numbers with its answer another problem's numbers with its answer, sorted: that catches a copy, a swap and an inverse
  alike, 57° giving 123 against 123° giving 57 (abacus #7350). Its answer is not its unit checkpoint's on a topic they
  share, or "it came out 7" passes the checkpoint by memory (abacus #7333). It is an item like any other, with its
  typed answer, its working and its slips as vectors.
- **A keys twin**, in a calculator lesson: ```` ```keys ID twin=<block ID> ````. Its prompt is the paragraph above
  it, after the example's own lines, so a twin needs at least two paragraphs between it and its example. Its
  operands are new, and check.py presses and runs it like any block. The page holds its keys back until the
  learner has tried.
- **A faded block**: ```` ```keys ID fade=N ```` hides the block's last N keystrokes until the learner has pressed
  them. A keystroke is a key with its shift: "GOLD INT÷" is one, and a fade may not split them. A fade hides at least
  one keystroke and leaves at least one shown, never on the setup and never on a twin. check.py runs the block
  unchanged. The paragraph above a faded block gives the reason, not the hidden keys: it may not name them in
  order, by legend or by word (× as multiply or times, + as add), or the learner copies instead of finding them
  (abacus #7321).
- After an attempt the page replays the student run to the end of the block, so every later block starts from the
  full keys (primer #7300).

check.py refuses each break of these rules, with red controls in rpn-01's set (keys twins and fades) and
whole-02's (item twins).

### Review sections

Two sections bring earlier lessons back (decision 76; docs/proposals/learning-science-plan.md):
- **`## From before`** opens a lesson, after its opening and before its first keys block (the setup
  included). It holds two items or more on topics taught by the lesson's prerequisites, taken
  transitively, outside unit 0. Each is `answer: type` and `calculator: no`: worked by hand and typed,
  so the device the student run presses is untouched. Where the course has one, at least one item comes
  from an earlier unit, not the lesson just before (spacing; a rule for the writer, read by abacus).
- **`## Mixed review`** comes after the last keys block, and before `## Checkpoint` where there is one.
  It holds four items or more, at least two of them on topics taught by earlier lessons, and no two
  items in a row share a topic (interleaving). Its items may use the calculator, and each carries its
  answer and working, with slips where a likely one exists.
- **`## Try it first`** (decision 81, the productive-failure trial; docs/proposals/productive-failure-trial.md)
  opens a lesson with a problem it has not taught yet, after From before and before the first keys block. It
  holds one item or more, each `answer: type` and `calculator: no`, and each on a topic the lesson itself
  teaches: the opposite of From before. Its slips are the likely ways in, made by the core, and their hints say
  what each attempt kept the same, not that it is wrong. The lesson's teaching then starts from those attempts.
  A lesson that carries it says so in its front matter, `trial: …`, naming the study it follows.

graph.py (in `make check`) refuses:
- an item followed by a keys block that is not in `## From before` or `## Try it first`;
- a Try-it-first item that is not `type` and `calculator: no`, or that tests a topic another lesson teaches;
  a Try-it-first section after a keys block, or with no item;
- a From-before item that is not `type` and `calculator: no`, or that tests a topic the lesson teaches,
  a topic no prerequisite teaches, or a unit-0 topic;
- a From-before set after a keys block, or of fewer than two items;
- a Mixed review of fewer than four items, with fewer than two on earlier topics, with two items in a row
  sharing a topic, or after the Checkpoint;
- any of the three sections given twice;
- an item ID used twice anywhere.

`graph.py --selftest` (in `make controls`) plants the sections in a copy of poly-02. That copy must
pass, and so must a reordered one. Then it plants each fault in turn, and each must be refused for its
own reason.

**One judge.** tools/judge.c compares the learner's value with an expectation: `judge_expect("X=10",
"+10E+0")` is right, `judge_expect("X#2,1E-15", got)` is right when |got − 2| ≤ 10⁻¹⁵, computed
exactly. It reads decimal text only (no core), so the learning page compiles it as it does report.c,
and the page and the checker cannot judge differently. `make check` proves it agrees with the
firmware's vector runner (tools/judge_check.py): for every exact expectation in every lesson, in the
lesson's own mode and entry, the same value written in another form (the core's E-form, a trailing
zero) must pass both, and one unit off in the 34th digit must fail both; and its tolerance is checked
against exact arithmetic at, inside and past its edges. `make controls` builds three wrong judges (one
that calls every answer right, one with an exclusive edge, one that counts trailing zeros) and each
must turn that check red (scripts/judge-controls.sh).

## Placement

A placement check finds where a learner should start a course (Michael, decision 67: "Both by hand and
calculator where appropriate … give them the option for it on screen"; the result remembered in the
browser; docs/proposals/placement.md). Its items live in `placement/<course>/lesson.md`, front matter
`kind: placement` and `course: <id>`, with their answers in that folder's vectors.txt. They are items
as above, with one more field:

- `places: N`: answering it right is evidence the learner can start unit N. Every topic it names must
  be taught before unit N, in the course or a prerequisite course it names (graph.py refuses one
  taught in unit N or later).
- Every unit from 2 on that has lessons needs two items or more. Unit 1 is where a learner who passes
  nothing starts; unit 0, the calculator, is taught to everyone and is suggested with any result.
- `graph.py --json` gives each course's `placement` items and each unit's `gateway`: the topics its
  lessons require from before it.

**The page's rules** (primer builds them; nothing is sent anywhere):
1. Search the course's units 2 to the last, as a binary search: ask the items that place the middle
   unit of what is left.
2. Both right: the learner is ready for that unit, so search the later half. Either wrong or left
   blank: search the earlier half.
3. The result is the last unit whose items were both right, or unit 1 if none were. Show it as "start
   at unit N", with unit 0 suggested beside it, and with each missed item's topics linked to the
   sections that teach them.
4. The learner may start anywhere instead. The result is a suggestion, never a lock, and is kept only in
   the browser.

## Lore: who appears

The world's canon is in `lore/` (lore/WORLD.md: the world, its ages, the rules every story keeps;
lore/ENTITIES and lore/EDGES, one line each, shaped to import one to one into loreworks for its 3D
view). A lesson names who appears in it in its front matter, as comma lists (a name may have spaces):

- `cast: Maren`: characters the story leans on. Each one's home lesson (in lore/ENTITIES) is this
  lesson or among its prerequisites, taken transitively, so every route to the lesson meets them
  first. A character no lesson introduces (home `world`) cannot be cast.
- `walk-ons: Tobin`: parts that stand alone; a learner who has never met them loses nothing. That is
  the non-author read's to check, not graph.py's.
- An `event` in lore/ENTITIES is a plot point ("the mill wheel broke"), homed in the lesson that tells it. A lesson
  whose story leans on it lists it in `cast:`, so the same rule holds: every route meets the event first. Otherwise
  the story tells it again in a line.

**Where we are, on every door** (routes, ruled 2026-10-11, abacus #6967). A learner can enter a unit at its first
lesson, or, on an open route, at a side door: a lesson whose prerequisites leave out an earlier lesson of its unit.
graph.py refuses such a lesson with a story voice whose story opening (before its first `##`) names no lore place
or age (lore/WORLD.md rule 4), so a learner who starts there is never lost. `--json` marks each side door
(`side_door: true`) for the map. A plain lesson needs no such line. `graph.py --selftest` plants an event leaned on
before its home, a unit's first lesson and a side door that say nowhere, and accepts an event after its home and
the plain side doors.

**What the map reads** (Michael's route cards; abacus #7153, #7155, #7157). Each course file says its default mode,
`route | guided` or `route | open` (pre-algebra and geometry guided, algebra to calculus open; a path link can set
either). A door opens when what the lesson leans on is done:
- inside a unit, a lesson is done when its own items are right, every one of them (From before and Try it first
  included: retries are allowed and nothing records a first attempt, abacus #7180); a lesson with none
  (`no_items: true` in `--json`) is done when the last keys block in its file has been tried, which is its last
  exercise's check, present in every mode and entry the lesson offers;
- a unit is done when its checkpoint passes, every item right, retries allowed (`checkpoint` in `--json`: its
  lesson and item ids; graph.py refuses a checkpoint split across two lessons);
- a unit with no checkpoint (`closes_on: lessons`) is done when each of its lessons is: the standing rule for a
  course's unit 0, the calculator, and the interim rule for any other unit until its checkpoint is written. graph.py's
  summary line names every unit on the interim rule, so the gap stays in view;
- a unit with no lessons yet (`closes_on: unwritten`) is shown as coming: never done, never stamped, and it
  opens nothing beyond it;
- placement opens the units before the one it places.

The passport says only what was checked: a unit is stamped "passed" for its checkpoint, "lessons done" when it
closed on its lessons, and "placed" when placement opened it.

graph.py (in `make check`) refuses an unknown kind or verb, an edge end or appearance that is not an
entity, a home that is not a lesson, and a cast character not met on every route. `--json` gives the
lore, each lesson's appearances, and every cameo (a character outside their home course) with the
home lesson the page links back to. Every name in lore/ is a stand-in until Michael rules on who
designs the world.

## Drawing tools

A lesson that introduces a drawing tool names it in its front matter, as a space list:
`tools: point straightedge ruler protractor`. The site adds each tool to the learner's drawing bar
from that lesson on and never takes it away (stu32-primer's docs/proposals/2026-10-09-geometry-drawing.md).
The tools are point, straightedge, compass, ruler and protractor (graph.py's TOOLS).

A lesson that introduces no tool has no `tools:` line. graph.py (in `make check`) refuses a name not in
the list, a tool named twice in one lesson, an empty line, and a tool named by two lessons: only the
lesson that introduces a tool names it. `--json` gives each tool's lesson, and each lesson's tools.
The line is site metadata, not content for the accuracy read, so changing it does not hold an
accepted lesson (abacus #6101).

## What `make check` proves

For each lesson, in each mode it offers (and each entry, for a lesson that offers entries: every
step below runs once per mode and entry), on that mode's view of it (its blocks, spans and quotes):

1. The mode's vectors pass on the firmware's runner, each from a fresh core and from a used one
   (the stack full, LAST x set, RAD), so no example leans on an empty stack.
2. `fmt-vectors.txt` passes on the firmware's display runner.
3. Every keys block, after the setup, is pressed on the device's own key layer (`firmware/app.c`
   through `app_key`, as the device, tally's app and the panels press theirs) by `tools/keyrun`,
   after the setup with the mode filled in. Each name is resolved to a key
   from the firmware's keymap (`km_lookup`, the menus, the letter layer), never from a table of
   ours; a soft-key label that is also a printed legend is refused as ambiguous. Every op that
   reaches the core is logged on both paths (`tools/trace.c`, a linker wrap of `ab_do_arg`), and
   the two logs must be the same ops with the same arguments in the same order. The vector's ops
   are then replayed on a fresh core and its state image must equal the one the keys left. The
   keys must leave the device at rest: no shift armed, no menu or prompt open, no device setting
   changed. Every vector of the mode is shown by a block of the mode's view, and only the first key
   of a vector sets the mode.
4. Every quoted display sits under its own example (after its block, before the next), is the
   text the device's screen shows on its X line after those keys (`screen_lines`; a value, not a
   number being typed or a message), and is its display vector's text, at the setting the vectors
   set and with the device's default options, of the vector's exact X result (N, ANS, on the
   algebraic line).
5. A student working through in the mode: the setup once, then every block of the mode's view in
   order on one device, with nothing reset between them (a continuation presses only its own keys;
   `student_sequence(lesson, mode, entry)` in tools/check.py assembles them, and the learning page's
   gate calls it; with no entry, a lesson that offers entries is worked in its default). It found, the first time it ran in 35s and STU, that a key pressed over a message only
   clears it there, so a lesson clears each message with C before the next example. After each block, every
   exact X, Y, Z and T in its vector must hold, and every quoted display and status annunciator must
   be what that student sees. Checks 1-4 judge each example from the setup; this one catches what
   an example inherits from the one before it: a display setting, Fraction display, a number still
   being typed. (It found five such breaks in four lessons the first time it ran, three of them
   already accepted.)
6. In Fraction display, a display vector's trailing indicator (` v` below, ` ^` above) must match
   the device's status band arrow (▼, ▲), and an exact fraction must show no arrow.
7. No em-dash in lesson.md, as a character or an HTML entity, front matter included. A fence that
   looks like a keys block but is not in the checked form, or a `<disp` tag not in the checked
   form, fails.

So a lesson that prints "GOLD 7" where its vector does something else fails, and so does one whose
keys no longer do what it says when the layout or the keymap changes (the layout is not ruled yet).

## Controls

`make controls` plants one fault at a time in a copy of rpn-01 (and, for what only rpn-02 has, of rpn-02) and requires `make check` to
fail for that fault's own reason; every lesson has its own set (tools/controls.py lists them, with the harmless changes that must stay
green). A fault that does not apply to the file, or applies more than once, is reported as an error, not counted as a pass.
`make controls` runs every folder in lessons/ and placement/, and a folder with no set fails it, so a new lesson cannot be left
out (until 2026-10-09 the Makefile named each lesson, and the first three geometry lessons were missed until their count was read).

## What it does not prove yet

- Keys written in inline code are not seen; only fenced keys blocks are checked. A number written
  in the prose in the display's FIX form (12.0000 at FIX 4) outside a `<disp>` tag fails, but any
  other wording of what the screen shows ("X holds 12") is checked only by the vectors behind it.
- On the algebraic line, the student run (check 5) sees the result only as the screen shows it: the
  exact X, Y, Z and T it compares are the stack, which ALG leaves alone, and keyrun does not report
  ANS. The exact result (N=) is checked by the vectors, from the setup, and the quoted displays
  carry it through the student's order.
- The words around an example are not checked against it. A machine check cannot tell that an
  explanation of correct keys is wrong; the non-author read exists for that (rpn-01's first draft
  said each x used a copy T dropped, and none did).
- Two device paths that skip the core are logged as the op the core would have received, and the
  state image confirms each: a key taken by the VIEW rule (ab_view_key), and a key pressed over a
  35s message (the app clears it with no op).
- Core entry points other than `ab_do_arg`, `ab_memory_clear` and `ab_eqn_add` (UNDO's state
  load, VIEW, an interrupt) are not traced; only the state image sees what they change, and fields
  the image leaves out (overflow, the device's slice and budget) are not compared.
- The screen's X line is compared as whole text; how the LS027 fits a long line (its scale and its
  window around the cursor) is not.
- Some correct keys are refused (false reds, not false passes): a shifted key with no legend in
  that shift, Equation mode's soft keys, CLR ALL?'s yes, and CONST's later pages.
- Maths spans: check.py proves each one reads back over its closed list, not that KaTeX renders it; the page's
  render with throwOnError is that check (primer). TeX drops the space after a command, so an author's `3 \times
  4` reads as "3 ×4": the numbers read the same.
- Pedagogy and voice: those are read by someone who did not write the lesson, and are Michael's.

## Courses

A course is a file `courses/<id>.course` (decision 63: courses a learner takes, not one long list), lines
`kind | fields` with `#` comments:

```
course | algebra-to-calculus | Algebra to Calculus
entry | rpn
unit | 0 | The calculator
lesson | rpn-01
```

- `course | id | title`: the id is the file's name.
- `entry | rpn alg`: the entries the course offers, its default first (decision 63: young learners' courses
  default to algebraic, with RPN offered). A lesson that offers only RPN stays RPN.
- `prerequisite | course-id` (any number, before the units): a course a learner is expected to have
  done first. None of the three courses names one yet.
- `unit | n | title`, then its `lesson | id` lines in order. A unit may have no lessons yet; the page
  shows it as in preparation, and shows only lessons on lessons/ACCEPTED.
- `tools/graph.py` (in `make check`) refuses a malformed line, an unknown or repeated lesson, an unknown
  prerequisite, a lesson in no course, and a lesson requiring a topic that is taught later in the same
  course, by a lesson in no course, or by a lesson neither earlier in this course nor in one of its
  prerequisites (taken transitively). A learner who starts a course must meet each topic before it,
  in that course or one it names (abacus #5112: frac-01 leaned on the algebra course's RPN start until
  pre-algebra had its own, start-01). The same idea taught in two courses is two topics, one each.
  `--json` prints the courses, prerequisites included, beside the topics and lessons; `make controls`
  plants seven course faults and checks that a named prerequisite is accepted.
