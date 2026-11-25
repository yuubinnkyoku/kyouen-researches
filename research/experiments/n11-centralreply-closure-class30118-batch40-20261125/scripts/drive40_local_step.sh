#!/bin/bash
# session-local drive step for batch-40 (Part EH, closure class 30484).
# Fork of the published batch-39 drive step (drive38_local_step.sh, sha256
# 2bd91341...): key-id regex ai[0-9]{3} -> aj[0-9]{3} (4 spots),
# batch-keys json b38 -> b39. The drive design is WIN-CONTINUE (single
# drive completes all 50 keys with honest labels; batch-35..39
# drive-level succession). Everything else (done-set extraction incl.
# WIN-HALT ids, worker/timeout design, MISMATCH hard-stop,
# empty-remaining-keys guard) is functionally identical.
# One invocation = at most 2 keys, up to 2 runbatch.sh workers in parallel
# (2-core host). Pre-registered stop rules live in the pinned runner
# (runbatch.sh, byte-clone f591f8c2): WIN rc=45 / MISMATCH rc=42 / p1/p2
# fail rc=43/44. WIN rows append the pre-registered WIN-HALT marker line and
# the drive continues (WIN verdicts are never consumed here; scrutiny-owner
# C++ gate required for any adoption). EXHAUSTED rows continue (honest
# UNKNOWN). Workers are wrapped in `timeout 260` so the inner timeout fires
# before the outer 290s tool cap (Part CN lesson: a truncated pass never
# produced a verdict; the runner's replay_done guard re-runs it fresh-cold).
set -u
cd "$(dirname "$0")/.."
mkdir -p output/raw
touch output/status.log
if grep -q "MISMATCH" output/status.log; then
  echo "HARD-STOP: determinism mismatch already recorded"
  exit 42
fi
rem=$(node -e '
const a = require("./input/batch-keys-b40.json");
const fs = require("fs");
const t = fs.readFileSync("output/status.log", "utf8").split("\n");
const done = new Set();
for (const line of t) {
  const m = line.match(/\b(aj[0-9]{3}) (?:PASS|EXHAUSTED)/);
  if (m) done.add(m[1]);
  const w = line.match(/\b(aj[0-9]{3}) WIN-HALT/);
  if (w) done.add(w[1]);
}
console.log(a.keys.map(q => q.key_id).filter(k => !done.has(k)).join(" "));')
if [ -z "$rem" ]; then
  echo "ALL-DONE (no remaining keys; empty-key guard: no runbatch invocation)"
  exit 0
fi
read -ra take <<< "$rem"
n=2
if [ "${#take[@]}" -lt 2 ]; then n=${#take[@]}; fi
inv=("${take[@]:0:$n}")
echo "invoking: ${inv[*]}"
pids=()
rcs=()
for k in "${inv[@]}"; do
  timeout 260 bash scripts/runbatch.sh "$k" &
  pids+=($!)
done
rc=0
i=0
for p in "${pids[@]}"; do
  wrc=0
  wait "$p" || wrc=$?
  rcs+=("$wrc")
  if [ "$wrc" -ne 0 ] && [ "$wrc" -ne 45 ]; then rc="$wrc"; fi
  i=$((i+1))
done
wins=$(node -e '
const fs = require("fs");
const t = fs.readFileSync("output/status.log", "utf8").split("\n");
const s = new Set();
for (const line of t) {
  const m = line.match(/\b(aj[0-9]{3}) WIN-HALT/);
  if (m) s.add(m[1]);
}
console.log(s.size);')
mm=$(grep -c "MISMATCH" output/status.log || true)
echo "step finished: invoked=$i worker_rcs=${rcs[*]} wins_distinct=${wins:-0} mismatch=${mm:-0}"
if [ "${mm:-0}" -ge 1 ]; then
  echo "HARD-STOP: determinism mismatch recorded"
  exit 42
fi
exit "$rc"
