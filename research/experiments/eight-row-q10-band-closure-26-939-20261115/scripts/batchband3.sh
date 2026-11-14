#!/bin/bash
# batchband3.sh — leanband3.sh for consecutive widths with a wall-clock guard.
# Usage: ./batchband3.sh W Q START END OUTDIR [GUARD_S]
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; GUARD=${6:-240}
DIR=$(dirname "$0")
T0=$(date +%s)
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s)
  ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  # genfast3 gen cost ~ O(m^2) (measured: m=26 def 0.0s, m=32 def 0.1s, m=939 projected ~30s)
  # + kissat solve; project ~4s per width for the post-transition band.
  PROJ=4
  if [ $((ELAPSED+PROJ)) -gt $((GUARD+35)) ]; then echo "PROJ_STOP before m=$M (elapsed ${ELAPSED}s, projected +${PROJ}s)"; break; fi
  "$DIR/leanband3.sh" "$W" "$M" "$Q" "$OUT" | tail -1
done
echo "BATCH_DONE"
