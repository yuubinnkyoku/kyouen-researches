#!/bin/bash
# Full sound-mode 3xm q=4 deficient-maximal exclusion, split across cores.
# Each chunk writes its own JSONL so a partial run stays auditable.
set -u
BIN=${1:-/tmp/q34/sound}
OUT=${2:-/tmp/q34}
mkdir -p "$OUT"
chunks="24:30 31:36 37:41 42:46 47:51 52:56 57:60 61:64 65:68"
pids=()
for c in $chunks; do
    lo=${c%%:*}; hi=${c##*:}
    "$BIN" "$lo" "$hi" 0 > "$OUT/sound_${lo}_${hi}.jsonl" 2>"$OUT/sound_${lo}_${hi}.err" &
    pids+=($!)
done
fail=0
for p in "${pids[@]}"; do
    wait "$p" || fail=1
done
cat "$OUT"/sound_*.jsonl > "$OUT/sound_all_unsorted.jsonl"
python3 - "$OUT/sound_all_unsorted.jsonl" "$OUT/sound_all.jsonl" <<'PY'
import json,sys
rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
rows.sort(key=lambda r: r["m"])
with open(sys.argv[2],"w") as f:
    for r in rows: f.write(json.dumps(r,separators=(",",":"))+"\n")
print("lengths",len(rows),"covered",sum(1 for r in rows if any(r["cover_exists"])))
print("range",min(r["m"] for r in rows),max(r["m"] for r in rows))
PY
echo "chunks_failed=$fail"