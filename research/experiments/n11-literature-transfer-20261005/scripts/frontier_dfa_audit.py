#!/usr/bin/env python3
"""Audit exact finite-language DFA compression on an n=11 proof frontier.

Input is an exact-replay target CSV whose columns 3,4 are the canonical
(lo,hi) bitset key.  The script treats each canonical position as the sorted
sequence of occupied point numbers, builds the complete canonical one-ply
image, and exactly minimizes the finite prefix tries by suffix-language
equivalence.

This measures representation size only.  It does not solve any game state.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EDGE=ROOT/"research/experiments/n11-search-methods/scripts"
sys.path.insert(0,str(EDGE))
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

N=11


def points_from_key(lo:int,hi:int):
    return tuple(
        [i for i in range(64) if (lo>>i)&1]
        + [i+64 for i in range(57) if (hi>>i)&1]
    )


def key_from_points(points):
    return d4_canonical_key(list(points))


def dfa_stats(words):
    nxt=[{}]
    terminal=[False]
    for word in words:
        s=0
        for label in word:
            t=nxt[s].get(label)
            if t is None:
                t=len(nxt)
                nxt[s][label]=t
                nxt.append({})
                terminal.append(False)
            s=t
        terminal[s]=True

    cls=[None]*len(nxt)
    signatures={}
    for s in range(len(nxt)-1,-1,-1):
        sig=(terminal[s],tuple(sorted((a,cls[t]) for a,t in nxt[s].items())))
        if sig not in signatures:
            signatures[sig]=len(signatures)
        cls[s]=signatures[sig]
    return {"trie_states":len(nxt),"minimal_dfa_states":len(signatures)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--targets",type=Path,required=True)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()

    parents=[]
    with args.targets.open(newline="",encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if len(row)<5:
                raise SystemExit(f"short target row: {row}")
            p=points_from_key(int(row[3]),int(row[4]))
            if len(p)!=5:
                raise SystemExit(f"target is not s5: {row[:5]}")
            parents.append(p)

    if len(parents)!=len(set(parents)):
        raise SystemExit("input contains duplicate canonical s5 targets")

    s6=set()
    transitions=0
    parents_by_s6=defaultdict(set)
    transition_multiplicity=Counter()
    for p in parents:
        occ=set(p)
        for z in legal_after(occ):
            k=key_from_points((*p,z))
            q=points_from_key(*k)
            if len(q)!=6:
                raise SystemExit("canonical child is not s6")
            transitions+=1
            s6.add(q)
            parents_by_s6[q].add(p)
            transition_multiplicity[q]+=1

    result={
        "n":N,
        "s5_targets":len(parents),
        "s5_language":dfa_stats(sorted(parents)),
        "raw_s5_to_s6_transitions":transitions,
        "canonical_s6":len(s6),
        "transition_dedup_fraction":(
            1.0-len(s6)/transitions if transitions else 0.0
        ),
        "s6_shared_by_multiple_distinct_parents":sum(
            len(ps)>=2 for ps in parents_by_s6.values()
        ),
        "s6_max_distinct_parent_count":max(
            (len(ps) for ps in parents_by_s6.values()),default=0
        ),
        "s6_reached_by_multiple_raw_transitions":sum(
            v>=2 for v in transition_multiplicity.values()
        ),
        "s6_max_raw_transition_multiplicity":max(
            transition_multiplicity.values(),default=0
        ),
        "s6_language":dfa_stats(sorted(s6)),
        "claim":"exact finite-language representation audit; no game verdict",
    }
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    print("FRONTIER_DFA_AUDIT_OK")
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text,encoding="utf-8")


if __name__=="__main__":
    raise SystemExit(main())
