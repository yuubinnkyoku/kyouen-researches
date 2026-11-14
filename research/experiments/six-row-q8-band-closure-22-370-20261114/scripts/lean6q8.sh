#!/bin/bash
# lean6q8.sh — one (6,m,8) def-mode band instance: genfast3.js chord-pair census
# (q=8=w+2; CNF byte-identical to sat2.js full-census on the controls recorded in
# this experiment's output/controls/) + kissat 4.0.4 (230s cap).
# SAT (unexpected in the band) -> decode + dual verify and emit SAT_WITNESS.
# Usage: ./lean6q8.sh W M Q OUTDIR [LEX]
set -u
W=$1; M=$2; Q=$3; OUT=$4; LEX=${5:-none}
SCR=$(dirname "$0")
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
DV="$SCR/decode_verify.js"
VW=/home/user/krwork/seven/scripts/verify_witness.py
mkdir -p "$OUT"
if [ "$LEX" = "none" ]; then LARGS=""; else LARGS="--lex=$LEX"; fi
TAG="s${W}x${M}q${Q}_$(echo $LEX | tr -d ',')"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 "$SCR/genfast3.js" "$W" "$M" "$Q" --deficient $LARGS "$CNF")
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout 230 "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"generator\":\"genfast3\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
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
