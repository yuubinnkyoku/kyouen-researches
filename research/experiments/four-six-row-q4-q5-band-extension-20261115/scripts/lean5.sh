#!/bin/bash
# lean5.sh — one (w,m,q) def-mode or rowY-fixed instance for the 2026-11-15
# four-to-six-row q=4/q=5 band-extension lane. sat3.js streaming census
# (byte-identical to sat2.js on all controls of this lane; crosses the sat2
# OOM wall at (5,4) m>=37 / (6,4) m>=32). kissat 4.0.4 official binary,
# cap from env KSCAP (default 100s). SAT -> decode + js verifyConfig +
# Python Fraction dual verify. CNF deleted after the run; md5 recorded.
# Usage: ./lean5.sh W M Q OUTDIR [LEX] [EXTRA]   EXTRA e.g. --rowY=3
set -u
W=$1; M=$2; Q=$3; OUT=$4; LEX=${5:-H,V,HV}; EXTRA=${6:-}
SCR=$(cd "$(dirname "$0")" && pwd)
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
KSCAP=${KSCAP:-100}
DV="$SCR/decode_verify.js"
VW="$SCR/verify_witness.py"
S3="$SCR/sat3.js"
mkdir -p "$OUT"
LARGS=""; [ "$LEX" != "none" ] && LARGS="--lex=$LEX"
TAG="s${W}x${M}q${Q}_rowY${EXTRA#--rowY=}_$(echo $LEX | tr -d ',')"
[ -z "$EXTRA" ] && TAG="s${W}x${M}q${Q}_$(echo $LEX | tr -d ',')"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
META=$(node "$S3" "$W" "$M" "$Q" --deficient $LARGS $EXTRA "$CNF") || { echo "{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"extra\":\"$EXTRA\",\"generator\":\"sat3\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"; exit 1; }
CNFMD5=$(md5sum "$CNF" | awk '{print $1}')
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout "$KSCAP" "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
VARS=$(echo "$META" | jq -r '.vars')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"lex\":\"$LEX\",\"extra\":\"$EXTRA\",\"generator\":\"sat3\",\"vars\":$VARS,\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"cnf_md5\":\"$CNFMD5\",\"cap\":$KSCAP,\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec\":$KSEC}"
if [ "$KRES" = "SAT" ]; then
  grep "^v " "$KSOUT" > "$OUT/$TAG.model.txt"
  DVO=$(node "$DV" "$W" "$M" "$Q" "$OUT/$TAG.model.txt")
  echo "$DVO" > "$OUT/$TAG.witness.json"
  STONES=$(echo "$DVO" | jq -c '.stones')
  PY=$(printf '%s' "$STONES" | python3 "$VW" "$W" "$M" "$Q")
  JSOK=$(echo "$DVO" | jq -c '{ok: .jsVerify.ok, size: .jsVerify.size, rows: .jsVerify.rows}')
  PYOK=$(printf '%s' "$PY" | jq -c '{ok, n, rows, min_row}')
  REC="$REC,\"witness\":$DVO,\"jsVerify\":$JSOK,\"pyVerify\":$PYOK"
fi
REC="$REC,\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$OUT/records.jsonl"
rm -f "$CNF"
echo "$REC"
