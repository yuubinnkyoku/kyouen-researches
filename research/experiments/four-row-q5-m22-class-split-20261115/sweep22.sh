#!/bin/bash
# (4,22,5) class-split k x minpos sweep — resumable driver (fast lane).
# Complete cover: 9 canonical deficiency classes mod V (rows 0<->3, 1<->2):
#   {0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3}
# Singleton classes split by exact deficient-row count k in {0,1,2,3} and, for k>=1,
# by minpos p in 0..10 (sound H-split: min(x1, (m-1)-xk) <= floor((m-1)/2) = 10).
# Multi classes run direct; INDET ones can be krow-decomposed in a follow-up batch.
# Deficiency for q=5: row with <= 3 stones (safe rows hold <= q-1 = 4).
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=${CAP:-600}
OUT=output
mkdir -p "$OUT"
SATFOUND=0
done_key() { grep -s -q "\"key\":\"$1\"" "$OUT/records.jsonl"; }
run() { # key w m Dspec extra
  local key=$1 W=$2 M=$3 Dspec=$4 extra=$5
  done_key "$key" && { grep -s "\"key\":\"$key\"" "$OUT/records.jsonl" | grep -s -q "\"result\":\"SAT\"" && SATFOUND=1; return 0; }
  local cnf="$OUT/${key}.cnf" log="$OUT/${key}.txt"
  local meta
  meta=$(node scripts/sat3.js $W $M 5 --class="$Dspec" $extra "$cnf") || { echo "{\"key\":\"$key\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"; return 1; }
  local md5=$(md5sum "$cnf" | awk '{print $1}')
  local t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  local sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  local conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  local res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":$W,\"m\":$M,\"q\":5,\"class\":\"$Dspec\",\"extra\":\"$extra\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
  if [ "$res" = "SAT" ]; then
    SATFOUND=1
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node scripts/sat3.js decode $W $M 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 scripts/verify_witness.py $W $M 5 > "$OUT/${key}.pyverify.json" 2>&1 || true
    echo "SAT_FOUND $key $(date -u +%FT%TZ)"
  fi
  rm -f "$cnf"
  return 0
}
# --- positive control first: (4,20,5) class {0} k=3 p=1 contains the V-image of the m=20 witness ---
run ctrl_4x20_c0k3p1 4 20 0 "--krow=0:3 --minpos=1"
SATFOUND=0  # control verdict must not abort the sweep (bugfix learned from sweep35.sh)
# --- priority: k=3 slices (witness regime), class {0} then {1} ---
for y in 0 1; do
  for p in $(seq 0 10); do
    [ "$SATFOUND" = "1" ] && break 2
    run "c${y}k3p${p}" 4 22 "$y" "--krow=$y:3 --minpos=$p"
  done
done
# --- multi classes direct ---
for D in 0,1 0,2 0,3 1,2 0,1,2 0,1,3 0,1,2,3; do
  [ "$SATFOUND" = "1" ] && break
  N=$(echo "$D" | tr -d ',')
  run "c${N}" 4 22 "$D" ""
done
# --- k=2, k=1, k=0 singleton splits ---
for k in 2 1; do
  for y in 0 1; do
    for p in $(seq 0 10); do
      [ "$SATFOUND" = "1" ] && break 3
      run "c${y}k${k}p${p}" 4 22 "$y" "--krow=$y:$k --minpos=$p"
    done
  done
done
for y in 0 1; do
  [ "$SATFOUND" = "1" ] && break
  run "c${y}k0" 4 22 "$y" "--krow=$y:0"
done
echo "SWEEP_BATCH_DONE satfound=$SATFOUND $(date -u +%FT%TZ)"
