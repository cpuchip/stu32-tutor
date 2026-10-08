# prob-01b evidence: loot boxes, gacha, and what 1% really costs

Decision 63 (Michael): "two lesson sets here, one that doesn't use poker, maybe it could use gotcha game
stats? why loot boxes suck! and the two cover the same material from different angles." prob-01b is
prob-01's material (one chance, not, and, at least one, combinations, random numbers) through a 1%
item's pulls. Its topics are its own in TOPICS (a topic is taught once), and the course lists it beside
prob-01 in unit 9. The rates and prices are examples, not any real game's.

## Expected values (2026-10-08, core c7ab388)

Oracle: build/proto/prob01b.py, modelling the keys (each operation rounded once; yˣ with a whole-number
power the exact power rounded once). Every formula is checked against its definition in exact
fractions: the pity average against the sum of the chances of reaching each pull; exactly one and two
against C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ. 15/15 vectors, 14/14 display vectors; the core agreed on every one at the
first run.

| Vector | What | Value (shown) |
|---|---|---|
| P01 | 1 − 0.01 | 0.99 |
| P02, P03 | 1 − 0.99¹⁰, 1 − 0.99¹⁰⁰ | 0.0956, 0.6340 |
| M01, M02 | 1 ÷ 0.01 pulls; × 1.50 | 100, 150 |
| T01, T02 | pity at 90: (1 − 0.99⁹⁰) ÷ 0.01; × 1.50 | 59.5268, 89.2902 |
| K00, K01, K02 | none, exactly one, exactly two in 100 | 0.3660, 0.3697, 0.1849 |
| R01 | RAND | within [0, 1], by property |
| E01, E02, E02B, E03 | a 5% item: at least one in 20; 1 ÷ 0.05; × 2; pity at 20 | 0.6415; 20; 40; 12.8303 |

Figures said in the prose without a block, computed exactly: 0.99³⁰⁰ ≈ 0.049 (about 1 player in 20 still
without the item after 300 pulls); 0.99⁸⁹ ≈ 0.41 (about 4 in 10 reach the 90th pull); none + one + two
≈ 0.921, three or more ≈ 0.079 (about 1 in 13).

## Non-author read (2026-10-08)

Every value matched and the stack traces landed. Taken:
- Why the sum of the chances of reaching each pull is the average: shown with 100 players; the sum's 90
  terms named; seq-01's form connected to the one used (both signs turned over).
- "The timer helps the unluckiest players": about 4 in 10 reach the 90th pull, so said.
- Exactly-k holds without a timer, said; why the C(100, 1) chances add (only one way can happen at a
  time) said; none shown as its own block (K00) instead of being worked from another.
- "A lucky streak of several rare items is rare too" overstated (three or more is about 1 in 13): now
  that figure.
- 1 ÷ p given its conditions and a reason.
- The game's motive ("the game sets the rates to make money") was stated as fact about real games, and
  its "so" did not follow: removed; the closing says what the averages are, over many items.
- "The game does not remember (unless it says so)" claimed real games always disclose: now the lesson's
  own assumption.
- The waiting numbers on the stack said (T01, K01); enter-copies, stack-levels and random added to
  requires; no block named in the prose.
- The title promised "the odds against you", which prob-01 defines as a negative expected value this
  lesson never computes (there is no cash payout): now "what 1% really costs", which is what it shows.
- "1% sounds like one in a hundred" (it is): now "a hundred pulls … can sound like a sure thing"; "fair"
  dropped; "gacha" defined; the RAND experiment at 10% so it can be done by hand; "no limit" grounded
  (1 in 20 past 300 pulls).
- Exercise 3 on the pity timer (12.8303 pulls for a 5% item with a timer at 20); exercise 1 in the
  lesson's own x↔y order.

## Checks

`make check`: 15/15 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (3): at least one in 100 quoted as certain, the pity sum without taking
0.99⁹⁰ from 1, exactly one without its C(100, 1); all red.
