#!/bin/bash
# run_replica_dh.sh <key_id> <pass> -- session-local replica runner for Part DH.
# ONE PASS PER INVOCATION (declared DH delta vs the DG runner run_replica_dg.sh,
# which ran both passes in one call under the uniform 15M budget: the P4 package
# rows carry PER-KEY decisive probe budgets -- aa011/aa054/aa022/aa034/aa037 =
# 15,000,000 (drive4/drive5 decisive logs), aa032/aa028/aa021 = 25,000,000
# (cs-25m reprobe), aa050 = 30,000,000 (ct-30m reprobe) -- and the heavier
# passes need per-key `timeout` headroom under the outer tool cap (Part CN
# lesson: inner timeout fires first; per-key TMO = published budget /
# ~92k nodes/s with margin). The pinned jsreplay.js (byte-clone 84585617) is
# invoked with the per-key published decisive budget. NOT a drive runner:
# no stop rules, no wave halt -- the published decisive semantics already
# halted on the published side; this runner only reproduces one published
# pass on this host. Determinism (p1==p2) and node-exactness vs the
# published raw at the per-key budget are gated by audit_dh.py G2b, not
# here; this script only records the run.
set -u
KEY="$1"; PASS="$2"
case "$KEY" in
  aa011|aa054|aa022|aa034|aa037) BUDGET=15000000; TMO=260;;
  aa032|aa028|aa021)            BUDGET=25000000; TMO=288;;
  aa050)                        BUDGET=30000000; TMO=295;;
  *) echo "REPLICA key=$KEY pass=$PASS UNKNOWN-KEY rc=47" >> output/status.log; exit 47;;
esac
case "$PASS" in
  p1|p2) ;;
  *) echo "REPLICA key=$KEY pass=$PASS UNKNOWN-PASS rc=47" >> output/status.log; exit 47;;
esac
cd "$(dirname "$0")/.."
mkdir -p output/replica
touch output/status.log
SRC="input/$KEY.input.csv"
[ -f "$SRC" ] || { echo "REPLICA key=$KEY pass=$PASS MISSING-INPUT rc=48" >> output/status.log; exit 48; }
OUT="output/replica/$KEY.$PASS.out"
timeout "$TMO" node scripts/jsreplay.js --exact-replay="$SRC" --exact-replay-budget="$BUDGET" > "$OUT" 2>&1
RC=$?
echo "REPLICA key=$KEY pass=$PASS budget=$BUDGET rc=$RC out=$OUT $(grep -o '^replay,.*' "$OUT" | head -1)" >> output/status.log
exit $RC
