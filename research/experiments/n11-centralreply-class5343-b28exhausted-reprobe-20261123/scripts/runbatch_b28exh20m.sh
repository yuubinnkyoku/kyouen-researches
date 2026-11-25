#!/bin/bash
# usage: runbatch.sh c001 c002 ...   (key ids from input/)
# Two-pass fresh cold replay per key, 2 workers max (2-core host).
# HARD-STOP on determinism mismatch. Status appended to output/status.log
set -u
BUDGET=20000000
cd "$(dirname "$0")/.."
run_key() {
  local k="$1"
  # host-interruption guard: an existing pass file counts as complete ONLY if it
  # carries its terminal "# replay_done" line (an environment reset can kill a
  # solver mid-write, leaving truncated headers without a verdict; such a file
  # is not evidence and is re-run fresh-cold - a truncated pass never produced
  # a verdict, so the no-15M-re-search rule for COMPLETED exhaustion rows is
  # unaffected). Guard verified against t002.p2/t003.p2 truncation, 2026-11-22.
  if [ -f "output/raw/$k.p1.out" ] && ! grep -q "# replay_done" "output/raw/$k.p1.out"; then mv "output/raw/$k.p1.out" "output/raw/$k.p1.truncated.$(date -u +%H%M%S).out"; echo "$(date -u +%FT%TZ) $k P1-TRUNCATED-RETRY" >> output/status.log; fi
  if [ -f "output/raw/$k.p2.out" ] && ! grep -q "# replay_done" "output/raw/$k.p2.out"; then mv "output/raw/$k.p2.out" "output/raw/$k.p2.truncated.$(date -u +%H%M%S).out"; echo "$(date -u +%FT%TZ) $k P2-TRUNCATED-RETRY" >> output/status.log; fi
  if ! [ -f "output/raw/$k.p1.out" ]; then
    node scripts/jsreplay.js --exact-replay="input/$k.input.csv" --exact-replay-budget=$BUDGET > "output/raw/$k.p1.out" 2>&1 || { echo "P1-FAIL $k" >> output/status.log; echo "P1-FAIL $k"; exit 43; }
  fi
  if ! [ -f "output/raw/$k.p2.out" ]; then
    node scripts/jsreplay.js --exact-replay="input/$k.input.csv" --exact-replay-budget=$BUDGET > "output/raw/$k.p2.out" 2>&1 || { echo "P2-FAIL $k" >> output/status.log; echo "P2-FAIL $k"; exit 44; }
  fi
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
  # result field 7: 0 = budget exhaustion (honest UNKNOWN, no same-condition
  # re-probe, NOT a stop condition), 1 = WIN (halt batch, pre-registered),
  # 2 = LOSS. jsreplay exits 0 on exhaustion, so the file-based guard above
  # never re-runs an exhausted pass. (batch-17 delta from the published
  # batch-16 script: exhaustion is honestly labeled instead of PASSing.)
  local res
  res=$(echo "$r1" | cut -d, -f7)
  if [ "$res" == "0" ]; then
    echo "$(date -u +%FT%TZ) $k EXHAUSTED $f2" >> output/status.log
    echo "$k EXHAUSTED $f2 (honest UNKNOWN, no same-condition re-probe)"
    return 0
  fi
  if [ "$res" == "1" ]; then
    echo "$(date -u +%FT%TZ) $k WIN-HALT" >> output/status.log
    echo "WIN-HALT $k"
    exit 45
  fi
}
for k in "$@"; do run_key "$k"; done
