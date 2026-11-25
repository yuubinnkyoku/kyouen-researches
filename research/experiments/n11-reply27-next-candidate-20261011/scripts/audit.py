#!/usr/bin/env python3
"""Fail-closed audit of three raw S5 LOSS probes and full 11x11 S4 frontier."""
from __future__ import annotations
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EX=ROOT/"research/experiments/n11-reply27-next-candidate-20261011"
RAW=EX/"output/raw"
BASE=ROOT/"research/experiments/n11-s6-universal-closure-20261011/output/merged-exact-s5.cache"
GEOM=ROOT/"research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
TARGET=(1297036692683752448,0)
sys.path.insert(0,str(ROOT/"research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0,str(ROOT/"research/experiments/n11-frontier-selection-20261005/scripts"))
from independent import Board
from s5_evidence_policy import quarantined_cache_keys

def mask(key):return key[0]|(key[1]<<64)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def csvrows(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return [row for row in csv.reader(f) if row and not row[0].startswith("#")]

def read_cache(path):
    vals={}
    forbidden=quarantined_cache_keys()
    for row in csvrows(path):
        assert len(row)==6 and row[0]=="s5verdict"
        k=(int(row[1]),int(row[2])); v=int(row[4])
        assert k not in forbidden and int(row[3])==5 and v in (1,2)
        assert k not in vals or vals[k]==v
        vals[k]=v
    return vals

def status(children,cache):
    values=[cache.get(tuple(z),0) for z in children]
    if 1 in values:return "WIN"
    if all(v==2 for v in values):return "LOSS"
    return "UNKNOWN"

def main():
    board=Board(11)
    inrows=csvrows(RAW/"targets.csv")
    assert len(inrows)==3
    expected={}
    for r in inrows:
        assert len(r)==11 and r[0]=="target" and int(r[2])==5 and int(r[7])==0
        k=(int(r[3]),int(r[4])); count=int(r[5])
        assert k not in expected and mask(k).bit_count()==5
        assert board.canonical(mask(k))==mask(k)
        assert board.legal(mask(k)).bit_count()==count
        expected[k]=count

    records={}
    for name,budget in [("probe-2m.csv",2_000_000),("probe-15m.csv",15_000_000)]:
        allrows=[r for r in csvrows(RAW/name) if r[0]=="replay"]
        assert len(allrows)==3 and len({(int(r[9]),int(r[10])) for r in allrows})==3
        for r in allrows:
            assert len(r)==11
            seq,stones,legal,is_or,limit,verdict,nodes,elapsed,lo,hi=map(int,r[1:])
            k=(lo,hi)
            assert k in expected and stones==5 and is_or==0 and legal==expected[k]
            assert limit==budget and 0<nodes<=limit
            if budget==2_000_000:
                assert verdict==0 and nodes==budget
            else:
                assert verdict==2 and nodes<budget
            records.setdefault(k,{})[name]={"verdict":verdict,"nodes":nodes,"legal":legal}
    assert set(records)==set(expected) and all(len(v)==2 for v in records.values())

    with gzip.open(GEOM,"rt") as f:
        geom=json.load(f)
    assert len(geom)==3384
    parents={tuple(g["key"]):g for g in geom}
    target=parents[TARGET]
    complete={tuple(k) for k in target["children"]}
    assert len(complete)==106 and set(expected)<=complete
    child_parents={k:[] for k in expected}
    for g in geom:
        matched=set(map(tuple,g["children"]))&set(expected)
        for key in matched:child_parents[key].append(g["key"])
    assert all(len(z) >= 1 for z in child_parents.values())

    old=read_cache(BASE)
    assert len(old)==5752 and sum(v==1 for v in old.values())==159
    for k in expected:assert k not in old
    new=old.copy()
    for k in expected:new[k]=2
    assert len(new)==len(old)+3
    previous_counts={s:sum(status(g["children"],old)==s for g in geom) for s in ("LOSS","WIN","UNKNOWN")}
    current_counts={s:sum(status(g["children"],new)==s for g in geom) for s in ("LOSS","WIN","UNKNOWN")}
    affected=[{"key":g["key"],"from":status(g["children"],old),"to":status(g["children"],new)} for g in geom
              if status(g["children"],old)!=status(g["children"],new)]
    assert previous_counts=={"LOSS":31,"WIN":274,"UNKNOWN":3079}
    assert status(target["children"],new)=="UNKNOWN"
    target_counts={"LOSS":sum(new.get(k)==2 for k in complete),
                  "WIN":sum(new.get(k)==1 for k in complete),
                  "UNKNOWN":sum(k not in new for k in complete)}
    assert target_counts=={"LOSS":10,"WIN":0,"UNKNOWN":96}

    secured=set()
    for g in geom:
        if status(g["children"],new)=="LOSS":secured.update(g["coverage"])
    remaining=set(range(121))-{60,27}-secured
    assert len(secured)==117 and remaining=={100,108}

    outcache=EX/"output/merged-exact-s5.cache"
    with outcache.open("w",encoding="utf-8",newline="") as f:
        f.write("# n11 raw direct S5 exact; audited 2026-10-11; solver-trusted leaves\n")
        for k,v in sorted(new.items()):
            f.write(f"s5verdict,{k[0]},{k[1]},5,{v},0\n")

    report={
        "source_main_at_start":"f33693cdd8be54738cedea8fc141553209c9a669",
        "source_cpp_sha256":sha(ROOT/"cpp/solvers/kyouen_dfpn_root.cpp"),
        "geometry_sha256":sha(GEOM),"independent_board_sha256":sha(ROOT/"research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "baseline_cache_path":BASE.relative_to(ROOT).as_posix(),"baseline_cache_sha256":sha(BASE),
        "raw_artifacts":[{"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p)} for p in sorted(RAW.iterdir())],
        "s4_target":list(TARGET),"s4_coverage":target["coverage"],"s4_s5_full_children":len(complete),
        "new_s5_exact_loss":[{"key":list(k),"parents":child_parents[k],
                               "legal":expected[k],"cold_2m":records[k]["probe-2m.csv"],
                               "cold_15m":records[k]["probe-15m.csv"]} for k in expected],
        "probe_total_nodes":sum(r["probe-2m.csv"]["nodes"]+r["probe-15m.csv"]["nodes"] for r in records.values()),
        "decisive_15m_nodes":sum(r["probe-15m.csv"]["nodes"] for r in records.values()),
        "baseline_s5":len(old),"merged_s5":len(new),
        "merged_s5_counts":{"WIN":sum(v==1 for v in new.values()),"LOSS":sum(v==2 for v in new.values()),"verdict_conflicts":0},
        "s4_class_counts_before":previous_counts,"s4_class_counts_after":current_counts,
        "s4_promotions":affected,"target_s5_counts":target_counts,
        "secured_third_moves":len(secured),"remaining_third_moves":sorted(remaining),
        "minimal_additional_loss_classes":1,"rational_lp_dual":1,
        "merged_cache_path":outcache.relative_to(ROOT).as_posix(),
        "merged_cache_sha256":sha(outcache),
        "evidence_limit":"Direct raw positive budget exact S5 verdicts with independent canonical/legal/parent verification; no terminal-only minimax certificate",
    }
    (EX/"output/audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"new_s5":3,"cache":report["merged_s5_counts"],"target":target_counts,
                      "s4":current_counts,"s4_promotions":affected,"remaining_third_moves":sorted(remaining),
                      "probe_nodes":report["probe_total_nodes"]},indent=2))
    return report

if __name__=="__main__":
    main()
