# Astronomy: the shape of a unit (PROPOSED)

**Status:** by tutor, astrometrics (the sky, the tools and the measurement) and primer (the widgets), for abacus's
review (#12366) before any unit 2 is written. abacus has answered its first questions (#12375); whether B may have
lessons without the calculator goes to Michael as a card, because it touches what the site says it is. The courses
themselves are docs/courses/astronomy.md; their four pilots are on main, accepted at 3b321c4.

**Why:** Michael's note on the astronomy-courses card (2026-11-01, via abacus #12366), verbatim: "This is good! And
ive looked at the demo I likr it. I think i do want the lessons to be more interactive, we have the star data and
charts and can walk through each lesson with animations and tools to help. I worry a bit that we are teaching to the
calculator though."

## The flow of a unit: sky → tool → measurement → calculator → check

1. **The sky** (astrometrics). A unit opens on a real object, in tonight's sky or in the sky of the finding it
   retells: a star, a cluster, a shower. The learner sees it before reading about it. The lesson links to
   astrometrics.cpuchip.net at the step of the story that tells the finding: `?thread=<story>&beat=<beat id>` opens
   the story there with the stars it names lit, and `&star=<HR number>` also opens that star's panel (its catalog
   brightness, color, Hipparcos distance, and the stories and ideas it appears in). Beat ids are stable, so a link
   holds when a story grows. A lesson can set the learner's sky with `&place=<a place id from the page's
   list>&date=<YYYY-MM-DD>`; without them the page shows New York City on the night of 15 to 16 November 2026. Every
   number the opening quotes comes from the catalog the page draws (the Yale Bright Star Catalogue, 5th revised
   edition, with Hipparcos distances) or from the story's own quoted source, so the lesson and the page agree.
2. **The tool.** The learner does something: turns the sphere, lays a hand across the sky, puts markers on a plate,
   reads a light curve. Either a widget in the lesson or one of astrometrics's tools, linked (below).
3. **The measurement.** A number the learner takes from the tool, with how sure it is: an angle, a time, a
   brightness. A widget's parameters set its starting state, and its `shows:` lines give the figures the lesson
   quotes from that state, so the number is one the checks can reproduce.
4. **The calculator.** The STU-32 does the work a measurement needs and a head cannot (the test is below).
5. **The check.** The answer against a catalog or a published figure, and the items: a learner who measured it and
   worked it out compares with what astronomers found.

## The tools, and which become widgets

**astrometrics's tools, each at a step of a story today** (astrometrics #12380):
- Hand ruler (little finger 1°, three middle fingers 5°, fist 10°, at arm's length): thread `measure`, beat
  `babylonian-degree`.
- Brightness limit (the faintest magnitude seen, from a city to a truly dark sky): `measure`, `ptolemy-magnitudes`.
- Grids, right ascension and declination or altitude and azimuth, turning with the stars: `measure`,
  `flamsteed-clock`.
- Precession dial (the grid redrawn for any year from 4001 BC to AD 16,000, the pole walking from Thuban to Polaris
  toward Vega): `measure`, `hipparchus-precession`.
- Eyepiece on Mizar, each era's measuring error drawn as a circle: `measure`, nine steps from `tycho-arcminute` on.
- Light curves (Goodricke's from his own words, Pickering's from his table, with a slider that dims Algol on the
  sky): `algol`, `algol-goodricke` and `algol-pickering`.
- 3D distance map (the bright stars at their Hipparcos distances): `distance`, four steps from `bessel-61-cygni`.
- A meteor shower from Olmsted's radiant (an ordinary year's rate as seen, the famous storms as labeled what-ifs):
  `leonids`, four steps from `olmsted-radiant`.
- Marked places no catalog star stands for (Tycho's star of 1572, the Crab, Cassiopeia A, the Leonid radiant), each
  from SIMBAD's coordinates as quoted: `new-stars`, `elements`, `leonids`.
- Spectroscope (measured spectra of the Sun and bright stars): `sun`, six steps.
- On every page: the lab (find a star by name, Bayer label, constellation or HR number, with filters), a star's
  panel, Run the night, star trails, and the place and night in the settings.
- Being built (the page's Calc station): the plate lab. Markers are laid on a plate (real archive plates where the
  licence allows, otherwise simulated from the catalog and labeled so), the separation is read off, and the
  arithmetic is worked on the STU-32.

The page's own tests hold each tool against astropy or its quoted source, and astrometrics can send those figures
per tool for a widget built on the same data.

**When a tool is a widget** (primer #12381). Only when the lesson needs it inline and quotes a number from it;
otherwise it is astrometrics's tool, linked from the step and not copied. A widget is one name in a `widget <name>`
block; its parameters set the starting state, and its `shows:` lines give the figures the lesson quotes. check.py
compares the prose with `shows:`, and primer's oracle checks that the page draws `shows:`: neither side trusts the
other. Each widget's oracle has (a) the page's function, exposed to the probe; (b) an independent computation in
primer's tools, sharing no code with the page; (c) named facts it must reproduce exactly; (d) a few thousand random
cases against (b); (e) the learner's readout equal to (b) for the starting state; (f) 390 px, light and dark, no
sideways scroll; (g) a planted wrong formula that must fail (c) and (d). abacus recomputes every `shows:` figure from
the catalog.

**Every widget names its epoch** (abacus #12384, #12387). The catalog's positions are J2000. A widget that takes a
sidereal time (the sphere prototype) draws them unprecessed, so its `shows:` says J2000; a widget that takes a date
precesses to it, and its oracle checks the precession against an independent formula. A lesson that quotes an
altitude or azimuth for a date either takes a precessed figure or says J2000 and rounds to what that supports
(precession since 2000 moves a star by up to about 0.4°, more than a little finger). Separations between two stars
barely move, so the hand-ruler's figures stand. astrometrics's page precesses its dome to the date (held against
astropy, worst of 324 named stars 0.0028°), draws its RA and Dec grid in J2000, and its star panel gives only "N
degrees up, toward the <compass>", rounded to whole degrees (astrometrics #12386; primer #12385).

**The first widgets:**
1. **sky-sphere** (the prototype Michael liked). Parameters: lat, lst, star (HR number), grids. Shows: alt, az, hour
   angle, and the star's RA and Dec as the grid reads them. Oracle: the vector rotation, 2,000 random cases and 4
   facts, a planted formula failing 1,783. Serves hms-01's new first step, B2 and B3.
2. **hand-ruler**, on the sphere: a fist, three fingers or a little finger laid between two stars. Shows: the
   catalog separation in degrees, and the hand marks it spans. Oracle: the great-circle separation two ways
   (haversine and vector dot), with the BSC5 figures as named facts: Dubhe–Merak 5.374, Castor–Pollux 4.505,
   Alnitak–Mintaka 2.736. Serves sky-02's new lead.
3. **star-field**, only if sky-01 needs it inline (else the limit tool, linked): the stars brighter than a limiting
   magnitude, with a slider from city to dark sky. Shows: the count at or above the limit. Oracle: the count from
   BSC5 directly, with the four Rate Your Night Sky limits as named states.
4. **Linked, not widgets yet:** the plate lab (for par-01), the light curves (B5), the eyepiece and the 3D distance
   map. Each becomes a widget only when a lesson must quote it inline, and then gets the same oracle.

## Where the calculator earns its place

A keys block belongs in an astronomy lesson when the step needs one of:
- a function the learner cannot do in their head: TAN, LOG, yˣ, ˣ√y, HMS→, 1/x of a small number;
- a constant or a chain too long to carry by hand without rounding (a parsec in light-years, from c and a Julian year);
- a number the tool measured, whose consequence is the point (Bessel's 0.3136 arcseconds to 657,732 AU).

It does not belong where the step is arithmetic a learner at that course's level does in their head (40 + 25, 7 − 2,
2 × 10). There the lesson says the sum in prose, or leaves it to the learner's head in an item, and moves on.

**This is a guide for the writer, with a lint that lists and does not fail** (abacus #12375): tools/calc_lint.py lists
any keys block in an astronomy course's lesson whose only operations are + − × ÷ on whole numbers under 100, with no
function key, for abacus's review. A listed block stands only with a `calculator_reason:` line in the lesson's front
matter saying why the calculator earns it. Its selftest plants sky-01's 40 + 25 (listed), par-01's TAN chain (not
listed) and a reasoned block (not listed).

## A lesson without the calculator

Allowed (abacus #12375), and done like any unit: check.py passes its items, every number it quotes traces to a cited
source or a widget's `shows:`, and it has abacus's review and a fresh reader. If it uses no calculator at all, it
drops the setup block too. On the route map a lesson is done when its items are right, or, with none, when its last
keys block has been tried, so a lesson with neither could never be done: every lesson keeps at least one item, which
is the check of step 5 (primer's recommendation, #12381). The other way, a widget step counting as tried, would be a
site and format change of primer's and tutor's, not proposed.

**Whether B may have such lessons is Michael's call**, because the live site's lede says, as its second sentence:
"Each lesson runs the calculator's own core in the page: press Try it beside an example and watch the keys." The card
(abacus writes it) carries two choices: B keeps a little calculator work in every lesson, or B may have lessons
without it and the lede changes. primer's draft for the second, with the first sentence unchanged ("Mathematics and
astronomy on the STU-32, course by course."): "The calculator's own core runs in the page: where a lesson works a
number out, press Try it beside the example and watch the keys."

## The four pilots, and how each changes

- **hms-01 (both courses).** Keeps its conversions: HMS→ and →HMS are real calculator work. Gains a first step on the
  sky-sphere: Vega found on the J2000 grid at about 18h 37m and +39°, which is as close as a grid reads; then the
  catalog row's exact 18h 36m 56.3s and +38° 47′ 01″ (said to be the catalog's, not the grid's), turned into hours
  and degrees.
- **par-01 (A1).** Keeps Bessel and the triangle: TAN and 1/x are the point. Gains a plate lab before them, linked:
  two plates six months apart, the near star's shift measured with markers, half of it the parallax (astrometrics's
  Calc station, #12367). astrometrics sends the link when it is live.
- **sky-01 (B unit 1).** Loses its keys blocks: its 40 + 25 and 7 − 2 are exactly the worry, and the lint lists them
  today. Leads with the brightness limit (linked, or the star-field widget) and the dark-adaptation timeline. Keeps
  its items, and safety stays first. If the card's answer is that B keeps a little calculator in every lesson, its
  one keys block is the one the measurement needs, not the minutes.
- **sky-02 (B unit 2).** Loses the fist arithmetic on the calculator. Leads with the hand-ruler widget: three fingers
  across the Pointers, then the catalog's 5.374 and how far off the hand was.

None of the four changes on learn until its rewrite passes abacus's review and a fresh reader, unit by unit.
