#!/bin/bash
set -u
W=$1; M=$2; Q=$3; ROWY=$4; OUT=$5; TMO=${6:-280}
export SEVEN_SCRIPTS=$(cd "$(dirname "$0")" && pwd)/scripts
GF=$SEVEN_SCRIPTS/genfast.js
KS=$(cd "$(dirname "$0")/.." && pwd)/kissat
DV=$SEVEN_SCRIPTS/decode_verify.js
mkdir -p "$OUT"
TAG="s${W}x${M}q${Q}_rowY${ROWY}"
CNF="$OUT/$TAG.cnf"; KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 "$GF" "$W" "$M" "$Q" --deficient --rowY=$ROWY "$CNF")
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N); timeout "$TMO" "$KS" "$CNF" > "$KSOUT" 2>&1; KSRC=$?
T1=$(date +%s.%N); KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
echo "RESULT $TAG $KRES rc=$KSRC conflicts=${KCONF:-null} sec=$KSEC"
if [ "$KRES" = "SAT" ]; then
  grep "^v " "$KSOUT" > "$OUT/$TAG.model.txt"
  DVO=$(node "$DV" "$W" "$M" "$Q" "$OUT/$TAG.model.txt")
  echo "$DVO" > "$OUT/$TAG.witness.json"
  echo "$DVO" | python3 -c "import json,sys;print(json.dumps(json.load(sys.stdin)['stones']))" | python3 "$SEVEN_SCRIPTS/verify_witness.py" "$W" "$M" "$Q"
fi
