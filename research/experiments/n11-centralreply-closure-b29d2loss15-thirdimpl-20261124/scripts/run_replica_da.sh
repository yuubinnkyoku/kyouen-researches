#!/bin/bash
# run_replica_da.sh <key_id> -- session-local replica runner for Part DA
# (batch-29 drive-2 ckpt-2/3 LOSS rows third-impl cross-verification).
# One key per invocation: 2-pass fresh-cold pinned-replica of the published
# batch-29 drive-2 LOSS row <key_id>, using the pinned jsreplay.js (byte-clone
# 84585617) with budget 15M (the declared batch-29 probe condition -- the
# single budget line is the ONLY functional delta from the published Part CW
# runner run_replica_cw.sh 8c123b65..; CW used the Part CQ 20M condition,
# CZ republished it for the WIN row ab028 -- Part DA keeps the same budget
# for the 15 LOSS rows).
# Passes are wrapped in `timeout 260` so the inner timeout fires before the
# outer tool cap (Part CN lesson). NOT a drive runner: no stop rules, no wave
# halt -- the batch-29 drive-2 semantics already halted on the published side
# (status.log WIN-HALT ab028 second solve); this runner only reproduces the
# published LOSS rows on this host. Determinism (p1==p2) and node-exactness vs
# the published raw are gated by scripts/audit_da.py G2b, not here; this
# script only records the runs.
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
