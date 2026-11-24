#!/bin/bash
# run_replica_cx.sh <key_id> -- session-local replica runner for Part CX.
# One key per invocation: 2-pass fresh-cold pinned-replica of the published
# batch-28 Part CQ 20M-reprobe WIN row, using the pinned jsreplay.js
# (byte-clone 84585617) with budget 20M (the published CQ reprobe condition;
# identical to the published Part CW runner run_replica_cw.sh 8c123b65.. --
# only this Part label header comment differs; Part CX covers the five
# remaining CQ-WIN rows aa005/aa030/aa031/aa047/aa053).
# Passes are wrapped in `timeout 260` so the inner timeout fires before the
# outer tool cap (Part CN lesson). NOT a drive runner: no stop rules, no wave
# halt -- the Part CQ 20M-reprobe semantics already halted on the published
# side; this runner only reproduces the two published rows on this host.
# Determinism (p1==p2) and node-exactness vs the published raw are gated by
# audit_cx.py G2b, not here; this script only records the runs.
set -u
KEY="$1"
cd "$(dirname "$0")/.."
mkdir -p output/replica
touch output/status.log
SRC="input/$KEY.input.csv"
[ -f "$SRC" ] || { echo "REPLICA key=$KEY MISSING-INPUT rc=48" >> output/status.log; exit 48; }
for P in p1 p2; do
  OUT="output/replica/$KEY.$P.out"
  timeout 260 node scripts/jsreplay.js --exact-replay="$SRC" --exact-replay-budget=20000000 > "$OUT" 2>&1
  RC=$?
  echo "REPLICA key=$KEY pass=$P rc=$RC out=$OUT $(grep -o '^replay,.*' "$OUT" | head -1)" >> output/status.log
  [ "$RC" -ne 0 ] && exit "$RC"
done
