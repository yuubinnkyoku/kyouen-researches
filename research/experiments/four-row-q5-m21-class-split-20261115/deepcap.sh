#!/bin/bash
# Deep-cap decision on the two remaining INDET buckets of the (4,21,5) sweep.
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=2400
OUT=output
for key in c0k3p0 c0k3p1; do
  grep -s -q "\"key\":\"$key\"" "$OUT/records.jsonl" && \
    grep -s "\"key\":\"$key\"" "$OUT/records.jsonl" | grep -s -q '"result":"\(SAT\|UNSAT\)"' && continue
  y=${key:1:1}; p=${key:6}
  cnf="$OUT/${key}_deep.cnf"; log="$OUT/${key}_deep.txt"
  node scripts/sat3.js 4 21 5 --class="$y" --krow=$y:3 --minpos=$p "$cnf"
  md5=$(md5sum "$cnf" | awk '{print $1}')
  t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":4,\"m\":21,\"q\":5,\"class\":\"$y\",\"extra\":\"--krow=$y:3 --minpos=$p\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
  if [ "$res" = "SAT" ]; then
    grep "^v " "$log" > "$OUT/${key}_deep.model.txt"
    node scripts/sat3.js decode 4 21 5 "$OUT/${key}_deep.model.txt" --json="$OUT/${key}_deep.witness.json" > "$OUT/${key}_deep.decode.txt" 2>&1
  fi
  rm -f "$cnf"
done
echo "DEEPCAP_DONE $(date -u +%FT%TZ)"
