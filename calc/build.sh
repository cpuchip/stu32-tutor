#!/usr/bin/env bash
# calc/build.sh [--fresh] [--tag-suffix S] [--dev]: the stu32-calc image at the accepted pin.
#
# The pin is the Makefile's CORE_PIN, which moves only when abacus accepts one; casim's is the
# firmware's own CASIM_PIN file at that pin. The runners are the binaries `make tools` builds (the
# ones make check runs), built in gcc:14 by scripts/check-docker.sh from export-core.sh's export.
# Casimir's CLI is built from a git archive of casim at CASIM_PIN, and the entry program
# (calc/stu32calc.c) beside it. The image itself is built with no network, from a staged folder
# holding only those binaries, the pins, the licences and the key-name page; it is never pushed to a
# registry (abacus #5737): it goes to another box by `docker save | ssh <box> docker load`.
#
# --fresh removes this pin's core export and the staged folder first (a rebuild from scratch).
# --tag-suffix tags a second build apart from the first, for the rebuild comparison.
# --dev allows uncommitted changes, and the pins then say so ("<commit>-dirty"): for iterating only.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
cd "$here"
fresh=0; suffix=""; dev=0
while [ $# -gt 0 ]; do
    case "$1" in
        --fresh) fresh=1 ;;
        --dev) dev=1 ;;
        --tag-suffix) suffix="$2"; shift ;;
        *) echo "build.sh: unknown argument $1" >&2; exit 2 ;;
    esac
    shift
done

# Both bases by digest, so a rebuild cannot pick up a moved tag.
GCC=gcc@sha256:9188ac751ca24431dc43dbd142a223c98ea74f01d2858e84d30ba342a0d67844
BASE=gcr.io/distroless/cc-debian13@sha256:e792ab3d241a468a4fd7519ddbbebe66b49b5f365771716ea688ad40b6c6f1c2

pin="$(sed -n 's/^CORE_PIN := //p' Makefile)"
fw="$(cd ../abacus-firmware && pwd)"
casim="$(cd ../casim && pwd)"
g() { git -c safe.directory='*' -C "$1" "${@:2}"; }
fw_full="$(g "$fw" rev-parse --verify "$pin^{commit}")"
cas_pin="$(g "$fw" show "$fw_full:CASIM_PIN" | tr -d '[:space:]')"
cas_full="$(g "$casim" rev-parse --verify "$cas_pin^{commit}")"
[ -n "$(g "$casim" branch -r --contains "$cas_full")" ] || { echo "build.sh: casim $cas_pin is on no remote branch" >&2; exit 1; }
# What the image says it was built from must be committed: the tutor's tools, Makefile and calc/.
tutor="$(git rev-parse HEAD)"
if [ -n "$(git status --porcelain -- tools calc scripts Makefile docs/lesson-format.md)" ]; then
    if [ "$dev" = 1 ]; then tutor="$tutor-dirty"; suffix="$suffix-dev"
    else echo "build.sh: tools/, calc/, scripts/, the Makefile or lesson-format.md has uncommitted changes; commit them first (or --dev)" >&2; exit 1; fi
fi
core="build/core-$pin"
stage="build/calc/stage-$pin$suffix"
if [ "$fresh" = 1 ]; then rm -rf "$core" "$stage"; fi
rm -rf "$stage"
mkdir -p "$stage/opt/stu32/bin" "$stage/opt/stu32/licenses" "$stage/opt/stu32/doc"

# 1. The runners, exactly as make check builds them.
GCC_IMAGE="$GCC" bash scripts/check-docker.sh tools
[ "$(cat "$core/.exported")" = "$fw_full" ] || { echo "build.sh: $core is not $fw_full" >&2; exit 1; }

# 2. Casimir's CLI at CASIM_PIN, the entry program, and every binary stripped into the stage. Casimir's
# build reads the firmware checkout beside it (../abacus-firmware), so that is mounted there, read only.
w() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }
MSYS_NO_PATHCONV=1 docker run --rm \
    -v "$(w "$here"):/w/stu32-tutor" -v "$(w "$casim"):/w/casim:ro" -v "$(w "$fw"):/x/abacus-firmware:ro" \
    -e GIT_CONFIG_COUNT=1 -e GIT_CONFIG_KEY_0=safe.directory -e GIT_CONFIG_VALUE_0='*' \
    -w /w/stu32-tutor "$GCC" bash -euo pipefail -c "
        mkdir -p /x/casim
        git -C /w/casim archive $cas_full | tar -x -C /x/casim
        make -s -C /x/casim build/casim >/dev/null
        cc -std=c11 -O2 -Wall -Wextra -Werror calc/stu32calc.c -o /tmp/stu32-calc
        for b in $core/build/keyrun $core/build/vectors $core/build/fmt_vectors /x/casim/build/casim /tmp/stu32-calc; do
            strip -o $stage/opt/stu32/bin/\$(basename \$b) \$b
        done
        cp /x/casim/LICENSE $stage/opt/stu32/licenses/casimir-MIT.txt"
cp "$core/third_party/LICENSE.intel-dfp.txt" "$stage/opt/stu32/licenses/intel-dfp-BSD-3.txt"
cp docs/lesson-format.md "$stage/opt/stu32/doc/lesson-format.md"
intel_sha="$(sed -n 's/.*sha256 `\([0-9a-f]\{64\}\)`.*/\1/p' "$core/third_party/README.md" | head -1)"
cat > "$stage/opt/stu32/pins" <<EOF
firmware $fw_full
casim $cas_full
stu32-tutor $tutor
intel-dfp-sha256 $intel_sha
builder $GCC
base $BASE
EOF

# 3. The image, with no network.
# The tools' commit is in the tag too, so two builds at one pin never share a tag.
tag="stu32-calc:fw-${pin}.cas-${cas_pin:0:7}.t-${tutor:0:7}$suffix"
docker build --network none -q -f calc/Dockerfile \
    --build-arg BASE="$BASE" \
    --label "org.opencontainers.image.title=stu32-calc" \
    --label "net.cpuchip.stu32.firmware=$fw_full" \
    --label "net.cpuchip.stu32.casim=$cas_full" \
    --label "net.cpuchip.stu32.tutor=$tutor" \
    --label "net.cpuchip.stu32.intel-dfp-sha256=$intel_sha" \
    --label "net.cpuchip.stu32.builder=$GCC" \
    -t "$tag" "$stage" >/dev/null
echo "build.sh: $tag"
(cd "$stage" && find opt -type f | sort | xargs sha256sum)
