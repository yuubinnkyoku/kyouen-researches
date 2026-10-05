#!/usr/bin/env python3
"""Derive exact s5 LOSS verdicts from selected shared s6 LOSS witnesses.

Every parent relation in the metadata is independently regenerated from the
n=11 geometry before use.  A selected s6 result only propagates upward when it
is exact LOSS; WIN or UNKNOWN s6 probes do not classify a parent because the
selected probes are not the complete s6 boundary.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EDGE=ROOT/"research/experiments/n11-search-methods/scripts"
sys.path.insert(0,str(EDGE))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def points_from_key(key):
    lo,hi=key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise SystemExit(f"key outside n=11 board: {key}")
    return tuple(
        [i for i in range(64) if (lo>>i)&1]
        + [i+64 for i in range(57) if (hi>>i)&1]
    )


def canonical_safe_key(key, stones):
    pts=points_from_key(key)
    if len(pts)!=stones or has_forbidden_quad(pts):
        raise SystemExit(f"not a safe s{stones} key: {key}")
    return d4_canonical_key(pts)


def verify_relations(meta):
    probes={}
    relation_count=0
    all_parents=set()
    normalized=0
    for p in meta["probes"]:
        raw=tuple(p["key"])
        s6=canonical_safe_key(raw,6)
        normalized+=raw!=s6
        if s6 in probes:
            raise SystemExit(f"duplicate D4 probe: {raw}")
        # Deleting a point from a safe s6 proves a legal extension of s5.
        # Canonicalize both ends: historical metadata used a different D4
        # representative for some s6 positions, and replay echoes that input.
        pts=points_from_key(s6)
        if len(legal_after(set(pts)))!=p["legal"]:
            raise SystemExit(f"metadata legal count mismatch: {raw}")
        predecessors={d4_canonical_key([x for x in pts if x!=z]) for z in pts}
        parents=set()
        # Metadata records only parents in the chosen frontier, not every
        # possible predecessor. Do not require equality with predecessors.
        for raw_parent in map(tuple,p["parents"]):
            parent=canonical_safe_key(raw_parent,5)
            if parent not in predecessors:
                raise SystemExit(f"invalid parent relation {raw_parent} -> {raw}")
            if parent in parents:
                raise SystemExit(f"duplicate D4 parent: {raw_parent}")
            parents.add(parent)
            relation_count+=1
        probes[s6]={**p,"key":list(s6),"parents":sorted(parents)}
        all_parents.update(parents)
    if len(probes)!=16:
        raise SystemExit(f"expected 16 probes, got {len(probes)}")
    if len(all_parents)!=meta["covered_s5_parents"]:
        raise SystemExit(f"parent union mismatch {len(all_parents)} != {meta['covered_s5_parents']}")
    return probes,relation_count,len(all_parents),normalized


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--meta",type=Path,required=True)
    ap.add_argument("--replay",nargs="+",required=True)
    ap.add_argument("--cache-out",type=Path,required=True)
    ap.add_argument("--summary-out",type=Path)
    args=ap.parse_args()

    meta=json.loads(args.meta.read_text(encoding="utf-8"))
    probes,relation_count,parent_count,normalized=verify_relations(meta)

    result={}
    paths=[]
    for pattern in args.replay:
        paths.extend(glob.glob(pattern))
    if not paths:
        raise SystemExit("no replay files")
    for path in sorted(set(paths)):
        with open(path,newline="",encoding="utf-8") as fp:
            for row in csv.reader(fp):
                if not row or row[0]!="replay":
                    continue
                if len(row)!=11 or int(row[2])!=6 or int(row[4])!=1:
                    raise SystemExit(f"not an s6 OR replay row: {row}")
                key=canonical_safe_key((int(row[9]),int(row[10])),6)
                verdict=int(row[6])
                if key not in probes:
                    raise SystemExit(f"unexpected s6 key {key}")
                if int(row[3])!=probes[key]["legal"]:
                    raise SystemExit(f"replay legal count mismatch: {key}")
                if verdict not in (0,1,2):
                    raise SystemExit(f"bad verdict {verdict}: {key}")
                old=result.get(key)
                if old is not None and old!=verdict:
                    raise SystemExit(f"CONFLICT {key}: {old} vs {verdict}")
                result[key]=verdict

    missing=set(probes)-set(result)
    if missing:
        raise SystemExit(f"missing probe results: {len(missing)}")

    parent_loss=set()
    for key,verdict in result.items():
        if verdict==2:
            parent_loss.update(map(tuple,probes[key]["parents"]))

    args.cache_out.parent.mkdir(parents=True,exist_ok=True)
    with args.cache_out.open("w",encoding="utf-8") as fp:
        fp.write(
            "# s5 verdict cache: n=11 schema=1 "
            "(selected shared-s6 LOSS witnesses; UNKNOWN omitted)\n"
        )
        for lo,hi in sorted(parent_loss):
            fp.write(f"s5verdict,{lo},{hi},5,2,0\n")

    hist={v:list(result.values()).count(v) for v in (0,1,2)}
    summary={
        "probes":len(probes),
        "verified_parent_relations":relation_count,
        "distinct_candidate_parents":parent_count,
        "normalized_metadata_keys":normalized,
        "s6_result_counts":hist,
        "derived_s5_loss":len(parent_loss),
        "canonical_s6_verdicts":[{"key":list(k),"verdict":v} for k,v in sorted(result.items())],
    }
    if args.summary_out:
        args.summary_out.parent.mkdir(parents=True,exist_ok=True)
        args.summary_out.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(summary,sort_keys=True))
    print("SHARED_S6_WITNESS_CACHE_OK")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
