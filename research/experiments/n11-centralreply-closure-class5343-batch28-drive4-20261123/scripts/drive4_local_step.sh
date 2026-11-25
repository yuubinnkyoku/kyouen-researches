#!/bin/bash
# session-local orchestration: next two undone keys, one per worker, parallel
K=/home/user/kr-exec/cj/b28drive4
mapfile -t REM < <(python3 - <<'PY'
import json
ks = json.load(open("/home/user/kr-exec/cj/b28drive4/input/batch-keys.json"))["keys"]
done = set()
for line in open("/home/user/kr-exec/cj/b28drive4/output/status.log"):
    parts = line.split()
    for i, p in enumerate(parts):
        if p in ("PASS", "WIN-HALT", "MISMATCH", "EXHAUSTED") and i >= 1:
            done.add(parts[i-1])
rem = [k["key_id"] for k in ks if k["key_id"] not in done]
print("\n".join(rem))
PY
)
echo "remaining=${#REM[@]}"
if [ "${#REM[@]}" -eq 0 ]; then echo ALL-DONE; exit 0; fi
cd "$K" || exit 9
if [ "${#REM[@]}" -ge 2 ]; then
  ( timeout 285 bash scripts/runbatch.sh "${REM[0]}" > /tmp/ckA.log 2>&1; echo "W-A ${REM[0]} rc=$?" ) &
  ( timeout 285 bash scripts/runbatch.sh "${REM[1]}" > /tmp/ckB.log 2>&1; echo "W-B ${REM[1]} rc=$?" ) &
  wait
else
  timeout 285 bash scripts/runbatch.sh "${REM[0]}"; echo "W-A ${REM[0]} rc=$?"
fi
tail -4 output/status.log
