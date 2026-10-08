---
id: prob-01
title: Probability, and why the odds are against you
requires: setup shift-keys soft-keys rpn-arithmetic stack-lift enter-copies stack-levels swap-roll power sto rcl letter-keys read-e type-e fix-overflow multiplication-principle combination
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Probability, and why the odds are against you

A probability says how likely something is, as a number from 0 to 1: 0 for what cannot happen, 1 for
what must, and in between for everything else. This lesson works probabilities out by counting, as
cnt-01 counted, and then uses them to answer a question every game of chance hides: over many plays,
how much does a bet win or lose on average? For a game of chance run to make money, the answer is that
it loses, and the calculator can show by how much. Last, it lets the calculator make random numbers to
imitate chance.

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

## Expected value: what a bet is worth

A game costs 1 dollar to play. Roll a die: a six pays you 5 dollars, and anything else pays nothing;
either way the dollar you paid is gone. In many plays, a six comes up about one play in six, so on
average a play pays 5 × 1/6 + 0 × 5/6, each payout times its probability, added up. 5 × 1/6 is 5 ÷ 6.
Take away the 1 dollar each play costs, and the average result per play is 5/6 − 1. That average,
over the outcomes, of what you end up gaining or losing, is the expected value of the bet:

```keys X01
5 ENTER 6 ÷ 1 −
```

X shows <disp v="X01">-0.1667</disp>: about 17 cents lost per play, on average. One play can still win;
the average is what many plays add up to, divided by the number of plays. Carrying on, the expected
total over 600 plays:

```keys X02 after=X01
600 ×
```

X shows <disp v="X02">-100.0000</disp>: a player expects to lose about 100 dollars over 600 plays; real
totals land above and below that, but the more someone plays, the more surely their average result
per play comes out close to the 17 cents lost. The chance of a six is fair, 1 in 6; what is against the
player is the payout. A fair game would pay 6 dollars on a six, and its expected value would be 0. A
game of pure chance run to make money from its players' bets has to take in more than it pays out, so
its expected value for the player is below 0: that is what "the odds are against you" means. In total,
what the people who run it take in, before their own costs, is what the players lose. People play
anyway because one play buys a chance at a prize; the expected value is what that chance costs, on
average, every time.

## Random numbers

RAND, gold above −, makes a random number: more than 0 and less than 1, spread evenly over that range.
Each press gives the next one:

```keys R01
GOLD RAND
```

A random number makes a die. Times 6, it is more than 0 and less than 6. Its whole part, the part before
the point (the whole part of 4.73 is 4), is then 0, 1, 2, 3, 4 or 5, each as likely; IP gives it, in
the POW menu, blue above yˣ (fn-02). And 1 more is a die's face, 1 to 6. Carrying on:

```keys R02 after=R01
6 × BLUE POW IP 1 +
```

X shows a whole number from 1 to 6. Press GOLD RAND and then 6 × BLUE POW IP 1 + again, as many times as
you like, and keep a tally: over many rolls, each face comes up about one time in six. Play the game
of the last section with it, counting 5 dollars for each six and 1 dollar paid each time, and watch
the total drift down.

The numbers are not truly random: the calculator works each one out from a hidden number it keeps and
moves on every time. SEED, blue above −, sets that hidden number from X. The same seed gives the same
numbers again, which is useful when a result has to be repeated. Seed with 7 and keep the first number in A;
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
   matter. What is the chance that one ticket of 6 numbers matches them all? If a ticket costs 2 dollars
   and the only prize is 10 million dollars, what is a ticket's expected value?
4. Seed with 1 and roll a die with RAND. Seed with 1 again and roll again. What do you notice?
5. A scratch card costs 1 dollar. It pays 10 dollars with probability 1/20, 2 dollars with probability
   1/10, and nothing otherwise. What is its expected value?

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
   FIX 4's places, so it is shown in scientific form. The expected value is the prize times that chance,
   less the ticket. Carrying on, 10 million (1 E 7) times the chance:

   ```keys E03B after=E03
   1 E 7 ×
   ```

   X shows <disp v="E03B">0.7151</disp>: a ticket wins about 72 cents, on average. Carrying on, less the
   2 dollars it cost:

   ```keys E03C after=E03B
   2 −
   ```

   X shows <disp v="E03C">-1.2849</disp>: each ticket loses about 1.28 dollars, on average.

4. The same face both times: seeding with 1 again makes the same random number, so the same roll. Keep
   the first face in A, and take it from the second:

   ```keys E04
   1 BLUE SEED GOLD RAND 6 × BLUE POW IP 1 + STO A 1 BLUE SEED GOLD RAND 6 × BLUE POW IP 1 + RCL A −
   ```

   X shows <disp v="E04">0.0000</disp>.

5. Each payout times its probability, added up, less the 1 dollar: 10 × 1/20 + 2 × 1/10 − 1.

   ```keys E05
   10 ENTER 20 ÷ 2 ENTER 10 ÷ + 1 −
   ```

   X shows <disp v="E05">-0.3000</disp>: 30 cents lost per card, on average.
