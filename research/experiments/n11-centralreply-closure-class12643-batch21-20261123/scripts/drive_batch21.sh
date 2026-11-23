#!/bin/bash
# drive_batch21.sh -- local foreground driver for this sandbosted session:
# computes the remaining undone key ids from output/status.log, splits them
# odd/even into two workers, and runs each worker as `timeout 260 bash
# scripts/runbatch.sh <keys...>` (the PUBLISHED Part BG runner, byte-pinned
# f591f8c2; two solver processes max, one key at a time per worker).
# Stop rules live inside the published runner (mismatch rc=42, P1/P2 fail
# rc=43/44, WIN rc=45); a worker killed by the timeout (rc=124) leaves its
# mid-write pass files truncated and the published completeness guard
# re-runs them fresh-cold on the next invocation (no completed row is ever
# re-run). No batch semantics are implemented here.
set -u
cd "$(dirname "$0")/.."
mapfile -t todo < <(python3 - <<'PY'
import json
ks = json.load(open("input/batch-keys.json"))["keys"]
done = set()
try:
    for line in open("output/status.log"):
        parts = line.split()
        for i, p in enumerate(parts):
            if p in ("PASS", "WIN-HALT", "MISMATCH", "EXHAUSTED"):
                done.add(parts[i-1])
except FileNotFoundError:
    pass
print("\n".join(k["key_id"] for k in ks if k["key_id"] not in done))
PY
)
n=${#todo[@]}
if [ "$n" -eq 0 ]; then echo "ALL-DONE"; exit 0; fi
odd=(); even=()
for i in "${!todo[@]}"; do
  if [ $((i % 2)) -eq 0 ]; then odd+=("${todo[$i]}"); else even+=("${todo[$i]}"); fi
done
echo "$(date -u +%FT%TZ) DRIVE-START remaining=$n"
rc1=0; rc2=0
if [ "${#odd[@]}" -gt 0 ]; then timeout 260 bash scripts/runbatch.sh "${odd[@]}" & P1=$!; else echo "no odd keys"; fi
if [ "${#even[@]}" -gt 0 ]; then timeout 260 bash scripts/runbatch.sh "${even[@]}" & P2=$!; else echo "no even keys"; fi
[ -n "${P1:-}" ] && wait $P1; rc1=$?
[ -n "${P2:-}" ] && wait $P2; rc2=$?
echo "$(date -u +%FT%TZ) DRIVE-END worker1_rc=$rc1 worker2_rc=$rc2"
if [ "$rc1" -eq 45 ] || [ "$rc2" -eq 45 ]; then echo "WIN-HALT"; fi
if [ "$rc1" -eq 42 ] || [ "$rc2" -eq 42 ]; then echo "HARD-STOP-MISMATCH"; fi
python3 - <<'PY'
import json
ks = json.load(open("input/batch-keys.json"))["keys"]
done = set()
for line in open("output/status.log"):
    parts = line.split()
    for i, p in enumerate(parts):
        if p in ("PASS", "WIN-HALT", "EXHAUSTED"):
            done.add(parts[i-1])
print(f"PROGRESS {len(done)}/53")
PY
