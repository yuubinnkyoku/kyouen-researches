#!/bin/bash
# session-local drive-2 step for batch-30 (Part CP takeover, closure class 34269).
# One invocation = at most 2 keys, up to 2 runbatch.sh workers in parallel
# (2-core host). Pre-registered stop rules live in the pinned runner
# (runbatch.sh, byte-clone f591f8c2): WIN rc=45 / MISMATCH rc=42 / p1/p2 fail
# rc=43/44. WIN-CONTINUE design (Part CP drive-2 declaration 7aaa0525 / Part
# CE/CK/CN precedent): the runner's rc=45 ends only that worker's key unit;
# the orchestration layer continues with the next wave until every remaining
# key carries a PASS/EXHAUSTED verdict (2-pass fresh-cold node-exact).
# EXHAUSTED rows continue (honest UNKNOWN). Workers are wrapped in
# `timeout 260` so the inner timeout fires before the outer 290s tool cap
# (Part CN lesson: a truncated pass never produced a verdict; the runner's
# replay_done guard re-runs it fresh-cold). The empty-remaining-keys case
# exits ALL-DONE without ever invoking runbatch.sh with an empty key (Part CN
# all-done empty-key guard).
#
# Delta from published drive-1 session script v2 (e7b627a8): the WIN-HALT
# wave logic (windistinct pre-check and post-wave WAVE-HALTED exits) is
# removed; everything else (dedup done-set extraction by distinct key id,
# MISMATCH hard-stop, timeout 260 wrapper, empty-key guard) is inherited
# unchanged. The original drive-2 session pre-declared a drive2_local_step.sh
# (95c3f15b...) that was never published (vanished host, no B' commit), so
# this takeover host re-creates it as a minimal delta of published v2.
set -u
cd "$(dirname "$0")/.."
mkdir -p output/raw
touch output/status.log
if grep -q "MISMATCH" output/status.log; then
  echo "HARD-STOP: determinism mismatch already recorded"
  exit 42
fi
rem=$(node -e '
const a = require("./input/batch-keys.json");
const fs = require("fs");
const t = fs.readFileSync("output/status.log", "utf8").split("\n");
const done = new Set();
for (const line of t) {
  const m = line.match(/\b(ac[0-9]{3}) (?:PASS|EXHAUSTED)/);
  if (m) done.add(m[1]);
  const w = line.match(/\b(ac[0-9]{3}) WIN-HALT/);
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
mm=$(grep -c "MISMATCH" output/status.log || true)
echo "step finished: invoked=$i worker_rcs=${rcs[*]} mismatch=${mm:-0}"
if [ "${mm:-0}" -ge 1 ]; then
  echo "HARD-STOP: determinism mismatch recorded"
  exit 42
fi
exit "$rc"
