#!/bin/bash
# run_replica_eg.sh <key_id> -- session-local replica runner for Part EG
# (class 34908 b33-win-6 third-impl cross-verification).
# One invocation: one key, 2-pass fresh-cold pinned-replica of the published
# honest-label WIN row, using the pinned jsreplay.js (byte-clone 84585617).
# Declared per-key budget map (the ONLY functional delta from the published
# Part CZ runner run_replica_cz.sh cb909064.., which hardcoded budget 15M for
# the single ab028 row):
#   af029/af047/af050/af053 -> 15000000  (published batch-33 15M drive rows)
#   af023/af048             -> 30000000  (published Part EA 30M reprobe rows;
#                              their 15M b33 runs ended EXHAUSTED, so a 15M
#                              reproduction would NOT be the published verdict)
#   af029-30m                -> 30000000  (published Part EA 30M anchor pair of
#                              the same af029 key: uses input/af029.input.csv,
#                              writes output/replica/af029-30m.p{1,2}.out)
# Passes are wrapped in `timeout 260` so the inner timeout fires before the
# outer tool cap (Part CN lesson); a truncated pass is NOT a verdict and is
# re-run fresh (cross-invocation resume is the pinned-runners' standard
# operation; truncated artifacts are kept as .truncated sidecars by the
# caller). Determinism (p1==p2) and node-exactness vs the published raw are
# gated by scripts/audit_eg.py G2b, not here; this script only records runs.
set -u
KEY="$1"
cd "$(dirname "$0")/.."
mkdir -p output/replica
touch output/status.log
case "$KEY" in
  af029|af047|af050|af053) BUDGET=15000000; SRCID="$KEY" ;;
  af023|af048)             BUDGET=30000000; SRCID="$KEY" ;;
  af029-30m)               BUDGET=30000000; SRCID="af029" ;;
  *) echo "REPLICA key=$KEY UNKNOWN-KEY rc=47" >> output/status.log; exit 47 ;;
esac
SRC="input/$SRCID.input.csv"
[ -f "$SRC" ] || { echo "REPLICA key=$KEY MISSING-INPUT rc=48" >> output/status.log; exit 48; }
for P in p1 p2; do
  OUT="output/replica/$KEY.$P.out"
  timeout 260 node scripts/jsreplay.js --exact-replay="$SRC" --exact-replay-budget=$BUDGET > "$OUT" 2>&1
  RC=$?
  echo "REPLICA key=$KEY pass=$P budget=$BUDGET rc=$RC out=$OUT $(grep -o '^replay,.*' "$OUT" | head -1)" >> output/status.log
  [ "$RC" -ne 0 ] && exit "$RC"
done
