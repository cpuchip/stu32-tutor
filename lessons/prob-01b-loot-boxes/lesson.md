---
id: prob-01b
title: Loot boxes, gacha, and what 1% really costs
requires: setup shift-keys soft-keys rpn-arithmetic enter-copies stack-lift stack-levels swap-roll power reciprocal x-squared percent multiplication-principle combination geometric-sum random
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Loot boxes, gacha, and what 1% really costs

Many games sell chances instead of things. A loot box costs money, or a currency bought with money, and
gives an item chosen at random. Gacha games (the name comes from capsule-toy machines) work the same
way: each "pull" gives a random character or item. The prize everyone wants is rare: say the game
publishes that its rare item comes in 1% of pulls. This lesson works out what that 1% means: how likely
a player is to get the item in 10 or 100 pulls, how many pulls it takes on average, what a "pity timer"
changes, and what it all costs. It covers the same ideas as prob-01, from another angle. The rates and
prices here are examples, not any real game's.

## From before

Two from before, by hand: independent tosses from prob-01, and a percent from num-04.

```item PB2F1
prompt: A fair coin is tossed three times. What is the probability of three tails?
topics: independent
answer: type
calculator: no
slip: PB2F1A | added the chances | Independent events multiply: 0.5 × 0.5 × 0.5.
```

```item PB2F2
prompt: What is 1% of 300?
topics: percent
answer: type
calculator: no
slip: PB2F2A | took 10% | 1% is one hundredth: 300 ÷ 100.
```

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each example starts fresh, except where one says it
carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## One pull

A probability is a number from 0 to 1 saying how likely something is; 1% is 0.01 (num-04). Each pull is
the rare item with probability 0.01, and anything else with the rest: either a pull gives the item or it
does not, so the two probabilities add to 1, and not getting it is 1 − 0.01:

```keys P01
1 ENTER 0.01 −
```

X shows <disp v="P01">0.9900</disp>: 99 pulls in 100 give something else.

## At least one in many pulls

This lesson assumes each pull is drawn afresh, with the same 1% whatever happened before; a pity timer,
below, is the exception. Pulls like that are independent, and the chance that several independent
things all happen is their probabilities multiplied, as cnt-01 multiplied choices. So no rare item in 10
pulls is 0.99 × 0.99 × … ten times, 0.99¹⁰, and at least one rare item is 1 minus that. x↔y puts the 1
first for the subtraction:

```keys P02
0.99 ENTER 10 yˣ 1 x↔y −
```

X shows <disp v="P02">0.0956</disp>: under a 1 in 10 chance after 10 pulls. And in 100 pulls:

```keys P03
0.99 ENTER 100 yˣ 1 x↔y −
```

X shows <disp v="P03">0.6340</disp>. A hundred pulls of a 1-in-100 item can sound like a sure thing, but
about 37 players in 100 still have not got the item.

## How many pulls, on average

If every pull has the same chance p, independently, then in many pulls about p of them give the item:
in 100 pulls at 1%, about 1. So, over many players, the pulls it takes to get one, counting the pull that
gives it, average 1 ÷ p. For 1%, 1 ÷ 0.01:

```keys M01
0.01 1/x
```

X shows <disp v="M01">100.0000</disp> pulls. At 1.50 dollars a pull, carrying on:

```keys M02 after=M01
1.5 ×
```

X shows <disp v="M02">150.0000</disp> dollars, on average, for one rare item. Some players pay far less;
some pay far more. About 1 player in 20 still has no rare item after 300 pulls, which is 450 dollars, since
0.99³⁰⁰ is about 0.049.

## A pity timer

Some games add a "pity timer": if 89 pulls in a row miss, the 90th is guaranteed to be the rare item.
That puts a limit on the cost, and it changes the average. A player makes pull number k only if the pulls
before it all missed: pull 1 always, pull 2 with probability 0.99, pull 3 with 0.99², and so on, up to
pull 90 with 0.99⁸⁹. Picture 100 players: about 100 make pull 1, about 100 × 0.99 make pull 2, and so on.
All their pulls together are 100 times the sum 1 + 0.99 + 0.99² + … + 0.99⁸⁹, so the average for one
player is that sum. It is a geometric sum (seq-01) of 90 terms with first term 1 and ratio 0.99:
1 × (0.99⁹⁰ − 1) ÷ (0.99 − 1), which, with both signs turned over, is (1 − 0.99⁹⁰) ÷ 0.01. With the 1 waiting
on the stack while 0.99⁹⁰ is worked out:

```keys T01
1 ENTER 0.99 ENTER 90 yˣ − 0.01 ÷
```

X shows <disp v="T01">59.5268</disp> pulls on average. Carrying on, at 1.50 a pull:

```keys T02 after=T01
1.5 ×
```

X shows <disp v="T02">89.2902</disp> dollars on average, and never more than 90 × 1.50, 135 dollars. The
timer is no small thing: since 0.99⁸⁹ is about 0.41, about 4 players in 10 reach the guaranteed pull. And
the average is still close to 90 dollars for one item.

## Exactly how many

Without a pity timer, how likely is it that 100 pulls give no rare item at all, exactly one, or exactly
two? None is 0.99¹⁰⁰:

```keys K00
0.99 ENTER 100 yˣ
```

X shows <disp v="K00">0.3660</disp>. For exactly one, one particular pull must be the item and the other 99
must not: 0.01 × 0.99⁹⁹. The one could be any of the 100 pulls, C(100, 1) ways to choose which (cnt-01),
and only one of those ways can happen at a time, so their chances add: C(100, 1) × 0.01 × 0.99⁹⁹. The first
product waits in Y while 0.99⁹⁹ is worked out:

```keys K01
100 ENTER 1 BLUE PROB Cn,r 0.01 × 0.99 ENTER 99 yˣ ×
```

X shows <disp v="K01">0.3697</disp>. Exactly two is C(100, 2) × 0.01² × 0.99⁹⁸, two pulls chosen from 100:

```keys K02
100 ENTER 2 BLUE PROB Cn,r 0.01 GOLD x² × 0.99 ENTER 98 yˣ ×
```

X shows <disp v="K02">0.1849</disp>. None, one and two together are about 0.92, so three or more rare
items in 100 pulls happen about 8 times in 100, roughly 1 in 13.

## A pull on the calculator

RAND (gold, above −) gives a random number more than 0 and less than 1, spread evenly (prob-01). Read it
as a pull for an item of 10%: below 0.1 is the item, which happens 1 time in 10:

```keys R01
GOLD RAND
```

Press it again and again, and count the presses until a number comes up below 0.1. Many runs take only a
few presses; some take twenty or more. For a 1% item the same experiment would usually take dozens of
presses, and often more than a hundred.

## What 1% costs

Every number here points the same way: a 1% chance per pull turns into a long and expensive average,
with no limit on the cost except a timer the game chose to add. The averages describe what happens
across many players, not to any one player, who may pay far less or far more. Knowing them is how to decide,
before paying, what an item is really worth to you.

## Exercises

1. An item comes in 5% of pulls. How likely is at least one in 20 pulls?
2. How many pulls does that item take on average, and what does that cost at 2 dollars a pull?
3. With a pity timer that makes the 20th pull a sure thing, how many pulls does that item take on
   average?

## Answers

1. 1 minus the chance of none: 1 − 0.95²⁰, with x↔y for the order, as for many pulls above:

   ```keys E01
   0.95 ENTER 20 yˣ 1 x↔y −
   ```

   X shows <disp v="E01">0.6415</disp>: about 64 in 100, not a sure thing.

2. 1 ÷ 0.05 pulls:

   ```keys E02
   0.05 1/x
   ```

   X shows <disp v="E02">20.0000</disp>. Carrying on, at 2 dollars each:

   ```keys E02B after=E02
   2 ×
   ```

   X shows <disp v="E02B">40.0000</disp> dollars on average.

3. The sum 1 + 0.95 + … + 0.95¹⁹, 20 terms, which is (1 − 0.95²⁰) ÷ 0.05:

   ```keys E03
   1 ENTER 0.95 ENTER 20 yˣ − 0.05 ÷
   ```

   X shows <disp v="E03">12.8303</disp> pulls, fewer than the 20 without the timer.

## Mixed review

Four from this lesson and the ones before it, in no order. Work each by hand unless it says to use
the calculator.

```item PB2M1
prompt: A rare item comes in 5% of pulls. How many pulls does it take on average?
topics: mean-tries
answer: type
calculator: no
slip: PB2M1A | gave the percent | On average it takes 1 ÷ p pulls: 1 ÷ 0.05.
```

```item PB2M2
prompt: Add 1 + 2 + 4 + 8 + 16.
topics: geometric-sum
answer: type
calculator: no
slip: PB2M2A | the next term, not the sum | The sum of 1, 2, 4, 8 and 16 is one less than the next term, 32.
```

```item PB2M3
prompt: A rare item comes in 2% of pulls. What is the chance one pull does not give it?
topics: pull-chance
answer: type
calculator: no
slip: PB2M3A | the chance of getting it | Not getting it is everything else: 1 − 0.02.
```

```item PB2M4
prompt: A bet pays 10 coins with probability 0.2, and nothing otherwise. What does it pay on average, before its cost?
topics: expected-value
answer: type
calculator: no
slip: PB2M4A | the payout as sure | It pays 10 only one time in five, on average: 10 × 0.2.
```

## Checkpoint

Questions on the whole unit. Work each by hand first (a few offer the calculator), then give your answer; the page checks it. A wrong answer that comes from a common slip gets a hint that names the step.

```item CP9A
prompt: In how many ways can 2 of 6 people be chosen, if the order does not matter?
topics: combination
answer: type
calculator: no
slip: CP9A1 | counted each pair twice | 6 × 5 counts each pair twice, once in each order: divide by 2.
slip: CP9A2 | 6 times 2 | Count the pairs: 6 × 5 ÷ 2.
```

```item CP9B
prompt: A fair coin is tossed twice. What is the probability of two heads?
topics: independent
answer: type
calculator: no
slip: CP9B1 | one head | Both tosses must be heads: 1/2 times 1/2.
slip: CP9B2 | added | A head and then a head again: multiply, 1/2 × 1/2, not add.
```

```item CP9C
prompt: A game costs 1 coin to play. A fair coin is tossed: heads pays 3 coins, and tails pays nothing. What is the expected value of one play, counting its cost?
topics: expected-value
answer: type
calculator: no
slip: CP9C1 | left out the cost | Take away the coin each play costs: 3 × 1/2 − 1.
slip: CP9C2 | the payout as sure | The 3 coins come only half the time: 3 × 1/2, then − 1.
```
