#!/bin/bash
# rowsplit.sh — one (w,m,q,rowY) rowfixed instance for the 2026-11-14 high-speed lane.
# CNF: sat2.js --rowY=Y (census encoding identical to lean3.sh's sat2 branch; the
# def-mode OR over the w deficient rows is split by fixing the deficient row).
# Verdict: kissat 4.0.4 (CAP seconds). SAT -> decode_verify.js + verify_witness.py dual verify.
# Record schema: identical to seven-row-q7-witness-search-20261114/output/row-split/records.jsonl.
# Usage: ./rowsplit.sh W M Q Y OUTDIR [CAP]
set -u
W=$1; M=$2; Q=$3; Y=$4; OUT=$5; CAP=${6:-200}
SCR=$(dirname "$0")
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
DV="$SCR/decode_verify.js"
VW="$SCR/verify_witness.py"
mkdir -p "$OUT"
TAG="s${W}x${M}q${Q}_rowY${Y}"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 "$SCR/sat2.js" "$W" "$M" "$Q" --rowY=$Y "$CNF")
GEN=sat2
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout "$CAP" "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"mode\":\"rowfixed\",\"rowY\":$Y,\"lex\":\"none\",\"generator\":\"$GEN\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec_cap\":$CAP}"
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
