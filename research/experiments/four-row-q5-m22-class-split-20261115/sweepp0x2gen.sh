#!/bin/bash
# Generalized second-stone x2 sub-split for the (4,22,5) buckets that resist
# the sweep22.sh CAP. Usage: bash sweepp0x2gen.sh <bucket>  e.g. c0k3p3 / c1k2p7
#   bucket = c<y>k<k>p<p>: row y has exactly k stones (k>=2), leftmost pinned
#   at column p by --minpos (sound H-split, p <= 10).
#   k>=3: B in p+1..20 (m-2; a 3rd stone must fit right of B)
#   k==2: B in p+1..21 (m-1; sat4.js 2026-11-15 k-aware bound)
# Complete disjoint case analysis on the 2nd-leftmost stone column B:
# all-UNSAT over B => the (class, krow, minpos) bucket is UNSAT.
# Resumable: per-key skip with comma-anchored match (prefix-collision safe),
# and re-run of a key is allowed only at a strictly higher CAP.
# Records append to output/records.jsonl with key <bucket>b<B>.
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=${CAP:-900}
OUT=output
BUCKET=${1:?bucket required, e.g. c0k3p3}
case "$BUCKET" in
  c[01]k[23]p[0-9]*) ;;
  *) echo "bad bucket $BUCKET (expected c{0,1}k{2,3}p<p>)" >&2; exit 1 ;;
esac
y=${BUCKET:1:1}; k=${BUCKET:3:1}; p=${BUCKET:5}
[ "$p" -le 10 ] || { echo "minpos p=$p out of H-split range (<=10)" >&2; exit 1; }
if [ "$k" = "3" ]; then BMAX=20; else BMAX=21; fi
BMIN=$((p + 1))
[ "$BMIN" -le "$BMAX" ] || { echo "empty B range for $BUCKET" >&2; exit 1; }
mkdir -p "$OUT"
for B in $(seq "$BMIN" "$BMAX"); do
  key="${BUCKET}b$B"
  rec=$(grep -s "\"key\":\"$key\"," "$OUT/records.jsonl")
  if [ -n "$rec" ]; then
    echo "$rec" | grep -s -q '"result":"\(SAT\|UNSAT\)"' && continue
    echo "$rec" | grep -s -q "\"cap\":$CAP," && continue
    echo "$rec" | grep -s -q '"genfail":true' && continue
  fi
  cnf="$OUT/${key}.cnf"; log="$OUT/${key}.txt"
  meta=$(node scripts/sat4.js 4 22 5 --class="$y" --krow="$y:$k" --minpos="$p" --x2="$B" "$cnf") \
    || { echo "{\"key\":\"$key\",\"genfail\":true,\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"; continue; }
  md5=$(md5sum "$cnf" | awk '{print $1}')
  t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"w\":4,\"m\":22,\"q\":5,\"class\":\"$y\",\"extra\":\"--krow=$y:$k --minpos=$p --x2=$B\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$OUT/records.jsonl"
  if [ "$res" = "SAT" ]; then
    grep "^v " "$log" > "$OUT/${key}.model.txt"
    node scripts/sat4.js decode 4 22 5 "$OUT/${key}.model.txt" --json="$OUT/${key}.witness.json" > "$OUT/${key}.decode.txt" 2>&1
    jq -c '.stones' "$OUT/${key}.witness.json" | python3 scripts/verify_witness.py 4 22 5 > "$OUT/${key}.pyverify.json" 2>&1 || true
    echo "SAT_FOUND $key $(date -u +%FT%TZ)"
  fi
  rm -f "$cnf"
done
echo "SWEEPP0X2GEN_DONE $BUCKET cap=$CAP $(date -u +%FT%TZ)"
