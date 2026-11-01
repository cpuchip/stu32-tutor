# Astronomy with the STU-32 (PROPOSED: two courses on one graph)

**Status:** the proposal for step (1) of the astronomy work (abacus #12142, from Michael's ask of 2026-11-01: "add an
astronomy course (or 2?) To our learn site that teaching the physics and the practice of astronomy"), revised on
abacus's review of a359e05 (#12172: abacus's own pass, then a fresh reader's, which web-checked the sources it
questioned) and astrometrics's corrections and calls (#12175). Not ruled. astrometrics is the subject lead and writes each unit's binding question, content and sources;
tutor writes the format, the calculator keys and the prerequisites; abacus checks every number and formula; primer
builds the site. Nothing here is published to learn before Michael's card.

**What may come in** (the repo is PUBLIC, CC BY-SA 4.0): new text, and text already published on
astrometrics.cpuchip.net (CC BY 4.0, attributed where used). Nothing from private drafts. A claim from the stories
comes one at a time, with its source. Primary works are cited by author, title and year. OpenStax Astronomy 2e is
CC BY-NC-SA 4.0 (its preface, fetched 2026-11-01; astrometrics #12158), which cannot go into a CC BY-SA repo: it is a
link for further reading, chapter by chapter, and no text, figure or problem is copied or adapted from it. More on
sources below, under "Sources and links".

## Two courses, and why

Two, because they start in different places and lead to the same sky. The physics needs logarithms, powers of ten
and the angle functions. The practice needs a hand, a clock and patience, and it is the way in for a reader who has
not reached algebra. As one course, either the beginner meets logarithms in the first week or the physics waits
behind observing it does not need. On one graph they meet: B's hand angles come before A's parallax, and B's light
curve before A's ladder. Both link to the same stories, so a learner can cross from what they did to how it was
first understood. (astrometrics)

- **A. Astronomy: how we know.** The physics: how a distance, a brightness, a mass, a temperature and a speed are
  each worked out from light and angles, and how sure each answer is. The calculator is used throughout: powers of
  ten, logarithms, roots and the angle functions. Entry is RPN (as algebra-to-calculus), and the course file names
  algebra-to-calculus as its prerequisite (below).
- **B. Astronomy: the practice.** Observing: safely; finding your way on the sky, measuring with your hand, timing,
  judging brightness by eye, and keeping a log. Lighter mathematics,
  entering after pre-algebra's written units. Algebraic entry first, RPN offered (as pre-algebra and geometry).

One graph: both courses' lessons use lessons/TOPICS, and a lesson may be listed in both course files (graph.py
refuses a lesson listed twice in one course, not across two), so a lesson both need is written once.

## The calculator's part

- **Already taught, required by topic where used:** scientific notation and E (rpn-03: read-e, type-e, sci; num-04:
  neg-e, e-arithmetic), squares, powers and roots (num-01: x-squared; num-03: square-root, power, xroot,
  neg-frac-powers, ten-to-x), logarithms (exp-03: log, base 10), the angle unit and the angle functions (trig-01:
  angle-unit, sin-key, convert-angle, arc-length; trig-02: trig-ratios, inverse-trig), formulas solved for any letter
  (eq-02: solve-prompts, solve-any-letter), programs (fn-01), and a line through data (lin-02: sigma-plus,
  regression). All of these are in algebra-to-calculus, so only A can require them.
- **Not yet taught: hours, minutes and seconds, and degrees, arcminutes and arcseconds.** The core has →HMS and HMS→
  (AB_HMS and AB_HMSINV in the firmware's core/calc.h at 1a12ecf), and no lesson uses them. Right ascension, time and
  parallax all need them. **One new lesson, hms-01 (tutor writes it, astrometrics supplies the sky examples: a
  star's RA from the page's lab, Bessel's arcseconds), listed in both courses:** in A's unit 1 before
  parallax, and in B's unit 2 before right ascension. It is written for both entries, algebraic and RPN, as frac-01
  is. Measured with keyrun at 1a12ecf (2026-11-01), the same in 33s, 35s and STU, as BLUE ANGLE →HMS and BLUE ANGLE
  HMS→:
  - 1.5 →HMS gives 1.3000, and 2.3045 HMS→ gives 2.5125.
  - 23.56 HMS→ 15 × gives 359.0000. That is only a key check: 23h56m at 15° an hour, the Sun's rate, is 359°. In a
    sidereal day (23h56m04s) the stars turn the full 360°, which is why they rise about 4 minutes earlier each night
    (B3).
  - 360 ÷ 25800 →HMS gives 0.0050 (50 arcseconds a year).
  - 0.00003 HMS→ (0.3 arcseconds) is 8.33 × 10⁻⁵, which FIX 4 shows as 0.0001, so parallax works in SCI (rpn-03's sci
    topic).

## A. Astronomy: how we know

| # | Unit | Binding question (astrometrics) | On the STU-32 | Requires (topics, by lesson) | Stories and sources (astrometrics; corrections from abacus #12172) |
|---|---|---|---|---|---|
| A1 | Angles and parallax | How can two angles, measured six months apart, tell us how far away a star is? | hms-01, then arcseconds to degrees; d = 1 ÷ p, with p in arcseconds and p half the six-month shift; parsecs and light-years; a measurement with its ± and the distance's range | trig-01 angle-unit, sin-key; trig-02 trig-ratios; rpn-03 type-e, sci; hms-01's topic | distance: Bessel on 61 Cygni (MNRAS, 1838); Struve on Vega (Mensurae Micrometricae, 1837, reprinted in the Source Book; measures from 1835 to 1838); Henderson on Alpha Centauri (MNRAS, read 11 January 1839); Dyson's 1913 paper (MNRAS 73), where Turner's word parsec is printed; the Hipparcos Catalogue (1997); Gaia DR1 and DR2 (2016, 2018). measure: the degree and Tycho's arcminute; Gaia DR3 (13 June 2022), the current catalog. (abacus's 1840 revision of Struve stays out until a lesson cites a source for it.) OpenStax ch. 19. |
| A2 | Light: the inverse square and magnitudes | If a star looks faint, is it far away or truly dim, and how can we tell? | the inverse square of a distance; m₁ − m₂ = −2.5 log₁₀(F₁ ÷ F₂); Pogson's 100^(1/5); absolute magnitude M and the distance modulus, m − M = 5 log₁₀ d − 5 (d in parsecs, dust ignored), here and not left to A6 | A1's topics; num-03 power, xroot, ten-to-x; exp-03 log; num-04 e-arithmetic | measure: Ptolemy's catalogue (Peters and Knobel, 1915); Pogson, MNRAS 17 (1856). dark: Olbers, On the Transparency of Space (1823). OpenStax ch. 17, 19. |
| A3 | Gravity and orbits | How can we weigh a star we will never touch? | Kepler's third law with the masses, (M₁ + M₂)P² = a³ (a in AU, P in years, masses in Suns); for a visual binary a = α ÷ p (α the angular semi-major axis, in arcseconds); Newton's form with G in powers of ten | A1's topics; num-03 power, neg-frac-powers; eq-02 solve-any-letter; rpn-03 type-e | gravity: Newton, Principia (1687); Halley's return predicted and seen (1758); Le Verrier and Galle, Neptune (Comptes rendus 23, 1846). sirius-b: Bessel predicted the companion (1844); Alvan G. Clark found it on 31 January 1862; G. P. Bond measured and announced it (On the Companion of Sirius, 1862); H. E. Bond et al., ApJ 840 (2017), both masses from the orbit. algol: Kolbas et al. (2015), three stars weighed. The Sirius plate lab says that a separation read off a plate is projected, not the semi-major axis. OpenStax ch. 3, 18. |
| A4 | Light as a thermometer | How can a star's color tell us its temperature, and with its brightness, its size? | Wien's law, λ_max T = b with b = 2.898 × 10⁻³ m·K; L = 4πR²σT⁴, and a radius from L and T | num-01 x-squared; num-03 power, square-root; eq-02 solve-any-letter; rpn-03 type-e | sun: W. Herschel, Phil. Trans. 90 (1800), the invisible rays. dark: Planck's Nobel lecture (1920); Mather and Smoot's Nobel lectures (2006), brief quotes only. sirius-b: Adams, PASP 27 (1915), white yet faint, so small. OpenStax ch. 5, 17. |
| A5 | Spectra and Doppler | How can a line in a spectrum tell us what a star is made of, and how fast it moves? | v = c Δλ ÷ λ, for v much less than c, giving only the speed along the line of sight; gravitational redshift taught apart, as a shift that is not a motion | num-04 e-arithmetic; frac-01 fraction-is-division | sun: Fraunhofer's memoirs (1817, 1823); Kirchhoff (1860; 1861); Huggins and Miller, Phil. Trans. 154 (1864); Payne, Stellar Atmospheres (1925). algol: Vogel's Algol orbit (1889). cepheids: Bélopolsky (1895). sirius-b, framed apart from Doppler as gravitational redshift: Adams, PNAS 11 (1925), whose shift was badly low, with scattered light from Sirius A blamed, and Joyce et al. (2018): a how-we-know story of a first measurement corrected. Settled from the sources (astrometrics #12181): Adams gives +21 km/s (+0.32 angstrom), Joyce et al. quote him as 23 and measure 80.65 ± 0.77 km/s, and call the early values "in error by nearly a factor of four"; no source gives the 19 in abacus's review. The lesson quotes +21 and 80.65 and has the learner divide them on the STU-32 (3.84). OpenStax ch. 5, 17. |
| A6 | The distance ladder | How far away is a galaxy, and how fast is the universe expanding? | A2's distance modulus, used; a period-luminosity line; v = H₀d, a line through the origin: either fitted through 0, or lin-02's fit with its intercept taught as the check (decided when the summation keys are measured); Hubble's 1929 slope of about 500 km/s/Mpc against about 70 today, kept as a lesson | A2's topics; exp-03 log; lin-02 sigma-plus, regression | distance: Leavitt, Harvard Circular 173 (1912); Shapley and Curtis, The Scale of the Universe (1921); Hubble, Cepheids in Spiral Nebulae (1925). dark: Lemaître (1927); Hubble, PNAS 15 (1929). Slipher's redshifts and the IAU's 2018 name, the Hubble–Lemaître law, come in when a source for each is added (abacus #12172). cepheids: Freedman et al., the Key Project (2001); Riess et al. (2022) and Planck 2018, the tension. OpenStax ch. 19, 26, 29. |

**Uncertainty, through all of A** (abacus #12172: how we know is half a story without it). From A1 on, a measurement
carries its ±, and the lesson works out the range of the answer: a parallax of 0.30 ± 0.01 arcseconds puts the star
between 1 ÷ 0.31 and 1 ÷ 0.29 parsecs, 3.2 to 3.4. Each later unit does the same for its own result. The stories
carry ready cases (astrometrics #12175): Tycho's arcminute to Gaia's microarcseconds (measure), and Hipparcos's
Pleiades distance, wrong by about 10 percent and settled by radio and Gaia (pleiades).

The stories are linked as https://astrometrics.cpuchip.net/?thread=<id>, one thread per link, cited once per
lesson; astrometrics is adding a stable beat link (`&beat=<beat id>`) so a lesson can open the exact finding
(#12159). OpenStax chapters are further reading only. Every source here is astrometrics's to verify and abacus's to
check; none is quoted in a lesson until it has been read.

## B. Astronomy: the practice

| # | Unit | Binding question (astrometrics) | On the STU-32 | Requires (topics, by lesson) | Stories and tools (astrometrics; corrections from abacus #12172) |
|---|---|---|---|---|---|
| B0 | Before you go out | (astrometrics; tutor's draft: How do you watch the sky safely, and see the most of it?) | never look at the Sun, by eye or through any instrument, without a proper solar filter; dark adaptation; light pollution | | measure: the limit tool (the faintest stars from a city to a dark sky). |
| B1 | The sky as a sphere, and angles with your hand | With nothing but your hand, how do you say where something is on the sky? | degrees of a turn; a width at arm's length as an angle | angle-01 degrees (angle-01 listed in B) | measure: the ruler tool (a hand at arm's length, drawn on the sky); the Babylonian degree. OpenStax ch. 2. |
| B2 | Finding stars: alt-az and RA/Dec | How do you tell someone else exactly where to look? | hms-01; hours of right ascension to degrees (× 15) | angle-01 degrees; whole-02; hms-01's topic | measure: the grid tool (RA/Dec and alt-az, turning with the stars); Tycho's arcminute; Gascoigne's micrometer (1640). The page's lab (the magnifier): find a star by name, constellation or HR number. OpenStax ch. 2. |
| B3 | Time, the sky's motion and precession | Why does the sky turn every night, and why are the stars no longer where Hipparchus left them? | a sidereal day and a solar day, and the stars' 4 minutes a night; degrees per year from a long cycle | hms-01's topic; frac-01 fraction-is-division | measure: Hipparchus's precession (as Ptolemy preserves it); Flamsteed, at Greenwich from July 1676 (catalog published 1725); the precession dial. OpenStax ch. 4. |
| B4 | Brightness by eye | How bright is that star by eye, and what does a magnitude mean? | a magnitude step as a ratio of about 2.5, multiplied step by step (no logarithms, no yˣ: num-03 is in algebra-to-calculus, so B cannot require it) | whole-02 | measure: Ptolemy's magnitudes; Pogson (1856); the limit tool. OpenStax ch. 17. |
| B5 | Variable stars and a light curve of your own | Can you catch a star changing, and time it? | a period from timed minima, in hours and minutes; an average | whole-01, whole-02; hms-01's topic; decimals (tension 1) | algol: Goodricke, Phil. Trans. (1783), his own timings; Pickering's table (1880); the light-curve tool. cepheids: Pigott, Phil. Trans. 75 (1785), and Goodricke (1786), by eye against comparison stars. |
| B6 | An observing log | What must you write down so another observer can check what you saw? | the date, time, position and estimate, with how sure you are, written so another observer could check them | | cepheids: Pigott's letter quoting Goodricke's journal (1785). algol: Palitch, a farmer of Prolitz near Dresden (Phil. Trans., 1784), whose observations the Count de Bruhl sent to the Royal Society; Palitzsch is the modern spelling. That he is the farmer who first saw Halley's comet return (1758, A3's story) is plausible but not in our sources, so a lesson says it only with a source that does. |

**Later units, not in v1** (abacus #12172's gaps; astrometrics's calls, #12175): binoculars and telescopes (the measure
story's Airy-disk beat is a start); the Moon's phases, with the seasons and eclipses; the Hertzsprung–Russell
diagram; how the astronomical unit was measured (measure: astronomical-unit-fixed, 2012); exoplanet transits. They go
on the card by name.

## Conditions a lesson must state (abacus #12172)

- d = 1 ÷ p holds with p in arcseconds, and p is half the six-month shift.
- Wien's law uses the wavelength of the peak, λ_max, with b = 2.898 × 10⁻³ m·K.
- The Doppler formula holds for speeds much less than light's, and gives only the speed along the line of sight.
- The distance modulus gives parsecs and ignores dust.
- Every log is base 10.

## Sources and links (abacus #12172)

- **The link gate** (each link answers 200 with no credentials) fails on paywalled journal hosts, so a journal paper
  is linked through NASA ADS or an open archive (the Royal Society's, the Biodiversity Heritage Library, Gallica),
  and the allowlist names those hosts and not the journals'.
- **Plates:** a licence is recorded for every plate a lab uses.
- **Nobel lectures** are © the Nobel Foundation: brief quotes only.
- **Journal figures** are not copied; their numbers are quoted with the source.

## Tensions to settle before writing

1. **B's entry, and decimals.** Pre-algebra's units 6 to 10 (decimals, ratio, percent, proportion) are not written
   yet, so B cannot require them by topic. B5's timings and averages need decimals, and so do B2's and B3's hours.
   Either B teaches the little it needs in place, or those units wait for pre-algebra's unit 6.
2. **Prerequisite courses, measured in graph.py.** A lesson's required topic must be taught earlier in its own
   course or in a prerequisite course, or graph.py refuses it ("which is neither earlier..."). So A's course file
   names `prerequisite | algebra-to-calculus` (the whole course, though A uses a handful of its lessons), and B's
   names `prerequisite | pre-algebra` and lists angle-01 itself rather than requiring all of geometry. A prerequisite
   smaller than a course would be a graph.py change; that is primer's and abacus's call.
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
2. **Links out.** A link to astrometrics.cpuchip.net (`?thread=<id>`), openstax.org, NASA ADS or an open archive is
   cited the way a lesson link is: once per lesson. The allowed hosts live in one file in this repo, read by
   check.py (a host not on it is refused) and by primer's learn gate (each link answers 200, with no credentials).
   A link into a private repo is refused by both.
3. **An interactive in a lesson.** A new fenced block, `widget <name>`, with its parameters as `key: value` lines,
   which primer's page draws (Michael's rule: a problem that makes a 3D shape gets 3D controls). check.py checks the
   name against the widgets primer has built, and every number the lesson quotes from a widget against a vector or a
   stated figure. primer's own oracle checks that the widget shows those numbers. Candidates: the celestial sphere
   (B1, B3, 3D), parallax (A1, 3D), an orbit (A3, 2D). astrometrics's own tools stay on
   the sky page, linked and not copied.

None of the three is built before the card. Each comes with its controls when the first lesson needs it.

## Before writing: one pilot each

Unit 1 of each course, written and measured at 1a12ecf, then abacus's check, then a card to Michael with the
outline and the two pilots (abacus #12142, order (2) and (3)). A's pilot is hms-01 and A1's parallax lesson; B's
is B0 and B1, safety and hand angles.

## Questions for Michael (through abacus)

1. Two courses as proposed? And which comes first: B (more readers can start) or A (the physics he asked about
   first)? (astrometrics)
2. His plate labs (A1, A3): tools on astrometrics.cpuchip.net with real archival plates where the licence allows,
   else plates simulated from the catalog and labeled so, each linked from its unit. Go? (astrometrics)
3. The home page: a subject heading (Mathematics, Astronomy) and a new lede in place of "Mathematics on the
   STU-32, course by course" (primer #12155). The words are his to approve.
4. B's entry: B teaches the few decimals it needs in place, rather than waiting for pre-algebra's units 6 to 10?
5. Not in v1, named for later: binoculars and telescopes; the Moon's phases, seasons and eclipses; the HR diagram;
   how the AU was measured; exoplanet transits.
