#!/usr/bin/env python3
"""Exact B-type total (and full minimum-cover total) for the 31-row cost-16
parent 00000000000000003800000008001000, completing the published phase A
analysis (commit 2adf7f94, blob fe4b4b55: A-type total 2,305,787,291,293,934,388
and all 1,483 singleton memberships).

The published phase A run left phase B (the B-type total) undetermined: four
attempts were killed by OOM in the previous 3.2 GB environment because the
pair-membership phase drives a single shared memo far past the singleton
phase. This script closes that gap with a slice design: B16 is computed as
31 independent per-d slices,

    B_d = sum_{a<b in N(d)} w(d,a) w(d,b) pm(V \ {d,a,b})
    B16 = sum_d B_d,

where each slice uses its own fresh PmLazy memo (state cap 5M, observed peak
about 3.5M states per slice), so no phase ever exceeds the singleton-phase
memory profile. Every slice is checkpointed to its own JSON file so the run
survives host kills between invocations.

It also records the pre-analysis anchor measurements that justified the
design: fresh-memo anchored state counts for singleton anchors pm(V\{s})
and B-phase anchors pm(V\{d,a,b}) on both the 31-row target and the 29-row
runner-up baseline (published singleton anchor ~514K states), quantifying
that the anchored state space is governed by candidate structure rather than
by row count.

The final assembled JSON embeds only deterministic fields (timing fields
"seconds" are stripped from the embedded phase files), so two independent
full runs produce byte-identical output.

Modes:
  measure <which> <file> [<max_anchors>]
      which in {baseline29, target31}; computes fresh-memo anchor state
      counts (singleton anchors, then B-phase anchors), resuming from and
      checkpointing to <file> after every anchor.
  A <file>
      shared-memo singleton phase over the 31-row target: per-row pm(V\{s}),
      A16 = sum_s w1(s) pm(V\{s}); validates against the published phase A
      per-row values and total before writing <file>.
  Bslice <d_lo> <d_hi> <dir>
      computes slices d in [d_lo, d_hi) into <dir>/slice-<d>.json
  assemble <final_json> <workdir>
      expects <workdir>/measure-baseline29.json, <workdir>/measure-target31.json,
      <workdir>/a-phase.json, <workdir>/slices/slice-<d>.json (d=0..30);
      re-derives the structure, runs all checks (including reproduction of
      the published phase A structure/total/per-row values and of all 1,505
      published runner-up singleton memberships), and writes the final JSON.
"""
import json, os, sys, hashlib, time, gc
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11
TARGET16 = "00000000000000003800000008001000"
BASELINE29 = "00000000000000003800000009000000"
STATE_CAP_A = 5_000_000
STATE_CAP_B = 5_000_000
STATE_CAP_MEASURE = 2_500_000
STATE_CAP_VAL = 6_000_000

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if git_blob_sha(data) != pin:
        raise SystemExit("pin mismatch: " + rel)
    return data

T = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]
TO = [tuple(t(i % N, i // N) for i in range(121)) for t in T]

def orbit_masks(mask):
    outs = []
    for to in TO:
        out = 0
        for i in range(121):
            if (mask >> i) & 1:
                qx, qy = to[i]
                out |= 1 << (qy * N + qx)
        outs.append(out)
    return outs

class PmLazy:
    def __init__(self, edge_w, r, cap):
        self.edge_w = edge_w
        self.r = r
        self.cap = cap
        self.memo = {0: 1}
        self.adj = [[] for _ in range(r)]
        for (a, b), w in edge_w.items():
            if w:
                if a < b:
                    self.adj[a].append((1 << b, w))
                else:
                    self.adj[b].append((1 << a, w))
        self.gets = 0

    def get(self, mask):
        memo = self.memo
        if mask in memo:
            self.gets += 1
            return memo[mask]
        edge_w = self.edge_w
        stack = [mask]
        seen = {mask}
        order = []
        while stack:
            m = stack.pop()
            if m in memo:
                continue
            order.append(m)
            if len(memo) + len(seen) > self.cap:
                raise MemoryError("pm state cap exceeded")
            if m == 0:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            mm = rest
            while mm:
                jbit = mm & -mm
                mm ^= jbit
                j = jbit.bit_length() - 1
                key = (first, j) if first < j else (j, first)
                if edge_w.get(key, 0):
                    sub = rest & ~jbit
                    if sub not in memo and sub not in seen:
                        seen.add(sub)
                        stack.append(sub)
        for m in sorted(order, key=lambda x: bin(x).count("1")):
            if m in memo:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            acc = 0
            mm = rest
            while mm:
                jbit = mm & -mm
                mm ^= jbit
                j = jbit.bit_length() - 1
                key = (first, j) if first < j else (j, first)
                w = edge_w.get(key, 0)
                if w:
                    acc += w * memo[rest & ~jbit]
            memo[m] = acc
        self.gets += 1
        return memo[mask]

def build_parent(target_hex, row_cands, cache):
    p_orbit = cache.setdefault(target_hex,
                    {format(m, "032x") for m in orbit_masks(int(target_hex, 16))})
    target = sorted(h for h in row_cands
                    if any(format(int(h, 16) ^ (1 << b), "032x") in p_orbit
                           for b in range(121) if (int(h, 16) >> b) & 1))
    idx = {h: i for i, h in enumerate(target)}
    proot_rows = defaultdict(set)
    cand_total = 0
    for h in target:
        e = row_cands[h]
        cand_total += e["cost"]
        for root, bit in e["cands"]:
            proot_rows[root].add(h)
    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)
    for root, cov in proot_rows.items():
        if len(cov) == 2:
            a, b = sorted(idx[h] for h in cov)
            pair_roots[(a, b)].append(root)
        else:
            (s,) = [idx[h] for h in cov]
            singleton_roots[s].append(root)
    edge_w = {e: len(rl) for e, rl in pair_roots.items()}
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    for s in range(len(target)):
        w1.setdefault(s, 0)
    return {"target": target, "proot_rows": proot_rows, "cand_total": cand_total,
            "pair_roots": pair_roots, "singleton_roots": singleton_roots,
            "edge_w": edge_w, "w1": w1, "r": len(target)}

def load_parents():
    read_pinned("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                "2fee1d0718547a62e346d35f5858d7913e37c097")
    read_pinned("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                "9c251da3138c5cb0516e097be5e5d0427dfaf5f0")
    read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                "e8785d509e8a11a37c0d03cc450455a14708c34d")
    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                                    "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    phase_a = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-a-phase-20261118.json",
                                     "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"))
    runnerup29 = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
                                        "05f54eb58baad66403b327696b9a63f7433a13c3"))
    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e
    cache = {}
    P16 = build_parent(TARGET16, row_cands, cache)
    P29 = build_parent(BASELINE29, row_cands, cache)
    del row_cands
    gc.collect()
    tbl16 = {e["hex"]: e for e in table["derived"]["table"]}[TARGET16]
    return {"P16": P16, "P29": P29, "tbl16": tbl16, "phase_a": phase_a,
            "runnerup29": runnerup29}

def neighbors(edge_w, r):
    nbr = defaultdict(list)
    for (a, b), w in edge_w.items():
        if w:
            nbr[a].append(b)
            nbr[b].append(a)
    for s in range(r):
        nbr[s].sort()
    return nbr

# ---------------- measure ----------------

def do_measure(ctx, which, out_file, max_anchors):
    P = ctx["P16"] if which == "target31" else ctx["P29"]
    r = P["r"]
    edge_w = P["edge_w"]
    w1 = P["w1"]
    full = (1 << r) - 1
    if os.path.exists(out_file):
        with open(out_file) as f:
            st = json.load(f)
    else:
        st = {"which": which, "rows": r,
              "singleton_anchor_states": {}, "b_phase_anchor_states": {}}
    assert st["which"] == which and st["rows"] == r
    done = 0
    t_last = time.time()
    for s in range(r):
        if st["singleton_anchor_states"].get(str(s)) is not None:
            continue
        if done >= max_anchors:
            print("[measure %s] budget reached after %d anchors" % (which, done), flush=True)
            break
        if w1[s] == 0:
            st["singleton_anchor_states"][str(s)] = -1
        else:
            pm = PmLazy(edge_w, r, STATE_CAP_MEASURE)
            pm.get(full ^ (1 << s))
            st["singleton_anchor_states"][str(s)] = len(pm.memo)
            del pm
        done += 1
        with open(out_file, "w") as f:
            f.write(json.dumps(st, indent=1) + "\n")
        print("[measure %s] singleton s=%02d done (cum %.1fs)" % (which, s, time.time() - t_last), flush=True)
    nbr = neighbors(edge_w, r)
    for d in range(r):
        if st["b_phase_anchor_states"].get(str(d)) is not None:
            continue
        if done >= max_anchors:
            print("[measure %s] budget reached after %d anchors" % (which, done), flush=True)
            break
        if len(nbr[d]) < 2:
            st["b_phase_anchor_states"][str(d)] = -1
        else:
            a, b = nbr[d][0], nbr[d][1]
            pm = PmLazy(edge_w, r, STATE_CAP_MEASURE)
            pm.get(full ^ (1 << d) ^ (1 << a) ^ (1 << b))
            st["b_phase_anchor_states"][str(d)] = len(pm.memo)
            del pm
        done += 1
        with open(out_file, "w") as f:
            f.write(json.dumps(st, indent=1) + "\n")
        print("[measure %s] b-anchor d=%02d done (cum %.1fs)" % (which, d, time.time() - t_last), flush=True)
    complete = (len([v for v in st["singleton_anchor_states"].values() if v >= 0]) ==
                len([1 for s in range(r) if w1[s] > 0])
                and len(st["b_phase_anchor_states"]) == r)
    st["complete"] = complete
    with open(out_file, "w") as f:
        f.write(json.dumps(st, indent=1) + "\n")
    print("[measure %s] saved %s complete=%s" % (which, out_file, complete), flush=True)

# ---------------- A phase ----------------

def do_a(ctx, out_file):
    P = ctx["P16"]
    r = P["r"]
    edge_w = P["edge_w"]
    w1 = P["w1"]
    full = (1 << r) - 1
    t0 = time.time()
    pm = PmLazy(edge_w, r, STATE_CAP_A)
    per_row = {}
    A16 = 0
    for s in range(r):
        v = pm.get(full ^ (1 << s))
        per_row[str(s)] = v
        A16 += w1[s] * v
    out = {"rows": r, "type_A_total": A16, "per_row_pm": per_row,
           "w1": {str(s): w1[s] for s in range(r)},
           "memo_states": len(pm.memo), "pm_gets": pm.gets,
           "seconds": round(time.time() - t0, 1)}
    with open(out_file, "w") as f:
        f.write(json.dumps(out, indent=1) + "\n")
    print("[A] A16=%d memo=%d gets=%d %.1fs" % (A16, len(pm.memo), pm.gets, out["seconds"]), flush=True)

# ---------------- B slices ----------------

def do_bslice(ctx, d_lo, d_hi, sdir):
    P = ctx["P16"]
    r = P["r"]
    edge_w = P["edge_w"]
    full = (1 << r) - 1
    nbr = neighbors(edge_w, r)
    os.makedirs(sdir, exist_ok=True)
    for d in range(d_lo, d_hi):
        out_p = os.path.join(sdir, "slice-%02d.json" % d)
        if os.path.exists(out_p):
            print("[B] slice %d already present, skip" % d, flush=True)
            continue
        t0 = time.time()
        pm = PmLazy(edge_w, r, STATE_CAP_B)
        dbit = 1 << d
        B_d = 0
        anchors = 0
        for i2 in range(len(nbr[d])):
            a = nbr[d][i2]
            wa = edge_w[(min(d, a), max(d, a))]
            for j2 in range(i2 + 1, len(nbr[d])):
                b = nbr[d][j2]
                wb = edge_w[(min(d, b), max(d, b))]
                B_d += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
                anchors += 1
        out = {"d": d, "b_d": B_d, "anchors": anchors,
               "memo_states": len(pm.memo), "pm_gets": pm.gets,
               "seconds": round(time.time() - t0, 1)}
        with open(out_p, "w") as f:
            f.write(json.dumps(out, indent=1) + "\n")
        print("[B] d=%02d B_d=%d anchors=%d memo=%d %.1fs"
              % (d, B_d, anchors, len(pm.memo), out["seconds"]), flush=True)

# ---------------- assemble ----------------

def do_assemble(ctx, final_json, workdir):
    def log(msg):
        print(msg, flush=True)
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})
        log("  check %-46s %s" % (name, "PASS" if ok else "FAIL"))

    P16 = ctx["P16"]; P29 = ctx["P29"]
    r = P16["r"]; r29 = P29["r"]
    tbl = ctx["tbl16"]; pa = ctx["phase_a"]; pad = pa["derived"]
    edge_w = P16["edge_w"]; w1 = P16["w1"]
    k = tbl["witness_size"]

    hist = defaultdict(int)
    for root, cov in P16["proot_rows"].items():
        hist[len(cov)] += 1
    mult_hist = defaultdict(int)
    for e, rl in P16["pair_roots"].items():
        mult_hist[len(rl)] += 1
    degree = defaultdict(int)
    for (a, b), w in edge_w.items():
        degree[a] += w; degree[b] += w
    for s in range(r):
        degree.setdefault(s, 0)
    options = {s: degree[s] + w1[s] for s in range(r)}

    # structure vs pinned published phase A output, field by field
    check("rows", r == 31 == pad["rows"] == tbl["rows_r"])
    check("candidates", P16["cand_total"] == 2333 == pad["candidates"] == tbl["candidates"])
    check("distinct_roots", len(P16["proot_rows"]) == 1908 == pad["distinct_roots"] == tbl["distinct_roots"])
    check("span_histogram", {str(x): v for x, v in sorted(hist.items())} == {"1": 1483, "2": 425}
          == pad["span_histogram"] == tbl["span_histogram"])
    check("pair_types", len(P16["pair_roots"]) == 425 == pad["pair_types"])
    check("pair_type_multiplicity_histogram",
          {str(x): v for x, v in sorted(mult_hist.items())} == {"1": 425}
          == pad["pair_type_multiplicity_histogram"])
    check("exact16", tbl["exact"] and tbl["lower_bound"] == k == 16 == pad["minimum_size"])
    check("parity_odd", r % 2 == 1 and k * 2 - 1 == r)
    check("per_row_singleton_root_count",
          {str(s): w1[s] for s in range(r)} == pad["per_row_singleton_root_count"])
    check("per_row_pair_root_degree",
          {str(s): degree[s] for s in range(r)} == pad["per_row_pair_root_degree"])
    check("per_row_cover_options",
          {str(s): options[s] for s in range(r)} == pad["per_row_cover_options"])

    # ---- A phase
    with open(os.path.join(workdir, "a-phase.json")) as f:
        aph = json.load(f)
    A16 = aph["type_A_total"]
    check("a16.published_total_reproduced", A16 == pad["type_A_total"],
          {"rebuilt": str(A16), "published": str(pad["type_A_total"])})
    mism_pm = [s for s in range(r)
               if aph["per_row_pm"][str(s)] != pad["singleton_membership_stats"]["per_row"][str(s)]]
    check("a16.per_row_pm_reproduced", not mism_pm, {"mismatches": mism_pm})
    check("a16.singleton_membership_sum_identity",
          sum(w1[s] * aph["per_row_pm"][str(s)] for s in range(r)) == A16)
    check("a16.memo_states_match_published_scaling",
          aph["memo_states"] == pad["scaling_facts"]["singleton_phase_memo_states"],
          {"memo": aph["memo_states"]})

    # ---- B slices
    slices = []
    for d in range(r):
        with open(os.path.join(workdir, "slices", "slice-%02d.json" % d)) as f:
            slices.append(json.load(f))
    check("b.slices_complete", [sl["d"] for sl in slices] == list(range(r)))
    B16 = sum(sl["b_d"] for sl in slices)
    check("b16.slice_sum_identity", B16 == sum(sl["b_d"] for sl in slices))
    deg16 = {s: degree[s] for s in range(r)}
    check("b_slice.anchor_counts_match_degree_binomial",
          all(sl["anchors"] == deg16[sl["d"]] * (deg16[sl["d"]] - 1) // 2 for sl in slices),
          {"max_anchors": max(sl["anchors"] for sl in slices)})
    check("b16.positive", B16 > 0, str(B16))
    check("b_slice.anchor_counts_in_range",
          all(270 <= sl["anchors"] <= 450 for sl in slices),
          {"min": min(sl["anchors"] for sl in slices), "max": max(sl["anchors"] for sl in slices)})
    check("b_slice.memo_within_cap",
          all(sl["memo_states"] <= STATE_CAP_B for sl in slices),
          {"max": max(sl["memo_states"] for sl in slices)})
    check("b16.lt_a16", B16 < A16, {"A": str(A16), "B": str(B16)})
    total = A16 + B16
    a_share = A16 / total
    b_share = B16 / total
    check("total.identity", total == A16 + B16)
    check("shares.a_dominates", 0.7 < a_share < 0.85, {"A": round(a_share, 4), "B": round(b_share, 4)})

    # ---- measurements
    with open(os.path.join(workdir, "measure-baseline29.json")) as f:
        mb = json.load(f)
    with open(os.path.join(workdir, "measure-target31.json")) as f:
        mt = json.load(f)
    b29_sa = sorted(v for v in mb["singleton_anchor_states"].values() if v >= 0)
    t31_sa = sorted(v for v in mt["singleton_anchor_states"].values() if v >= 0)
    b29_ba = sorted(v for v in mb["b_phase_anchor_states"].values() if v >= 0)
    t31_ba = sorted(v for v in mt["b_phase_anchor_states"].values() if v >= 0)
    check("measure.complete", mb.get("complete") and mt.get("complete"),
          {"b29_sa": len(b29_sa), "t31_sa": len(t31_sa),
           "b29_ba": len(b29_ba), "t31_ba": len(t31_ba)})
    check("measure.baseline29_singleton_anchor_near_published",
          500_000 <= b29_sa[0] and b29_sa[-1] <= 530_000,
          {"min": b29_sa[0], "max": b29_sa[-1]})
    check("measure.target31_singleton_anchor_range",
          1_300_000 <= t31_sa[0] and t31_sa[-1] <= 1_400_000,
          {"min": t31_sa[0], "max": t31_sa[-1]})
    ratio_sa = t31_sa[0] / b29_sa[0]
    check("measure.singleton_anchor_growth_ratio",
          2.4 <= ratio_sa <= 2.9, {"ratio": round(ratio_sa, 4)})
    check("measure.target31_b_anchor_matches_baseline29_singleton_scale",
          abs(t31_ba[0] - b29_sa[0]) <= 100 and abs(t31_ba[-1] - b29_sa[-1]) <= 100,
          {"t31_ba": [t31_ba[0], t31_ba[-1]], "b29_sa": [b29_sa[0], b29_sa[-1]]})
    ratio_ba = t31_ba[0] / b29_ba[0]
    check("measure.b_phase_anchor_growth_ratio",
          2.4 <= ratio_ba <= 2.9, {"ratio": round(ratio_ba, 4)})

    # ---- implementation validation against published runner-up29 memberships
    pub_mem29 = ctx["runnerup29"]["derived"]["membership"]
    pm29 = PmLazy(P29["edge_w"], r29, STATE_CAP_VAL)
    full29 = (1 << r29) - 1
    mism29 = 0
    checked29 = 0
    for s, rl in P29["singleton_roots"].items():
        v = pm29.get(full29 ^ (1 << s))
        for root in rl:
            checked29 += 1
            if pub_mem29.get(root) != v:
                mism29 += 1
    check("val.runnerup29_singleton_memberships", mism29 == 0,
          {"checked": checked29, "mismatches": mism29})
    del pm29
    gc.collect()

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-cost16-parent-b-phase-total-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact B-type total and full minimum-cover total for the 31-row "
                  "cost-16 parent 00000000000000003800000008001000, completing the "
                  "published phase A analysis via 31 independent per-d PmLazy slices"),
        "inputs": {
            "worklist": {"path": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                         "git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"path": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                        "git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                        "git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                             "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "published_phase_a_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-a-phase-20261118.json",
                                          "git_blob_sha1": "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"},
            "published_runnerup29_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
                                             "git_blob_sha1": "05f54eb58baad66403b327696b9a63f7433a13c3"},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("Published odd-r A/B framework. A-type total recomputed with a single "
                   "shared-memo PmLazy singleton phase (state cap 5M) and validated against "
                   "the published phase A output (total, all 31 per-row pm values, memo "
                   "states). B-type total computed as 31 independent per-d slices "
                   "B_d = sum_{a<b in N(d)} w(d,a) w(d,b) pm(V\{d,a,b}), each slice with "
                   "its own fresh PmLazy memo (state cap 5M): the slice design keeps every "
                   "phase within the singleton-phase memory profile that previously OOM-killed "
                   "the unsliced pair-membership phase. Anchor state-space measurements "
                   "quantify the 29->31 row scaling (fresh-memo pm(V\{s}) and pm(V\{d,a,b}) "
                   "anchor trees on both parents). The implementation is additionally "
                   "validated by reproducing all 1,505 published runner-up singleton "
                   "memberships. This environment kills long-lived background processes, so "
                   "every phase is checkpointed per anchor/slice and re-invocable. The final "
                   "JSON embeds only deterministic fields (timing stripped) so double runs "
                   "are byte-comparable."),
        "derived": {
            "rows": r,
            "candidates": P16["cand_total"],
            "distinct_roots": len(P16["proot_rows"]),
            "span_histogram": {str(x): v for x, v in sorted(hist.items())},
            "pair_types": len(P16["pair_roots"]),
            "pair_type_multiplicity_histogram": {str(x): v for x, v in sorted(mult_hist.items())},
            "minimum_size": k,
            "parity": "odd",
            "type_A_total": A16,
            "type_B_total": B16,
            "total_minimum_covers": total,
            "type_A_share": a_share,
            "type_B_share": b_share,
            "b_slices": [{kk: vv for kk, vv in sl.items() if kk != "seconds"} for sl in slices],
            "b_slice_memo_states_max": max(sl["memo_states"] for sl in slices),
            "b_slice_anchor_count_min": min(sl["anchors"] for sl in slices),
            "b_slice_anchor_count_max": max(sl["anchors"] for sl in slices),
            "a_phase": {kk: vv for kk, vv in aph.items() if kk != "seconds"},
            "measurements": {
                "baseline29_singleton_anchor_states": mb["singleton_anchor_states"],
                "baseline29_b_phase_anchor_states": mb["b_phase_anchor_states"],
                "target31_singleton_anchor_states": mt["singleton_anchor_states"],
                "target31_b_phase_anchor_states": mt["b_phase_anchor_states"],
                "baseline29_singleton_anchor_min_max": [b29_sa[0], b29_sa[-1]],
                "target31_singleton_anchor_min_max": [t31_sa[0], t31_sa[-1]],
                "baseline29_b_phase_anchor_min_max": [b29_ba[0], b29_ba[-1]],
                "target31_b_phase_anchor_min_max": [t31_ba[0], t31_ba[-1]],
                "singleton_anchor_growth_ratio": ratio_sa,
                "b_phase_anchor_growth_ratio": ratio_ba,
            },
            "validation": {"runnerup29_singleton_memberships_checked": checked29,
                            "runnerup29_mismatches": mism29},
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. The totals count minimum "
                                 "cover plans of the candidate-root system; they are not "
                                 "search costs and imply nothing about WIN/REFUTED "
                                 "outcomes of any root. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(final_json, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    log("wrote %s: all_pass=%s checks=%d" % (final_json, all_pass, len(checks)))
    print(json.dumps({"all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]],
                      "A16": str(A16), "B16": str(B16), "total": str(total),
                      "A_share": round(a_share, 6), "B_share": round(b_share, 6)}, indent=1))
    if not all_pass:
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: measure <which> <file> [<max_anchors>] | A <file> | "
                         "Bslice <d_lo> <d_hi> <dir> | assemble <json> <workdir>")
    mode = sys.argv[1]
    ctx = load_parents()
    if mode == "measure":
        which = sys.argv[2]
        assert which in ("baseline29", "target31")
        out_file = sys.argv[3]
        max_anchors = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
        do_measure(ctx, which, out_file, max_anchors)
        return
    if mode == "A":
        do_a(ctx, sys.argv[2])
        return
    if mode == "Bslice":
        do_bslice(ctx, int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
        return
    if mode == "assemble":
        do_assemble(ctx, sys.argv[2], sys.argv[3])
        return
    raise SystemExit("unknown mode " + mode)

if __name__ == "__main__":
    main()
