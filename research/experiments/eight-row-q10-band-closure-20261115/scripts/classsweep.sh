#!/bin/bash
# classsweep.sh W M Q CAP GUARD OUTDIR [LISTJSON] — canonical class sweep, resume-safe.
set -u
W=$1; M=$2; Q=$3; CAP=$4; GUARD=$5; OUT=$6; LIST=${7:-/home/user/krwork/canonical_classes_w8.json}
mkdir -p "$OUT"
REC="$OUT/classes-${W}x${M}q${Q}.jsonl"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CF=/home/user/krwork/seven/scripts/classfast.js
T0=$(date +%s)
for D in $(python3 -c "
import json
done=set()
try:
    for l in open('$REC'):
        r=json.loads(l)
        if r['kissat']['result'] in ('UNSAT','SAT'): done.add(tuple(r['class']))
except FileNotFoundError: pass
for c in json.load(open('$LIST')):
    t=tuple(c)
    if t not in done: print(','.join(map(str,t)))
"); do
  NOW=$(date +%s); EL=$((NOW-T0))
  if [ $EL -gt $GUARD ]; then echo "GUARD_STOP (elapsed ${EL}s)"; break; fi
  if [ $((EL+CAP+15)) -gt $((GUARD+45)) ]; then echo "PROJ_STOP (elapsed ${EL}s)"; break; fi
  TAG="s${W}x${M}q${Q}_c$(echo "$D" | tr ',' '-')"
  META=$(node --max-old-space-size=6144 "$CF" "$W" "$M" "$Q" --class="$D" "$OUT/$TAG.cnf")
  S0=$(date +%s.%N)
  timeout $CAP "$KS" "$OUT/$TAG.cnf" > "$OUT/$TAG.kissat.txt" 2>&1
  RC=$?
  S1=$(date +%s.%N)
  SEC=$(echo "$S1 $S0" | awk '{printf "%.1f", $1-$2}')
  RES=INDET; [ $RC = 10 ] && RES=SAT; [ $RC = 20 ] && RES=UNSAT
  CONF=$(grep -E "^c conflicts" "$OUT/$TAG.kissat.txt" | tail -1 | awk '{print $3}')
  V=$(echo "$META" | jq -r '.vars'); CL=$(echo "$META" | jq -r '.clauses')
  echo "{\"w\":$W,\"m\":$M,\"q\":$Q,\"class\":[$D],\"generator\":\"sat3+genfast3-chord\",\"vars\":$V,\"clauses\":$CL,\"kissat\":{\"result\":\"$RES\",\"rc\":$RC,\"conflicts\":${CONF:-null},\"sec\":$SEC},\"cap\":$CAP,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$REC"
  echo "class=[$D] $RES conf=${CONF:-0} ${SEC}s"
  rm -f "$OUT/$TAG.cnf"
  if [ "$RES" = "SAT" ]; then echo "SAT_WITNESS class=[$D] m=$M"; break; fi
done
echo "SWEEP_PASS_DONE"
