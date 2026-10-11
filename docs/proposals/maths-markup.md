# Maths markup in lesson.md, for KaTeX (PROPOSAL, with primer)

**Status:** proposal, to agree with primer (#6727) before either of us builds. Michael asked for it on his phone:
"we definitely need pretty print for all of the equations." The page renders with KaTeX (MIT, vendored), and
lesson.md says where the maths is. Until we agree, fixtures stand in, as with voices and whys.

The lessons write maths in Unicode, as `d(t) = 2t²`, `√x`, `x − 2 ≥ 0` and `1/4`. In the prose a learner reads
(default voice, outside every fence and `<disp>` quote), **683 paragraphs** hold an equation, power, root,
function notation, operator, fraction or inequality, and so do **565** item and why fields. No lesson.md has a
`$` today.

## 1. The markup

- **Inline:** `$…$`. A span opens at a `$` and closes at the next `$` on the same line. It may not be empty, start
  or end with a space, or cross a line break. The lessons are hard-wrapped, and a span that may not wrap is a rule
  both readers can match exactly. A `$` that is not maths is written `\$` (none today); both readers take that
  before markdown-it, which would otherwise eat the backslash.
- **Display:** a ```` ```math ```` fence, one equation per fence.
- **Where it may go:** prose, an item's `prompt:` and slip hints, and a why block's `ask:` and `because:`. It may
  not go in a heading (headings are topic anchors in lessons/TOPICS), a keys block, a `<disp>` quote or a tag's
  attribute.
- **It may not cross a voice tag.** We agree on this. A span lies wholly inside one `<voice>` span or wholly
  outside them all.
- **Key names stay out of maths** (your question 1). The author writes the maths in `$…$` and a key's name plain,
  as in "the x² key", therefore the markup itself keeps them apart. check.py also refuses a span followed directly
  by "key", as a cheap guard: 12 places today write a key name that looks like maths before the word "key".

## 2. What goes inside a span: one question to settle first

Two ways are open, and which is better depends on what KaTeX does with the Unicode the lessons already use. That
is the riskiest unknown here, and a few minutes with the vendored copy answers it.

1. **Keep the Unicode:** `$d(t) = 2t²$`. The conversion only adds the `$` marks, and the numbers read exactly as
   now. It works only if KaTeX, with `throwOnError` on and in strict mode, renders ², ⁻¹, √, ×, ÷, − and ≤ as maths.
2. **Write TeX:** `$d(t) = 2t^2$`, `\sqrt{x}`, `\frac{1}{4}`. KaTeX's own input, rendered at its best, but both
   readers then need one function, `maths_text(tex)`, that gives back the plain text: `^2` → ², `\frac{1}{4}` →
   1/4, `\sqrt{x}` → √x, `\times` → ×, `-` → −, over a closed list of commands. A command not on the list is
   refused. That is the TeX check you said check.py might do: a whitelist, not KaTeX's own check.

**My recommendation is 2, if 1 renders badly anywhere,** and 1 otherwise, since it changes nothing a check reads.
Could you try ², ⁻¹, √x, √(x + 1), ×, ÷, −, ≤, ≥ and ′ in your copy, strict and with throwOnError, and send what
renders?

## 3. Numbers inside maths (your question 3)

They count, and they count as they do today, for the why rule (check_why's `seen()`) and the voices rule
(`prose_numbers`) alike: both read a span through the same reading (as written in option 1, `maths_text` in
option 2). 1/4 names 1 and 4. A superscript is not a numeral, as now: `\d` does not match ², so `2t²` names only
2, checked in Python.

**Two hazards in `seen()` to fix before maths arrives:**
- it strips `<…>` as a tag, so in "$x < 2$ … >" it would eat the text between;
- it drops `\b[a-z]+-\d{2}\b` as a lesson id, which "$x-10$" matches.

Maths spans are therefore lifted out first and read through the one reading, and only then are tags and ids
stripped.

**Controls** (in controls.py, as for whys):
- a why number shown only inside an example's maths: green;
- a why number not in the maths: refused;
- voices whose maths differ in a number: refused;
- the same maths in both voices: green;
- a span across a voice tag, across a line, in a heading, in a keys block, or (option 2) with an unknown command:
  refused, one control each;
- "$x < 2$" and "$x-10$" read whole: green.

## 4. Converting the lessons, and the check on it

683 paragraphs and 565 fields are too many to convert by hand and trust. A script converts them, and a round
trip checks it: for every lesson, the text with each span replaced by its reading must equal today's text byte for
byte. So every check.py and graph.py result stays the same, every voice reads the same numbers, and only the
markup changes. Then your page renders every span with `throwOnError`, and a planted bad span is the red control
(your question 4). The two checks are differently shaped: the round trip proves nothing a check reads has changed,
and the render proves the TeX is valid.

You add `maths` as a question in tools/tutor_lesson.py: each span's start, end and text, per lesson. check.py's
reader answers the same question, gated byte for byte, as with keys, voices and whys.

## 5. What counts as maths: Michael's call

"All of the equations" leaves one boundary open, the arithmetic in running prose: "360 − 60 = 300°", "3 × 4
pairs", "By hand, 7 + 5 = 12".
1. **Everything:** every equation, and every expression with a letter, power, root, fraction or operator, goes in
   `$…$`. A page then never mixes typeset and plain maths. This is my recommendation.
2. **Algebra only:** letters, powers, roots, fractions and function notation. Plain arithmetic stays as text. That
   means fewer spans, but a page would show x = 6 typeset beside 7 × 12 = 84 plain.

The conversion touches the same prose as the voice pass (docs/proposals/voice-pass.md). Since it is done by a
script with its own exact check, it can run before or after a course's voice pass, but not in the middle of one.
