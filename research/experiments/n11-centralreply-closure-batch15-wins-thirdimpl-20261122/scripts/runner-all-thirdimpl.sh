#!/bin/bash
# Part AL runner: rules gate -> negatives -> anchors (a/b) -> targets (a/b)
# 2-core host: at most 2 concurrent solver processes (pairs).
set -u
cd "$(dirname "$0")/.."
echo "$(date -u +%FT%TZ) PARTAL-RUNNER-START host=$(hostname) cores=$(nproc)" >> output/status.log
node scripts/verify_tbl.js > output/rules-gate.txt 2>&1 || echo "$(date -u +%FT%TZ) RULES-GATE-FAIL rc=$?" >> output/status.log
echo "$(date -u +%FT%TZ) RULES-GATE-DONE" >> output/status.log
bash scripts/run_thirdimpl.sh ng1 a negative && bash scripts/run_thirdimpl.sh ng2 a negative
for k in k02a l1a; do
  bash scripts/run_thirdimpl.sh "$k" a anchor & p1=$!
  bash scripts/run_thirdimpl.sh "$k" b anchor & p2=$!
  wait $p1 $p2
done
for k in r001 r002; do
  bash scripts/run_thirdimpl.sh "$k" a target & p1=$!
  bash scripts/run_thirdimpl.sh "$k" b target & p2=$!
  wait $p1 $p2
done
echo "$(date -u +%FT%TZ) PARTAL-RUNNER-EXIT" >> output/status.log
