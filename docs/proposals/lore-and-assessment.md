# Lore, quizzes and checkpoints (PROPOSAL, for Michael)

**Status:** a proposal. Nothing is built until abacus's cards carry his picks (basecamp #5221).

**Ruled** (Michael, relayed verbatim by basecamp #5221): the shared universe with a new cast per course
("its like series in star trek ... and we could have cameos in each story and graph links back to
where those characters live originally!"). docs/proposals/story-world.md's Shape B stands, with
cameos.

**His next words:** "We need lore, casts of characters, shared universe, stories, amd problems to
solve. With quizzes/tests and checkpoints for formative assessment along the way, with achievements
too! We could.. game-ify it abit and make the courses rougelike, letting the adventurer choose their
course? Or lesson path? Not just take each course. With multiple entry points?"

How the work divides:
- **tutor:** the lore (as checked data), the quizzes and checkpoints (with the core as judge), and the
  graph data a route map needs.
- **primer:** the surfaces: achievements, the choose-your-route map, cameo links, and the 3D view if
  wanted.

## 1. The lore bible, as data the check reads

**Where it lives.** The lore is part of a public CC BY-SA curriculum and must stay true to the lessons
that use it, so its canon lives in stu32-tutor beside them, versioned and checked by `make check`,
like lessons/TOPICS. Three files under `lore/`:

- `lore/WORLD.md`: the prose bible. The world's shape, its eras in order, what each era built, its
  tone, and the rules every story keeps.
- `lore/ENTITIES`: one line per character, place, object or era:
  `kind | name | home | summary`. `home` is the course and lesson that introduces it (a place or
  object may be `world`).
- `lore/EDGES`: one line per typed relation: `from | verb | to`, from a fixed verb list (lives_in,
  located_in, member_of, made, carried_by, descends_from, appears_in, before). For example: the
  survey ship `appears_in` geometry; Thornwick's ledger `carried_by` the survey's youngest; one era
  `before` the next.

A lesson's front matter names who appears in it, in two kinds (abacus #5227):
- **`cast: name name`:** characters the story leans on. A reader must already have met them.
- **`walk-ons: name name`:** characters whose part stands alone, readable without their home lesson.

**Why two kinds.** Under open routes (section 3) a learner reaches a lesson by any path the
prerequisites allow, so "before" has no single meaning. A check against one course order would pass
a lesson that some route reaches before the character's home lesson. The rule must hold on every
route.

**What graph.py refuses:**
- a name in `cast:` or `walk-ons:` that is not in ENTITIES;
- an entity whose home lesson does not exist;
- a `cast:` character whose home lesson is not among the lesson's prerequisites, taken transitively
  through the lesson graph. Every route to the lesson then passes through the home, whatever order
  the learner takes. A course's own cast is introduced in its unit 0, which every later lesson of
  the course requires, so the rule costs that cast nothing;
- an edge with an unknown verb, or an endpoint that is not an entity.

That a walk-on's text stands alone cannot be machine-checked. The non-author read checks it, reading
the lesson as a learner who has not met them.

**A cameo** is a character in a lesson outside their home course. graph.py marks it, and `--json`
gives each cameo its home lesson. Those are the "graph links back to where those characters live
originally" Michael asked for: data primer renders, not prose to maintain.

A cameo never carries mathematics; the graph does. A cameo the plot leans on is in `cast:` and must
pass the prerequisite rule above, so its home lesson is on every route to it. A passing appearance is
a walk-on, readable alone, with the link back as an invitation, not a dependency. It is a door back
to another course, never a wall.

**Controls,** one for each rule:
- a `cast:` character whose home is not a prerequisite;
- a cast name not in the lore;
- an edge with an unknown verb;
- a walk-on that the planted text leans on, caught by the read, not by graph.py. That limit is
  stated, not hidden.

**Loreworks** (pg-ai-stewards' world engine) models a world the same way: entities with kind, name,
aliases, summary and source references, and typed directed edges with a verb vocabulary. It gives the
3D graph view basecamp mentions. I recommend ENTITIES and EDGES shaped to map one-to-one onto its
`world_entities` and `world_edges`, so loading the universe into loreworks is an import of two files.
The source of truth stays these files, for three reasons:
- loreworks' content is private by policy (engine public, content private), and this lore is public;
- the site is static, with no database behind it;
- every lore line must be checked against the lessons in the same commit that changes them.

If Michael wants the 3D view, the import is one command, and loreworks is a projection of the canon,
not its home.

**What the bible holds before any story is written:**
- the world and its eras, in order: Thornwick's market age, the survey age, the rocket yard's age,
  and the warp age (or the Emberline, if he joins it);
- a cast per course, three or four people each;
- the places, and the heirlooms that pass between eras;
- the cameo rules;
- for each unit of a course, the problem its story turns on, chosen from the unit's mathematics:
  the maths picks the plot, never the reverse.

Every name is invented. Nothing is taken from the book he named.

## 2. Quizzes and checkpoints, judged by the core

**One item format for three uses:** a quiz inside a lesson, a checkpoint at the end of a unit, and
placement (docs/proposals/placement.md).

- **In the lesson:** a ```` ```quiz Q07 ```` block, with the question in the prose above it. Its
  answer is a vector in vectors.txt, Q07, written and checked like every example. Each item names the
  topics it tests (`topics:`), so a miss links back to the section that teaches them.
- **The core as judge.** The learner works the question by hand, then enters the answer on the
  in-page calculator, or types the number the calculator would show. The page compares the core's
  value with the vector's exact result. Where a question is numeric (a SOLVE or an integral), the
  tolerance is the vector's own, `X#c,t`, proven by a control as now.
- **Formative, not a grade.** A wrong answer gets a hint, not a mark. Each item may list likely
  wrong answers, each with the slip that produces it and a hint naming the step. For a fraction sum,
  "adding tops and bottoms gives 3/7" comes with "a common bottom first". Each wrong answer is
  computed by an oracle of the slip, so a hint fires only on the exact value that slip makes.
- **Checkpoints:** a short set at the end of a unit, drawn from the unit's topics, worked by hand
  and then checked. The result says which sections to revisit, and nothing is sent anywhere.

**What check.py and the controls add:**
- every quiz block has a passing vector;
- no quiz's answer is quoted in the prose before its block, so the lesson does not give it away;
- every listed wrong answer differs from the right one, and each is produced by its stated slip;
- every item's topics exist.

Controls plant a leaked answer, a wrong answer equal to the right one, and a hint whose slip does not
make its value.

## 3. Routes, entry points and achievements: the graph's part

His "choose their course, or lesson path ... multiple entry points" needs no new data. The
prerequisite graph already says which lessons a learner is ready for: those whose required topics
they have met. What I would add:

- **`--json` gains, per lesson, the topics it teaches and the lessons that unlock it.** primer can
  then draw a map where any lesson whose requirements are met is open, in any course. That is the
  roguelike shape: the learner chooses the next room among the open doors.
- **Entry points are each course's unit 0** (start-01, rpn-01, and geometry's when written), plus
  wherever placement lands a learner.
- **Each unit's story stands alone** (a one-line recap opens it), so a learner who takes units out
  of order still reads a whole story. This is Shape B's rule already.
- **Achievements are primer's.** I would suggest they follow the graph and the checkpoints, not time
  spent: a unit's checkpoint passed, a course finished, a cameo's home visited. They are kept in the
  browser only, since there are no accounts and nothing is sent, so an achievement lives on one
  device.

## For him to choose

1. **The lore as files in stu32-tutor,** with loreworks as an optional 3D view of them (recommended),
   or loreworks as the home.
2. **Wrong-answer hints in the quizzes,** each tied to a named slip (recommended), or right/wrong
   only.
3. **Open routes:** any lesson whose requirements are met is open (recommended), or the courses in
   order with the map as a guide.
4. **The first course to get its bible and cast:** pre-algebra (two lessons written, the bakery
   already in them), as recommended, or another.
