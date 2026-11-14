#!/bin/bash
# five-row q=7 m=21 witness-free sweep by class-split SAT (kissat 4.0.4 at $KISSAT).
# 19 canonical classes: 17 decided directly; {0},{1} decided by the complete
# k x minpos decomposition (k=0..4 exact row count; k=5 x minpos=0..10 sound
# column-mirror split: min(x1, m-1-x5) <= (m-1)/2 = 10 for m=21).
set -eu
KISSAT=${KISSAT:-/home/user/krwork/kissat}
OUT=${OUT:-../output}
run(){ local cnf=$1 log=$2; timeout "${T:-280}" "$KISSAT" "$cnf" > "$log" 2>&1 || true; }
for D in 0 1 2 0,1 0,2 0,3 0,4 1,2 1,3 0,1,2 0,1,3 0,1,4 0,2,3 0,2,4 1,2,3 0,1,2,3 0,1,2,4 0,1,3,4 0,1,2,3,4; do
  N=$(echo "$D" | tr -d ',')
  node sat3.js 5 21 7 --class="$D" "$OUT/c5x21q7_$N.cnf" > /dev/null
  T=280 run "$OUT/c5x21q7_$N.cnf" "$OUT/r5x21q7_c$N.txt"
done
for y in 0 1; do
  for k in 0 1 2 3 4; do
    node sat3.js 5 21 7 --class=$y --krow=$y:$k "$OUT/c5x21q7_${y}k${k}.cnf" > /dev/null
    T=280 run "$OUT/c5x21q7_${y}k${k}.cnf" "$OUT/r5x21q7_${y}k${k}.txt"
  done
  for p in 0 1 2 3 4 5 6 7 8 9 10; do
    node sat3.js 5 21 7 --class=$y --krow=$y:5 --minpos=$p "$OUT/c5x21q7_${y}k5p${p}.cnf" > /dev/null
    T=285 run "$OUT/c5x21q7_${y}k5p${p}.cnf" "$OUT/r5x21q7_${y}k5p${p}.txt"
  done
done
# lex=H cross-encoding re-checks (column-reflection lex-leader, class-preserving)
node sat3.js 5 21 7 --class=0,1 --lex=H "$OUT/c5x21q7_01_lexH.cnf" > /dev/null
T=285 run "$OUT/c5x21q7_01_lexH.cnf" "$OUT/r5x21q7_c01_lexH.txt"
node sat3.js 5 21 7 --class=2 --lex=H "$OUT/c5x21q7_2_lexH.cnf" > /dev/null
T=285 run "$OUT/c5x21q7_2_lexH.cnf" "$OUT/r5x21q7_c2_lexH.txt"
# positive control: 5x18 class {0} must be SAT (K0332 29-stone witness board)
node sat3.js 5 18 7 --class=0 "$OUT/c5x18q7_0.cnf" > /dev/null
T=285 run "$OUT/c5x18q7_0.cnf" "$OUT/r_ctrl_5x18_c0.txt"
node sat3.js decode 5 18 7 "$OUT/r_ctrl_5x18_c0.txt"
