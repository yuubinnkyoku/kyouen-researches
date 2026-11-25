#!/usr/bin/env python3
"""Refine a cache-aware reply27 repair frontier for distinct unknown s5 union.

The upstream MILP minimizes the additive sum of uncached s5 children.  This
script independently rebuilds all 3,384 classes from board geometry, validates
the supplied selected repair, then performs deterministic best-improvement
one-class exchanges that preserve complete vertex coverage while directly
minimizing the DISTINCT union of uncached canonical s5 roots.

This is scheduling optimization only.  UNKNOWN classes are never promoted to
certificates.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

FIRST,R2=60,27


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def load_cache(path:Path):
    _s5_quarantine = quarantined_cache_keys()
    out={}
    with path.open(newline="",encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"): continue
            if row[0]!="s5verdict": continue
            key=(int(row[1]),int(row[2])); value=int(row[4])
            if key in _s5_quarantine:
                continue
            if value not in (1,2):
                raise SystemExit(f"invalid cache verdict {value}: {key}")
            old=out.get(key)
            if old is not None and old!=value:
                raise SystemExit(f"CONFLICT {key}: {old} vs {value}")
            out[key]=value
    return out


def build():
    base={FIRST,R2}
    verts=set(legal_after(base))
    groups=defaultdict(list)
    for a in verts:
        for b in legal_after(base|{a}):
            if b<=a: continue
            groups[d4_canonical_key([FIRST,R2,a,b])].append((a,b))
    assert len(verts)==119 and len(groups)==3384
    coverage={k:{x for a,b in es for x in (a,b)} for k,es in groups.items()}
    children={}
    for k,es in groups.items():
        a,b=es[0]
        occ=base|{a,b}
        children[k]={
            d4_canonical_key(list(occ|{z}))
            for z in legal_after(occ)
        }
    return verts,coverage,children


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--s5-cache",type=Path,required=True)
    ap.add_argument("--initial",type=Path,required=True,
                    help="JSON output of cache_aware_reply27_cover.py")
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()

    cache=load_cache(args.s5_cache)
    verts,coverage,children=build()

    status={}; unknown={}
    for k,ss in children.items():
        vals=[cache.get(ch,0) for ch in ss]
        if 1 in vals: status[k]="WIN"
        elif all(v==2 for v in vals): status[k]="LOSS"
        else:
            status[k]="UNKNOWN"
            unknown[k]={ch for ch in ss if ch not in cache}

    secured=set()
    for k,s in status.items():
        if s=="LOSS": secured.update(coverage[k])

    doc=json.loads(args.initial.read_text(encoding="utf-8"))
    selected=[tuple(x["key"]) for x in doc["repair_selected"]]
    if any(status.get(k)!="UNKNOWN" for k in selected):
        raise SystemExit("initial repair contains non-UNKNOWN class")

    candidates=sorted(k for k,s in status.items() if s=="UNKNOWN")
    selected_set=set(selected)

    def cov(sel):
        got=set(secured)
        for k in sel: got.update(coverage[k])
        return got

    def target_union(sel):
        if not sel: return set()
        return set().union(*(unknown[k] for k in sel))

    if cov(selected_set)!=verts:
        raise SystemExit("initial repair does not cover all vertices")

    before_union=target_union(selected_set)
    before_add=sum(len(unknown[k]) for k in selected_set)
    history=[]

    while True:
        best=None
        current_union=target_union(selected_set)
        current_key=(len(current_union),
                     sum(len(unknown[k]) for k in selected_set),
                     tuple(sorted(selected_set)))
        for old in sorted(selected_set):
            base_sel=selected_set-{old}
            base_cov=cov(base_sel)
            missing=verts-base_cov
            for new in candidates:
                if new in selected_set: continue
                if not missing.issubset(coverage[new]): continue
                trial=base_sel|{new}
                u=target_union(trial)
                key=(len(u),sum(len(unknown[k]) for k in trial),
                     tuple(sorted(trial)))
                if key<current_key and (best is None or key<best[0]):
                    best=(key,old,new)
        if best is None: break
        key,old,new=best
        selected_set.remove(old); selected_set.add(new)
        history.append({
            "remove":list(old),"add":list(new),
            "unique_unknown_s5":key[0],
            "additive_unknown_s5":key[1],
        })

    final_union=target_union(selected_set)
    final_add=sum(len(unknown[k]) for k in selected_set)
    assert cov(selected_set)==verts
    out={
        "root":[FIRST,R2],
        "cache_entries":len(cache),
        "class_status_counts":dict(sorted(Counter(status.values()).items())),
        "secured_vertices":len(secured),
        "repair_classes":len(selected_set),
        "initial_unique_unknown_s5":len(before_union),
        "initial_additive_unknown_s5":before_add,
        "refined_unique_unknown_s5":len(final_union),
        "refined_additive_unknown_s5":final_add,
        "one_swap_improvements":len(history),
        "history":history,
        "repair_selected":[
            {
                "key":list(k),
                "coverage":sorted(coverage[k]),
                "uncached_s5":len(unknown[k]),
            }
            for k in sorted(selected_set)
        ],
        "claim":"scheduling frontier only; UNKNOWN classes are not certificates",
    }
    text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    print("CACHE_AWARE_REPLY27_UNION_REFINE_OK")
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
