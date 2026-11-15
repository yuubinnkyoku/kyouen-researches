#!/bin/bash
# Blocker-circle gpin sub-split of the (4,21,5) buckets that resist deep caps.
# Usage: bash sweepp0gpin.sh <bucket>   with bucket in {c0k3p0, c0k3p1}
# Case A: right-end cell (m-1,0) is a stone: one instance, key <bucket>gA.
# Case B: right-end cell empty: maximality forces a count-4 circle g through it;
#   enumerate (g, S) pin instances (sat5.js listcases, adapted: p1 81 / p0 86 cases),
#   keys <bucket>g<ci>, with --emptytail. All-UNSAT over A + B => bucket UNSAT
#   (complete case analysis; see sat5.js header).
# Resumable: key-based skip (SAT/UNSAT done, or already attempted at this CAP).
# Records append to output/records.jsonl with key <bucket>gA / <bucket>g<i>.
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=900
OUT=output
BUCKET=${1:?bucket required}
y=${BUCKET:1:1}; p=${BUCKET:5}; k=3
case "$BUCKET" in
  c0k3p0|c0k3p1) ;;
  *) echo "unknown bucket $BUCKET"; exit 1 ;;
esac

run_case() {
  local key=$1; shift
  if grep -s "\"key\":\"$key\"" "$OUT/records.jsonl"; then
    if grep -s "\"key\":\"$key\"" "$OUT/records.jsonl" | grep -s -q '"result":"\(SAT\|UNSAT\)"'; then return 0; fi
    if grep -s "\"key\":\"$key\"" "$OUT/records.jsonl" | grep -s -q "\"cap\":$CAP"; then return 0; fi
  fi
  local cnf="$OUT/${key}.cnf" log="$OUT/${key}.txt"
  node scripts/sat5.js 4 21 5 --class="$y" --krow=$y:$k --minpos=$p "$@" "$cnf"
  local md5=$(md5sum "$cnf" | awk '{print $1}')
  local t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  local sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  local conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  local res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  local extra="$*"
  echo "{\"key\":\"$key\",\"w\":4,\"m\":21,\"q\":5,\"class\":\"$y\",\"extra\":\"--krow=$y:$k --minpos=$p $extra\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
  if [ "$res" = "SAT" ]; then
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node scripts/sat5.js decode 4 21 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
  fi
  rm -f "$cnf"
}

# Case A: right-end cell is a stone
run_case "${BUCKET}gA" --gpin=$((21-1)):$y

# Case B: right-end cell empty + blocker-circle pins
node scripts/sat5.js listcases 4 21 5 --class=$y --minpos=$p > "$OUT/${BUCKET}.gpin-cases.json"
n=$(node -e 'const a=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(a.caseCount)' "$OUT/${BUCKET}.gpin-cases.json")
for i in $(seq 0 $((n-1))); do
  pins=$(node -e 'const a=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));process.stdout.write(a.cases[Number(process.argv[2])].pins)' "$OUT/${BUCKET}.gpin-cases.json" "$i")
  run_case "${BUCKET}g$i" --emptytail --gpin="$pins"
done
echo "SWEEPP0GPIN_DONE $BUCKET $(date -u +%FT%TZ)"
