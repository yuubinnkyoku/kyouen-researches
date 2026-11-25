#!/usr/bin/env python3
"""Materialize the complete canonical s6 boundary below two current hard reply27 s5 roots."""
from __future__ import annotations
import argparse,json,sys
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EDGE=ROOT/"research/experiments/n11-search-methods/scripts"
sys.path.insert(0,str(EDGE))
from dfpn_edge_classes import d4_canonical_key,legal_after  # noqa:E402

HARD=[
    (10376575016438337536,131072),  # model-guided probe unresolved at 15M
    (1297036692818001920,0),        # max-sharing tight probe unresolved at 15M
]

def decode(key):
    lo,hi=key
    pts={p for p in range(64) if (lo>>p)&1}
    pts.update(q+64 for q in range(64) if (hi>>q)&1)
    return pts

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--meta-out",type=Path,required=True)
    ap.add_argument("--hard",action="append",default=[],help="optional lo:hi s5 key; repeatable")
    args=ap.parse_args()

    hard=HARD if not args.hard else [tuple(map(int,x.split(":"))) for x in args.hard]
    if not hard:
        raise SystemExit("no hard s5 roots")
    parents=defaultdict(set); per=[]
    for i,key in enumerate(hard):
        occ=decode(key)
        children={d4_canonical_key(list(occ|{z})) for z in legal_after(occ)}
        per.append(len(children))
        for ch in children: parents[ch].add(i)

    hist=Counter(len(v) for v in parents.values())
    if not parents or any(n==0 for n in per):
        raise SystemExit(f"empty hard boundary per={per}")

    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("w",encoding="utf-8") as fp:
        for seq,key in enumerate(sorted(parents)):
            legal=len(legal_after(decode(key)))
            fp.write(
                f"reply27-hard2-s6,{seq},6,{key[0]},{key[1]},"
                f"{legal},0,1,0,0,0\n"
            )
    meta={
        "hard_s5":[list(k) for k in hard],
        "per_parent_canonical_s6":per,
        "unique_canonical_s6":len(parents),
        "distinct_parent_histogram":dict(sorted(hist.items())),
        "parents":{f"{k[0]}:{k[1]}":sorted(v) for k,v in sorted(parents.items())},
        "claim":"structural boundary only; no outcome asserted",
    }
    args.meta_out.write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"hard_s5":len(hard),"per_parent":per,"unique_s6":len(parents),"parent_hist":dict(sorted(hist.items()))},sort_keys=True))
    print("REPLY27_HARD2_S6_MATERIALIZED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
