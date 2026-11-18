#!/usr/bin/env python3
"""Elimination/survival structure of the 359,610 minimum covers of the
head-1476 class-2 11-row cover problem, on top of the published membership
counts (minimum-cover-root-membership-20261118.json).

Questions answered exactly, all by 0/1 knapsack count DPs over row masks:
 1. survival(k): if the k highest-membership roots are excluded (e.g. their
    own subproblems turn out unusable), how many of the 359,610 minimum
    covers survive? Marginal kill per root shows overlap between top roots.
 2. lex-plan resilience: covers avoiding all 6 roots of the published
    lexicographically-first minimum cover.
 3. joint membership m(r_i, r_j) for the top-10 membership roots: how many
    covers contain both. Greedy-by-membership ignores this overlap.
Sanity: single-root kill must equal the published membership of that root;
sum identities re-checked.
All bookkeeping; no engine, no verdict, no closure claim.
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
                 "8e870809251fdc27701518d66d6b8a65ec6798c7"),
    "membership": ("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json",
                    "ab1e655f4a89a677e57515cdbacfe56894323013"),
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

def count_covers(cmask_list, target, kmax, init_mask=0, init_k=0):
    """Exact count of (kmax - init_k)-root subsets of cmask_list whose union
    with init_mask covers target. Skip-if-no-new is correct because every
    root in a minimum cover is essential (min size is global-minimal)."""
    dp = [defaultdict(int) for _ in range(1 << 11)]
    dp[init_mask][init_k] = 1
    for x in cmask_list:
        if x & ~target:
            continue  # root covers rows outside the problem (cannot happen here)
        updates = []
        for mask in range(1 << 11):
            if not dp[mask]:
                continue
            nxt = mask | x
            if nxt == mask:
                continue
            for k, w in dp[mask].items():
                if k < kmax:
                    updates.append((nxt, k + 1, w))
        for nxt, k, w in updates:
            dp[nxt][k] += w
    return dp[target][kmax]

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "minimum-cover-elimination-structure-20261118.json")
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    cen = json.loads(read_pinned("census"))
    led = json.loads(read_pinned("ledger"))
    pub = json.loads(read_pinned("head1476"))
    mem = json.loads(read_pinned("membership"))
    for k in INPUTS:
        check("pin.%s" % k, True, INPUTS[k][1])

    rows = {}
    wl_lines = read_pinned("worklist").decode("utf-8").rstrip("\r\n").split("\n")
    headers = [h.strip() for h in wl_lines[0].split(",")]
    for line in wl_lines[1:]:
        vals = line.split(",")
        r = {h: (vals[i].strip() if i < len(vals) else "") for i, h in enumerate(headers)}
        rows[r["s6_canonical_hex"]] = r
    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}

    def join(parent):
        j = []
        for h in rows:
            m = int(h, 16)
            bits = [i for i in range(121) if (m >> i) & 1]
            if parent in {canon_hex(m ^ (1 << b)) for b in bits}:
                j.append(h)
        return sorted(j)

    current = [h for h in join(TARGET_PARENT) if h not in closed]
    nons = [h for h in current if h not in sterile]
    check("target.rows", len(current) == 11 and len(nons) == 11, len(current))
    target_hexes = sorted(current)
    target_set = set(target_hexes)
    rowIndex = {h: i for i, h in enumerate(target_hexes)}

    root_occ = {}
    for h in target_hexes:
        m = int(h, 16)
        stones = [i for i in range(121) if (m >> i) & 1]
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
                root_occ.setdefault(canon_hex(m | (1 << d)), []).append({"row": h, "bit": d})
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

    full = (1 << 11) - 1
    cmask = {r: sum(1 << rowIndex[h] for h in roots[r]["cover_rows"]) for r in root_list}
    all_cmask = [cmask[r] for r in root_list]

    total = count_covers(all_cmask, full, 6)
    check("total.minimum_covers", total == 359610, total)

    # published membership crosscheck: killing one root leaves total - m(r)
    pub_mem = {e["root"]: e["membership"] for e in mem["derived"]["all_root_memberships"]}
    check("membership.table_size", len(pub_mem) == 757, len(pub_mem))

    # ---------- survival curve: exclude top-k by membership ----------
    by_mem = sorted(root_list, key=lambda r: (-pub_mem[r], r))
    TOPK = 12
    survival = []
    prev_killed = 0
    remaining_roots = [cmask[r] for r in root_list]
    excluded = set()
    for k in range(0, TOPK + 1):
        if k > 0:
            rk = by_mem[k - 1]
            excluded.add(rk)
        sub = [cmask[r] for r in root_list if r not in excluded]
        rem = count_covers(sub, full, 6)
        killed = total - rem
        survival.append({
            "k": k,
            "excluded_next": by_mem[k] if k < TOPK else None,
            "surviving_covers": rem,
            "killed_covers": killed,
            "killed_share": round(killed / total, 6),
            "marginal_kill": killed - prev_killed,
            "membership_of_next": pub_mem[by_mem[k]] if k < TOPK else None,
        })
        prev_killed = killed
    for k in range(1, TOPK + 1):
        s = survival[k]
        check("survival.monotone.%d" % k,
              s["surviving_covers"] < survival[k - 1]["surviving_covers"],
              {"k": k, "rem": s["surviving_covers"]})
    # single-exclusion kill == membership (exactness crosscheck for k=1)
    check("survival.k1_kill_equals_membership",
          survival[1]["marginal_kill"] == pub_mem[by_mem[0]],
          {"kill": survival[1]["marginal_kill"], "membership": pub_mem[by_mem[0]]})

    # ---------- lex-plan resilience ----------
    lex_roots = [e["root"] for e in pub["derived"]["candidate_cover"]["lexicographically_first_minimum_cover"]]
    sub_lex = [cmask[r] for r in root_list if r not in set(lex_roots)]
    rem_lex = count_covers(sub_lex, full, 6)
    lex_result = {
        "lex_cover_roots": lex_roots,
        "covers_avoiding_all_lex_roots": rem_lex,
        "killed_share": round((total - rem_lex) / total, 6),
    }

    # ---------- joint membership of the top-10 roots ----------
    top10 = by_mem[:10]
    joint = []
    for i in range(len(top10)):
        for j in range(i + 1, len(top10)):
            ri, rj = top10[i], top10[j]
            init = cmask[ri] | cmask[rj]
            if init & ~full:
                continue
            sub = [cmask[r] for r in root_list if r not in (ri, rj)]
            # count 4-root completions covering full, starting from init
            m_ij = count_covers(sub, full, 6, init_mask=init, init_k=2)
            joint.append({"a": ri, "b": rj,
                          "membership_a": pub_mem[ri], "membership_b": pub_mem[rj],
                          "joint_membership": m_ij})
    # pairwise sanity: joint <= min(m_a, m_b)
    check("joint.bounded", all(e["joint_membership"] <= min(e["membership_a"], e["membership_b"]) for e in joint),
          len(joint))
    # exactness spot-check: forced inclusion of the top root must reproduce its membership
    r0 = by_mem[0]
    init0 = cmask[r0]
    sub0 = [cmask[r] for r in root_list if r != r0]
    m0 = count_covers(sub0, full, 6, init_mask=init0, init_k=1)
    check("joint.top1_forced_inclusion", m0 == pub_mem[r0], {"forced": m0, "published": pub_mem[r0]})

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-minimum-cover-elimination-structure-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Survival of the 359,610 minimum covers under root elimination; joint membership of the top-10 roots",
        "inputs": {k: {"path": INPUTS[k][0], "git_blob_sha1": INPUTS[k][1]} for k in INPUTS},
        "method": ("0/1 knapsack count DP over the 11-row mask (2048 states), restricted to the "
                   "non-excluded candidate roots; forced-inclusion variant with init_mask/init_k "
                   "for joint memberships. Skip-if-no-new is exact because in a size-6 cover every "
                   "root is essential (5 covers do not exist)."),
        "derived": {
            "total_minimum_covers": total,
            "survival_curve_excluding_topk_membership_roots": survival,
            "lex_plan_resilience": lex_result,
            "top10_joint_membership": joint,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Bookkeeping and combinatorics only. No engine run, no verdict, no "
                                 "fold, no closure claim. 'Excluded' models a root becoming unusable "
                                 "for certificate planning; the counts measure how many minimum-size "
                                 "6-root plans remain, and imply nothing about WIN/REFUTED outcomes "
                                 "or about non-minimum plans. REFUTED-D10 and STERILE are not LOSS "
                                 "proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(checks),
                      "failed": [c for c in checks if not c["pass"]],
                      "survival": [{"k": s["k"], "rem": s["surviving_covers"],
                                    "marginal": s["marginal_kill"]} for s in survival],
                      "lex": lex_result["covers_avoiding_all_lex_roots"],
                      "top_joint_max": max(joint, key=lambda e: e["joint_membership"]) if joint else None},
                     indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
