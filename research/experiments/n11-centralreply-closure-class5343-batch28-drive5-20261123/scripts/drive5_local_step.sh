#!/bin/bash
# session-local orchestration (Part CN drive-5): next two undone keys, one per
# worker, parallel. Identical design to the published Part CK drive-4 session
# script (scripts/drive4_local_step.sh, sha ea0db83e) except:
#   * K root path is this Part CN kit;
#   * per-worker timeout is 260s (drive-4 used 285s): this host's outer shell
#     cap is 290s and a worker killed by ITS inner timeout (rc=124) must
#     return inside the invocation so no outer tool-timeout reset can
#     un-write evidence files. Truncated pass files are renamed fresh-cold
#     by the published runbatch.sh completeness guard on the next invocation.
# WIN-CONTINUE (Part CE / Part CK precedent): a worker's rc=45 (WIN row) does
# not stop the orchestration; only rc=42 (mismatch) is a hard stop, and the
# invocation always returns normally so status.log stays bookkeeping-clean.
K=/home/user/work/b28drive5
mapfile -t REM < <(python3 - <<'PY'
import json
ks = json.load(open("/home/user/work/b28drive5/input/batch-keys.json"))["keys"]
done = set()
for line in open("/home/user/work/b28drive5/output/status.log"):
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
  ( timeout 260 bash scripts/runbatch.sh "${REM[0]}" > /tmp/cnA.log 2>&1; echo "W-A ${REM[0]} rc=$?" ) &
  ( timeout 260 bash scripts/runbatch.sh "${REM[1]}" > /tmp/cnB.log 2>&1; echo "W-B ${REM[1]} rc=$?" ) &
  wait
else
  timeout 260 bash scripts/runbatch.sh "${REM[0]}"; echo "W-A ${REM[0]} rc=$?"
fi
tail -6 output/status.log
