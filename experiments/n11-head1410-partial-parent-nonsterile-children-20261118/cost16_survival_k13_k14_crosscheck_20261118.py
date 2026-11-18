#!/usr/bin/env python3
"""Independent arithmetic and structural cross-check of the published
cost-16 survival-curve extensions k=13 (commit 3a1b9481), k=14 (dc8cb4a4),
k=15 (commit be21591ef), k=16 (b39202a4), k=17 (5b4b4f99), k=18 (2c307c6a),
k=19 (00c4a352), k=20 (52501cad), and k=21 (e3efa46a), verification lane.

Two independent layers, no experiment-script imports:

  1. value layer: exact BigInt arithmetic over the published numbers
     (grand-total identity, monotonicity, marginal chain, A/B split,
     share percentages, reproduce anchors, cross-publication series
     consistency, and the independent per-d-slice survive anchors
     at k=4/8/10 plus the k=11/12 A/B split anchors);
  2. structure layer: a fresh re-derivation of the structural census
     (shared/disjoint new pairs, b_only/zero/disjoint new triples and
     quads, full triple census, all-C(N,5) 5-subsets zero) from the
     pinned phase-B aggregate with an inline row-multiplicity
     classifier, compared against the published structure fields.

Fetches the published output JSONs at their pinned git blob sha1s
(via the jsdelivr mirror with a raw.githubusercontent.com fallback).
No recomputation of pm values: every value check is exact BigInt
arithmetic over the published numbers.

Usage: python3 cost16_survival_k13_k14_crosscheck_20261118.py [--local DIR]
"""
import argparse
import hashlib
import itertools
import json
import sys
import urllib.request

REPO = "yuubinnkyoku/kyouen-researches"
PATH = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output"
PINS = {
    "k13": ("cost16-survival-k13-20261118.json", "bcf680f7529a119223f362099ed89685b9e37db6"),
    "k14": ("cost16-survival-k14-20261118.json", "1f0b64b1d0587333be30b412e87178dd28afec6a"),
    "k15": ("cost16-survival-k15-20261118.json", "fdf99a93571c8c76d5e97325dd2e92ef4b57ce31"),
    "k16": ("cost16-survival-k16-20261118.json", "c6902c85424680b98e00d959f497562b6c3ef729"),
    "k17": ("cost16-survival-k17-20261118.json", "37e9e848c8b7b9c0faa0ba536eb56cb9464ef576"),
    "k18": ("cost16-survival-k18-20261118.json", "f35df4f230d46c158cbc4655e325dde60878017f"),
    "k19": ("cost16-survival-k19-20261118.json", "7c87ba5b0b69109b8caddf18b323b7819d4a6c26"),
    "k20": ("cost16-survival-k20-20261118.json", "69c7d84edeae57d79291a9603e3a2e130b7d97bf"),
    "k21": ("cost16-survival-k21-20261118.json", "5631e3f307119cdc067e7c6de24a305cd09a1109"),
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
}
# Independent anchors: survive totals recomputed per-d-slice from scratch
# with the ban-survival runner (script cost16_ban_survival_20261118.py,
# point/assemble modes; k=4/8/10 from commit 33abfdb8, k=11/12 extended on
# 2026-11-18, assemble 11-check JSON all_pass).
DIRECT_SURVIVE = {4: 2453842390618094434, 8: 2001925712552127087,
                   10: 1789978398755093008, 11: 1684364881947656288,
                   12: 1592021370388208692}
# Same direct recomputation, A-type / B-type split (exact integers from the
# per-d-slice B sums; independently confirms the published kill_A/kill_B
# split at every direct anchor, including the first two points k=11/12
# beyond the k=10 inclusion-exclusion curve range).
DIRECT_SPLIT = {
    4: (1912189176067079977, 541653214551014457),
    8: (1564239038548375836, 437686674003751251),
    10: (1400734279274103379, 389244119480989629),
    11: (1319225112917587991, 365139769030068297),
    12: (1247882269674605395, 344139100713603297),
}
QUINTS = {15: 3003, 16: 4368, 17: 6188, 18: 8568, 19: 11628, 20: 15504, 21: 20349}

def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def fetch(name: str, want_sha: str, local_dir: str | None) -> dict:
    if local_dir:
        data = open(f"{local_dir}/{name}", "rb").read()
    else:
        urls = [
            f"https://cdn.jsdelivr.net/gh/{REPO}@main/{PATH}/{name}",
            f"https://raw.githubusercontent.com/{REPO}/main/{PATH}/{name}",
        ]
        data = None
        for u in urls:
            try:
                data = urllib.request.urlopen(u, timeout=60).read()
                break
            except Exception:
                continue
        if data is None:
            raise RuntimeError(f"could not fetch {name}")
    got = git_blob_sha1(data)
    if got != want_sha:
        raise RuntimeError(f"{name}: blob sha1 {got} != pinned {want_sha}")
    return json.loads(data)

def classify(rows, combo):
    """Row-multiplicity classifier, written independently for this
    cross-check (same definition as the k14 publication): 'zero' for a
    3x row or two 2x rows, 'b_only' for exactly one 2x row, 'disjoint'
    otherwise."""
    c = {}
    for i in combo:
        for r in rows[i]:
            c[r] = c.get(r, 0) + 1
    if max(c.values()) >= 3:
        return "zero"
    twos = [r for r, v in c.items() if v == 2]
    if len(twos) >= 2:
        return "zero"
    if len(twos) == 1:
        return "b_only"
    return "disjoint"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default=None, help="directory with the published JSONs (offline mode; sha1 still checked)")
    args = ap.parse_args()

    js = {tag: fetch(*PINS[tag], args.local) for tag in PINS}
    for tag in [t for t in js if t != "agg"]:
        if not js[tag].get("all_pass"):
            print(f"FAIL {tag} all_pass is false")
            return 1
    agg = js["agg"]
    top = agg["derived"]["top50_by_membership"]
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]

    V = js["k21"]["values"]  # contains the full k=1..21 series
    kill = {int(k[1:]): int(v) for k, v in V["kill"].items()}
    A = {int(k[1:]): int(v) for k, v in V["A_survive"].items()}
    B = {int(k[1:]): int(v) for k, v in V["B_survive_full_singleton_ban"].items()}
    sh = {int(k[1:]): v for k, v in V["B_survive_share_percent"].items()}
    ksh = {int(k[1:]): v for k, v in V["kill_share_percent"].items()}
    kA = {int(k[1:]): int(v) for k, v in V["kill_A"].items()}
    kB = {int(k[1:]): int(v) for k, v in V["kill_B"].items()}
    K = 21
    checks = []

    # 1. grand-total identity, constant across all k
    T = A[1] + B[1] + kill[1]
    checks.append((f"grand_total_constant_k1_{K}",
                   all(A[k] + B[k] + kill[k] == T for k in kill), T))
    # 2. B(0) anchor == B16
    checks.append(("B0_equals_B16", B[0] == 660663050386546968, None))
    checks.append(("B0_share_k0_consistent", abs(B[0] / T * 100 - sh[0]) < 5e-6, None))
    # 3. monotonicity over the full series
    checks.append((f"kill_monotone_k1_{K}", all(kill[k] < kill[k + 1] for k in range(1, K)), None))
    checks.append(("A_survive_monotone_decreasing", all(A[k] > A[k + 1] for k in range(1, K)), None))
    checks.append(("B_survive_monotone_decreasing", all(B[k] > B[k + 1] for k in range(0, K)), None))
    # 4. marginal chain vs published marginals
    marg = {k: kill[k + 1] - kill[k] for k in range(1, K)}
    km = None
    for c in js["k13"]["checks"]:
        if c["name"] == "survival.marginals" and isinstance(c["detail"], dict):
            km = {int(k.split("_minus_")[0][1:]): int(v) for k, v in c["detail"].items()}
    checks.append((f"marginal_chain_k2_k{K}_matches_published",
                   km is not None and all(marg[k - 1] == km[k] for k in km),
                   f"k2..k{max(km) if km else 0} from k13"))
    chain_ok = True
    m_ok = True
    for n in range(14, K + 1):
        det = None
        for c in js["k%d" % n]["checks"]:
            if c["name"] == "survival.marginal":
                det = c["detail"]
        if det is None:
            chain_ok = False
            continue
        chain_ok = chain_ok and marg[n - 1] == int(det["k%d_minus_k%d" % (n, n - 1)])
        m_ok = m_ok and int(det["m%d" % n]) == mem[n - 1] and marg[n - 1] <= mem[n - 1]
    checks.append(("marginal_chain_k14_k21_matches_published", chain_ok, None))
    checks.append(("marginal_le_membership_k14_k21", m_ok,
                   "mN from pinned aggregate, independent of published detail"))
    # 5. independent direct-recomputation anchors (survive totals + A/B split)
    checks.append(("survive_totals_match_direct_recompute_k4k8k10k11k12",
                   all(A[k] + B[k] == DIRECT_SURVIVE[k] for k in DIRECT_SURVIVE),
                   sorted(DIRECT_SURVIVE)))
    checks.append(("A_B_split_matches_direct_recompute_k4k8k10k11k12",
                   all(A[k] == DIRECT_SPLIT[k][0] and B[k] == DIRECT_SPLIT[k][1]
                       for k in DIRECT_SPLIT),
                   {k: (str(DIRECT_SPLIT[k][0]), str(DIRECT_SPLIT[k][1]))
                    for k in DIRECT_SPLIT}))
    # 6. A/B kill split identity
    checks.append(("kill_A_plus_kill_B_identity",
                   all(kA[k] + kB[k] == kill[k] for k in kA), f"k=1..{max(kA)}"))
    checks.append((f"kill_A_monotone_k1_{K}", all(kA[k] <= kA[k + 1] for k in range(1, K)), None))
    checks.append((f"kill_B_monotone_k1_{K}", all(kB[k] <= kB[k + 1] for k in range(1, K)), None))
    # 7. share percentages consistent
    checks.append((f"B_share_percent_consistent_k0_{K}",
                   all(abs(B[k] / T * 100 - sh[k]) < 5e-6 for k in sh), None))
    checks.append((f"kill_share_percent_consistent_k1_{K}",
                   all(abs(kill[k] / T * 100 - ksh[k]) < 5e-6 for k in ksh), None))
    # 8. mixed full-singleton-ban endpoint == B_survive(14)
    mixed = None
    for c in js["k14"]["checks"]:
        if c["name"] == "mixed.k14_value":
            mixed = int(c["detail"]["full_singleton_ban_survive_k14"])
    checks.append(("mixed_k14_endpoint_equals_B_survive_14", mixed == B[14], (mixed, B[14])))
    # 9. published reproduce anchors
    rep = None
    for c in js["k13"]["checks"]:
        if c["name"] == "survival.reproduce_k1_k10":
            rep = c["detail"]
    checks.append(("k13_json_reproduces_direct_k10",
                   rep is not None and rep["k10_mine"] == rep["k10_pub"] == str(kill[10]), None))
    rep14 = None
    for c in js["k14"]["checks"]:
        if c["name"] == "reproduce_k1_13":
            rep14 = c["detail"]
    checks.append(("k14_json_reproduces_k13",
                   rep14 is not None and rep14["k13_mine"] == rep14["k13_pub"] == str(kill[13]), None))
    checks.append(("k15_json_reproduces_k1_14",
                   any(c["name"] == "reproduce_k1_14" and c["pass"] for c in js["k15"]["checks"]), None))
    rep_ok = True
    for n in range(16, K + 1):
        rep_ok = rep_ok and any(
            c["name"] == "reproduce_k1_%d" % (n - 1) and c["pass"]
            for c in js["k%d" % n]["checks"])
    checks.append(("k16_k21_reproduce_anchors_all_pass", rep_ok, None))
    # 10. quints all-zero anchors as published
    q_ok = True
    for n in range(15, K + 1):
        q_ok = q_ok and any(
            c["name"] == "quints.all_zero_%d" % QUINTS[n] and c["pass"]
            for c in js["k%d" % n]["checks"])
    checks.append(("quints_all_zero_published_k15_k21", q_ok,
                   "checks quints.all_zero_3003..20349 in each publication"))

    # ---- structure layer: independent re-derivation from the aggregate
    s_ok = True
    s_bad = []
    for n in range(16, K + 1):
        tag = "k%d" % n
        st = js[tag]["structure"]
        rk = st["rank%d_root" % n]
        idx = n - 1
        if sorted(rk["rows"]) != sorted(rows[idx]) or rk["root"] != top[idx]["root"]:
            s_ok = False
            s_bad.append((tag, "rank rows"))
        if int(rk["membership"]) != mem[idx] or int(rk["a_part"]) != memA[top[idx]["root"]] \
                or int(rk["b_part"]) != memB[top[idx]["root"]]:
            s_ok = False
            s_bad.append((tag, "membership split"))
    checks.append(("rank_root_fields_match_aggregate_k16_k21", s_ok, s_bad[:4]))
    pc_ok = True
    pc_bad = []
    for n in range(16, K + 1):
        det = None
        for c in js["k%d" % n]["checks"]:
            if c["name"] == "pairs.new_census":
                det = c["detail"]
        shared = sum(1 for i in range(n - 1) if set(rows[i]) & set(rows[n - 1]))
        if det is None or det["shared"] != shared or det["disjoint"] != (n - 1) - shared:
            pc_ok = False
            pc_bad.append((n, shared, det))
    checks.append(("new_pair_census_rederived_k16_k21", pc_ok, pc_bad[:4]))
    tc_ok = True
    tc_bad = []
    for n in range(16, K + 1):
        cen = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(n), 3):
            cen[classify(rows, c)] += 1
        pub = js["k%d" % n]["structure"]["triple_census_k%d" % n]
        if cen != pub:
            tc_ok = False
            tc_bad.append((n, cen, pub))
    checks.append(("full_triple_census_rederived_k16_k21", tc_ok, tc_bad[:4]))
    qc_ok = True
    qc_bad = []
    for n in range(16, K + 1):
        cen = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(n - 1), 3):
            cen[classify(rows, (n - 1,) + c)] += 1
        pub = js["k%d" % n]["structure"]["new_quad_census"]
        if cen["disjoint"] != 0 or pub["b_only"] != cen["b_only"] or pub["zero"] != cen["zero"]:
            qc_ok = False
            qc_bad.append((n, cen, pub))
    checks.append(("new_quad_census_rederived_k16_k21", qc_ok, qc_bad[:4]))
    n5_ok = True
    n5_bad = []
    for n in range(15, K + 1):
        cnt = 0
        for c in itertools.combinations(range(n), 5):
            cnt += 1
            if classify(rows, c) != "zero":
                n5_ok = False
                n5_bad.append((n, c))
        if cnt != QUINTS[n]:
            n5_ok = False
            n5_bad.append((n, "count", cnt))
    checks.append(("quints_rederived_all_zero_k15_k21", n5_ok,
                   "C(N,5) counts %s, bad %s" % (QUINTS, n5_bad[:4])))
    # ---- cross-publication series consistency (no history rewrite)
    xs_ok = True
    xs_bad = []
    for n in range(13, K + 1):
        v = js["k%d" % n]["values"]
        for key, ref in (("kill", kill), ("kill_A", kA), ("kill_B", kB)):
            for kk, vv in v[key].items():
                k = int(kk[1:])
                if k <= K and int(vv) != ref[k]:
                    xs_ok = False
                    xs_bad.append((n, key, kk))
    checks.append(("kill_series_consistent_across_publications_k13_k21", xs_ok, xs_bad[:4]))

    n_fail = 0
    for name, ok, extra in checks:
        print(("PASS" if ok else "FAIL"), name, extra if extra is not None else "")
        n_fail += 0 if ok else 1
    print(f"--- {len(checks)} checks, {n_fail} failures")
    print(f"grand total = {T}")
    print("kill(k)% =", {k: round(kill[k] / T * 100, 4) for k in sorted(kill)})
    return 0 if n_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
