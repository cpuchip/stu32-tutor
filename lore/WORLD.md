# The world (the lore bible)

**Status:** pre-algebra first (decision 67: "files in the lessons repo, loreworks as a view,
pre-algebra first"). Shape B, ruled 2026-10-08: one shared world, a new cast for each course, cameos
that link back to where each character lives (docs/proposals/story-world.md). **Every name here is a
stand-in.** Whether Michael's children design the world (its names, its places, its cast) is his
open question; if they do, their design is the spec and replaces these.

Nothing here is taken from the algebra book Michael named as inspiration: no ruler being taught, no
court of advisors, no kingdom bringing problems to a throne. Every character is invented, and none is
about any real person.

## The world

One land, seen across four ages. Each age builds on what the one before it worked out, so a course's
story sits in its age, and the next course's people live with what this course's people made.

| Age | Course | What the people of the age are working out |
|---|---|---|
| The market age | Pre-algebra | Trade, recipes, shares, a harvest that has to last the winter |
| The survey age | Geometry | Maps, a bridge over the river, a lighthouse, the stars for finding the way |
| The engine age | Algebra to Calculus | Engines, then the first rocket: rates, growth, paths through the air |
| The far age | the advanced courses | A team working on a drive to the stars (left open: Michael may join this to shipwright's Emberline) |

The tone is warm and practical. Problems are real ones a small town or a crew would have, the
mathematics decides how they turn out, and nobody is mocked for not knowing yet. Wonder is allowed;
cruelty and danger to children are not.

## The market age: Thornwick (pre-algebra)

Thornwick is a hill town where two roads cross a river, the Thorn. Its market fills the square every
day but the last of the week. A mill on the Thorn grinds the town's grain, and the bakery on the square
turns it into bread and pies.

- **Maren** runs the bakery. She keeps its accounts in a ledger by hand and checks them on the
  calculator: what an order costs, how a pie divides, whether the flour will last.
- **Tobin** carries the bakery's orders across town and keeps a tally of what goes where.
- **Hesk** runs the mill, and knows to the sack what the town's grain is and how long it must last.

The ledger matters later: Maren's ledger is kept by her family after her, and in the survey age it
goes to sea as the first page of a ship's log.

## The survey age: Gullhaven (geometry)

Long after Thornwick's market days, its people have reached the sea. Gullhaven is a harbour town on a
wide bay, with a lighthouse that marks the way in. Its streets are new, and nobody has yet drawn a
true map of the town or the bay.

- **Corwen** surveys Gullhaven: directions as angles from fixed points, distances by chain, all of it
  drawn to scale. Unit 1 measures the bay from the end of the harbour wall and the streets where the
  roads meet; later units are the bridge, the lighthouse and the stars the course plan names.

## The rules every story keeps

1. **The mathematics picks the plot, never the reverse.** Each unit's story turns on one problem that
   unit's mathematics solves, and every number in it is one the calculator computes (the vectors).
2. **The story never carries the mathematics.** A learner who skips it, or reads a lesson's plain
   voice when that exists, loses no step.
3. **A character the story leans on is met first** (`cast:` in a lesson's front matter: their home
   lesson is among the lesson's prerequisites, on every route). One who only passes by stands alone
   (`walk-ons:`), and the link back to their home is an invitation, never a need.
4. **A unit's story stands alone.** Its first lesson opens with one line that says where we are, so a
   learner who starts there (placement, or a chosen route) is never lost.
5. **No real person,** and nothing about the learners.

## The files

- `lore/ENTITIES`: one line per character, place, object or age: `kind | name | home | summary`. `home`
  is the lesson that introduces them (`world` for a place or an age that belongs to the whole world).
- `lore/EDGES`: one line per relation: `from | verb | to`, with the verbs `lives_in`, `located_in`,
  `works_with`, `keeps`, `made`, `passes_to`, `before`.
- They map one to one onto loreworks' `world_entities` and `world_edges`, so loading the world into
  loreworks for its 3D view is an import of these two files. These files stay the canon.
- `tools/graph.py` checks them in `make check`.
