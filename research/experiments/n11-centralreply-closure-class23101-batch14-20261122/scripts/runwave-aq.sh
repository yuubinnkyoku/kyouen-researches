#!/bin/bash
# takeover (Part AQ) wave runner: runs the given keys' p1/p2 in parallel (one
# runbatch.sh per key), logs WAVE-START/WAVE-END to output/status.log, and
# enforces a "# replay_done" completeness guard: any raw file lacking the
# replay_done trailer is discarded (truncated by host event), so the key can
# be re-run fresh-cold later. rc>=42 from a member stops the wave echo.
set -u
cd "$(dirname "$0")/.."
WAVE="$*"
echo "$(date -u +%FT%TZ) WAVE-START $WAVE" >> output/status.log
pids=(); rcs=()
i=0
for k in $WAVE; do
  bash scripts/runbatch.sh "$k" > "output/raw/$k.wave.log" 2>&1 &
  pids+=($!)
done
stop=0
for p in "${pids[@]}"; do
  wait "$p"; rc=$?
  rcs+=($rc)
  if [ "$rc" -ge 42 ]; then stop=1; fi
done
# completeness guard for-this-wave keys
for k in $WAVE; do
  for pass in p1 p2; do
    f="output/raw/$k.$pass.out"
    if [ -f "$f" ] && ! grep -q "# replay_done" "$f"; then
      rm -f "$f"
      echo "$(date -u +%FT%TZ) TRUNCATED-DISCARDED $k.$pass" >> output/status.log
      stop=2
    fi
  done
done
echo "$(date -u +%FT%TZ) WAVE-END ${WAVE} stop=$stop" >> output/status.log
exit $stop
