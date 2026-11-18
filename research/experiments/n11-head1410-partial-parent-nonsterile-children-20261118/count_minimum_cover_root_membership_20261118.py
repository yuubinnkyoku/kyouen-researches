#!/usr/bin/env python3
"""Exact cover-membership counts for the 757 candidate roots of the head-1476
class-2 cover problem (11 S6 rows of parent 00000000000000403800000008000000).

For each D4-canonical 7-stone candidate root, count the number of minimum
(6-root) covers of the 11 rows that contain it. Two cover shapes exist
(verified in the crosscheck of the published census):
  - 1 singleton root + 5 disjoint pair roots: 337,020 covers
  - 6 pair roots with exactly one doubly-covered row: 22,590 covers
Membership is computed combinatorially:
  - a singleton root covering row i is in exactly ways10[i] covers, where
    ways10[i] = weighted perfect matchings of the other 10 rows by pair roots;
  - a pair root covering {a,b} is in g(a,b) covers, where
    g(a,b) = sum_{i in R} singleton_i * pm(R\\{i})            (singleton type)
           + dp2[R][5]                                       (6-pair, doubled row outside {a,b})
           + pm(full\\{b}) + pm(full\\{a})                   (6-pair, doubled row == a or == b),
    R = the other 9 rows, pm = weighted perfect matchings, dp2[mask][j] =
    number of j-subsets of the 49 pair roots with union exactly mask.
Sanity identity: sum of all root memberships == 6 * total minimum covers.
"""
import json, sys, os, hashlib
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
INPUTS = {
    "worklist": ("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                 "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "census": ("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
               "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "ledger": ("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
               "e8785d509e8a11a37c0d03cc450455a14708c34d"),
    "head1476": ("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-parent-census-and-class2-cover-20261118.json",
                 "28a0993d7192e599a95ab93becb5dc0d983a8d35"),
}
TARGET_PARENT = "00000000000000403800000008000000"
N = 11

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(name):
    rel, pin = INPUTS[name]
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    sha = git_blob_sha(data)
    if sha != pin:
        raise SystemExit("%s git blob SHA mismatch: %s != %s" % (name, sha, pin))
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

def transform(mask, t):
    out = 0
    for i in range(121):
        if (mask >> i) & 1:
            qx, qy = t(i % N, i // N)
            out |= 1 << (qy * N + qx)
    return out

def canon(mask):
    return min(transform(mask, t) for t in T)

def canon_hex(mask):
    return format(canon(mask), "032x")

def det3(a, b, c):
    x1, y1 = a % N, a // N
    x2, y2 = b % N, b // N
    x3, y3 = c % N, c // N
    A, B, C = x1 * x1 + y1 * y1, x1, y1
    D, E, F = x2 * x2 + y2 * y2, x2, y2
    G, H, I = x3 * x3 + y3 * y3, x3, y3
    return A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)

def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "minimum-cover-root-membership-20261118.json")
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    wl_bytes = read_pinned("worklist")
    cen = json.loads(read_pinned("census"))
    led = json.loads(read_pinned("ledger"))
    pub = json.loads(read_pinned("head1476"))
    for k in INPUTS:
        check("pin.%s" % k, True, INPUTS[k][1])

    wl_lines = wl_bytes.decode("utf-8").rstrip("\r\n").split("\n")
    headers = [h.strip() for h in wl_lines[0].split(",")]
    rows = {}
    for line in wl_lines[1:]:
        vals = line.split(",")
        r = {h: (vals[i].strip() if i < len(vals) else "") for i, h in enumerate(headers)}
        rows[r["s6_canonical_hex"]] = r
    def cost(h):
        return int(rows[h]["own_candidates_s6_s7_edge_cost"])
    parents = [p["hex"] for p in cen["open_s5_census"]]
    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}

    # recompute the head-1476 class-2 ranking top parent via 5-subset canon join
    def join(parent):
        j = []
        for h in rows:
            m = int(h, 16)
            bits = [i for i in range(121) if (m >> i) & 1]
            if parent in {canon_hex(m ^ (1 << b)) for b in bits}:
                j.append(h)
        return sorted(j)

    jp = join(TARGET_PARENT)
    current = [h for h in jp if h not in closed]
    nons = [h for h in current if h not in sterile]
    check("target.parent_rows", len(current) == 11 and len(nons) == 11, len(current))
    check("target.rows_match_published",
          sorted(current) == sorted(x["hex"] for x in pub["derived"]["selected_parent"]["target_s6_rows"]))

    target_hexes = sorted(current)
    target_set = set(target_hexes)
    rowIndex = {h: i for i, h in enumerate(target_hexes)}

    # det4 re-enumeration of candidates and roots
    root_occ = {}
    occ_total = 0
    for h in target_hexes:
        m = int(h, 16)
        stones = [i for i in range(121) if (m >> i) & 1]
        cnt = 0
        for d in range(121):
            if (m >> d) & 1:
                continue
            ok = True
            for i in range(6):
                if not ok:
                    break
                for j in range(i + 1, 6):
                    if not ok:
                        break
                    for k in range(j + 1, 6):
                        if det4(stones[i], stones[j], stones[k], d) == 0:
                            ok = False
                            break
            if ok:
                cnt += 1
                root = canon_hex(m | (1 << d))
                root_occ.setdefault(root, []).append({"row": h, "bit": d})
        check("cand.%s" % h, cnt == cost(h), cnt)
        occ_total += cnt
    check("cand.total", occ_total == 806, occ_total)

    roots = {}
    for root, occs in root_occ.items():
        m = int(root, 16)
        cover = set()
        for d in range(121):
            if (m >> d) & 1:
                ch = canon_hex(m ^ (1 << d))
                if ch in target_set:
                    cover.add(ch)
        occs.sort(key=lambda o: (o["row"], o["bit"]))
        roots[root] = {"cover_rows": sorted(cover), "occurrences": occs}
    root_list = sorted(roots)
    check("roots.distinct", len(root_list) == 757, len(root_list))
    pub_roots = {x["root"]: x for x in pub["derived"]["candidate_cover"]["all_candidate_roots"]}
    check("roots.published_table_match",
          set(pub_roots) == set(roots) and all(
              pub_roots[r]["cover_rows"] == roots[r]["cover_rows"]
              and pub_roots[r]["occurrences"] == roots[r]["occurrences"] for r in root_list))
    hist = defaultdict(int)
    for r in root_list:
        hist[len(roots[r]["cover_rows"])] += 1
    check("roots.histogram", dict(hist) == {1: 708, 2: 49}, dict(hist))

    full = (1 << 11) - 1
    singleton = [0] * 11
    pair_mult = {}
    pair_roots = []
    for r in root_list:
        cov = roots[r]["cover_rows"]
        if len(cov) == 1:
            singleton[rowIndex[cov[0]]] += 1
        elif len(cov) == 2:
            a, b = sorted(rowIndex[h] for h in cov)
            pair_mult[(a, b)] = pair_mult.get((a, b), 0) + 1
            pair_roots.append((r, a, b))
    check("structure.singletons", sum(singleton) == 708)
    check("structure.pairs", len(pair_roots) == 49)

    # weighted perfect matchings of a row subset by pair multiplicities
    memo = {}
    def pm(mask):
        if mask == 0:
            return 1
        if mask in memo:
            return memo[mask]
        first = 0
        while ((mask >> first) & 1) == 0:
            first += 1
        total = 0
        for j in range(first + 1, 11):
            if mask & (1 << j):
                w = pair_mult.get((first, j), 0)
                if w:
                    total += w * pm(mask & ~(1 << first) & ~(1 << j))
        memo[mask] = total
        return total

    ways10 = [pm(full & ~(1 << i)) for i in range(11)]
    matching_sum = sum(ways10)
    check("match.ways10_sum", matching_sum == 5250, ways10)
    singleton_type_total = sum(singleton[i] * ways10[i] for i in range(11))
    check("match.singleton_type_total", singleton_type_total == 337020, singleton_type_total)

    # dp2[mask][j] = number of j-subsets of the 49 pair roots with union exactly mask
    dp2 = [defaultdict(int) for _ in range(1 << 11)]
    dp2[0][0] = 1
    for (r, a, b) in pair_roots:
        cm = (1 << a) | (1 << b)
        updates = []
        for mask in range(1 << 11):
            if not dp2[mask]:
                continue
            for j, w in dp2[mask].items():
                if j < 6:
                    updates.append((mask | cm, j + 1, w))
        for nxt, j, w in updates:
            dp2[nxt][j] += w
    six_pair_total = dp2[full][6]
    check("match.six_pair_total", six_pair_total == 22590, six_pair_total)
    total_min_covers = singleton_type_total + six_pair_total
    check("match.total", total_min_covers == 359610, total_min_covers)

    # independent full knapsack re-count (third path)
    cmask = {r: sum(1 << rowIndex[h] for h in roots[r]["cover_rows"]) for r in root_list}
    cnt_dp = [defaultdict(int) for _ in range(1 << 11)]
    cnt_dp[0][0] = 1
    for root in root_list:
        x = cmask[root]
        updates = []
        for mask in range(1 << 11):
            if not cnt_dp[mask]:
                continue
            nxt = mask | x
            if nxt == mask:
                continue
            for k, w in cnt_dp[mask].items():
                if k < 6:
                    updates.append((nxt, k + 1, w))
        for nxt, k, w in updates:
            cnt_dp[nxt][k] += w
    check("match.knapsack_recount", cnt_dp[full][6] == total_min_covers, cnt_dp[full][6])

    # minimum cover size re-derivation
    INF = 99
    best = [INF] * (1 << 11)
    best[0] = 0
    for root in root_list:
        x = cmask[root]
        old = best[:]
        for mask in range(1 << 11):
            if old[mask] < INF and (mask | x) != mask:
                nxt = mask | x
                v = old[mask] + 1
                if v < best[nxt]:
                    best[nxt] = v
    check("cover.minimum", best[full] == 6, best[full])

    # ---------- membership counts ----------
    membership = {}
    memb_A = {}   # singleton-type (1 singleton + 5 pairs) covers containing the root
    memb_B = {}   # six-pair-type covers containing the root
    for r in root_list:
        cov = roots[r]["cover_rows"]
        if len(cov) == 1:
            i = rowIndex[cov[0]]
            membership[r] = memb_A[r] = ways10[i]
            memb_B[r] = 0
        else:
            a, b = sorted(rowIndex[h] for h in cov)
            R = full & ~(1 << a) & ~(1 << b)
            # singleton-type part: singleton on row i in R + 4 pairs matching R\{i}
            gA = 0
            for i in range(11):
                if R & (1 << i):
                    gA += singleton[i] * pm(R & ~(1 << i))
            # six-pair-type part, doubled row d:
            #   d not in {a,b}: the other 5 pair roots have union exactly R
            #   d == a: p is one of the two roots covering a; the other 5 roots
            #           perfectly match full\{b}  (b is covered only by p)
            #   d == b: symmetric, pm(full\{a})
            gB = dp2[R][5] + pm(full & ~(1 << b)) + pm(full & ~(1 << a))
            membership[r] = gA + gB
            memb_A[r] = gA
            memb_B[r] = gB
    total_membership = sum(membership.values())
    check("membership.identity_6x", total_membership == 6 * total_min_covers,
          {"sum": total_membership, "6x": 6 * total_min_covers})
    check("membership.singleton_type_sum",
          sum(memb_A.values()) == 6 * singleton_type_total,
          {"sum": sum(memb_A.values()), "expected": 6 * singleton_type_total,
           "note": "each singleton-type cover holds 1 singleton + 5 pair roots"})
    check("membership.six_pair_type_sum",
          sum(memb_B.values()) == 6 * six_pair_total,
          {"sum": sum(memb_B.values()), "expected": 6 * six_pair_total})

    zero_membership = [r for r in root_list if membership[r] == 0]
    ranked = sorted(root_list, key=lambda r: (-membership[r], r))
    lex_cover = [e["root"] for e in pub["derived"]["candidate_cover"]["lexicographically_first_minimum_cover"]]
    lex_memberships = {r: membership[r] for r in lex_cover}

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-minimum-cover-root-membership-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Exact cover-membership counts of the 757 candidate roots over the 359,610 minimum covers of the head-1476 class-2 11-row cover problem",
        "inputs": {k: {"path": INPUTS[k][0], "git_blob_sha1": INPUTS[k][1]} for k in INPUTS},
        "method": ("det4 candidate re-enumeration of the 11 target rows (crosschecked against the "
                   "published census root table), weighted-perfect-matching and exact-union-subset "
                   "DP over the 1-singleton+5-pair and 6-pair cover shapes, plus an independent "
                   "full 0/1 knapsack re-count of all minimum covers; membership identity "
                   "sum(memberships) == 6 * covers is asserted"),
        "derived": {
            "cover_space": {
                "singleton_type_covers": singleton_type_total,
                "six_pair_covers": six_pair_total,
                "total_minimum_covers": total_min_covers,
                "minimum_root_count": best[full],
                "knapsack_recount": cnt_dp[full][6],
            },
            "per_row": [
                {"row": h, "singleton_roots": singleton[i], "ways10": ways10[i]}
                for i, h in enumerate(target_hexes)
            ],
            "lexicographic_first_cover_membership": lex_memberships,
            "top50_roots_by_membership": [
                {"root": r, "membership": membership[r], "cover_rows": roots[r]["cover_rows"]}
                for r in ranked[:50]
            ],
            "zero_membership_roots": zero_membership,
            "membership_histogram": {
                str(m): sum(1 for r in root_list if membership[r] == m)
                for m in sorted({membership[r] for r in root_list})
            },
            "all_root_memberships": [
                {"root": r, "membership": membership[r],
                 "singleton_type_covers": memb_A[r], "six_pair_type_covers": memb_B[r],
                 "cover_rows": roots[r]["cover_rows"]}
                for r in root_list
            ],
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Bookkeeping and combinatorics only. No engine run, no verdict, no "
                                 "fold, no closure claim. Membership counts rank how many "
                                 "alternative 6-root certificate plans each candidate root "
                                 "participates in; they are not search costs and imply nothing "
                                 "about WIN/REFUTED outcomes. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(checks),
                      "failed": [c for c in checks if not c["pass"]],
                      "cover_space": output["derived"]["cover_space"],
                      "membership_sum": total_membership,
                      "zero_membership": len(zero_membership),
                      "lex": lex_memberships}, indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
