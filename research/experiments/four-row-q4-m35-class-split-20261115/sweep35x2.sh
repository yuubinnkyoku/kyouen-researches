#!/bin/bash
# sweep35x2.sh — parallel-2 wrapper around the published (4,35,4) class-split sweep driver
# (sweep35.sh, four-row-q4-m35-class-split-20261115). Same keys, same CNF (byte-identical
# md5s), same per-key JSONL record format, same cap semantics (CAP env, default 700).
# Changes vs published driver (operational only): up to 2 pending keys in the same
# published priority order are solved concurrently (2 cores); CNF generations run
# sequentially in the foreground (2-parallel node census builds can OOM in ~2GB RAM),
# then the two kissat runs go in parallel. Records append only for pieces that finish
# inside this call; a killed in-flight piece leaves no record. A failed generation
# records nothing (the piece is simply retried on a later call).
# x2 mode: env X2=1 switches the singleton k>=2 keys to the second-stone position
# split (sat4.js --x2=B), keys "c{y}k2p{p}x2{B}" for the K1208-era resistant buckets;
# coverage accounting: all-UNSAT over B in p+1..34 (krow k=2) proves the bucket.
set -u
cd "$(dirname "$0")"
KS=/home/user/work/q44m35/kissat-4.0.4-linux-amd64
CAP=${CAP:-700}
OUT=output
X2=${X2:-0}
mkdir -p "$OUT"
done_key() { grep -s -q "\"key\":\"$1\"," "$OUT/records.jsonl"; }
gen_key() { # spec -> generates OUT/${key}.cnf ; echoes "W M Dspec extra key"
  local spec=$1
  IFS='|' read -r k W M D E <<< "$spec"
  if [ "$X2" = "1" ] && [[ "$k" == *x2* ]]; then
    local base="${k%%x2*}" p="${k#*k2p}"; p="${p%%x2*}"; local B="${k#*x2}"
    node scripts/sat4.js $W $M 4 --class="$D" $E --x2=$B "$OUT/${k}.cnf" > "$OUT/${k}.gen.meta" 2>/dev/null
  else
    node scripts/sat3.js $W $M 4 --class="$D" $E "$OUT/${k}.cnf" > "$OUT/${k}.gen.meta" 2>/dev/null
  fi
}
solve_one() { # W M Dspec extra key
  local W=$1 M=$2 Dspec=$3 extra=$4 key=$5
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
  return 0
}
ALLKEYS=("ctrl_4x34_c1k2p7|4|34|1|--krow=1:2 --minpos=7")
for y in 1 0; do
  for p in $(seq 0 17); do
    ALLKEYS+=("c${y}k2p${p}|4|35|${y}|--krow=${y}:2 --minpos=${p}")
    if [ "$X2" = "1" ]; then
      for B in $(seq $((p+1)) 34); do
        ALLKEYS+=("c${y}k2p${p}x2${B}|4|35|${y}|--krow=${y}:2 --minpos=${p}")
      done
    fi
  done
done
for D in 0,1 0,2 0,3 1,2 0,1,2 0,1,3 0,1,2,3; do N=$(echo "$D" | tr -d ','); ALLKEYS+=("c${N}|4|35|${D}|"); done
for y in 1 0; do
  for p in $(seq 0 17); do ALLKEYS+=("c${y}k1p${p}|4|35|${y}|--krow=${y}:1 --minpos=${p}"); done
  ALLKEYS+=("c${y}k0|4|35|${y}|--krow=${y}:0")
done
pending=()
for spec in "${ALLKEYS[@]}"; do
  k="${spec%%|*}"
  done_key "$k" || pending+=("$spec")
done
echo "PENDING ${#pending[@]} of ${#ALLKEYS[@]}"
i=0
while [ $i -lt ${#pending[@]} ]; do
  a="${pending[$i]}"; ka="${a%%|*}"
  if ! gen_key "$a"; then
    echo "GENFAIL_A $ka (no record)"; rm -f "$OUT/${ka}.cnf"; i=$((i+1)); continue
  fi
  IFS='|' read -r ka Wa Ma Da Ea <<< "$a"
  b=""
  if [ $((i+1)) -lt ${#pending[@]} ]; then
    b="${pending[$i+1]}"; kb="${b%%|*}"
    if gen_key "$b"; then
      IFS='|' read -r kb Wb Mb Db Eb <<< "$b"
      solve_one "$Wa" "$Ma" "$Da" "$Ea" "$ka" &
      solve_one "$Wb" "$Mb" "$Db" "$Eb" "$kb" &
      wait
      i=$((i+2))
      continue
    else
      echo "GENFAIL_B $kb (no record)"; rm -f "$OUT/${kb}.cnf"; b=""
    fi
  fi
  solve_one "$Wa" "$Ma" "$Da" "$Ea" "$ka"
  i=$((i+1))
done
echo "SWEEP_BATCH_DONE $(date -u +%FT%TZ)"
