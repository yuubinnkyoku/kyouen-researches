#!/bin/bash
# ladder.sh — resume-safe per-key probe ladder for the fourth-cost batch.
# usage: ladder.sh <w2dir> <ord1> [ord2 ...]
# Serial execution (one node process at a time): the sandbox has died before
# under 2 concurrent 2^22-entry PnTT solvers, so we keep memory headroom.
# per key kNN: at2m (2M) -> if UNKNOWN: at15m-run1 -> at15m-run2 (both recorded).
set -u
W="$1"; shift
IN="$W/probe/input"; RAW="$W/probe/raw"; JS="$W/inputs/jsreplay.js"
mkdir -p "$RAW"
run_stage() { # $1=order $2=tag $3=budget
  local o=$1 tag=$2 bud=$3 f n
  n=$(printf '%02d' "$o")
  f="$RAW/at${tag}-k${n}.out.csv"
  if [ -s "$f" ]; then echo "skip $o $tag" >> "$W/probe/status.log"; return 0; fi
  node "$JS" --exact-replay="$IN/k${n}.input.csv" \
    --exact-replay-budget="$bud" > "$f" 2>/dev/null
  echo "done $o $tag rc=$?" >> "$W/probe/status.log"
}
get_result() { # $1=file -> print result (or -1)
  awk -F, '/^replay,/{print $7; exit}' "$1" 2>/dev/null || echo -1
}
for o in "$@"; do
  n=$(printf '%02d' "$o")
  run_stage "$o" 2m 2000000
  res=$(get_result "$RAW/at2m-k${n}.out.csv")
  if [ "$res" = "0" ]; then
    run_stage "$o" 15m-run1 15000000
    run_stage "$o" 15m-run2 15000000
  fi
  echo "key $n status=done res2m=$res" >> "$W/probe/status.log"
done
