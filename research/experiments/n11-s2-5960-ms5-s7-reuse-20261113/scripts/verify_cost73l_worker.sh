#!/bin/sh
# Verify-as-available worker for the 73l certificates: waits for each
# bitN.cert to appear (extraction still running), then runs the independent
# verification orchestrator. Usage: verify_cost73l_worker.sh <bit>...
# One argument per bit; skips bits whose verify-complete marker exists.
set -u
D="$(cd "$(dirname "$0")/.." && pwd)"
for BIT in "$@"; do
  CERT="$D/output/class2-lane-cost73l-certificates/bit${BIT}.cert"
  DONE="$D/output/class2-lane-cost73l-certificates/bit${BIT}-verified.marker"
  [ -f "$DONE" ] && { echo "skip bit $BIT (marker)"; continue; }
  I=0
  while [ ! -f "$CERT" ] && [ $I -lt 720 ]; do sleep 5; I=$((I+1)); done
  [ -f "$CERT" ] || { echo "TIMEOUT waiting for bit $BIT cert"; continue; }
  ROOT=$(python3 -c "print('%032x' % (int('00000000000000c09002000000400000',16)|(1 << $BIT)))")
  if bash "$D/scripts/verify_cost73l_one.sh" "$BIT" "$ROOT" "$CERT"; then
    : > "$DONE"
    echo "verified bit $BIT"
  else
    echo "VERIFY FAIL bit $BIT"
  fi
done
