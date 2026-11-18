#!/usr/bin/env python3
"""Phase 2: minimum certificate-cover cost table for all 174 open S5 parents,
on the post-fold-chain (head-1476) open non-STERILE row state.

For each parent P: target rows T = open rows whose 5-stone parent set contains
P. Candidate roots are the D4-canonical 7-stone extensions of T's own rows
(phase-1 JSONL). A root "covers" the rows of T it contains as a 1-stone-removal
child. A "certificate cover" of P is a set of roots covering all rows of T.

Exactness: every root covers at most maxspan rows, so any cover has size >=
ceil(r / maxspan) (elementary incidence bound). If a witness of that size is
exhibited, the minimum is exactly ceil(r / maxspan). With maxspan <= 2 the
witness reduces to a matching problem (disjoint pair roots + singletons) and
greedy matching with deterministic restarts finds it for these dense graphs.
All bookkeeping; no engine run, no verdict, no closure claim.
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

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "parent-minimum-cover-cost-table-20261118.json")
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
    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}

    # row -> parents (5-stone canon of each stone removal)
    row_parents = {}
    for h in rows:
        m = int(h, 16)
        bits = [i for i in range(121) if (m >> i) & 1]
        row_parents[h] = {canon_hex(m ^ (1 << b)) for b in bits}

    # phase-1 candidates
    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e
    check("phase1.rows", len(row_cands) == sum(1 for h in rows if h not in closed and h not in sterile),
          {"loaded": len(row_cands)})
    check("phase1.cost_assert", all(len(e["cands"]) == e["cost"] for e in row_cands.values()))

    # global root -> occurrences over open rows
    root_occ = defaultdict(list)
    for h, e in row_cands.items():
        for root, bit in e["cands"]:
            root_occ[root].append((h, bit))
    check("phase1.distinct_roots", len(root_occ) > 0, len(root_occ))

    parents = cen["open_s5_census"]
    check("census.parents", len(parents) == 174, len(parents))

    # global census crosscheck: census remaining_s6_orbits counts ALL remaining
    # rows of the parent (STERILE rows included; the worklist is the head-1410
    # open state), and remaining_s7_edge_cost is the sum of their candidate costs.
    mism = []
    tot = 0
    for p in parents:
        ph = p["hex"]
        jr = [h for h in rows if ph in row_parents[h]]
        tot += p["remaining_s6_orbits"]
        if len(jr) != p["remaining_s6_orbits"] or sum(int(rows[h]["own_candidates_s6_s7_edge_cost"]) for h in jr) != p["remaining_s7_edge_cost"]:
            mism.append(ph)
    check("census.join_crosscheck_all174", not mism, mism[:5])
    check("census.remaining_row_refs_total", tot == cen["census_totals"]["remaining_row_refs"], tot)

    table = []
    exact_count = 0
    union_targets = set()
    for p in parents:
        ph = p["hex"]
        target = sorted(h for h in row_cands if ph in row_parents[h])
        union_targets.update(target)
        r = len(target)
        tset = set(target)
        # per-parent root map
        proot_rows = defaultdict(set)
        proot_occ = defaultdict(list)
        cand_total = 0
        for h in target:
            e = row_cands[h]
            cand_total += e["cost"]
            for root, bit in e["cands"]:
                proot_rows[root].add(h)
                proot_occ[root].append((h, bit))
        # restrict cover rows to target (they are by construction, but a root may
        # also cover non-target rows via occurrences in other parents' rows;
        # proot_rows only holds target occurrences)
        hist = defaultdict(int)
        for root, cov in proot_rows.items():
            hist[len(cov)] += 1
        maxspan = max(hist) if hist else 0
        lb = (r + maxspan - 1) // maxspan if maxspan else 0

        # greedy cover (upper bound + fallback witness)
        def greedy_cover():
            uncovered = set(tset)
            chosen = []
            # index roots by uncovered rows for speed: simple scan is fine (roots <= few k)
            rlist = sorted(proot_rows)
            while uncovered:
                best = None
                for root in rlist:
                    gain = len(proot_rows[root] & uncovered)
                    if gain == 0:
                        continue
                    if best is None or gain > best[0]:
                        best = (gain, root)
                if best is None:
                    return None
                gain, root = best
                chosen.append(root)
                uncovered -= proot_rows[root]
            return chosen

        # matching-style witness for maxspan <= 2
        witness = None
        method = None
        if r == 0:
            witness = []
            method = "trivial_empty"
        elif maxspan <= 2:
            pair_edges = defaultdict(list)  # (rowA,rowB) -> roots
            for root, cov in proot_rows.items():
                if len(cov) == 2:
                    a, b = sorted(cov)
                    pair_edges[(a, b)].append(root)
            # try matchings: r even -> perfect; r odd -> leave one row for singleton
            rng = random.Random(20261118)
            edge_list = sorted(pair_edges)
            best_match = None
            for trial in range(60):
                order = edge_list[:] if trial == 0 else rng.sample(edge_list, len(edge_list))
                matched = {}
                used = set()
                for (a, b) in order:
                    if a in used or b in used:
                        continue
                    matched[(a, b)] = pair_edges[(a, b)][0]
                    used.add(a); used.add(b)
                if best_match is None or len(matched) > len(best_match[0]):
                    best_match = (matched, used)
                need = r // 2 if r % 2 == 0 else (r - 1) // 2
                if len(matched) == need:
                    best_match = (matched, used)
                    break
            matched, used = best_match
            need = r // 2 if r % 2 == 0 else (r - 1) // 2
            if len(matched) == need:
                wit = [matched[k] for k in sorted(matched)]
                if r % 2 == 1:
                    leftover = [h for h in target if h not in used]
                    if len(leftover) != 1:
                        # matching covered more than r-1 rows (impossible) or left many
                        witness = None
                        method = "greedy_bound"
                    else:
                        lo = leftover[0]
                        sroots = [root for root, cov in proot_rows.items()
                                  if len(cov) == 1 and lo in cov]
                        if sroots:
                            wit.append(sorted(sroots)[0])
                            witness = wit
                            method = "matching_plus_singleton"
                        else:
                            witness = None
                            method = "greedy_bound"
                else:
                    witness = wit
                    method = "perfect_matching"
            else:
                witness = None
                method = "greedy_bound"
        else:
            witness = None
            method = "greedy_bound"
        if witness is None and r > 0:
            witness = greedy_cover()
            if witness is None:
                method = "no_cover"
            else:
                method = "greedy_cover"
        size = len(witness) if witness is not None else None
        exact = (r == 0) or (witness is not None and size == lb)
        if exact:
            exact_count += 1
        # verify witness
        if witness is not None:
            covered = set()
            for root in witness:
                covered |= proot_rows[root]
            check("witness.covers.%s" % ph[-8:], covered == tset)
            check("witness.distinct.%s" % ph[-8:], len(set(witness)) == len(witness))
            # each occurrence must canonize to the root: canon(row | 1<<bit) == root
            okocc = True
            for root in witness:
                rm = int(root, 16)
                for (h, bit) in proot_occ[root]:
                    hm = int(h, 16)
                    if canon_hex(hm | (1 << bit)) != root:
                        okocc = False
            check("witness.occurrences_canon.%s" % ph[-8:], okocc)
        table.append({
            "hex": ph,
            "classes": p["classes"],
            "classification": p["classification"],
            "rows_r": r,
            "candidates": cand_total,
            "distinct_roots": len(proot_rows),
            "span_histogram": {str(k): v for k, v in sorted(hist.items())},
            "maxspan": maxspan,
            "lower_bound": lb,
            "witness_size": size,
            "exact": exact,
            "method": method,
            "witness_roots": sorted(witness or []),
        })
    table.sort(key=lambda e: (not e["exact"], e["lower_bound"], e["rows_r"], e["hex"]))

    # spot crosschecks against published top-parent census values
    top = [e for e in table if e["hex"] == "00000000000000403800000008000000"][0]
    check("spot.top_parent", top["rows_r"] == 11 and top["candidates"] == 806
          and top["distinct_roots"] == 757 and top["span_histogram"] == {"1": 708, "2": 49}
          and top["exact"] and top["witness_size"] == 6,
          {k: top[k] for k in ("rows_r", "candidates", "distinct_roots", "witness_size")})
    run2 = [e for e in table if e["hex"] == "00000000000000003800000009000000"][0]
    check("spot.runner_up", run2["rows_r"] == 29 and run2["candidates"] == 2203
          and run2["distinct_roots"] == 1854
          and run2["span_histogram"] == {"1": 1505, "2": 349}
          and run2["exact"] and run2["witness_size"] == 15,
          {k: run2[k] for k in ("rows_r", "candidates", "distinct_roots", "witness_size")})
    check("targets.cover_all_open_rows", union_targets == set(row_cands),
          {"union": len(union_targets), "open": len(row_cands)})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-parent-minimum-cover-cost-table-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Minimum certificate-cover cost per open S5 parent on the head-1476 open non-STERILE row state",
        "inputs": {
            "worklist": {"path": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                          "git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"path": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                        "git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                        "git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
        },
        "method": ("Per parent: target rows = open non-STERILE rows whose 5-stone canon "
                   "parent set contains the parent. Candidate roots = D4-canonical "
                   "7-stone extensions of the target rows (phase-1 global enumeration, "
                   "each row's candidate count asserted equal to its published "
                   "own_candidates_s6_s7_edge_cost). Lower bound = ceil(r/maxspan) by "
                   "elementary incidence counting; exact when a witness of that size is "
                   "exhibited (for maxspan<=2: disjoint pair roots + at most one "
                   "singleton = matching, found by deterministic greedy matching with "
                   "60 restarts). Every witness is machine-verified at build time to "
                   "cover exactly the target rows with distinct roots, and each "
                   "witness root's generating (row, bit) occurrences satisfy "
                   "canon(row|1<<bit) == root. The output lists witness roots as "
                   "hexes; the full generating detail is reproducible by rerunning "
                   "the published phase-1 and phase-2 scripts (~45s total)."),
        "derived": {
            "parents": len(table),
            "exact_parents": exact_count,
            "rows_total": sum(e["rows_r"] for e in table),
            "summary_by_classification": {},
            "table": table,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Bookkeeping and combinatorics only. The 'minimum cover "
                                 "cost' is the smallest number of candidate roots whose "
                                 "hypothetical certificates would cover all remaining "
                                 "rows of a parent; it presumes every chosen root would "
                                 "actually validate and implies nothing about "
                                 "WIN/REFUTED outcomes. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    from collections import Counter
    sc = defaultdict(lambda: {"parents": 0, "exact": 0, "rows": 0})
    for e in table:
        s = sc[e["classification"]]
        s["parents"] += 1
        s["exact"] += 1 if e["exact"] else 0
        s["rows"] += e["rows_r"]
    output["derived"]["summary_by_classification"] = dict(sc)
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    slim = [{k: e[k] for k in ("hex", "classification", "classes", "rows_r", "candidates",
                                "distinct_roots", "maxspan", "lower_bound", "witness_size",
                                "exact", "method")} for e in table]
    print(json.dumps({"all_pass": all_pass, "checks": len(checks),
                      "failed": [c["name"] for c in checks if not c["pass"]][:10],
                      "exact": exact_count, "total": len(table),
                      "top10": slim[:10], "nonexact": [s for s in slim if not s["exact"]][:10]},
                     indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
