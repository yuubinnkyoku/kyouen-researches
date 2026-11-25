#!/bin/bash
# hardbatch.sh — hardzone.sh for consecutive widths with an adaptive wall-clock guard.
# The guard is ADAPTIVE: the projection for the next width is the measured duration of
# the previous width + 40s slack (hard-zone widths can each take up to CAP1+CAP2+gen,
# so a fixed projection would either never start or overrun).
# Usage: ./hardbatch.sh W Q START END OUTDIR [GUARD_S]
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; GUARD=${6:-240}
DIR=$(dirname "$0")
T0=$(date +%s)
LASTDUR=0
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s)
  ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  PROJ=$((LASTDUR+40))
  if [ $((ELAPSED+PROJ)) -gt $((GUARD+35)) ]; then echo "PROJ_STOP before m=$M (elapsed ${ELAPSED}s, projected +${PROJ}s)"; break; fi
  W0=$(date +%s)
  "$DIR/hardzone.sh" "$W" "$M" "$Q" "$OUT" | tail -1
  W1=$(date +%s)
  LASTDUR=$((W1-W0))
done
echo "BATCH_DONE"
