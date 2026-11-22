#!/bin/bash
# usage: runbatch.sh b001 b002 ...   (key ids from input/)
# Two-pass fresh cold replay per key, 2 workers max (2-core host).
# HARD-STOP on determinism mismatch. Status appended to output/status.log
set -u
BUDGET=15000000
cd "$(dirname "$0")/.."
run_key() {
  local k="$1"
  local missing=0
  [ -f "output/raw/$k.p1.out" ] || { : > "output/raw/$k.p1.out.tmp"; missing=1; }
  if ! [ -f "output/raw/$k.p1.out" ]; then
    node scripts/jsreplay.js --exact-replay="input/$k.input.csv" --exact-replay-budget=$BUDGET > "output/raw/$k.p1.out" 2>&1 || { echo "P1-FAIL $k"; exit 43; }
  fi
  if ! [ -f "output/raw/$k.p2.out" ]; then
    node scripts/jsreplay.js --exact-replay="input/$k.input.csv" --exact-replay-budget=$BUDGET > "output/raw/$k.p2.out" 2>&1 || { echo "P2-FAIL $k"; exit 44; }
  fi
  rm -f "output/raw/$k.p1.out.tmp"
  local r1 r2 f1 f2
  r1=$(grep "^replay," "output/raw/$k.p1.out")
  r2=$(grep "^replay," "output/raw/$k.p2.out")
  f1=$(echo "$r1" | cut -d, -f6,7,8)
  f2=$(echo "$r2" | cut -d, -f6,7,8)
  if [ "$f1" == "$f2" ]; then
    echo "$(date -u +%FT%TZ) $k PASS $f2" >> output/status.log
    echo "$k PASS $f2"
  else
    echo "$(date -u +%FT%TZ) $k MISMATCH p1=$f1 p2=$f2" >> output/status.log
    echo "HARD-STOP: determinism mismatch on $k"
    exit 42
  fi
  # WIN detection: result field 7 == 1 -> halt batch (pre-registered stop rule)
  local res
  res=$(echo "$r1" | cut -d, -f7)
  if [ "$res" == "1" ]; then
    echo "$(date -u +%FT%TZ) $k WIN-HALT" >> output/status.log
    echo "WIN-HALT $k"
    exit 45
  fi
}
for k in "$@"; do run_key "$k"; done
