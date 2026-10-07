# Proposal: one lesson, three modes (decision 56)

**Status:** APPROVED by abacus (#4527, 2026-10-07), with Michael's rulings: a first visit opens in STU,
and every lesson offers STU from day one. Being built into the checker.

Michael (decision 56): "33s mode should act as close to a 33s as possible … for the lessons you can
pick the mode on the page and it'll show you how to do it in that mode, much like the programming
language switch box for apis like go, python, typescript".

So a lesson is written once and read in the mode the student picks: 33s, 35s or STU. Where the keys
are the same in every mode, the lesson prints them once. Where they differ, it carries one variant
per mode, and the checker presses each variant in its own mode on the device's key layer. The
current rule, printed 33s keys pressed again in 35s mode with `33s` swapped for `35s`, is retired,
and so is the planned auto-ENTER for 036b: a 35s variant shows its ENTER.

## 1. Front matter: the modes a lesson offers

```
modes: 33s 35s STU
default: 33s
setup: BLUE MODE {mode} GOLD DISP FIX 4
```

- `modes` lists what the page's switch offers (default: all three). A lesson that cannot be done in
  a mode leaves it out and says why in `modes_reason:` (poly-04's 33s until unit 039; a lesson about
  TABLE, which is STU only).
- The page opens in: the link's ?mode= if offered, else the reader's remembered choice if offered,
  else STU (Michael, decision 56), else `default:`, else the first of `modes` (primer #4536). So
  `default:` is needed only by a lesson that does not offer STU, and `modes` defaults to all three
  (abacus #4527).
- `setup` may use `{mode}` for the mode's own soft key (`33s`, `35s`, `STU`); the setup block prints
  it the same way, and the page fills it in.

## 2. Keys blocks: one shared, or one per mode

A block with no `mode=` is shared: its keys are printed for every mode and must pass in every mode
the lesson offers. Where a mode needs other keys, a variant block follows it at once, with the same
ID:

````
```keys S03 after=S02
XEQ F
```
```keys S03 mode=35s,STU
XEQ F ENTER
```
````

- The variant replaces the shared block in the modes it names; the shared block stays for the rest.
  A block may also have only variants (no shared block), one per offered mode.
- `after=` on the shared block holds for its variants unless a variant gives its own. A mode's
  chain can differ: an STU-only block (variants for STU alone) sits in STU's chain only, so the
  next block's 33s and 35s variants name the block before it in their own chain (primer #4513).
- Mode names are the MODE menu's labels: `33s`, `35s`, `STU`, everywhere (blocks, spans, quotes).
- The page shows the block for the mode chosen; the checker presses, in each offered mode, the
  setup for that mode and then that mode's block.

## 3. Vectors: shared unless a mode differs

- A vector keeps its one ID and starts `MODE33` as now. In each offered mode the checker runs it
  with the first token made that mode (`MODE35`, `STU`): the maths is the core's, not the keys', so
  the same ops serve every mode unless a mode's maths differs.
- Where it does (STU's implied multiplication and right-to-left powers, decision 53; a 35s-only
  display), a per-mode vector carries the ID with the mode after an `@`: `S03@STU | … | STU FIX4 … |
  …`. It replaces the shared vector in that mode.
- A key variant whose ops differ from the shared vector is caught by the key/vector comparison (the
  printed keys issue other ops), so a needed per-mode vector cannot be forgotten silently.

## 4. Displays and prose

- A `<disp>` with no `mode` holds in every offered mode and is checked in each.
- `<disp v="S03" m="35s">…</disp>` holds in that mode only, and stands beside its siblings for
  the other modes. The page shows the one for the chosen mode.
- Prose that differs by mode goes in `<mode m="35s,STU">…</mode>` spans, inline or around whole
  paragraphs (primer's form: a renderer shows one mode without parsing grammar). A `<disp>` inside a
  span inherits the span's modes.
- Display vectors (`fmt-vectors.txt`) stay shared: they test the formatter, which every mode shares.

## 5. The checker

For each offered mode: the vectors (shared, with the mode token set, or the mode's own), the keys
(that mode's block, after that mode's setup), the quotes in that mode, and the student run in order
with that mode's setup and blocks. A failure names the mode. The student run's assembly becomes an
importable function, `student_sequence(lesson, mode)` returning the "ID<TAB>keys" text, so primer's
gate calls the checker's own assembly instead of mirroring it (primer #4513). The controls gain one per new rule:
a variant that is wrong in its own mode, a shared block that fails in one mode (the variant missing),
a mode-only quote checked in the wrong mode, and a `<mode>` span with a bad mode name.

## 6. Migration

The 20 accepted lessons have 33s keys checked in 33s and (translated) 35s. On the change, each runs
in all three modes with its keys as printed; every failure is a place a variant is needed. I would
report those places to abacus before writing any, since each is a fact about how the modes differ.
fn-02's TABLE section, which today switches into STU mid-lesson, becomes an STU-only section
(`<mode m="STU">`) in a lesson that offers all three; its GRAPH section waits for this format.

## Open questions

1. Should `modes` default to all three, or to 33s alone until a lesson is migrated?
2. Is `@` for the per-mode vector ID safe in the firmware's runner (an ID is any text before the
   first `|`)?
3. primer asked for variants keyed by block ID and mode beside the shared block (#4513), as here.
