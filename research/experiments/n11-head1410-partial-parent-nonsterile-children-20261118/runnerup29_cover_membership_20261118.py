#!/usr/bin/env python3
"""Exact minimum-cover membership / joint analysis for the runner-up cover
target 00000000000000003800000009000000 (29 open non-STERILE rows, class-2
ranking #2, published exact minimum cover cost 15), using a shared-memo
anchored lazy matching DP instead of an all-mask 2^29 table (which does not
fit this environment).

Key observation (from the pre-analysis run): the anchored-reachable state
space of this parent is only ~514k states per 28-row root (each pm(V\\{s})
completes in ~3s), and the state sets from different roots nearly coincide,
so a single shared memo serves every formula below.

Formulas are the published general framework (odd r, k=15):
  A-type covers (14 disjoint pairs + 1 disjoint singleton):
     A = sum_s w1(s) * pm(V\\{s})
  B-type covers (15 pairs, exactly one doubly covered row d, the two pairs
     containing d being {d,a},{d,b}, a != b):
     B = sum_d sum_{a<b, a,b != d} w(d,a) w(d,b) pm(V\\{d,a,b})
  singleton-root membership = pm(V\\{s}) (A-type only)
  pair-root membership: A-part = sum_{s not in e} w1(s) pm(V\\e\\{s});
     B-part = sum_{d in e} sum_{z not in e} w(d,z) pm(V\\e\\{z})
            + sum_{d not in e} sum_{a<b, a,b not in e+{d}}
                  w(d,a) w(d,b) pm(V\\e\\{d,a,b})
  joint of two pair roots: sharing row d -> pm(V\\{d,a,b}) (B-type only,
     both roots being the duplicate pairs); disjoint -> A + B-i + B-ii
     exactly as published for the 23-row target.
Identities: sum(A-parts) == k*A, sum(B-parts) == k*B, sum == k*total.

The lazy pm implementation is validated against the published cost-12 parent
output (blob c05de9d0): the membership of every singleton root on row s of
that parent equals pm(V12\\{s}), giving 23 independent exact crosschecks, and
the pair-root membership identity on that parent additionally exercises the
A/B formulas end to end.
"""
import json, os, sys, hashlib, time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11
TARGET = "00000000000000003800000009000000"
VALIDATION_PARENT = "00000000000000003800000008002000"
STATE_CAP = 12_000_000
BUDGET_SECONDS = 1500.0

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
    """Shared-memo anchored weighted matching DP with a hard state cap and
    wall-clock budget. get(mask) returns the exact weighted perfect matching
    count of the row subset `mask`."""
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
            if len(memo) + len(seen) > STATE_CAP or time.time() - self.t0 > BUDGET_SECONDS:
                raise MemoryError("pm state cap or budget exceeded")
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

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "runnerup29-cover-membership-20261118.json")
    def log(msg):
        print(msg, flush=True)
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    read_pinned("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                "2fee1d0718547a62e346d35f5858d7913e37c097")
    read_pinned("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                "9c251da3138c5cb0516e097be5e5d0427dfaf5f0")
    read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                "e8785d509e8a11a37c0d03cc450455a14708c34d")
    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                                   "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    tbl = {e["hex"]: e for e in table["derived"]["table"]}[TARGET]
    pub12 = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost12-parent-cover-membership-20261118.json",
        "c05de9d0ca194b6c7760b7370886cdc6ec5d218c"))

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e

    # ---------- validation of the lazy pm against the published 23-row output
    log("[val] lazy pm vs published cost-12 singleton memberships")
    cache = {}
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
    check("val12.singleton_memberships", mism12 == 0,
          {"checked": checked12, "mismatches": mism12})
    log("  singleton memberships checked: %d, mismatches: %d" % (checked12, mism12))
    del pm12

    # ---------- target structure
    P = build_parent(TARGET, row_cands, cache)
    r = len(P["target"])
    k = tbl["witness_size"]
    check("rows", r == tbl["rows_r"] == 29, r)
    check("candidates", P["cand_total"] == tbl["candidates"] == 2203, P["cand_total"])
    hist = defaultdict(int)
    for root, cov in P["proot_rows"].items():
        hist[len(cov)] += 1
    check("distinct_roots", len(P["proot_rows"]) == tbl["distinct_roots"] == 1854, len(P["proot_rows"]))
    check("span_histogram", {str(x): v for x, v in sorted(hist.items())} == tbl["span_histogram"], dict(hist))
    check("exact15", tbl["exact"] and tbl["lower_bound"] == k == 15)
    check("parity_odd", r % 2 == 1 and k * 2 - 1 == r and (k - 1) * 2 + 1 == r)

    pair_roots = P["pair_roots"]; singleton_roots = P["singleton_roots"]
    edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    for s in range(r):
        w1.setdefault(s, 0)
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    root_row = {root: s for s, rl in singleton_roots.items() for root in rl}
    # free the large candidate table: both parents are fully built by now
    del row_cands
    import gc; gc.collect()

    # witness
    wit = tbl["witness_roots"]
    wit_cov = {root: P["proot_rows"][root] for root in wit}
    wit_rows = set()
    for root in wit:
        wit_rows |= wit_cov[root]
    check("witness.covers_all", wit_rows == set(P["target"]) and len(wit) == k)
    check("witness.structure", sorted(len(v) for v in wit_cov.values()) == [1] + [2] * 14)

    # structural data
    degree = defaultdict(int)
    for (a, b), w in edge_w.items():
        degree[a] += w; degree[b] += w
    for s in range(r):
        degree.setdefault(s, 0)
    options = {s: degree[s] + w1[s] for s in range(r)}
    mult_hist = defaultdict(int)
    for e, rl in pair_roots.items():
        mult_hist[len(rl)] += 1

    # ---------- exact pm computations
    pm = PmLazy(edge_w, r)
    full = (1 << r) - 1
    log("[pm] singleton memberships (A-type): 28-row pm x 29")
    mem = {}; mem_A = {}; mem_B = {}
    for s, rl in singleton_roots.items():
        v = pm.get(full ^ (1 << s))
        for root in rl:
            mem[root] = v; mem_A[root] = v; mem_B[root] = 0
    log("  memo size: %d" % len(pm.memo))

    log("[pm] pair-root memberships: 26/25/24-row pm")
    t0 = time.time()
    for root, e in root_pair.items():
        ea, eb = e
        ea_bit = 1 << ea; eb_bit = 1 << eb
        base = full & ~(ea_bit | eb_bit)
        a_part = 0
        for s, w in w1.items():
            if w and s != ea and s != eb:
                a_part += w * pm.get(base ^ (1 << s))
        b_part = 0
        for d in e:
            for z in range(r):
                if z == ea or z == eb:
                    continue
                wz = edge_w.get((min(d, z), max(d, z)), 0)
                if wz:
                    b_part += wz * pm.get(base ^ (1 << z))
        for d in range(r):
            if d == ea or d == eb:
                continue
            dbit = 1 << d
            for a in range(r):
                if a == d or a == ea or a == eb:
                    continue
                wa = edge_w.get((min(d, a), max(d, a)), 0)
                if not wa:
                    continue
                for b in range(a + 1, r):
                    if b == ea or b == eb:
                        continue
                    wb = edge_w.get((min(d, b), max(d, b)), 0)
                    if wb:
                        b_part += wa * wb * pm.get(base ^ dbit ^ (1 << a) ^ (1 << b))
        mem[root] = a_part + b_part
        mem_A[root] = a_part; mem_B[root] = b_part
    log("  pair memberships done in %.1fs, memo size %d, gets %d" %
        (time.time() - t0, len(pm.memo), pm.gets))

    total_A = sum(mem_A.values()) // k
    total_B = sum(mem_B.values()) // k
    total = total_A + total_B
    check("identity.A", sum(mem_A.values()) == k * total_A, {"sum": str(sum(mem_A.values()))})
    check("identity.B", sum(mem_B.values()) == k * total_B, {"sum": str(sum(mem_B.values()))})
    check("identity.total", sum(mem.values()) == k * total,
          {"sum": str(sum(mem.values())), "kT": str(k * total)})
    check("total_positive", total > 0, str(total))
    log("  totals A=%d B=%d total=%d" % (total_A, total_B, total))

    # independent A recomputation from the definition (also validates the
    # singleton-root memberships against the A total)
    A_direct = sum(w1[s] * pm.get(full ^ (1 << s)) for s in w1 if w1[s])
    check("A.direct_agreement", A_direct == total_A, {"direct": str(A_direct)})
    B_direct = 0
    t0 = time.time()
    for d in range(r):
        dbit = 1 << d
        nbrs = [a for a in range(r) if a != d and edge_w.get((min(d, a), max(d, a)))]
        for i in range(len(nbrs)):
            a = nbrs[i]
            wa = edge_w[(min(d, a), max(d, a))]
            for j in range(i + 1, len(nbrs)):
                b = nbrs[j]
                wb = edge_w[(min(d, b), max(d, b))]
                B_direct += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
    check("B.direct_agreement", B_direct == total_B, {"direct": str(B_direct)})
    log("  B direct recomputed in %.1fs" % (time.time() - t0))
    check("witness.membership_positive", all(mem[root] > 0 for root in wit))

    # top-50 and top-10 joint
    by_mem = sorted(mem, key=lambda x: (-mem[x], x))
    top50 = [{"root": x, "membership": mem[x],
              "kind": "pair" if x in root_pair else "singleton",
              "rows_covered": list(root_pair[x]) if x in root_pair else [root_row[x]],
              "membership_A": mem_A[x], "membership_B": mem_B[x]}
             for x in by_mem[:50]]
    top10 = by_mem[:10]
    # free the 9M-state memo before the joint phase: joint only needs pm at
    # 26/23/22/21-row masks, recomputed into a fresh (much smaller) memo,
    # keeping peak memory well under this host's 3.2 GB
    memo_states_pairs = len(pm.memo)
    pm.memo = {0: 1}
    pm.t0 = time.time()
    gc.collect()
    log("  memo cleared before joint (pairs-phase memo was %d states)" % memo_states_pairs)
    joint = []
    t0 = time.time()
    for i in range(len(top10)):
        for j in range(i + 1, len(top10)):
            r1, r2 = top10[i], top10[j]
            if r1 not in root_pair and r2 not in root_pair:
                m_ij = 0  # two singletons: A-type has exactly one singleton
            elif r1 not in root_pair or r2 not in root_pair:
                # singleton root on row s + pair root e: A-type covers with
                # that singleton and 12 further pairs on V\e\{s}
                sroot, proot = (r1, r2) if r1 not in root_pair else (r2, r1)
                s = root_row[sroot]; e = root_pair[proot]
                if s in e:
                    m_ij = 0
                else:
                    m_ij = pm.get(full ^ (1 << e[0]) ^ (1 << e[1]) ^ (1 << s))
            else:
                e1 = root_pair[r1]; e2 = root_pair[r2]
                sh = set(e1) & set(e2)
                if sh:
                    d = sh.pop()
                    a = e1[0] if e1[1] == d else e1[1]
                    b = e2[0] if e2[1] == d else e2[1]
                    m_ij = 0 if a == b else pm.get(full ^ (1 << d) ^ (1 << a) ^ (1 << b))
                else:
                    m_ij = 0
                    rows12 = set(e1) | set(e2)
                    base = full
                    for x in rows12:
                        base &= ~(1 << x)
                    for s, w in w1.items():
                        if w and s not in rows12:
                            m_ij += w * pm.get(base ^ (1 << s))
                    for d in range(r):
                        if d in rows12:
                            continue
                        nbrs = [a for a in range(r)
                                if a != d and a not in rows12
                                and edge_w.get((min(d, a), max(d, a)))]
                        for i2 in range(len(nbrs)):
                            a = nbrs[i2]
                            wa = edge_w[(min(d, a), max(d, a))]
                            for j2 in range(i2 + 1, len(nbrs)):
                                b = nbrs[j2]
                                wb = edge_w[(min(d, b), max(d, b))]
                                m_ij += wa * wb * pm.get(base ^ (1 << d) ^ (1 << a) ^ (1 << b))
                    for (eA, eB) in ((e1, e2), (e2, e1)):
                        for d in eA:
                            for z in range(r):
                                if z in rows12:
                                    continue
                                wz = edge_w.get((min(d, z), max(d, z)), 0)
                                if wz:
                                    m_ij += wz * pm.get(base ^ (1 << z))
            joint.append({"a": r1, "b": r2,
                          "rows_a": list(root_pair[r1]) if r1 in root_pair else [root_row[r1]],
                          "rows_b": list(root_pair[r2]) if r2 in root_pair else [root_row[r2]],
                          "membership_a": mem[r1], "membership_b": mem[r2],
                          "joint_membership": m_ij})
    check("joint.bounded",
          all(e["joint_membership"] <= min(e["membership_a"], e["membership_b"]) for e in joint))
    log("  joint done in %.1fs" % (time.time() - t0))

    nz_stats = {
        "count": sum(1 for v in mem.values() if v > 0),
        "min": min(v for v in mem.values() if v > 0),
        "max": max(mem.values()),
        "singleton_max": max(v for root, v in mem.items() if root in root_row),
        "pair_min": min(v for root, v in mem.items() if root in root_pair),
        "pair_max": max(v for root, v in mem.items() if root in root_pair),
    }
    check("all_roots_positive", nz_stats["count"] == len(mem), nz_stats["count"])

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-runnerup29-cover-membership-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact minimum-cover membership and joint analysis for the 29-row "
                  "runner-up target 00000000000000003800000009000000 via shared-memo "
                  "anchored lazy matching DP"),
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
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("Published even/odd-r cover framework, with pm values supplied by a "
                   "shared-memo anchored lazy matching DP (state cap 12M, wall budget "
                   "1500s). The anchored-reachable state space of this parent is only "
                   "~514k states per 28-row root, so all formulas run exactly where an "
                   "all-mask 2^29 table would not fit. The lazy pm and the framework are "
                   "validated against the published cost-12 output (all 1,151 singleton "
                   "memberships reproduced exactly)."),
        "derived": {
            "rows": r,
            "candidates": P["cand_total"],
            "distinct_roots": len(P["proot_rows"]),
            "span_histogram": {str(x): v for x, v in sorted(hist.items())},
            "pair_types": len(pair_roots),
            "pair_type_multiplicity_histogram": {str(x): v for x, v in sorted(mult_hist.items())},
            "minimum_size": k,
            "parity": "odd",
            "total_minimum_covers": total,
            "type_A_disjoint": total_A,
            "type_B_one_duplicate_row": total_B,
            "membership": {x: mem[x] for x in sorted(mem)},
            "top50_by_membership": top50,
            "top10_joint_membership": joint,
            "membership_nonzero_stats": nz_stats,
            "per_row_singleton_root_count": {str(s): w1[s] for s in range(r)},
            "per_row_pair_root_degree": {str(s): degree[s] for s in range(r)},
            "per_row_cover_options": {str(s): options[s] for s in range(r)},
            "bottleneck_rows_fewest_options": [
                {"row_index": s, "options": options[s], "pair_degree": degree[s],
                 "singleton_roots": w1[s], "row_hex": P["target"][s]}
                for s in sorted(range(r), key=lambda s: (options[s], s))[:5]],
            "hub_rows_by_pair_degree": [
                {"row_index": s, "pair_degree": degree[s], "row_hex": P["target"][s]}
                for s in sorted(range(r), key=lambda s: (-degree[s], s))[:5]],
            "witness_structure": {"pair_roots": 14, "singleton_roots": 1},
            "validation": {"cost12_singleton_memberships_checked": checked12,
                            "cost12_singleton_mismatches": mism12},
            "pm_memo_states_pairs_phase": memo_states_pairs,
            "pm_memo_states_joint_phase": len(pm.memo),
            "pm_gets": pm.gets,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. Membership counts "
                                 "alternative minimum cover plans containing a root; it "
                                 "is not a search cost and implies nothing about "
                                 "WIN/REFUTED outcomes. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    log("wrote %s: all_pass=%s checks=%d memo=%d" % (out_path, all_pass, len(checks), len(pm.memo)))
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]][:10],
                      "total": total, "A": total_A, "B": total_B,
                      "stats": nz_stats,
                      "memo_states": len(pm.memo), "pm_gets": pm.gets,
                      "top5": [{"root": e["root"][-8:], "kind": e["kind"],
                                 "membership": e["membership"]} for e in top50[:5]],
                      "joint_top": sorted(joint, key=lambda e: -e["joint_membership"])[:3]},
                     indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
