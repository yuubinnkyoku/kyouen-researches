#!/usr/bin/env bash
# Part SY runner: one target, one pass, one process. Pinned invocation.
# Usage: run_target.sh <kNN> <pN> <outdir>
set -u
K="$1"; PASS="$2"; OUTDIR="$3"
GR="$(dirname "$0")/../input/gate-rows.json"
IMPL="$(dirname "$0")/third_impl.js"
LO=$(python3 -c "import json;print(json.load(open('$GR'))['targets']['$K']['lo'])")
HI=$(python3 -c "import json;print(json.load(open('$GR'))['targets']['$K']['hi'])")
LG=$(python3 -c "import json;print(json.load(open('$GR'))['targets']['$K']['legal'])")
mkdir -p "$OUTDIR"
node "$IMPL" --lo="$LO" --hi="$HI" --stones=5 --legal="$LG" \
  --row="$K.$PASS" --cap=400000000 --wallcap=260 --memo-power=22 \
  > "$OUTDIR/$K.$PASS.txt" 2>&1
rc=$?
echo "rc=$rc" >> "$OUTDIR/$K.$PASS.txt"
exit $rc
