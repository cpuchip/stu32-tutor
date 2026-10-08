# stu32-tutor

An original math, physics and programming curriculum around the STU-32 calculator, and the site that teaches it (working name tutor).

Private until Michael sets the curriculum's licence. Everything here is written fresh: published textbooks are used for scope and order only, and no text, figure or problem is copied from any of them or from any calculator's manual.

## Layout

- `lessons/<id>/`: one lesson. `vectors.txt` (the maths, as key vectors), `fmt-vectors.txt` (the displays the prose quotes), `lesson.md` (the prose and the keys the student presses).
- `docs/lesson-format.md`: the rules, and what `make check` proves.
- `docs/evidence/`: the independent recomputation of every lesson's expected values.
- `tools/`: the checker. `keyrun` presses a lesson's printed keys on the firmware's own key layer and compares them with the lesson's vectors.

## Running

`make check` runs every lesson on the firmware's core at `CORE_PIN` (a pushed commit of cpuchip/abacus-firmware, exported with git archive). `make controls` proves the check can fail. It needs four clones side by side, each fetched so the pin it is asked for is on its origin:

1. this repo;
2. cpuchip/abacus-firmware at `../abacus-firmware` (`CORE_PIN`);
3. cpuchip/stu32-arcade at `../stu32-arcade`: the games the firmware's APPS lists (its `games.list`), compiled only, never read;
4. cpuchip/casimir at `../casim`: the computer algebra the core links from CAS 004 (the firmware's `CASIM_PIN`), compiled only.

The firmware's build finds 3 and 4 through `GAMES_REPOS` (the directory holding stu32-arcade) and `CASIM_REPO` (the casimir clone); `scripts/check-docker.sh` sets both. Natively, set them to the paths above, since the build runs inside the exported copy under build/. Then `make check`, with gcc, make, git and python3. On fermion, which has no native toolchain for the core: `scripts/check-docker.sh` (or `scripts/check-docker.sh controls`), in the gcc:14 container.
