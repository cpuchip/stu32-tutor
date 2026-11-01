# Astronomy with the STU-32 (PROPOSED: two courses on one graph)

**Status:** a skeleton for step (1) of the astronomy work (abacus #12142, from Michael's ask of 2026-11-01: "add an
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

<!-- astrometrics: the case for two courses, in a paragraph. -->

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
  and parallax all need them, so a new topic is needed early in both courses. Their keys and screens in each mode
  get measured with keyrun before any prose.

## A. Astronomy: how we know

| # | Unit | Binding question (astrometrics) | On the STU-32 | Requires (topics, by lesson) | Stories and sources (astrometrics) |
|---|---|---|---|---|---|
| A1 | Angles and parallax | | arcseconds to degrees (HMS→, or ÷ 3600); d = 1 ÷ p in parsecs; a small angle's tangent | trig-01 angle-unit, sin-key; trig-02 trig-ratios; rpn-03 type-e; the new HMS topic | |
| A2 | Light: the inverse square and magnitudes | | the inverse square of a distance; m₁ − m₂ = −2.5 log(F₁ ÷ F₂); Pogson's 100^(1/5) | num-03 power, xroot; exp-03 log; num-04 e-arithmetic | |
| A3 | Gravity and orbits | | P² = a³ (years, AU, solar masses); Newton's form with G in powers of ten; a mass from an orbit | num-03 power, neg-frac-powers; eq-02 solve-any-letter; rpn-03 type-e | |
| A4 | Light as a thermometer | | Wien's λT = b; L = 4πR²σT⁴, and a radius from L and T | num-01 x-squared; num-03 power, square-root; eq-02 solve-any-letter | |
| A5 | Spectra and Doppler | | v = c Δλ ÷ λ; a shift as a fraction of the wavelength | num-04 e-arithmetic; frac-01 fraction-is-division | |
| A6 | The distance ladder | | the distance modulus d = 10^((m − M + 5) ÷ 5); a period-luminosity line; Hubble's v = H₀d as a line through data | exp-03 log; lin-02 sigma-plus, regression | |

## B. Astronomy: the practice

| # | Unit | Binding question (astrometrics) | On the STU-32 | Requires (topics, by lesson) | Stories and tools (astrometrics) |
|---|---|---|---|---|---|
| B1 | The sky as a sphere, and angles with your hand | | degrees of a turn; a width at arm's length as an angle | angle-01 degrees | |
| B2 | Finding stars: alt-az and RA/Dec | | hours to degrees (× 15); the new HMS topic | angle-01 degrees; whole-02 | |
| B3 | Time, the sky's motion and precession | | a sidereal day; degrees per year from a long cycle | the new HMS topic; frac-01 fraction-is-division | |
| B4 | Brightness by eye | | a magnitude step as a ratio, without logarithms | num-03 power (or a table, if B comes before num-03) | |
| B5 | Variable stars and a light curve of your own | | a period from timed minima; an average | whole-01, whole-02 | |
| B6 | An observing log | | the date, time, position and estimate, written so another observer could check them | | |

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

<!-- after astrometrics's sections are in -->
