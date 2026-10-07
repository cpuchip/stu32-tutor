# exp-02 evidence

## Expected values (2026-10-07, core 8f304cd)

The oracle is build/proto/exp02.py, modelling the keys: each operation rounded once to 34 digits,
half even; yˣ with a whole power exact, then rounded once (unit 038); eˣ correctly rounded (60
digits, then 34). Every vector matched the core exactly on the first run.

| Vector | What | FIX 4 |
|---|---|---|
| C01 | 1000 × 1.06 | 1,060.0000 |
| C02 | 1000 × (1 + 0.06/12)¹² | 1,061.6778 |
| C03 | 1000 × (1 + 0.06/365)³⁶⁵ | 1,061.8313 |
| L01-L03 | (1 + 1/n)ⁿ for 12, 365, 1000000 | 2.6130, 2.7146, 2.7183 |
| L04 | e¹ | 2.7183 (2.718281828459045235360287471352662) |
| L05, L06 | (1 + 0.06/10⁶)^10⁶ and e^0.06 | 1.0618, 1.0618 (within 1E-8, asserted) |
| G01 | 1000 × e^0.06 | 1,061.8365 |
| E01-E03 | 2500: e^0.4, 1.04¹⁰, (1 + 0.04/12)¹²⁰ | 3,729.5617, 3,700.6107, 3,727.0817 |

The oracle asserts the orderings the prose states: yearly < monthly < daily < continuous, the
limits increasing towards e, and yearly < monthly < continuous in the exercises.

## Sources and probes

- eˣ is the second key of the top row and 1/x the fifth (keymap.c keys 7 and 10); "a power of a
  power multiplies the powers" leans on num-03's (2³)² = 64.
- Two slips of mine caught before any reader: "twelve times as many payments" (12 to 365 is about
  thirty), and E01's 2500 said to wait in Y (it is in Z until the first ×).

## Non-author read (2026-10-07)

No wrong mathematics or keys; ten findings, all taken. The largest: C02's 1000 "waited in Y below",
but it waits in Z most of the way and reaches Y only for the last ×. Also: r is the rate as a
decimal (a learner fresh from exp-01's r% could type 6); the limit of (1 + r/n)ⁿ shown, not asserted
(L05 and L06); (eʳ)ᵗ = e^(r × t) given its power-of-a-power step; the amount of 1 in (1 + 1/n)ⁿ named,
and the order of the addition explained; ALL pointed to for the 34 digits; the opening no longer
says the key gives e; "limit" defined where it first appears; a third exercise practises the
lesson's own (1 + r/n)ⁿ.

## Checks

`make check`: 13/13 vectors in 33s, 35s and STU, from a fresh and a used core; 14 keys blocks.
Controls: a monthly rate keyed without ÷ 12, 10ˣ for eˣ, the limit quoted to more places than FIX 4
shows; all red.

## Abacus's accuracy read (#4646, 2026-10-07)

Accepted at 7f1d58f (24/24 in 33s, 35s and STU). mpmath confirms 1061.6778, 1061.8313, 1061.8365 and the sixth-decimal difference (2.7182804… against
2.7182818…); statements (1)-(4) right.
