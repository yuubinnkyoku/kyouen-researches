#!/bin/bash
# hardzone.sh — one (w,m,q) HARD-ZONE band instance, two-stage:
#   stage 1: def-mode CNF + kissat 4.0.4 (CAP1, default 250s)
#   stage 2 (only if stage 1 INDET): def+lex=H,V,HV cross-encoding CNF + kissat (CAP2, default 250s)
# Both stages append a JSONL record to ${OUT}/records.jsonl (a stage-1 INDET is kept as an
# honest negative; stage-2 result carries lex="H,V,HV"). Per-stage kissat logs and CNF
# meta are kept; an unexpected SAT decodes + dual-verifies exactly like leanband3.sh
# (decode_verify.js + verify_witness.py via SEVEN_SCRIPTS) and emits SAT_WITNESS.
# Usage: ./hardzone.sh W M Q OUTDIR   (CAP1 / CAP2 overridable by env)
set -u
W=$1; M=$2; Q=$3; OUT=$4
CAP1=${CAP1:-250}; CAP2=${CAP2:-250}
SCR=$(dirname "$0")
KS=${KISSAT_BIN:-/home/user/work/kissat-4.0.4-linux-amd64}
SEV=${SEVEN_SCRIPTS:-/home/user/work/seven/scripts}
G3=${GENFAST3_JS:-/home/user/work/genfast3.js}
DV=${DV_JS:-"$SEV/decode_verify.js"}
VW="$SEV/verify_witness.py"
mkdir -p "$OUT"

run_stage () {
  LEXREC=$1; FILETAG=$2; LEXARG=$3; CAP=$4
  TAG="s${W}x${M}q${Q}_${FILETAG}"
  CNF="$OUT/$TAG.cnf"
  KSOUT="$OUT/$TAG.kissat.txt"
  META=$(node --max-old-space-size=6144 "$G3" "$W" "$M" "$Q" --deficient $LEXARG "$CNF")
  echo "$META" > "$OUT/$TAG.meta.json"
  T0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$CNF" > "$KSOUT" 2>&1
  KSRC=$?
  T1=$(date +%s.%N)
  KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
  KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
  if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
  VARS=$(echo "$META" | jq -r '.vars')
  REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEXREC\",\"generator\":\"genfast3\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC},\"cap\":$CAP"
  if [ "$KRES" = "SAT" ]; then
    grep "^v " "$KSOUT" > "$OUT/$TAG.model.txt"
    DVO=$(node "$DV" "$W" "$M" "$Q" "$OUT/$TAG.model.txt")
    echo "$DVO" > "$OUT/$TAG.witness.json"
    STONES=$(echo "$DVO" | jq -c '.stones')
    PY=$(printf '%s' "$STONES" | python3 "$VW" "$W" "$M" "$Q")
    JSOK=$(echo "$DVO" | jq -c '{ok: .jsVerify.ok, size: .jsVerify.size, rows: .jsVerify.rows}')
    PYOK=$(printf '%s' "$PY" | jq -c '{ok, n, rows, min_row}')
    REC="$REC,\"witness\":$DVO,\"jsVerify\":$JSOK,\"pyVerify\":$PYOK"
    echo "SAT_WITNESS $TAG"
  fi
  REC="$REC,\"date\":\"$(date -u +%FT%TZ)\"}"
  echo "$REC" >> "$OUT/records.jsonl"
  echo "$REC"
  rm -f "$CNF"
  [ "$KRES" = "SAT" ] && exit 0
  return 0
}

run_stage "none" "none" "" "$CAP1"
S1=$(tail -1 "$OUT/records.jsonl" | jq -r '.kissat.result')
if [ "$S1" = "INDET" ]; then
  run_stage "H,V,HV" "lexHVH" "--lex=H,V,HV" "$CAP2"
fi
echo "HARDZONE_DONE"
