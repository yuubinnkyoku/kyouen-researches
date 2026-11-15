#!/bin/bash
# sweep30.sh — (7,30,6) absence-capable class-split sweep, resumable driver.
# 71 row-mirror-canonical deficiency classes (w=7, q=6: deficient row = <=4 stones,
# full row = 5 = q-1; mirror i <-> 6-i; canonical reps cover all 127 nonempty patterns).
# Positive control first: (7,29,6) class {3} must be SAT (contains the m=29 witness
# rows [5,5,5,4,5,5,5] of seven-row-q5-q8-sat-frontier-20261115).
# Every UNSAT verdict is final for its class; INDET classes get k/minpos or krow-pin
# decomposition in follow-up phases (run_one.sh with extra opts), new keys.
# SATFOUND aborts the loop: a 7x30 witness extends the band (M_{7,6} >= 31) and the
# remaining classes are then moot; per-key skip keeps the driver resumable either way.
# Resume: per-key skip via output/records.jsonl; CNF regeneration is deterministic.
set -u
cd "$(dirname "$0")"
CAP=900 ./run_one.sh ctrl_7x29_c3 7 29 3
CAP=${CAP:-600}
while IFS= read -r D; do
  last=$(tail -1 output/records.jsonl 2>/dev/null)
  case "$last" in
    *'"m":30'*'"result":"SAT"'*) echo "SWEEP_SAT_ABORT $(date -u +%FT%TZ)"; exit 0 ;;
  esac
  key="c$(echo "$D" | tr -d ',')"
  ./run_one.sh "$key" 7 30 "$D"
done < classes.txt
echo "SWEEP_PASS_DONE $(date -u +%FT%TZ)"
