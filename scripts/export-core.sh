#!/usr/bin/env bash
# export-core.sh FIRMWARE PIN DIR [ARCADE]: the firmware at PIN, exported with git archive into DIR.
# PIN must be on a remote branch of FIRMWARE (pushed), so anyone can rebuild what we tested. A core
# whose app layer links apps from stu32-arcade (an ARCADE_PIN file, from a7f49a7 on) also gets them,
# exported by the firmware's own scripts/fetch-arcade.sh from the arcade clone ARCADE (default the
# checkout beside FIRMWARE), never written into.
set -euo pipefail
fw="$1"; pin="$2"; dir="$3"; arcade="${4:-$fw/../stu32-arcade}"
g() { git -c safe.directory='*' -C "$fw" "$@"; }
full="$(g rev-parse --verify "$pin^{commit}")"
if [ -z "$(g branch -r --contains "$full")" ]; then
    echo "export-core: $pin is on no remote branch of $fw (fetch it, or pin a pushed commit)" >&2
    exit 1
fi
rm -rf "$dir"
mkdir -p "$dir"
g archive "$full" | tar -x -C "$dir"
if [ -f "$dir/ARCADE_PIN" ]; then
    # The clone may belong to another user inside the container: allow it for this command only.
    GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' \
        ARCADE_REPO="$(cd "$arcade" && pwd)" sh "$dir/scripts/fetch-arcade.sh"
fi
echo "$full" > "$dir/.exported"
echo "export-core: $full -> $dir"
