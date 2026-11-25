#!/bin/bash
set -euo pipefail
# Usage: ./run_s5_gate_bench.sh /path/to/dfpn /path/to/exact-record.csv OUTDIR
DFPN=$1
RECORD=$2
OUT=${3:-s5-gate-bench}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
python3 "$HERE/s5_gate_bench.py" prepare "$RECORD" "$OUT/s5roots.csv" --manifest "$OUT/manifest.json" --stones 5
if ! "$DFPN" --help 2>&1 | grep -q 'residual-iso-gate'; then echo 'dfpn lacks residual micro-solver flags; native integration not built' >&2; exit 2; fi
for G in 0 4 5 6 7; do
 CSV="$OUT/gate_$G.csv"
 /usr/bin/time -f '%e' -o "$OUT/gate_$G.wall" "$DFPN" --n=11 --memo=22 --exact-replay="$OUT/s5roots.csv" --only=5 --exact-replay-budget=10000000 --residual-micro-gate=12 --residual-iso-gate="$G" --csv="$CSV" >"$OUT/gate_$G.stdout" 2>"$OUT/gate_$G.stderr"
done
python3 "$HERE/s5_gate_bench.py" compare "$OUT/gate_0.csv" "$OUT/gate_4.csv" "$OUT/gate_5.csv" "$OUT/gate_6.csv" "$OUT/gate_7.csv" --out "$OUT/verdict-audit.json"
python3 - "$OUT" <<'PY'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); rows=[]
for g in [0,4,5,6,7]:
 rows.append({'iso_gate':g,'wall_seconds':float((p/f'gate_{g}.wall').read_text().strip())})
best=min(rows,key=lambda x:x['wall_seconds'])
(p/'wall-summary.json').write_text(json.dumps({'arms':rows,'best':best},indent=2)+'\n')
print(json.dumps({'arms':rows,'best':best},indent=2))
PY
