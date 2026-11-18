#!/usr/bin/env python3
"""Third-implementation cross-check of the published joint certificate-cover
analysis for the five cheapest cover targets (commit 3a04ca5b, output blob
40581746dc3304bdaff4b1934fd6f1d3d2981ea5, 91 checks all PASS).

The published extension determines every joint minimum cover size exactly via
min-cover = r - max_matching (Gallai) with a self-contained blossom. This
cross-check is deliberately algorithm-independent:

1. Tutte-matrix rank (algebraic): max matching size = rank(T)/2 of the
   skew-symmetric random evaluation of the Tutte matrix over two different
   prime fields with independent deterministic LCG streams. Schwartz-Zippel
   error probability is << 1/p per field; agreement of both fields is checked.
2. Exact 2^r minimum-cover DP (combinatorial, uses no matching at all) for
   the subsets with r <= 18 rows, verifying the published witness size and
   the Gallai identity on real instances.
3. Full field-by-field comparison of all 31 published subset results
   (rows_union, candidates, distinct_roots, span_histogram, maxspan,
   lower_bound, max_matching, witness_size, exact, cross_parent_roots,
   sum_individual_costs, sharing_benefit, witness count) plus independent
   validation of every published witness (distinct, in-universe, covers all
   rows, count == r - m).
4. Independent re-derivation of the target universes from the pinned inputs
   (worklist/census/ledger + pinned candidate JSONL, D4 join), the cheapest-5
   selection from the cover table, target disjointness (112 rows), and
   reproduction of the 15 published 4-parent subset sizes.

Verification-side bookkeeping only: no engine run, no verdict.
"""
import json, os, sys, hashlib, itertools
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11

PARENTS = [
    ("00000000000000403800000008000000", 6),
    ("00000000000000821082000000000000", 9),
    ("00000000000000003800000008002000", 12),
    ("00000000000000003800000009000000", 15),
    ("00000000000000003800000008001000", 16),
]

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

class LCG:
    """Deterministic LCG, independent of host RNG/seed."""
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFFFFFFFFFF
    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return self.s >> 33
    def below(self, n):
        return self.next() % n

def rank_mod(a, p):
    """Rank of matrix a (list of lists) over GF(p). Destroys a."""
    n = len(a)
    m = len(a[0]) if n else 0
    piv_row = 0
    for c in range(m):
        piv = None
        for i in range(piv_row, n):
            if a[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        a[piv_row], a[piv] = a[piv], a[piv_row]
        inv = pow(a[piv_row][c], p - 2, p)
        row_p = a[piv_row]
        for i in range(piv_row + 1, n):
            row_i = a[i]
            if row_i[c] % p:
                f = row_i[c] * inv % p
                if f:
                    for j in range(c, m):
                        row_i[j] = (row_i[j] - f * row_p[j]) % p
        piv_row += 1
        if piv_row == n:
            break
    return piv_row

def tutte_matching(r, edges, p, seed):
    """Max matching size via rank of the skew-symmetric Tutte matrix
    evaluation over GF(p): T[a][b] = v, T[b][a] = -v for edge (a,b)."""
    rng = LCG(seed)
    t = [[0] * r for _ in range(r)]
    for (a, b) in edges:
        v = 1 + rng.below(p - 2)
        t[a][b] = v
        t[b][a] = (p - v) % p
    return rank_mod(t, p) // 2

def tutte_matching_two(r, edges):
    return (tutte_matching(r, edges, 1000000007, 0x5DEECE66D),
            tutte_matching(r, edges, 998244353, 0x2545F4914F6CDD1D))

def tutte_selftest(trials=500):
    """Validate the Tutte-rank matcher against brute-force maximum matching
    on small deterministic graphs (independent of the published blossom's
    3000-graph self-test stream)."""
    rng = LCG(0xC0FFEE123456)
    fails = 0
    for _ in range(trials):
        n = 2 + rng.below(7)
        ne = rng.below(11)
        edges = set()
        for _ in range(ne):
            a = rng.below(n)
            b = rng.below(n)
            if a != b:
                edges.add((min(a, b), max(a, b)))
        # brute force max matching
        best = 0
        elist = sorted(edges)
        def rec(i, used, cnt):
            nonlocal best
            best = max(best, cnt)
            if i == len(elist):
                return
            rec(i + 1, used, cnt)
            a, b = elist[i]
            if not (used >> a) & 1 and not (used >> b) & 1:
                rec(i + 1, used | (1 << a) | (1 << b), cnt + 1)
        rec(0, 0, 0)
        m1, m2 = tutte_matching_two(n, sorted(edges))
        if m1 != best or m2 != best or m1 != m2:
            fails += 1
    return trials, fails

def min_cover_dp_impl(r, single_set, pair_set):
    """Exact minimum number of roots covering all r rows (bitmask DP).
    single_set: row indices with >=1 singleton root. pair_set: (a,b) index
    pairs (a<b) with >=1 pair root. Uses no matching at all."""
    INF = 1 << 30
    dp = [INF] * (1 << r)
    dp[0] = 0
    full = (1 << r) - 1
    for mask in range(1, 1 << r):
        low = mask & -mask
        v = low.bit_length() - 1
        rest = mask ^ low
        best = INF
        if v in single_set and dp[rest] < INF:
            best = dp[rest] + 1
        mm = rest
        while mm:
            jbit = mm & -mm
            mm ^= jbit
            u = jbit.bit_length() - 1
            e = (v, u) if v < u else (u, v)
            if e in pair_set:
                sub = rest ^ jbit
                if dp[sub] < INF and dp[sub] + 1 < best:
                    best = dp[sub] + 1
        dp[mask] = best
    return dp[full]

def main():
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})
        print("  check %-52s %s" % (name, "PASS" if ok else "FAIL"), flush=True)

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
    pub4 = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-20261118.json",
                                  "f1a4783292897a6e9128dc1a5718617a33b119a1"))
    pub5 = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-cost16-20261118.json",
                                  "40581746dc3304bdaff4b1934fd6f1d3d2981ea5"))
    check("pub5.pin", True)
    jsonl_data = read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/global-candidate-roots-20261118.jsonl",
                             "89b24065d0588b0891395c9283e3a5b3d5551595")
    check("jsonl.pin", True)

    row_cands = {}
    for line in jsonl_data.decode().splitlines():
        e = json.loads(line)
        row_cands[e["row"]] = e

    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}
    all_open = sorted(h for h in rows if h not in closed and h not in sterile)
    check("universe.rows", len(all_open) == len(row_cands) == 6337,
          {"worklist_open": len(all_open), "jsonl_rows": len(row_cands)})

    trials, fails = tutte_selftest(500)
    check("tutte.selftest_vs_bruteforce", fails == 0,
          {"graphs": trials, "failures": fails})

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
          {"union": len(union_all), "sum": sum(len(targets[ph]) for ph, _ in PARENTS)})

    pubres4 = {tuple(sorted(r["subset"])): r for r in pub4["derived"]["joint_results"]}
    pubres5 = {tuple(sorted(r["subset"])): r for r in pub5["derived"]["joint_results"]}

    field_mismatch = []
    witnesses_bad = []
    dp_verified = []
    tutte_disagree = []
    subsets_compared = 0
    results = []
    for k in range(1, 6):
        for combo in itertools.combinations([ph for ph, _ in PARENTS], k):
            tset_all = sorted({h for ph in combo for h in targets[ph]})
            tset = set(tset_all)
            idx = {h: i for i, h in enumerate(tset_all)}
            r = len(tset_all)
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
            cross_roots = [root for root, cov in proot_rows.items()
                           if len({ph for ph in combo if cov & targets[ph]}) >= 2]
            pair_edges = sorted({tuple(sorted(cov)) for cov in proot_rows.values() if len(cov) == 2})
            covered = set()
            for cov in proot_rows.values():
                covered |= cov
            if covered != tset:
                field_mismatch.append(("uncovered", [ph[-6:] for ph in combo]))
                continue
            eidx = [(idx[a], idx[b]) for (a, b) in pair_edges]
            m1, m2 = tutte_matching_two(r, eidx)
            if m1 != m2:
                tutte_disagree.append((combo, m1, m2))
                continue
            exact_size = r - m1
            lb = (r + maxspan - 1) // maxspan
            pr = pubres5[tuple(sorted(combo))]
            subsets_compared += 1
            cmp = {
                "rows_union": r == pr["rows_union"],
                "candidates": cand_total == pr["candidates"],
                "distinct_roots": len(proot_rows) == pr["distinct_roots"],
                "span_histogram": {str(x): v for x, v in sorted(hist.items())} == pr["span_histogram"],
                "maxspan": maxspan == pr["maxspan"],
                "lower_bound": lb == pr["lower_bound"],
                "max_matching": m1 == pr["max_matching"],
                "witness_size": exact_size == pr["witness_size"],
                "exact": (exact_size == lb) == pr["exact"],
                "cross_parent_roots": len(cross_roots) == pr["cross_parent_roots"],
                "sum_individual_costs": sum(dict(PARENTS)[ph] for ph in combo) == pr["sum_individual_costs"],
                "sharing_benefit": (sum(dict(PARENTS)[ph] for ph in combo) - exact_size) == pr["sharing_benefit"],
                "witness_count": len(pr["witness_roots"]) == exact_size,
            }
            bad = [kk for kk, vv in cmp.items() if not vv]
            if bad:
                field_mismatch.append(([ph[-6:] for ph in combo], bad))
            wr = pr["witness_roots"]
            wit_ok = len(set(wr)) == len(wr)
            wit_cov = set()
            for root in wr:
                if root not in proot_rows:
                    wit_ok = False
                    break
                wit_cov |= proot_rows[root]
            if wit_ok and (wit_cov != tset or len(wr) != exact_size):
                wit_ok = False
            if not wit_ok:
                witnesses_bad.append([ph[-6:] for ph in combo])
            dp_res = None
            if r <= 18:
                single_set = {idx[h] for h in tset_all
                              if any(len(cov) == 1 and h in cov for cov in proot_rows.values())}
                pset = {(idx[a], idx[b]) for (a, b) in pair_edges}
                dp_res = min_cover_dp_impl(r, single_set, pset)
                dp_verified.append({"subset": [ph[-6:] for ph in combo], "r": r,
                                    "dp": dp_res, "gallai": exact_size,
                                    "published": pr["witness_size"]})
            results.append({"subset": [ph[-6:] for ph in combo], "r": r,
                            "tutte": [m1, m2], "exact_size": exact_size,
                            "dp": dp_res})

    check("joint.fields_31_subsets", not field_mismatch and subsets_compared == 31,
          {"compared": subsets_compared, "mismatches": field_mismatch[:5]})
    check("joint.tutte_two_fields_agree", not tutte_disagree, tutte_disagree[:3])
    check("joint.witnesses_valid", not witnesses_bad, witnesses_bad[:3])
    dp_ok = all(x["dp"] == x["published"] == x["gallai"] for x in dp_verified)
    check("dp.exact_agreement_r_le_18", dp_ok and len(dp_verified) == 2,
          {"verified": len(dp_verified), "detail": dp_verified})
    pub4_ok = True
    for k in range(1, 5):
        for combo in itertools.combinations([ph for ph, _ in PARENTS[:4]], k):
            pr5 = pubres5[tuple(sorted(combo))]
            pr4 = pubres4.get(tuple(sorted(combo)))
            if pr4 is None or pr5["witness_size"] != pr4["witness_size"] or not pr4.get("exact"):
                pub4_ok = False
    check("pub4.fifteen_subset_sizes_reproduced", pub4_ok)
    check("pub5.check_count_agrees", pub5.get("check_count") == 91 and pub5.get("all_pass") is True,
          {"check_count": pub5.get("check_count"), "all_pass": pub5.get("all_pass")})
    q5 = pubres5[tuple(sorted([ph for ph, _ in PARENTS]))]
    check("quint.headline", q5["witness_size"] == 56 and q5["sum_individual_costs"] == 58
          and q5["sharing_benefit"] == 2 and q5["rows_union"] == 112 and q5["exact"],
          {"joint": q5["witness_size"], "rows": q5["rows_union"], "benefit": q5["sharing_benefit"]})
    c16 = "00000000000000003800000008001000"
    r16 = pubres5[(c16,)]
    check("cost16.singleton_size", r16["witness_size"] == 16 and r16["exact"])

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-joint-cover-cost16-third-impl-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Third-implementation cross-check of the five-cheapest joint certificate-cover "
                  "analysis (commit 3a04ca5b): algorithm-independent determination of all 31 subset "
                  "minimum cover sizes via Tutte-matrix rank (two prime fields) plus exact 2^r DP "
                  "on the r <= 18 subsets, with full field comparison and witness validation"),
        "inputs": {
            "published_cost16_extension": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-cost16-20261118.json",
                                            "git_blob_sha1": "40581746dc3304bdaff4b1934fd6f1d3d2981ea5"},
            "published_4parent_joint": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-20261118.json",
                                        "git_blob_sha1": "f1a4783292897a6e9128dc1a5718617a33b119a1"},
            "cover_table": {"git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "candidate_roots_jsonl": {"git_blob_sha1": "89b24065d0588b0891395c9283e3a5b3d5551595"},
            "worklist": {"git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
        },
        "method": ("Independent re-derivation of all 31 subset universes from the pinned inputs; "
                   "max matching determined by randomized Tutte-matrix rank over GF(1000000007) and "
                   "GF(998244353) with independent deterministic LCG streams (algebraic method, "
                   "disjoint from the published blossom), self-tested against brute force on 500 "
                   "deterministic small graphs; minimum cover size r - m (Gallai) independently "
                   "confirmed on the two r <= 18 subsets by an exact 2^r bitmask minimum-cover DP "
                   "that uses no matching at all; every published witness validated for "
                   "distinctness, universe membership, count == r - m, and full row coverage; "
                   "all 31 published subset results compared field by field."),
        "derived": {
            "subsets": results,
            "dp_verified": dp_verified,
            "field_mismatches": field_mismatch,
            "witness_invalid": witnesses_bad,
            "tutte_field_disagreements": tutte_disagree,
            "subsets_compared": subsets_compared,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. Joint cover cost presumes every "
                                 "chosen root would validate as a certificate; sharing benefit is "
                                 "a planning count, not a WIN/REFUTED claim. REFUTED-D10 and "
                                 "STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    out_path = os.path.join(HERE, "output", "joint-cover-cost16-third-impl-crosscheck-20261118.json")
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=1) + "\n")
    print("wrote %s all_pass=%s checks=%d" % (out_path, all_pass, len(checks)))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
