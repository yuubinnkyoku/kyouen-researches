#!/bin/bash
# batchband3.sh — run leanband3.sh for consecutive widths with an adaptive wall-clock
# guard (stop cleanly before the container ~290s hard stop, leaving the rest for the
# next command). Per-instance cost estimate = 2x max of last 3 kissat secs + gen,
# floored at 10s; kissat cap 200s bounds the overshoot risk.
# Usage: ./batchband3.sh W Q START END OUTDIR [GUARD_S]
set -u
W=$1; Q=$2; S=$3; E=$4; OUT=$5; GUARD=${6:-235}
DIR=$(dirname "$0")
T0=$(date +%s)
for M in $(seq "$S" "$E"); do
  NOW=$(date +%s)
  ELAPSED=$((NOW-T0))
  if [ "$ELAPSED" -gt "$GUARD" ]; then echo "GUARD_STOP after m=$((M-1)) (elapsed ${ELAPSED}s)"; break; fi
  # adaptive: recent max kissat sec (from records.jsonl tail)
  RECENT=$(tail -3 "$OUT/records.jsonl" 2>/dev/null | jq -r '.kissat.sec // 0' | sort -n | tail -1)
  EST=$(( $(python3 -c "print(max(10, int(2*(${RECENT:-4}+2)))") ))
  if [ $((ELAPSED+EST)) -gt $((GUARD+45)) ]; then echo "EST_STOP before m=$M (elapsed ${ELAPSED}s, est +${EST}s)"; break; fi
  "$DIR/leanband3.sh" "$W" "$M" "$Q" "$OUT" | tail -1
done
echo "BATCH_DONE"
