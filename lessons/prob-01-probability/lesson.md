---
id: prob-01
title: Probability
requires: setup shift-keys soft-keys rpn-arithmetic stack-lift enter-copies stack-levels swap-roll power sto rcl letter-keys read-e fix-overflow multiplication-principle combination
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Probability

A probability says how likely something is, as a number from 0 to 1: 0 for what cannot happen, 1 for
what must, and in between for everything else. This lesson works probabilities out by counting, as
cnt-01 counted, and then lets the calculator make random numbers to imitate chance.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each example starts fresh, except where one says
it carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Counting the ways

An outcome is one way things can turn out, like rolling a 4, and an event is a group of outcomes, like
rolling an even number. When every outcome is as likely as every other, the probability of an event is
the number of outcomes in it divided by the number of outcomes in all. A fair die has 6 faces, each as likely as the others.
The chance of rolling a 4 is 1 in 6:

```keys D01
1 ENTER 6 ÷
```

X shows <disp v="D01">0.1667</disp>. An even number is 3 of the 6 faces, 2, 4 and 6:

```keys D02
3 ENTER 6 ÷
```

X shows <disp v="D02">0.5000</disp>: as likely as not, which is called an even chance.

## Not

An event either happens or it does not, so the two probabilities add to 1. The probability that
something does not happen is 1 minus the probability that it does. Not rolling a 6 is 1 − 1/6. The
first 1 waits on the stack while 1/6 is worked out, and − then takes 1/6 from it:

```keys N01
1 ENTER 1 ENTER 6 ÷ −
```

X shows <disp v="N01">0.8333</disp>.

## And

Two events are independent when one happening does not change the chances of the other, as with two
dice. The probability that both happen is then the two probabilities multiplied. For two fair dice
you can see why by counting: cnt-01's rule of multiplying the choices gives 6 × 6 = 36 outcomes, all
equally likely, and only one of them is a 6 and a 6, so 1 in 36, which is 1/6 × 1/6. Both dice
showing 6, as 1/6 times 1/6:

```keys A01
1 ENTER 6 ÷ 1 ENTER 6 ÷ ×
```

X shows <disp v="A01">0.0278</disp>: exactly 1 in 36, which FIX 4 rounds to four places.

"At least one" is easier through "not". The chance of at least one 6 in four rolls of a die is 1 minus
the chance of no 6 at all. No 6 in one roll is 5/6, and in four independent rolls it is (5/6)⁴:

```keys A02
1 ENTER 5 ENTER 6 ÷ 4 yˣ −
```

X shows <disp v="A02">0.5177</disp>: a little better than an even chance.

## Counting with combinations

A hand of 5 cards from 52 can be dealt in C(52, 5) ways (cnt-01), and when the deck is well shuffled
every hand is equally likely. The hands that are all hearts are the ways to choose 5 of the 13 hearts:
C(13, 5). So the chance of a hand of five hearts is C(13, 5) ÷ C(52, 5). C(13, 5) waits in Y while
C(52, 5) is worked out:

```keys H01
13 ENTER 5 BLUE PROB Cn,r 52 ENTER 5 BLUE PROB Cn,r ÷
```

X shows <disp v="H01">0.0005</disp>: about 1 hand in 2,000. The number is 0.000495…, and FIX 4 rounds it
to 0.0005; it has a digit other than 0 within four places, so FIX 4 does not switch to scientific form.

## Random numbers

RAND, gold above −, makes a random number: at least 0 and less than 1, spread evenly over that range.
Each press gives the next one:

```keys R01
GOLD RAND
```

A random number makes a die. Times 6, it is at least 0 and less than 6. Its whole part, the part before
the point (the whole part of 4.73 is 4), is then 0, 1, 2, 3, 4 or 5, each as likely; IP gives it, in
the POW menu, blue above yˣ (fn-02). And 1 more is a die's face, 1 to 6. Carrying on:

```keys R02 after=R01
6 × BLUE POW IP 1 +
```

X shows a whole number from 1 to 6. Press GOLD RAND and then 6 × BLUE POW IP 1 + again, as many times as
you like, and keep a tally: over many rolls, each face comes up about one time in six.

The numbers are not truly random: the calculator works each one out from the one before. SEED, blue
above −, sets where that work starts, from the number in X. The same seed gives the same numbers
again, which is useful when a result has to be repeated. Seed with 7 and keep the first number in A;
seed with 7 again and make a number. RCL A brings the first one back to X, and − takes it from the
second:

```keys S01
7 BLUE SEED GOLD RAND STO A 7 BLUE SEED GOLD RAND RCL A −
```

X shows <disp v="S01">0.0000</disp>: the two numbers were the same, and so are the ones after them.

## Exercises

1. One card is drawn from a shuffled deck of 52, which has 4 aces. What is the chance it is an ace?
2. A fair coin is flipped three times. What is the chance of three heads? Of at least one tail?
3. A lottery draws 6 different numbers from 49 at random, and the order they come out in does not
   matter. What is the chance that one ticket of 6 numbers matches them all?
4. Seed with 1 and roll a die with RAND. Seed with 1 again and roll again. What do you notice?

## Answers

1. 4 of the 52 cards are aces:

   ```keys E01
   4 ENTER 52 ÷
   ```

   X shows <disp v="E01">0.0769</disp>, 1 in 13.

2. Each flip is heads with probability 0.5, and the flips are independent, so three heads is 0.5³:

   ```keys E02
   0.5 ENTER 3 yˣ
   ```

   X shows <disp v="E02">0.1250</disp>, 1 in 8. At least one tail is "not three heads". Carrying on, with
   0.125 in X, 1 − 0.125 needs the 1 first, so x↔y puts them in order:

   ```keys E02B after=E02
   1 x↔y −
   ```

   X shows <disp v="E02B">0.8750</disp>.

3. The draws are combinations of 6 from 49, all equally likely, and a ticket is one of them:
   1 ÷ C(49, 6):

   ```keys E03
   1 ENTER 49 ENTER 6 BLUE PROB Cn,r ÷
   ```

   X shows <disp v="E03">7.1511E-8</disp>: about 7 in 100 million, or 1 in nearly 14 million, too small for
   FIX 4's places, so it is shown in scientific form.

4. The same face both times: seeding with 1 again makes the same random number, so the same roll. Keep
   the first face in A, and take it from the second:

   ```keys E04
   1 BLUE SEED GOLD RAND 6 × BLUE POW IP 1 + STO A 1 BLUE SEED GOLD RAND 6 × BLUE POW IP 1 + RCL A −
   ```

   X shows <disp v="E04">0.0000</disp>.
