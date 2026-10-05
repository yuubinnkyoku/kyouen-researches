#!/usr/bin/env bash
set -euo pipefail

BIN="${1:-/tmp/kyouen_dfpn_root}"
OUT="${2:-/tmp/n11-residual-share-gate-sweep}"
mkdir -p "$OUT"

PYTHONPATH=research/experiments/n11-search-methods/scripts python - <<'PY' > "$OUT/fixture.csv"
from dfpn_edge_classes import legal_after, d4_canonical_key
base={0,1,2,60}
z=legal_after(base)[0]
lo,hi=d4_canonical_key(base|{z})
print(f"fixture,0,5,{lo},{hi},0,0,0,0,0,0")
PY

echo "gate,result,wall_s,residual_memo_states,shared_hits,shared_stores,canonicalized,shared_size"
for gate in 0 1 2 3 4 5 6; do
  out="$OUT/gate-$gate.out"
  tf="$OUT/gate-$gate.time"
  args=(--n=11 --memo=18 --exact-replay="$OUT/fixture.csv" --only=5
        --exact-replay-budget=200000 --residual-exact-legal=6 --csv="$out")
  if (( gate > 0 )); then
    args+=(--residual-share-gate="$gate")
  fi
  /usr/bin/time -f '%e' -o "$tf" "$BIN" "${args[@]}"
  result=$(awk -F, '/^replay,/{print $7; exit}' "$out")
  wall=$(cat "$tf")
  read -r memo hits stores canon size < <(
    awk '/^# residual_shadow row=/{
      for(i=1;i<=NF;i++){
        split($i,a,"=")
        if(a[1]=="residual_memo_states") memo=a[2]
        if(a[1]=="shared_hits") hits=a[2]
        if(a[1]=="shared_stores") stores=a[2]
        if(a[1]=="canonicalized") canon=a[2]
        if(a[1]=="shared_size") size=a[2]
      }
    } END{print memo+0,hits+0,stores+0,canon+0,size+0}' "$out"
  )
  echo "$gate,$result,$wall,$memo,$hits,$stores,$canon,$size"
done
