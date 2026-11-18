#!/usr/bin/env python3
"""Extension of the joint certificate-cover sharing analysis to the five
cheapest cover targets, including the 31-row cost-16 parent.

The published joint-parent-cover-sharing analysis covered the four cheapest
parents (individual exact minimum cover costs 6 / 9 / 12 / 15) and used a
restarted greedy matching plus a greedy fallback to exhibit witnesses. This
extension adds the cost-16 parent 00000000000000003800000008001000 (31 target
rows, individual exact cost 16) and replaces the witness search with an exact
determination: since every candidate root covers at most 2 target rows
(span <= 2 in every subset universe), the minimum certificate-cover size
equals r - m where r is the number of target rows and m is the maximum
matching of the pair graph (rows as vertices, edge {a,b} iff some root covers
exactly {a,b} within the subset universe). The bound size >= r - m holds
because the 2-roots of any cover contain a matching of size at least
|V(H)| - m... more directly: a cover with k2 2-roots and k1 1-roots satisfies
k2 + k1 >= r - m (extract a maximal vertex-disjoint pair set from the cover
and charge the remaining rows); achievability takes the maximum matching
pairs (one witness root each) plus one arbitrary covering root per unmatched
row. The maximum matching is computed with a self-contained blossom
algorithm validated in-script against brute force on 3000 deterministic
random graphs.

Cross-validation: for all 15 subsets of the original four parents the exact
size must equal the published witness size (the published analysis marked
all of them exact), independently confirming the published output.

Bookkeeping and combinatorics only: cover semantics (a root covers a row iff
the row generates the root as a 1-stone D4-canonical extension) presume the
chosen roots would validate as certificates; this is planning arithmetic, not
a WIN/REFUTED claim.
"""
import json, os, sys, hashlib, random, itertools
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11

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

def canon_hex(mask):
    best = None
    for to in TO:
        out = 0
        for i in range(121):
            if (mask >> i) & 1:
                qx, qy = to[i]
                out |= 1 << (qy * N + qx)
        if best is None or out < best:
            best = out
    return format(best, "032x")

PARENTS = [
    ("00000000000000403800000008000000", 6),
    ("00000000000000821082000000000000", 9),
    ("00000000000000003800000008002000", 12),
    ("00000000000000003800000009000000", 15),
    ("00000000000000003800000008001000", 16),
]

# ---------------------------------------------------------------------------
# blossom maximum matching (general graph), e-maxx style, with in-script
# validation against brute force on small deterministic random graphs
# ---------------------------------------------------------------------------

def max_matching(n, adj):
    """Returns (size, mate) with mate[i] = j or -1."""
    match = [-1] * n
    p = [-1] * n
    base = list(range(n))
    blossom = [False] * n

    def lca(a, b):
        used_l = [False] * n
        while True:
            a = base[a]
            used_l[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if used_l[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, child):
        while base[v] != b:
            blossom[base[v]] = True
            blossom[base[match[v]]] = True
            p[v] = child
            child = match[v]
            v = p[match[v]]

    def find_path(root):
        used = [False] * n
        for i in range(n):
            p[i] = -1
            base[i] = i
        used[root] = True
        queue = [root]
        qi = 0
        while qi < len(queue):
            v = queue[qi]; qi += 1
            for to in adj[v]:
                if base[v] == base[to] or match[v] == to:
                    continue
                if to == root or (match[to] != -1 and p[match[to]] != -1):
                    curbase = lca(v, to)
                    for i in range(n):
                        blossom[i] = False
                    mark_path(v, curbase, to)
                    mark_path(to, curbase, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = curbase
                            if not used[i]:
                                used[i] = True
                                queue.append(i)
                elif p[to] == -1:
                    p[to] = v
                    if match[to] == -1:
                        u = to
                        while u != -1:
                            pv = p[u]; ppv = match[pv]
                            match[u] = pv
                            match[pv] = u
                            u = ppv
                        return True
                    else:
                        used[match[to]] = True
                        queue.append(match[to])
        return False

    res = 0
    for v in range(n):
        if match[v] == -1:
            if find_path(v):
                res += 1
    return res, match

def brute_force_matching(n, edges):
    best = 0
    edges = list(edges)
    def rec(i, used, cnt):
        nonlocal best
        if cnt + (len(edges) - i) <= best:
            return
        if i == len(edges):
            best = max(best, cnt)
            return
        a, b = edges[i]
        rec(i + 1, used, cnt)
        if a not in used and b not in used:
            used.add(a); used.add(b)
            rec(i + 1, used, cnt + 1)
            used.remove(a); used.remove(b)
    rec(0, set(), 0)
    return best

def blossom_selftest(trials=3000):
    rng = random.Random(20261118)
    fails = 0
    for _ in range(trials):
        n = rng.randint(1, 9)
        m = rng.randint(0, min(12, n * (n - 1) // 2) if n > 1 else 0)
        edge_set = set()
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
        while len(edge_set) < m and pairs:
            edge_set.add(rng.choice(pairs))
        edges = sorted(edge_set)
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b); adj[b].append(a)
        got, mate = max_matching(n, adj)
        exp = brute_force_matching(n, edges)
        valid = True
        npairs = 0
        for i in range(n):
            if mate[i] != -1:
                if mate[mate[i]] != i or (min(i, mate[i]), max(i, mate[i])) not in edge_set:
                    valid = False
                if i < mate[i]:
                    npairs += 1
        if npairs != got or got != exp or not valid:
            fails += 1
    return trials, fails

# ---------------------------------------------------------------------------

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "joint-parent-cover-sharing-cost16-20261118.json")
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    wl = read_pinned("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                     "2fee1d0718547a62e346d35f5858d7913e37c097").decode().rstrip("\r\n").split("\n")
    headers = [h.strip() for h in wl[0].split(",")]
    rows = {}
    for line in wl[1:]:
        vals = line.split(",")
        r = {h: (vals[i].strip() if i < len(vals) else "") for i, h in enumerate(headers)}
        rows[r["s6_canonical_hex"]] = r
    cen = json.loads(read_pinned("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                                 "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"))
    led = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                                 "e8785d509e8a11a37c0d03cc450455a14708c34d"))
    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                                   "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    pub = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-20261118.json",
                                 "f1a4783292897a6e9128dc1a5718617a33b119a1"))
    jsonl_path = os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")
    with open(jsonl_path, "rb") as f:
        jsonl_data = f.read()
    jsonl_pin = git_blob_sha(jsonl_data)
    check("jsonl.pin", jsonl_pin == "89b24065d0588b0891395c9283e3a5b3d5551595", jsonl_pin)
    row_cands = {}
    for line in jsonl_data.decode().splitlines():
        e = json.loads(line)
        row_cands[e["row"]] = e

    trials, fails = blossom_selftest(3000)
    check("blossom.selftest", fails == 0, {"graphs": trials, "failures": fails})

    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}
    all_open = sorted(h for h in rows if h not in closed and h not in sterile)
    check("universe.rows", len(all_open) == len(row_cands) == 6337,
          {"worklist_open": len(all_open), "jsonl_rows": len(row_cands)})

    row_parents = {}
    for h in row_cands:
        m = int(h, 16)
        bits = [i for i in range(121) if (m >> i) & 1]
        row_parents[h] = {canon_hex(m ^ (1 << b)) for b in bits}

    targets = {ph: set(sorted(h for h in row_cands if ph in row_parents[h])) for ph, _ in PARENTS}
    tbl = {e["hex"]: e for e in table["derived"]["table"]}
    for ph, cost in PARENTS:
        check("table.%s" % ph[-8:],
              tbl[ph]["witness_size"] == cost and tbl[ph]["exact"] and tbl[ph]["rows_r"] == len(targets[ph]),
              {"cost": tbl[ph]["witness_size"], "rows_r": tbl[ph]["rows_r"], "targets": len(targets[ph])})
    cheapest5 = sorted((e for e in table["derived"]["table"] if e["rows_r"] > 0),
                       key=lambda e: (e["witness_size"], e["hex"]))[:5]
    check("selection.cheapest5", {e["hex"] for e in cheapest5} == {ph for ph, _ in PARENTS},
          [(e["hex"], e["witness_size"]) for e in cheapest5])
    union_all = set().union(*[targets[ph] for ph, _ in PARENTS])
    check("targets.disjoint", len(union_all) == sum(len(targets[ph]) for ph, _ in PARENTS) == 112,
          {"union": len(union_all),
           "sum": sum(len(targets[ph]) for ph, _ in PARENTS)})

    pubres = {tuple(sorted(r["subset"])): r for r in pub["derived"]["joint_results"]}

    def joint(subset):
        tset_all = sorted({h for ph in subset for h in targets[ph]})
        tset = set(tset_all)
        idx = {h: i for i, h in enumerate(tset_all)}
        proot_rows = defaultdict(set)
        cand_total = 0
        for h in tset_all:
            e = row_cands[h]
            cand_total += e["cost"]
            for root, bit in e["cands"]:
                proot_rows[root].add(h)
        hist = defaultdict(int)
        for root, cov in proot_rows.items():
            hist[len(cov)] += 1
        maxspan = max(hist) if hist else 0
        r = len(tset_all)
        lb = (r + maxspan - 1) // maxspan if maxspan else 0
        if maxspan > 2:
            raise SystemExit("span > 2 in subset " + ",".join(subset) + ": exact formula not applicable")
        cross_roots = []
        for root, cov in proot_rows.items():
            phs = {ph for ph in subset if cov & targets[ph]}
            if len(phs) >= 2:
                cross_roots.append(root)
        cross_roots = sorted(cross_roots)
        pair_edges = defaultdict(list)
        for root, cov in proot_rows.items():
            if len(cov) == 2:
                a, b = sorted(cov)
                pair_edges[(a, b)].append(root)
        covered = set()
        for root, cov in proot_rows.items():
            covered |= cov
        if covered != tset:
            return {"subset": list(subset), "rows_union": r, "candidates": cand_total,
                    "distinct_roots": len(proot_rows),
                    "span_histogram": {str(k): v for k, v in sorted(hist.items())},
                    "maxspan": maxspan, "lower_bound": lb,
                    "max_matching": None, "witness_size": None, "exact": False,
                    "method": "no_cover", "cross_parent_roots": len(cross_roots),
                    "witness_roots": []}
        adj = [[] for _ in range(r)]
        for (a, b) in sorted(pair_edges):
            adj[idx[a]].append(idx[b])
            adj[idx[b]].append(idx[a])
        m, mate = max_matching(r, adj)
        exact_size = r - m
        witness = []
        for i in range(r):
            if mate[i] != -1 and i < mate[i]:
                a, b = tset_all[i], tset_all[mate[i]]
                witness.append(sorted(pair_edges[(a, b)])[0])
        for i in range(r):
            if mate[i] == -1:
                h = tset_all[i]
                sroots = sorted(root for root, cov in proot_rows.items() if h in cov)
                witness.append(sroots[0])
        wit_cov = set()
        for root in witness:
            wit_cov |= proot_rows[root]
        tag = "-".join(ph[-6:] for ph in subset)
        check("joint.covers.%s" % tag, wit_cov == tset)
        check("joint.distinct.%s" % tag, len(set(witness)) == len(witness) == exact_size,
              {"size": len(witness), "r_minus_m": exact_size})
        exact = exact_size == lb
        return {
            "subset": list(subset),
            "rows_union": r,
            "candidates": cand_total,
            "distinct_roots": len(proot_rows),
            "span_histogram": {str(k): v for k, v in sorted(hist.items())},
            "maxspan": maxspan,
            "lower_bound": lb,
            "max_matching": m,
            "witness_size": exact_size,
            "exact": exact,
            "method": "edge_cover_from_blossom_matching",
            "cross_parent_roots": len(cross_roots),
            "witness_roots": sorted(witness),
        }

    results = []
    for k in range(1, 6):
        for combo in itertools.combinations([ph for ph, _ in PARENTS], k):
            res = joint(combo)
            indiv = sum(dict(PARENTS)[ph] for ph in combo)
            res["sum_individual_costs"] = indiv
            res["sharing_benefit"] = indiv - res["witness_size"]
            results.append(res)

    # cross-validation against the published 4-parent analysis
    for k in range(1, 5):
        for combo in itertools.combinations([ph for ph, _ in PARENTS[:4]], k):
            res = next(r for r in results if tuple(sorted(r["subset"])) == tuple(sorted(combo)))
            pr = pubres[tuple(sorted(combo))]
            check("crosscheck.pub.%s" % "-".join(ph[-6:] for ph in combo),
                  res["witness_size"] == pr["witness_size"] and pr["exact"] and res["exact"],
                  {"mine": res["witness_size"], "published": pr["witness_size"]})

    # cost-16 singleton reproduces the published cover-table entry
    c16 = "00000000000000003800000008001000"
    res16 = next(r for r in results if r["subset"] == [c16])
    check("cost16.singleton", res16["witness_size"] == 16 and res16["exact"] and res16["sharing_benefit"] == 0,
          {"size": res16["witness_size"], "exact": res16["exact"]})

    # headline: the 5-way joint
    quad5 = next(r for r in results if len(r["subset"]) == 5)
    check("quint.exact", quad5["exact"])
    check("quint.rows", quad5["rows_union"] == 112, quad5["rows_union"])
    check("quint.benefit", quad5["sharing_benefit"] == 2,
          {"joint": quad5["witness_size"], "individual_sum": quad5["sum_individual_costs"]})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-joint-parent-cover-sharing-cost16-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Joint minimum certificate-cover cost for subsets of the five cheapest cover targets (cost-16 parent extension, exact edge-cover determination)",
        "inputs": {
            "worklist": {"path": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                         "git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"path": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                       "git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                       "git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                            "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "published_joint": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-20261118.json",
                               "git_blob_sha1": "f1a4783292897a6e9128dc1a5718617a33b119a1"},
            "candidate_roots_jsonl": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/global-candidate-roots-20261118.jsonl",
                                      "git_blob_sha1": "89b24065d0588b0891395c9283e3a5b3d5551595",
                                      "note": "deterministic artifact of the published enumerate_global_candidate_roots_20261118.py over the pinned worklist/census/ledger"},
        },
        "method": ("Same cover semantics as the published joint analysis: a root "
                   "covers the rows that generate it as a 1-stone D4-canonical "
                   "extension (phase-1 enumeration). Joint target = union of the "
                   "member parents' open non-STERILE rows. Every root covers at "
                   "most 2 rows in every subset universe (asserted), so the "
                   "minimum cover size equals r - m with m the maximum matching "
                   "of the pair graph; m is computed exactly with a self-contained "
                   "blossom algorithm validated against brute force on 3000 "
                   "deterministic random graphs, and the exhibited witness (one "
                   "root per matched pair plus one covering root per unmatched "
                   "row) is machine-verified. exact means witness size equals "
                   "ceil(r/maxspan). All 15 published 4-parent subset sizes are "
                   "reproduced as a cross-check."),
        "derived": {
            "parents": [{"hex": ph, "individual_cost": c} for ph, c in PARENTS],
            "joint_results": results,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Bookkeeping and combinatorics only. Joint cover "
                                 "cost presumes every chosen root would validate "
                                 "as a certificate; sharing benefit is a planning "
                                 "count, not a WIN/REFUTED claim. REFUTED-D10 and "
                                 "STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    slim = [{k: r[k] for k in ("subset", "rows_union", "maxspan", "lower_bound",
                                "max_matching", "witness_size", "exact",
                                "sum_individual_costs", "sharing_benefit",
                                "cross_parent_roots")} for r in results]
    print(json.dumps({"all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]][:10],
                      "results": slim}, indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
