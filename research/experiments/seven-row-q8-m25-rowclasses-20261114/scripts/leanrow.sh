#!/bin/bash
# leanrow.sh — one (w,m,q) rowfixed instance: genfast.js CNF (q>=w+1; byte-identical
# to sat2.js per K0820/K0825 validation) + kissat 4.0.4 verdict (240s cap).
# SAT -> decode_verify.js + verify_witness.py dual verify. Usage:
#   ./leanrow.sh W M Q ROWY OUTDIR [LEX]
# Round 10 continuation of the (7,8) 7x25 row-split: rowY in {0,1,2} were the
# unswept V-mirror classes (K0825 honest negative: rowY=3 only, INDET 250s).
set -u
W=$1; M=$2; Q=$3; ROWY=$4; OUT=$5; LEX=${6:-none}
SCR=$(dirname "$0")
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
DV="$SCR/decode_verify.js"
VW=/home/user/krwork/seven/scripts/verify_witness.py
mkdir -p "$OUT"
if [ "$LEX" = "none" ]; then LARGS=""; else LARGS="--lex=$LEX"; fi
TAG="s${W}x${M}q${Q}_rowY${ROWY}$( [ "$LEX" != "none" ] && echo -n "_$(echo $LEX | tr -d ',')" )"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 "$SCR/genfast.js" "$W" "$M" "$Q" --deficient --rowY=$ROWY $LARGS "$CNF")
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout 240 "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"mode\":\"rowfixed\",\"rowY\":$ROWY,\"generator\":\"genfast\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
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
