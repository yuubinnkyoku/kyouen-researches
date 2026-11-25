#!/usr/bin/env python3
"""Complete exact survival curve under top-k root bans for the runner-up cover
target 00000000000000003800000009000000 (29 open non-STERILE rows, class-2
ranking #2, published exact minimum cover cost 15, published total
45,949,721,018,967,524 minimum covers).

This extends the published ban-survival curve (95b11316, 15 checks,
k in {0,1,2,3,4,5,6,7,8,10,12}) to ALL k = 0..12: the two previously
missing points k=9 and k=11 are determined, all 11 published points are
reproduced exactly (total/A/B/memo/gets), and the whole 13-point curve is
double-run byte-identical. Per published membership, the naive top-10 simple
sum is 50.69% of all minimum covers, but killing the covers that contain any
banned root requires the union, so the exact post-ban survival must be
recomputed with joint overlaps included. For every k = 0..12 this script
computes the exact number of minimum covers of the reduced system in which
the top-k roots (by published membership, ties broken by root hex) are
banned, using the same shared-memo anchored lazy matching DP (PmLazy) as
the published analysis:

  surviving(k) = A2 + B2 with reduced weights
     A2 = sum_s w1'(s) * pm(V\\{s})
     B2 = sum_d sum_{a<b} w'(d,a) w'(d,b) pm(V\\{d,a,b})

Semantics identical to the published cost-12 survival curve
(general_parent_cover_membership_20261118.py): a minimum cover of the reduced
system is exactly an original minimum (15-root) cover that avoids every
banned root, because maxspan is 2, every 15-root cover is A-type (14 disjoint
pairs + 1 singleton) or B-type (15 pairs, one doubly covered row), and the
formulas enumerate both types completely.

Two modes (the environment kills long-lived background processes, so each
curve point is computed inside its own short invocation and checkpointed):

  point <kk> [<kk2>] <points_dir>
      compute curve points kk (inclusive) .. kk2 (exclusive, default kk+1),
      writing one JSON file per point into <points_dir>
  assemble <final_json> <points_dir>
      re-derive the structure, run every structural / identity check
      (including the PmLazy re-validation against all 1,151 published
      cost-12 singleton memberships), read the point files, and write the
      final output JSON

Exact machine checks against the published output (in assemble mode):
  - k=0 rebuilds the published totals from scratch (total / A / B),
  - k=1 marginal kill == published membership of the top root,
  - k=2 kill == m1 + m2 - joint(r1, r2) from the published top-10 joint
    table, and the k=2 marginal gap == the same published joint,
  - structure (rows, roots, span histogram, per-row degrees/options)
    matches the published derived fields field by field.
"""
import json, os, sys, hashlib, time, gc
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11
TARGET = "00000000000000003800000009000000"
VALIDATION_PARENT = "00000000000000003800000008002000"
STATE_CAP = 6_000_000
BUDGET_SECONDS = 1_000_000_000.0  # effectively off; determinism relies on the state cap only
SURVIVAL_K = 12

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
    """Shared-memo anchored weighted matching DP with a hard state cap.
    get(mask) returns the exact weighted perfect matching count of the row
    subset `mask`."""
    def __init__(self, edge_w, r):
        self.edge_w = edge_w
        self.r = r
        self.memo = {0: 1}
        self.adj = [[] for _ in range(r)]
        for (a, b), w in edge_w.items():
            if w:
                if a < b:
                    self.adj[a].append((1 << b, w))
                else:
                    self.adj[b].append((1 << a, w))
        self.t0 = time.time()
        self.gets = 0

    def get(self, mask):
        memo = self.memo
        if mask in memo:
            self.gets += 1
            return memo[mask]
        edge_w = self.edge_w
        adj = self.adj
        stack = [mask]
        seen = {mask}
        order = []
        while stack:
            m = stack.pop()
            if m in memo:
                continue
            order.append(m)
            if len(memo) + len(seen) > STATE_CAP:
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
    return {"target": target, "proot_rows": proot_rows, "cand_total": cand_total,
            "pair_roots": pair_roots, "singleton_roots": singleton_roots,
            "edge_w": edge_w}

def load_context(with_validation):
    """Load pinned inputs, rebuild the target structure, and return a dict
    with everything both modes need."""
    read_pinned("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                "2fee1d0718547a62e346d35f5858d7913e37c097")
    read_pinned("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                "9c251da3138c5cb0516e097be5e5d0427dfaf5f0")
    read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                "e8785d509e8a11a37c0d03cc450455a14708c34d")
    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                                   "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    tbl = {e["hex"]: e for e in table["derived"]["table"]}[TARGET]
    pub = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
        "05f54eb58baad66403b327696b9a63f7433a13c3"))
    ctx = {"tbl": tbl, "pub": pub, "pub_der": pub["derived"],
           "pub_mem": pub["derived"]["membership"]}

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e

    cache = {}
    if with_validation:
        pub12 = json.loads(read_pinned(
            "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost12-parent-cover-membership-20261118.json",
            "c05de9d0ca194b6c7760b7370886cdc6ec5d218c"))
        V12 = build_parent(VALIDATION_PARENT, row_cands, cache)
        r12 = len(V12["target"])
        pm12 = PmLazy(V12["edge_w"], r12)
        full12 = (1 << r12) - 1
        pub_mem12 = pub12["cost12_parent"]["membership"]
        mism12 = 0
        checked12 = 0
        for s, rl in V12["singleton_roots"].items():
            v = pm12.get(full12 ^ (1 << s))
            for root in rl:
                checked12 += 1
                if pub_mem12.get(root) != v:
                    mism12 += 1
        ctx["checked12"] = checked12
        ctx["mism12"] = mism12
        del pm12
        gc.collect()

    P = build_parent(TARGET, row_cands, cache)
    r = len(P["target"])
    pair_roots = P["pair_roots"]; singleton_roots = P["singleton_roots"]
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    for s in range(r):
        w1.setdefault(s, 0)
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    root_row = {root: s for s, rl in singleton_roots.items() for root in rl}
    del row_cands
    gc.collect()
    ctx.update({"P": P, "r": r, "pair_roots": pair_roots,
                "singleton_roots": singleton_roots, "edge_w": P["edge_w"],
                "w1": w1, "root_pair": root_pair, "root_row": root_row,
                "cand_total": P["cand_total"]})
    return ctx

def compute_point(ctx, kk):
    """Exact surviving count at ban level kk (fresh PmLazy)."""
    edge_w = ctx["edge_w"]; w1 = ctx["w1"]; root_pair = ctx["root_pair"]
    r = ctx["r"]; pub_mem = ctx["pub_mem"]
    by_mem = sorted(pub_mem, key=lambda x: (-pub_mem[x], x))
    ban_order = by_mem[:SURVIVAL_K]
    full = (1 << r) - 1
    ew = dict(edge_w)
    ww1 = dict(w1)
    for root in ban_order[:kk]:
        e = root_pair[root]
        ew[e] = ew[e] - 1
        assert ew[e] >= 0
    pm = PmLazy(ew, r)
    t0 = time.time()
    A2 = 0
    for s, w in ww1.items():
        if w > 0:
            A2 += w * pm.get(full ^ (1 << s))
    B2 = 0
    for d in range(r):
        dbit = 1 << d
        nbrs = [a for a in range(r)
                if a != d and ew.get((min(d, a), max(d, a)), 0)]
        for i2 in range(len(nbrs)):
            a = nbrs[i2]
            wa = ew[(min(d, a), max(d, a))]
            for j2 in range(i2 + 1, len(nbrs)):
                b = nbrs[j2]
                wb = ew[(min(d, b), max(d, b))]
                B2 += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
    tot = A2 + B2
    print("[k=%02d] surviving=%d A=%d B=%d memo=%d gets=%d %.1fs"
          % (kk, tot, A2, B2, len(pm.memo), pm.gets, time.time() - t0), flush=True)
    return {"k": kk, "surviving_covers": tot, "type_A_surviving": A2,
            "type_B_surviving": B2, "pm_memo_states": len(pm.memo),
            "pm_gets": pm.gets}

def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: ... point <kk> [<kk2>] <dir> | assemble <json> <dir>")
    mode = sys.argv[1]
    if mode == "point":
        kk = int(sys.argv[2])
        if sys.argv[3].isdigit():
            kk2 = int(sys.argv[3])
            pdir = sys.argv[4]
        else:
            kk2 = kk + 1
            pdir = sys.argv[3]
        ctx = load_context(with_validation=False)
        for k in range(kk, kk2):
            pt = compute_point(ctx, k)
            out = os.path.join(pdir, "point-%02d.json" % k)
            with open(out, "w") as f:
                f.write(json.dumps(pt, indent=2) + "\n")
        return
    if mode == "assemble":
        out_path = sys.argv[2]
        pdir = sys.argv[3]
    else:
        raise SystemExit("unknown mode " + mode)

    def log(msg):
        print(msg, flush=True)
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})
        log("  check %-46s %s" % (name, "PASS" if ok else "FAIL"))

    log("[val] lazy pm vs published cost-12 singleton memberships")
    ctx = load_context(with_validation=True)
    P = ctx["P"]; r = ctx["r"]; tbl = ctx["tbl"]; pub_der = ctx["pub_der"]
    pub_mem = ctx["pub_mem"]; pair_roots = ctx["pair_roots"]
    singleton_roots = ctx["singleton_roots"]; edge_w = ctx["edge_w"]
    w1 = ctx["w1"]; root_pair = ctx["root_pair"]; root_row = ctx["root_row"]
    k = tbl["witness_size"]

    hist = defaultdict(int)
    for root, cov in P["proot_rows"].items():
        hist[len(cov)] += 1
    # published 15-check ban-survival curve (95b11316): 11 points, k=9/k=11 missing
    pub_bs = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-ban-survival-curve-20261118.json",
        "92db40a2560d6b2b1f4b65bc735f31bfc88b2c5e"))
    ctx["pub_bs"] = pub_bs
    mult_hist = defaultdict(int)
    for e, rl in pair_roots.items():
        mult_hist[len(rl)] += 1
    degree = defaultdict(int)
    for (a, b), w in edge_w.items():
        degree[a] += w; degree[b] += w
    for s in range(r):
        degree.setdefault(s, 0)
    options = {s: degree[s] + w1[s] for s in range(r)}

    check("val12.singleton_memberships", ctx["mism12"] == 0,
          {"checked": ctx["checked12"], "mismatches": ctx["mism12"]})
    check("rows", r == tbl["rows_r"] == 29 == pub_der["rows"], r)
    check("candidates", P["cand_total"] == tbl["candidates"] == 2203
          == pub_der["candidates"], P["cand_total"])
    check("distinct_roots", len(P["proot_rows"]) == tbl["distinct_roots"] == 1854
          == pub_der["distinct_roots"], len(P["proot_rows"]))
    check("span_histogram", {str(x): v for x, v in sorted(hist.items())} == tbl["span_histogram"]
          == pub_der["span_histogram"], dict(hist))
    check("pair_types", len(pair_roots) == pub_der["pair_types"] == 349, len(pair_roots))
    check("pair_type_multiplicity_histogram",
          {str(x): v for x, v in sorted(mult_hist.items())}
          == pub_der["pair_type_multiplicity_histogram"], dict(mult_hist))
    check("exact15", tbl["exact"] and tbl["lower_bound"] == k == 15
          == pub_der["minimum_size"])
    check("parity_odd", r % 2 == 1 and k * 2 - 1 == r and (k - 1) * 2 + 1 == r)
    check("root_set_matches_published", set(P["proot_rows"]) == set(pub_mem),
          {"rebuilt": len(P["proot_rows"]), "published": len(pub_mem)})
    check("per_row_singleton_root_count",
          {str(s): w1[s] for s in range(r)} == pub_der["per_row_singleton_root_count"])
    check("per_row_pair_root_degree",
          {str(s): degree[s] for s in range(r)} == pub_der["per_row_pair_root_degree"])
    check("per_row_cover_options",
          {str(s): options[s] for s in range(r)} == pub_der["per_row_cover_options"])

    # ---------- ban order: top-k by published membership (ties by root hex)
    by_mem = sorted(pub_mem, key=lambda x: (-pub_mem[x], x))
    pub_top50 = [e["root"] for e in pub_der["top50_by_membership"]]
    check("published_top50_order_matches_membership_sort", by_mem[:50] == pub_top50)
    pub_top50_mem = [e["membership"] for e in pub_der["top50_by_membership"]]
    check("published_top50_memberships_match_table",
          all(pub_mem[x] == m for x, m in zip(pub_top50, pub_top50_mem)))
    ban_order = by_mem[:SURVIVAL_K]
    check("ban_order_all_pair_roots", all(x in root_pair for x in ban_order))
    check("ban_order_distinct_pair_types",
          len({root_pair[x] for x in ban_order}) == len(ban_order))

    # ---------- read the checkpointed curve points
    total = pub_der["total_minimum_covers"]
    pts = []
    for kk in range(0, SURVIVAL_K + 1):
        p = os.path.join(pdir, "point-%02d.json" % kk)
        with open(p) as f:
            pts.append(json.load(f))
    check("points_complete", [p["k"] for p in pts] == list(range(SURVIVAL_K + 1)))

    survival = []
    prev_killed = 0
    for kk, pt in enumerate(pts):
        tot = pt["surviving_covers"]
        killed = total - tot
        naive_killed = sum(pub_mem[x] for x in ban_order[:kk])
        marginal = killed - prev_killed
        survival.append({
            "k": kk,
            # published convention: entry k lists the root banned going from
            # level k to level k+1 (None at the last level)
            "banned_root": ban_order[kk] if kk < SURVIVAL_K else None,
            "banned_rows": list(root_pair[ban_order[kk]]) if kk < SURVIVAL_K else None,
            "banned_published_membership": (pub_mem[ban_order[kk]]
                                             if kk < SURVIVAL_K else None),
            # the root whose ban produced this level (drives marginal_kill)
            "last_banned_root": ban_order[kk - 1] if kk >= 1 else None,
            "last_banned_rows": list(root_pair[ban_order[kk - 1]]) if kk >= 1 else None,
            "last_banned_published_membership": (pub_mem[ban_order[kk - 1]]
                                                 if kk >= 1 else None),
            "surviving_covers": tot,
            "type_A_surviving": pt["type_A_surviving"],
            "type_B_surviving": pt["type_B_surviving"],
            "killed_covers": killed,
            "killed_share": killed / total,
            "marginal_kill": marginal,
            # covers containing the last-banned root and some earlier banned
            # root: membership(last) - marginal(last), >= 0 by the union bound
            "marginal_overlap_with_earlier_bans": ((pub_mem[ban_order[kk - 1]] - marginal)
                                                    if kk >= 1 else None),
            "naive_simple_sum_killed": naive_killed,
            "naive_simple_sum_share": naive_killed / total,
            "joint_overlap_returned": naive_killed - killed,
            "pm_memo_states": pt["pm_memo_states"],
            "pm_gets": pt["pm_gets"],
        })
        prev_killed = killed

    # ---------- checks against published values
    s0, s1, s2 = survival[0], survival[1], survival[2]
    check("k0.total_reproduced", s0["surviving_covers"] == total,
          {"rebuilt": str(s0["surviving_covers"]), "published": str(total)})
    check("k0.A_reproduced", s0["type_A_surviving"] == pub_der["type_A_disjoint"],
          {"rebuilt": str(s0["type_A_surviving"])})
    check("k0.B_reproduced", s0["type_B_surviving"] == pub_der["type_B_one_duplicate_row"],
          {"rebuilt": str(s0["type_B_surviving"])})
    check("survival.k1_marginal_equals_membership",
          s1["marginal_kill"] == pub_mem[ban_order[0]],
          {"marginal": str(s1["marginal_kill"]),
           "membership": str(pub_mem[ban_order[0]])})
    j12 = None
    for e in pub_der["top10_joint_membership"]:
        if {e["a"], e["b"]} == {ban_order[0], ban_order[1]}:
            j12 = e["joint_membership"]
    check("k2.joint_lookup_found", j12 is not None)
    ie_killed = (pub_mem[ban_order[0]] + pub_mem[ban_order[1]]) - j12
    check("survival.k2_killed_equals_inclusion_exclusion",
          s2["killed_covers"] == ie_killed,
          {"direct": str(s2["killed_covers"]), "inclusion_exclusion": str(ie_killed),
           "joint": str(j12)})
    check("survival.monotone",
          all(survival[i]["surviving_covers"] <= survival[i - 1]["surviving_covers"]
              for i in range(1, len(survival))))
    check("survival.marginal_nonnegative",
          all(e["marginal_kill"] >= 0 for e in survival[1:]))
    check("survival.marginal_bounded_by_last_membership",
          all(e["marginal_kill"] <= e["last_banned_published_membership"]
              for e in survival[1:]))
    check("survival.k2_marginal_gap_equals_published_joint",
          survival[2]["marginal_overlap_with_earlier_bans"] == j12,
          {"gap": str(survival[2]["marginal_overlap_with_earlier_bans"]),
           "joint": str(j12)})
    check("survival.marginal_overlap_nonnegative",
          all(e["marginal_overlap_with_earlier_bans"] >= 0 for e in survival[1:]))
    check("survival.exact_kill_le_naive_sum",
          all(e["killed_covers"] <= e["naive_simple_sum_killed"] for e in survival))
    check("survival.overlap_nonnegative",
          all(e["joint_overlap_returned"] >= 0 for e in survival))
    check("survival.k12_positive", survival[-1]["surviving_covers"] > 0,
          str(survival[-1]["surviving_covers"]))

    # ---------- cross-check against the published 15-check curve (95b11316)
    pub_bs = ctx["pub_bs"]
    pub_pts = {e["k"]: e for e in pub_bs["derived"]["curve"]}
    by_k = {p["k"]: p for p in pts}
    mism = 0
    for kk, e in sorted(pub_pts.items()):
        mine = by_k[kk]
        if (mine["surviving_covers"] != e["total"]
                or mine["type_A_surviving"] != e["type_A"]
                or mine["type_B_surviving"] != e["type_B"]
                or mine["pm_memo_states"] != e["memo_states"]
                or mine["pm_gets"] != e["pm_gets"]):
            mism += 1
    check("published_ban_survival_11_points_reproduced_exactly",
          mism == 0 and len(pub_pts) == 11,
          {"published_points": len(pub_pts), "mismatches": mism})
    check("published_ban_survival_ban_order_matches",
          pub_pts[12]["banned_roots"] == ban_order)
    check("new_points_are_k9_and_k11",
          set(pub_bs["derived"]["ban_points"]) == set(range(13)) - {9, 11}
          and {9, 11} == (set(range(13)) - set(pub_bs["derived"]["ban_points"])),
          {"published": pub_bs["derived"]["ban_points"]})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-runnerup29-survival-curve-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve of the 45,949,721,018,967,524 minimum covers "
                  "of the 29-row runner-up target 00000000000000003800000009000000 "
                  "under top-k root bans (k=0..12), joint overlaps included"),
        "inputs": {
            "worklist": {"path": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                         "git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"path": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                        "git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                        "git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                             "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "published_cost12_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost12-parent-cover-membership-20261118.json",
                                          "git_blob_sha1": "c05de9d0ca194b6c7760b7370886cdc6ec5d218c"},
            "published_runnerup29_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
                                             "git_blob_sha1": "05f54eb58baad66403b327696b9a63f7433a13c3"},
            "published_ban_survival_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-ban-survival-curve-20261118.json",
                                              "git_blob_sha1": "92db40a2560d6b2b1f4b65bc735f31bfc88b2c5e"},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("Published even/odd-r cover framework with reduced weights per ban "
                   "level (identical semantics to the cost-12 survival curve): "
                   "surviving(k) = A2 + B2 over the reduced system, pm values supplied "
                   "by the shared-memo anchored lazy matching DP (state cap 6M; each "
                   "curve point computed in its own invocation because this "
                   "environment kills long-lived background processes). The k=0 point "
                   "is a full from-scratch recomputation of the published total/A/B; "
                   "k=1 and k=2 reproduce the published membership and "
                   "membership+joint inclusion-exclusion identities exactly."),
        "derived": {
            "rows": r,
            "minimum_size": k,
            "total_minimum_covers": total,
            "survival_curve_banning_topk": survival,
            "ban_order": [{"root": x, "rows_covered": list(root_pair[x]),
                           "published_membership": pub_mem[x],
                           "published_rank": i + 1}
                          for i, x in enumerate(ban_order)],
            "validation": {"cost12_singleton_memberships_checked": ctx["checked12"],
                            "cost12_singleton_mismatches": ctx["mism12"]},
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. The survival curve "
                                 "counts minimum cover plans that avoid the banned "
                                 "roots; it is not a search cost and implies nothing "
                                 "about WIN/REFUTED outcomes of any root. REFUTED-D10 "
                                 "and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    log("wrote %s: all_pass=%s checks=%d" % (out_path, all_pass, len(checks)))
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]][:10],
                      "curve": [{"k": e["k"],
                                 "surviving": e["surviving_covers"],
                                 "killed_share": e["killed_share"],
                                 "naive_share": e["naive_simple_sum_share"]}
                                for e in survival]}, indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
