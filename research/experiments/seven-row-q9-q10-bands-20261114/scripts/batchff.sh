#!/bin/bash
# batchff.sh — run leanff.sh for W M Q over m in [MSTART,MEND] with a wall-clock budget.
# Stops cleanly after the budget so a 240s-capped command can resume later.
# Usage: ./batchff.sh W Q OUTDIR MSTART MEND BUDGET_S [LEX] [PAR]
#   PAR: parallel instances (default 2). Progress state in $OUT/progress.txt.
set -u
W=$1; Q=$2; OUT=$3; MSTART=$4; MEND=$5; BUDGET=$6
LEX=${7:-none}
PAR=${8:-2}
LFF=/home/user/krwork/seven/leanff.sh
mkdir -p "$OUT"
T0=$(date +%s)
M=$MSTART
DONE=0
while [ "$M" -le "$MEND" ]; do
  NOW=$(date +%s)
  ELAPSED=$((NOW - T0))
  LEFT=$((BUDGET - ELAPSED))
  if [ "$LEFT" -lt 45 ]; then echo "BUDGET_STOP m=$M elapsed=${ELAPSED}s done=$DONE"; break; fi
  TAG="s${W}x${M}q${Q}_$(echo "$LEX" | tr -d ',')"
  if [ -f "$OUT/$TAG.kissat.txt" ]; then M=$((M+1)); continue; fi
  # launch up to PAR instances
  PIDS=""
  LAUNCHED=0
  while [ "$LAUNCHED" -lt "$PAR" ] && [ "$M" -le "$MEND" ]; do
    TAG="s${W}x${M}q${Q}_$(echo "$LEX" | tr -d ',')"
    if [ ! -f "$OUT/$TAG.kissat.txt" ]; then
      bash "$LFF" "$W" "$M" "$Q" "$OUT" "$LEX" "$LEFT" > "$OUT/$TAG.launch.log" 2>&1 &
      PIDS="$PIDS $!"
      LAUNCHED=$((LAUNCHED+1))
    fi
    M=$((M+1))
  done
  for P in $PIDS; do wait "$P"; DONE=$((DONE+1)); done
  echo "$M" > "$OUT/progress.txt"
done
echo "BATCH_DONE next_m=$M done_this_run=$DONE elapsed=$(( $(date +%s) - T0 ))s"
