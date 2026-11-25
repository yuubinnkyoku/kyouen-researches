#!/usr/bin/env bash
# run_class.sh W M Q "D" CAP ABSDIR [extra args...] — encode (if absent) + kissat + JSONL append
set -u
W=$1; M=$2; Q=$3; D=$4; CAP=$5; DIR=$6; shift 6
EXA=$(echo "$@" | tr -cd 'a-zA-Z0-9' | head -c 24)
EXS=$(echo "$@" | tr ' ' '_')
TAG="c${W}x${M}q${Q}_$(echo "$D" | tr ',' '_')${EXS:+_x}${EXS}"
mkdir -p "$DIR/enc" "$DIR/out"
CNF="$DIR/enc/$TAG.cnf"
LOG="$DIR/out/$TAG.txt"
cd /home/user/knowledge/kyouen-research/_q66-m24-lane-kit/scripts
if [ ! -s "$CNF" ]; then node sat3.js "$W" "$M" "$Q" --class="$D" "$@" "$CNF" > "$DIR/enc/$TAG.meta.json" 2>&1 || { echo "ENCODE_FAIL $D"; exit 3; }; fi
T0=$(date +%s)
timeout "$CAP" ${KISSAT:-/home/user/work/kr66/kissat-4.0.4-linux-amd64} "$CNF" > "$LOG" 2>&1
RC=$?
T1=$(date +%s)
CONF=$(grep -E "^c conflicts:" "$LOG" | tail -1 | awk '{print $3}')
if [ "$RC" = "10" ]; then R=SAT; elif [ "$RC" = "20" ]; then R=UNSAT; else R=INDET; fi
EXTRA=$(echo "$*" | tr ' ' '-')
REC="{\"w\":$W,\"m\":$M,\"q\":$Q,\"class\":\"$D\",\"result\":\"$R\",\"rc\":$RC,\"conflicts\":${CONF:-null},\"seconds\":$((T1-T0)),\"cap\":$CAP,\"extra\":\"$EXTRA\",\"date\":\"$(date -u +%FT%TZ)\"}"
echo "$REC" >> "$DIR/records.jsonl"
echo "$REC"
