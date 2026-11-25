#!/bin/bash
# (4,23,5) second-stone x2 sub-split for a resisting bucket c{y}k{2,3}p{p}.
# k=3: B in p+1..21 (m-2); k=2: B in p+1..22 (m-1, k-aware bound).
# Chunk-hardened like runner23.sh (CAP=220, BUDGET=60, kissat copied to /tmp).
# Usage: bash x2gen23.sh <bucket>   e.g. c0k3p0
set -u
KIT="$(cd "$(dirname "$0")" && pwd)"
OUT="$KIT/output"
KS=/tmp/kissat_run/kissat
mkdir -p "$OUT" /tmp/kissat_run
[ -x "$KS" ] || { cp "$KIT/kissat-4.0.4-linux-amd64" "$KS" && chmod +x "$KS"; }
CAP=${CAP:-220}
BUDGET=${BUDGET:-60}
BUCKET=${1:?bucket required, e.g. c0k3p0}
case "$BUCKET" in
  c[01]k[23]p[0-9]*) ;;
  *) echo "bad bucket $BUCKET" >&2; exit 1 ;;
esac
y=${BUCKET:1:1}; k=${BUCKET:3:1}; p=${BUCKET:5}
[ "$p" -le 11 ] || { echo "minpos p=$p out of H-split range (<=11)" >&2; exit 1; }
if [ "$k" = "3" ]; then BMAX=21; else BMAX=22; fi
BMIN=$((p + 1))
T0=$(date +%s)
SATFOUND=0
for B in $(seq "$BMIN" "$BMAX"); do
  key="${BUCKET}b$B"
  if grep -s -q "\"key\":\"$key\",\"w\":4,\"m\":23" "$OUT/records23.jsonl"; then
    grep -s "\"key\":\"$key\"," "$OUT/records23.jsonl" | grep -s -q '"result":"SAT"' && SATFOUND=1
    continue
  fi
  if [ $(( $(date +%s) - T0 )) -ge "$BUDGET" ]; then echo "X2_CHUNK_TIMEOUT $BUCKET at B=$B"; exit 0; fi
  cnf="$OUT/${key}.cnf"; log="$OUT/${key}.txt"
  meta=$(node "$KIT/scripts/sat4.js" 4 23 5 --class="$y" --krow="$y:$k" --minpos="$p" --x2="$B" "$cnf") \
    || { echo "{\"key\":\"$key\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records23.jsonl"; continue; }
  md5=$(md5sum "$cnf" | awk '{print $1}')
  t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":4,\"m\":23,\"q\":5,\"class\":\"$y\",\"extra\":\"--krow=$y:$k --minpos=$p --x2=$B\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records23.jsonl"
  if [ "$res" = "SAT" ]; then
    SATFOUND=1
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node "$KIT/scripts/sat4.js" decode 4 23 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 "$KIT/scripts/verify_witness.py" 4 23 5 > "$OUT/${key}.pyverify.json" 2>&1 || true
    echo "SAT_FOUND $key $(date -u +%FT%TZ)"
    break
  fi
  rm -f "$cnf"
done
echo "X2GEN23_CHUNK_DONE $BUCKET satfound=$SATFOUND $(date -u +%FT%TZ)"
