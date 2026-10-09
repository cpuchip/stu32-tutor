# stu32-calc: the STU-32's core in a container

One private image per accepted pin.
- **What it holds:** the firmware's runners, Casimir's CLI and an entry program, at the firmware commit in the Makefile's
  `CORE_PIN` and the casim commit that firmware names in `CASIM_PIN`.
- **What a call does:** it runs printed key sequences, vectors files or Casimir ops, one call per fresh container, and
  answers in JSON. Every limit has its own status.
- **Its users:** the public-domain books pilot, which checks each extracted answer through it, and our own lessons.
- **The ruling:** proposed in private-workspace `.spec/proposals/stu32-calc.md` and ruled by abacus (#5737).

The image is **private**: it holds the firmware's binaries.
- It is never pushed to a registry. It reaches another box by `docker save | ssh <box> docker load`.
- This folder holds only the wrapper, the Dockerfile, the build script and the tests. No firmware source or binary is
  committed here.

## Build

```
bash calc/build.sh            # stu32-calc:fw-<pin>.cas-<casim>.t-<this repo's commit>, from a committed tree
bash calc/build.sh --fresh    # the same, after removing this pin's core export (a rebuild from scratch)
bash calc/build.sh --dev      # an uncommitted tree; the pins say "<commit>-dirty" and the tag ends -dev
```

The build has five parts:
1. **The runners** are the binaries `make tools` builds, the ones `make check` runs. They are built in gcc:14 (pinned
   by digest) by `scripts/check-docker.sh` from `export-core.sh`'s export, which refuses a pin that isn't pushed.
2. **Casimir's CLI** is built from a git archive of casim at `CASIM_PIN`, and the entry program (`stu32calc.c`) beside
   it. Everything is stripped.
3. **The image** is distroless `cc-debian13` (pinned by digest; the same Debian 13 and glibc as gcc:14), built with
   `--network none` from a stage folder holding only:
   - the five binaries;
   - `/opt/stu32/pins`;
   - the licences: Intel's BSD-3 notice, which every build must carry, and Casimir's MIT licence;
   - `docs/lesson-format.md` as the key-name page.
4. **Labels:** the image's OCI labels repeat the pins.

## Call

```
bash calc/run.sh pins
printf 'A\t3452 ENTER 1879 +\n' | bash calc/run.sh keys --mode STU --entry rpn
printf 'V1 | 3452 + 1879 | STU RPN FIX4 3452 ENTER 1879 + | X=5331
' | bash calc/run.sh vectors
bash calc/run.sh casim defint "3×X^2" X 0 2 RAD
```

`run.sh` starts one fresh container per call:
- `--network none --read-only --cap-drop ALL --security-opt no-new-privileges`;
- user 65532, 256 MB, 16 pids, 1 CPU, `--init`.

It also holds the outer deadline, 30 s by default (`--deadline S`). When the deadline passes, it kills the container by
the id in `--cidfile`, because killing the docker client alone leaves its container running.

The image is `--image TAG`, `$STU32_CALC_IMAGE`, or the one tagged for the Makefile's pin.

### The commands (the image's entry point, `stu32calc.c`)

- `keys [--mode STU|33s|35s] [--entry alg|rpn] [--angle DEG|RAD|GRAD] [--fix N]`
  - **stdin:** one step per line, as printed key names (docs/lesson-format.md), optionally `ID<TAB>keys`.
  - **Setup:** with `--mode`, the lessons' setup is pressed first, as step `setup`. Without it, the first line can be
    a setup of your own.
  - **The run:** every step is pressed on one device, in order, by `keyrun --sequence`, the same student run that
    `make check` passes for every lesson.
  - **Each step reports:** the X and Y display lines with their kinds, the status band, X/Y/Z/T as exact text,
    `ans` and `shown`, and any graph.
    - `ans` is the last result, exact: algebraic entry's answer, which leaves the stack untouched. A book record
      uses `ans` in algebraic entry and X in RPN.
    - `shown` is the value an algebraic X line shows: a history entry while one is selected, else `ans` (soroban
      #5854).
- `vectors [--display]`
  - **stdin:** a vectors file in the core's tokens (`ID | note | STU RPN FIX4 … | X=…`), or a display-vectors file.
  - **Status:** PASS or FAIL, with the runner's report lines.
- `casim OP ARG...`
  - **Ops:** derive, simplify, expand, collect, subst, solve, integrate, defint, factor, pdiv, pgcd and cancel, with
    the CLI's own arguments (`casim derive "X^2×SIN(X)" X RAD`).
  - **Status:** OK; CASIM_STATUS with Casimir's own status as the text (UNDEFINED, IMPROPER, SYNTAX n, …); or
    BAD_REQUEST with the CLI's usage.
- `pins`

**Every answer** is one JSON object carrying the pins.
- **Exit codes:** 0 done (a FAIL is done), 1 a bad request, 124 a limit.
- **Limit statuses:**
  - TIMEOUT: `cpu 10 s` or `wall 15 s`, or from run.sh `layer: outside`;
  - OUTPUT_LIMIT: 64 KiB;
  - INPUT_LIMIT: 64 KiB;
  - KILLED: a signal.
- **The core's own limit:** an endless program stops at the core's RUN LIMIT message before any of these.

## MCP

`calc/mcp/server.py` is a stdio MCP server using only the standard library. It offers four tools: `calc_keys`,
`calc_vectors`, `calc_casim` and `calc_pins`.
- **One call per container:** each tool call is one `run.sh` call, so every call gets the container's limits and the
  outer deadline. The server keeps no state and never runs the core itself.
- **Errors:** a tool answer is an error (`isError`) only when the call did not run (a bad request, a bad key, a limit,
  no image). FAIL and Casimir's statuses are answers.
- **Self-test:** `python calc/mcp/server.py --selftest` starts the server and speaks to it.

A client's entry for it:

```json
{"command": "python", "args": ["<repo>/calc/mcp/server.py"],
 "env": {"STU32_CALC_IMAGE": "stu32-calc:fw-<pin>.cas-<casim>.t-<commit>"}}
```

## Problem records

`tools/records.py FILE.jsonl` checks the pilot's problem records (abacus #5698, #5737):
- it checks every field;
- it recomputes each verdict (OK, CALC or FLAGGED) from the printed answer, the core's value and mpmath's;
- it refuses a record whose written verdict differs.

The comparison rules and what the check cannot catch are in its header. mpmath is never in the image: the record's
maker works the problem in mpmath outside it, so the core cannot confirm itself.

## Acceptance

`python calc/acceptance.py IMAGE [--rebuild IMAGE2]` runs these checks:
- **pins;**
- **per-call cost;**
- **the probe set:** every lesson's vectors in each mode and entry, its display vectors, its student run and a list of
  Casimir ops. Each must PASS or be OK, as `make check` finds, and the whole set is hashed into a digest.
- **a planted wrong expectation;**
- **the runaway layers:** the core's RUN LIMIT, the CPU limit, the wall clock, and run.sh's deadline, leaving no
  container in any case;
- **the output and input floods;**
- **the container's posture:** `probe.c` as the entry point, writing nowhere and reaching no network;
- **no network syscall** from the binaries under strace, beside a control that makes one;
- **with `--rebuild`:** the same probe digest from an image rebuilt from scratch.

Measured on a Windows desktop (Docker Desktop), 2026-10-09:
- **Per call:** a median of 1.37 s, almost all of it container start. The core's own work takes 1 to 3 ms, and an
  endless program stops at RUN LIMIT in about 90 ms.
- **The probe:** 374 calls in 322 s with 4 workers.
- **Peak memory:** 2.7 MB for the largest lesson's vectors, 2.6 MB for its student run, and 2.1 MB for a Casimir
  factorization.
- **Image:** 23.5 MB by `docker image inspect`, of which the distroless base is 10.7 MB.
