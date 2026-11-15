#!/bin/bash
# (4,35,4) class-split k x minpos sweep — resumable driver (fast lane).
# Complete cover: 9 canonical deficiency classes mod V (rows 0<->3, 1<->2):
#   {0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3}
# Singleton classes split by exact deficient-row count k in {0,1,2} and, for k>=1,
# by minpos p in 0..17 (sound H-split: min(x1, (m-1)-xk) <= floor((m-1)/2) = 17).
# Multi classes run direct (deficient rows <= 2 stones each); INDET ones can be
# decomposed by krow pins in a follow-up batch. Cap from env CAP (default 700).
# Every instance appends one JSONL record; the driver skips instances already
# recorded (resumable across environment resets; CNF regeneration is deterministic).
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=${CAP:-700}
OUT=output
mkdir -p "$OUT"
SATFOUND=0
done_key() { grep -s -q "\"key\":\"$1\"" "$OUT/records.jsonl"; }
run() { # key w m Dspec extra
  local key=$1 W=$2 M=$3 Dspec=$4 extra=$5
  done_key "$key" && { grep -s "\"key\":\"$key\"" "$OUT/records.jsonl" | grep -s -q "\"result\":\"SAT\"" && SATFOUND=1; return 0; }
  local cnf="$OUT/${key}.cnf" log="$OUT/${key}.txt"
  local meta
  meta=$(node scripts/sat3.js $W $M 4 --class="$Dspec" $extra "$cnf") || { echo "{\"key\":\"$key\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"; return 1; }
  local md5=$(md5sum "$cnf" | awk '{print $1}')
  local t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  local sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  local conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  local res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":$W,\"m\":$M,\"q\":4,\"class\":\"$Dspec\",\"extra\":\"$extra\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
  if [ "$res" = "SAT" ]; then
    SATFOUND=1
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node scripts/sat3.js decode $W $M 4 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 scripts/verify_witness.py $W $M 4 > "$OUT/${key}.pyverify.json" 2>&1 || true
    echo "SAT_FOUND $key $(date -u +%FT%TZ)"
  fi
  rm -f "$cnf"
  return 0
}
# --- positive control first: (4,34,4) class {1} k=2 p=7 contains the m=34 witness ---
run ctrl_4x34_c1k2p7 4 34 1 "--krow=1:2 --minpos=7"
SATFOUND=0  # bugfix 2026-11-15: control-SAT must not abort the sweep
# --- priority: class {1} k=2 (the historical witness orbit), then {0} k=2 ---
for y in 1 0; do
  for p in $(seq 0 17); do
    [ "$SATFOUND" = "1" ] && break 2
    run "c${y}k2p${p}" 4 35 "$y" "--krow=$y:2 --minpos=$p"
  done
done
# --- multi classes direct ---
for D in 0,1 0,2 0,3 1,2 0,1,2 0,1,3 0,1,2,3; do
  [ "$SATFOUND" = "1" ] && break
  N=$(echo "$D" | tr -d ',')
  run "c${N}" 4 35 "$D" ""
done
# --- k=1 and k=0 singleton splits ---
for y in 1 0; do
  for p in $(seq 0 17); do
    [ "$SATFOUND" = "1" ] && break 2
    run "c${y}k1p${p}" 4 35 "$y" "--krow=$y:1 --minpos=$p"
  done
  [ "$SATFOUND" = "1" ] && break
  run "c${y}k0" 4 35 "$y" "--krow=$y:0"
done
echo "SWEEP_BATCH_DONE satfound=$SATFOUND $(date -u +%FT%TZ)"
