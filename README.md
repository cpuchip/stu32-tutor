# stu32-tutor

An original math, physics and programming curriculum around the STU-32 calculator, and the site that teaches it (working name tutor).

Public since 2026-10-09, under the licences in LICENSE. Everything here is written fresh: published textbooks are used for scope and order only, and no text, figure or problem is copied from any of them or from any calculator's manual. A quotation from someone else's work is marked as one, with its source.

## Layout

- `lessons/<id>/`: one lesson. `vectors.txt` (the maths, as key vectors), `fmt-vectors.txt` (the displays the prose quotes), `lesson.md` (the prose and the keys the student presses).
- `docs/lesson-format.md`: the rules, and what `make check` proves.
- `docs/evidence/`: the independent recomputation of every lesson's expected values.
- `docs/how-this-was-built.md`: who wrote this, how a lesson is checked and accepted, and what the `#NNNN` numbers in
  the history mean.
- `tools/`: the checker. `keyrun` presses a lesson's printed keys on the firmware's own key layer and compares them with the lesson's vectors.

## Running

The lessons can be read, used and adapted from this repository alone, under the licences below. Running
the checks needs the STU-32 firmware and its build inputs, all public repositories.

`make check` runs every lesson on the firmware's core at `CORE_PIN` (a pushed commit of cpuchip/stu32-firmware, exported with git archive). `make controls` proves the check can fail. It needs four clones side by side, each fetched so the pin it is asked for is on its origin:

1. this repo;
2. cpuchip/stu32-firmware at `../stu32-firmware` (`CORE_PIN`);
3. cpuchip/stu32-arcade at `../stu32-arcade`: the games the firmware's APPS lists (its `games.list`), compiled only, never read;
4. cpuchip/casimir at `../casim`: the computer algebra the core links from CAS 004 (the firmware's `CASIM_PIN`), compiled only.

The firmware's build finds 3 and 4 through `GAMES_REPOS` (the directory holding stu32-arcade) and `CASIM_REPO` (the casimir clone); `scripts/check-docker.sh` sets both. Natively, set them to the paths above, since the build runs inside the exported copy under build/. Then `make check`, with gcc, make, git and python3. Without a native toolchain for the core: `scripts/check-docker.sh` (or `scripts/check-docker.sh controls`), in the gcc:14 container.

The firmware was cpuchip/abacus-firmware, private, until it went public with its history rewritten once. The firmware
commits that docs/ cites (as abacus-firmware) carry their ids from before the rewrite; stu32-firmware's
`docs/commit-map.txt` maps each old id to its new one (`grep ^<old id> docs/commit-map.txt`).

## Trademarks

HP, 35s, 33s and the other product names in this repository are trademarks of their respective owners,
used only to identify compatible behaviour.
