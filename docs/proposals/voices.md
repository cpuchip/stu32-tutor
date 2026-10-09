# Two voices: story and plain (PROPOSAL, for Michael)

**Status:** a proposal (decision 67's question, relayed by abacus #5320). Nothing is built until he
rules.

**His words** (decision 67): "Should we support two ways to learn, straight no story just math and
applications? And then story for those that learn better that way? Same content and problems, just no
fluff?"

## The proposal: voice as a third axis, beside mode and entry

A lesson already varies by mode (33s, 35s, STU) and by entry (RPN, algebraic) without changing what it
teaches. Voice would be one more such axis, and the narrowest of the three, because it changes only
the prose around the examples:

- **Front matter:** `voices: story plain` (the default first). A lesson with no `voices:` has one
  voice, as every lesson has today.
- **Prose spans:** text that belongs to one voice goes in `<voice v="story">…</voice>` or
  `<voice v="plain">…</voice>`. Everything outside the spans is shared.
  - The story voice carries Thornwick and its people (lore/WORLD.md).
  - The plain voice carries the same problem as a bare statement: "Two pies of the same size are cut
    into 4 and 2 equal pieces; 2 of the 4 and 1 of the 2 are taken. Which is more?"
- **What may not differ:** the keys blocks, the vectors, the quoted displays, the exercises' numbers
  and the items. The problems are the same problems in both voices. Only the words that set them up
  differ.
- **check.py proves that.** For each lesson that offers voices, it builds each voice's reading and
  requires that every reading have:
  - the same keys blocks, with the same IDs and the same keys, in the same order;
  - the same quotes;
  - the same items.

  A keys block, a `<disp>` or an item inside a voice span is refused. The planted controls are a keys
  block in one voice only, a number changed in one voice's prose quote, and an item in one voice only.
- **The page** shows the voice the learner chose and remembers it in the browser, as it does the mode
  and the entry.

## What it costs

- **Each lesson with a story is written twice** around the same skeleton: the shared examples, then
  two framings. In practice the plain voice is mostly the story voice with the names taken out, and
  shorter.
- **The non-author read reads both,** since a plain sentence can drop a step the story carried.
- **Cast and walk-ons (lore/) belong to the story voice.** graph.py checks them as now, and the plain
  voice names no one.
- **The algebra course has almost no story,** so it needs no voices. The axis matters most for
  pre-algebra and geometry, which are written now, so the cost is paid as those courses are written,
  not as a rewrite.

## The other way, and why not

The alternative is two lessons, one per voice, linked as a pair. That doubles the vectors, the
checks, the accepts and the graph's topics, and the two could drift apart in what they teach without
anything noticing. One lesson with two voices keeps one set of examples, one accept, and a check that
the voices cannot drift.

## For him to choose

1. **Two voices as an axis of one lesson** (recommended), or two lessons per idea, or story only.
2. **The default voice** for the young courses: story (recommended, as his direction for the courses
   has been) or plain.
3. **The algebra course stays one voice,** plain with light examples, as it is (recommended).
