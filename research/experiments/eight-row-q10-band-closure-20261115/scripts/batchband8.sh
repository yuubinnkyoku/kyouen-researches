#!/bin/bash
# batchband8.sh — leanband8.sh for consecutive widths with a wall-clock guard.
# Usage: ./batchband8.sh W Q START END OUTDIR CAP GUARD_S
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; CAP=$6; GUARD=${7:-250}
DIR=$(dirname "$0")
T0=$(date +%s)
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s); ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  if [ $((ELAPSED+CAP+20)) -gt $((GUARD+40)) ]; then echo "PROJ_STOP before m=$M (elapsed ${ELAPSED}s)"; break; fi
  "$DIR/leanband8.sh" "$W" "$M" "$Q" "$OUT" "$CAP" | tail -1
done
echo "BATCH_DONE"
