#!/bin/bash
# run_one.sh — one (7,m,6,class) sat3.js class-split instance, resumable unit runner.
# Usage: KEY=<key> CAP=<sec> ./run_one.sh <key> <w> <m> <Dspec> [extra sat3.js opts]
# Writes one JSONL record to output/records.jsonl; skips if the key already has a record.
# kissat rc 10 = SAT, 20 = UNSAT, else INDET (cap/OOM). CNF regenerated deterministically.
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=${CAP:-600}
OUT=output
key=$1; W=$2; M=$3; Dspec=$4; extra=${5:-}
mkdir -p "$OUT"
if grep -s -q "\"key\":\"$key\"" "$OUT/records.jsonl"; then echo "SKIP $key"; exit 0; fi
cnf="$OUT/${key}.cnf"; log="$OUT/${key}.txt"
meta=$(node --max-old-space-size=6144 scripts/sat3.js "$W" "$M" 6 --class="$Dspec" $extra "$cnf") || {
  echo "{\"key\":\"$key\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"; exit 1; }
md5=$(md5sum "$cnf" | awk '{print $1}')
t0=$(date +%s.%N)
timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
rc=$?
t1=$(date +%s.%N)
sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
echo "{\"key\":\"$key\",\"w\":$W,\"m\":$M,\"q\":6,\"class\":\"$Dspec\",\"extra\":\"$extra\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
if [ "$res" = "SAT" ]; then
  grep "^v " "$log" > "$OUT/${key}.model.txt"
  node scripts/sat3.js decode "$W" "$M" 6 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
  jq -c '.stones' "$OUT/${key}.witness.json" | python3 scripts/verify_witness.py "$W" "$M" 6 > "$OUT/${key}.pyverify.json" 2>&1 || true
  echo "SAT_FOUND $key $(date -u +%FT%TZ)"
fi
rm -f "$cnf"
echo "$res $key conflicts=${conf:-na} sec=$sec"
