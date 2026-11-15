#!/bin/bash
# Resumable driver for the |S n T| = j case split of n10_ge20_cuts (j = 0..9).
# All-UNSAT over the 10 sub-instances proves the base instance UNSAT
# => K_10 <= 19 (conditional on the published X1/X2 complete enumerations).
# Per-instance records to n10_split_records.jsonl (1 line per finished run);
# keys are skipped on resume (comma-anchored match). CAP is wall-clock
# (env CAP, default 3600); INDET records keep the key re-runnable at a
# strictly higher CAP (same-CAP reruns are skipped).
set -u
cd "$(dirname "$0")"
KS=/home/user/krwork/kissat-4.0.4-linux-amd64
CAP=${CAP:-3600}
REC=n10_split_records.jsonl
python3 split_ge20cuts.py > split_gen.log 2>&1 || { echo "split generation failed"; exit 1; }
for j in $(seq 0 9); do
  key="tj$j"
  rec=$(grep -s "\"key\":\"$key\"," "$REC")
  if [ -n "$rec" ]; then
    echo "$rec" | grep -s -q '"result":"\(SAT\|UNSAT\)"' && continue
    echo "$rec" | grep -s -q "\"cap\":$CAP," && continue
  fi
  cnf="n10_ge20_cuts_${key}.cnf"; log="n10_ge20_cuts_${key}.txt"
  md5=$(md5sum "$cnf" | awk '{print $1}')
  t0=$(date +%s.%N)
  timeout "$CAP" "$KS" "$cnf" > "$log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  sec=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')
  conf=$(grep -a -E "^c conflicts" "$log" | tail -1 | awk '{print $3}')
  res=INDET; [ "$rc" = "10" ] && res=SAT; [ "$rc" = "20" ] && res=UNSAT
  echo "{\"key\":\"$key\",\"cnf_md5\":\"$md5\",\"cap\":$CAP,\"kissat\":{\"result\":\"$res\",\"rc\":$rc,\"conflicts\":${conf:-null},\"sec\":$sec},\"date\":\"$(date -u +%FT%TZ)\"}" >> "$REC"
  [ "$res" = "SAT" ] && echo "SAT_FOUND $key $(date -u +%FT%TZ)"
done
echo "N10_SPLIT_DONE cap=$CAP $(date -u +%FT%TZ)"
