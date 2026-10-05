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
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402


def points_from_key(key):
    lo,hi=key
    return tuple(
        [i for i in range(64) if (lo>>i)&1]
        + [i+64 for i in range(57) if (hi>>i)&1]
    )


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--meta",type=Path,required=True)
    ap.add_argument("--replay",nargs="+",required=True)
    ap.add_argument("--cache-out",type=Path,required=True)
    args=ap.parse_args()

    meta=json.loads(args.meta.read_text(encoding="utf-8"))
    probes={tuple(p["key"]):p for p in meta["probes"]}
    if len(probes)!=16:
        raise SystemExit(f"expected 16 probes, got {len(probes)}")

    # Independently verify every recorded parent->child relation.
    relation_count=0
    all_parents=set()
    for s6,p in probes.items():
        s6_pts=points_from_key(s6)
        if len(s6_pts)!=6:
            raise SystemExit(f"not an s6 key: {s6}")
        # The replay target may be a raw representative rather than the D4
        # canonical key. Exact game value is symmetry invariant, but parent
        # incidence must be checked against the canonical child identity used
        # by the frontier maps.
        s6_canon=d4_canonical_key(list(s6_pts))
        for parent in map(tuple,p["parents"]):
            pts=points_from_key(parent)
            if len(pts)!=5:
                raise SystemExit(f"not an s5 parent: {parent}")
            children={
                d4_canonical_key(list(pts)+[z])
                for z in legal_after(set(pts))
            }
            if s6_canon not in children:
                raise SystemExit(
                    f"invalid parent relation {parent} -> raw {s6} "
                    f"(canonical {s6_canon})"
                )
            relation_count+=1
            all_parents.add(parent)

    if len(all_parents)!=meta["covered_s5_parents"]:
        raise SystemExit(
            f"parent union mismatch {len(all_parents)} != "
            f"{meta['covered_s5_parents']}"
        )

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
                key=(int(row[9]),int(row[10]))
                verdict=int(row[6])
                if key not in probes:
                    raise SystemExit(f"unexpected s6 key {key}")
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
    print(json.dumps({
        "probes":len(probes),
        "verified_parent_relations":relation_count,
        "distinct_candidate_parents":len(all_parents),
        "s6_result_counts":hist,
        "derived_s5_loss":len(parent_loss),
    },sort_keys=True))
    print("SHARED_S6_WITNESS_CACHE_OK")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
