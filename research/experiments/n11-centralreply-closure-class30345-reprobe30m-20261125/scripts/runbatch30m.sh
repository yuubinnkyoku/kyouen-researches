#!/bin/bash
# usage: runbatch30m.sh c001 c002 ...   (key ids from input/)
# Part ES (class 30345 exhausted-6 re-probe, 30M condition).
# Fork of the published batch-38 runner scripts/runbatch.sh (Part EF kit,
# sha256 f591f8c2...).  DISCLOSED DIFF: (1) BUDGET 15000000 -> 30000000 -
# a DIFFERENT condition, chosen precisely because the 6 target keys are
# the batch-38 15M honest-EXHAUSTED rows whose same-condition re-probe is
# banned; NO 15M re-probe of any completed exhaustion row happens anywhere
# in this kit; (2) the WIN-HALT exit-45 branch is removed -> WIN-CONTINUE
# (pre-registered: this batch probes all 6 keys regardless of any WIN; WIN
# rows are logged and are NEVER consumed here - canonical adoption of a WIN
# is the scrutiny-owner C++ second-implementation gate's exclusive right;
# LOSS rows are Part-EM loss-only adoption territory, equally unconsumed).
# Everything else is byte-equivalent to the pinned source: two-pass
# fresh-cold replay per key, the truncated-pass replay_done guard (a
# truncated pass never produced a verdict and is re-run fresh-cold),
# MISMATCH determinism hard-stop rc=42, P1/P2 runner-fail rc=43/44, and
# honest EXHAUSTED labeling (an exhaustion is an honest UNKNOWN at this
# 30M condition and would need a 60M+ different condition or a third
# implementation; no 30M re-probe of a completed 30M exhaustion row).
set -u
BUDGET=30000000
cd "$(dirname "$0")/.."
run_key() {
  local k="$1"
  # host-interruption guard: an existing pass file counts as complete ONLY if it
  # carries its terminal "# replay_done" line (an environment reset can kill a
  # solver mid-write, leaving truncated headers without a verdict; such a file
  # is not evidence and is re-run fresh-cold - a truncated pass never produced
  # a verdict, so the no-same-condition-re-search rule for COMPLETED exhaustion
  # rows is unaffected).  Guard identical to the pinned batch-38 source.
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
  # result field 7: 0 = budget exhaustion (honest UNKNOWN at THIS condition,
  # no same-condition re-probe), 1 = WIN, 2 = LOSS.
  local res
  res=$(echo "$r1" | cut -d, -f7)
  if [ "$res" == "0" ]; then
    echo "$(date -u +%FT%TZ) $k EXHAUSTED $f2" >> output/status.log
    echo "$k EXHAUSTED $f2 (honest UNKNOWN at 30M, no same-condition re-probe)"
    return 0
  fi
  if [ "$res" == "1" ]; then
    echo "$(date -u +%FT%TZ) $k WIN $f2" >> output/status.log
    echo "WIN-CONTINUE $k (unconsumed probe-level WIN; scrutiny C++ gate exclusive for adoption)"
    return 0
  fi
}
for k in "$@"; do run_key "$k"; done
