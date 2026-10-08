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
  `tools/accepted.py` (a lesson changed since abacus last saw it is held back).
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
