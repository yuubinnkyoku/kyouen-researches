#!/bin/bash
# drive2_step.sh — session-local orchestration for Part CI takeover drive-2
# (Part CI takeover drive-2 declaration ec9c7191, D3 pre-registered design)
# - Enumerates remaining keys from batch-keys.json (published order, s5 asc):
#   a key is COMPLETE iff both output/raw/{k}.p1.out and .p2.out exist and each
#   carries its terminal "# replay_done" line (host-interruption guard, same
#   semantics as runbatch.sh; split/truncated files are NOT evidence).
# - Runs up to 2 workers (2-core host), each `timeout 260 bash scripts/runbatch.sh <k>`.
# - WIN-CONTINUE: runbatch rc=45 (WIN-HALT) is recorded by runbatch.sh in
#   status.log; orchestration continues (pre-registered, runner untouched).
# - MISMATCH rc=42 / P1-FAIL 43 / P2-FAIL 44 -> hard-stop this script with the
#   same rc (declaration D3). rc=124 (inner timeout) leaves a truncated pass
#   file which the next invocation's guard re-runs fresh-cold.
# - "if rem" guard: never invoke runbatch.sh with an empty key list (Part CN).
set -u
cd "$(dirname "$0")"

ALL=$(python3 - <<'EOF'
import json, os
ks = [k['key_id'] for k in json.load(open('input/batch-keys.json'))['keys']]
def complete(k):
    for p in ('p1', 'p2'):
        fn = f"output/raw/{k}.{p}.out"
        if not os.path.exists(fn):
            return False
        with open(fn) as f:
            if '# replay_done' not in f.read():
                return False
    return True
rem = [k for k in ks if not complete(k)]
print(' '.join(rem))
EOF
)
if [ -z "${ALL:-}" ]; then
  echo "NO-REMAINING-KEYS (drive-2 fully complete)"
  exit 0
fi
echo "REMAINING: $ALL"
W1=$(echo $ALL | awk '{print $1}')
W2=$(echo $ALL | awk '{if (NF>=2) print $2}')
rc_overall=0

run_worker() {
  local k="$1"
  local log="output/log-$k.txt"
  timeout 260 bash scripts/runbatch.sh "$k" > "$log" 2>&1
  local rc=$?
  echo "worker $k rc=$rc :: $(tr '\n' ';' < $log)"
  return $rc
}

if [ -n "${W2:-}" ]; then
  run_worker "$W1" & p1=$!
  run_worker "$W2" & p2=$!
  wait $p1; rc1=$?
  wait $p2; rc2=$?
  echo "wave rc1=$rc1 rc2=$rc2"
  for rc in $rc1 $rc2; do
    if [ "$rc" -eq 42 ] || [ "$rc" -eq 43 ] || [ "$rc" -eq 44 ]; then exit $rc; fi
  done
else
  run_worker "$W1"; rc1=$?
  echo "wave rc1=$rc1"
  if [ "$rc1" -eq 42 ] || [ "$rc1" -eq 43 ] || [ "$rc1" -eq 44 ]; then exit $rc1; fi
fi
exit 0
