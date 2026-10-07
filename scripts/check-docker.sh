#!/usr/bin/env bash
# check-docker.sh [make args]: make check in the gcc:14 container (fermion has no native
# toolchain for the core). Mounts this repo, and the firmware and stu32-arcade checkouts beside it,
# read only (the arcade's apps are linked by the app layer from a7f49a7 on).
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
fw="$(cd "$here/../abacus-firmware" && pwd)"
arcade="$(cd "$here/../stu32-arcade" && pwd)"
w() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }
MSYS_NO_PATHCONV=1 exec docker run --rm \
    -v "$(w "$here"):/w/stu32-tutor" -v "$(w "$fw"):/w/abacus-firmware:ro" \
    -v "$(w "$arcade"):/w/stu32-arcade:ro" \
    -w /w/stu32-tutor gcc:14 make "${@:-check}"
