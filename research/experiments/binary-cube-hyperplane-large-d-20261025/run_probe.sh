#!/bin/bash
# Parallel probe of greedy-achievable general-position set sizes in the
# binary d-cube for d = 6..20.  Each dimension starts at m = d+3 (known
# possible for d = 6..10) and climbs until two consecutive sizes fail.
set -u
cd "$(dirname "$0")"
mkdir -p probe_logs
pids=()
for d in $(seq 6 20); do
  (
    /tmp/hlsearch --probe "$d" $((d + 3)) $((d + 8)) $((d * 1000 + 1)) 300 90 \
      "wit_d${d}.txt" > "probe_logs/d${d}.log" 2>&1
  ) &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
echo ALL_DONE
