#!/bin/bash
# session-local drive-1 step for batch-31 (Part CY, closure class 5804).
# Fork of the published batch-30 v2 (sha256 e7b627a8...): functional body
# identical (same done-set/WIN-HALT wave logic, same worker/timeout design);
# only the key-id regex classes ac[0-9]{3} -> ad[0-9]{3} and this header
# target line changed (minimal-delta discipline, pre-registered in the
# Part CY declaration). The v2 history comment below is kept verbatim.
# One invocation = at most 2 keys, up to 2 runbatch.sh workers in parallel
# (2-core host). Pre-registered stop rules live in the pinned runner
# (runbatch.sh, byte-clone f591f8c2): WIN rc=45 / MISMATCH rc=42 / p1/p2 fail
# rc=43/44. The orchestration layer halts the WAVE once the status log
# carries WIN-HALT lines for >= 2 DISTINCT keys (drive-1 WIN-HALT design,
# batch-28 drive-1/2 and batch-29 succession). EXHAUSTED rows continue
# (honest UNKNOWN). Workers are wrapped in `timeout 260` so the inner
# timeout fires before the outer 290s tool cap (Part CN lesson: a truncated
# pass never produced a verdict; the runner's replay_done guard re-runs it
# fresh-cold). The empty-remaining-keys case exits ALL-DONE without ever
# invoking runbatch.sh with an empty key (Part CN all-done empty-key guard).
#
# v2 (honest fix, pre-publication): v1's done-extraction regex matched
# "PASS acNNN" instead of the actual status line form "acNNN PASS", so a
# completed wave pair was re-invoked once (no solver re-run happened: the
# pinned runner skips existing complete pass files; only duplicate status
# lines were appended, and duplicate WIN-HALT lines of a single key wrongly
# halted the wave at wins=2 for 1 key). v2 deduplicates by distinct key id
# for both the done set and the WIN count. The append-only status.log keeps
# the v1 duplicate lines; disclosure lives in the README/completion log.
set -u
cd "$(dirname "$0")/.."
mkdir -p output/raw
touch output/status.log
windistinct=$(node -e '
const fs = require("fs");
const t = fs.readFileSync("output/status.log", "utf8").split("\n");
const s = new Set();
for (const line of t) {
  const m = line.match(/\b(ad[0-9]{3}) WIN-HALT/);
  if (m) s.add(m[1]);
}
console.log(s.size);')
if [ "$windistinct" -ge 2 ]; then
  echo "WAVE-HALTED wins_distinct=$windistinct (drive-1 pre-registered WIN-HALT wave end)"
  exit 0
fi
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
  const m = line.match(/\b(ad[0-9]{3}) (?:PASS|EXHAUSTED)/);
  if (m) done.add(m[1]);
  const w = line.match(/\b(ad[0-9]{3}) WIN-HALT/);
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
wins2=$(node -e '
const fs = require("fs");
const t = fs.readFileSync("output/status.log", "utf8").split("\n");
const s = new Set();
for (const line of t) {
  const m = line.match(/\b(ad[0-9]{3}) WIN-HALT/);
  if (m) s.add(m[1]);
}
console.log(s.size);')
mm=$(grep -c "MISMATCH" output/status.log || true)
echo "step finished: invoked=$i worker_rcs=${rcs[*]} wins_distinct=${wins2:-0} mismatch=${mm:-0}"
if [ "${mm:-0}" -ge 1 ]; then
  echo "HARD-STOP: determinism mismatch recorded"
  exit 42
fi
if [ "${wins2:-0}" -ge 2 ]; then
  echo "WAVE-HALTED wins_distinct=$wins2 (drive-1 pre-registered WIN-HALT wave end)"
  exit 45
fi
exit "$rc"
