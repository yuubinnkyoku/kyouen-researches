#!/usr/bin/env python3
"""Audit direct, cold S5 exact verdicts independently of the DFPN engine."""
from __future__ import annotations

import collections
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-reply27-20more-20261011"
RAW = EXP / "output/raw"
BASE = ROOT / "research/experiments/n11-reply27-ten-loss-20261011/output/merged-exact-s5.cache"
GEOM = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
TARGET = (1297036692683752448, 0)
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from independent import Board
from s5_evidence_policy import quarantined_cache_keys

def mask(k):
    return k[0] | (k[1] << 64)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def csvrows(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return [r for r in csv.reader(f) if r and not r[0].startswith("#")]

def cache(path):
    q = quarantined_cache_keys()
    values = {}
    for r in csvrows(path):
        assert len(r) == 6 and r[0] == "s5verdict"
        k=(int(r[1]),int(r[2]))
        val=int(r[4])
        assert int(r[3])==5 and val in (1,2) and k not in q and k not in values
        values[k]=val
    return values

def status(children, exact):
    values=[exact.get(tuple(k),0) for k in children]
    if 1 in values:return "WIN"
    if all(v==2 for v in values):return "LOSS"
    return "UNKNOWN"

def audit():
    board=Board(11)
    chosen=json.loads((EXP/"output/selection.json").read_text())
    assert len(chosen)==20
    preflight={}
    for i in range(10):
        ins=csvrows(RAW/f"target-{i:02}.csv")
        assert len(ins)==2
        for j,r in enumerate(ins):
            assert len(r)==11 and r[0]=="target" and int(r[1])==j and int(r[2])==5
            assert all(int(x)==0 for x in r[6:]), r
            k=(int(r[3]),int(r[4])); legal=int(r[5])
            assert k not in preflight and mask(k).bit_count()==5
            assert board.canonical(mask(k))==mask(k)
            assert board.legal(mask(k)).bit_count()==legal
            meta=chosen[i*2+j]
            assert meta["key"] == f"{k[0]}:{k[1]}" and meta["legal"]==legal and meta["batch"]==i
            preflight[k]=meta
    assert len(preflight)==20
    decisive={}
    for i in range(10):
        rr=[r for r in csvrows(RAW/f"probe-{i:02}.csv") if r[0]=="replay"]
        assert len(rr)==2, (i,len(rr))
        for j,r in enumerate(rr):
            assert len(r)==11
            seq,stones,legal,isor,budget,verdict,nodes,sec,lo,hi=map(int,r[1:])
            k=(lo,hi)
            assert seq==j and stones==5 and isor==0 and budget==15_000_000
            assert k in preflight and k not in decisive
            assert preflight[k]["batch"]==i and preflight[k]["legal"]==legal
            assert verdict==2 and 0<nodes<budget and sec>=0, (i,k,verdict,nodes)
            decisive[k]={"key":[lo,hi],"legal":legal,"nodes":nodes,"reported_seconds":sec,
                         "shared_live_parents":preflight[k]["live_parents"],
                         "csv":f"probe-{i:02}.csv"}
    assert set(decisive)==set(preflight)
    with gzip.open(GEOM,"rt") as f:geometry=json.load(f)
    assert len(geometry)==3384
    parents={tuple(g["key"]):g for g in geometry}
    assert len(parents)==3384 and TARGET in parents
    target=parents[TARGET]
    assert len(target["children"])==106 and target["coverage"]==[100,108,110,120]
    target_children={tuple(k) for k in target["children"]}
    assert set(decisive)<=target_children
    incidences={k:[] for k in decisive}
    for parent,g in parents.items():
        for k in set(map(tuple,g["children"])) & set(decisive):
            assert mask(k) in board.children(mask(parent)), ("illegal edge",parent,k)
            incidences[k].append(parent)
    for k in decisive:
        assert len(incidences[k])>=preflight[k]["live_parents"], (k,incidences[k])
    before=cache(BASE)
    assert len(before)==5765 and sum(v==1 for v in before.values())==159
    assert not set(before)&set(decisive)
    after=dict(before)
    after.update({k:2 for k in decisive})
    assert len(after)==5785 and sum(v==1 for v in after.values())==159 and sum(v==2 for v in after.values())==5626
    old_class=collections.Counter(status(g["children"],before) for g in geometry)
    new_class=collections.Counter(status(g["children"],after) for g in geometry)
    # No new S4 LOSS/WIN class is claimed unless the full child boundary demonstrates it.
    updated=[{"key":list(k),"before":status(parents[k]["children"],before),
              "after":status(parents[k]["children"],after)}
             for k in parents if status(parents[k]["children"],before)!=status(parents[k]["children"],after)]
    t_before={n:sum(before.get(k,0)==v for k in target_children) for n,v in [("UNKNOWN",0),("WIN",1),("LOSS",2)]}
    t_after={n:sum(after.get(k,0)==v for k in target_children) for n,v in [("UNKNOWN",0),("WIN",1),("LOSS",2)]}
    assert t_before=={"UNKNOWN":86,"WIN":0,"LOSS":20}
    assert t_after=={"UNKNOWN":66,"WIN":0,"LOSS":40}
    assert new_class==old_class==collections.Counter({"LOSS":31,"WIN":274,"UNKNOWN":3079})
    assert not updated
    secured=set()
    for g in geometry:
        if status(g["children"],after)=="LOSS":secured.update(g["coverage"])
    remaining=sorted(set(range(121))-{60,27}-secured)
    assert len(secured)==117 and remaining==[100,108]
    cached=EXP/"output/merged-exact-s5.cache"
    with cached.open("w") as f:
        f.write("# n11 exact S5 cache, after 20 independent cold raw solver LOSS results\n")
        for k,val in sorted(after.items()):
            f.write(f"s5verdict,{k[0]},{k[1]},5,{val},0\n")
    result={
        "source_main_sha":"1c2c010762e2e781ce04ed7d00e8592fc114776e",
        "solver_source_commit":"f33693cdd8be54738cedea8fc141553209c9a669",
        "solver_binary_sha256":"2878dc74ab1228c1bba6b13140dcd8f65f457f9813ae98d801a1709c77497ee5",
        "solver_flags":"--n=11 --memo=22 --only=5 --exact-order=count --exact-replay-budget=15000000; cold per input row",
        "geometry_sha256":digest(GEOM),
        "independent_board_sha256":digest(ROOT/"research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "old_cache_sha256":digest(BASE),
        "input_sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in sorted(RAW.glob("target-*.csv"))},
        "raw_sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in sorted(RAW.glob("probe-*.csv"))},
        "root_s4_key":list(TARGET),
        "root_s4_coverage":target["coverage"],
        "new_s5_count":20,
        "new_s5_verdicts":{"LOSS":20,"WIN":0,"UNKNOWN":0},
        "new_s5_total_nodes":sum(x["nodes"] for x in decisive.values()),
        "new_s5_total_reported_seconds":sum(x["reported_seconds"] for x in decisive.values()),
        "new_s5_shared_other_live_parent":sum(x["shared_live_parents"]==2 for x in decisive.values()),
        "new_s5_positions":{f"{k[0]}:{k[1]}":{**v,"parents":[list(z) for z in incidences[k]]} for k,v in sorted(decisive.items())},
        "s5_cache_before":len(before),"s5_cache_after":len(after),
        "s5_cache_after_WIN":sum(v==1 for v in after.values()),
        "s5_cache_after_LOSS":sum(v==2 for v in after.values()),
        "s5_cache_conflicts":0,
        "s5_cache_sha256":digest(cached),
        "target_s4_before":t_before,"target_s4_after":t_after,
        "s4_before":dict(old_class),"s4_after":dict(new_class),"s4_status_changes":updated,
        "secured_third_moves":len(secured),
        "unresolved_third_moves":remaining,
        "additional_loss_classes_min":1,
        "proof_evidence_boundary":"solver-trusted direct exact S5; geometry and boundary independently validated, terminal-only proofs not produced",
    }
    (EXP/"output/audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("new_s5_count","new_s5_verdicts","new_s5_total_nodes","s5_cache_after","s5_cache_after_LOSS","target_s4_after","s4_after","unresolved_third_moves")},ensure_ascii=False,indent=2))
    return result

if __name__=="__main__":
    audit()
