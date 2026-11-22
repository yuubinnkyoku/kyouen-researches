#!/usr/bin/env python3
"""Part BD minimal independent checker (verification host B, 2026-11-22).

Self-written verification of the published Part BC batch-14residual
(class 23101) 10-LOSS canonical adoption, WITHOUT using any Part BC
script: raw/3-way re-derivation, cache set-arithmetic, graph-based
class recomputation, holder subtraction, worklist/closure/per-root
diffs. Verdict consumption: NONE (read-only). 11x11 stays UNKNOWN;
nodes are bookkeeping, never verdicts.
"""
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

import os
ROOT = Path(os.environ.get("KR_BD_ROOT", str(Path(__file__).resolve().parents[4])))
# the published Part BC adoption experiment (byte-verify target, on main)
PUB = ROOT / "research/experiments/n11-centralreply-class23101-residualloss10-adoption-reaudit-20261122"
AV = ROOT / "research/experiments/n11-centralreply-class10661-loss52-adoption-reaudit-20261122"
AW = ROOT / "research/experiments/n11-centralreply-closure-class23101-batch14-residual-20261122"

GR = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
U8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"

results = {}
fails = []

def ck(name, cond, detail=""):
    results[name] = {"ok": bool(cond), "detail": str(detail)[:400]}
    if not cond:
        fails.append(name)
    print(("OK  " if cond else "FAIL") + f" {name} {detail if not cond else ''}")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read_cache(path):
    """my own reader: returns (comments, verdict map {(lo,hi): (v,nodes)}, order list)"""
    comments, vm = [], {}
    order = []
    with Path(path).open(encoding="utf-8-sig", newline="") as fh:
        for i, row in enumerate(csv.reader(fh), 1):
            if not row or row[0].lstrip().startswith("#"):
                if row:
                    comments.append(",".join(row))
                continue
            assert len(row) == 6 and row[0] == "s5verdict", f"bad row {i}: {row}"
            lo, hi, st, v, nd = map(int, row[1:])
            assert st == 5 and v in (1, 2)
            k = (lo, hi)
            assert k not in vm, f"dup key {k} in {path}"
            vm[k] = (v, nd)
            order.append(k)
    return comments, vm, order

# ---------------- A. increment 3-way re-derivation ----------------
def parse_raw(p):
    rows = []
    for line in Path(p).read_text().splitlines():
        if line.startswith("replay,"):
            f = line.split(",")
            rows.append(dict(order=int(f[1]), stones=int(f[2]), legal=int(f[3]),
                             is_or=int(f[4]), budget=int(f[5]), result=int(f[6]),
                             nodes=int(f[7]), wall=float(f[8]), lo=int(f[9]), hi=int(f[10])))
    return rows

bk = json.loads((AW / "input/batch-keys.json").read_text())["keys"]
bkmap = {k["key_id"]: k for k in bk}
ra = json.loads((AW / "output/row-audit.json").read_text())
ramap = {r["key_id"]: r for r in ra["rows"]}
stat = {}
for line in (AW / "output/status.log").read_text().splitlines():
    parts = line.split()
    for kw in ("PASS", "WAVE-END", "VAL-GATE"):
        pass
    if len(parts) >= 4 and parts[1:2] == ["PASS"]:
        b, r, n = parts[2].split(",")
        stat[parts[0].split()[-1] if False else parts[0]] = (int(b), int(r), int(n))
# simpler re-parse for IDs like q043 PASS 15000000,2,2573254 (timestamp prefix)
stat = {}
for line in (AW / "output/status.log").read_text().splitlines():
    f = line.split()
    if len(f) == 4 and f[2] == "PASS" and "," in f[3]:
        b, r, n = f[3].split(",")
        stat[f[1]] = (int(b), int(r), int(n))

adopted = {}
for kid in [f"q{i:03d}" for i in range(43, 53)]:
    p1, p2 = parse_raw(AW / f"output/raw/{kid}.p1.out"), parse_raw(AW / f"output/raw/{kid}.p2.out")
    assert len(p1) == 1 and len(p2) == 1, kid
    a, b = p1[0], p2[0]
    for fld in ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi", "order"):
        assert a[fld] == b[fld], (kid, fld, a[fld], b[fld])
    k = bkmap[kid]
    assert (a["lo"], a["hi"]) == (int(k["lo"]), int(k["hi"])), kid
    assert a["legal"] == int(k["legal"]), kid
    assert "replay_done rows=1" in (AW / f"output/raw/{kid}.p1.out").read_text(), kid
    r = ramap[kid]
    assert (r["result"], r["nodes"], r["budget"]) == (a["result"], a["nodes"], a["budget"]), kid
    assert (r["lo"], r["hi"]) == (a["lo"], a["hi"]) and r["legal"] == a["legal"], kid
    assert kid in stat and stat[kid] == (a["budget"], a["result"], a["nodes"]), kid
    adopted[(a["lo"], a["hi"])] = dict(kid=kid, s5=int(k["s5_index"]), result=a["result"],
                                       nodes=a["nodes"], legal=a["legal"], budget=a["budget"])
ck("A.raw_3way_all10", len(adopted) == 10 and all(v["result"] == 2 and v["budget"] == 15000000 for v in adopted.values()),
   f"{len(adopted)} keys")
ck("A.nowin_noexhaust", ra["wins"] == [] and ra["exhausted_result0"] == [] and ra["mismatch"] == 0)
tot = sum(v["nodes"] for v in adopted.values())
ck("A.nodes_total_per_pass", tot == 23252550 == ra["total_nodes_per_pass"], tot)

# my own re-render of the increment data lines
lines = ["s5verdict,%d,%d,5,2,%d" % (lo, hi, adopted[(lo, hi)]["nodes"]) for (lo, hi) in sorted(adopted)]
pub_incr = (PUB / "output/increment-batch14residual-loss10-20261122.cache").read_text().splitlines()
pub_data = [l for l in pub_incr if not l.startswith("#")]
ck("A.increment_rerender", lines == pub_data, f"mine={lines[:2]} pub={pub_data[:2]}")

man = json.loads((PUB / "output/increments-manifest.json").read_text())
ck("A.manifest_fields", man["row_counts"]["losses"] == 10 and man["row_counts"]["wins"] == 0
   and man["row_counts"]["resolved_rows"] == 10 and man["win_scenario_exists"] is False
   and man["base_cache_rows"] == 6172 and man["base_cache_absent_hits"] == 0
   and man["quarantine_hits"] == 0 and man["full_packet_eq_loss_only"] is True
   and sorted(man["loss_ids"]) == [f"q{i:03d}" for i in range(43, 53)])

# q042 exclusion + batch17 s5-disjoint (my own)
b17 = json.loads((ROOT / "research/experiments/n11-centralreply-closure-class10661-batch17-20261122/input/batch-keys.json").read_text())["keys"]
b17s5 = {int(k["s5_index"]) for k in b17}
ck("A.q042_excluded", (1152921505747697664, 1032) not in adopted and 745184 not in {v["s5"] for v in adopted.values()})
ck("A.b17_s5_disjoint", not (b17s5 & {v["s5"] for v in adopted.values()}))
q = json.loads((ROOT / "results/n11-s5-evidence-quarantine.json").read_text())
qkeys = set()
for e in q["entries"]:
    qkeys.add((int(e["key"][0]), int(e["key"][1])))
ck("A.quarantine_disjoint", not (qkeys & set(adopted)), f"{len(qkeys)} quarantined keys")

# ---------------- B. cache set-arithmetic ----------------
bc, BV, BO = read_cache(AV / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-20261122.cache")
sc, SV, SO = read_cache(PUB / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-20261122.cache")
ck("B.base_rows", len(BV) == 6172 and sha(AV / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-20261122.cache").startswith("a5540811"))
ck("B.scen_rows", len(SV) == 6182)
ck("B.scen_sorted_unique", SO == sorted(SO))
ck("B.base_subset", all(BV[k][0] == SV[k][0] for k in BV))
new_keys = set(SV) - set(BV)
ck("B.new_keys_eq_incr", new_keys == set(adopted) and all(SV[k][0] == 2 for k in new_keys),
   f"new={len(new_keys)}")
w = sum(1 for k in SV if SV[k][0] == 1); l = sum(1 for k in SV if SV[k][0] == 2)
bw = sum(1 for k in BV if BV[k][0] == 1); bl = sum(1 for k in BV if BV[k][0] == 2)
ck("B.verdict_counts", (w, l, bw, bl) == (158, 6024, 158, 6014), f"W{w} L{l} bW{bw} bL{bl}")
ck("B.scen_nodes_follow_base_or_incr",
   all(SV[k] == (BV[k] if k in BV else (2, adopted[k]["nodes"])) for k in SV))
ck("B.comments_carried", sc == bc, f"{len(sc)} comment lines")

# ---------------- C. graph-based recomputation ----------------
with gzip.open(GR, "rt", encoding="utf-8") as fh:
    g = json.load(fh)
s5m = g["s5_masks"]; s4m = g["s4_masks"]; s4s = g["s4_status"]; s4c = g["s4_cost"]
m2i = {(lo, hi): i for i, (lo, hi) in enumerate(s5m)}
u8 = json.loads(U8.read_text())
rec = {int(k): int(v) for k, v in u8["resolved_s5_verdicts"].items()}

def world(vm):
    iv = {}
    for (lo, hi), (v, _) in vm.items():
        i = m2i.get((lo, hi))
        if i is not None:
            assert i not in iv or iv[i] == v, f"conflict at {i}"
            iv[i] = v
    for i, v in rec.items():
        assert iv.get(i, v) == v, f"receipt conflict {i}"
        iv[i] = v
    return iv

ivB, ivS = world(BV), world(SV)
def unknowns(iv, c):
    return [x for x in c if x not in iv]

adidx = sorted(m2i[(lo, hi)] for (lo, hi) in adopted)
cA = s4c[23101]
uB, uS = unknowns(ivB, cA), unknowns(ivS, cA)
ck("C.class23101_base_unknown11", len(uB) == 11 and set(uB) == {745184} | set(adidx), f"{sorted(uB)}")
ck("C.class23101_base_unknown", sorted(uB) == [745184] + adidx, f"{sorted(uB)}")
ck("C.class23101_scen_unknown_eq_leftover", uS == [745184], f"{uS}")
ck("C.class23101_mask", s4m[23101] == [1152921504892059648, 16] and s5m[745184] == [1152921505747697664, 1032])
ck("C.q042_index_nonconsumed", 745184 not in ivS and m2i[(1152921505747697664, 1032)] == 745184)

# holder classes: classes containing an adopted index in s4_cost
holders = {}
for ci in range(len(s4m)):
    own = [x for x in s4c[ci] if x in set(adidx)]
    if own:
        holders[ci] = own
pub_h = json.loads((PUB / "output/decomp-deltas-batch14residual-adoption.json").read_text())["holder_classes"]
ck("C.holders_match", sorted(int(k) for k in pub_h) == sorted(holders),
   f"mine={sorted(holders)} pub={sorted(int(k) for k in pub_h)}")
ok = True
for k, v in pub_h.items():
    ci = int(k)
    ok &= (holders[ci] and len(holders[ci]) == v["own_membership_in_increment"]
           and v["scenario_unknown_now"] == len(unknowns(ivS, s4c[ci]))
           and v["base_unknown_now"] == len(unknowns(ivB, s4c[ci])))
ck("C.holder_values_match", ok)

# full-world class counts (my classification): for each class compute
# unknown_now and win_hit under the scenario
cnt = {"excluded": 0, "unknown": 0, "zero_unknown_candidates": 0, "win_hit": 0}
my_unknown_now = {}
for ci in range(len(s4m)):
    base = s4s[ci]
    if base == -1:
        cnt["excluded"] += 1
        continue
    u = unknowns(ivS, s4c[ci])
    my_unknown_now[ci] = len(u)
    winhit = any(ivS.get(x) == 1 for x in s4c[ci])
    if winhit:
        cnt["win_hit"] += 1
    if u:
        cnt["unknown"] += 1
    else:
        cnt["zero_unknown_candidates"] += 1
ss = json.loads((PUB / "reaudit/output/refresh-summary.json").read_text())["class_status_counts"]
bv = json.loads((PUB / "reaudit/output/refresh-summary.json").read_text())["board_verification"]
# my classification: excluded(base) / win_hit -> excluded_now / u==0 & !winhit -> free_now candidate / else unknown
my_free = my_zero_nohit = 0
cnt2 = {"excluded": 0, "excluded_now": 0, "free_now": 0, "unknown": 0}
for ci in range(len(s4m)):
    base = s4s[ci]
    if base == -1:
        cnt2["excluded"] += 1
        continue
    winhit = any(ivS.get(x) == 1 for x in s4c[ci])
    if winhit:
        cnt2["excluded_now"] += 1
    elif my_unknown_now.get(ci, 0) == 0:
        cnt2["free_now"] += 1
    else:
        cnt2["unknown"] += 1
ck("C.world_counts_vs_published", cnt2 == ss and bv["board_verified_free"] == ss["free_now"]
   and bv["free_candidates"] == ss["free_now"], f"mine={cnt2} pub={ss}")

# update8 replication
fu = json.loads((PUB / "reaudit/output/refresh-summary.json").read_text())["frozen_update8_refresh"]
res_s = fu["resolved_among_baseline_requirement"]
req = u8["required_new_s5"]
known_req = [i for i in req if i in ivS]
known_req_b = [i for i in req if i in ivB]
ck("C.update8_resolved80_inv", len(res_s) == 80 and sorted(res_s) == sorted(known_req)
   and sorted(known_req_b) == sorted(known_req) and fu["remaining_now"] == 31779
   and len(req) == 31859 and fu["groups_free_now"] == 127,
   f"scen_known={len(known_req)} base_known={len(known_req_b)}")

# closure table: my own check that 23101 rank1 + churn by direct csv diff
def rd(p):
    with open(p) as fh:
        return list(csv.DictReader(fh))
clB = rd(AV / "reaudit/output/closure-classes.csv")
clS = rd(PUB / "reaudit/output/closure-classes.csv")
setB = {r["class_index"] for r in clB}
setS = {r["class_index"] for r in clS}
ck("C.closure_sets_808", len(clB) == 808 and len(clS) == 808 and len(setB) == 808 and len(setS) == 808)
left = setB - setS
entered = setS - setB
ck("C.closure_churn", left == {"22149"} and entered == {"23965"} and len(setB & setS) == 807,
   f"left={left} entered={entered}")
ck("C.closure_rank1_is23101", clS[0]["class_index"] == "23101" and int(clS[0]["unknown_now"]) == 1)
# my unknown_now equals the published per-class unknown_now column for every class
mism = [r["class_index"] for r in clS if my_unknown_now.get(int(r["class_index"])) != int(r["unknown_now"])]
ck("C.closure_unknown_now_col_matches_mine", not mism, f"{mism[:5]} ({len(mism)})")

# per-root coverage diff (my own row-level comparison)
prB = (AV / "reaudit/output/per-root-coverage.csv").read_text().splitlines()
prS = (PUB / "reaudit/output/per-root-coverage.csv").read_text().splitlines()
ck("F.prc_same_rowcount", len(prB) == len(prS) == 21, f"{len(prB)} {len(prS)}")
diffcols = {}
for a, b in zip(prB, prS):
    fa, fb = a.split(","), b.split(",")
    if fa != fb:
        for i, (x, y) in enumerate(zip(fa, fb)):
            if x != y:
                diffcols.setdefault(i, 0)
                diffcols[i] += 1
hdr = prS[0].split(",")
ck("F.prc_changes_only_greedy_col",
   set(diffcols) == {5} and all(fa[:5] == fb[:5] for fa, fb in zip(prB, prS) ),
   f"diffcols={ {hdr[i]: c for i, c in diffcols.items()} }")

# probe worklists: recount + diff classification
SCEN_LOCAL = PUB
wlB, wlS = None, None
have_wl = (AV / "reaudit/output/probe-worklist.csv").is_file() and (SCEN_LOCAL / "reaudit/output/probe-worklist.csv").is_file()
if have_wl:
    assert sha(AV / "reaudit/output/probe-worklist.csv").startswith("667dc815")
    assert sha(SCEN_LOCAL / "reaudit/output/probe-worklist.csv").startswith("fe71be60")
    wlB = rd(AV / "reaudit/output/probe-worklist.csv")
    wlS = rd(SCEN_LOCAL / "reaudit/output/probe-worklist.csv")
ck("E.worklist_counts", (not have_wl) or (len(wlB) == 64888 and len(wlS) == 64872),
   "skipped (worklists are unpublished regenerated artifacts)" if not have_wl else f"{len(wlB)} -> {len(wlS)}")
kB = {(r["s5_index"], r["lo"], r["hi"]) for r in wlB}
kS = {(r["s5_index"], r["lo"], r["hi"]) for r in wlS}
onlyB, onlyS = kB - kS, kS - kB
# NOTE: the worklist is a (key, serving_class) row multiset, not a plain key
# set; the plain key-set symmetric difference (onlyB/onlyS) is bookkeeping churn
# and NOT the -16; the row-level multiset diff below is the correct invariant.
if have_wl:
  # worklist is a row-multiset over (key, serving_class) pairs (best-option bookkeeping)
  from collections import Counter
  psB = Counter((r["s5_index"], r["lo"], r["hi"], r["serving_class"]) for r in wlB)
  psS = Counter((r["s5_index"], r["lo"], r["hi"], r["serving_class"]) for r in wlS)
  rem = psB - psS
  add = psS - psB
  ck("E.worklist_removed_added_copies", sum(rem.values()) - sum(add.values()) == 16,
     f"removed={sum(rem.values())} added={sum(add.values())}")
  rem_serving = Counter()
  for k, n in rem.items():
      rem_serving[k[3]] += n
  add_serving = Counter()
  for k, n in add.items():
      add_serving[k[3]] += n
  ck("E.worklist_churn_matches_closure_churn",
     rem_serving.get("22149") == 108 and add_serving.get("23965") >= 100
     and rem_serving.get("23101") == 10,
     f"rem={rem_serving.most_common(8)} add={add_serving.most_common(8)}")
  adopted_str_keys = {("%d" % lo, "%d" % hi) for (lo, hi) in adopted}
  multS = Counter((r["lo"], r["hi"]) for r in wlS)
  multB = Counter((r["lo"], r["hi"]) for r in wlB)
  ck("E.adopted_keys_gone_from_scen_worklist",
     all(multS[k] == 0 for k in adopted_str_keys) and all(multB[k] >= 1 for k in adopted_str_keys),
     f"base copies={sum(multB[k] for k in adopted_str_keys)} scen copies={sum(multS[k] for k in adopted_str_keys)}")
  # every removed (key,serving_class) pair outside 22149/23101 is served by a class
  # whose s4_cost holds an adopted index (my own membership recompute)
  adidx_str = {str(x) for x in adidx}
  odd = [k for k in rem if k[3] not in ("22149", "23101")]
  odd_ok = True
  for k in odd:
      ci = int(k[3])
      odd_ok &= bool(set(map(str, s4c[ci])) & adidx_str)
  ck("E.odd_removed_pairs_all_holder_served", odd_ok and len(odd) == 5,
     f"{[(k[0], k[3]) for k in odd]}")

sha_incr = sha(PUB / "output/increment-batch14residual-loss10-20261122.cache")
ck("PUBSHA.increment", sha_incr.startswith("c3f201a6"))
ck("PUBSHA.manifest", sha(PUB / "output/increments-manifest.json").startswith("f7287b7b"))
ck("PUBSHA.scen_cache", sha(PUB / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-20261122.cache").startswith("0b594f7e"))
ck("PUBSHA.summary", sha(PUB / "reaudit/output/refresh-summary.json").startswith("5f3a09c6"))
ck("PUBSHA.closure", sha(PUB / "reaudit/output/closure-classes.csv").startswith("52ec3d4b"))
ck("PUBSHA.prc", sha(PUB / "reaudit/output/per-root-coverage.csv").startswith("1f54065a"))
ck("PUBSHA.delta", sha(PUB / "output/decomp-deltas-batch14residual-adoption.json").startswith("62de8c16"))

print()
print("TOTAL checks:", len(results), "FAILS:", len(fails), fails)
json.dump({"results": results, "fin": fails}, (Path(__file__).resolve().parents[1] / "output/bd-minimal-check-result.json").open("w"), indent=1, sort_keys=True)
sys.exit(1 if fails else 0)
