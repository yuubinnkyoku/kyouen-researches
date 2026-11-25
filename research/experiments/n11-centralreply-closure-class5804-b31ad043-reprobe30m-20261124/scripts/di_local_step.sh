#!/bin/bash
# session-local orchestration (Part DI): single worker, one key per invocation.
# Fork of the published Part CT ct_local_step.sh (854daf1e...) with EXACTLY the
# kit-root path, the registry/step script names and this header changed; all
# orchestration logic (done-set extraction, truncation bookkeeping,
# WINDOW-EXCEEDED pre-registered rule, empty-remaining-key ALL-DONE guard,
# timeout 260 inner / 290 outer) identical.
# WIN-CONTINUE (Part CE/CK/CN/CQ/CS/CT precedent): a runner rc=45 (WIN row) does
# NOT stop the orchestration; only rc=42 (determinism mismatch) is a hard stop
# and the runner exits hard itself in that case. EXHAUSTED-at-30M rows are
# honest UNKNOWN and continue. Pre-registered WINDOW-EXCEEDED rule: a key
# whose same pass shows >= 2 TRUNCATED-RETRY events in status.log cannot fit
# the 260s inner window at 30M on this host and is SKIPPED this Part (honest
# unresolved; left to a future Part with a different window/budget design); it
# is reported on stdout and recorded by the audit, never silently dropped.
# Cross-invocation p1/p2 resume is the pre-registered design for 30M (published
# 15M exhaustion pass wall 108s -> expected 30M pass ~216s: a single invocation
# cannot host p1+p2 inside the 260s inner window; the published runner
# file-existence + truncated-sidecar guard carries the pass boundary, as
# exercised in Part CS/CT on batch-28).
# if-rem guard: never invoke the runner with an empty key (Part CN lesson).
K=/home/user/kr/di
mapfile -t REM < <(python3 - <<'PY'
import json
import sys
reg = json.load(open("/home/user/kr/di/input/reprobe-keys.json"))["keys"]
ks = [k["key_id"] for k in reg]
ids = set(ks)
done = set()
trunc = {}
for line in open("/home/user/kr/di/output/status.log"):
    parts = line.split()
    for i in range(1, len(parts)):
        p = parts[i]
        prev = parts[i-1]
        if p in ("PASS", "WIN-HALT", "MISMATCH", "EXHAUSTED") and prev in ids:
            done.add(prev)
        if p in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY") and prev in ids:
            trunc[(prev, p[:2])] = trunc.get((prev, p[:2]), 0) + 1
rem = [k for k in ks if k not in done
        and trunc.get((k, "P1"), 0) < 2 and trunc.get((k, "P2"), 0) < 2]
skip = [k for k in ks if k not in done
        and (trunc.get((k, "P1"), 0) >= 2 or trunc.get((k, "P2"), 0) >= 2)]
for s in skip:
    print(f"WINDOW-EXCEEDED-CANDIDATE {s} (unresolved at 30M in the 260s window; "
          f"honest UNKNOWN; skipped this Part)", file=sys.stderr)
if rem:
    print("\n".join(rem))
PY
)
echo "remaining=${#REM[@]}"
if [ "${#REM[@]}" -eq 0 ]; then echo ALL-DONE; tail -4 "$K/output/status.log"; exit 0; fi
cd "$K" || exit 9
timeout 260 bash scripts/runbatch_b31ad043-30m.sh "${REM[0]}"
rc=$?
echo "W-A ${REM[0]} rc=$rc"
tail -4 output/status.log
