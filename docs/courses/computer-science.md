# Computer science: how we got here, and how it works (proposed)

**Status: a proposal, outline level (T65).** Michael said yes to a pilot lesson for the learn reader, teens and up,
and asked for a syllabus "from Jr high level up through college topics including AI and systems engineer in the age
of AI" (the T65 card, A30, 2026-11-19). The pilot, bin-01, is written. Nothing here is a lesson yet, and nothing is
live. The units and their order are for him and the course's first reader to change.

## The shape

- **History, then the problem, done on the page.** Each lesson opens with the people who found the idea and the
  question they faced, told from texts we opened and cite (```quote``` blocks are checked word for word against the
  cached source). Then the learner works the problems on the page, and a machine judges every answer before any
  person reads the lesson.
- **No device.** These lessons need no calculator (`device: none`, docs/lesson-format.md). Where the STU-32 helps it
  can come back: its core has binary, octal and hex modes and the logic operations, so a later lesson can say "your
  calculator counts in binary too" with ordinary checked keys.
- **Three stages** in one course for now (courses/computer-science.course): junior high (what a computer is made
  of), high school (how programs and networks work), college (what can be computed, and how large systems, AI among
  them, are built and checked). The stages can become three courses, each the next one's prerequisite, once there
  are lessons in more than the first.
- **The exercises the page can judge today:** a typed answer (a word, a bit string, a number in base 2, 8, 10 or 16)
  and a table with blanks (a truth table, a traced algorithm). Later units need more, and each is a decision to make
  with primer before its unit is written: choosing among options, ordering steps, and running a short program.

## Stage 1: what a computer is made of (junior high)

| Unit | Title | Its question | What it covers |
|---|---|---|---|
| 1 | Counting in two symbols | How can a machine that only knows two symbols hold any number? | Place value; binary counting, reading and writing; binary addition; one column of a sum as a table. **The pilot, bin-01.** |
| 2 | Logic and gates | How does a machine made of switches decide anything? | AND, OR, NOT and XOR as truth tables; gates; a full adder chained into an adder; a sum worked through the gates. |
| 3 | Letters, pictures and sound as numbers | How does a row of bits become a letter, a colour or a sound? | Character codes; pixels and colour as numbers; sampling a sound; how many bits a thing needs. |
| 4 | Algorithms by hand | What is a step-by-step method, and how do you know it will finish? | Following and tracing a method in a table; Euclid's method for the greatest common factor; sorting a hand of cards. |
| 5 | A first program | How do you tell a machine exactly what to do? | Instructions, order, repetition and choice; a program traced by hand; the first programs written for machines. |

## Stage 2: how programs and networks work (high school)

| Unit | Title | Its question | What it covers |
|---|---|---|---|
| 6 | The machine that follows instructions | What happens inside a processor when it runs a program? | Memory and addresses; the stored program; fetch, decode, execute, traced step by step. |
| 7 | Keeping things in order | How do you store many things so you can find them again? | Lists, stacks (the calculator's own stack), queues, trees, and tables found by a key. |
| 8 | How long will it take? | How much more work does a method need when its input doubles? | Searching a sorted list by halves; sorting methods compared; counting steps as the input grows. |
| 9 | Networks | How does a message cross the world in pieces and arrive whole? | Packets, addresses and routes; how lost pieces are noticed and sent again; how the web is built on that. |
| 10 | Secrets in public | How can two strangers agree on a secret while everyone listens? | Old ciphers and how they were broken; arithmetic that wraps around; a key exchange worked with small numbers. |

## Stage 3: what can be computed, and how large systems are built (college)

| Unit | Title | Its question | What it covers |
|---|---|---|---|
| 11 | What no program can do | Are there questions no program can ever answer? | A machine reduced to its simplest form; programs that read programs; why some questions have no general answer. |
| 12 | Proving a program right | How can you know a program is correct, not only that it passed its tests? | Invariants; recursion and induction; a loop proved by hand. |
| 13 | Many programs at once | How does one machine run many programs without them spoiling each other's work? | Processes and scheduling; two programs sharing one thing; locks, and how they go wrong. |
| 14 | Information | How much can a message carry, and how can it survive noise? | Measuring information in bits; compression; codes that find and fix their own errors. |
| 15 | Machines that learn | How can a program get better at a task from examples? | Fitting a line as learning; a single artificial neuron; learning by small corrections; what a model is. |
| 16 | Language models | How does a machine write a sentence one word at a time? | Text as tokens; predicting the next one from probabilities; what such a model can and cannot be trusted with. |
| 17 | Building large systems | How do you build something too big for one person to hold in their head, and have it work? | Requirements, interfaces and tests; how real systems failed and what was learned. |
| 18 | Systems engineering in the age of AI | When a model writes part of a system, who checks it, and how? | Saying what a system must do precisely enough to test it; checks that can fail; keeping a person's judgment where it matters. |

## The history, still to be opened

Each unit's history is told from sources opened when its lesson is written, the way the pilot's are (sources/SOURCES.tsv;
every quote checked against the cached text). The names below are where each unit is likely to look; none is a claim
yet, and no date is given until its source is read.

- Unit 2: Boole and Shannon again; the first relay and electronic computers.
- Unit 3: telegraph codes and the character codes that followed them.
- Unit 4: Euclid; al-Khwarizmi.
- Unit 5: Jacquard's loom; Ada Lovelace's notes on Babbage's Analytical Engine.
- Unit 6: Babbage; the stored-program designs of the 1940s.
- Units 9 and 10: the first packet networks and their protocols; the wartime codebreakers; public-key cryptography.
- Unit 11: Turing and Church on what can be computed.
- Unit 14: Shannon's theory of communication; Hamming's error-correcting codes.
- Units 15 and 16: Turing's question about thinking machines; the perceptron; the transformer.
- Units 17 and 18: the Apollo guidance software and the reports of systems that failed.

## Questions for Michael and the course's reader

1. **Programming.** Units 5 onward want the learner to write and run programs. In which language: one the page runs
   itself (Python in the browser, say), or the STU-32's own programs? This decides what primer builds.
2. **Where the stages start.** Is junior high the right first stage, or should stage 1 be gentler still?
3. **The order of units 15 to 18.** AI could come earlier, in stage 2, as something to use and question, with the
   mathematics of it in stage 3.
