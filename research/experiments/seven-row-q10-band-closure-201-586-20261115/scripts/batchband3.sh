#!/bin/bash
# batchband3.sh — leanband3.sh for consecutive widths with a wall-clock guard.
# Usage: ./batchband3.sh W Q START END OUTDIR [GUARD_S]
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; GUARD=${6:-250}
DIR=$(dirname "$0")
T0=$(date +%s)
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s)
  ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  # genfast3 gen cost ~ O(m^2): projected from genfast3 at m=201 (~1.0s per 100^2... measured live);
  # use measured calibration factor PROJ_PER_M s per width (kissat solve ~0.2..0.5s included)
  PROJ=4
  if [ $((ELAPSED+PROJ)) -gt $((GUARD+35)) ]; then echo "PROJ_STOP before m=$M (elapsed ${ELAPSED}s, projected +${PROJ}s)"; break; fi
  "$DIR/leanband3.sh" "$W" "$M" "$Q" "$OUT" | tail -1
done
echo "BATCH_DONE"
