#!/usr/bin/env python3
"""Independent geometry audit of the 90-S6 universal WIN boundary.

Raw S6 verdicts are trusted solver leaves, NOT independent terminal minimax.
The parent S5 WIN and S4 WIN are independently verified AND/OR propagation.
"""
from __future__ import annotations

import argparse
import collections
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EX = ROOT / "research/experiments/n11-s6-universal-closure-20261011"
RAW = EX / "output/raw"
GEOM = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
BASE = ROOT / "research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-9-rebased-main.cache"
SRC = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
S5_HARD = (1188950301626859520, 603979776)
S5_LOSSES = ((1152921504606851072, 805306370), (1188950301626859520, 671088640))
S5_FILES = ["s5-cold-2m.csv", "s5-shared-2m.csv", "s5-cold-15m.csv", "s5-shared-15m.csv"]
S6_BASE = ["s6-lowest3", "s6-stratified15"] + [f"s6-batch{i}" for i in range(1, 5)]
S6_MORE = ["s6-escalate-a", "s6-escalate-b"]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from independent import Board, aggregate
from s5_evidence_policy import quarantined_cache_keys

def asmask(k):
    return k[0] | (k[1] << 64)

def askey(m):
    return (m & ((1<<64)-1), m >> 64)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def check_input(path, exact_budget, n, expected):
    with path.open(encoding="utf-8-sig",newline="") as stream:
        rows = [r for r in csv.reader(stream) if r and not r[0].startswith("#")]
    assert len(rows)==expected, (path, len(rows), expected)
    for row in rows:
        assert len(row)==11 and row[0] in ("target","s5target"), (path,row)
        assert int(row[2])==n and int(row[7])==(n%2==0)
    return { (int(r[3]),int(r[4])):(int(r[5]),r) for r in rows }

def read_rows(path, stones, budget):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows=[r for r in csv.reader(stream) if r and r[0]=="replay"]
    assert len(rows)>0,(path,"no replay evidence")
    out=[]
    for r in rows:
        assert len(r)==11
        seq,n,legal,isor,lim,v,nodes,wall,lo,hi=map(int,r[1:])
        assert n==stones and isor==(stones%2==0)
        assert lim==budget and v in (0,1,2) and 0<=nodes<=lim
        if v==0:
            assert nodes==lim
        out.append({"key":(lo,hi),"legal":legal,"budget":lim,"verdict":v,
                    "nodes":nodes,"elapsed_reported_seconds":wall,"sequence":seq})
    assert len({d["key"] for d in out})==len(out),(path,"duplicate canonical replay")
    return out

def read_cache(path):
    vals={}
    quarantined=quarantined_cache_keys()
    with path.open(encoding="utf-8-sig",newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].startswith("#"): continue
            assert len(row)==6 and row[0]=="s5verdict"
            k=(int(row[1]),int(row[2]));v=int(row[4])
            assert int(row[3])==5 and v in (1,2) and int(row[5])>=0
            if k in quarantined:
                raise AssertionError(f"quarantined exact cache entry: {k}")
            assert k not in vals or vals[k]==v,(path,k,"verdict conflict")
            vals[k]=v
    return vals

def run(basepath):
    b=Board(11)
    assert b.canonical(asmask(S5_HARD))==asmask(S5_HARD)
    s6_keys={askey(m) for m in b.children(asmask(S5_HARD))}
    assert len(s6_keys)==90 and b.legal(asmask(S5_HARD)).bit_count()==90
    all_proof={}
    rawfiles=[f for f in RAW.iterdir() if f.is_file()]
    assert len(rawfiles)==21, len(rawfiles)
    raw_manifest=[{"path":f.relative_to(ROOT).as_posix(),"sha256":sha(f),"bytes":f.stat().st_size} for f in sorted(rawfiles)]
    sources={}

    # Source CSVs from an exact cold process and shared-TT experiment.
    shared_cost={}
    s5input=check_input(RAW/"s5-input.csv",0,5,2)
    assert set(s5input)==set(S5_LOSSES)
    for name in S5_FILES:
        budget=2_000_000 if "2m" in name else 15_000_000
        rows=read_rows(RAW/name,5,budget)
        assert {r["key"] for r in rows}==set(S5_LOSSES)
        for r in rows:
            assert r["legal"]==s5input[r["key"]][0]
            assert b.canonical(asmask(r["key"]))==asmask(r["key"])
            assert len(b.points(asmask(r["key"])))==5
            assert b.legal(asmask(r["key"])).bit_count()==r["legal"]
            assert r["verdict"]==(0 if budget==2_000_000 else 2)
        shared_cost[name]=sum(r["nodes"] for r in rows)

    # S6 children are a COMPLETE canonical legal set, not sampled targets.
    observations=collections.defaultdict(list)
    base_rows=[]
    s6_total_nodes=0
    for name in S6_BASE+S6_MORE:
        inpath=RAW/f"{name}.input.csv"
        outpath=RAW/f"{name}.out.csv"
        exp=3 if name=="s6-lowest3" else 15 if name=="s6-stratified15" else (18 if name.startswith("s6-batch") else (2 if name=="s6-escalate-a" else 3))
        budget=2_000_000 if name=="s6-lowest3" else 15_000_000 if name in S6_MORE else 1_000_000
        inputs=check_input(inpath,budget,6,exp)
        rows=read_rows(outpath,6,budget)
        assert len(rows)==exp and set(inputs)=={r["key"] for r in rows},(name,"input/output mismatch")
        for r in rows:
            assert r["key"] in s6_keys,(name,r["key"],"illegal/noncanonical child")
            assert r["legal"]==inputs[r["key"]][0]
            assert b.canonical(asmask(r["key"]))==asmask(r["key"])
            assert len(b.points(asmask(r["key"])))==6
            assert b.legal(asmask(r["key"])).bit_count()==r["legal"]
            observations[r["key"]].append({**r,"source":outpath.relative_to(ROOT).as_posix()})
        s6_total_nodes+=sum(r["nodes"] for r in rows)
        if name in S6_BASE: base_rows.extend(rows)
        sources[name]={"budget":budget,"rows":len(rows),
                       "win":sum(r["verdict"]==1 for r in rows),
                       "unknown":sum(r["verdict"]==0 for r in rows),
                       "nodes":sum(r["nodes"] for r in rows)}
    assert len(base_rows)==90 and {r["key"] for r in base_rows}==s6_keys
    unknown={r["key"] for r in base_rows if r["verdict"]==0}
    assert len(unknown)==5 and sum(r["verdict"]==1 for r in base_rows)==85
    assert len(observations)==90
    assert all(len(observations[k])==1+(k in unknown) for k in s6_keys)
    for k,logs in observations.items():
        exact=[r for r in logs if r["verdict"] in (1,2)]
        assert len(exact)==1 and exact[0]["verdict"]==1,(k,logs)
        assert all(r["verdict"] in (0,1) for r in logs)
        all_proof[k]=exact[0]

    # At odd S5, all S6 WIN -> S5 WIN (AND universal).
    assert aggregate(5,[r["verdict"] for r in all_proof.values()])==1
    assert b.legal(asmask(S5_HARD)).bit_count()==90

    cache=read_cache(basepath)
    initial={"WIN":sum(v==1 for v in cache.values()),"LOSS":sum(v==2 for v in cache.values())}
    delta={S5_HARD:1, **dict.fromkeys(S5_LOSSES,2)}
    new=0
    for k,v in delta.items():
        if k in cache:
            assert cache[k]==v,(k,"cache/derived verdict conflict")
        else:
            new+=1
        cache[k]=v

    full=[(tuple(g["key"]),set(map(tuple,g["children"])),g["coverage"]) for g in json.loads(gzip.open(GEOM,"rt").read())]
    assert len(full)==3384
    def status(ch,vals):
        v=[vals.get(k,0) for k in ch]
        if 1 in v: return "WIN"
        if all(x==2 for x in v):return "LOSS"
        return "UNKNOWN"
    # The value of a S4 class is OR at fixed-original-first-player perspective.
    before=read_cache(basepath)
    oldstats=collections.Counter(status(ch,before) for _,ch,_ in full)
    newstats=collections.Counter(status(ch,cache) for _,ch,_ in full)
    changed=[]
    for parent,ch,coverage in full:
        prev=status(ch,before)
        now=status(ch,cache)
        if prev!=now:
            changed.append({"s4_key":list(parent),"coverage":coverage,"old":prev,"new":now,
                            "s5_win_witness":list(S5_HARD) if S5_HARD in ch else None,
                            "full_boundary_size":len(ch)})
        if S5_HARD in ch:
            assert status(ch,cache)=="WIN"
            assert asmask(S5_HARD) in b.children(asmask(parent))
    assert len(changed)>=1 and all(z["old"]=="UNKNOWN" and z["new"]=="WIN" for z in changed)
    secured=set()
    for p,ch,coverage in full:
        if status(ch,cache)=="LOSS":secured.update(coverage)
    remain=set(range(121))-{60,27}-secured
    assert len(secured)==117 and remain=={100,108}
    candidate=[(p,ch,coverage) for p,ch,coverage in full if 100 in coverage or 108 in coverage]
    assert len(candidate)==115
    assert all(100 in cov and 108 in cov for _,_,cov in candidate)
    unknown_target=sum(status(ch,cache)=="UNKNOWN" for _,ch,_ in candidate)
    assert unknown_target>=1
    # All remaining vertices jointly covered by every relevant class, so
    # minimum additional LOSS class count is 1 and LP dual y100=1,y108=0.
    mincover=1
    dual={"100":"1","108":"0"}

    EX.joinpath("output").mkdir(exist_ok=True)
    merged=EX/"output/merged-exact-s5.cache"
    with merged.open("w",encoding="utf-8",newline="") as f:
        f.write("# n11 exact S5 with solver-trusted S6 universal closure; see independent geometry audit\n")
        for k,v in sorted(cache.items()):
            f.write(f"s5verdict,{k[0]},{k[1]},5,{v},0\n")
    proofcsv=EX/"output/s6-win-complete.csv"
    with proofcsv.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n")
        w.writerow(["s6_lo","s6_hi","legal","exact_verdict","nodes","source"])
        for k,r in sorted(all_proof.items()):
            w.writerow([*k,r["legal"],"WIN",r["nodes"],r["source"]])
    compact={
        "s5":list(S5_HARD),"s5_value":"WIN","s5_legal":90,
        "s6_complete_child_count":90,"s6_accurate_verdicts":{"WIN":90,"LOSS":0,"UNKNOWN":0},
        "s6_direct_exact_only":True,"s6_raw_runs":{"initial_exact":85,"initial_unknown":5,"after_escalation_win":5},
        "root_proof_polarity":"S5 AND WIN iff every legal canonical S6 child is WIN",
        "S4_polarity":"S4 OR WIN iff at least one legal canonical S5 child is WIN",
        "S6_terminal_only_independently_checked":False,
        "S6_verdict_trust":"raw positive-budget unmodified solver, each legal canonical child; exact leaves are solver-trusted",
    }
    (EX/"output/s5-universal-witness.json").write_text(json.dumps(compact,indent=2)+"\n")
    report={
        "schema":"n11-s6-universal-closure-v1",
        "source_commit_at_start":"581e72c277d05149b847d997c47a15bfc77a36c7",
        "source_cpp_sha256":sha(SRC),"source_residual_hpp_sha256":sha(ROOT/"cpp/solvers/kyouen_residual_micro.hpp"),
        "solver_binary_sha256":"98aadf580119ea3fb89be77fa161defded6feb87f5cb2f30b0503e35a4163c01",
        "solver_options":"--n=11 --memo=22 --exact-order=count, fresh per S6 row, 1M/2M -> 15M",
        "independent_geometry_sha256":sha(ROOT/"research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "geometry_sha256":sha(GEOM),"baseline_cache_path":str(basepath.relative_to(ROOT)),
        "baseline_cache_sha256":sha(basepath),"baseline_cache_rows":len(before),
        "baseline_verdict_counts":initial,
        "raw_sources":raw_manifest,"s6_trials":sources,
        "s6_trial_total_nodes":s6_total_nodes,
        "s6_all_children_complete":True,
        "s6_first_pass_distinct":90,"s6_first_pass_WIN":85,"s6_first_pass_UNKNOWN":5,
        "s6_15m_escalated_WIN":5,"s6_new_loss":0,
        "s6_final_WIN":90,
        "S5_derived_WIN":list(S5_HARD),
        "s5_cold_2m_nodes":shared_cost["s5-cold-2m.csv"],
        "s5_cold_15m_nodes":shared_cost["s5-cold-15m.csv"],
        "s5_shared_2m_nodes":shared_cost["s5-shared-2m.csv"],
        "s5_shared_15m_nodes":shared_cost["s5-shared-15m.csv"],
        "s5_shared_tt_node_saving":shared_cost["s5-cold-15m.csv"]-shared_cost["s5-shared-15m.csv"],
        "s5_LOSS_new":[list(k) for k in S5_LOSSES],
        "raw_direct_replay_S5_LOSS":True,
        "new_s5_keys_vs_baseline":new,
        "total_new_exact_S5":len(delta),
        "merged_cache_path":merged.relative_to(ROOT).as_posix(),"merged_cache_sha256":sha(merged),"merged_cache_rows":len(cache),
        "merged_cache_verdicts":{"WIN":sum(v==1 for v in cache.values()),"LOSS":sum(v==2 for v in cache.values()),"conflict":0},
        "s4_before":dict(oldstats),"s4_after":dict(newstats),"s4_promoted_to_WIN":changed,
        "third_moves":{"secured":len(secured),"total":119,"remaining":sorted(remain),
                       "minimum_additional_class_count":mincover,"rational_dual":dual},
        "scope":"Solver-trusted S6 WIN leaves; all 90 S6 legal children independently regenerated; S5/S4 upper propagation independently verified",
        "does_not_prove":"{60,27} LOSS or 11x11 empty result; cache-only leaves not yet terminal-only independently reproved",
    }
    (EX/"output/audit.json").write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print(json.dumps({
        "s6_win":90,"s6_total_nodes":s6_total_nodes,"s5_derived_WIN":list(S5_HARD),
        "class_promotions":changed,"s4_counts":dict(newstats),"cache":report["merged_cache_verdicts"],
        "secured":len(secured),"remaining":sorted(remain),"saved_nodes_shared_TT":report["s5_shared_tt_node_saving"]
    },ensure_ascii=False,indent=2))
    return report

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline-cache",type=Path,default=BASE)
    arg=ap.parse_args()
    run(arg.baseline_cache.resolve())
