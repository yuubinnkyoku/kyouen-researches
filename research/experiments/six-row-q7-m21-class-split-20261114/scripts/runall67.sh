#!/bin/bash
# six-row q=7 witness search by class-split SAT (kissat 4.0.4 at $KISSAT).
# Usage: ./runall67.sh M CLASS   e.g. ./runall67.sh 21 2
set -eu
KISSAT=${KISSAT:-/home/user/krwork/kissat}
M=$1; D=$2
OUT=${OUT:-../output}
node sat3.js 6 "$M" 7 --class="$D" "$OUT/c6x${M}q7_$D.cnf" > /dev/null
timeout 280 "$KISSAT" "$OUT/c6x${M}q7_$D.cnf" > "$OUT/r6x${M}q7_c$D.txt" 2>&1 || true
if grep -q "^s SATISFIABLE" "$OUT/r6x${M}q7_c$D.txt"; then
  node sat3.js decode 6 "$M" 7 "$OUT/r6x${M}q7_c$D.txt"
fi
