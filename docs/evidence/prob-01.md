# prob-01 evidence: probability

## Expected values (2026-10-07, core c7ab388)

Oracle: build/proto/prob01.py, modelling the keys: each operation rounded once to 34 digits, half even.
14/14 vectors, 12/12 display vectors.

| Vector | What | Value (shown) |
|---|---|---|
| D01, D02 | a 4; an even number | 1/6 (0.1667); 0.5 |
| N01 | not a 6: 1 − 1/6 | 0.8333… (0.8333) |
| A01 | both 6: 1/6 × 1/6, each rounded | 0.0277…78 (0.0278) |
| A02 | at least one 6 in four: 1 − (5/6)⁴ | 0.51774691… (0.5177) |
| H01 | five hearts: C(13, 5) ÷ C(52, 5) = 1287/2598960 | 0.000495198… (0.0005) |
| R01, R02 | RAND; IP(6 × RAND) + 1 | checked by property: within [0, 1]; within [1, 6] |
| S01, E04 | the same seed, the same number; the same die face | difference exactly 0 |
| E01..E03 | 4/52; 0.5³ and 1 − 0.125; 1/C(49, 6) | 0.0769; 0.125, 0.875; 7.1511E-8 |

RAND's numbers cannot be predicted without the core's generator, so no RAND value is quoted, and its
vectors assert the properties the lesson states. The tolerance expectations (X#) are checked by the
student run too: a control plants X#10,0.5 on R02 and is red ("expected X#10,0.5, got +2E+0").

## Probe: the RAND claims, measured (keyrun --sequence, 35s mode, a fresh device)

300 RANDs: all at least 0 and below 1 (least 0.00703, greatest 0.99905), all different, mean 0.4904.
300 die faces IP(6 × RAND) + 1: all whole numbers from 1 to 6, counts 1: 58, 2: 50, 3: 36, 4: 52,
5: 55, 6: 49 (about 50 each; the 36 is within chance for 300 rolls). Seeding with 7 twice gives the
same first and second numbers, and the first differs from the second. A fresh device's RAND sequence
is the same every time (the probe's first RAND was 0.2360 in 33s, 35s and STU mode), which is why the
lesson does not say "yours will not match anyone else's".

## Non-author read (2026-10-07)

Every block matched its vector. Taken:
- "The probability that both happen is the two probabilities multiplied, because of cnt-01's rule":
  the count proves it for fair dice only, and A01 computed 1 ÷ 36, never multiplying probabilities. Now
  the rule is stated for independent events, the count shown as why for fair dice, and A01 keys
  1/6 × 1/6.
- "all equally likely when the deck is shuffled (cnt-01)" credited cnt-01 with a claim it never made:
  the condition is now the lesson's own.
- "Each press gives a new one, so yours will not match anyone else's" contradicted SEED, and a fresh
  device's sequence is fixed: dropped.
- S01's narration took the subtraction the wrong way ("take the second … from the first"): RCL A
  brings the first to X, and − takes it from the second.
- RAND's claims (range, whole faces, "the same numbers" plural) were not checked by the vectors: the
  probe above measures them.
- N01's waiting 1 and H01's waiting C(13, 5) explained; IP's whole part with an example (4.73 is 4);
  "the two blocks" as the keys themselves; `stack-levels` and `read-e` added to requires.
- Nothing exercised RAND or SEED: exercise 4 (the same seed, the same die face).
- Exercise 3 now states the lottery's conditions (different numbers, at random, order not mattering).
- "outcome" and "event" defined; "cnt-01's rule of multiplying the choices"; "exactly 1 in 36"; "an
  even chance" tied to "as likely as not"; "the ways to choose 5 of the 13 hearts"; why H01 shows
  0.0005 and not scientific form.
- One sentence of history ("Gamblers in the 1600s bet on exactly this …") was cut in the self-audit:
  no source for it was read this session.
- Left for Michael: the poker hand and the lottery are gambling settings for learners 13 and over.

## Checks

`make check`: 14/14 vectors in 33s, 35s and STU, from a fresh and a used core, and the student run in
order in each mode. Controls (4): "not" worked as 1/6 − 1, at least one 6 quoted without the not, the
same seed shown without seeding again, a die face claimed outside 1 to 6 (the tolerance checked); all
red.
