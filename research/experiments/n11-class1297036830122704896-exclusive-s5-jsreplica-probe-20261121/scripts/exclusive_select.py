#!/usr/bin/env python3
"""n11 candidate-class 1297036830122704896:0 exclusive single-live-parent key selector.

Adapted from research/experiments/n11-s5-class-closure-priority-20261121/
scripts/class_closure_priority.py (ccp lane) with the same gating logic,
pins, and fail-closed style (selection-only). Publishes the authoritative
machine list for the third-cost-class exclusive probe lane (declaration
research/log/2026-11-21-n11-class1297036830122704896-exclusive-s5-jsreplica-probe-single-owner.md).

Dual layout: uses pub_paths.resolve (kit layout or published repo layout).
No verdicts are read or written here.
"""
from __future__ import annotations
import csv, gzip, hashlib, json, sys
from collections import defaultdict
from pathlib import Path
import pub_paths

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
CANDIDATE_LEDGER_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
PROFILE_SHA = "6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

MY_CLASS = (1297036830122704896, 0)
FOCUS_CLASS = (1188950301626859520, 536870912)
CERT_CLASS = (1297036692683752448, 0)

FOCUS_LANE_35 = sorted(set([
 "10376293541461622816:68719476737","10376293545756590112:68719476736",
 "10412322338481635328:536870912","1152921504606851072:536870922",
 "1152921504606851072:536870978","1152921504606851072:536936450",
 "1152921504606851072:537001986","1152921504606851072:553648130",
 "1152921504606851072:570425346","1152921504606851072:603979778",
 "1152921504741064705:68719476738","1152921504741068800:68719476738",
 "1188950301626859520:536870913","1188950301626859520:536870976",
 "1188950301626859520:537001984","1188950301626859520:537133056",
 "1188950301626859520:603979776","1188950301626859520:805306368",
 "1188950301626863616:536870912","1188950301626867712:536870912",
 "1188950301626892288:536870912","1188950310216794112:536870912",
 "1188950301643636736:536870912","1188950302700601344:536870912",
 "1188950305921826816:536870912","1188950576504766464:536870912",
 "1188951401138487296:536870912","1188959097719881728:536870912",
 "1189020670371037184:536870912","1189091039115214848:536870912",
 "1193453901254230016:536870912","1197957500881600512:536870912",
 "1261007895664787456:536870912","1765411053930283008:536870912",
 "5800636320054247424:536870912"]))
assert len(FOCUS_LANE_35) == 35, len(FOCUS_LANE_35)

SBD_EXTRA = {(1152921504606851072, 805306370), (1188950301626859520, 671088640)}
REQUIRED = {100, 108}

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fail(m):
    print(f"GATE FAILED: {m}", file=sys.stderr); raise SystemExit(1)

def main():
    P = pub_paths.resolve(__file__)
    geo_p, cache_p = P["geometry"], P["cache"]
    supply_p, ledger_p = P["supply"], P["ledger"]
    profile_p, quar_p = P["profile"], P["quar"]
    for p, s in [(geo_p,GEOMETRY_SHA),(cache_p,CACHE_SHA),(supply_p,SUPPLY_SHA),
                 (ledger_p,CANDIDATE_LEDGER_SHA),(profile_p,PROFILE_SHA),(quar_p,QUARANTINE_SHA)]:
        if digest(p) != s: fail(f"{p} sha mismatch")
    geo = json.loads(gzip.open(geo_p, "rt", encoding="utf-8").read())
    if len(geo) != 3384: fail("geometry class count")
    cache = {}
    for row in csv.reader(cache_p.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"): continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1,2): fail(f"cache row {row}")
        k=(int(row[1]),int(row[2])); v=int(row[4])
        if k in cache and cache[k] != v: fail(f"conflict {k}")
        cache[k]=v
    if len(cache) != 5756: fail(f"cache rows {len(cache)}")
    def stage(vals):
        if 1 in vals: return "WIN"
        if all(v==2 for v in vals): return "LOSS"
        return "UNKNOWN"
    counts=defaultdict(int); candidates=[]; my_entry=None
    for g in geo:
        ch={tuple(z) for z in g["children"]}
        vals=[cache.get(z,0) for z in ch]
        st=stage(vals); counts[st]+=1
        e=(tuple(g["key"]),g["coverage"],ch,st)
        if REQUIRED.intersection(g["coverage"]): candidates.append(e)
        if tuple(g["key"]) == MY_CLASS: my_entry=e
    if my_entry is None: fail("my class missing")
    if len(candidates) != 115: fail("candidate count")
    active=[c for c in candidates if c[3]=="UNKNOWN"]
    if len(active) != 62 or counts["WIN"] != 272 or counts["LOSS"] != 31: fail("ledger invariants")
    if sum(1 for c in candidates if c[3]=="WIN") != 53: fail("candidate WIN count")
    if my_entry[3] != "UNKNOWN": fail("my class stage")
    if not REQUIRED.issubset(my_entry[1]): fail("coverage")
    live_par=defaultdict(set)
    for k,cov,ch,st in active:
        for child in ch:
            if child not in cache: live_par[child].add(k)
    supply={}
    for row in csv.DictReader(supply_p.open(newline="")):
        lo,hi=row["key"].split(":"); supply[(int(lo),int(hi))]=row
    if set(supply) != set(live_par) or len(supply) != 4562: fail("supply mismatch")
    deg=defaultdict(int)
    for c in live_par: deg[len(live_par[c])]+=1
    if deg != {1:2688,2:1874}: fail("degree distribution")
    k,cov,ch,st = my_entry
    unk=sorted(c for c in ch if c not in cache)
    exclusive=[c for c in unk if len(live_par[c])==1 and next(iter(live_par[c]))==MY_CLASS]
    shared=[c for c in unk if len(live_par[c])>1]
    if len(exclusive)!=39: fail("exclusive count")
    if len(unk)!=100 or len(shared)!=61: fail("closure split")
    if len(ch)!=107: fail("children count")
    ledger={r["key"]:r for r in csv.DictReader(ledger_p.open(newline=""))}
    ks=f"{MY_CLASS[0]}:{MY_CLASS[1]}"
    lr=ledger.get(ks)
    if lr is None: fail("ledger row")
    if int(lr["s5_unknown"])!=len(unk) or int(lr["s5_unknown_shared_with_other_live_classes"])!=len(shared): fail("ledger cross-check")
    quar=json.loads(quar_p.read_text(encoding="utf-8"))
    qq=set()
    def collect(o):
        if isinstance(o,dict):
            for kk,vv in o.items():
                if kk in ("key","keys","quarantined") and isinstance(vv,(str,list)):
                    qq.update([vv] if isinstance(vv,str) else vv)
                else: collect(vv)
        elif isinstance(o,list):
            for v in o: collect(v)
    collect(quar)
    order=sorted(exclusive,key=lambda c:(int(supply[c]["truncated_cost_proxy_nodes"]),c))
    out_rows=[]
    for i,c in enumerate(order):
        lo,hi=c; kc=f"{lo}:{hi}"
        if c in cache: fail(f"{kc} in cache")
        if kc in qq: fail(f"{kc} quarantined")
        if kc in FOCUS_LANE_35: fail(f"{kc} overlaps focus claim")
        if c in SBD_EXTRA: fail(f"{kc} overlaps sbd extras")
        out_rows.append({"order":i+1,"key":kc,"legal":int(supply[c]["legal"]),"live_parents":len(live_par[c]),
          "truncated_cost_proxy_nodes":int(supply[c]["truncated_cost_proxy_nodes"]),
          "bin_win_count":int(supply[c]["bin_win_count"]),"bin_sample_size":int(supply[c]["bin_sample_size"])})
    cert_unk=None
    for ek,ecov,ech,est in active:
        if ek==CERT_CLASS: cert_unk=[c for c in ech if c not in cache and len(live_par[c])==1]
    if cert_unk is None or len(cert_unk)!=38: fail("cert exclusive")
    mine=set(f"{c[0]}:{c[1]}" for c in exclusive)
    if mine & set(f"{c[0]}:{c[1]}" for c in cert_unk): fail("cert overlap")
    if mine & set(FOCUS_LANE_35): fail("focus overlap")
    res={"input_pins":{"geometry_sha256":GEOMETRY_SHA,"cache_sha256":CACHE_SHA,"supply_sha256":SUPPLY_SHA,
        "candidate_ledger_sha256":CANDIDATE_LEDGER_SHA,"profile_sha256":PROFILE_SHA,"quarantine_sha256":QUARANTINE_SHA},
      "class_key":ks,"coverage":sorted(cov),"s5_children":len(ch),"s5_unknown":len(unk),
      "unknown_exclusive":len(exclusive),"unknown_shared":len(shared),
      "proxy_exclusive_sum":sum(int(supply[c]["truncated_cost_proxy_nodes"]) for c in exclusive),
      "proxy_total":sum(int(supply[c]["truncated_cost_proxy_nodes"]) for c in unk),
      "gates":"3384 classes; 115 candidates; 62 UNKNOWN/53 WIN/0 LOSS; supply 4562 (1:2688 2:1874); my class 107 children, 100 unknown (39 exclusive / 61 shared); ledger cross-check OK; quarantine/content/focus/sbd disjointness OK",
      "exclusive_probe_order":out_rows,
      "status_guard":"selection only; no verdict read or written; the 11x11 empty board, the two-stone root {60,27}, and third moves 100/108 remain UNKNOWN"}
    out = Path(sys.argv[1]) if len(sys.argv)>1 else P["exp"]/"output"/"exclusive-selection.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(res,indent=1,ensure_ascii=False)+"\n",encoding="utf-8")
    print("ALL GATES PASS")
    print(f"class {ks} coverage={sorted(cov)} unknown={len(unk)} exclusive={len(exclusive)} shared={len(shared)}")
    print(f"proxy_exclusive_sum={res['proxy_exclusive_sum']} proxy_total={res['proxy_total']}")

if __name__ == "__main__":
    main()
