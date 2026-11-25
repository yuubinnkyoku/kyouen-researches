#!/usr/bin/env python3
"""Exact ban-survival curve for the runner-up cover target
00000000000000003800000009000000 (29 rows, minimum cover cost 15).

For k in [0,1,2,3,4,5,6,7,8,10,12], ban the k pair roots with the highest
published membership (from the published membership output, blob 05f54eb5),
i.e. decrement each banned root's pair-type multiplicity (all
multiplicities are 1 here, so the type is deleted), and exactly recompute

  A_k = sum_s w1(s) * pm_k(V\\{s})                       (A-type covers)
  B_k = sum_d sum_{a<b} w(d,a) w(d,b) pm_k(V\\{d,a,b})   (B-type covers)

with a fresh shared-memo anchored lazy matching DP (PmLazy) per point.

Independent validations:
  k=0: total must equal the published 45,949,721,018,967,524 exactly.
  k=1: survival must equal total - membership(top1) exactly.
  k=2: survival must equal total - (mem1 + mem2 - joint(top1, top2)) using
       the published joint membership.
  monotonicity: strictly decreasing (every banned root has positive
       membership, all covers containing it are removed).
"""
import json, os, sys, hashlib, time, gc
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
TARGET = "00000000000000003800000009000000"
BAN_POINTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
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

N = 11
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

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "runnerup29-ban-survival-curve-20261118.json")
    def log(msg):
        print(msg, flush=True)
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    table = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
        "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    pub = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
        "05f54eb58baad66403b327696b9a63f7433a13c3"))

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e

    p_orbit = {format(m, "032x") for m in orbit_masks(int(TARGET, 16))}
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
    del row_cands
    gc.collect()
    r = len(target)
    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)
    for root, cov in proot_rows.items():
        if len(cov) == 2:
            a, b = sorted(idx[h] for h in cov)
            pair_roots[(a, b)].append(root)
        else:
            (s,) = [idx[h] for h in cov]
            singleton_roots[s].append(root)
    edge_w0 = {e: len(rl) for e, rl in pair_roots.items()}
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    for s in range(r):
        w1.setdefault(s, 0)
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    check("rows", r == 29, r)
    check("candidates", cand_total == 2203, cand_total)
    check("roots", len(proot_rows) == 1854, len(proot_rows))
    check("all_pair_types_mult1", all(w == 1 for w in edge_w0.values())
          and len(edge_w0) == 349, {"types": len(edge_w0)})

    # published values and ban ranking
    pub_mem = pub["derived"]["membership"]
    pub_total = pub["derived"]["total_minimum_covers"]
    pub_A = pub["derived"]["type_A_disjoint"]
    pub_B = pub["derived"]["type_B_one_duplicate_row"]
    check("published_total", pub_total == 45949721018967524, str(pub_total))
    by_mem = sorted(pub_mem, key=lambda x: (-pub_mem[x], x))
    top12 = by_mem[:12]
    check("ban_set_all_pair_roots", all(x in root_pair for x in top12),
          [x for x in top12 if x not in root_pair])
    # membership of each banned root under the fresh build must match published
    # (weak structural check: same roots, same pair types)
    check("ban_roots_in_parent", all(x in proot_rows for x in top12))
    pub_joint = pub["derived"]["top10_joint_membership"]
    joint12 = None
    for e in pub_joint:
        pair = {e["a"], e["b"]}
        if pair == {top12[0], top12[1]}:
            joint12 = e["joint_membership"]
    check("joint_top2_found", joint12 is not None)

    full = (1 << r) - 1
    results = []
    t_start = time.time()
    for k in BAN_POINTS:
        edge_w = dict(edge_w0)
        banned = top12[:k]
        for root in banned:
            e = root_pair[root]
            if edge_w[e] <= 0:
                raise SystemExit("ban underflow at " + root)
            edge_w[e] -= 1
        pm = PmLazy(edge_w, r)
        t0 = time.time()
        A = 0
        for s in range(r):
            w = w1[s]
            if w:
                A += w * pm.get(full ^ (1 << s))
        B = 0
        for d in range(r):
            dbit = 1 << d
            nbrs = [a for a in range(r) if a != d and edge_w.get((min(d, a), max(d, a)))]
            for i in range(len(nbrs)):
                a = nbrs[i]
                wa = edge_w[(min(d, a), max(d, a))]
                for j in range(i + 1, len(nbrs)):
                    b = nbrs[j]
                    wb = edge_w[(min(d, b), max(d, b))]
                    B += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
        total = A + B
        results.append({"k": k, "banned_roots": banned,
                        "type_A": A, "type_B": B, "total": total,
                        "kill_share": None,  # filled below, keep deterministic
                        "memo_states": len(pm.memo), "pm_gets": pm.gets})
        log("k=%2d total=%d memo=%d gets=%d (%.1fs)" %
            (k, total, len(pm.memo), pm.gets, time.time() - t0))
        del pm
        gc.collect()
    log("all points done in %.1fs" % (time.time() - t_start))

    total0 = results[0]["total"]
    check("baseline_reproduces_published", total0 == pub_total,
          {"recomputed": str(total0), "published": str(pub_total)})
    check("baseline_split", results[0]["type_A"] == pub_A and results[0]["type_B"] == pub_B)
    surv1 = total0 - pub_mem[top12[0]]
    check("k1_independence", results[1]["total"] == surv1,
          {"recomputed": str(results[1]["total"]), "total_minus_mem": str(surv1)})
    surv2 = total0 - (pub_mem[top12[0]] + pub_mem[top12[1]] - joint12)
    check("k2_independence", results[2]["total"] == surv2,
          {"recomputed": str(results[2]["total"]), "incl_excl": str(surv2)})
    mono = all(results[i]["total"] > results[i + 1]["total"]
               for i in range(len(results) - 1))
    check("strictly_decreasing", mono,
          [str(x["total"]) for x in results])
    for e in results:
        e["kill_share"] = 1.0 if total0 == 0 else round(
            (total0 - e["total"]) / total0, 6)
    check("kill_shares_monotone", all(
        results[i]["kill_share"] <= results[i + 1]["kill_share"]
        for i in range(len(results) - 1)))
    # the naive membership-sum bound vs exact survival
    naive = {"k": 12, "sum_membership_top12": sum(pub_mem[x] for x in top12),
             "sum_share_of_total": round(sum(pub_mem[x] for x in top12) / total0, 6),
             "exact_survival_share": round(results[-1]["total"] / total0, 6)}
    check("k12_union_bound", results[-1]["total"] >= total0 - naive["sum_membership_top12"],
          {"exact": str(results[-1]["total"]),
           "union_bound": str(total0 - naive["sum_membership_top12"])})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-runnerup29-ban-survival-curve-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact ban-survival curve for the 29-row runner-up target "
                  "00000000000000003800000009000000 (ban top-k membership pair roots, "
                  "recompute exact A/B minimum cover totals)"),
        "inputs": {
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                             "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "published_membership_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
                                             "git_blob_sha1": "05f54eb58baad66403b327696b9a63f7433a13c3"},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("For each k, the top-k membership pair roots (published ranking) are "
                   "banned by deleting their pair type (all multiplicities are 1), and the "
                   "exact A-type and B-type minimum cover totals are recomputed from "
                   "scratch with a fresh shared-memo anchored lazy matching DP. k=0 "
                   "reproduces the published total; k=1 and k=2 match the "
                   "membership/inclusion-exclusion predictions from the published "
                   "membership and joint values, giving two independent validations of "
                   "the ban machinery."),
        "derived": {
            "rows": r,
            "ban_points": BAN_POINTS,
            "baseline_total": total0,
            "curve": results,
            "naive_membership_sum_vs_exact": naive,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. The survival curve "
                                 "counts alternative minimum cover plans avoiding the "
                                 "banned roots; it is not a search cost and implies "
                                 "nothing about WIN/REFUTED verdicts of the banned "
                                 "roots. REFUTED-D10 and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    log("wrote %s: all_pass=%s checks=%d" % (out_path, all_pass, len(checks)))
    print(json.dumps({"all_pass": all_pass,
                      "failed": [c["name"] for c in checks if not c["pass"]],
                      "curve": [{"k": e["k"], "total": e["total"],
                                 "kill%": round(100 * e["kill_share"], 3)}
                                for e in results],
                      "naive": naive},
                     indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
