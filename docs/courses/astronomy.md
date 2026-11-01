# Astronomy with the STU-32 (PROPOSED: two courses on one graph)

**Status:** the proposal for step (1) of the astronomy work, with astrometrics's sections placed (#12159), for abacus's
fresh reader (abacus #12142, from Michael's ask of 2026-11-01: "add an
astronomy course (or 2?) To our learn site that teaching the physics and the practice of astronomy"). Not ruled.
astrometrics is the subject lead and writes each unit's binding question, content and sources; tutor writes the
format, the calculator keys and the prerequisites; abacus checks every number and formula; primer builds the site.
Nothing here is published to learn before abacus's review and Michael's card.

**What may come in** (the repo is PUBLIC, CC BY-SA 4.0): new text, and text already published on
astrometrics.cpuchip.net (CC BY 4.0, attributed where used). Nothing from private drafts. A claim from the stories
comes one at a time, with its source. Primary works are cited by author, title and year. OpenStax Astronomy 2e is
CC BY-NC-SA 4.0 (its preface, fetched 2026-11-01; astrometrics #12158), which cannot go into a CC BY-SA repo: it is a
link for further reading, chapter by chapter, and no text, figure or problem is copied or adapted from it.

## Two courses, and why

Two, because they start in different places and lead to the same sky. The physics needs logarithms, powers of ten
and the angle functions. The practice needs a hand, a clock and patience, and it is the way in for a reader who has
not reached algebra. As one course, either the beginner meets logarithms in the first week or the physics waits
behind observing it does not need. On one graph they meet: B's hand angles come before A's parallax, and B's light
curve before A's ladder. Both link to the same stories, so a learner can cross from what they did to how it was
first understood. (astrometrics)

- **A. Astronomy: how we know.** The physics: how a distance, a brightness, a mass, a temperature and a speed are
  each worked out from light and angles. The calculator is used throughout: powers of ten, logarithms, roots and the
  angle functions. Entry is RPN (as algebra-to-calculus).
- **B. Astronomy: the practice.** Observing: finding your way on the sky, measuring with your hand, timing, judging
  brightness by eye, and keeping a log. Lighter mathematics, entering around pre-algebra. Algebraic entry first, RPN
  offered (as pre-algebra and geometry).

One graph: both courses' lessons use lessons/TOPICS, so a B lesson can feed an A lesson (B's hand angles before A's
parallax) without being repeated.

## The calculator's part

- **Already taught, required by topic where used:** scientific notation and E (rpn-03: read-e, type-e, sci; num-04:
  neg-e, e-arithmetic), powers and roots (num-03: power, xroot, neg-frac-powers), logarithms (exp-03: log), the angle
  unit and the angle functions (trig-01: angle-unit, sin-key, convert-angle, arc-length; trig-02: trig-ratios,
  inverse-trig), formulas solved for any letter (eq-02: solve-prompts, solve-any-letter), programs (fn-01), and a
  line through data (lin-02: sigma-plus, regression).
- **Not yet taught:** hours, minutes and seconds, and degrees, arcminutes and arcseconds. The core has →HMS and HMS→
  (AB_HMS and AB_HMSINV in the firmware's core/calc.h at 1a12ecf), but no lesson uses them. Right ascension, time
  and parallax all need them, so a new topic is needed early in both courses. Measured with keyrun at 1a12ecf
  (2026-11-01), the same in 33s, 35s and STU, as BLUE ANGLE →HMS and BLUE ANGLE HMS→: 1.5 →HMS gives 1.3000;
  2.3045 HMS→ gives 2.5125; 23.56 HMS→ 15 × gives 359.0000 (a sidereal day's turn, in degrees); 360 ÷ 25800 →HMS
  gives 0.0050 (50 arcseconds a year). 0.00003 HMS→ (0.3 arcseconds) is 8.33 × 10⁻⁵, which FIX 4 shows as 0.0001,
  so the parallax unit works in SCI (rpn-03's sci topic).

## A. Astronomy: how we know

| # | Unit | Binding question (astrometrics) | On the STU-32 | Requires (topics, by lesson) | Stories and sources (astrometrics) |
|---|---|---|---|---|---|
| A1 | Angles and parallax | How can two angles, measured six months apart, tell us how far away a star is? | arcseconds to degrees (HMS→, or ÷ 3600); d = 1 ÷ p in parsecs; a small angle's tangent | trig-01 angle-unit, sin-key; trig-02 trig-ratios; rpn-03 type-e; the new HMS topic | distance: Bessel on 61 Cygni (MNRAS, 1838); Henderson and Struve (1839); Dyson, the parsec (MNRAS 73, 1913); the Hipparcos Catalogue (1997); Gaia DR1 and DR2 (2016, 2018). measure: the degree and Tycho's arcminute. OpenStax ch. 19. |
| A2 | Light: the inverse square and magnitudes | If a star looks faint, is it far away or truly dim, and how can we tell? | the inverse square of a distance; m₁ − m₂ = −2.5 log(F₁ ÷ F₂); Pogson's 100^(1/5) | num-03 power, xroot; exp-03 log; num-04 e-arithmetic | measure: Ptolemy's catalogue (Peters and Knobel, 1915); Pogson, MNRAS 17 (1856). dark: Olbers, On the Transparency of Space (1823). OpenStax ch. 17, 19. |
| A3 | Gravity and orbits | How can we weigh a star we will never touch? | P² = a³ (years, AU, solar masses); Newton's form with G in powers of ten; a mass from an orbit | num-03 power, neg-frac-powers; eq-02 solve-any-letter; rpn-03 type-e | gravity: Newton, Principia (1687); Halley's return predicted and seen (1758); Le Verrier and Galle, Neptune (Comptes rendus 23, 1846). sirius-b: G. P. Bond, On the Companion of Sirius (1862); H. E. Bond et al., ApJ 840 (2017), both masses from the orbit. algol: Kolbas et al. (2015), three stars weighed. OpenStax ch. 3, 18. |
| A4 | Light as a thermometer | How can a star's color tell us its temperature, and with its brightness, its size? | Wien's λT = b; L = 4πR²σT⁴, and a radius from L and T | num-01 x-squared; num-03 power, square-root; eq-02 solve-any-letter | sun: W. Herschel, Phil. Trans. 90 (1800), the invisible rays. dark: Planck's Nobel lecture (1920); Mather and Smoot's Nobel lectures (2006). sirius-b: Adams, PASP 27 (1915), white yet faint, so small. OpenStax ch. 5, 17. |
| A5 | Spectra and Doppler | How can a line in a spectrum tell us what a star is made of, and how fast it moves? | v = c Δλ ÷ λ; a shift as a fraction of the wavelength | num-04 e-arithmetic; frac-01 fraction-is-division | sun: Fraunhofer's memoirs (1817, 1823); Kirchhoff (1860; 1861); Huggins and Miller, Phil. Trans. 154 (1864); Payne, Stellar Atmospheres (1925). algol: Vogel's Algol orbit (1889). cepheids: Bélopolsky (1895). sirius-b: Adams, PNAS 11 (1925) and Joyce et al. (2018), light climbing out of gravity. OpenStax ch. 5, 17. |
| A6 | The distance ladder | How far away is a galaxy, and how fast is the universe expanding? | the distance modulus d = 10^((m − M + 5) ÷ 5); a period-luminosity line; Hubble's v = H₀d as a line through data | exp-03 log; lin-02 sigma-plus, regression | distance: Leavitt, Harvard Circular 173 (1912); Shapley and Curtis, The Scale of the Universe (1921); Hubble, Cepheids in Spiral Nebulae (1925). dark: Hubble, PNAS 15 (1929). cepheids: Freedman et al., the Key Project (2001); Riess et al. (2022) and Planck 2018, the tension. OpenStax ch. 19, 26, 29. |

The stories are linked as https://astrometrics.cpuchip.net/?thread=<id>, one thread per link, cited once per
lesson; astrometrics is adding a stable beat link (`&beat=<beat id>`) so a lesson can open the exact finding
(#12159). OpenStax chapters are further reading only (see above). Every source here is astrometrics's to verify
and abacus's to check; none is quoted in a lesson until it has been read.

## B. Astronomy: the practice

| # | Unit | Binding question (astrometrics) | On the STU-32 | Requires (topics, by lesson) | Stories and tools (astrometrics) |
|---|---|---|---|---|---|
| B1 | The sky as a sphere, and angles with your hand | With nothing but your hand, how do you say where something is on the sky? | degrees of a turn; a width at arm's length as an angle | angle-01 degrees | measure: the ruler tool (a hand at arm's length, drawn on the sky); the Babylonian degree. OpenStax ch. 2. |
| B2 | Finding stars: alt-az and RA/Dec | How do you tell someone else exactly where to look? | hours to degrees (× 15); the new HMS topic | angle-01 degrees; whole-02 | measure: the grid tool (RA/Dec and alt-az, turning with the stars); Tycho's arcminute; Gascoigne's micrometer (1640). The page's lab (the magnifier): find a star by name, constellation or HR number. OpenStax ch. 2. |
| B3 | Time, the sky's motion and precession | Why does the sky turn every night, and why are the stars no longer where Hipparchus left them? | a sidereal day; degrees per year from a long cycle | the new HMS topic; frac-01 fraction-is-division | measure: Hipparchus's precession (as Ptolemy preserves it); Flamsteed's clock (1725); the precession dial. OpenStax ch. 4. |
| B4 | Brightness by eye | How bright is that star by eye, and what does a magnitude mean? | a magnitude step as a ratio, without logarithms | num-03 power (or a table, if B comes before num-03) | measure: Ptolemy's magnitudes; Pogson (1856); the limit tool (the faintest stars from a city to a dark sky). OpenStax ch. 17. |
| B5 | Variable stars and a light curve of your own | Can you catch a star changing, and time it? | a period from timed minima; an average | whole-01, whole-02 | algol: Goodricke, Phil. Trans. (1783), his own timings; Pickering's table (1880); the light-curve tool. cepheids: Pigott, Phil. Trans. 75 (1785), and Goodricke (1786), by eye against comparison stars. |
| B6 | An observing log | What must you write down so another observer can check what you saw? | the date, time, position and estimate, written so another observer could check them | | cepheids: Pigott's letter quoting Goodricke's journal (1785). algol: Palitch, a farmer, whose observations the Count de Bruhl sent to the Royal Society (1784). |

## Tensions to settle before writing

1. **B's entry.** Pre-algebra's units 6 to 10 (decimals, ratio, percent, proportion) are not written yet, so B
   cannot require them by topic. Either B uses only what pre-algebra has (whole numbers, integers, fractions,
   degrees from geometry's angle-01), or B teaches the little it needs in place.
2. **A course file can only require a whole course** (`prerequisite | algebra-to-calculus` would be all of it). A's
   real prerequisites are a handful of lessons, so they go lesson by lesson as topics, and the course file names
   none. (Or graph.py learns a course prerequisite smaller than a course; that is primer's and abacus's call.)
3. **Labs on photographic plates** (astrometrics #12147, from Michael: real work on the STU-32 with markers laid on a
   plate): Sirius B's separation over years with Kepler III (A3), a parallax from two plates six months apart (A1),
   Fomalhaut b's motion between two Hubble epochs. The tools would live on the sky page and the course would link to
   them; the lesson's own checks can only cover the calculator's part (the numbers read off the plate are given in
   the lesson).
4. **Real data and the vectors.** Every screen in a lesson is a vector checked at the pinned firmware, so a real
   measurement is quoted to the places the lesson shows, and the source's own figure stays in the prose with its
   citation.

## The site (primer #12155), and what the format adds

1. **A subject per course.** A `subject | astronomy` line after the `course |` line, one word from a fixed list in
   graph.py (`mathematics`, `astronomy`). A course file without it is mathematics, so no existing file changes.
   primer groups the home page by it. The home page's new heading and lede are site text, so they go on Michael's
   card.
2. **Links out.** A link to astrometrics.cpuchip.net (`?thread=<id>`), openstax.org or a primary source's host is
   cited the way a lesson link is: once per lesson. The allowed hosts live in one file in this repo, read by
   check.py (a host not on it is refused) and by primer's learn gate (each link answers 200, with no credentials).
   A link into a private repo is refused by both.
3. **An interactive in a lesson.** A new fenced block, `widget <name>`, with its parameters as `key: value` lines,
   which primer's page draws (Michael's rule: a problem that makes a 3D shape gets 3D controls). check.py checks the
   name against the widgets primer has built, and every number the lesson quotes from a widget against a vector or a
   stated figure. primer's own oracle checks that the widget shows those numbers. Candidates: the celestial sphere
   (B1, B3, 3D), parallax (A1, 3D), an orbit (A3, 2D). astrometrics's own tools stay on the sky page, linked and not
   copied.

None of the three is built before the card. Each comes with its controls when the first lesson needs it.

## Before writing: one pilot each

Unit 1 of each course, written and measured at 1a12ecf, then abacus's check, then a card to Michael with the
outline and the two pilots (abacus #12142, order (2) and (3)).

## Questions for Michael (through abacus)

1. Two courses as proposed? And which comes first: B (more readers can start) or A (the physics he asked about
   first)? (astrometrics)
2. His plate labs (A1, A3): tools on astrometrics.cpuchip.net with real archival plates where the licence allows,
   else plates simulated from the catalog and labeled so, each linked from its unit. Go? (astrometrics)
3. The home page: a subject heading (Mathematics, Astronomy) and a new lede in place of "Mathematics on the
   STU-32, course by course" (primer #12155). The words are his to approve.
4. B's entry: B uses only what pre-algebra has written so far (whole numbers, integers, fractions, and geometry's
   degrees), teaching the little else it needs in place, rather than waiting for pre-algebra's units 6 to 10?
