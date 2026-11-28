#!/bin/bash
set -u
W=$1; M=$2; Q=$3; CLS=$4; KROW=$5; MP=$6; OUT=$7; TMO=${8:-280}
export SEVEN_SCRIPTS=$(cd "$(dirname "$0")" && pwd)/scripts
S3=$SEVEN_SCRIPTS/sat3.js
KS=$(cd "$(dirname "$0")/.." && pwd)/kissat
mkdir -p "$OUT"
TAG="c${CLS}k${KROW/:/}p${MP}"
CNF="$OUT/r${W}x${M}q${Q}_${TAG}.cnf"; KSOUT="$OUT/r${W}x${M}q${Q}_${TAG}.txt"
META=$(node --max-old-space-size=6144 "$S3" "$W" "$M" "$Q" --class="$CLS" --krow="$KROW" --minpos="$MP" "$CNF")
echo "$META" > "$OUT/meta_${TAG}_${M}.json"
T0=$(date +%s.%N); timeout "$TMO" "$KS" "$CNF" > "$KSOUT" 2>&1; KSRC=$?
T1=$(date +%s.%N); KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
echo "RESULT w$W m$M class$CLS krow$KROW minpos$MP -> $KRES rc=$KSRC conflicts=${KCONF:-null} sec=$KSEC"
if [ "$KRES" = "SAT" ]; then
  grep "^v " "$KSOUT" > "$OUT/model_${TAG}_${M}.txt"
  node "$S3" decode "$W" "$M" "$Q" "$OUT/model_${TAG}_${M}.txt" > "$OUT/witness_${TAG}_${M}.json" 2>&1
  head -c 400 "$OUT/witness_${TAG}_${M}.json"; echo
fi
