#!/usr/bin/env bash
# calc/run.sh [--image TAG] [--deadline S] [--test-no-inner | --test-no-cpu-limit] COMMAND ARGS...: one
# stu32-calc call, in a fresh container with the limits abacus ruled (#5737), and the outer deadline.
# stdin passes through.
#
# The outer deadline kills the CONTAINER, by the id docker writes to --cidfile: killing the docker
# client alone leaves its container running. A kill here prints
# {"status":"TIMEOUT","layer":"outside",...} and exits 124, the inner layer's code.
#
# The image is $STU32_CALC_IMAGE, or the one tagged for the Makefile's CORE_PIN. --test-no-inner turns
# off the entry program's CPU limit and wall clock (calc/acceptance.py: the outer layer alone), and
# --test-no-cpu-limit the CPU limit alone (the wall clock alone).
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
deadline=30
image="${STU32_CALC_IMAGE:-}"
testenv=()
while [ $# -gt 0 ]; do
    case "$1" in
        --image) image="$2"; shift 2 ;;
        --deadline) deadline="$2"; shift 2 ;;
        --test-no-inner) testenv=(-e STU32_CALC_TEST_NO_INNER=1); shift ;;
        --test-no-cpu-limit) testenv=(-e STU32_CALC_TEST_NO_INNER=cpu); shift ;;
        *) break ;;
    esac
done
if [ -z "$image" ]; then
    pin="$(sed -n 's/^CORE_PIN := //p' "$here/Makefile")"
    # The newest image for the pin (docker lists the newest first), never a -dev, -rebuild or other suffix.
    image="$(docker image ls --format '{{.Repository}}:{{.Tag}}' "stu32-calc" | grep -E ":fw-$pin\.cas-[0-9a-f]{7}\.t-[0-9a-f]{7}$" | head -1)"
    [ -n "$image" ] || { echo '{"status":"NO_IMAGE","detail":"no stu32-calc image for the Makefile pin; calc/build.sh"}'; exit 1; }
fi
tmp="$(mktemp -d)"
cid="$tmp/cid"
flag="$tmp/timed-out"
w() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }
(
    for _ in $(seq "$deadline"); do sleep 1; done
    touch "$flag"
    if [ -s "$cid" ]; then docker kill "$(cat "$cid")" >/dev/null 2>&1; fi
) &
watchdog=$!
MSYS_NO_PATHCONV=1 docker run --rm -i --init \
    --network none --read-only --cap-drop ALL --security-opt no-new-privileges --user 65532:65532 \
    --memory 256m --memory-swap 256m --pids-limit 16 --cpus 1 \
    --ulimit nofile=64:64 --ulimit core=0:0 \
    "${testenv[@]}" --cidfile "$(w "$cid")" "$image" "$@"
rc=$?
kill "$watchdog" 2>/dev/null
wait "$watchdog" 2>/dev/null
if [ -e "$flag" ]; then
    printf '{"status":"TIMEOUT","layer":"outside","limit":"wall %s s","image":"%s"}\n' "$deadline" "$image"
    rc=124
fi
rm -rf "$tmp"
exit "$rc"
