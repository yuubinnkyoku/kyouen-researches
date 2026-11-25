#!/bin/bash
# rowfrontier.sh — one (w,m,q) def-mode or rowfixed instance for the 2026-11-15
# high-speed lane (seven-row q<=w frontier SAT search).
# CNF: sat3.js streaming census (byte-identical to sat2.js on published controls;
# q<=w families; --deficient = OR over the w deficient rows, --rowY=Y fixes the
# deficient row = the mirror-class split used by seven-row-q5-q6-frontier-row-split).
# Solver: kissat 4.0.4 official prebuilt (CAP seconds). SAT -> decode_verify.js
# (sat.js verifyConfig) + verify_witness.py (Python Fraction) dual verify.
# CNF deleted after the run (cnf_md5 recorded). meta saved as TAG.meta.json.
# Usage: ./rowfrontier.sh W M Q OUTDIR [CAP] [MODEARGS...]
#   MODEARGS: def          (default)  -> sat3.js --deficient
#             rowY=K                 -> sat3.js --rowY=K
#             lex=H                  -> sat3.js --deficient --lex=H
# Example: ./rowfrontier.sh 7 33 5 out/q5-m33-rowY0 250 rowY=0
set -u
W=$1; M=$2; Q=$3; OUT=$4; CAP=${5:-200}; MODEARG=${6:-def}
SCR=$(dirname "$0")
KS=/home/user/kr/bin/kissat
DV="$SCR/decode_verify.js"
VW="$SCR/verify_witness.py"
mkdir -p "$OUT"
case "$MODEARG" in
  def)    GENARGS="--deficient"; TAGMODE="def";;
  lex=*)  GENARGS="--deficient --lex=${MODEARG#lex=}"; TAGMODE="lex${MODEARG#lex=}";;
  rowY=*) GENARGS="--rowY=${MODEARG#rowY=}"; TAGMODE="rowY${MODEARG#rowY=}";;
  *) echo "bad MODEARG $MODEARG"; exit 2;;
esac
TAG="s${W}x${M}q${Q}_${TAGMODE}"
CNF="$OUT/$TAG.cnf"
KSOUT="$OUT/$TAG.kissat.txt"
T0=$(date +%s.%N)
META=$(node --max-old-space-size=2560 "$SCR/sat3.js" "$W" "$M" "$Q" $GENARGS "$CNF") || { echo "GEN FAIL"; exit 1; }
T1=$(date +%s.%N)
GEN=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
CNFMD5=$(md5sum "$CNF" | awk '{print $1}')
echo "$META" > "$OUT/$TAG.meta.json"
T0=$(date +%s.%N)
timeout "$CAP" "$KS" "$CNF" > "$KSOUT" 2>&1
KSRC=$?
T1=$(date +%s.%N)
KSEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
KCONF=$(grep -E "^c conflicts" "$KSOUT" | tail -1 | awk '{print $3}')
if [ "$KSRC" = "10" ]; then KRES=SAT; elif [ "$KSRC" = "20" ]; then KRES=UNSAT; else KRES=INDET; fi
MODE=$( [ "$TAGMODE" = "def" ] && echo deficient || ([ "${TAGMODE#rowY}" != "$TAGMODE" ] && echo rowfixed || echo deficient) )
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"mode\":\"$MODE\",\"rowY\":$( [ "${TAGMODE#rowY}" != "$TAGMODE" ] && echo "${TAGMODE#rowY}" || echo null),\"lex\":\"none\",\"generator\":\"sat3\",\"vars\":$(echo "$META" | jq -r '.vars'),\"clauses\":$(echo "$META" | jq -r '.clauses'),\"curves\":$(echo "$META" | jq -r '.curves'),\"cnf_md5\":\"$CNFMD5\",\"gen_sec\":$GEN,\"kissat\":{\"result\":\"$KRES\",\"rc\":$KSRC,\"conflicts\":${KCONF:-null},\"sec_cap\":$CAP,\"sec\":$KSEC}"
if [ "$KRES" = "SAT" ]; then
  grep "^v " "$KSOUT" > "$OUT/$TAG.model.txt"
  DVO=$(node "$DV" "$W" "$M" "$Q" "$OUT/$TAG.model.txt")
  echo "$DVO" > "$OUT/$TAG.witness.json"
  STONES=$(echo "$DVO" | jq -c '.stones')
  PY=$(printf '%s' "$STONES" | python3 "$VW" "$W" "$M" "$Q")
  JSOK=$(echo "$DVO" | jq -c '{ok: .jsVerify.ok, size: .jsVerify.size, rows: .jsVerify.rows}')
  PYOK=$(printf '%s' "$PY" | jq -c '{ok, n, rows, min_row}')
  WIT=$(echo "$DVO" | jq -c '{nStones, rows, stones}')
  REC="$REC,\"witness\":$WIT,\"jsVerify\":$JSOK,\"pyVerify\":$PYOK"
  echo "SAT_WITNESS $TAG"
fi
REC="$REC,\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$OUT/records.jsonl"
echo "$REC"
rm -f "$CNF"
