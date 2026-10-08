# poly-04 evidence

## Expected values (2026-10-07, core 7c96617)

The oracle is build/proto/poly04.py: Python's complex arithmetic on Gaussian integers (exact here),
asserting i² = -1, (4i)² = -16, (6i)² = -36, each root from the formula, and each root a zero of its
polynomial, before the vectors run.

| Vector | What | Exact |
|---|---|---|
| C01A, C01 | i typed (0i1_), then i × i | -1 + 0i |
| C02 | 4i × 4i | -16 + 0i |
| V01, V02 | √x and x² of a complex number | INVALID DATA |
| R01, R02 | (-2 ± 4i) / 2 | -1 + 2i, -1 - 2i |
| H01 | -1 + 2i in x² + 2x + 5 by Horner | 0 + 0i |
| H02A, H02 | -1 - 2i typed (-1i-2_), then Horner | 0 + 0i |
| E01-E03 | x² - 4x + 13: (4 ± 6i) / 2; 2 + 3i by Horner | 2 + 3i, 2 - 3i, 0 + 0i |

All exact on the core at 7c96617, in 33s and 35s modes.

## Sources and probes

- Complex numbers on the stack: abacus-firmware unit 009 (the 35s guide ch.9); the vector token CI
  is the i between the parts; CMPLX is blue above +/− (keymap.c, key 20), its first soft key i.
- Probed first (keyrun --sequence, 7c96617): typing shows 0i1_ and -1i-2_ (+/− before the i acts on
  the real part, after it on the imaginary part); √x and x² of a complex number give INVALID DATA;
  (-16 i 0)^0.5 by yˣ gives 3.875E-44 i 4, inside unit 009's accuracy rule but left out of the lesson
  (abacus #4503 agrees: it teaches the wrong thing at that point).
- The harness: keyrun now prints a complex stack level as its two exact parts joined by "i", and
  check.py's in-order comparison takes both parts (a real never passes for a complex, nor the
  reverse); falsified on nine hand cases before use.

## Non-author read (2026-10-07)

Eight findings, all taken. The largest: the display puts the i between the parts, the reverse of
the written 2i, so -1.0000i2.0000 reads as "-1i, then 2"; the lesson now says plainly that the number
before the i is the real part and the one after it the imaginary part, with the entry 0i1_ quoted.
Also: "+/− after the i" pointed at the wrong example; now +/− before the i (real part) and after it
(imaginary part) are each shown, with the entry -1i-2_ quoted. The conjugate-pair reason was a
quadratic's, stated for every polynomial; now the quadratic's reason is given and the general fact
is marked as needing more. √(−d) = √d × i stated as a rule, with √x and x² refusing a complex number
shown (V01, V02, INVALID DATA). 4i keyed as 0 i 4 said again; CMPLX described as a menu like MODE;
"a real number times i", "imaginary part", and the triple-root clause.

## Checks

`make check`: 13/13 vectors in 33s and 35s, from a fresh and a used core; 14 keys blocks; 13 quotes.
Controls: a root's imaginary part quoted with the wrong sign, -b typed without ENTER, the conjugate
typed without the second +/−; all red.

## Abacus's accuracy read (#4509, 2026-10-07)

Accepted at 49857fe (20/20 in order, 20 controls sets red). Values confirmed. (1), (2) the display
reads real, i, imaginary, and +/− applies to the part being typed. (3) Faithful: the 35s guide's
"Functions for One Complex Number" (p.9-2) has no x² or √x; powers go through yˣ (p.9-3). (4) the
conjugate pair from the formula's ±√, the general fact needing more. (5) the fundamental theorem of
algebra with multiplicity. Optional note taken: typing a complex number with CMPLX i is the STU-32's
own (from the 35s); an HP 33s keeps complex numbers as pairs, so a one-sentence aside now says so.

## Repin to 7776c7c (2026-10-07): firmware 041, 33s mode as a 33s

041 (decision 58) hides CMPLX's i in 33s mode, as on an HP 33s. At the repin poly-04's vectors failed
in 33s mode alone (C01A onward: the i not typed), as the watch predicted, and passed in 35s and STU.
So the lesson offers `modes: 35s STU`, with a modes_reason; its topics are tagged @35s,STU in TOPICS;
the sentence that said typing with i works "in every mode" now says it is the 35s's way and STU's,
and why 33s mode is not offered. Two controls moved from 33s mode to 35s mode. A 33s version, with
the 33s's pairs, is to come.

## The 33s version (2026-10-07, core c7ab388): firmware 039's pairs

poly-04 is offered in all three modes again. In 33s mode, as on an HP 33s, a complex number is a pair
(imaginary in Y, real in X, typed imaginary ENTER real), and CMPLX before +, −, ×, ÷ works on the pair
in Z and T and the pair in Y and X (work/039-33s-cmplx-pairs.md and its vectors read for the layout).
Every block has a mode=33s variant, vectors ID@33s, and its own display vectors D-ID@33s (the real part
on the X line), for which check.py now looks before D-ID. The √x and x² refusals are a 35s,STU-only
section: 33s mode has no complex values to refuse. Horner's keys need a complex number in every level,
which pairs cannot give, so the 33s check is term by term: z × z with CMPLX ×, then + 2z (worked in the
head) with CMPLX +, then + c as a pair. The oracle asserts each term in exact Gaussian arithmetic; the
stacks were traced by hand before the vectors ran, and 11/11 pair vectors (22 expectations) passed first
time. Controls added: a pair typed real part first; the imaginary part quoted as the X line.

A non-author read of the 33s path traced every block by hand and agreed with every vector. Taken: "CMPLX
has no square root among its operations" (039 lists yˣ) became "there is no complex square root key";
the ENTER between two pairs named in the prose wherever the keys have it; why a result pair moves up to
Z and T when a pair is typed (rpn-01's lift, two numbers); that CMPLX keeps the first number in Z and T,
and that CMPLX ÷ divides the first by the second; a picture of the four levels; H02A's Y named; 2z and
−4z said to be worked in the head; √(−d) = √d × i stated as the chosen root of two (shared text); "of
degree 1 or more" (shared text).

## Abacus's read of the 33s version (#4975, 2026-10-07)

Accepted at 0c1f1a1, the 33s path rechecked by hand; the pair order matches 039; CMPLX ÷ and "no complex
square root key" true of 33s mode (a √ can still be had as CMPLX yˣ with 0.5, so the lesson does not say it
cannot be computed); √(−d) as the principal root true. One change, made: "exactly n roots" is true only
counted with multiplicity, so it now says "when a root that repeats is counted as many times as it
repeats" (as CAS 005 will print MULT 2).
