#!/usr/bin/env python3
"""Analyze decisive s6 witness rank below the reply27 hard9 s5 boundary.

Consumes the archived hard9 boundary metadata plus exact replay outputs.
No game verdict is inferred from a heuristic: all labels come from exact replay.
The script only measures how early a known LOSS child appears when each parent
orders its canonical s6 children by legal-move count ascending or descending.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--meta", type=Path, required=True)
    ap.add_argument("--replay", nargs="+", required=True)
    args=ap.parse_args()

    meta=json.loads(args.meta.read_text(encoding="utf-8"))
    hard=[tuple(x) for x in meta["hard_s5"]]
    parents={
        tuple(map(int,k.split(":"))): list(v)
        for k,v in meta["parents"].items()
    }

    rows={}
    paths=[]
    for pat in args.replay:
        paths.extend(glob.glob(pat))
    if not paths:
        raise SystemExit("no replay files")
    for p in sorted(set(paths)):
        with open(p,newline="",encoding="utf-8") as fp:
            for r in csv.reader(fp):
                if not r or r[0]!="replay":
                    continue
                key=(int(r[9]),int(r[10]))
                cur=(int(r[6]),int(r[3]),int(r[7]))
                old=rows.get(key)
                if old is not None and old!=cur:
                    raise SystemExit(f"CONFLICT {key}: {old} vs {cur}")
                rows[key]=cur

    if set(rows)!=set(parents):
        raise SystemExit(
            f"boundary mismatch rows={len(rows)} expected={len(parents)}"
        )

    child=[[] for _ in hard]
    for key,ps in parents.items():
        for p in ps:
            child[p].append(key)

    desc_ranks=[]; asc_ranks=[]; target92_ranks=[]; details=[]
    desc_nodes=[]; asc_nodes=[]; target92_nodes=[]
    for i,kids in enumerate(child):
        desc=sorted(kids,key=lambda k:(-rows[k][1],k))
        asc=sorted(kids,key=lambda k:( rows[k][1],k))
        target92=sorted(kids,key=lambda k:(abs(rows[k][1]-92),-rows[k][1],k))
        def first_loss(order):
            cumulative=0
            for rank,key in enumerate(order,1):
                verdict,legal,nodes=rows[key]
                cumulative += nodes
                if verdict==2:
                    return rank,legal,key,nodes,cumulative
            return None
        d=first_loss(desc); a=first_loss(asc); t=first_loss(target92)
        if d is not None:
            desc_ranks.append(d[0]); asc_ranks.append(a[0]); target92_ranks.append(t[0])
            desc_nodes.append(d[4]); asc_nodes.append(a[4]); target92_nodes.append(t[4])
        details.append({
            "parent_index":i,
            "children":len(kids),
            "status":"LOSS" if d is not None else "WIN",
            "first_loss_desc":None if d is None else {
                "rank":d[0],"legal":d[1],"key":list(d[2]),"nodes":d[3],
                "cumulative_cold_nodes":d[4]},
            "first_loss_asc":None if a is None else {
                "rank":a[0],"legal":a[1],"key":list(a[2]),"nodes":a[3],
                "cumulative_cold_nodes":a[4]},
            "first_loss_target92":None if t is None else {
                "rank":t[0],"legal":t[1],"key":list(t[2]),"nodes":t[3],
                "cumulative_cold_nodes":t[4]},
        })

    hist=Counter(v for v,_,_ in rows.values())
    legal_by_result={}
    for verdict in (0,1,2):
        vals=[legal for v,legal,_ in rows.values() if v==verdict]
        legal_by_result[str(verdict)]={
            "n":len(vals),
            "min":min(vals) if vals else None,
            "max":max(vals) if vals else None,
            "mean":mean(vals) if vals else None,
            "median":median(vals) if vals else None,
        }

    out={
        "boundary_s6":len(rows),
        "s6_result_counts":{"UNKNOWN":hist[0],"WIN":hist[1],"LOSS":hist[2]},
        "legal_by_result":legal_by_result,
        "loss_parent_count":len(desc_ranks),
        "loss_witness_rank_desc":desc_ranks,
        "loss_witness_rank_asc":asc_ranks,
        "desc_rank_mean":mean(desc_ranks),
        "desc_rank_median":median(desc_ranks),
        "desc_rank_max":max(desc_ranks),
        "asc_rank_mean":mean(asc_ranks),
        "asc_rank_median":median(asc_ranks),
        "asc_rank_max":max(asc_ranks),
        "target92_rank_mean":mean(target92_ranks),
        "target92_rank_median":median(target92_ranks),
        "target92_rank_max":max(target92_ranks),
        "desc_cumulative_cold_nodes":sum(desc_nodes),
        "asc_cumulative_cold_nodes":sum(asc_nodes),
        "target92_cumulative_cold_nodes":sum(target92_nodes),
        "top2_desc_covers":sum(r<=2 for r in desc_ranks),
        "top6_desc_covers":sum(r<=6 for r in desc_ranks),
        "top14_desc_covers":sum(r<=14 for r in desc_ranks),
        "details":details,
        "claim":"finite exact-boundary ordering measurement only",
    }
    print(json.dumps(out,indent=2,sort_keys=True))
    print("HARD9_S6_ORDERING_ANALYSIS_OK")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
