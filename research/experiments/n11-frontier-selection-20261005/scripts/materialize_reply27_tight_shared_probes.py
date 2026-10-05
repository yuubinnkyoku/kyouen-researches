#!/usr/bin/env python3
"""Materialize highest-sharing UNKNOWN s5 roots across all dual-tight reply27 classes.

Given a current exact s5 cache and the exact cardinality/dual certificate, rebuild
all 3,384 canonical s4 classes.  A class is "dual-tight" when the sum of positive
dual vertex weights on its coverage is exactly 1; every class in a minimum-cardinality
certificate must be dual-tight when the dual lower bound equals the integer optimum.

Among currently UNKNOWN dual-tight classes, count how many classes contain each
uncached canonical s5 child.  Emit all children attaining the maximum sharing
frequency (optionally capped).  This is scheduling only.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SCRIPTS=ROOT/"research/experiments/n11-frontier-selection-20261005/scripts"
sys.path.insert(0,str(SCRIPTS))
import cache_aware_reply27_cardinality as C  # noqa: E402
from dfpn_edge_classes import legal_after  # noqa: E402


def decode_key(key):
    lo,hi=key
    pts={p for p in range(64) if (lo>>p)&1}
    pts.update(q+64 for q in range(64) if (hi>>q)&1)
    return pts


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--s5-cache",type=Path,required=True)
    ap.add_argument("--cardinality",type=Path,required=True)
    ap.add_argument("--csv-out",type=Path,required=True)
    ap.add_argument("--json-out",type=Path)
    ap.add_argument("--cap",type=int,default=32)
    args=ap.parse_args()

    cache=C.load_cache(args.s5_cache)
    card=json.loads(args.cardinality.read_text(encoding="utf-8"))
    if not card.get("dual_certificate_matches_integer_optimum"):
        raise SystemExit("dual certificate is not tight")
    weights={int(v):Fraction(w) for v,w in card["dual_positive_weights"].items()}

    verts,coverage,children=C.build()
    status={}
    unknown={}
    for key,ss in children.items():
        vals=[cache.get(ch,0) for ch in ss]
        if 1 in vals:
            status[key]="WIN"
        elif vals and all(v==2 for v in vals):
            status[key]="LOSS"
        else:
            status[key]="UNKNOWN"
            unknown[key]={ch for ch in ss if ch not in cache}

    tight=[]
    for key,st in status.items():
        if st!="UNKNOWN":
            continue
        w=sum((weights.get(v,Fraction(0)) for v in coverage[key]),Fraction(0))
        if w==1:
            tight.append(key)

    freq=Counter()
    owners=defaultdict(list)
    for key in tight:
        for ch in unknown[key]:
            freq[ch]+=1
            owners[ch].append(key)
    if not freq:
        raise SystemExit("no unknown children in dual-tight classes")
    maxfreq=max(freq.values())
    chosen=sorted(
        (ch for ch,n in freq.items() if n==maxfreq),
        key=lambda ch:(len(legal_after(decode_key(ch))),ch[1],ch[0]),
    )
    if args.cap>0:
        chosen=chosen[:args.cap]

    args.csv_out.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    with args.csv_out.open("w",encoding="utf-8") as fp:
        for seq,ch in enumerate(chosen):
            legal=len(legal_after(decode_key(ch)))
            fp.write(
                f"reply27-tight-shared,{seq},5,{ch[0]},{ch[1]},"
                f"{legal},0,0,0,0,0\n"
            )
            rows.append({
                "key":list(ch),
                "legal":legal,
                "frequency":freq[ch],
                "classes":[
                    {
                        "key":list(k),
                        "coverage":sorted(coverage[k]),
                        "unknown_s5":len(unknown[k]),
                    }
                    for k in sorted(owners[ch])
                ],
            })

    hist=Counter(freq.values())
    out={
        "root":[C.FIRST,C.R2],
        "cache_entries":len(cache),
        "dual_positive_vertices":len(weights),
        "minimum_additional_classes":card["minimum_additional_classes"],
        "dual_tight_unknown_classes":len(tight),
        "unique_unknown_s5_across_tight_classes":len(freq),
        "sharing_frequency_histogram":dict(sorted(hist.items())),
        "maximum_sharing_frequency":maxfreq,
        "emitted_probes":len(rows),
        "probes":rows,
        "claim":"scheduling only; exact probe verdicts remain required",
    }
    text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    print("REPLY27_TIGHT_SHARED_PROBES_OK")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(text,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
