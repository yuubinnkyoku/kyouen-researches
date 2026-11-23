#!/bin/bash
# runwave.sh -- foreground executor (one 2-key wave per invocation; this host
# is 2-core and the declared batch-17 protocol caps concurrent solver
# processes at 2). Picks the next undone keys from output/status.log, honors
# the pre-registered stop rules: determinism mismatch -> HARD-STOP;
# WIN -> HALT the batch; truncated pass files are re-run fresh-cold.
set -u
cd "$(dirname "$0")/.."
declare -a todo=()
for key in $(python3 - <<'PY'
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
); do
  todo+=("$key")
done
n=${#todo[@]}
if [ "$n" -eq 0 ]; then echo "ALL-DONE"; exit 0; fi
wave=("${todo[@]:0:2}")
echo "$(date -u +%FT%TZ) WAVE-START ${wave[*]}" >> output/status.log
declare -a pids=()
for k in "${wave[@]}"; do
  bash scripts/runbatch.sh "$k" > "/tmp/b17.$k.log" 2>&1 &
  pids+=($!)
done
stop=0
for p in "${pids[@]}"; do
  wait "$p"; rc=$?
  if [ "$rc" -ge 42 ]; then stop=1; fi
done
if [ "$stop" -eq 1 ]; then
  echo "$(date -u +%FT%TZ) RUNNER-STOP stop-condition rc>=42 in wave" >> output/status.log
  echo "WAVE-STOP"
  exit 0
fi
echo "WAVE-DONE (${wave[*]}) remaining=$((n-2))"
