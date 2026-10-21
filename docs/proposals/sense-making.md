# Drawing the problem: bar models and sense-making (PROPOSAL, for primer and abacus)

**Status:** proposal by tutor, 2026-10-21, at Michael's ask. Sections 5 and 6 are built (c51c51d), waiting on abacus's read; sections 1 to 4 are not built. Sections 1 to 4 are for the
word-problems course (primer's blueprint, stu32-primer branch word-problems,
docs/proposals/2026-10-14-word-problems.md) and wait on its card. Sections 5 and 6 are two additions to
pre-algebra lessons that abacus has accepted, so they would go to abacus as one batch.

**The ask.** Michael, 2026-10-21, on a short from Greg Tang's channel, Tang Math Games: "Can you review that channel?
He has a fun way of teaching." After the review: "Yes write it up!"

**The binding question:** which of Tang's methods would make our lessons easier to follow, in a form our checks
can hold, without copying any of his problems?

## What was read and seen

- **The channel:** 230 shorts and 27 longer videos, listed with yt-dlp on 2026-10-21. The longer videos are teacher
  workshops of about an hour, a TEDx talk ("Greg Tang - Math Makes Sense!") and how-tos for his games. The shorts
  are mostly clips from the workshops.
- **Transcripts read:** 17, saved in the workspace under yt/tang-math-games/: the TEDx talk, a nine-minute workshop
  excerpt on word problems (ulM1-AoZd6o), and 15 shorts chosen for fractions, equations, percent and word problems.
  One short had no subtitles.
- **Frames looked at:** 32, from 8 of those videos.

**The rule for using it.** The README's fresh-only rule applies: we take his methods and none of his problems,
figures or wording. Every example below is new and was checked with SymPy. Short quotes are his, marked with the
video and the second.

## What makes his teaching work

- **He asks rather than tells.** Nearly every line is a question the room answers, and our `ask:` prompts are the
  same idea in a lesson.
- **He does it the bad way first.** He grinds through the procedure and then shows the sensible way. lin-01's
  productive-failure trial (docs/proposals/productive-failure-trial.md) is our version, built and judged by reading.
- **He reads twice:** "the first time we read it, it's always for context" (ulM1-AoZd6o, 0:20), and the details
  come on the second read.
- **He refuses keywords and circled numbers.** Circling a number "pulls the number out of context" (ulM1-AoZd6o,
  1:18). The equation judge's `needs:` rule is built the same way, reading the story's numbers with their words.

The four methods below are the parts we can turn into lesson formats.

## 1. Bar models for word problems

**Seen on screen** (0Wsdt6M9CGw at 0:30 to 1:14; ulM1-AoZd6o at 5:00 to 9:00; the TEDx talk at 4:10). Every bar
model of his uses the same few marks:
- a vertical starting line, with the names of the things compared to its left;
- equal units, so the length of a bar is how many units it holds;
- a change (a gift, a purchase) drawn as a dashed unit, "just so it looks different" (0Wsdt6M9CGw, 1:04);
- braces, under the parts and over the whole, labelled with a number or "?".

That's a small, fixed set, so the page can draw one from a few lines in the problem block. It needn't be a
hand-drawn picture, which section 6 of the blueprint rules out anyway.

**The format, a sketch.** An example of ours:

> Maren has 3 times as many rolls as Tobin. She gives Tobin 10 rolls, and now they have the same number. How many
> rolls did Maren have at first?

````
```bar W12
row: Maren | 3u
row: Tobin | u
change: Maren | -10
change: Tobin | +10
equal: Maren, Tobin
ask: Maren | before
```
````

The page draws Maren's bar as 3 units and Tobin's as 1. On tap, 10 comes off Maren's bar and 10 is added dashed to
Tobin's, and the two ends line up. That's the one place the picture moves, under Michael's ruling of motion only
where things change, on tap (abacus #8295).

**The check: the bar model is a set of equations, so it is checked like one.** Each row is a length in units, each
change adds or takes away, and `equal:` says two lengths match: 3u − 10 = u + 10. check.py solves that system
(u = 10, so Maren had 30) and compares it with the problem's answer, so a bar that doesn't fit its story fails.
The drawing itself is checked under blueprint section 6's rules: generated from the numbers, given a text
alternative ("Maren's bar is 3 units, Tobin's is 1; after the change they are equal at 20"), and read back from the
SVG by a separate script. Its controls are:
- one unit drawn a different width;
- a change put on the wrong bar;
- `equal:` naming two bars that don't end level.

Each must fail.

**Where it goes.**
- In the six rows, a bar model is the picture of **Need**. It is shown in worked examples, offered on a tap, and
  shown after a miss on Need, rather than added as a seventh row.
- **Units 2 to 5** are where it earns most: compare problems, parts of a whole, before-and-after problems, and
  fractions of an unknown (2 parts of 5 are 18, so the whole is 45).
- From unit 5 on, the letters carry it and the bar becomes optional.

**The size, measured by primer** (#9440, a throwaway prototype, nothing committed):
- the bar module is 3,647 B raw and 1,548 B gzipped; it parses the block, solves u from `equal:`, draws the SVG with
  the change in its own group for the tap, and writes the text alternative;
- with the chart it's 2,229 B gzipped, and with the 3D solids too it's 3,475 B, all under section 6's 10 KB;
- one drawing of W12 is 902 B of SVG;
- the check reads only the SVG and takes u from the stated answer, not from `equal:`, so it's shaped apart from
  the drawer;
- the three controls above, and a wrong number in the text alternative, each failed on their own check.

It hasn't been seen rendered or tried on a phone yet.

## 2. The clause a number came from

**Seen on screen** (0Wsdt6M9CGw; ulM1-AoZd6o at 5:00 to 9:00). He underlines a whole clause just before he draws
it, never a keyword or a lone number, so the number stays with the words that give it its meaning.

**The format:** each `given:` names the clause it comes from:

```
given: rolls given = 10 | rolls @ "She gives Tobin 10 rolls"
```

**The check:** check.py refuses a clause that isn't in `text:` word for word, or that doesn't contain the value,
as digits or a number word ("twice", "a dozen"). That's the same reader as the `needs:` rule.

**The page:** when a Given row is judged or revealed, its clause is highlighted in the problem's text. The
learner sees where each number came from, and a wrong given can be answered by showing the clause it should have
come from.

## 3. "Compared to what?"

In his workshop, "compared to what" is "the whole key" (SC_MZphz4h0, 1:08). Percent change goes wrong when the
learner takes the wrong whole: the new price instead of the old. Fraction problems go wrong when the whole changes
partway through.

**The format:** a percent or fraction given names its whole:

```
given: discount = 20% | of the price before
```

check.py refuses a percent or fraction given without `of`.

**The slip:** the wrong whole. Here's an example of ours: a price after 20% off is 36. The old price was 45, and
taking 20% of the 36 instead is the slip. That slip is a vector like any other.

**Where:** unit 4's percent lesson, and every later unit that carries a percent.

## 4. Wording: comparisons that point the wrong way

Two of his points, both about words that mislead:

- **"Times more" and "times as many" differ.** In 15 against 5, 15 is three times as many, but "two times more"
  counts only the difference of 10 (nEzbzTfmJeo). Our lessons say neither today: a grep for "times more" in
  lessons/ finds 0. A check.py line that refuses "times more" in a lesson's prose would keep it that way.
- **Some compare problems are harder because the word points the wrong way:** "fewer" or "less", where the answer
  is found by adding (Tw-LFUwkZOg, eC_ddPX6Ifk). The blueprint's unit 2 already gives compare problems their own
  lesson. Within it, problems whose word matches the operation come first, and the reversed ones get their own
  section after, with that as the hint.

## 5. pre-algebra expr-02: cover the part you don't like

**Seen on screen** (the TEDx talk at 10:20; -Xq3w5YHpyk). He sets the step-by-step solution, headed "Traditional",
beside a "Common sense" column. In that column the same equation carries braces: one under the part being covered
gives its value, and the next brace is drawn inside it.

**The method:** expr-02 teaches solving by undoing the steps in reverse order (socks and shoes). Covering up is a
second way to see the same equation, using the lesson's own example, 3n + 5 = 20:
- cover the 3n: something plus 5 is 20, so the something is 15;
- 3 times n is 15, so n is 5.

A deeper one: 3(n + 2) − 5 = 25. The covered part, 3(n + 2), is 30, so n + 2 is 10 and n is 8.

**A section after "Another order of steps"**, with a twin, and the calculator checking each covered value as the
lesson's blocks do now.

**Its limit, said in the lesson:** covering works when the unknown appears once. With n on both sides, the
undoing steps (or algebra later) do the work. The ratio problem in zKougXjUcng is Tang switching for exactly that
reason.

**The braces are a picture,** generated from the equation and checked like section 1's.

## 6. pre-algebra whole-02: dividing in parts

whole-02 already has "Multiplying in parts". Its division section goes from remainders straight to long division,
and the parts method is missing.

**The method:** 117 ÷ 9, with 9 rolls to a box, as in the lesson:
- break 117 into 90 and 27, two parts 9 divides;
- 90 ÷ 9 is 10, and 27 ÷ 9 is 3, so 117 ÷ 9 is 13.

Tang's division short (ZHajGeLjLPI) makes the same move with a split mark under the number.

**A second move:** halve both numbers, as a fraction is simplified (frac-01's "A fraction is a division"). 156 ÷ 12
is 78 ÷ 6, which is 39 ÷ 3, which is 13. Tang's EvGgH44yGK4 makes the point that division can be simplified
like a fraction.

**In the lesson:** a short section before "Long division", with a twin. Long division stays as the method for
when no friendly split shows.

## What this does not take

- **Any of his problems, drawings or slides.** His shells, apples and ratio problems are his.
- **His "ten four" naming idea** (QpyLUyRzn8k): renaming numbers is outside what a lesson here can change.
- **His claim that most textbooks ignore the order of problem types.** That's his view, not a measurement, so
  section 4 rests on the blueprint's own unit order, not on it.

## Who does what, and in what order

| part | owner | waits on |
|---|---|---|
| 1. bar block and its check | tutor: format and check.py; primer: the drawing, its check and a size prototype | the word-problems card |
| 2. clause-highlighting | tutor: format and check.py; primer: the highlight | the card |
| 3. a whole for each percent given | tutor | the card |
| 4. the "times more" check; reversed compare problems in their own section | tutor | the card (the check.py line could land any time) |
| 5. expr-02's cover-up section | tutor | abacus: re-acceptance of expr-02 |
| 6. whole-02's dividing in parts | tutor | abacus: re-acceptance of whole-02 |

Sections 5 and 6 change accepted lessons, so `tools/accepted.py` will hold both back until abacus reads them again.

**Questions for abacus and primer:**
- Do sections 5 and 6 go now as one pre-algebra batch, or wait until pre-algebra's next unit?
- Is a bar model the picture of Need, as proposed, or a seventh row the learner draws? Drawing one needs drag
  controls and a way to judge a drawing. That would be a larger build, worth a prototype only if Michael wants
  learners to draw.
