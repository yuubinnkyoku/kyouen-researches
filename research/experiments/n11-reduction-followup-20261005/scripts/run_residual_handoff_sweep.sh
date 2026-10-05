#!/usr/bin/env bash
set -euo pipefail

BIN="${1:-/tmp/kyouen_dfpn_root}"
OUT="${2:-/tmp/n11-residual-handoff-sweep}"
mkdir -p "$OUT"

PYTHONPATH=research/experiments/n11-search-methods/scripts python - <<'PY' > "$OUT/fixture.csv"
from dfpn_edge_classes import legal_after, d4_canonical_key
base={0,1,2,60}
for i,z in enumerate(legal_after(base)[:3]):
    lo,hi=d4_canonical_key(base|{z})
    print(f"fixture,{i},5,{lo},{hi},0,0,0,0,0,0")
PY

"$BIN" --n=11 --memo=18 --exact-replay="$OUT/fixture.csv" --only=5 \
  --exact-replay-budget=200000 --csv="$OUT/baseline.csv"

for gate in 4 5 6; do
  "$BIN" --n=11 --memo=18 --exact-replay="$OUT/fixture.csv" --only=5 \
    --exact-replay-budget=200000 --residual-exact-legal="$gate" \
    --csv="$OUT/gate-$gate.csv"
done

python - "$OUT" <<'PY'
import csv,re,sys
from pathlib import Path
root=Path(sys.argv[1])

def replay(path):
    ans={}
    nodes=0
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            x=next(csv.reader([line]))
            ans[int(x[1])]=int(x[6]); nodes+=int(x[7])
    return ans,nodes

base,bnodes=replay(root/"baseline.csv")
print("gate,roots_match,board_nodes,exact_calls,residual_memo_states,module_removed,component_splits")
for gate in (4,5,6):
    p=root/f"gate-{gate}.csv"
    got,nodes=replay(p)
    totals={k:0 for k in ("exact_calls","residual_memo_states","module_removed","component_splits")}
    for line in p.read_text().splitlines():
        if line.startswith("# residual_shadow row="):
            d=dict(re.findall(r"(\\w+)=([0-9]+)",line))
            for k in totals: totals[k]+=int(d[k])
    print(gate,got==base,nodes,*[totals[k] for k in totals],sep=",")
print("baseline_nodes",bnodes)
PY
