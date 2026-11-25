#!/bin/bash
# 6x20 q=8 full 35-canonical-class sweep driver (run from the scripts dir; kissat 4.0.4 at $KISSAT).
# Classes: canonical representatives of the 63 non-empty deficiency subsets of {0..5} under row mirror y->5-y.
set -eu
KISSAT=${KISSAT:-/home/user/krwork/kissat}
OUT=${OUT:-../output}
CLASSES="0 1 2 01 02 03 04 05 12 13 14 23 012 013 014 015 023 024 025 034 123 124 0123 0124 0125 0134 0135 0145 0234 0235 1234 12345 02345 01345 012345"
mkdir -p "$OUT"
for D in $CLASSES; do
  CL=$(echo "$D" | sed 's/./&,/g; s/,$//')
  node sat3.js 6 20 8 --class="$CL" "$OUT/c6x20q8_$D.cnf" > "$OUT/c6x20q8_$D.meta.json"
  timeout 285 "$KISSAT" "$OUT/c6x20q8_$D.cnf" > "$OUT/r6x20q8_c$D.txt" 2>&1 || true
done
# cross-encoding re-checks (hardest singleton classes, lex=H column reflection, class-preserving)
for D in 1 2; do
  node sat3.js 6 20 8 --class=$D --lex=H "$OUT/c6x20q8_${D}_lexH.cnf" > /dev/null
  timeout 285 "$KISSAT" "$OUT/c6x20q8_${D}_lexH.cnf" > "$OUT/r6x20q8_c${D}_lexH.txt" 2>&1 || true
done
# positive control: the 6x18 witness board (K0815) must be rediscovered SAT
node sat3.js 6 18 8 --class=1 "$OUT/c6x18q8_1.cnf" > /dev/null
timeout 285 "$KISSAT" "$OUT/c6x18q8_1.cnf" > "$OUT/r_ctrl_6x18_c1.txt" 2>&1 || true
node sat3.js decode 6 18 8 "$OUT/r_ctrl_6x18_c1.txt"
