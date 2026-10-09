#!/usr/bin/env bash
# check-docker.sh [make args]: make check in the gcc:14 container (for a machine with no native
# toolchain for the core). Mounts this repo, and the firmware and stu32-arcade checkouts beside it,
# read only (the arcade's apps are linked by the app layer from a7f49a7 on; from 7776c7c the
# firmware's games list finds the clone through GAMES_REPOS, and CAS 004 builds casim from a
# cpuchip/casimir clone at ../casim, CASIM_REPO; both compiled only, never read). GCC_IMAGE picks the
# image (calc/build.sh passes gcc:14 by digest); gcc:14 by default.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
fw="$(cd "$here/../abacus-firmware" && pwd)"
arcade="$(cd "$here/../stu32-arcade" && pwd)"
casim="$(cd "$here/../casim" && pwd)"
w() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }
MSYS_NO_PATHCONV=1 exec docker run --rm \
    -v "$(w "$here"):/w/stu32-tutor" -v "$(w "$fw"):/w/abacus-firmware:ro" \
    -v "$(w "$arcade"):/w/stu32-arcade:ro" -v "$(w "$casim"):/w/casim:ro" \
    -e GAMES_REPOS=/w -e CASIM_REPO=/w/casim \
    -w /w/stu32-tutor "${GCC_IMAGE:-gcc:14}" make "${@:-check}"
