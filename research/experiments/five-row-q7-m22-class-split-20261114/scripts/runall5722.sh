#!/bin/bash
# five-row q=7 m=22 witness-free sweep by class-split SAT (kissat 4.0.4 at $KISSAT).
# Completion driver of the 2026-11-14 batch-1 lane (takeover, fast lane 2026-11-15):
# the 17 direct classes were already decided UNSAT by batch-1 and are re-run here for
# bit-exact reproduction; {0},{1} are decided by the complete k x minpos decomposition
# (k=0..4 exact row count; k=5 x minpos=0..10 sound column-mirror split: the leftmost
# stone of the first deficient row is pinned at column P, and every configuration or
# its column mirror has leftmost stone column <= (m-1)/2 = 10 for m=22).
set -eu
KISSAT=${KISSAT:-/home/user/kr67/bin/kissat}
OUT=${OUT:-../output}
run(){ local cnf=$1 log=$2; timeout "${T:-260}" "$KISSAT" "$cnf" > "$log" 2>&1 || true; }
# 17 direct classes (bit-exact re-run of the batch-1 logs)
for D in 2 0,1 0,2 0,3 0,4 1,2 1,3 0,1,2 0,1,3 0,1,4 0,2,3 0,2,4 1,2,3 0,1,2,3 0,1,2,4 0,1,3,4 0,1,2,3,4; do
  N=$(echo "$D" | tr -d ',')
  node sat3.js 5 22 7 --class="$D" "$OUT/c5x22q7_$N.cnf" > /dev/null
  T=260 run "$OUT/c5x22q7_$N.cnf" "$OUT/r5x22q7_c$N.txt"
done
# {0},{1}: complete k x minpos decomposition
for y in 0 1; do
  for k in 0 1 2 3 4; do
    node sat3.js 5 22 7 --class=$y --krow=$y:$k "$OUT/c5x22q7_${y}k${k}.cnf" > /dev/null
    T=260 run "$OUT/c5x22q7_${y}k${k}.cnf" "$OUT/r5x22q7_${y}k${k}.txt"
  done
  for p in 0 1 2 3 4 5 6 7 8 9 10; do
    node sat3.js 5 22 7 --class=$y --krow=$y:5 --minpos=$p "$OUT/c5x22q7_${y}k5p${p}.cnf" > /dev/null
    T=260 run "$OUT/c5x22q7_${y}k5p${p}.cnf" "$OUT/r5x22q7_${y}k5p${p}.txt"
  done
done
# lex=H cross-encoding re-checks (column-reflection lex-leader, class-preserving)
node sat3.js 5 22 7 --class=0,1 --lex=H "$OUT/c5x22q7_01_lexH.cnf" > /dev/null
T=260 run "$OUT/c5x22q7_01_lexH.cnf" "$OUT/r5x22q7_c01_lexH.txt"
node sat3.js 5 22 7 --class=2 --lex=H "$OUT/c5x22q7_2_lexH.cnf" > /dev/null
T=260 run "$OUT/c5x22q7_2_lexH.cnf" "$OUT/r5x22q7_c2_lexH.txt"
# positive control: 5x18 class {0} must be SAT (K0332 29-stone witness board)
node sat3.js 5 18 7 --class=0 "$OUT/c5x18q7_0.cnf" > /dev/null
T=260 run "$OUT/c5x18q7_0.cnf" "$OUT/r_ctrl_5x18_c0.txt"
node sat3.js decode 5 18 7 "$OUT/r_ctrl_5x18_c0.txt"
# records.jsonl / summary.json (direct-class logs = batch-1 raw logs in this output dir)
node mkrecords5722.js "$OUT" "$OUT"
