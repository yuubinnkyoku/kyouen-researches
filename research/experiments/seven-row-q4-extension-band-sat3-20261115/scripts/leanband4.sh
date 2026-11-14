#!/bin/bash
# leanband4.sh — one (w,m,q) def-mode instance with the sat3.js streaming census
# (q <= w families; sat2.js all-triples census is byte-identical but OOMs at 7x28+).
# kissat 4.0.4 (200s cap). SAT -> decode + dual verify (decode_verify.js sat.js
# verifyConfig + verify_witness.py Python Fraction). CNF deleted after the run
# (cnf_md5 recorded in the record for auditability).
# Usage: ./leanband4.sh W M Q OUTDIR [LEX]
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
T0=$(date +%s.%N)
META=$(node --max-old-space-size=2560 "$SCR/sat3.js" "$W" "$M" "$Q" --deficient $LARGS "$CNF") || exit 1
T1=$(date +%s.%N)
GEN=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
CNFMD5=$(md5sum "$CNF" | awk '{print $1}')
T0=$(date +%s.%N)
timeout 200 "$KS" "$CNF" > "$OUT/$TAG.kissat.txt" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$OUT/$TAG.kissat.txt" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"generator\":\"sat3\",\"vars\":$(echo "$META" | jq -r .vars),\"clauses\":$(echo "$META" | jq -r .clauses),\"curves\":$(echo "$META" | jq -r .curves),\"cnf_md5\":\"$CNFMD5\",\"gen_sec\":$GEN,\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
if [ "$KRES" = "SAT" ]; then
  grep "^v " "$OUT/$TAG.kissat.txt" > "$OUT/$TAG.model.txt"
  DVO=$(node "$DV" "$W" "$M" "$Q" "$OUT/$TAG.model.txt")
  cp "$OUT/$TAG.model.txt" /dev/null 2>/dev/null
  STONES=$(echo "$DVO" | jq -c '.stones')
  PY=$(printf '%s' "$STONES" | python3 "$VW" "$W" "$M" "$Q")
  JSOK=$(echo "$DVO" | jq -c '{ok: .jsVerify.ok, size: .jsVerify.size, rows: .jsVerify.rows, minRow: ( .jsVerify.rows | min )}')
  PYOK=$(echo "$PY" | jq -c '{ok, n, rows, min_row}')
  WIT=$(echo "$DVO" | jq -c '{nStones, rows, stones}')
  REC="$REC,\"witness\":$WIT,\"jsVerify\":$JSOK,\"pyVerify\":$PYOK"
  echo "$DVO" > "$OUT/$TAG.witness.json"
  echo "SAT_WITNESS $TAG"
fi
REC="$REC,\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$OUT/records.jsonl"
echo "$REC"
rm -f "$CNF"
