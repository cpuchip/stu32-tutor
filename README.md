# stu32-tutor

An original math, physics and programming curriculum around the STU-32 calculator, and the site that teaches it (working name tutor).

Private until Michael sets the curriculum's licence. Everything here is written fresh: published textbooks are used for scope and order only, and no text, figure or problem is copied from any of them or from any calculator's manual.

## Layout

- `lessons/<id>/`: one lesson. `vectors.txt` (the maths, as key vectors), `fmt-vectors.txt` (the displays the prose quotes), `lesson.md` (the prose and the keys the student presses).
- `docs/lesson-format.md`: the rules, and what `make check` proves.
- `docs/evidence/`: the independent recomputation of every lesson's expected values.
- `tools/`: the checker. `keyrun` presses a lesson's printed keys on the firmware's own key layer and compares them with the lesson's vectors.

## Running

`make check` runs every lesson on the firmware's core at `CORE_PIN` (a pushed commit of cpuchip/abacus-firmware, exported with git archive). `make controls` proves the check can fail. It needs three clones side by side:

1. this repo;
2. cpuchip/abacus-firmware at `../abacus-firmware`, fetched so that `CORE_PIN` is on one of its remote branches;
3. cpuchip/stu32-arcade at `../stu32-arcade` (the apps the firmware's app layer links, compiled only, never read): the export checks it out at the firmware's `ARCADE_PIN` and fails without it. A different place can be given as `scripts/export-core.sh`'s fourth argument.

Then `make check`, with gcc, make, git and python3. On fermion, which has no native toolchain for the core: `scripts/check-docker.sh` (or `scripts/check-docker.sh controls`), in the gcc:14 container.
