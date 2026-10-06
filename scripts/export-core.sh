#!/usr/bin/env bash
# export-core.sh FIRMWARE PIN DIR: the firmware at PIN, exported with git archive into DIR.
# PIN must be on a remote branch of FIRMWARE (pushed), so anyone can rebuild what we tested.
set -euo pipefail
fw="$1"; pin="$2"; dir="$3"
g() { git -c safe.directory='*' -C "$fw" "$@"; }
full="$(g rev-parse --verify "$pin^{commit}")"
if [ -z "$(g branch -r --contains "$full")" ]; then
    echo "export-core: $pin is on no remote branch of $fw (fetch it, or pin a pushed commit)" >&2
    exit 1
fi
rm -rf "$dir"
mkdir -p "$dir"
g archive "$full" | tar -x -C "$dir"
echo "$full" > "$dir/.exported"
echo "export-core: $full -> $dir"
