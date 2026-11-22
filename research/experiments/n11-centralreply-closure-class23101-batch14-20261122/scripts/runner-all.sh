#!/bin/bash
# batch14 runner-all: 4-key waves in probe order, resume-safe (skips PASSed keys),
# stops launching new waves if any rc >= 42 (42 mismatch / 43 p1fail / 44 p2fail / 45 WIN-HALT).
# In-flight wave members always complete. Records to output/status.log.
set -u
cd "$(dirname "$0")/.."
declare -a ALL=()
for i in $(seq -w 1 52); do ALL+=(q0$i); done
echo "$(date -u +%FT%TZ) RUNNER-START host=$(hostname) cores=$(nproc)" >> output/status.log
while :; do
  declare -a todo=()
  for k in "${ALL[@]}"; do
    if grep -qE " ${k} (PASS|WIN-HALT|MISMATCH)" output/status.log 2>/dev/null; then continue; fi
    todo+=("$k")
  done
  n=${#todo[@]}
  if [ "$n" -eq 0 ]; then
    echo "$(date -u +%FT%TZ) ALL-DONE" >> output/status.log
    break
  fi
  wave=("${todo[@]:0:4}")
  echo "$(date -u +%FT%TZ) WAVE-START ${wave[*]}" >> output/status.log
  declare -a pids=()
  for k in "${wave[@]}"; do
    bash scripts/runbatch.sh "$k" > "/tmp/b14.$k.log" 2>&1 &
    pids+=($!)
  done
  stop=0
  for p in "${pids[@]}"; do
    wait "$p"; rc=$?
    if [ "$rc" -ge 42 ]; then stop=1; fi
  done
  if [ "$stop" -eq 1 ]; then
    echo "$(date -u +%FT%TZ) RUNNER-STOP stop-condition rc>=42 in wave" >> output/status.log
    break
  fi
done
echo "$(date -u +%FT%TZ) RUNNER-EXIT" >> output/status.log
