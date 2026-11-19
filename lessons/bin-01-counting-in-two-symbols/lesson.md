---
id: bin-01
title: Counting in two symbols
device: none
requires:
status: pilot, draft prose (accuracy: lessons/ACCEPTED; not yet read by Michael)
---

# Counting in two symbols

Inside a computer, every number, every letter and every picture is held as a long row of bits, and a bit is only
ever 0 or 1. Two symbols is all a computer has to write with. How can two symbols hold any number at all? The
answer was worked out with pen and paper, centuries before there was a machine to use it.

## Ten symbols, and where they sit

We count with ten symbols, 0 to 9. After 9 there is no new symbol: we write 10, a 1 moved one place to the left. Each
place is worth ten of the place to its right, so the places are worth 1, 10, 100, 1000 and on. The number 4302 is 4
thousands, 3 hundreds, 0 tens and 2 ones. The 0 matters: it holds the tens place open, so the 3 stays a hundred.

Nothing about this needs ten. Ten is only where we start a new place.

## Leibniz's two symbols

In 1703 Gottfried Wilhelm Leibniz wrote a short paper for the Academy of Sciences in Paris, *Explication de
l'arithmétique binaire*, the explanation of binary arithmetic. He had counted for years, he wrote, by twos instead of
by tens, with only two symbols, 0 and 1. Starting a new place at two instead of ten, he wrote:

```quote leibniz-1703 p. 224
C’est pourquoi deux s’écrit ici par 10, et deux fois deux ou quatre par 100, et deux fois quatre ou huit par 1000, et
deux fois huit ou seize par 10000, et ainsi de suite.
```

That is: "This is why two is written here as 10, and twice two, or four, as 100, and twice four, or eight, as 1000,
and twice eight, or sixteen, as 10000, and so on." (He wrote in French; the English is ours.)

So in binary each place is worth two of the place to its right: 1, 2, 4, 8, 16, 32 and on. Counting goes like this.
When the ones place is full, it goes back to 0 and the next place gains a 1, just as 9 turns into 10.

| Number | In binary |
|---|---|
| 0 | 0 |
| 1 | 1 |
| 2 | 10 |
| 3 | 11 |
| 4 | 100 |
| 5 | 101 |
| 6 | 110 |
| 7 | 111 |
| 8 | 1000 |

```item BN1A
prompt: You are counting in binary and have reached 1011. What number do you write next?
topics: binary-counting
answer: text
calculator: no
slip: BN1AA | the last digit counted on as in tens | There is no 2 in binary. Adding 1 fills the ones place, so it goes back to 0 and carries 1 into the twos place, as $9 + 1$ does in tens. The twos place is full too, so it carries on into the fours.
slip: BN1AB | counted down, not up | That is the number before 1011. Add 1 to go up.
```

## Reading a binary number

To read a binary number, write each place's worth over its digit, right to left from 1, and add the places that hold
a 1. Leibniz gave this example:

```quote leibniz-1703 p. 224
1101 ou 13 est la somme de huit, quatre et un.
```

"1101, or 13, is the sum of eight, four and one." Over 1101 the places are 8, 4, 2 and 1. The 1s sit under 8, 4 and 1,
and $8 + 4 + 1 = 13$.

Another: 10110. Five digits, so the places are 16, 8, 4, 2, 1. The 1s sit under 16, 4 and 2, and $16 + 4 + 2 = 22$.

```item BN1B
prompt: What is the binary number 11010 in our ten symbols?
topics: binary-to-decimal
answer: text
calculator: no
slip: BN1BA | the places read from the left | The ones place is on the right, as it is in tens. Over 11010 the places are 16, 8, 4, 2, 1 from the left.
slip: BN1BB | the digits typed again | That is 11010 again, read as a number in tens. Add up the worth of the places that hold a 1.
```

## Writing a number in binary

Going the other way, start from the largest place that fits. For 37: the places are 1, 2, 4, 8, 16, 32, and 64 is too
big. 32 fits, and leaves 5. 16 does not fit in 5, nor does 8. 4 fits, and leaves 1. 2 does not fit; 1 does. Write a 1
for each place you used and a 0 for each you skipped, largest first:

| 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 1 | 0 | 1 |

So 37 is 100101 in binary. Check it by reading it back: $32 + 4 + 1 = 37$.

```item BN1C
prompt: Write 44 in binary.
topics: decimal-to-binary
answer: text
calculator: no
slip: BN1CA | written smallest place first | The largest place is written first, on the left, as in tens: 44 starts with the 32.
slip: BN1CB | each digit converted on its own | 44 is forty-four, not a 4 and a 4. Find the largest place that fits in 44 and work down.
```

## Adding with no tables

To add in tens you had to learn tables by heart: that 6 and 7 make 13. Leibniz pointed out that binary needs none:

```quote leibniz-1703 p. 225
On n’a point besoin non plus de rien apprendre par coeur ici, comme il faut faire dans le calcul ordinaire, où il
faut, savoir, par exemple, que 6 et 7 pris ensemble font 13
```

"Nor is there any need to learn anything by heart here, as there is in ordinary arithmetic, where one has to know,
for example, that 6 and 7 taken together make 13." All of binary addition is three facts: $0 + 0 = 0$, $0 + 1 = 1$,
and $1 + 1 = 10$, which is write 0 and carry 1. With a carry coming in, $1 + 1 + 1 = 11$: write 1 and carry 1.

Add 1011 and 110, column by column from the right, as you add in tens:

| | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|
| | | 1 | 0 | 1 | 1 |
| + | | 0 | 1 | 1 | 0 |
| = | 1 | 0 | 0 | 0 | 1 |

The ones: $1 + 0 = 1$. The twos: $1 + 1 = 10$, write 0 and carry 1. The fours: $0 + 1$ and the carry make 10, write 0
and carry 1. The eights: $1 + 0$ and the carry make 10 again, write 0 and carry 1 into the sixteens. So the sum is
10001. Check it in tens: 1011 is 11, 110 is 6, and 10001 is $16 + 1 = 17$.

```item BN1D
prompt: Add 1011 and 111 in binary.
topics: binary-addition
answer: text
calculator: no
slip: BN1DA | no carries | $1 + 1$ is 10 in binary: write the 0 and carry the 1 into the next place, then add it there.
```

## The columns repeat

Write the numbers 0 to 7 in binary with three digits each, zeros in front where a number is short: 000, 001, 010,
011, 100, 101, 110, 111. Read down each column. The ones column goes 0, 1, 0, 1, and repeats. The twos column goes
0, 0, 1, 1, and repeats.

```item BN1E
prompt: In the count from 000 to 111, what are the eight digits down the fours column, from the top? Type them in order.
topics: binary-columns
answer: text
calculator: no
slip: BN1EA | the twos column's block | That is the twos column, which changes every two numbers. The fours column changes every four.
```

Leibniz saw the same thing:

```quote leibniz-1703 p. 225
Dans la première colonne c’est 01, dans la seconde 0011, dans la troisième 00001111, dans la quatrième
0000000011111111, et ainsi de suite.
```

"In the first column it is 01, in the second 0011, in the third 00001111, in the fourth 0000000011111111, and so on."
Each column's block is twice as long as the one before, because each place is worth twice as much.

He did not ask anyone to give up counting in tens:

```quote leibniz-1703 p. 225
Cependant je ne recommande point cette manière de compter, pour la faire introduire à la place de la pratique
ordinaire par dix.
```

"Still, I do not recommend this way of counting to be brought in in place of the usual practice by tens." Binary
numbers are long. But he thought binary was the most basic arithmetic there is, and good for discovering things.
He also wrote that the ancient Chinese figures he called the figures of Fohy, built of whole and broken lines, read
as binary if a whole line is 1 and a broken one is 0. A French Jesuit in Beijing, Bouvet, had written to him about
them on 14 November 1701.

## Two values: Boole

A century and a half later, in 1854, George Boole, professor of mathematics at Queen's College, Cork, published *An
Investigation of the Laws of Thought*. He wrote logic, the rules of reasoning, as algebra. In his algebra a symbol
stands for a class of things, and a class taken together with itself is the same class, so his symbols obey the rule
$x \times x = x$. He noticed that only two numbers obey it: $0 \times 0 = 0$ and $1 \times 1 = 1$. So he proposed:

```quote boole-1854 ch. II, section 15
Let us conceive, then, of an Algebra in which the symbols x, y, z, etc. admit indifferently of the values 0 and 1,
and of these values alone.
```

An algebra with only 0 and 1 in it: the same two symbols as Leibniz's binary, though Boole meant something different
by them. Take each symbol as a statement, and 1 can stand for true and 0 for false, which is how Shannon's table
below reads them.

## Switches that add

In 1937 Claude Shannon, a graduate student in electrical engineering at MIT, finished a master's thesis, *A Symbolic
Analysis of Relay and Switching Circuits*. He showed that circuits of switches and relays follow the same algebra as
Boole's logic, since a switch, like Boole's symbols, has only two states. His table of the match reads 1 as a true
statement (and a circuit open) and 0 as a false one (a circuit closed). Near the end he designed a circuit of relays
to add two numbers, and he chose binary for it:

```quote shannon-1937 p. 59
Although any numbering base could be used the circuit is greatly simplified by using the scale of two.
```

Each column of a binary sum follows one small rule, and Shannon wrote it out for his relays. Take one column with
digits a and b. The sum digit is 1 when exactly one of a and b is 1. The carry is 1 when both are. A table with a row
for every pair of digits holds the whole rule.

```item BN1F
prompt: Fill in the table for one column of a binary sum: for each pair of digits a and b, the sum digit and the carry.
topics: half-adder-table
answer: table
calculator: no
table: a | b | sum digit | carry
row: 0 | 0 | ? | ?
row: 0 | 1 | ? | ?
row: 1 | 0 | ? | ?
row: 1 | 1 | ? | ?
slip: BN1FA | the sum digit 1 for 1 + 1 | $1 + 1 = 10$: the sum digit is the 0, and the 1 is carried to the next column.
slip: BN1FB | the sum digit and the carry swapped | The sum digit is the right-hand digit of $a + b$, and the carry is the left-hand one.
```

That table is all of binary addition for one column. Pass each column's carry to the next one along and the same rule
adds numbers of any length, which is what Shannon's relay circuit was designed to do.

## Sources

- Leibniz, *Explication de l'arithmétique binaire* (1703), in C. I. Gerhardt (ed.), *Leibnizens mathematische
  Schriften*, vol. 7 (1863), pp. 223 to 227, read on
  [French Wikisource](https://fr.wikisource.org/wiki/Leibniz-en.francais-Gerhardt.Math.1a7.djvu/Num%C3%A9ration.binaire).
- George Boole, *An Investigation of the Laws of Thought* (1854), chapter II, read in
  [Project Gutenberg's text](https://archive.org/details/aninvestigationo15114gut).
- Claude Elwood Shannon, *A Symbolic Analysis of Relay and Switching Circuits*, a thesis for the Master of Science at
  MIT, signed 10 August 1937 (the degree is dated 1940), read in [MIT's copy](http://hdl.handle.net/1721.1/11173).
