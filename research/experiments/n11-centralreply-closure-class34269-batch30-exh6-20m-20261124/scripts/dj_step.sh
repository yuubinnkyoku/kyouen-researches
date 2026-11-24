#!/bin/bash
# session step for Part DJ batch-30 EXH-6 20M reprobe (closure class 34269).
# Remaining keys: ac006/ac013/ac032/ac036/ac044/ac047 (previously EXHAUSTED at
# 15M budget in the published batch-30 drives, honest UNKNOWN). One invocation
# = at most 2 keys, up to 2 runner workers in parallel. Pre-registered stop
# rules live in the DJ runner (runner_dj.sh = pinned runbatch.sh f591f8c2
# byte-clone with the single declared delta BUDGET=15000000 -> 20000000):
# WIN rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44. WIN-CONTINUE (drive-3
# precedent): rc=45 ends only that worker's key unit; the step continues with
# the next wave until every remaining key carries a PASS/EXHAUSTED verdict
# (2-pass fresh-cold node-exact). EXHAUSTED-at-20M rows continue (honest
# UNKNOWN; a same-condition re-probe is forbidden, the next budget tier is a
# separate declared lane). Workers are wrapped in `timeout 260` so the inner
# timeout fires before the outer 290s tool cap (Part CN lesson; a truncated
# pass never produced a verdict, the runner's replay_done guard re-runs it
# fresh-cold). The empty-remaining-keys case exits ALL-DONE without invoking
# the runner with an empty key (Part CN all-done empty-key guard).
#
# Deltas from the published drive-3 session script
# (drive3_local_step.sh 41c5719c...):
#   (1) lock file renamed .dj.lock (separate Part, separate lock).
#   (2) worker/orphan pattern renamed runner_dj.sh.
#   (3) MISMATCH policy is STRICT: this Part's status.log is fresh and
#       single-writer, so ANY MISMATCH row (real divergence with both values,
#       or any empty-p2 row) is a hard-stop rc=42. The drive-3 incident
#       allowances (2 indexed empty-p2 rows) do NOT apply here.
# Everything else (done-set extraction, 2-key waves, timeout 260 wrapper,
# empty-key guard, flock single-orchestrator guard, orphan-liveness guard) is
# inherited unchanged.
set -u
cd "$(dirname "$0")/.."
mkdir -p output/raw
touch output/status.log
exec 9>.dj.lock
if ! flock -n 9; then
  echo "LOCK-BUSY: another DJ step holds .dj.lock"
  exit 46
fi
orphans=0
for d in /proc/[0-9]*; do
  if tr '\0' ' ' < "$d/cmdline" 2>/dev/null | grep -qE "bash scripts/runner_dj\.sh ac[0-9]{3}"; then
    orphans=$((orphans+1))
  fi
done
if [ "$orphans" -gt 0 ]; then
  echo "ORPHAN-DETECTED: $orphans surviving runner_dj.sh process(es)"
  exit 47
fi
realmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=[0-9]" output/status.log || true)
incmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=$" output/status.log || true)
if [ "${realmm:-0}" -ge 1 ]; then
  echo "HARD-STOP: real determinism mismatch (both values present) already recorded"
  exit 42
fi
if [ "${incmm:-0}" -ge 1 ]; then
  echo "HARD-STOP: any empty-p2 MISMATCH row is a hard-stop for this fresh single-writer lane"
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
  echo "ALL-DONE (no remaining keys; empty-key guard: no runner invocation)"
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
  timeout 260 bash scripts/runner_dj.sh "$k" &
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
realmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=[0-9]" output/status.log || true)
incmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=$" output/status.log || true)
echo "step finished: invoked=$i worker_rcs=${rcs[*]} real_mismatch=${realmm:-0} empty_p2_mismatch=${incmm:-0}"
if [ "${realmm:-0}" -ge 1 ]; then
  echo "HARD-STOP: real determinism mismatch (both values present) recorded"
  exit 42
fi
if [ "${incmm:-0}" -ge 1 ]; then
  echo "HARD-STOP: empty-p2 MISMATCH row recorded (fresh single-writer lane)"
  exit 42
fi
exit "$rc"
