#!/usr/bin/env python3
"""Cross-parent certificate sharing for the four cheapest cover targets.

For every nonempty subset of the four parents with the smallest exact minimum
certificate-cover cost (6 / 9 / 12 / 15), compute the joint minimum cover cost
over the union of their target rows, exactly (elementary incidence lower bound
ceil(r/maxspan) + machine-verified witness), and compare with the sum of the
individual costs. The difference is the certificate-sharing benefit of solving
the parents together. A root covers a row iff the row generates the root as a
1-stone D4-canonical extension (phase-1 enumeration), so cross-parent spans
are captured naturally.
"""
import json, os, sys, hashlib, random
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
]

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "joint-parent-cover-sharing-20261118.json")
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
    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json", "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}

    row_parents = {}
    for h in rows:
        m = int(h, 16)
        bits = [i for i in range(121) if (m >> i) & 1]
        row_parents[h] = {canon_hex(m ^ (1 << b)) for b in bits}

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e

    tbl = {e["hex"]: e for e in table["derived"]["table"]}
    for ph, cost in PARENTS:
        check("table.%s" % ph[-8:], tbl[ph]["witness_size"] == cost and tbl[ph]["exact"],
              {"cost": tbl[ph]["witness_size"]})
    # the four selected parents must be the four cheapest nonempty parents of the
    # published table
    cheapest = sorted((e for e in table["derived"]["table"] if e["rows_r"] > 0),
                      key=lambda e: (e["witness_size"], e["hex"]))[:4]
    check("selection.cheapest4", {e["hex"] for e in cheapest} == {ph for ph, _ in PARENTS},
          [(e["hex"], e["witness_size"]) for e in cheapest])
    targets = {ph: set(sorted(h for h in row_cands if ph in row_parents[h])) for ph, _ in PARENTS}
    for ph, _ in PARENTS:
        check("target.%s" % ph[-8:], len(targets[ph]) == tbl[ph]["rows_r"], len(targets[ph]))

    def joint(subset):
        tset_all = sorted({h for ph in subset for h in targets[ph]})
        tset = set(tset_all)
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
        # cross-parent span: roots covering rows of 2+ member parents
        cross_roots = []
        for root, cov in proot_rows.items():
            phs = {ph for ph in subset if cov & targets[ph]}
            if len(phs) >= 2:
                cross_roots.append(root)
        cross_roots = sorted(cross_roots)
        # witness: matching for maxspan<=2 else greedy
        witness = None
        method = None
        if maxspan <= 2:
            pair_edges = defaultdict(list)
            for root, cov in proot_rows.items():
                if len(cov) == 2:
                    a, b = sorted(cov)
                    pair_edges[(a, b)].append(root)
            rng = random.Random(20261118)
            edge_list = sorted(pair_edges)
            need = r // 2 if r % 2 == 0 else (r - 1) // 2
            best = None
            for trial in range(60):
                order = edge_list[:] if trial == 0 else rng.sample(edge_list, len(edge_list))
                matched = {}
                used = set()
                for (a, b) in order:
                    if a in used or b in used:
                        continue
                    matched[(a, b)] = pair_edges[(a, b)][0]
                    used.add(a); used.add(b)
                if best is None or len(matched) > len(best[0]):
                    best = (matched, used)
                if len(matched) == need:
                    best = (matched, used)
                    break
            matched, used = best
            if len(matched) == need:
                wit = [matched[k] for k in sorted(matched)]
                if r % 2 == 1:
                    leftover = [h for h in tset_all if h not in used]
                    if len(leftover) == 1:
                        lo = leftover[0]
                        sroots = [root for root, cov in proot_rows.items()
                                  if len(cov) == 1 and lo in cov]
                        if sroots:
                            wit.append(sorted(sroots)[0])
                            witness = wit
                            method = "matching_plus_singleton"
                else:
                    witness = wit
                    method = "perfect_matching"
        if witness is None:
            # greedy fallback
            uncovered = set(tset_all)
            wit = []
            rlist = sorted(proot_rows)
            ok = True
            while uncovered:
                bestg = None
                for root in rlist:
                    gain = len(proot_rows[root] & uncovered)
                    if gain and (bestg is None or gain > bestg[0]):
                        bestg = (gain, root)
                if bestg is None:
                    ok = False
                    break
                wit.append(bestg[1])
                uncovered -= proot_rows[bestg[1]]
            witness = wit if ok else None
            method = "greedy_cover" if ok else "no_cover"
        size = len(witness) if witness is not None else None
        exact = (r == 0) or (witness is not None and size == lb)
        if witness is not None:
            covered = set()
            for root in witness:
                covered |= proot_rows[root]
            check("joint.covers.%s" % "-".join(ph[-6:] for ph in subset), covered == tset)
            check("joint.distinct.%s" % "-".join(ph[-6:] for ph in subset),
                  len(set(witness)) == len(witness))
        return {
            "subset": list(subset),
            "rows_union": r,
            "candidates": cand_total,
            "distinct_roots": len(proot_rows),
            "span_histogram": {str(k): v for k, v in sorted(hist.items())},
            "maxspan": maxspan,
            "lower_bound": lb,
            "witness_size": size,
            "exact": exact,
            "method": method,
            "cross_parent_roots": len(cross_roots),
            "witness_roots": sorted(witness or []),
        }, proot_rows

    results = []
    import itertools
    for k in range(1, 5):
        for combo in itertools.combinations([ph for ph, _ in PARENTS], k):
            res, _ = joint(combo)
            indiv = sum(dict(PARENTS)[ph] for ph in combo)
            res["sum_individual_costs"] = indiv
            res["sharing_benefit"] = (indiv - res["witness_size"]) if res["witness_size"] is not None else None
            results.append(res)

    # headline: the 4-way joint
    quad = [r for r in results if len(r["subset"]) == 4][0]
    check("quad.exact", quad["exact"])
    check("quad.benefit", quad["sharing_benefit"] is not None and quad["sharing_benefit"] >= 0,
          {"joint": quad["witness_size"], "individual_sum": quad["sum_individual_costs"]})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-joint-parent-cover-sharing-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Joint minimum certificate-cover cost for subsets of the four cheapest cover targets (cross-parent certificate sharing)",
        "inputs": {
            "worklist": {"path": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                          "git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"path": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                        "git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                        "git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json", "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
        },
        "method": ("Same cover semantics as the published per-parent table: a root "
                   "covers the rows that generate it as a 1-stone D4-canonical "
                   "extension (phase-1 enumeration), so cross-parent spans appear "
                   "naturally. Joint target = union of member parents' open non-STERILE "
                   "rows; joint universe = candidates of those rows. Lower bound "
                   "ceil(r/maxspan); exact when a machine-verified witness of that "
                   "size is exhibited (deterministic greedy matching, 60 restarts)."),
        "derived": {
            "parents": [{"hex": ph, "individual_cost": c} for ph, c in PARENTS],
            "joint_results": results,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Bookkeeping and combinatorics only. Joint cover "
                                 "cost presumes every chosen root would validate as a "
                                 "certificate; sharing benefit is a planning count, "
                                 "not a WIN/REFUTED claim. REFUTED-D10 and STERILE "
                                 "are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    slim = [{k: r[k] for k in ("subset", "rows_union", "maxspan", "lower_bound",
                                "witness_size", "exact", "sum_individual_costs",
                                "sharing_benefit", "cross_parent_roots")} for r in results]
    print(json.dumps({"all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]][:10],
                      "results": slim}, indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
