#!/bin/bash
# batchband.sh — run leanband.sh for consecutive widths with a wall-clock guard
# (stop cleanly before the container ~290s hard stop, leaving the rest for the
# next command). Usage: ./batchband.sh W Q START END OUTDIR [GUARD_S]
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; GUARD=${6:-250}
DIR=$(dirname "$0")
T0=$(date +%s)
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s)
  ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  # estimate next gen cost as (M/101)^3 * 22s; skip if projected to burst the guard
  PROJ=$(python3 -c "print(int(22*(($M/101.0)**3)+10))")
  if [ $((ELAPSED+PROJ)) -gt $((GUARD+35)) ]; then echo "PROJ_STOP before m=$M (elapsed ${ELAPSED}s, projected +${PROJ}s)"; break; fi
  ./scripts/leanband.sh "$W" "$M" "$Q" "$OUT" | tail -1
done
echo "BATCH_DONE"
