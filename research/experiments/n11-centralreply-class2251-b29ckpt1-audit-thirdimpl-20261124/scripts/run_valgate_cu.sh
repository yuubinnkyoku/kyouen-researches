#!/bin/bash
# run_valgate_cu.sh -- session-local this-host val-gate runner for Part CU.
# One fresh-cold jsreplay pass per sanctioned val-gate key (pinned published
# baseline comparison is done by audit_cu.py G7; this script only records
# the runs). Budget per the published batch-29 scaffold convention:
# at2m keys 2,000,000 / 15m keys 15,000,000.
set -u
cd "$(dirname "$0")/.."
mkdir -p val-gate
touch output/status.log
run_vg() {
  local key="$1" budget="$2"
  local out="val-gate/$key.cu-host.out"
  timeout 260 node scripts/jsreplay.js --exact-replay="val-gate/$key.input.csv" --exact-replay-budget=$budget > "$out" 2>&1
  local rc=$?
  echo "VALGATE key=$key budget=$budget rc=$rc out=$out $(grep -o '^replay,.*' "$out" | head -1)" >> output/status.log
  [ "$rc" -ne 0 ] && return "$rc"
  return 0
}
run_vg "at2m-s5-1152921504606851072-536870946" 2000000 || exit $?
run_vg "at2m-s5-1188950301626860544-536870912" 2000000 || exit $?
run_vg "first-15m-s5-1152921504606851072-536870946" 15000000 || exit $?
run_vg "second-15m-s5-1188950301626860544-536870912" 15000000 || exit $?
echo "VALGATE done 4/4"
