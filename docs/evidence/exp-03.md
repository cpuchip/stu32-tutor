# exp-03 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/exp03.py, modelling the keys: LN and LOG correctly rounded (60 digits, then
34), each division rounded once. It asserts that log 2 ÷ log 1.04 and ln 2 ÷ ln 1.04 come out equal
at 34 digits, which the lesson's "the base cancels" leans on. Every vector matched the core on the
first run, and both round trips (10^(log 2), e^(ln 2)) give exactly 2, as does 1.04 to its doubling
power.

| Vector | What | FIX 4 |
|---|---|---|
| L01 | log 1000 | 3.0000 |
| L02, L03 | log 2, then 10ˣ | 0.3010, 2.0000 |
| N01, N02 | ln 2, then eˣ | 0.6931, 2.0000 |
| S01, S03 | log 2 ÷ log 1.04, ln 2 ÷ ln 1.04 | 17.6730 (17.67298768512971317198964813362911) |
| S02 | 1.04 to that power | 2.0000 (exactly 2) |
| Y17, Y18 | 1.04¹⁷, 1.04¹⁸ | 1.9479, 2.0258 (doubles at the 18th yearly payment) |
| V01, V01B | 0 LOG; C | LOG(0) |
| H01 | ln 0.5 ÷ ln 0.9 | 6.5788 |
| C01 | ln 2 ÷ 0.06 | 11.5525 |
| E01-E01C | ln 3 ÷ ln 1.04; 1.04²⁸, 1.04²⁹ | 28.0110; 2.9987, 3.1187 (29 years) |
| E02, E03 | ln 0.5 ÷ ln 0.8, ln 2 ÷ 0.03 | 3.1063, 23.1049 |

## Sources and probes

- Keys (keymap.c): LN is the third key of the top row with LOG gold above it; eˣ the second with 10ˣ
  gold above it.
- "A power of a power multiplies the powers": exp-02 and num-03; negative powers: num-03.
- LOG of 0 shows LOG(0) and LN of a negative LOG(NEG) (probed, keyrun --sequence, 8f304cd).
- The oracle asserts 1.04¹⁷ < 2 < 1.04¹⁸ and 1.04²⁸ < 3 < 1.04²⁹ (exact powers, rounded once).

## Non-author read (2026-10-07)

Nine findings, all taken. The largest was mathematical: growth paid once a year grows only at
each payment, so 17.67 years means doubling at the 18th payment and tripling takes 29 years, not
28.01; the lesson now checks the whole years either side (Y17, Y18, E01B, E01C) and says a fraction
of a year counts only for smooth growth. Also: "the base cancels" replaced by the same argument
with e in place of 10; "base" defined; the four shown places of log 2 said to be rounded (typing
them back would not give 2); negative logarithms explained by num-03's negative powers, and 0 and
negatives shown refused (LOG(0)); the stacks of S01 and S02 narrated, with typing after a function
pushing up as after + or ×; 10ˣ tied to num-03; (10^(log 1.04))ⁿ written out; a third exercise on
ln 2 ÷ r.

## Checks

`make check`: 19/19 vectors in 33s, 35s and STU, from a fresh and a used core; 20 keys blocks.
Controls: the division the wrong way round, LOG keyed without its gold shift, the half-life quoted
as negative; all red.

## Abacus's accuracy read (#4646, 2026-10-07)

Accepted at 7f1d58f (24/24 in 33s, 35s and STU). log 2 ÷ log 1.04 = …13362911 (correctly rounded); the powers 1.9479, 2.0258, 2.9987, 3.1187 right;
functions enable lift (the 33s guide's appendix B); LOG(NEG) and LOG(0) are the guides' texts (35s p.F-3).
