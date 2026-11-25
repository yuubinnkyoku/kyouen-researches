#!/bin/bash
# per-key driver for the second-environment verification of published batch-38:
# one pinned runbatch.sh invocation per key, rc 45 (WIN-HALT, pre-registered) continues.
# Mirrors drive38_local_step.sh worker semantics (WIN-CONTINUE); pinned scripts unmodified.
set -u
cd "$(dirname "$0")/.."
for k in "$@"; do
  bash scripts/runbatch.sh "$k"
  rc=$?
  echo "$(date -u +%FT%TZ) wrapper: $k rc=$rc" >> wrapper.log
  if [ "$rc" -ne 0 ] && [ "$rc" -ne 45 ]; then
    echo "$(date -u +%FT%TZ) wrapper ABORT key=$k rc=$rc" >> wrapper.log
    exit "$rc"
  fi
done
echo "$(date -u +%FT%TZ) wrapper DONE" >> wrapper.log
