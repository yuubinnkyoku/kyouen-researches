#!/bin/bash
# sweep_driver_6q8_band3.sh — band3 sweep driver for the (6,m,8) def-mode widths
# (kissat resume, currently m=109..370 under single-owner declaration 7bc633a6).
# In-band semantics: scripts/lean6q8.sh APPENDS output/band3/records.jsonl itself
# and deletes the CNF after each run, so this driver is read-only w.r.t. records
# (no duplicate appends). Widths already present in records.jsonl are skipped,
# hence re-runs and multi-session resumes are idempotent.
# GUARD: stops before starting a new width if elapsed + estimated next width
# would exceed the 230s kissat cap window (est = last width sec + 20, floor 60).
# Usage: bash sweep_driver_6q8_band3.sh M1 M2   (M1..M2 inclusive, e.g. 109 160)
set -u
cd /home/user/krwork/band
OUT=out3
T0=$(date +%s)
for M in $(seq \"$1\" \"$2\"); do
  if grep -q \"\\\"m\\\":$M,\\\"q\\\":8,\\\"lex\\\":\\\"none\\\"\" \"$OUT/records.jsonl\" 2>/dev/null; then echo \"SKIP $M\"; continue; fi
  NOW=$(date +%s); ELAPSED=$((NOW-T0))
  LAST=$(cat \"$OUT/.last_sec\" 2>/dev/null || echo 40)
  BUD=$(( LAST + 20 )); [ $BUD -lt 60 ] && BUD=60
  if [ $((ELAPSED+BUD)) -gt 230 ]; then echo \"GUARD_STOP before m=$M (elapsed ${ELAPSED}s budget ${BUD}s)\"; break; fi
  O=$(bash lean6q8.sh 6 \"$M\" 8 \"$OUT\")
  REC=$(printf '%s\\n' \"$O\" | grep '^{' | tail -1)
  if [ -z \"$REC\" ]; then echo \"NO_RECORD m=$M\"; break; fi
  R=$(printf '%s' \"$REC\" | python3 -c \"import json,sys; r=json.load(sys.stdin); print(r['kissat']['result'],r['kissat']['conflicts'],r['kissat']['sec'])\")
  SEC=$(printf '%s' \"$REC\" | python3 -c \"import json,sys; print(int(float(json.load(sys.stdin)['kissat']['sec'])))\")
  echo \"$SEC\" > \"$OUT/.last_sec\"
  echo \"DONE m=$M $R\"
  case \"$R\" in UNSAT*) ;; *) echo \"NONUNSAT m=$M — stop\"; break;; esac
done
echo \"BATCH_END elapsed=$(( $(date +%s)-T0 ))s records=$(wc -l < \"$OUT/records.jsonl\")\"
