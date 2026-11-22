#!/bin/bash
# sample35.sh — one-wave (<=2 pieces, CAP env) sampler for category-hardness calibration
# of the (4,35,4) class-split sweep. Records use the published per-key JSONL format and
# append to output/records.jsonl; recorded keys are skipped. Same CNF generators as
# sweep35.sh (sat3.js; sat4.js only for keys carrying x2).
# Usage: CAP=200 bash sample35.sh key:W:M:Dspec:extra [key2:...]
set -u
cd "$(dirname "$0")"
KS=/home/user/work/q44m35/kissat-4.0.4-linux-amd64
CAP=${CAP:-200}
OUT=output
done_key() { grep -s -q "\"key\":\"$1\"," "$OUT/records.jsonl"; }
gen_cnf() { # key W M Dspec extra
  local key=$1 W=$2 M=$3 Ds=$4 ex=$5
  if [[ "$key" == *x2* ]]; then
    local B="${key##*x2}"
    node scripts/sat4.js $W $M 4 --class="$Ds" $ex --x2=$B "$OUT/${key}.cnf" > "$OUT/${key}.gen.meta" 2>/dev/null
  else
    node scripts/sat3.js $W $M 4 --class="$Ds" $ex "$OUT/${key}.cnf" > "$OUT/${key}.gen.meta" 2>/dev/null
  fi
}
solve_one() { # key W M Dspec extra
  local key=$1 W=$2 M=$3 Dspec=$4 extra=$5
  local cnf="$OUT/${key}.cnf" log="$OUT/${key}.txt"
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
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    if [[ "$key" == *x2* ]]; then
      node scripts/sat4.js decode $W $M 4 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    else
      node scripts/sat3.js decode $W $M 4 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    fi
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 scripts/verify_witness.py $W $M 4 > "$OUT/${key}.pyverify.json" 2>&1 || true
    echo "SAT_FOUND $key $(date -u +%FT%TZ)"
  fi
  rm -f "$cnf"
  echo "DONE $key $res conflicts=${conf} sec=${sec}"
}
specs=()
for a in "$@"; do specs+=("$a"); done
pids=()
for spec in "${specs[@]}"; do
  IFS=':' read -r key W M Ds <<< "$spec"
  ex=""
  case "$key" in
    c0k0) ex="--krow=0:0";;
    c1k0) ex="--krow=1:0";;
    c*k1p*) p=$(echo "$key" | sed -E 's/^c(.)k1p([0-9]+)$/\2/'); y=$(echo "$key" | sed -E 's/^c(.)k1p([0-9]+)$/\1/'); ex="--krow=${y}:1 --minpos=${p}";;
    c*k2p*) if [[ "$key" != *x2* ]]; then p=$(echo "$key" | sed -E 's/^c(.)k2p([0-9]+)$/\2/'); y=$(echo "$key" | sed -E 's/^c(.)k2p([0-9]+)$/\1/'); ex="--krow=${y}:2 --minpos=${p}"; fi;;
  esac
  if done_key "$key"; then echo "SKIP $key (recorded)"; continue; fi
  if gen_cnf "$key" "$W" "$M" "$Ds" "$ex"; then
    solve_one "$key" "$W" "$M" "$Ds" "$ex" &
    pids+=($!)
  else
    echo "GENFAIL $key"
  fi
done
[ ${#pids[@]} -gt 0 ] && wait
echo "WAVE_DONE $(date -u +%FT%TZ)"
