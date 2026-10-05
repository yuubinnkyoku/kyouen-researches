#!/usr/bin/env python3
"""Materialize high-sharing canonical s6 probes from an n=11 s5 frontier.

Input rows are exact-replay-style s5 targets with canonical (lo,hi) in columns
3,4.  Every legal one-ply child is D4-canonicalized.  Candidate s6 roots are
ranked greedily by the number of *new distinct parent s5 roots* they can cover,
then by lower s6 legal count and higher total parent multiplicity.

The output contains only structure.  No s5 or s6 verdict is inferred.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EDGE=ROOT/"research/experiments/n11-search-methods/scripts"
sys.path.insert(0,str(EDGE))
from dfpn_edge_classes import d4_canonical_key,legal_after  # noqa: E402


def points_from_key(key):
    lo,hi=key
    pts=[i for i in range(64) if (lo>>i)&1]
    pts.extend(i+64 for i in range(57) if (hi>>i)&1)
    return tuple(pts)


def exact_row(tag,seq,key,legal):
    return f"{tag},{seq},6,{key[0]},{key[1]},{legal},0,0,0,0,0\n"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--targets",type=Path,required=True)
    ap.add_argument("--count",type=int,default=16)
    ap.add_argument("--min-parents",type=int,default=2)
    ap.add_argument("--exclude-s6",type=Path,action="append",default=[])
    ap.add_argument("--csv-out",type=Path,required=True)
    ap.add_argument("--meta-out",type=Path,required=True)
    args=ap.parse_args()
    if args.count<1 or args.min_parents<2:
        raise SystemExit("invalid count/min-parents")

    parents={}
    with args.targets.open(newline="",encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if len(row)<5:
                raise SystemExit(f"short target row: {row}")
            key=(int(row[3]),int(row[4]))
            pts=points_from_key(key)
            if len(pts)!=5:
                raise SystemExit(f"not an s5 target: {key}")
            parents[key]=pts
    if not parents:
        raise SystemExit("empty s5 target set")

    excluded=set()
    for path in args.exclude_s6:
        with path.open(newline="",encoding="utf-8") as fp:
            for row in csv.reader(fp):
                if not row or row[0].startswith("#"):
                    continue
                if len(row)<5:
                    continue
                key=(int(row[3]),int(row[4]))
                pts=points_from_key(key)
                if len(pts)==6:
                    excluded.add(d4_canonical_key(list(pts)))

    parent_map=defaultdict(set)
    raw_transitions=0
    for pk,pts in parents.items():
        occ=set(pts)
        for z in legal_after(occ):
            ck=d4_canonical_key(list(pts)+[z])
            parent_map[ck].add(pk)
            raw_transitions+=1

    candidates={
        k:ps for k,ps in parent_map.items()
        if len(ps)>=args.min_parents and k not in excluded
    }
    legal_cache={}
    def legal_count(k):
        if k not in legal_cache:
            legal_cache[k]=len(legal_after(set(points_from_key(k))))
        return legal_cache[k]

    chosen=[]
    covered=set()
    remaining=set(candidates)
    for seq in range(args.count):
        best=None
        best_rank=None
        for k in remaining:
            ps=candidates[k]
            new=ps-covered
            if not new:
                continue
            rank=(-len(new),legal_count(k),-len(ps),k[1],k[0])
            if best_rank is None or rank<best_rank:
                best_rank=rank; best=(k,new)
        if best is None:
            break
        k,new=best
        chosen.append({
            "key":list(k),
            "legal":legal_count(k),
            "parents":[list(p) for p in sorted(candidates[k])],
            "parent_count":len(candidates[k]),
            "new_parent_count":len(new),
        })
        covered.update(new)
        remaining.remove(k)

    args.csv_out.parent.mkdir(parents=True,exist_ok=True)
    with args.csv_out.open("w",encoding="utf-8") as fp:
        for seq,row in enumerate(chosen):
            fp.write(exact_row("reply27-shared-s6",seq,tuple(row["key"]),row["legal"]))

    meta={
        "source_targets":str(args.targets),
        "s5_frontier":len(parents),
        "raw_s5_to_s6_transitions":raw_transitions,
        "canonical_s6":len(parent_map),
        "candidate_s6_min_parents":len(candidates),
        "excluded_s6":len(excluded),
        "selected_probes":len(chosen),
        "covered_s5_parents":len(covered),
        "selection_rule":"maximize newly covered distinct s5 parents, then low s6 legal count, then total parent count",
        "probes":chosen,
        "claim":"structural probe selection only; exact s6 replay is required for any parent verdict",
    }
    args.meta_out.parent.mkdir(parents=True,exist_ok=True)
    args.meta_out.write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "s5_frontier":len(parents),
        "raw_transitions":raw_transitions,
        "canonical_s6":len(parent_map),
        "candidate_s6":len(candidates),
        "selected":len(chosen),
        "covered_parents":len(covered),
    },sort_keys=True))
    print("SHARED_S6_PROBES_OK")


if __name__=="__main__":
    raise SystemExit(main())
