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
