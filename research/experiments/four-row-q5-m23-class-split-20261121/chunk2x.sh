#!/bin/bash
# chunk2x.sh — 2-way parallel chunk driver for the (4,23,5) x2 residual sweep.
# Semantics identical to x2gen23.sh (same records schema, same skip/resume rule,
# same cap semantics: INDET = honest negative at cap), except it runs TWO
# undecided consecutive B values of one bucket concurrently (2 cores) and
# appends both records afterwards (serial append keeps JSONL intact).
# CNF generation is deterministic (sat4.js); kissat is single-threaded and
# conflict counts are deterministic per instance; only wall sec varies.
# Usage: bash chunk2x.sh <bucket>   e.g. c0k3p0    (env CAP default 250)
set -u
KIT="$(cd "$(dirname "$0")" && pwd)"
OUT="$KIT/output"
KS=/tmp/kissat_run/kissat
mkdir -p "$OUT" /tmp/kissat_run
[ -x "$KS" ] || { cp "$KIT/kissat-4.0.4-linux-amd64" "$KS" && chmod +x "$KS"; }
CAP=${CAP:-250}
BUCKET=${1:?bucket required, e.g. c0k3p0}
case "$BUCKET" in
  c[01]k[23]p[0-9]*) ;;
  *) echo "bad bucket $BUCKET" >&2; exit 1 ;;
esac
y=${BUCKET:1:1}; k=${BUCKET:3:1}; p=${BUCKET:5}
[ "$p" -le 11 ] || { echo "minpos p=$p out of H-split range (<=11)" >&2; exit 1; }
if [ "$k" = "3" ]; then BMAX=21; else BMAX=22; fi
BMIN=$((p + 1))

# pick next two undecided B values
PICK=()
for B in $(seq "$BMIN" "$BMAX"); do
  key="${BUCKET}b$B"
  if grep -s -q "\"key\":\"$key\",\"w\":4,\"m\":23" "$OUT/records23.jsonl"; then continue; fi
  PICK+=("$B")
  [ "${#PICK[@]}" -ge 2 ] && break
done
if [ "${#PICK[@]}" -eq 0 ]; then echo "X2_BUCKET_COMPLETE $BUCKET $(date -u +%FT%TZ)"; exit 0; fi

run_one() {
  B=$1
  key="${BUCKET}b$B"
  cnf="$OUT/${key}.cnf"; log="$OUT/${key}.txt"
  meta=$(node "$KIT/scripts/sat4.js" 4 23 5 --class="$y" --krow="$y:$k" --minpos="$p" --x2="$B" "$cnf" 2>/tmp/${key}.generr) || {
    echo "{\"key\":\"$key\",\"w\":4,\"m\":23,\"q\":5,\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" > "$OUT/${key}.rec"
    return
  }
  md5=$(md5sum "$cnf" | awk '{print $1}')
  t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":4,\"m\":23,\"q\":5,\"class\":\"$y\",\"extra\":\"--krow=$y:$k --minpos=$p --x2=$B\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" > "$OUT/${key}.rec"
  if [ "$res" = "SAT" ]; then
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node "$KIT/scripts/sat4.js" decode 4 23 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 "$KIT/scripts/verify_witness.py" 4 23 5 > "$OUT/${key}.pyverify.json" 2>&1 || true
  fi
  rm -f "$cnf"
}

for B in "${PICK[@]}"; do run_one "$B" & done
wait
SATFOUND=0
for B in "${PICK[@]}"; do
  key="${BUCKET}b$B"
  cat "$OUT/${key}.rec" >> "$OUT/records23.jsonl"
  grep -q '"result":"SAT"' "$OUT/${key}.rec" && { SATFOUND=1; echo "SAT_FOUND $key $(date -u +%FT%TZ)"; }
  rm -f "$OUT/${key}.rec"
done
echo "CHUNK2X_DONE $BUCKET picked=${PICK[*]} satfound=$SATFOUND $(date -u +%FT%TZ)"
