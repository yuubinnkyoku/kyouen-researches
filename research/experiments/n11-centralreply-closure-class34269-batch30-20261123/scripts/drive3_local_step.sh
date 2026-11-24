#!/bin/bash
# session-local drive-3 step for batch-30 (Part CP, closure class 34269).
# Remaining keys: ac030..ac054 (25 keys). One invocation = at most 2 keys,
# up to 2 runbatch.sh workers in parallel (2-core host). Pre-registered stop
# rules live in the pinned runner (runbatch.sh, byte-clone f591f8c2): WIN
# rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44. WIN-CONTINUE design (Part CP
# drive-3 declaration, Part CE/CK/CN precedent): the runner's rc=45 ends only
# that worker's key unit; the orchestration layer continues with the next wave
# until every remaining key carries a PASS/EXHAUSTED verdict (2-pass
# fresh-cold node-exact). EXHAUSTED rows continue (honest UNKNOWN). Workers are
# wrapped in `timeout 260` so the inner timeout fires before the outer 290s
# tool cap (Part CN lesson: a truncated pass never produced a verdict; the
# runner's replay_done guard re-runs it fresh-cold). The empty-remaining-keys
# case exits ALL-DONE without ever invoking runbatch.sh with an empty key
# (Part CN all-done empty-key guard).
#
# Delta from published drive-2 session script (drive2_local_step.sh 466f475f),
# all three changes pre-registered in the drive-3 declaration:
#   (1) incident-aware MISMATCH checks. status.log carries 2 indexed
#       incident rows (Koyeb zombie-race, drive-2 02:17:46Z/02:19:25Z):
#       "ac028 MISMATCH p1=15000000,2,5087946 p2=" and
#       "ac029 MISMATCH p1=15000000,2,9204933 p2=" (p2 empty = mid-write
#       read, not a determinism divergence; 3 independent write attempts
#       agreed on node counts). Hard-stop therefore happens ONLY on
#       (a) a MISMATCH row with BOTH p1 and p2 non-empty (real divergence),
#       or (b) more than 2 empty-p2 MISMATCH rows (new racing artifacts).
#       The 2 indexed rows alone never fire a stop.
#   (2) flock single-orchestrator guard: the whole invocation takes an
#       exclusive lock on .drive3.lock; a second concurrent step exits
#       rc=46 LOCK-BUSY (retryable, not a hard stop).
#   (3) orphan-liveness guard: if any surviving process whose /proc cmdline
#       matches the actual worker invocation shape "bash scripts/runbatch.sh
#       acNNN" ( optionally behind timeout(1) ) exists at invocation start
#       (Koyeb lesson: an infra-failed parent leaves its workers running),
#       the step exits rc=47 ORPHAN-DETECTED without invoking anything
#       (retryable, not a hard stop; the operator waits for the orphan or
#       records an incident). The match pattern is deliberately narrow so
#       that the bash-tool wrapper processes (whose cmdline carries the
#       orchestration text mentioning runbatch.sh) never self-match.
# Everything else (dedup done-set extraction by distinct key id, 2-key waves,
# timeout 260 wrapper, empty-key guard) is inherited unchanged from 466f475f.
# ac028/ac029 stay in the done set (their published pairs are adopted as
# incident-area evidence, verdict-unconsumed; no fresh reprobe).
set -u
cd "$(dirname "$0")/.."
mkdir -p output/raw
touch output/status.log
exec 9>.drive3.lock
if ! flock -n 9; then
  echo "LOCK-BUSY: another drive-3 step holds .drive3.lock"
  exit 46
fi
orphans=0
for d in /proc/[0-9]*; do
  if tr '\0' ' ' < "$d/cmdline" 2>/dev/null | grep -qE "bash scripts/runbatch\.sh ac[0-9]{3}"; then
    orphans=$((orphans+1))
  fi
done
if [ "$orphans" -gt 0 ]; then
  echo "ORPHAN-DETECTED: $orphans surviving runbatch.sh process(es)"
  exit 47
fi
realmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=[0-9]" output/status.log || true)
incmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=\$" output/status.log || true)
if [ "${realmm:-0}" -ge 1 ]; then
  echo "HARD-STOP: real determinism mismatch (both values present) already recorded"
  exit 42
fi
if [ "${incmm:-0}" -gt 2 ]; then
  echo "HARD-STOP: more than the 2 indexed incident MISMATCH rows recorded"
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
realmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=[0-9]" output/status.log || true)
incmm=$(grep -cE "MISMATCH p1=[0-9][0-9,]* p2=\$" output/status.log || true)
echo "step finished: invoked=$i worker_rcs=${rcs[*]} real_mismatch=${realmm:-0} incident_mismatch=${incmm:-0}"
if [ "${realmm:-0}" -ge 1 ]; then
  echo "HARD-STOP: real determinism mismatch (both values present) recorded"
  exit 42
fi
if [ "${incmm:-0}" -gt 2 ]; then
  echo "HARD-STOP: more than the 2 indexed incident MISMATCH rows recorded"
  exit 42
fi
exit "$rc"
