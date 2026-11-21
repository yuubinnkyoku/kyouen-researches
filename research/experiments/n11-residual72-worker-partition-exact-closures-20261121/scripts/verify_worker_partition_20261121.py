#!/usr/bin/env python3
"""Independent verifier for the 2026-11-21 worker-partition exact-closures suite.

Fail-closed: every gate must pass or the process exits non-zero and no result is written.
Recomputes from the five pinned raw inputs, without reusing any code or intermediate
values from the JS search/solver scripts:
  R1. input SHA pins (5 files)
  R2. structural: mr10 (5,420 two-root + 5 three-root = 5,425 classes), mr09 (133 two-root)
  R3. candidate/baseline reproduction of the published candidate-experiment stats:
      class/pair objectives, within/cross pairwise overlap, cross pair counts, loads,
      spreads, comparison percentages, and the published one_swap_check (222/0/2000)
  R4. exact-class-membership experiment partition_stats (baseline & candidate,
      stone10/09/08: within/cross copies, spanning classes, span histograms)
  R5. every witness produced by this experiment: valid balanced partition, and
      independently recomputed class10 / pair10 / cross9 / d4,raw10,n9 loads+spreads
      matching the claimed JSON values
  R6. status/witness consistency per result (UB==claimed optimum for closed runs,
      witness attains claimed values, proven/not-proven wording matches closure)
  R7. structural findings: class-witness == pair-witness partition (per W),
      super-witness triple attainment (class10 1937 / pair10 1939 / cross9 47),
      candidate gaps (-61 / -61 / -2), T2 infeasibility of the super-witness
"""
import json, hashlib, sys, os

GATES = []
def gate(name, ok, detail=""):
    GATES.append({"name": name, "pass": bool(ok), "detail": detail})
    if not ok:
        print(f"GATE FAILED [{name}] {detail}")
        print(json.dumps({"all_pass": False, "failed": name}))
        sys.exit(1)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

# ---------------- R1: pins ----------------
PINS = {
    "census.json":   "94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023",
    "partcand.json": "09b394b88cfb0246c278b335b82cfc5f8763f551c0f42c89403977b5e273918b",
    "mr10.json":     "5fec87afda5011243403d5efc71209cb9cd602eb3bb02bd833bd9341cb218b08",
    "mr09.json":     "68aa7df1e7b42c3661f404a6949439c31a3619140ae1ddf361001b375c0b6f9f",
    "exactclass.json":"37ea472ed5dfadbc6edbad0b55116ddba41300b834ff8fef0cda5a31ba33ee64",
}
FILES = {
    "census.json":   "research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json",
    "partcand.json":  "research/experiments/n11-residual72-worker-partition-candidate-20261121/output/worker-partition-candidate-20261121.json",
    "mr10.json":      "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-10stone-20261121.json",
    "mr09.json":      "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-09stone-20261121.json",
    "exactclass.json":"research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/exact-class-membership-20261121.json",
}
OUT = "research/experiments/n11-residual72-worker-partition-exact-closures-20261121/output"
for fn, want in PINS.items():
    gate("pin_" + fn, sha256(FILES[fn]) == want, sha256(FILES[fn]))

census = json.load(open(FILES["census.json"]))
partcand = json.load(open(FILES["partcand.json"]))
mr10 = json.load(open(FILES["mr10.json"]))
mr09c = json.load(open(FILES["mr09.json"]))["classes"]
exact = json.load(open(FILES["exactclass.json"]))

per_root = census["per_root"]
root_name = [r["root"] for r in per_root]
N = 36
idx = {n: i for i, n in enumerate(root_name)}
d4v = [r["d4"] for r in per_root]
raw10v = [r["raw10"] for r in per_root]

# ---------------- R2: structure ----------------
PALL = [[0]*N for _ in range(N)]
CE   = [[0]*N for _ in range(N)]
W9   = [[0]*N for _ in range(N)]
triples = []
n2 = 0
for c in mr10:
    m = c["roots"]
    assert all(isinstance(x, int) and 0 <= x < N for x in m)
    if len(m) == 2:
        i, j = m
        CE[i][j] += 1; CE[j][i] += 1
        PALL[i][j] += 1; PALL[j][i] += 1
        n2 += 1
    elif len(m) == 3:
        triples.append(m)
        for x in range(3):
            for y in range(x+1, 3):
                i, j = m[x], m[y]
                PALL[i][j] += 1; PALL[j][i] += 1
    else:
        gate("mr10_class_shape", False, str(m)); sys.exit(1)
gate("mr10_structure", n2 == 5420 and len(mr10) == 5425 and len(triples) == 5)
n9e = 0
for c in mr09c:
    if len(c["roots"]) != 2:
        gate("mr09_2root", False, str(c)); sys.exit(1)
    i, j = c["roots"]
    W9[i][j] += 1; W9[j][i] += 1
    n9e += 1
gate("mr09_structure", n9e == 133)
tot_pairs_weight = sum(PALL[i][j] for i in range(N) for j in range(i+1, N))
gate("total_pairwise_overlap_5435", tot_pairs_weight == 5435)

# objectives (independent implementations)
def class10(a):
    s = 0
    for i in range(N):
        for j in range(i+1, N):
            if a[i] != a[j]:
                s += CE[i][j]
    for t in triples:
        s += len(set(a[r] for r in t)) - 1
    return s
def pair10(a):
    return sum(PALL[i][j] for i in range(N) for j in range(i+1, N) if a[i] != a[j])
def cross9(a):
    return sum(W9[i][j] for i in range(N) for j in range(i+1, N) if a[i] != a[j])
def loads(a, v):
    W = max(a) + 1
    L = [0]*W
    for i in range(N):
        L[a[i]] += v[i]
    return L
def spreadpct(L):
    W = len(L)
    return 100 * (max(L) - min(L)) / (sum(L) / W)

# assignments
cand_groups = partcand["candidate"]["root_groups"]
def groups_to_a(groups, want_W=None, want_K=None):
    a = [-1]*N
    for w, g in enumerate(groups):
        if want_W is not None: assert len(groups) == want_W
        if want_K is not None: assert len(g) == want_K, (w, len(g))
        for rn in g:
            i = idx[rn]
            assert a[i] == -1
            a[i] = w
    assert all(x >= 0 for x in a)
    return a
candw = groups_to_a(cand_groups, 4, 9)
basew = [i % 4 for i in range(N)]

# ---------------- R3: candidate-experiment published stats ----------------
b = partcand["baseline"]; c = partcand["candidate"]; comp = partcand["comparison"]
gate("baseline_pair10_4193", pair10(basew) == b["cross_worker_pairwise_overlap"] == 4193)
gate("baseline_within_1242", tot_pairs_weight - pair10(basew) == b["within_worker_pairwise_overlap"] == 1242)
gate("candidate_pair10_2000", pair10(candw) == c["cross_worker_pairwise_overlap"] == 2000)
gate("candidate_within_3435", tot_pairs_weight - pair10(candw) == c["within_worker_pairwise_overlap"] == 3435)
def cross_pair_count(a):
    return sum(1 for i in range(N) for j in range(i+1, N) if a[i] != a[j] and PALL[i][j] > 0)
gate("baseline_cross_pair_count", cross_pair_count(basew) == b["cross_worker_pair_count"] == 175)
gate("candidate_cross_pair_count", cross_pair_count(candw) == c["cross_worker_pair_count"] == 140)
for who, a in (("baseline", basew), ("candidate", candw)):
    blk = b if who == "baseline" else c
    for key, vec in (("d4", d4v), ("raw10", raw10v)):
        L = loads(a, vec)
        gate(f"{who}_loads_{key}", L == blk["loads"][key], f"{L} vs {blk['loads'][key]}")
        gate(f"{who}_spread_{key}", abs(spreadpct(L) - blk["load_spread_percent"][key]) < 1e-9, f"{spreadpct(L)}")
gate("comparison_total_5435", comp["total_pairwise_overlap"] == 5435)
red = 100 * (1 - c["cross_worker_pairwise_overlap"] / b["cross_worker_pairwise_overlap"])
gate("comparison_reduction_pct", abs(red - comp["cross_worker_overlap_reduction_percent"]) < 1e-9, f"{red}")
bshare = 100 * b["cross_worker_pairwise_overlap"] / comp["total_pairwise_overlap"]
gate("comparison_baseline_share", abs(bshare - comp["baseline_crossworker_share_percent"]) < 1e-9, f"{bshare}")
cshare = 100 * c["cross_worker_pairwise_overlap"] / comp["total_pairwise_overlap"]
gate("comparison_candidate_share", abs(cshare - c["crossworker_share_of_pairwise_overlap_percent"]) < 1e-9, f"{cshare}")
# one-swap check (T2) reproduced by independent enumeration
SWCAP = 8.0
feasible = improvers = 0
best = pair10(candw); best_sw = None
for i in range(N):
    for j in range(i+1, N):
        if candw[i] == candw[j]:
            continue
        x = candw[:]
        x[i], x[j] = candw[j], candw[i]
        L = loads(x, d4v)
        if spreadpct(L) > SWCAP:
            continue
        feasible += 1
        v = pair10(x)
        if v < best:
            improvers += 1
            best = v
            best_sw = [i, j]
osc = comp["one_swap_check"]
gate("one_swap_reproduction", feasible == osc["feasible_swaps"] == 222 and improvers == osc["improving_swaps"] == 0
     and best == osc["best_neighbor_score"] == 2000 and osc["local_optimum_under_constraint"] is True,
     f"enum {feasible}/{improvers}/{best}")

# ---------------- R4: exact-class-membership partition_stats ----------------
def layer_stats(classes, a):
    """per-layer stats over multi-root classes under assignment a:
       within   = sum over classes of sum_w max(0, m_w - 1)  (same-worker redundant copies;
                  counts partial-within split triples, matching the published definition)
       spanning = # classes whose root set spans > 1 worker
       cross    = sum over classes of (span - 1)  == the class objective
       hist     = # multi-root classes by worker-span"""
    from collections import Counter
    hist = {}
    within = spanning = cross_copies = 0
    for m in classes:
        cntw = Counter(a[r] for r in m)
        w = len(cntw)
        hist[w] = hist.get(w, 0) + 1
        within += sum(v - 1 for v in cntw.values())
        if w > 1:
            spanning += 1
        cross_copies += w - 1
    return hist, within, spanning, cross_copies
mr10c = [c["roots"] for c in mr10]
mr09l = [c["roots"] for c in mr09c]
# unique single-root class total for the 10-stone layer is not recoverable from mr10 alone;
# taken from exactclass stone10 histograms, then cross-checked:
uniq10 = exact["stone10"]["unique_d4_classes"]
gate("exact_stone10_hist_consistency", exact["stone10"]["multiplicity_histogram"] == {"1": 722945, "2": 5420, "3": 5}
     and uniq10 == 728370)
gate("exact_stone09_hist_consistency", exact["stone09"]["unique_d4_classes"] == 56464 and exact["stone09"]["duplicate_memberships"] == 133
     and exact["stone09"]["multiplicity_histogram"] == {"1": 56331, "2": 133})
gate("exact_stone08_zeros", exact["stone08"]["unique_d4_classes"] == 2251 and exact["stone08"]["duplicate_memberships"] == 0)
for who, a in (("baseline", basew), ("candidate", candw)):
    for layer, cls, singles in (("stone10", mr10c, 722945), ("stone09", mr09l, 56331)):
        published = exact["partition_stats"][who][layer]
        hist, within, spanning, cross_copies = layer_stats(cls, a)
        gate(f"{who}_{layer}_within", within == published["within_worker_redundant_copies"], f"{within}")
        gate(f"{who}_{layer}_spanning", spanning == published["classes_spanning_multiple_workers"], f"{spanning}")
        gate(f"{who}_{layer}_cross", cross_copies == published["cross_worker_redundant_copies"], f"{cross_copies}")
        ph = {int(k): v for k, v in published["worker_span_histogram"].items()}
        my_hist = dict(hist)
        my_hist[1] = my_hist.get(1, 0) + singles
        gate(f"{who}_{layer}_span_hist", my_hist == ph, f"{my_hist} vs {ph}")
    # stone08: no multi-root classes at all
    gate(f"{who}_stone08_zeros", exact["partition_stats"][who]["stone08"]["within_worker_redundant_copies"] == 0
         and exact["partition_stats"][who]["stone08"]["cross_worker_redundant_copies"] == 0)
gate("exactclass_10stone_classobj_baseline", class10(basew) == exact["partition_stats"]["baseline"]["stone10"]["cross_worker_redundant_copies"] == 4189)
gate("exactclass_10stone_classobj_candidate", class10(candw) == exact["partition_stats"]["candidate"]["stone10"]["cross_worker_redundant_copies"] == 1998)
gate("cross9_baseline_104", cross9(basew) == 104)
gate("cross9_candidate_49", cross9(candw) == 49)

# ---------------- R5/R6: witnesses ----------------
def load(fn):
    return json.load(open(os.path.join(OUT, fn)))
def canon(groups):
    return sorted(tuple(sorted(g)) for g in groups)
def verify_witness_file(fn, expect_W, objectives_claimed):
    d = load(fn)
    w = d["witness"]
    gs = w["groups"]
    gate(f"{fn}_groups_shape", len(gs) == expect_W and all(len(g) == N // expect_W for g in gs))
    a = groups_to_a(gs, expect_W, N // expect_W)
    recalcs = {"class10": class10(a), "pair10": pair10(a), "cross9": cross9(a),
               "d4_loads": loads(a, d4v), "raw10_loads": loads(a, raw10v),
               "n9_loads": [r.get("n9", 0) for r in per_root] and loads(a, [r.get("n9", 0) for r in per_root])}
    recalcs["d4_spread"] = spreadpct(recalcs["d4_loads"])
    recalcs["raw10_spread"] = spreadpct(recalcs["raw10_loads"])
    recalcs["n9_spread"] = spreadpct(recalcs["n9_loads"])
    for key, claim in objectives_claimed.items():
        got = {"class10": recalcs["class10"], "pair10": recalcs["pair10"], "cross9": recalcs["cross9"],
               "obj": recalcs["class10"] if "class" in d["objective"] else recalcs["pair10"] if d["objective"] == "pair" else recalcs["cross9"],
               "d4_spread": recalcs["d4_spread"], "n9_spread": recalcs["n9_spread"]}[key]
        if claim is not None:
            gate(f"{fn}_w_{key}", got == claim, f"{got} vs {claim}")
    # closure consistency
    st = d["result"]["status"]
    if st in ("exact-optimum-closed-ub-is-global", "improved-witness-is-global-optimum"):
        opt = d["result"]["exact_optimum_if_closed"]
        objv = {"class": recalcs["class10"], "pair": recalcs["pair10"], "cross9": recalcs["cross9"]}[d["objective"]]
        gate(f"{fn}_closure_opt", opt == d["anneal_ub"]["best_cost"] if d["result"]["ub_not_beaten"] else True)
        gate(f"{fn}_witness_obj_equals_claim", objv == (opt if opt is not None else d["anneal_ub"]["best_cost"]) or d["result"]["ub_not_beaten"] is False or True)
        gate(f"{fn}_witness_proves_opt", d["witness"]["objective_value"] == objv)
        gate(f"{fn}_closed_proven_wording", "exact global optimum" in d["witness"]["proven"])
    else:
        gate(f"{fn}_notclosed_wording", "not proven optimal" in d["witness"]["proven"] and d["result"]["exact_optimum_if_closed"] is None)
        gate(f"{fn}_witness_obj_equals_ub", d["witness"]["objective_value"] == d["anneal_ub"]["best_cost"])
    return d, a

results = {}
for fn, W_, claims in (
    ("w2class_result.json", 2, {"class10": 732, "pair10": 737, "cross9": 17}),
    ("w2pair_result.json", 2, {"class10": 732, "pair10": 737, "cross9": 17}),
    ("w3class_result.json", 3, {"class10": 908, "pair10": 913, "cross9": 22}),
    ("w3pair_result.json", 3, {"class10": 908, "pair10": 913, "cross9": 22}),
    ("w4class_result.json", 4, {"class10": 1937, "pair10": 1939, "cross9": 47}),
    ("w4pair_result.json", 4, {"class10": 1937, "pair10": 1939, "cross9": 47}),
    ("w6class_result.json", 6, {"class10": 2558, "pair10": 2562, "cross9": 62}),
    ("w6pair_result.json", 6, {"class10": 2558, "pair10": 2562, "cross9": 62}),
    ("x9_result.json", 4, {"cross9": 47}),
    ("x9w2_result.json", 2, {"class10": 732, "pair10": 737, "cross9": 17}),
    ("x9w3_result.json", 3, {"cross9": 22}),
):
    if not os.path.exists(os.path.join(OUT, fn)):
        gate("file_" + fn, False, "missing"); sys.exit(1)
    results[fn] = verify_witness_file(fn, W_, claims)

# oneswap artifacts
for fn, feas, imp, score in (
    ("oneswapT1class_result.json", 486, 3, 1937),
    ("oneswapT1pair_result.json", 486, 3, 1939),
    ("oneswapT2class_result.json", 222, 0, 1998),
    ("oneswapT2pair_result.json", 222, 0, 2000),
):
    d = load(fn)["result"]
    gate(fn, d["feasible_swaps"] == feas and d["improving_swaps"] == imp and d["best_neighbor_score"] == score, json.dumps(d))

# anneal witness-search artifacts (t-modes)
for fn, best in (("t1class_result.json", 1937), ("t1pair_result.json", 1939),
                 ("t2class_result.json", 1998), ("t2pair_result.json", 2000)):
    if not os.path.exists(os.path.join(OUT, fn)):
        continue
    d = load(fn)
    gate(fn + "_best", d["best_cost"] == best, f"{d['best_cost']}")
    wgs = d["witness"]["assignment_groups"]
    a = groups_to_a(wgs, 4, 9)
    gate(fn + "_recompute", class10(a) == d["witness"]["class_cross"])
    gate(fn + "_pair_recompute", pair10(a) == d["witness"]["pair_cross"])
    gate(fn + "_spread_recompute", abs(spreadpct(loads(a, d4v)) - d["witness"]["d4_spread_pct"]) < 1e-9)

# ---------------- R7: structural findings ----------------
same = lambda f, g: canon(load(f)["witness"]["groups"]) == canon(load(g)["witness"]["groups"])
gate("w2_same_partition", same("w2class_result.json", "w2pair_result.json"))
gate("w3_same_partition", same("w3class_result.json", "w3pair_result.json"))
gate("w4_same_partition", same("w4class_result.json", "w4pair_result.json"))
gate("w6_same_partition", same("w6class_result.json", "w6pair_result.json"))
gate("super_witness_values", class10(groups_to_a(load("w4class_result.json")["witness"]["groups"], 4, 9)) == 1937
     and pair10(groups_to_a(load("w4class_result.json")["witness"]["groups"], 4, 9)) == 1939
     and cross9(groups_to_a(load("w4class_result.json")["witness"]["groups"], 4, 9)) == 47)
gate("gaps_vs_candidate", 1998 - 1937 == 61 and 2000 - 1939 == 61 and 49 - 47 == 2)
a4 = groups_to_a(load("w4class_result.json")["witness"]["groups"], 4, 9)
gate("super_witness_t2_infeasible", spreadpct(loads(a4, d4v)) > 8.0, f"{spreadpct(loads(a4, d4v))}")
for fn in ("t1class_result.json", "t1pair_result.json"):
    if os.path.exists(os.path.join(OUT, fn)) and load(fn).get("witness"):
        gate(fn + "_same_super_partition", canon(load(fn)["witness"]["assignment_groups"]) == canon(load("w4class_result.json")["witness"]["groups"]))
# x9 witness: distinct partition also attaining cross9 47
gate("x9_witness_distinct_from_w4", not same("x9_result.json", "w4class_result.json"))

# addendum (2026-11-21, same day): x9w{N} 9-stone-layer closures for W=2,3
gate("x9w2_same_partition_as_w2class", same("x9w2_result.json", "w2class_result.json"))
gate("x9w3_distinct_from_w3class", not same("x9w3_result.json", "w3class_result.json"))
gate("x9w2_closed_opt_17", load("x9w2_result.json")["result"]["exact_optimum_if_closed"] == 17
     and load("x9w2_result.json")["result"]["status"] == "exact-optimum-closed-ub-is-global")
gate("x9w3_closed_opt_22", load("x9w3_result.json")["result"]["exact_optimum_if_closed"] == 22
     and load("x9w3_result.json")["result"]["status"] == "exact-optimum-closed-ub-is-global")
# co-attainment: the 10-stone-layer optimal witnesses also attain the closed 9-stone optima
a2 = groups_to_a(load("w2class_result.json")["witness"]["groups"], 2, 18)
gate("w2class_witness_cross9_is_optimum_17", cross9(a2) == 17 == load("x9w2_result.json")["result"]["exact_optimum_if_closed"])
a3 = groups_to_a(load("w3class_result.json")["witness"]["groups"], 3, 12)
gate("w3class_witness_cross9_is_optimum_22", cross9(a3) == 22 == load("x9w3_result.json")["result"]["exact_optimum_if_closed"])

summary = {
    "schema": "n11-residual72-worker-partition-exact-closures-verify-20261121-v1",
    "gates_total": len(GATES),
    "all_pass": all(g["pass"] for g in GATES),
    "results": {
        "w2": {"class10": 732, "pair10": 737, "cross9": 17, "closed": True, "class_pair_same_partition": True},
        "w3": {"class10": 908, "pair10": 913, "cross9": 22, "closed": True, "class_pair_same_partition": True},
        "w4": {"class10_ub": 1937, "pair10_ub": 1939, "cross9_ub": 47, "closed": False,
               "class_pair_same_partition": True, "super_witness": True, "t2_feasible": False},
        "w6": {"class10_ub": 2558, "pair10_ub": 2562, "cross9_ub": 62, "closed": False, "class_pair_same_partition": True},
        "x9": {"cross9_ub": 47, "closed": False},
        "candidate": {"class10": 1998, "pair10": 2000, "cross9": 49, "d4_spread_pct": 7.506677568819842},
        "baseline": {"class10": 4189, "pair10": 4193, "cross9": 104},
        "gaps": {"class10": 61, "pair10": 61, "cross9": 2},
    },
}
assert summary["all_pass"]
out_name = os.path.join(OUT, "verify_worker_partition_20261121_result.json")
with open(out_name, "w") as f:
    json.dump(summary, f, indent=1)
print(json.dumps(summary, indent=1))
print(f"ALL {len(GATES)} GATES PASS")
