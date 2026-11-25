#!/bin/bash
# run_replica_df.sh <key_id> -- session-local replica runner for Part DF.
# One key per invocation: 2-pass fresh-cold pinned-replica of the published
# batch-28 drive-4/drive-5 15M-probe WIN row, using the pinned jsreplay.js
# (byte-clone 84585617) with budget 15M (the published batch-28 drive-4/5
# probe condition; identical to the published Part DE runner
# run_replica_de.sh 3e4263cc.. except for this Part label header comment --
# the budget and the body are byte-unchanged; Part DF covers
# the eight P2-package 15M-solved WIN rows aa014/aa049/aa051/aa019/aa013/
# aa020/aa010/aa040 of the b28-win46 third-impl queue registry).
# Passes are wrapped in `timeout 260` so the inner timeout fires before the
# outer tool cap (Part CN lesson). NOT a drive runner: no stop rules, no wave
# halt -- the published batch-28 drive semantics already halted on the
# published side; this runner only reproduces the two published rows on this
# host.
# Determinism (p1==p2) and node-exactness vs the published raw are gated by
# audit_df.py G2b, not here; this script only records the runs.
set -u
KEY="$1"
cd "$(dirname "$0")/.."
mkdir -p output/replica
touch output/status.log
SRC="input/$KEY.input.csv"
[ -f "$SRC" ] || { echo "REPLICA key=$KEY MISSING-INPUT rc=48" >> output/status.log; exit 48; }
for P in p1 p2; do
  OUT="output/replica/$KEY.$P.out"
  timeout 260 node scripts/jsreplay.js --exact-replay="$SRC" --exact-replay-budget=15000000 > "$OUT" 2>&1
  RC=$?
  echo "REPLICA key=$KEY pass=$P rc=$RC out=$OUT $(grep -o '^replay,.*' "$OUT" | head -1)" >> output/status.log
  [ "$RC" -ne 0 ] && exit "$RC"
done
