#!/bin/bash
# lean3.sh — one (w,m,q) def-mode instance for the 2026-11-14 high-speed lane round 9.
# CNF: genfast.js when q >= w+1 (byte-identical to sat2.js, K0820-validated), else sat2.js.
# Verdict: kissat 4.0.4 (240s cap). SAT -> decode_verify.js + verify_witness.py dual verify.
# Usage: ./lean3.sh W M Q OUTDIR [LEX]
set -u
W=$1; M=$2; Q=$3; OUT=$4; LEX=${5:-none}
SCR=$(dirname "$0")
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
DV="$SCR/decode_verify.js"
VW="$SCR/verify_witness.py"
mkdir -p "$OUT"
if [ "$LEX" = "none" ]; then LARGS=""; else LARGS="--lex=$LEX"; fi
TAG="s${W}x${M}q${Q}_$(echo $LEX | tr -d ',')"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
if [ "$Q" -ge $((W+1)) ]; then
  META=$(node --max-old-space-size=6144 "$SCR/genfast.js" "$W" "$M" "$Q" --deficient $LARGS "$CNF")
  GEN=genfast
else
  META=$(node --max-old-space-size=6144 "$SCR/sat2.js" "$W" "$M" "$Q" --deficient $LARGS "$CNF")
  GEN=sat2
fi
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout 240 "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"generator\":\"$GEN\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
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
