#!/bin/bash
# sweep one deficiency class: ./sweep.sh W M Q "D" OUTDIR [TIMEOUT] [EXTRA_ARGS]
# records go to OUTDIR/records.jsonl (serialized via flock-like append of a single line)
set -u
W=$1; M=$2; Q=$3; D=$4; OUT=$5; TMO=${6:-275}; EXTRA=${7:-}
case $OUT in /*) ;; *) OUT=$PWD/$OUT;; esac
mkdir -p "$OUT"
TAG="c${W}x${M}q${Q}_$(echo "$D" | tr ',' '_')"
[ -n "$EXTRA" ] && TAG="${TAG}_$(echo "$EXTRA" | tr ' =:.' '___-')"
CNF="$OUT/$TAG.cnf"
RES="$OUT/$TAG.txt"
cd /home/user/krwork/enc
node sat3.js "$W" "$M" "$Q" --class="$D" $EXTRA "$CNF" > "$OUT/$TAG.meta.json" 2>&1 || { echo "ENCODE_FAIL $D"; exit 3; }
T0=$(date +%s.%N)
timeout "$TMO" /home/user/krwork/kissat "$CNF" > "$RES" 2>&1
RC=$?
T1=$(date +%s.%N)
SEC=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
CONF=$(grep -E "^c conflicts:" "$RES" | tail -1 | awk '{print $3}')
if [ "$RC" = "10" ]; then R=SAT; elif [ "$RC" = "20" ]; then R=UNSAT; else R=INDET; fi
REC='{"w":'"$W"',"m":'"$M"',"q":'"$Q"',"class":"'"$D"'","extra":"'"$EXTRA"'","result":"'"$R"'","rc":'"$RC"',"conflicts":'${CONF:-null}',"seconds":'"$SEC"',"date":"'"$(date -u +%FT%TZ)"'"}'
echo "$REC" > "$OUT/records.$$.tmp"
cat "$OUT/records.$$.tmp" >> "$OUT/records.jsonl" && rm -f "$OUT/records.$$.tmp"
echo "$REC"
