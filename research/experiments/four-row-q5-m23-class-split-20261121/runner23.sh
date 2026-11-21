#!/bin/bash
# (4,23,5) class-split sweep — resumable chunk runner (post-reset hardened).
# Kit dir is persistent (knowledge mount, noexec) -> kissat is copied to /tmp per chunk.
# Chunk budget: start new pieces only within the first BUDGET seconds of the chunk;
# with CAP=220s piece cap the worst-case chunk is ~60+220+ overhead < 300s bash limit.
# Records: output/records23.jsonl (append-only, skip decided keys incl. INDET rows).
# Phase order: k2 -> k1 -> k0 -> multi direct -> k3 direct. INDET = honest negative.
set -u
KIT="$(cd "$(dirname "$0")" && pwd)"
OUT="$KIT/output"
KS=/tmp/kissat_run/kissat
mkdir -p "$OUT" /tmp/kissat_run
[ -x "$KS" ] || { cp "$KIT/kissat-4.0.4-linux-amd64" "$KS" && chmod +x "$KS"; }
[ -x "$KS" ] || { echo "kissat setup failed" >&2; exit 2; }
"$KS" --version >/dev/null 2>&1 || { echo "kissat not runnable" >&2; exit 2; }
CAP=${CAP:-220}
BUDGET=${BUDGET:-60}
T0=$(date +%s)
SATFOUND=0
decided() { grep -s -q "\"key\":\"$1\",\"w\":4,\"m\":23" "$OUT/records23.jsonl"; }
timelp() { [ $(( $(date +%s) - T0 )) -ge "$BUDGET" ]; }
run() { # key Dspec extra...
  local key=$1 Dspec=$2; shift 2
  local extra="$*"
  if decided "$key"; then
    grep -s "\"key\":\"$key\"," "$OUT/records23.jsonl" | grep -s -q '"result":"SAT"' && SATFOUND=1
    return 0
  fi
  timelp && return 9
  local cnf="$OUT/${key}.cnf" log="$OUT/${key}.txt"
  local meta
  meta=$(node "$KIT/scripts/sat3.js" 4 23 5 --class="$Dspec" $extra "$cnf") || { echo "{\"key\":\"$key\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records23.jsonl"; return 1; }
  local md5=$(md5sum "$cnf" | awk '{print $1}')
  local t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  local sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  local conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  local res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":4,\"m\":23,\"q\":5,\"class\":\"$Dspec\",\"extra\":\"$extra\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records23.jsonl"
  if [ "$res" = "SAT" ]; then
    SATFOUND=1
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node "$KIT/scripts/sat3.js" decode 4 23 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 "$KIT/scripts/verify_witness.py" 4 23 5 > "$OUT/${key}.pyverify.json" 2>&1 || true
    echo "SAT_FOUND $key $(date -u +%FT%TZ)"
  fi
  rm -f "$cnf"
  return 0
}
if [ "$SATFOUND" != "1" ]; then
  for k in 2 1; do
    for y in 0 1; do
      for p in $(seq 0 11); do
        run "c${y}k${k}p${p}" "$y" "--krow=$y:$k --minpos=$p" || { [ $? = 9 ] && break 3; }
        [ "$SATFOUND" = "1" ] && break 3
      done
    done
  done
fi
if [ "$SATFOUND" != "1" ]; then
  for y in 0 1; do
    run "c${y}k0" "$y" "--krow=$y:0" || true
    [ "$SATFOUND" = "1" ] && break
  done
fi
if [ "$SATFOUND" != "1" ]; then
  for D in 0,1 0,2 0,3 1,2 0,1,2 0,1,3 0,1,2,3; do
    N=$(echo "$D" | tr -d ',')
    run "c${N}" "$D" "" || { [ $? = 9 ] && break; }
    [ "$SATFOUND" = "1" ] && break
  done
fi
if [ "$SATFOUND" != "1" ]; then
  for y in 0 1; do
    for p in $(seq 0 11); do
      run "c${y}k3p${p}" "$y" "--krow=$y:3 --minpos=$p" || { [ $? = 9 ] && break 2; }
      [ "$SATFOUND" = "1" ] && break 2
    done
  done
fi
echo "RUNNER23_CHUNK_DONE satfound=$SATFOUND rows=$(wc -l < "$OUT/records23.jsonl") $(date -u +%FT%TZ)"
