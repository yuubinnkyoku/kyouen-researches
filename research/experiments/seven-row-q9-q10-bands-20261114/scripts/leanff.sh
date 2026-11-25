#!/bin/bash
# leanff.sh — one (w,m,q) def-mode instance: genff.js CNF + kissat 4.0.4 verdict.
# Same contract as lean2.sh but encodes with genff.js (same-row-pair-pair census,
# ~30-70x faster than genfast.js at m in the hundreds; CNF byte-identical — see
# scripts/genff-verification.md). Use for the m=101+ band extensions; CNF files are
# deleted after the kissat run (only kissat.txt + records.jsonl are kept).
# SAT -> decode + dual verify (decode_verify.js + verify_witness.py).
# Usage: ./leanff.sh W M Q OUTDIR [LEX] [KSTIMEOUT]
set -u
W=$1; M=$2; Q=$3; OUT=$4; LEX=${5:-none}; KSTO=${6:-180}
GF=$(dirname "$0")/genff.js
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
DV=$(dirname "$0")/decode_verify.js
VW=/home/user/krwork/seven/scripts/verify_witness.py
mkdir -p "$OUT"
if [ "$LEX" = "none" ]; then LARGS=""; else LARGS="--lex=$LEX"; fi
TAG="s${W}x${M}q${Q}_$(echo "$LEX" | tr -d ',')"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
T0=$(date +%s.%N)
META=$(node "$GF" "$W" "$M" "$Q" --deficient $LARGS "$CNF") || { echo "GENFF_FAIL $TAG"; exit 1; }
T1=$(date +%s.%N)
GSEC=$(awk -v a="$T0" -v b="$T1" 'BEGIN{printf "%.1f", b-a}')
T2=$(date +%s.%N)
timeout "$KSTO" "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T3=$(date +%s.%N)
rm -f "$CNF"
KSEC=$(awk -v a="$T2" -v b="$T3" 'BEGIN{printf "%.1f", b-a}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"gen_sec\":$GSEC,\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
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
