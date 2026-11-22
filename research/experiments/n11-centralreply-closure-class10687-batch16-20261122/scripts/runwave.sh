#!/bin/bash
# runwave.sh -- foreground one-wave executor (host recycles kill background
# runners between turns; each invocation completes exactly one 4-key wave and
# checkpoints all raws under this kit dir). Picks the next undone keys from
# output/status.log, honors the same stop rules as runner-all.sh.
set -u
cd "$(dirname "$0")/.."
declare -a todo=()
for i in $(seq -w 1 52); do
  k="t0$i"
  if grep -qE " ${k} (PASS|WIN-HALT|MISMATCH)" output/status.log 2>/dev/null; then continue; fi
  todo+=("$k")
done
n=${#todo[@]}
if [ "$n" -eq 0 ]; then echo "ALL-DONE"; exit 0; fi
wave=("${todo[@]:0:4}")
echo "$(date -u +%FT%TZ) WAVE-START ${wave[*]}" >> output/status.log
declare -a pids=()
for k in "${wave[@]}"; do
  bash scripts/runbatch.sh "$k" > "/tmp/b16.$k.log" 2>&1 &
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
echo "WAVE-DONE (${wave[*]}) remaining=$((n-4))"
