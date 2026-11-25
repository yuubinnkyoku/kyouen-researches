#!/bin/bash
# leanband.sh — one (w,m,q) def-mode band instance for the m>=101 extension round:
# genfast2.js CNF (integer-keyed census, byte-identical to genfast.js per controls_byteid.json) + kissat 4.0.4
# (200s cap), JSONL record appended to $OUT/records.jsonl, per-width kissat log kept.
# SAT (unexpected) -> decode + dual verify and emit SAT_WITNESS marker.
# Usage: ./leanband.sh W M Q OUTDIR
set -u
W=$1; M=$2; Q=$3; OUT=$4
SCR=$(dirname "$0")
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
DV="$SCR/decode_verify.js"
VW=/home/user/krwork/seven/scripts/verify_witness.py
mkdir -p "$OUT"
TAG="s${W}x${M}q${Q}_none"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 "$SCR/genfast2.js" "$W" "$M" "$Q" --deficient "$CNF")
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout 200 "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
GSEC=$(echo "$META" | jq -r '.gen_sec // empty')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"none\",\"generator\":\"genfast2\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
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
