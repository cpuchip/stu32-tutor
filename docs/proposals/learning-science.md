# Learning science for the lessons (PROPOSAL, for Michael)

**Status:** a proposal (abacus #6119); its citations were checked against the papers by abacus (#6138).
Nothing is built.

**His words** (relayed verbatim by abacus #6119): "For the lessons are we using modern teaching techniques? I
think spaced repetition is one? Can you do some research to see how best we can approach the teaching? Or have
tutor do it?"

**The binding question:** which learning-science techniques have strong evidence for *mathematics* learning,
and how does each fit stu32-tutor as it is? The constraints are:
- a static, public CC BY-SA curriculum;
- no accounts;
- the core as judge;
- browser storage only as a convenience;
- COPPA in mind.

## How the evidence was read

Every number and quotation below comes from a paper's own text, opened on 2026-10-10. Each PDF was turned
into text with pdftotext and the sentence found in it. The sentences are kept in a ledger, one source per
entry, with where each copy came from (`build/learning-science/evidence.md`, local).

Where a paper could not be opened, this says so and gives no numbers from it:
- **Sinha & Kapur (2021):** the publisher refused the fetch.
- **Bloom (1984):** the copy is a scan, so its text could not be read; only its title was.
- **Kulik, Kulik & Bangert-Drowns (1990):** not found as an open copy.
- **The expertise-reversal paper (Sweller, Ayres, Kalyuga & Chandler 2003):** not found as an open copy.
- **Dunlosky et al.'s full 2013 monograph:** not found as an open copy. What was read is Dunlosky's own
  summary of it in *American Educator* (Fall 2013).

| Technique | Evidence for school maths | Fit here |
|---|---|---|
| Interleaved practice | strongest: three classroom studies in grade 7, one a preregistered RCT | a mixed review section per lesson, checked mechanically |
| Retrieval practice | strong in classrooms (IES: "Strong"); maths items are retrieval by nature | already in the checkpoints; add a short "From before" set to each lesson |
| Spacing | strong in general; mixed for maths procedures | the "From before" set spaces by the graph; an optional review queue in the browser |
| Worked examples, alternated and faded | moderate (IES), including grade 8 and 9 algebra | already example-heavy; alternate and fade explicitly; problems first for placed learners |
| Self-explanation | moderate overall; small to moderate in maths | "Why?" prompts after examples |
| Feedback on errors | consistent for specific, elaborated feedback; timing depends on the task | already: slips and their hints |
| Mastery learning | contested: weak on standardized measures | already: "done" means the checkpoint passed, as guidance |
| Productive failure | not opened here | a question for Michael, not a recommendation |

## 1. Interleaved practice: the strongest maths-specific evidence

Interleaved practice mixes problems of different kinds, so the learner must choose the strategy as well as
carry it out. Blocked practice is a set of problems that all use the lesson just taught.

**The evidence:**
- **Rohrer, Dedrick & Stershic** (*J. Educ. Psych.*, online 2014, printed 2015): "126 seventh-grade students
  received the same practice problems over a 3-month period", interleaved or blocked. Interleaved practice
  scored higher on a test 1 or 30 days later, with Cohen's d of 0.42 and 0.79.
- **Rohrer, Dedrick & Burgess** (*Psychon. Bull. Rev.* 2014): "grade 7 students (n = 140) received blocked or
  interleaved practice over a nine-week period". The unannounced test two weeks later gave "72 % vs. 38 %,
  d = 1.05". This held "even though the different kinds of problems were superficially dissimilar from each
  other".
- **Rohrer, Dedrick, Hartwig & Cheung** (*J. Educ. Psych.*, online 2019): a "preregistered, cluster randomized
  controlled trial". "Each of 54 7th-grade mathematics classes periodically completed interleaved or blocked
  assignments over a period of 4 months". One month later, "the interleaved group outscored the blocked group,
  61% versus 38%". The effect size was d = 0.83. "Teachers were able to implement the intervention without
  training".
- **Rohrer & Taylor** (*Instr. Sci.* 2007), with college students:
  - In practice, mixing hurt: "the Blockers' average of 89% ... statistically exceeded the Mixers' average of
    60%".
  - On the test a week later, "the mean test performance of Mixers (63% ...) was far greater than that of the
    Blockers (20% ...)".

  So a learner who mixes will feel worse at practice and do better on the test.

**The limits are the authors' own** (the 2019 trial's four caveats):
1. "Interleaved practice probably takes more time".
2. The benefit "might be smaller at shorter test delays". One study of seventh graders (Ostrow et al. 2015,
   tested 2 to 5 days later) found "a positive but not statistically significant effect".
3. It "might be less effective or too difficult if students do not first receive at least a small amount of
   blocked practice"; "the data do not suggest that students should entirely avoid blocked practice."
4. It "might be effective only if students receive corrective feedback."

**What we do now:**
- **Exercises:** 49 lessons have `## Exercises`, and every set is blocked on its own lesson.
- **Checkpoints:** the 13 unit checkpoints are already interleaved within their unit. parallel-01's checkpoint
  has 9 items on 9 different topics.
- **Across units:** no lesson has a set mixed across units.

**What it would change:**
- **The section:** a `## Mixed review` section in each lesson after a course's first unit, placed after the
  blocked exercises (caveat 3). It holds items from earlier lessons on the lesson's prerequisite routes, with
  answers and slips (caveat 4).
- **The check:** "no two consecutive items share a topic" is mechanical, since every item already names its
  `topics:`. check.py can refuse a set that breaks it, with a planted control.
- **Cost:** items to write, nothing for the page beyond what items already need.

## 2. Retrieval practice: answering from memory

**The evidence:**
- **Roediger & Karpicke** (*Psych. Sci.* 2006): "One hundred twenty Washington University undergraduates" studied
  prose passages. "When the final test was given after 5 min, repeated studying improved recall relative to
  repeated testing. However, on the delayed tests, prior testing produced substantially greater retention than
  studying". After a week, "The tested group recalled 56% of the material, whereas the restudy group recalled
  only 42%", with d = 0.83.
- **Agarwal, Nunes & Blunt** (*Educ. Psych. Rev.* 2021), a systematic review of classroom studies: "50
  experiments", "49 effect sizes and a total n = 5374, the majority of which (57%) revealed medium or large
  benefits". It held across "a variety of education levels, content areas, experimental designs, final test
  delays".
- **IES practice guide** (Pashler et al. 2007, Recommendation 5b, closed-book quizzes): level of evidence
  "Strong". It rests on "nine experimental studies examining the effects of this practice for improving K-12
  students' performance on academic content".
- **Dunlosky's summary:** practice testing is one of the two strategies "rated ... as the most effective of
  those we reviewed".

**The limits:**
- Most laboratory work uses prose and facts.
- Agarwal et al. note "only 6% of experiments were conducted in non-WEIRD countries."
- The immediate test favours restudy. That matters for how we judge our own lessons: practice that feels
  fluent today is not evidence that it was learned.

**What we do now:** a maths item is retrieval by nature, since the learner works the problem without the page
showing how.
- **Items:** 65 items across 13 lessons' checkpoints and the algebra-to-calculus placement (22 of them).
- **Hand first:** every item is worked by hand first (decision 63).

**What it would change:** a short `## From before` set opening each lesson: two or three items from the
lessons it requires, which graph.py already knows (`needs`).
- **Fixed:** the set is the same for every learner and needs no storage. The graph does what a per-learner
  scheduler would do, roughly.
- **Wider:** the same move puts spacing (section 3) and interleaving (section 1) into every lesson.

## 3. Spacing: the same material again, weeks later

**The evidence:**
- **Cepeda, Pashler, Vul, Wixted & Rohrer** (*Psych. Bull.* 2006): "839 assessments of distributed practice in
  317 experiments located in 184 articles". "the ISI producing maximal retention increased as retention
  interval increased". In other words, the longer the material must last, the longer the best gap between
  study sessions.
- **IES Recommendation 1** (moderate): "Arrange for students to be exposed to each main element of material on
  at least two occasions, separated by a period of at least several weeks--and preferably several months."
- **Rohrer & Taylor (2007), Experiment 1:** one maths problem type, college students. "the Spacers' mean test
  accuracy of 74% ... exceeded both the Massers' average of 49% ... and the Light Massers' average of 46%".

**The tension, which belongs on the card:**
- **Children:** Cepeda et al. wrote that "we cannot say for certain that children's long-term memory will
  benefit from distributed practice", for want of long-interval data in children.
- **Maths procedures:** Ebersbach & Barzagar Nazari (*Front. Psychol.* 2020) taught university students
  (N = 235) a counting procedure. "Contrary to our expectations, the analyses revealed no effect of
  distributed practice". They suggest spacing is "less robust of even absent" for procedural skills.
- **A school study:** the same paper reports that the authors' earlier study of third and seventh graders found
  "The distributed practicing students outperformed the massed practicing students after 1 week and after 6
  weeks, except for third graders, were the effect disappeared after 6 weeks." (Its errors are the paper's
  own.)

So spacing is well supported for facts and concepts, and less certain for a procedure practised to fluency.
Interleaving carries spacing inside it ("inherently incorporates the learning strategies of spacing and
retrieval practice", Rohrer et al. 2019) and has the stronger maths evidence. This is why the recommendation
leads with sections 1 and 2.

**What it would change:**
- **Fixed, in the lessons:** the "From before" sets space each topic by the graph's distance.
- **Optional, in the browser:** a review queue kept on the device, never sent anywhere. It holds the IDs of
  checkpoint items passed and the date of each. An item comes back after a few weeks, as IES's "several
  weeks" suggests.
  - Clearing it loses nothing the lessons don't already give.
  - It holds no name and no answer text, so nothing about the learner. It is like the stored mode and entry.

## 4. Worked examples: alternated, then faded

**The evidence:** IES Recommendation 2 (moderate): "interleave worked example solutions and problem-solving
exercises--literally alternating between worked examples demonstrating one possible solution path and
problems that the student is asked to solve".
- **Classroom support:** "Some classroom experiments provide further evidence that the recommendation can be
  practically and effectively implemented in real courses at the K-12 and college levels."
- **Algebra:** one series of algebra experiments used "8th and 9th grade students".
- **Expertise:** "As students develop greater expertise, reduce the number of worked examples provided and
  increase the number of problems that students solve independently."
- **Fading:** "Gradually 'fading' examples into problems, by giving early steps in a problem and requiring
  students to provide more and more of the later steps ... also seems to benefit student learning."

This is the expertise-reversal effect: help that suits a beginner can hinder someone who already knows the
material. The original paper was not opened, so this note relies on the guide's summary of it.

**What we do now:** the lessons are built on worked examples.
- **Keys blocks:** 1003 of them, each run by the core in every mode.
- **Exercises:** most lessons follow the examples with exercises.
- **Missing:** the alternation, an example and then its twin to solve, is not a rule. Nothing is faded.

**What it would change:**
- **A "Your turn" twin:** follows each main example. It is an item, so the core judges it.
- **A faded block:** a keys block whose last steps the page hides until the learner has tried them. check.py
  still runs the whole block, so a faded example stays verified.
- **Problems first for placed learners:** for a learner whom placement put past a unit, the page could open
  that unit's lessons at their checkpoint, with the examples one link away.

## 5. Self-explanation: saying why a step works

**The evidence:**
- **Bisra, Liu, Nesbit, Salimi & Winne** (*Educ. Psych. Rev.* 2018), a meta-analysis: "a random effects analysis
  of 69 effect sizes (5917 participants) obtained an overall point estimate of g = .55". They conclude that "beneficial effects of
  inducing self-explanation seem to be available for most subject areas studied in school, and for both
  conceptual (declarative) and procedural knowledge".
- **For maths specifically:** they report a separate meta-analysis (Rittle-Johnson et al. 2017) in which
  prompting "had a small to moderate effect".
- **IES Recommendation 7** (deep explanatory questions): "Strong".
- **Dunlosky's summary** puts self-explanation among the strategies best for "comprehension of what they are
  reading".

**What it would change:**
- **Prose prompts:** a "Why?" after the key step of a main example: "Why does the 180 come in here?" No check
  is possible, since the core judges numbers, not reasons.
- **Or a reason item:** an item whose answer is one of several stated reasons. It would be a new answer kind
  and would need Michael's word.

## 6. Feedback: specific, and timed to the task

**The evidence:** Shute ("Focus on Formative Feedback", *Rev. Educ. Res.* 2008) finds "no consistent main
effect of timing". Her guidelines are:
- "For difficult tasks, use immediate feedback."
- "For relatively simple tasks, use delayed feedback."

She also notes that "low-achieving students may benefit from immediate feedback". Her catalogue of elaborated
feedback includes feedback "that focuses on the learner's specific response" and feedback "requiring error
analysis and diagnosis".

**What we do now:** this already fits. A slip is a likely wrong answer, made by its own keys in the core, and
its hint names the step that produced it (decision 67). There are 78 slip lines across the 65 items. A `work`
item shows its working after the attempt, and a miss links back to the section that teaches the topic.

**What it would change:** little.
- The checkpoint gives its feedback at once, which suits difficult work.
- The mixed review (section 1) needs answers and slips too, which is the 2019 trial's fourth caveat.

## 7. Mastery learning: contested

**What was read:**
- Bloom's 1984 paper is titled "The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective
  as One-to-One Tutoring". Its text was a scan and was not read here.
- **Slavin** (*Rev. Educ. Res.* 1987) reviewed group mastery learning in schools over at least four weeks. He
  "found essentially no evidence to support the effectiveness of group-based mastery learning on standardized
  achievement measures. On experimenter-made measures, effects were generally positive but moderate in
  magnitude, with little evidence that effects maintained over time." (The scan's text errors are corrected
  here.)
- Kulik et al.'s 1990 meta-analysis of mastery programmes was not opened, so nothing from it is used here.

**What we do now:** the adventure-route note's rule that a lesson is done when "the unit checkpoint passed", and a miss linking back,
are mastery's two parts: a criterion, and correction. In both they guide, never lock. The evidence does not
justify making them stricter.

## 8. Productive failure: not recommended yet

The meta-analysis by Sinha & Kapur (*Rev. Educ. Res.* 2021) compares problem solving before instruction with
instruction first. It could not be opened (the publisher refused the fetch), so no claim from it is made here.

It is named because it pulls the other way from section 4: a puzzle before the explanation, against an example
before the problem. A puzzle-first opener in one conceptual lesson is possible, judged as the lesson's other
items are, but the paper must be read first.

## The overviews, for the card

**Dunlosky's summary** of the 2013 review (*American Educator*, Fall 2013):
- practice testing and distributed practice are "the most effective of those we reviewed because they can help
  students regardless of age";
- interleaved practice is among the "Strategies with Much Promise".

Rohrer's later grade 7 trials (section 1) came after that review.

**The IES practice guide** (Pashler et al. 2007) grades its recommendations:
- spacing: moderate;
- examples alternated with problems: moderate;
- graphics with words: moderate;
- concrete with abstract: moderate;
- pre-questions: low;
- quizzing: strong;
- judging one's own learning: low;
- deep questions: strong.

## For him to choose

1. **"From before" sets:** two or three retrieval items from the lesson's prerequisites, opening each lesson,
   fixed and needing no storage. Recommended. This is the biggest gain for the least.
2. **A mixed review section per lesson**, interleaved and checked mechanically (no two consecutive items on one
   topic). Recommended. Pre-algebra and geometry would get them as they are written, algebra as a sweep.
3. **The browser review queue:** item IDs and dates on the device only. Recommended after 1 and 2, as a
   convenience.
4. **Worked examples:** a "Your turn" twin after each main example, faded blocks, and problems first for placed
   learners. Recommended in that order.
5. **Self-explanation:** "Why?" prompts as prose (recommended), or a new reason item kind.
6. **Productive failure:** read the meta-analysis first, then perhaps one trial lesson; or not now.

None of these collects anything about a learner. The queue in choice 3 is the only new stored state, kept like
the mode and the entry.
