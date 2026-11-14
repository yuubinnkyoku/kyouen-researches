#!/bin/bash
# lean1.sh — one (w,m,q) def-mode instance: kissat verdict (lean; no fastsat).
# SAT -> decode + dual verify. Usage: ./lean1.sh W M Q OUTDIR [LEX]
set -u
W=$1; M=$2; Q=$3; OUT=$4; LEX=${5:-none}
mkdir -p "$OUT"
if [ "$LEX" = "none" ]; then LARGS=""; else LARGS="--lex=$LEX"; fi
TAG="s${W}x${M}q${Q}_$(echo $LEX | tr -d ',')"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 /home/user/krwork/seven/scripts/sat2.js "$W" "$M" "$Q" --deficient $LARGS "$CNF")
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout 275 /home/user/krwork/kissat-4.0.4-linux-amd64 "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
if [ "$KRES" = "SAT" ]; then
  grep "^v " "$KSOUT" > "$OUT/$TAG.model.txt"
  DV=$(node /home/user/krwork/seven/scripts/decode_verify.js "$W" "$M" "$Q" "$OUT/$TAG.model.txt")
  echo "$DV" > "$OUT/$TAG.witness.json"
  STONES=$(echo "$DV" | jq -c '.stones')
  PY=$(printf '%s' "$STONES" | python3 /home/user/krwork/seven/scripts/verify_witness.py "$W" "$M" "$Q")
  JSOK=$(echo "$DV" | jq -c '{ok: .jsVerify.ok, size: .jsVerify.size, rows: .jsVerify.rows}')
  PYOK=$(printf '%s' "$PY" | jq -c '{ok, n, rows, min_row}')
  REC="$REC,\"witness\":$DV,\"jsVerify\":$JSOK,\"pyVerify\":$PYOK"
fi
REC="$REC,\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$OUT/records.jsonl"
echo "$REC"
