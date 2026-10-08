---
id: cnt-01
title: Counting
requires: setup shift-keys soft-keys rpn-arithmetic stack-lift power read-e fix-overflow display-rounds clear-message
status: draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} GOLD DISP FIX 4
display: FIX 4
---

# Counting

How many ways can something happen? Listing the ways works for a few, and fails for many: there are
far too many orders of a deck of cards to list. This lesson counts them without listing: multiply
the choices, count orders with a factorial, and choose some of a group with or without caring about
their order.

## Before you start

The setup from rpn-01: the mode you chose and FIX 4. Each example starts fresh, except where one says
it carries on.

```keys setup
BLUE MODE {mode} GOLD DISP FIX 4
```

## Multiplying the choices

A wardrobe has 3 shirts, 4 pairs of trousers and 2 pairs of shoes. An outfit is one of each. Each of
the 3 shirts goes with each of the 4 trousers, which makes 3 × 4 pairs, and each pair goes with each
of the 2 shoes. When one choice is made after another, and each step has the same number of choices
whatever was picked before it, the number of ways is the numbers of choices multiplied together:

```keys M01
3 ENTER 4 × 2 ×
```

X shows <disp v="M01">24.0000</disp> outfits.

## Orders: the factorial

Five books go on a shelf in a row. Any of the 5 can go first; then any of the 4 left can go second,
then 3, then 2, and the last one has 1 place. So there are 5 × 4 × 3 × 2 × 1 orders. A whole number
times every whole number below it, down to 1, is its factorial, written with an exclamation mark: 5!,
said "five factorial". n! is gold, above ×:

```keys F01
5 GOLD n!
```

X shows <disp v="F01">120.0000</disp>. Factorials grow fast. The orders of a deck of 52 cards:

```keys F02
52 GOLD n!
```

X shows <disp v="F02">8.0658E67</disp>: just over 8 times ten to the 67th, a number 68 digits long, too
long for the screen at FIX 4, so it is shown in scientific form (rpn-01, rpn-03). The calculator keeps
the first 34 of those 68 digits, rounded (rpn-03).

0! is 1. That can be read as one way to arrange nothing, and the next section shows why it has to be
so:

```keys F03
0 GOLD n!
```

X shows <disp v="F03">1.0000</disp>.

## Choosing in order: permutations

Ten runners race, and the first three get gold, silver and bronze. Any of the 10 can win gold, then
any of the 9 left silver, then any of the 8 left bronze: 10 × 9 × 8. No runner is picked twice. Three
chosen from 10, in order, is a permutation, and the number of them is written P(10, 3). It is the start
of 10!, stopped after 3 factors. Since 10! is 10 × 9 × 8 × 7!, dividing 10! by 7! leaves 10 × 9 × 8, and
7 is 10 − 3. So P(n, r) is n! ÷ (n − r)!. When every item is chosen, r is n, and P(n, n) is n! ÷ 0!;
it has to be n!, all of them in order, so 0! has to be 1.

The PROB menu (for probability, blue above ×) has it: its first two soft keys are Cn,r and Pn,r, which
mean C(n, r) and P(n, r). Type n, the size of the group, then ENTER, then r, how many are chosen:

```keys P01
10 ENTER 3 BLUE PROB Pn,r
```

X shows <disp v="P01">720.0000</disp>.

## Choosing without order: combinations

Now pick 3 of the 10 runners for a relay team, where it does not matter who was picked first. The 720
orders count each team many times: the same three runners can be put in order in 3! = 6 ways, and
each of those 6 is a different permutation but the same team. So the number of teams is 720 ÷ 6. A
group chosen without order is a combination, and their number is written C(10, 3); it is P(10, 3)
divided by 3!:

```keys C01
10 ENTER 3 BLUE PROB Cn,r
```

X shows <disp v="C01">120.0000</disp> teams. The 5-card hands that can be dealt from 52 cards are
combinations too, since a hand is the same whatever order its cards arrive in:

```keys C02
52 ENTER 5 BLUE PROB Cn,r
```

X shows <disp v="C02">2,598,960.0000</disp> hands.

Choosing 5 different items from a group of 2 cannot be done: there are no ways. The calculator does not
answer 0, though; whenever r is bigger than n, it refuses:

```keys C03
2 ENTER 5 BLUE PROB Cn,r
```

The screen shows <disp v="C03" kind="message">INVALID DATA</disp>. Clear it with C:

```keys C03B after=C03
C
```

X shows <disp v="C03B">5.0000</disp>, and Y the 2.

Which rule to use comes down to a few questions. Can a choice repeat, each step free of the ones
before, like the outfit or a digit in a code? Multiply the choices. Is every item used once, in some
order? A factorial. Are some chosen from more, none twice? Then does their order matter: if a
different order is a different result, as with prizes, it is a permutation; if not, as with a team, a
combination.

## Exercises

1. A lock opens with a code of 4 digits, each 0 to 9, and a digit may be used more than once. How many
   codes are there?
2. In how many orders can 6 people sit in a row of 6 chairs?
3. A pizza takes 3 different toppings from a list of 8. How many different three-topping pizzas can be
   made?
4. A club of 12 chooses a president, a vice-president and a treasurer, three different people. In how
   many ways?

## Answers

1. 10,000. Each of the 4 digits has 10 choices, and a digit can repeat, so the choices multiply: 10 × 10
   × 10 × 10, which is 10⁴:

   ```keys E01
   10 ENTER 4 yˣ
   ```

   X shows <disp v="E01">10,000.0000</disp>.

2. 720. Every person is seated, in some order: 6!.

   ```keys E02
   6 GOLD n!
   ```

   X shows <disp v="E02">720.0000</disp>.

3. 56. Three toppings are chosen from 8, and their order on the pizza does not matter: C(8, 3).

   ```keys E03
   8 ENTER 3 BLUE PROB Cn,r
   ```

   X shows <disp v="E03">56.0000</disp>.

4. 1,320. Three are chosen from 12, and the order matters, since president and treasurer are different
   jobs: P(12, 3).

   ```keys E04
   12 ENTER 3 BLUE PROB Pn,r
   ```

   X shows <disp v="E04">1,320.0000</disp>.
