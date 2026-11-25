#!/bin/bash
# batch6q8.sh — lean6q8.sh for consecutive band widths with a wall-clock guard.
# Usage: ./batch6q8.sh W Q START END OUTDIR [GUARD_S]
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; GUARD=${6:-250}
DIR=$(dirname "$0")
T0=$(date +%s)
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s)
  ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  PROJ=4
  if [ $((ELAPSED+PROJ)) -gt $((GUARD+35)) ]; then echo "PROJ_STOP before m=$M (elapsed ${ELAPSED}s, projected +${PROJ}s)"; break; fi
  "$DIR/lean6q8.sh" "$W" "$M" "$Q" "$OUT" | tail -1
done
echo "BATCH_DONE"
