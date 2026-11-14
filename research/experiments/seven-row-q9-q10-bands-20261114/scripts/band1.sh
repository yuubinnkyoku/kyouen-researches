#!/bin/bash
# band1.sh — one (w,m,q) def+lex instance: fastsat calibration + kissat independent verdict.
# Usage: ./band1.sh W M Q LEX OUTDIR
set -u
W=$1; M=$2; Q=$3; LEX=$4; OUT=$5
mkdir -p "$OUT"
LARGS="--lex=$LEX"
LTAG=$(echo "$LEX" | tr -d ',')
TAG="c${W}x${M}q${Q}_${LTAG}"
CNF="$OUT/$TAG.cnf"
FSOUT="$OUT/$TAG.fastsat.txt"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node --max-old-space-size=6144 /home/user/krwork/seven/scripts/sat2.js "$W" "$M" "$Q" --deficient $LARGS "$CNF")
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
node /home/user/krwork/seven/scripts/fastsat.js "$CNF" --maxseconds=275 --model="$OUT/$TAG.model.txt" > "$FSOUT" 2>&1
T1=$(date +%s.%N)
FSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
FSSTAT=$(tail -1 "$FSOUT" | jq -r '.status')
FSCONF=$(tail -1 "$FSOUT" | jq -r '.conflicts')
T0=$(date +%s.%N)
timeout 275 /home/user/krwork/kissat-4.0.4-linux-amd64 "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"vars\":$(echo "$META" | jq -r '.vars'),\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"fastsat\":{\"status\":\"$FSSTAT\",\"conflicts\":$FSCONF,\"sec\":$FSEC},\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC},\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$OUT/records.jsonl"
echo "$REC"
