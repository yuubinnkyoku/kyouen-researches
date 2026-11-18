#!/usr/bin/env python3
"""Exact weighted-perfect-matching totals (minimum cover counts) for the two
cost-18 36-row parents (cover-table rank 6/7): even r = 36, so every minimum
cover is an exact perfect matching of 18 pair roots (a double-covered row
would leave some row uncovered), and the total minimum-cover count is
pm(full) over the weighted pair graph, computed with the same PmLazy
anchored-DP machinery that determined the 31-row parent totals (validated
there against two independent implementations).

The 36-row parents are the current frontier for exact totals: pair-type
counts are ~2.6x the 31-row parent's and the anchored tree of the full mask
is measured here for the first time. A state cap (default 8M, ~800MB) bounds
the attempt: if the anchored tree exceeds the cap, the script records the
frontier measurement (states at cap) instead of a total, which is itself a
publishable scaling fact for planning future exact computations.

Structure is validated against the published cover table (rows, candidates,
distinct roots, span histogram, cost 18 exact) and the maximum matching is
confirmed at 18 by the algebraic Tutte-rank method over two prime fields
(same independent machinery as the joint-cover third-implementation
cross-check), so pm(full) is the exact total rather than a partial
decomposition.

Timing fields are recorded in the console output only; the JSON is
deterministic so double runs are byte-comparable.
"""
import json, os, sys, hashlib, time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11
STATE_CAP = 8_000_000

PARENTS = [
    ("00000000000000003802000000000020", 18),
    ("00000000000000805082000000000000", 18),
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

class LCG:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFFFFFFFFFF
    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return self.s >> 33
    def below(self, n):
        return self.next() % n

def rank_mod(a, p):
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
    rng = LCG(seed)
    t = [[0] * r for _ in range(r)]
    for (a, b) in edges:
        v = 1 + rng.below(p - 2)
        t[a][b] = v
        t[b][a] = (p - v) % p
    return rank_mod(t, p) // 2

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
        self.states_at_cap = None

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
                self.states_at_cap = len(memo) + len(seen)
                raise MemoryError("pm state cap exceeded: %d" % (len(memo) + len(seen)))
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

def build_parent(target_hex, row_cands):
    p_orbit = {format(m, "032x") for m in orbit_masks(int(target_hex, 16))}
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

def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else STATE_CAP
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})
        print("  check %-52s %s" % (name, "PASS" if ok else "FAIL"), flush=True)

    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                                    "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    jsonl_data = read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/global-candidate-roots-20261118.jsonl",
                             "89b24065d0588b0891395c9283e3a5b3d5551595")
    check("jsonl.pin", True)
    row_cands = {}
    for line in jsonl_data.decode().splitlines():
        e = json.loads(line)
        row_cands[e["row"]] = e
    tbl = {e["hex"]: e for e in table["derived"]["table"]}

    per_parent = []
    for ph, cost in PARENTS:
        P = build_parent(ph, row_cands)
        r = P["r"]
        e = tbl[ph]
        hist = defaultdict(int)
        for root, cov in P["proot_rows"].items():
            hist[len(cov)] += 1
        mult_hist = defaultdict(int)
        for et, rl in P["pair_roots"].items():
            mult_hist[len(rl)] += 1
        degree = defaultdict(int)
        for (a, b), w in P["edge_w"].items():
            degree[a] += w
            degree[b] += w
        check("struct.%s.rows" % ph[-8:], r == 36 == e["rows_r"])
        check("struct.%s.candidates" % ph[-8:], P["cand_total"] == e["candidates"])
        check("struct.%s.roots" % ph[-8:], len(P["proot_rows"]) == e["distinct_roots"])
        check("struct.%s.span" % ph[-8:], {str(x): v for x, v in sorted(hist.items())} == e["span_histogram"])
        check("struct.%s.cost18" % ph[-8:], e["witness_size"] == cost == 18 and e["exact"]
              and e["lower_bound"] == 18)
        check("struct.%s.even_parity" % ph[-8:], r % 2 == 0 and r // 2 == cost)
        edges = [(a, b) for (a, b), w in P["edge_w"].items() if w]
        m1 = tutte_matching(r, edges, 1000000007, 0x5DEECE66D)
        m2 = tutte_matching(r, edges, 998244353, 0x2545F4914F6CDD1D)
        check("tutte.%s.fields_agree" % ph[-8:], m1 == m2, {"m1": m1, "m2": m2})
        check("tutte.%s.perfect_matching" % ph[-8:], m1 == 18, m1)
        iso_rows = [s for s in range(r) if degree[s] == 0]
        check("tutte.%s.no_isolated_rows" % ph[-8:], not iso_rows, iso_rows)
        t0 = time.time()
        pm = PmLazy(P["edge_w"], r, cap)
        total = None
        cap_exceeded = False
        states_at_cap = None
        try:
            total = pm.get((1 << r) - 1)
        except MemoryError:
            cap_exceeded = True
            states_at_cap = pm.states_at_cap
        secs = time.time() - t0
        rec = {
            "hex": ph,
            "rows": r,
            "candidates": P["cand_total"],
            "distinct_roots": len(P["proot_rows"]),
            "span_histogram": {str(x): v for x, v in sorted(hist.items())},
            "pair_types": len(P["pair_roots"]),
            "pair_type_multiplicity_histogram": {str(x): v for x, v in sorted(mult_hist.items())},
            "singleton_root_count": sum(P["w1"].values()),
            "max_matching_tutte": m1,
            "perfect_matching_confirmed": m1 == 18,
            "minimum_cover_semantics": ("even r: every minimum cover is an exact "
                                        "perfect matching of 18 pair roots; a "
                                        "double-covered row would leave a row uncovered"),
            "cap": cap,
            "cap_exceeded": cap_exceeded,
            "states_at_cap": states_at_cap,
            "memo_states": len(pm.memo),
            "total_minimum_covers": total,
            "degree_min_max": [min(degree.values()), max(degree.values())],
        }
        per_parent.append(rec)
        if cap_exceeded:
            print("[%s] CAP EXCEEDED at %d states (%.1fs)" % (ph[-8:], states_at_cap, secs), flush=True)
        else:
            print("[%s] total=%d memo=%d %.1fs" % (ph[-8:], total, len(pm.memo), secs), flush=True)
        del pm

    # cross-consistency: the cover table's exact-18 rows agree with perfect matchings
    check("cover_table.ranks_6_7", all(tbl[ph]["witness_size"] == 18 for ph, _ in PARENTS))

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-cost18-36row-parent-totals-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact minimum-cover totals (or frontier cap measurements) for the two cost-18 "
                  "36-row parents, cover-table ranks 6/7: even-r perfect-matching semantics with "
                  "PmLazy anchored DP and algebraic perfect-matching confirmation"),
        "inputs": {
            "cover_table": {"git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "candidate_roots_jsonl": {"git_blob_sha1": "89b24065d0588b0891395c9283e3a5b3d5551595"},
        },
        "method": ("Even r = 36: every minimum cover is an exact perfect matching of 18 pair roots "
                   "(18 pair roots cover at most 36 rows; any double-covered row leaves some row "
                   "uncovered; 17 pairs + 1 singleton cover only 35 rows), so the total "
                   "minimum-cover count is pm(full) over the weighted pair graph. Perfect "
                   "matching confirmed at 18 by Tutte-matrix rank over GF(1000000007) and "
                   "GF(998244353) (algebraic, independent of the combinatorial DP). pm(full) "
                   "computed with PmLazy (same machinery validated against two independent "
                   "implementations on the 31-row cost-16 parent) under a %d-state cap; if the "
                   "anchored tree exceeds the cap the script records the frontier measurement "
                   "(states at cap) instead of a total." % STATE_CAP),
        "derived": {"parents": per_parent},
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. Totals count minimum cover "
                                 "plans of the candidate-root system; they are not search costs "
                                 "and imply nothing about WIN/REFUTED outcomes of any root. "
                                 "REFUTED-D10 and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    out_path = os.path.join(HERE, "output", "cost18-36row-parent-totals-20261118.json")
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=1) + "\n")
    print("wrote %s all_pass=%s checks=%d" % (out_path, all_pass, len(checks)))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
