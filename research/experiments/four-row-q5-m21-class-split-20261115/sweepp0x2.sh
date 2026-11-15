#!/bin/bash
# Second-stone x2 sub-split of the (4,21,5) buckets that resist deep caps.
# Usage: bash sweepp0x2.sh <bucket>   with bucket in {c0k3p0, c0k3p1}
#   c0k3p0: row0 = {0, b, c}, b in 1..19   (a=0 pinned by minpos=0)
#   c0k3p1: row0 = {1, b, c}, b in 2..19   (a=1 pinned by minpos=1)
# Complete disjoint case analysis on b: all-UNSAT => bucket UNSAT.
# Resumable: key-based skip (SAT/UNSAT done, or already attempted at this CAP).
# Records append to output/records.jsonl with key <bucket>b<b>.
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=900
OUT=output
BUCKET=${1:?bucket required}
y=${BUCKET:1:1}; p=${BUCKET:5}; k=3
case "$BUCKET" in
  c0k3p0) BMAX=19 ;;
  c0k3p1) BMIN=2; BMAX=19 ;;
  *) echo "unknown bucket $BUCKET"; exit 1 ;;
esac
BMIN=${BMIN:-$((p + 1))}
for b in $(seq $BMIN $BMAX); do
  key="${BUCKET}b$b"
  grep -s -q "\"key\":\"$key\"," "$OUT/records.jsonl" && \
    grep -s "\"key\":\"$key\"," "$OUT/records.jsonl" | grep -s -q '"result":"\(SAT\|UNSAT\)"' && continue
  grep -s "\"key\":\"$key\"," "$OUT/records.jsonl" | grep -s -q "\"cap\":$CAP" && continue
  cnf="$OUT/${key}.cnf"; log="$OUT/${key}.txt"
  node scripts/sat4.js 4 21 5 --class="$y" --krow=$y:$k --minpos=$p --x2=$b "$cnf"
  md5=$(md5sum "$cnf" | awk '{print $1}')
  t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":4,\"m\":21,\"q\":5,\"class\":\"$y\",\"extra\":\"--krow=$y:$k --minpos=$p --x2=$b\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
  if [ "$res" = "SAT" ]; then
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node scripts/sat4.js decode 4 21 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
  fi
  rm -f "$cnf"
done
echo "SWEEPP0X2_DONE $BUCKET $(date -u +%FT%TZ)"
