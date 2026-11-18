#!/usr/bin/env python3
"""Independent arithmetic and structural cross-check of the published
cost-16 survival-curve extensions k=13 (commit 3a1b9481), k=14 (dc8cb4a4),
k=15 (commit be21591ef), k=16 (b39202a4), k=17 (5b4b4f99), k=18 (2c307c6a),
k=19 (00c4a352), k=20 (52501cad), k=21 (e3efa46a), k=22
(d9d48bd6), k=23 (c0179112), k=24 (b89cd0f5), k=25
(9c41b23a), k=26 (674cdf06 result JSON 3b68d6b4,
per-record JSONL d974042f), k=27 (script+log 16ca07d0,
result JSON 9b804a9c, per-record JSONL d43eb059), k=28 (script+log
a6010eef, result JSON efc500fa, per-record JSONL 42182831), k=29
(script+log f6966f18, result JSON 29fb9f92, per-record JSONL
40f74ef1), and k=30 (script+log 69b4e029, result JSON f6a08dc5,
per-record JSONL b3b5ee32), verification lane.

Three independent layers, no experiment-script imports:

  1. value layer: exact BigInt arithmetic over the published numbers
     (grand-total identity, monotonicity, marginal chain, A/B split,
     share percentages, reproduce anchors, cross-publication series
     consistency, and the independent per-d-slice survive anchors
     at k=4/8/10 plus the k=11/12 A/B split anchors);
  2. structure layer: a fresh re-derivation of the structural census
     (shared/disjoint new pairs, b_only/zero/disjoint new triples and
     quads, full triple census, all-C(N,5) 5-subsets zero up to k=25,
     and the k=26..k=30 5-subset censuses, the first ranks that are
     not all-zero, with the new-sensitive prev/new split)
     from the pinned phase-B aggregate with an inline row-multiplicity
     classifier, compared against the published structure fields;
  3. record layer (k=26 through k=30): each per-record JSONL is
     fetched at its own pinned git blob sha1, every joint record is
     re-classified with the same independent classifier, the new
     pairs / triples / quads and the recorded new b_only quint set
     are checked for combinatorial completeness,
     and the marginal inclusion-exclusion identities (total, A-type,
     B-type) are re-summed from the record joints alone.

Fetches the published output JSONs (and, for layer 3, the
k=26..k=30 per-record JSONLs) at their pinned git blob sha1s
(via the jsdelivr mirror with a raw.githubusercontent.com fallback;
a mirror serving stale-but-wrong bytes fails the sha1 check and the
next mirror is tried).
No recomputation of pm values: every value check is exact BigInt
arithmetic over the published numbers.

Usage: python3 cost16_survival_k13_k14_crosscheck_20261118.py [--local DIR]
"""
import argparse
import hashlib
import itertools
import json
import math
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
    "k22": ("cost16-survival-k22-20261118.json", "c1e9598ba79b7dc424a8d975b9b93179e4a13abf"),
    "k23": ("cost16-survival-k23-20261118.json", "fc60c3660c42e71a92ddf2964d11656b9aa263c9"),
    "k24": ("cost16-survival-k24-20261118.json", "a0955297355beef8b2cf2560afebb0001fcf880b"),
    "k25": ("cost16-survival-k25-20261118.json", "c69b63354314537880006bea4590d99fe1921b62"),
    "k26": ("cost16-survival-k26-20261118.json", "1841a281ff604e7f677b8c7772a7312f6f9da5e1"),
    "k27": ("cost16-survival-k27-20261118.json", "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8"),
    "k28": ("cost16-survival-k28-20261118.json", "99db3a9a48d044727b3a4d83fb7fc97daa7513d2"),
    "k29": ("cost16-survival-k29-20261118.json", "795665316c300a186979bafd2817b6961de2de60"),
    "k30": ("cost16-survival-k30-20261118.json", "9c24e7a30ad213d3b7675e620ec606b00f73a330"),
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
}
# k=26 per-record JSONL (published 2026-11-18, commit d974042f): 4,513
# records = pair 25 + triple 300 + quad 2,300 + quint 1,872 (b_only only;
# the 10,778 new zero quints are structural, joint 0) + anchors 8 + cross 8.
JSONL_K26 = ("cost16-survival-k26-20261118.jsonl", "e39f9c2d0cde767bad9b0dbdc74df7439177d6ca")
# k=27 per-record JSONL (published 2026-11-18, commit d43eb059): 3,278
# records = pair 26 + triple 325 + quad 2,600 + quint 309 (new b_only
# only; the 14,641 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=26 disjoint quads x both lineages)
# + cross 8.
JSONL_K27 = ("cost16-survival-k27-20261118.jsonl", "9674ab19e14a41836e065ee4b1d5042ab94eb18b")
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
# k=28 per-record JSONL (published 2026-11-18, commit 42182831): 3,652
# records = pair 27 + triple 351 + quad 2,925 + quint 331 (new b_only
# only; the 17,219 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=27 disjoint quads x both lineages)
# + cross 8.
JSONL_K28 = ("cost16-survival-k28-20261118.jsonl", "6316793b94fe7e95c3d91e283a4229cc7c7f5730")
# k=29 per-record JSONL (published 2026-11-18, commit 40f74ef1): 5,828
# records = pair 28 + triple 378 + quad 3,276 + quint 2,128 (new b_only
# only; the 18,347 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=28 disjoint quads x both lineages)
# + cross 8.
JSONL_K29 = ("cost16-survival-k29-20261118.jsonl", "7b2afe8559de6d94a82a4b0d3f62208572b51910")
# k=30 per-record JSONL (published 2026-11-18, commit b3b5ee32): 5,435
# records = pair 29 + triple 406 + quad 3,654 + quint 1,328 (new b_only
# only; the 22,423 new zero quints are structural, joint 0) + anchors 10
# (anchor4 = the two published k=29 disjoint quads x both lineages)
# + cross 8.
JSONL_K30 = ("cost16-survival-k30-20261118.jsonl", "98062c66b522e8df6604cd508427f37b2fbe8220")
# 5-subset counts are machine-derived with math.comb (no hand-written
# table): C(15..25,5) = 3003..53130, all verified zero-valued; k=26 and
# k=27 are the first censuses that are not all-zero (C(26,5) = 65,780
# with 1,872 b_only / 63,908 zero / 0 disjoint; C(27,5) = 80,730 with
# 2,181 b_only / 78,549 zero / 0 disjoint, of which the rank-27-new
# 5-subsets are 309 b_only / 14,641 zero / 0 disjoint), so their
# quints checks are census-based instead of the quints.all_zero
# anchors used at k<=25; k=28 (C(28,5) = 98,280: 2,512 b_only /
# 95,768 zero / 0 disjoint), k=29 (C(29,5) = 118,755: 4,640
# b_only / 114,115 zero / 0 disjoint, the rank-29-new layer being
# 2,128 b_only / 18,347 zero, with row 16 joining the double-row
# family {15,16,18,19}) and k=30 (C(30,5) = 142,506: 5,968 b_only /
# 136,538 zero / 0 disjoint, the rank-30-new layer being 1,328
# b_only / 22,423 zero) continue the census-based treatment.  At
# k=30 the quint double-row family stays {15,16,18,19}: row 14
# enters the quad double-row family for the first time (9 b_only
# quads) but never the quint one.


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def fetch_bytes(name: str, want_sha: str, local_dir: str | None) -> bytes:
    if local_dir:
        data = open(f"{local_dir}/{name}", "rb").read()
    else:
        urls = [
            f"https://cdn.jsdelivr.net/gh/{REPO}@main/{PATH}/{name}",
            f"https://raw.githubusercontent.com/{REPO}/main/{PATH}/{name}",
        ]
        data = None
        shas = []
        for u in urls:
            try:
                data = urllib.request.urlopen(u, timeout=60).read()
            except Exception:
                continue
            got = git_blob_sha1(data)
            if got == want_sha:
                break
            shas.append((u.split("/")[2], got))
            data = None
        if data is None:
            raise RuntimeError(f"could not fetch {name} at pinned sha "
                               f"{want_sha} (mirror results: {shas})")
        return data
    got = git_blob_sha1(data)
    if got != want_sha:
        raise RuntimeError(f"{name}: blob sha1 {got} != pinned {want_sha}")
    return data


def fetch(name: str, want_sha: str, local_dir: str | None) -> dict:
    return json.loads(fetch_bytes(name, want_sha, local_dir))


def fetch_lines(name: str, want_sha: str, local_dir: str | None) -> list:
    data = fetch_bytes(name, want_sha, local_dir)
    return [json.loads(l) for l in data.decode("utf-8").splitlines() if l]


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


def classify2(rows, combo):
    """classify plus provenance: returns (class, doubled_row_or_None);
    the doubled row is the b_only signature used for the k=26 quint
    double-row census."""
    c = {}
    for i in combo:
        for r in rows[i]:
            c[r] = c.get(r, 0) + 1
    if max(c.values()) >= 3:
        return "zero", None
    twos = [r for r, v in c.items() if v == 2]
    if len(twos) >= 2:
        return "zero", None
    if len(twos) == 1:
        return "b_only", twos[0]
    return "disjoint", None


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

    V = js["k30"]["values"]  # contains the full k=1..30 series
    kill = {int(k[1:]): int(v) for k, v in V["kill"].items()}
    A = {int(k[1:]): int(v) for k, v in V["A_survive"].items()}
    B = {int(k[1:]): int(v) for k, v in V["B_survive_full_singleton_ban"].items()}
    sh = {int(k[1:]): v for k, v in V["B_survive_share_percent"].items()}
    ksh = {int(k[1:]): v for k, v in V["kill_share_percent"].items()}
    kA = {int(k[1:]): int(v) for k, v in V["kill_A"].items()}
    kB = {int(k[1:]): int(v) for k, v in V["kill_B"].items()}
    K = 30
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
    checks.append((f"marginal_chain_k14_k{K}_matches_published", chain_ok, None))
    checks.append((f"marginal_le_membership_k14_k{K}", m_ok,
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
    checks.append((f"k16_k{K}_reproduce_anchors_all_pass", rep_ok, None))
    # 10. quints all-zero anchors as published (k=15..k=25 only: at
    # k>=26 non-zero quint censuses appear and are handled below)
    q_ok = True
    for n in range(15, 26):
        q_ok = q_ok and any(
            c["name"] == "quints.all_zero_%d" % math.comb(n, 5) and c["pass"]
            for c in js["k%d" % n]["checks"])
    checks.append(("quints_all_zero_published_k15_k25", q_ok,
                   "checks quints.all_zero_3003..53130 at k=15..25 (machine.comb counts)"))

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
    checks.append((f"rank_root_fields_match_aggregate_k16_k{K}", s_ok, s_bad[:4]))
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
    checks.append((f"new_pair_census_rederived_k16_k{K}", pc_ok, pc_bad[:4]))
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
    checks.append((f"full_triple_census_rederived_k16_k{K}", tc_ok, tc_bad[:4]))
    qc_ok = True
    qc_bad = []
    for n in range(16, K + 1):
        cen = {"b_only": 0, "zero": 0, "disjoint": 0}
        for c in itertools.combinations(range(n - 1), 3):
            cen[classify(rows, (n - 1,) + c)] += 1
        pub = js["k%d" % n]["structure"]["new_quad_census"]
        if "disjoint" in pub:
            # k=26 and later: full census comparison (k=26 is the first
            # rank with a nonzero disjoint new-quad count: 233 records)
            ok = cen == pub
        else:
            # k<=25 publications list b_only/zero only; disjoint must be 0
            ok = cen["disjoint"] == 0 and pub["b_only"] == cen["b_only"] and pub["zero"] == cen["zero"]
        if not ok:
            qc_ok = False
            qc_bad.append((n, cen, pub))
    checks.append((f"new_quad_census_rederived_k16_k{K}", qc_ok, qc_bad[:4]))
    n5_ok = True
    n5_bad = []
    for n in range(15, 26):
        cnt = 0
        for c in itertools.combinations(range(n), 5):
            cnt += 1
            if classify(rows, c) != "zero":
                n5_ok = False
                n5_bad.append((n, c))
        if cnt != math.comb(n, 5):
            n5_ok = False
            n5_bad.append((n, "count", cnt))
    checks.append(("quints_rederived_all_zero_k15_k25", n5_ok,
                   "machine.comb counts 3003..53130 at k=15..25, bad %s" % (n5_bad[:4],)))
    # k=26 and k=27 quint censuses: the first non-all-zero 5-subset
    # censuses. Machine re-derivation over all C(n,5) 5-subsets with
    # the independent classifier, including the b_only double-row
    # histogram and the new-sensitive split (b_only 5-subsets that
    # contain the new rank n-1 are the recorded new-b_only layer).
    q_new_b_only = {}
    q_full = {}
    for n in (26, 27, 28, 29, 30):
        qn = {"b_only": 0, "zero": 0, "disjoint": 0}
        qn_twos = {}
        for c in itertools.combinations(range(n), 5):
            cl, two = classify2(rows, c)
            qn[cl] += 1
            if cl == "b_only":
                qn_twos[two] = qn_twos.get(two, 0) + 1
                if (n - 1) in c:
                    q_new_b_only.setdefault(n, set()).add(c)
        q_full[n] = qn
        q_new_b_only.setdefault(n, set())
        strn = js["k%d" % n]["structure"]
        checks.append((f"quint_census_k{n}_machine_rederived_C{n}5_{math.comb(n, 5)}",
                       qn["b_only"] + qn["zero"] + qn["disjoint"] == math.comb(n, 5)
                       and qn == strn["quint_census_k%d" % n]
                       and int(strn["quints_zero_synth_count"]) == math.comb(n - 1, 4) - len(q_new_b_only[n]),
                       (qn, qn_twos)))
        checks.append((f"quint_b_only_double_rows_k{n}_machine_rederived",
                       qn_twos == {int(k): v for k, v in strn["quint_b_only_double_rows"].items()},
                       qn_twos))
    # consecutive-era prev-layer identities: full(k) minus the
    # rank-k-new 5-subsets (C(k-1,4) counted as new b_only + new
    # zero) must equal the full census of the previous rank, for
    # the whole quint era k=27..30.
    for n, m in ((27, 26), (28, 27), (29, 28), (30, 29)):
        checks.append((f"quint_census_k{n}_prev_layer_equals_published_k{m}_census",
                       q_full[n]["b_only"] - len(q_new_b_only[n]) == q_full[m]["b_only"]
                       and q_full[n]["zero"] - (math.comb(n - 1, 4) - len(q_new_b_only[n])) == q_full[m]["zero"]
                       and q_full[n]["disjoint"] == q_full[m]["disjoint"] == 0,
                       (len(q_new_b_only[n]), q_full[n], q_full[m])))
    # k=26 is all-new: every b_only 5-subset of the C(26,5) census
    # contains the rank-26 root (published as such), so the full
    # census b_only set equals the new layer (len 1,872).
    checks.append(("k26_all_census_b_only_contain_rank26",
                   len(q_new_b_only[26]) == q_full[26]["b_only"], len(q_new_b_only[26])))
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
    checks.append((f"kill_series_consistent_across_publications_k13_k{K}", xs_ok, xs_bad[:4]))

    # ---- record layer (k=26 through k=30): each per-record JSONL is fetched
    # at its own pinned blob sha1; every joint record is re-classified
    # with the same independent classifier, the new pairs / triples /
    # quads and the recorded new b_only quint set are checked for
    # combinatorial completeness, and the marginal inclusion-exclusion
    # identities are re-summed from the record joints alone (no
    # experiment-script imports, no pm calls). anchor4 agreement is
    # re-derived from the two lineage records per combo; at k=26 the
    # single anchor4 combo is the published (25,3,4,16), at k=27 the
    # two combos are the published (25,3,4,16)/(25,3,4,17) disjoint
    # quads of the k=26 record layer, and k=28/k=29/k=30 likewise
    # anchor on the two published disjoint quads of the previous
    # rank's record layer.
    for n, pin, a4c in ((26, JSONL_K26, 1), (27, JSONL_K27, 2),
                         (28, JSONL_K28, 2), (29, JSONL_K29, 2),
                         (30, JSONL_K30, 2)):
        jl = fetch_lines(*pin, args.local)
        new = n - 1
        kinds = {}
        rec = {"pair": [], "triple": [], "quad": [], "quint": []}
        rl_ok = True
        for r in jl:
            k = r["kind"]
            kinds[k] = kinds.get(k, 0) + 1
            if k in rec:
                rec[k].append(r)
            elif k.startswith("anchor") or k.startswith("cross"):
                # anchor4 records carry no match field (the two lineages
                # are the two records; agreement re-derived separately)
                rl_ok = rl_ok and r.get("match", True) is True
            else:
                rl_ok = False
        kinds_exp = {"pair": new, "triple": math.comb(new, 2), "quad": math.comb(new, 3),
                     "quint": len(q_new_b_only[n]), "anchor2": 4, "anchor3": 2,
                     "anchor4": 2 * a4c, "cross3": 2, "cross4": 2,
                     "cross5": 2, "crossq4": 2}
        checks.append((f"jsonl_record_kind_counts_k{n}_{len(jl)}",
                       kinds == kinds_exp and len(jl) == sum(kinds_exp.values()), kinds))
        checks.append((f"jsonl_anchor_cross_records_all_match_k{n}", rl_ok, None))
        # anchor4 records carry no "match" field: the two lineages are
        # the two records themselves, so the agreement is re-derived
        # here (both lineages present per combo, identical A/B joints,
        # union rows re-derived from the aggregate where present).
        a4 = {}
        a4_ok = True
        for r in jl:
            if r["kind"] == "anchor4":
                key = tuple(sorted(r["combo"]))
                a4.setdefault(key, {})[r["lineage"]] = (int(r["joint_A"]), int(r["joint_B"]))
            elif r["kind"].startswith("anchor") or r["kind"].startswith("cross"):
                if r.get("union") is not None:
                    u = set()
                    for i in r["combo"]:
                        u |= set(rows[i])
                    if sorted(r["union"]) != sorted(u):
                        a4_ok = False
        a4_ok = a4_ok and len(a4) == a4c and all(
            sorted(v) == ["lazypm", "mypm"] for v in a4.values()) and all(
            len({v["lazypm"], v["mypm"]}) == 1 for v in a4.values())
        checks.append((f"jsonl_anchor4_two_lineage_agreement_{a4c}x8_union_rederived_k{n}",
                       a4_ok, None))
        p_ok = True
        for r in rec["pair"]:
            i, j = r["idx_i"], r["idx_j"]
            if j != new or not (0 <= i <= new - 1):
                p_ok = False
            elif r["shared_row"] != bool(set(rows[i]) & set(rows[j])):
                p_ok = False
            elif int(r["joint"]) != int(r["joint_A"]) + int(r["joint_B"]):
                p_ok = False
        checks.append((f"jsonl_pairs_are_exactly_the_{new}_new_pairs",
                       p_ok and sorted(r["idx_i"] for r in rec["pair"]) == list(range(new)),
                       None))
        # records store combos as (new, sorted others); classify is
        # order-independent so we normalize with sorted() everywhere
        cl_ok = True
        for kind in ("triple", "quad", "quint"):
            for r in rec[kind]:
                combo = tuple(sorted(r["combo"]))
                if new not in combo or r["class"] != classify(rows, combo) \
                        or (r["class"] == "zero" and int(r.get("joint", 0)) != 0):
                    cl_ok = False
        checks.append((f"jsonl_joint_records_reclassified_independently_k{n}", cl_ok, None))
        t_ex = {tuple(sorted((new,) + c)) for c in itertools.combinations(range(new), 2)}
        q_ex = {tuple(sorted((new,) + c)) for c in itertools.combinations(range(new), 3)}
        checks.append((f"jsonl_new_triples_quads_combinatorially_complete_k{n}",
                       {tuple(sorted(r["combo"])) for r in rec["triple"]} == t_ex
                       and {tuple(sorted(r["combo"])) for r in rec["quad"]} == q_ex,
                       (len(t_ex), len(q_ex))))
        checks.append((f"jsonl_quints_are_exactly_the_new_b_only_set_k{n}",
                       {tuple(sorted(r["combo"])) for r in rec["quint"]} == q_new_b_only[n],
                       len(q_new_b_only[n])))
        qc2 = {"b_only": 0, "zero": 0, "disjoint": 0}
        for r in rec["quad"]:
            qc2[r["class"]] += 1
        checks.append((f"jsonl_quad_record_census_matches_structure_k{n}",
                       qc2 == js["k%d" % n]["structure"]["new_quad_census"], qc2))
        # marginal inclusion-exclusion identities from the record joints
        s2 = sum(int(r["joint"]) for r in rec["pair"])
        s3 = sum(int(r["joint"]) for r in rec["triple"])
        s4 = sum(int(r["joint"]) for r in rec["quad"])
        s5 = sum(int(r["joint"]) for r in rec["quint"])
        rootn = top[new]["root"]
        mn, mna, mnb = int(mem[new]), int(memA[rootn]), int(memB[rootn])
        checks.append((f"jsonl_ie_marginal_identity_k{n}_total",
                       mn - s2 + s3 - s4 + s5 == kill[n] - kill[n - 1],
                       (mn - s2 + s3 - s4 + s5, kill[n] - kill[n - 1])))
        s2a = sum(int(r["joint_A"]) for r in rec["pair"])
        s2b = sum(int(r["joint_B"]) for r in rec["pair"])
        s3a = sum(int(r["joint_A"]) for r in rec["triple"])
        s3b = sum(int(r["joint_B"]) for r in rec["triple"])
        s4a = s4b = 0
        for r in rec["quad"]:
            if r["class"] == "disjoint":
                s4a += int(r["joint_A"])
                s4b += int(r["joint_B"])
            elif r["class"] == "b_only":
                s4b += int(r["joint"])
        s5b = sum(int(r["joint_B"]) for r in rec["quint"])
        checks.append((f"jsonl_ie_marginal_identity_k{n}_A_type",
                       mna - s2a + s3a - s4a == kA[n] - kA[n - 1],
                       (mna - s2a + s3a - s4a, kA[n] - kA[n - 1])))
        checks.append((f"jsonl_ie_marginal_identity_k{n}_B_type",
                       mnb - s2b + s3b - s4b + s5b == kB[n] - kB[n - 1],
                       (mnb - s2b + s3b - s4b + s5b, kB[n] - kB[n - 1])))


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
