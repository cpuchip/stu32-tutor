#!/usr/bin/env bash
# check-docker.sh [make args]: make check in the gcc:14 container (fermion has no native
# toolchain for the core). Mounts this repo and the firmware checkout beside it, read only.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
fw="$(cd "$here/../abacus-firmware" && pwd)"
w() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }
MSYS_NO_PATHCONV=1 exec docker run --rm \
    -v "$(w "$here"):/w/stu32-tutor" -v "$(w "$fw"):/w/abacus-firmware:ro" \
    -w /w/stu32-tutor gcc:14 make "${@:-check}"
