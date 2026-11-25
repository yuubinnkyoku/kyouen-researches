#!/bin/bash
# sweep one deficiency class: ./sweep1.sh W M Q "D" ABS_OUTDIR
# appends one JSON line to ABS_OUTDIR/records.jsonl and keeps raw kissat output
set -u
W=$1; M=$2; Q=$3; D=$4; OUT=$5
mkdir -p "$OUT"
TAG="c${W}x${M}q${Q}_$(echo "$D" | tr ',' '_')"
CNF="$OUT/$TAG.cnf"
RES="$OUT/$TAG.txt"
cd /home/user/krwork/enc
node sat3.js "$W" "$M" "$Q" --class="$D" "$CNF" > "$OUT/$TAG.meta.json" 2>&1 || { echo "ENCODE_FAIL $D"; exit 3; }
T0=$(date +%s.%N)
timeout 275 /home/user/krwork/kissat "$CNF" > "$RES" 2>&1
RC=$?
T1=$(date +%s.%N)
SEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
CONF=$(grep -E "^c conflicts:" "$RES" | tail -1 | awk '{print $3}')
if [ "$RC" = "10" ]; then R=SAT; elif [ "$RC" = "20" ]; then R=UNSAT; else R=INDET; fi
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"class\":\"$D\",\"result\":\"$R\",\"rc\":$RC,\"conflicts\":${CONF:-null},\"seconds\":$SEC,\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$OUT/records.jsonl"
echo "$REC"
