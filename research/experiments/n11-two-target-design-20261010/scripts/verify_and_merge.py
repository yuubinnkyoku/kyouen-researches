#!/usr/bin/env python3
"""Collect two tiny shared-S5 probes and independently check their geometry.

A terminal-only minimax proof is NOT produced; solver outcomes remain trusted.
Run --collect exactly once from the original scratch environment, then audit
with no flags from any clean checkout.
"""
from __future__ import annotations
import argparse
import collections
import csv
import gzip
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-two-target-design-20261010"
SCRATCH = ROOT / ".local/n11-two-target/probes"
RAW = EXP / "output/raw"
BASE = ROOT / "research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-3.cache"
GEO = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
SOURCE = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
OUTCACHE = EXP / "output/merged-exact-s5.cache"
OUTAUDIT = EXP / "output/probe-audit.json"

sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from independent import Board, aggregate
from s5_evidence_policy import quarantined_cache_keys

TARGETS = [
  ((1152921504606851072,536870946), 98, 3651923),
  ((1188950301626860544,536870912), 99, 5040200),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_cache(p):
    d={}
    for r in csv.reader(p.open(encoding="utf-8-sig",newline="")):
        if not r or r[0].startswith("#"):
            continue
        assert len(r)==6 and r[0]=="s5verdict" and int(r[3])==5 and int(r[4]) in (1,2)
        k=tuple(map(int,r[1:3]));v=int(r[4])
        assert k not in d or d[k]==v, (k,"verdict conflict")
        assert k not in quarantined_cache_keys(), (k,"quarantined")
        d[k]=v
    return d

def read_run(path, key, legal, budget, expected):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows=[r for r in csv.reader(stream) if r and r[0]=="replay"]
    assert len(rows)==1 and len(rows[0])==11,(path,rows)
    r=rows[0]
    assert int(r[2])==5 and int(r[3])==legal and int(r[4])==0
    assert int(r[5])==budget and int(r[6])==expected and tuple(map(int,r[9:11]))==key
    assert int(r[7])>=0
    return int(r[7])

def process(collect):
    RAW.mkdir(parents=True,exist_ok=True)
    if collect:
        for key,_,_ in TARGETS:
            label=f"s5-{key[0]}-{key[1]}"
            for phase in ("at2m","first-15m" if key==TARGETS[0][0] else "second-15m"):
                prefix=SCRATCH / phase / label
                for ext in (".input.csv",".out.csv",".log"):
                    src=Path(str(prefix)+ext)
                    assert src.is_file(), src
                    dst=RAW/f"{phase}-{label}{ext}"
                    assert not dst.exists() or src.read_bytes()==dst.read_bytes()
                    shutil.copyfile(src,dst)
    cache=read_cache(BASE)
    assert len(cache)==5741 and collections.Counter(cache.values())=={1:158,2:5583}
    geometry=json.loads(gzip.open(GEO,"rt",encoding="utf-8").read())
    assert len(geometry)==3384
    board=Board(11)
    root=(1<<60)|(1<<27)
    assert board.legal(root).bit_count()==119
    assert all(board.legal(root)&(1<<m) for m in (100,108))
    refl=lambda n:n//11*11+10-n%11
    assert refl(60)==60 and refl(27)==27 and refl(100)==108 and refl(108)==100
    # Stronger, direct independent geometric test: corresponding S3 boards
    # have exactly reflected legal third-to-fourth moves.
    s3a=board.legal(root|(1<<100))
    s3b=board.legal(root|(1<<108))
    assert {refl(p) for p in board.points(s3a)}==set(board.points(s3b))

    raw_manifest=[]
    new={}
    summary=[]
    for key,legal,nodes in TARGETS:
        label=f"s5-{key[0]}-{key[1]}"
        phases=("at2m","first-15m" if key==TARGETS[0][0] else "second-15m")
        st={}
        for phase in phases:
            stem=RAW/f"{phase}-{label}"
            inp=Path(str(stem)+".input.csv")
            raw=Path(str(stem)+".out.csv")
            log=Path(str(stem)+".log")
            assert all(p.exists() for p in (inp,raw,log))
            input_rows=[r for r in csv.reader(inp.open(encoding="utf-8")) if r]
            assert len(input_rows)==1 and len(input_rows[0])==11
            assert input_rows[0][0]=="target" and tuple(map(int,input_rows[0][3:5]))==key
            budget=2_000_000 if phase=="at2m" else 15_000_000
            n=read_run(raw,key,legal,budget,0 if budget==2_000_000 else 2)
            assert n==(2_000_000 if budget==2_000_000 else nodes)
            st[phase]={"nodes":n,"budget":budget,"verdict":"UNKNOWN" if budget==2_000_000 else "LOSS"}
            for p in (inp,raw,log):
                raw_manifest.append({"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p)})
        mask=key[0]|(key[1]<<64)
        assert board.canonical(mask)==mask and len(board.points(mask))==5
        assert board.legal(mask).bit_count()==legal
        parent_keys=[]
        for g in geometry:
            if list(key) in g["children"]:
                parent=tuple(g["key"])
                pmask=parent[0]|(parent[1]<<64)
                assert len(board.points(pmask))==4 and board.canonical(pmask)==pmask
                assert mask in board.children(pmask)
                parent_keys.append(parent)
        assert len(parent_keys)>=2, (key,parent_keys)
        assert key not in cache
        new[key]=2
        summary.append({"s5_key":list(key),"legal":legal,"raw_verdict":"LOSS",
                        "nodes_at_2m":2_000_000,"nodes_at_15m":nodes,
                        "related_s4_keys":[list(k) for k in parent_keys],
                        "independent_geometry":"safe canonical child; complete S4 legal incidence",
                        "independent_terminal_minimax":"not established",
                        "stages":st})
    cache.update(new)
    assert len(cache)==5743 and collections.Counter(cache.values())=={1:158,2:5585}
    with OUTCACHE.open("w",encoding="utf-8",newline="") as f:
        f.write("# S5 solver-trusted exact; source manifest in probe-audit.json\n")
        for k,v in sorted(cache.items()):
            f.write(f"s5verdict,{k[0]},{k[1]},5,{v},{dict((x,n) for x,_,n in TARGETS).get(k,0)}\n")
    # Recompute all boundary statuses from fixed geometry with new exact rows.
    counts=collections.Counter()
    covered=set()
    affected=[]
    candidate=collections.Counter()
    for g in geometry:
        c=[cache.get(tuple(k),0) for k in g["children"]]
        status="WIN" if 1 in c else "LOSS" if all(v==2 for v in c) else "UNKNOWN"
        counts[status]+=1
        if status=="LOSS":
            covered.update(g["coverage"])
        if any(k in g["children"] for k in [list(z) for z in new]):
            affected.append({"key":g["key"],"coverage":g["coverage"],"status":status,
                             "S5_LOSS":c.count(2),"S5_WIN":c.count(1),"S5_UNKNOWN":c.count(0)})
        if 100 in g["coverage"] or 108 in g["coverage"]:
            assert 100 in g["coverage"] and 108 in g["coverage"]
            candidate[status]+=1
    assert counts=={"WIN":272,"LOSS":31,"UNKNOWN":3081}
    assert len(covered)==117 and candidate=={"WIN":53,"UNKNOWN":62}
    assert sorted(set(range(121))-{60,27}-covered)==[100,108]
    report={
      "title":"Two shared-S5 targeted probes; strict solver/geometry trust separation",
      "source_cpp_sha256":sha(SOURCE),
      "solver_binary_sha256_from_probe_host":"98aadf580119ea3fb89be77fa161defded6feb87f5cb2f30b0503e35a4163c01",
      "solver_compile":"g++ 14.2.0 -O3 -std=c++20 -DNDEBUG on Intel Core i5-9400T (Debian)",
      "source_residual_hpp_sha256":sha(ROOT/"cpp/solvers/kyouen_residual_micro.hpp"),
      "independent_geometry_python_sha256":sha(ROOT/"research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
      "baseline_cache_sha256":sha(BASE),"baseline_cache_rows":5741,
      "geometry_sha256":sha(GEO),
      "merged_cache_sha256":sha(OUTCACHE),"merged_cache_rows":5743,
      "merged_s5_verdicts":{"WIN":158,"LOSS":5585,"conflict":0},
      "s4_class_counts":dict(counts),
      "remaining_third_moves":[100,108],"secured":117,
      "minimum_additional_loss_classes":1,
      "rational_dual":1,
      "new_raw_exact":2,"new_loss_s4_classes":0,"new_win_s4_classes":0,
      "nodes_exact_replays":sum(n for _,_,n in TARGETS),
      "nodes_initial_2m":4_000_000,
      "nodes_all_replays":sum(n for _,_,n in TARGETS)+4_000_000,
      "candidate_classes":dict(candidate),
      "changed_boundaries":affected,
      "probes":summary,
      "raw_artifacts":sorted(raw_manifest,key=lambda r:r["path"]),
      "exact_evidence_type":"raw solver-trusted; S4/S5 geometry independently checked; terminal-only minimax NOT complete",
      "cache_quarantine":"validated against current S5 evidence policy; UNKNOWN not merged",
    }
    OUTAUDIT.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"merged":len(cache),"new":2,"exact_nodes":report["nodes_exact_replays"],
                      "total_nodes":report["nodes_all_replays"],"affected":affected,
                      "outcache_sha":sha(OUTCACHE)},ensure_ascii=False,indent=2))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--collect",action="store_true")
    a=p.parse_args()
    process(a.collect)
