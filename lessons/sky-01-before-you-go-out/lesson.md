---
id: sky-01
title: Before you go out
modes: STU
modes_reason: algebraic entry, this course's default, is STU mode's alone (firmware 029); RPN is offered in STU mode too
entries: alg rpn
requires: calc-setup calc-shift-keys calc-soft-keys calc-first-calculation column-addition column-subtraction
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
display: FIX 4
---

# Before you go out

Step outside on a clear night and at first only a few stars show. Wait, and more and more of them appear, though
the sky has not changed at all: your eyes have. Two things decide what you will see, how dark your eyes have
become and how dark the sky is where you stand, and one thing you must never do: look at the Sun. How do you get
ready to see the most, safely?

## From before

```item SK1F1
prompt: Work out $45 + 25$.
topics: column-addition
answer: type
calculator: no
slip: SK1F1A | forgot to carry | $5 + 5 = 10$: write the 0 and carry the 1 into the tens.
```

```item SK1F2
prompt: Work out $82 − 47$.
topics: column-subtraction
answer: type
calculator: no
slip: SK1F2A | took the smaller digit from the larger | $2 − 7$ needs a borrow: $12 − 7$, with one ten fewer.
```

## Before you start

The setup turns the calculator on and shows four places after the point.
<entry e="alg">Type each calculation the way it is written, then press ENTER, which works as = here.</entry><entry e="rpn">In
RPN, type the first number, ENTER, the second, then the operation.</entry>

```keys setup
BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4
```

## The Sun: never by eye

Never look at the Sun, not even when the Moon covers most of it. NASA's eclipse safety guidance is plain about it.
Ordinary sunglasses, however dark, are not safe. A safe solar viewer, or eclipse glasses, is thousands of times
darker, and should meet the international standard ISO 12312-2. Looking at any part of the bright Sun through a
camera lens, binoculars or a telescope without a special solar filter fixed over its front end causes severe eye
injury at once. Wearing eclipse glasses does not make it safe to look through binoculars or a telescope either.

There is a safe way that needs no special glasses: a pinhole projector. Stand with your back to the Sun and let its
light pass through a small hole onto a card in front of you, and watch the image on the card. Never look at the Sun
through the pinhole.

## Eyes that open slowly

After white light, your eyes take 20 to 30 minutes to adjust to the dark (the US National Park Service's stargazing
advice). Red light disturbs them much less, so observers use a red flashlight, or a white one covered with red
cellophane. One brief flash of white light, from a phone or a car's headlights, can set your night vision back by
several minutes.

So plan the wait. You step outside at 9:40 in the evening and give your eyes 25 minutes. That is 40 minutes past 9
plus 25 minutes:

```keys D01 entry=alg
40 + 25 ENTER
```

```keys D01 entry=rpn
40 ENTER 25 +
```

The screen shows <disp v="D01">65.0000</disp>. An hour has 60 minutes, so 65 minutes past 9 is 5 minutes past 10:

```keys D02 entry=alg
65 − 60 ENTER
```

```keys D02 entry=rpn
65 ENTER 60 −
```

The screen shows <disp v="D02">5.0000</disp>: your eyes are ready at 10:05.

## The sky you can see

Light from streets and buildings brightens the whole sky, and the faint stars vanish into it. Astronomers count a
star's brightness by its magnitude, and a bigger magnitude means a fainter star. The National Park Service's guide
to rating a night sky gives the faintest magnitude you can see: about 2 in a city, 4 in a suburb, 6 in the country,
and 7 under a truly dark sky, far from any lights. How many magnitudes fainter can you see under a truly dark sky
than in a city?

```keys L01 entry=alg
7 − 2 ENTER
```

```keys L01 entry=rpn
7 ENTER 2 −
```

The screen shows <disp v="L01">5.0000</disp>: five magnitudes fainter. What five magnitudes means in brightness comes
later in the course.

## Exercises

1. You go outside at 8:50 and give your eyes 30 minutes. When are they ready?
2. You drive from a suburb to a truly dark sky. How many magnitudes fainter can you see?

## Answers

1. 50 minutes past 8 and 30 more:

   ```keys E01 entry=alg
   50 + 30 ENTER
   ```

   ```keys E01 entry=rpn
   50 ENTER 30 +
   ```

   The screen shows <disp v="E01">80.0000</disp>. 80 minutes past 8 is 20 minutes past 9:

   ```keys E01B entry=alg
   80 − 60 ENTER
   ```

   ```keys E01B entry=rpn
   80 ENTER 60 −
   ```

   The screen shows <disp v="E01B">20.0000</disp>: ready at 9:20.

2. A suburb shows stars to magnitude 4, a truly dark sky to 7:

   ```keys E02 entry=alg
   7 − 4 ENTER
   ```

   ```keys E02 entry=rpn
   7 ENTER 4 −
   ```

   The screen shows <disp v="E02">3.0000</disp>: three magnitudes fainter.

## Mixed review

```item SK1M1
prompt: Your eyes need 30 minutes in the dark. You go outside at 9:45. How many minutes past 10 are they ready?
topics: dark-adaptation
answer: type
calculator: no
slip: SK1M1A | did not take away the hour | $45 + 30 = 75$ minutes past 9, and 60 of those make the hour to 10.
```

```item SK1M2
prompt: Work out $91 − 36$.
topics: column-subtraction
answer: type
calculator: no
slip: SK1M2A | took the smaller digit from the larger | $1 − 6$ needs a borrow: $11 − 6$, with one ten fewer.
```

```item SK1M3
prompt: A city sky shows stars down to magnitude 2, and a country sky down to magnitude 6. How many magnitudes fainter can you see in the country?
topics: light-pollution
answer: type
calculator: no
slip: SK1M3A | added the magnitudes | Fainter by the difference: $6 − 2$.
```

```item SK1M4
prompt: Work out $38 + 47$.
topics: column-addition
answer: type
calculator: no
slip: SK1M4A | forgot to carry | $8 + 7 = 15$: write the 5 and carry the 1 into the tens.
```
