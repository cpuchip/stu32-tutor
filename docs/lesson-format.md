# Lesson format

A lesson is a folder `lessons/<id>/` with three files. The examples exist as vectors before any
prose is written around them, and `make check` (on fermion: `scripts/check-docker.sh`) runs every
one of them on the STU-32's own core at `CORE_PIN`.

## vectors.txt: the maths

The firmware's key-vector format (`abacus-firmware/tests/vectors.c`): `ID | note | keys |
expectations`, one example per line. Rules (abacus, 2026-10-06):

- Every vector's keys begin `MODE33` and a display setting (`FIX4`, `SCI2`, `ALL`...), so nothing
  depends on how the core started (`ab_init` gives ALL, MEMORY CLEAR gives FIX 4).
- Every vector passes in 33s mode as written and again with `MODE33` changed to `MODE35`. A lesson
  that is about a difference between the modes says so in its front matter (`modes: 33` and a
  `modes_reason:`); the differences are abacus decisions 22, 45 and 46.
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
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---
```

- `setup` is the keys the student presses once; the checker presses them before every example.
  The lesson prints them in a ```` ```keys setup ```` block, which must match.
- Each example is a ```` ```keys Snn ```` block: the keys the student presses, by the legends
  printed on the STU-32 (abacus `layout/stu32-v0.json`). A shifted function is `GOLD` or `BLUE` and
  then the legend printed in that colour (`GOLD LASTx`, never `LASTx` alone). A number is its
  digits (`1.05`). A soft key is the label its menu shows (`FIX`, `33s`). A variable is its letter
  (`STO A`).
- A block that carries on from the one just before it is ```` ```keys Snn after=Smm ````, and holds
  only the keys pressed next. Its vector holds the full sequence (Smm's keys, then these). Use it
  wherever the text says "now press", and always after a stopping point: a stopping point leaves a
  number half typed, and a fresh example after it would type into that number.
- A quoted display is `<disp v="Snn">text</disp>`. An annunciator in the status band (the fraction
  indicator ▼ or ▲, RAD) is `<disp v="Snn" kind="status">▼</disp>`. A screen line that is not a value (a VIEW's
  `B=49.75`) is `<disp v="Snn" kind="view">text</disp>`, checked against the device's X line
  (text and kind) since no display vector covers it. The kinds are view, prompt, message and entry
  (a number still being typed shows with its cursor: 7_). A quoted value's display vector may carry
  `w=21`, the device's X-line width (firmware/screen.c FMT_WIDTH); the runner's default of 22
  agrees with the device only for short values.
- No em-dashes (the house voice, external-voice skill). No child is ever named.

## What `make check` proves

For each lesson:

1. `vectors.txt` passes on the firmware's runner in 33s and 35s modes, each from a fresh core and
   from a used one (the stack full, LAST x set, RAD), so no example leans on an empty stack.
2. `fmt-vectors.txt` passes on the firmware's display runner.
3. Every keys block, after the setup, is pressed on the device's own key layer (`firmware/app.c`
   through `app_key`, as the device, tally's app and the panels press theirs) by `tools/keyrun`,
   in 33s mode and again with the setup's 33s soft key made 35s. Each name is resolved to a key
   from the firmware's keymap (`km_lookup`, the menus, the letter layer), never from a table of
   ours; a soft-key label that is also a printed legend is refused as ambiguous. Every op that
   reaches the core is logged on both paths (`tools/trace.c`, a linker wrap of `ab_do_arg`), and
   the two logs must be the same ops with the same arguments in the same order. The vector's ops
   are then replayed on a fresh core and its state image must equal the one the keys left. The
   keys must leave the device at rest: no shift armed, no menu or prompt open, no device setting
   changed. Every vector is shown by a block, and only the first key of a vector sets the mode.
4. Every quoted display sits under its own example (after its block, before the next), is the
   text the device's screen shows on its X line after those keys (`screen_lines`; a value, not a
   number being typed or a message), and is its display vector's text, at the setting the vectors
   set and with the device's default options, of the vector's exact X result.
5. A student working through: the setup once, then every block in lesson order on one device, with
   nothing reset between them (a continuation presses only its own keys). After each block, every
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
fail for that fault's own reason (30 controls, and 3 harmless changes that must stay green: tools/controls.py lists them). A fault that does
not apply to the file is reported as an error, not counted as a pass.

## What it does not prove yet

- Keys written in inline code are not seen; only fenced keys blocks are checked. A number written
  in the prose in the display's FIX form (12.0000 at FIX 4) outside a `<disp>` tag fails, but any
  other wording of what the screen shows ("X holds 12") is checked only by the vectors behind it.
- The words around an example are not checked against it. A machine check cannot tell that an
  explanation of correct keys is wrong; the non-author read exists for that (rpn-01's first draft
  said each x used a copy T dropped, and none did).
- Core entry points other than `ab_do_arg`, `ab_memory_clear` and `ab_eqn_add` (UNDO's state
  load, VIEW, an interrupt) are not traced; only the state image sees what they change, and fields
  the image leaves out (overflow, the device's slice and budget) are not compared.
- The screen's X line is compared as whole text; how the LS027 fits a long line (its scale and its
  window around the cursor) is not.
- Some correct keys are refused (false reds, not false passes): a shifted key with no legend in
  that shift, Equation mode's soft keys, CLR ALL?'s yes, and CONST's later pages.
- Pedagogy and voice: those are read by someone who did not write the lesson, and are Michael's.
