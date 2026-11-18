#!/usr/bin/env python3
"""Independent arithmetic cross-check of the published cost-16 survival-curve
extensions k=13 (commit 3a1b9481), k=14 (commit dc8cb4a4), and k=15
(commit be21591ef), verification lane.

Fetches the three published output JSONs at their pinned git blob sha1s
(via the jsdelivr mirror with a raw.githubusercontent.com fallback) and runs
21 machine checks over the published values. No recomputation: every check
is exact BigInt arithmetic over the published numbers.

Usage: python3 cost16_survival_k13_k14_crosscheck_20261118.py [--local DIR]
"""
import argparse
import hashlib
import json
import sys
import urllib.request

REPO = "yuubinnkyoku/kyouen-researches"
PATH = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output"
PINS = {
    "k13": ("cost16-survival-k13-20261118.json", "bcf680f7529a119223f362099ed89685b9e37db6"),
    "k14": ("cost16-survival-k14-20261118.json", "1f0b64b1d0587333be30b412e87178dd28afec6a"),
    "k15": ("cost16-survival-k15-20261118.json", "fdf99a93571c8c76d5e97325dd2e92ef4b57ce31"),
}
# Independent anchors: survive totals recomputed per-d-slice from scratch
# (commit 33abfdb8, script cost16_ban_survival_20261118.py, 9-check JSON).
DIRECT_SURVIVE = {4: 2453842390618094434, 8: 2001925712552127087, 10: 1789978398755093008}


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default=None, help="directory with the three JSONs (offline mode; sha1 still checked)")
    args = ap.parse_args()

    k13 = fetch(*PINS["k13"], args.local)
    k14 = fetch(*PINS["k14"], args.local)
    k15 = fetch(*PINS["k15"], args.local)
    for tag, j in (("k13", k13), ("k14", k14), ("k15", k15)):
        if not j.get("all_pass"):
            print(f"FAIL {tag} all_pass is false")
            return 1

    V = k15["values"]  # contains the full k=1..15 series
    kill = {int(k[1:]): int(v) for k, v in V["kill"].items()}
    A = {int(k[1:]): int(v) for k, v in V["A_survive"].items()}
    B = {int(k[1:]): int(v) for k, v in V["B_survive_full_singleton_ban"].items()}
    sh = {int(k[1:]): v for k, v in V["B_survive_share_percent"].items()}
    kA = {int(k[1:]): int(v) for k, v in V["kill_A"].items()}
    kB = {int(k[1:]): int(v) for k, v in V["kill_B"].items()}
    checks = []

    # 1. grand-total identity, constant across all k
    T = A[1] + B[1] + kill[1]
    checks.append(("grand_total_constant_k1_15",
                   all(A[k] + B[k] + kill[k] == T for k in kill), T))
    # 2. B(0) anchor == B16
    checks.append(("B0_equals_B16", B[0] == 660663050386546968, None))
    checks.append(("B0_share_k0_consistent", abs(B[0] / T * 100 - sh[0]) < 5e-6, None))
    # 3. monotonicity
    checks.append(("kill_monotone_k1_15", all(kill[k] < kill[k + 1] for k in range(1, 15)), None))
    checks.append(("A_survive_monotone_decreasing", all(A[k] > A[k + 1] for k in range(1, 15)), None))
    checks.append(("B_survive_monotone_decreasing", all(B[k] > B[k + 1] for k in range(0, 15)), None))
    # 4. marginal chain vs published marginals
    marg = {k: kill[k + 1] - kill[k] for k in range(1, 15)}
    km = None
    for c in k13["checks"]:
        if c["name"] == "survival.marginals" and isinstance(c["detail"], dict):
            # keys "kN_minus_k(N-1)" hold kill(N)-kill(N-1)
            km = {int(k.split("_minus_")[0][1:]): int(v) for k, v in c["detail"].items()}
    checks.append(("marginal_chain_k2_k13_matches_published",
                   km is not None and all(marg[k - 1] == km[k] for k in km), f"{len(km)} points"))
    m14 = None
    for c in k14["checks"]:
        if c["name"] == "survival.marginal":
            m14 = int(c["detail"]["m14"])
            checks.append(("marginal_k14_matches_published",
                           marg[14] == int(c["detail"]["k14_minus_k13"]), marg[14]))
    checks.append(("marginal_k14_le_m14", marg[14] <= m14, (marg[14], m14)))
    m15 = None
    for c in k15["checks"]:
        if c["name"] == "survival.marginal":
            m15 = int(c["detail"]["m15"])
            checks.append(("marginal_k15_matches_published",
                           marg[15] == int(c["detail"]["k15_minus_k14"]), marg[15]))
    checks.append(("marginal_k15_le_m15", marg[15] <= m15, (marg[15], m15)))
    # 5. independent direct-recomputation anchors (survive totals)
    checks.append(("survive_totals_match_direct_recompute_k4k8k10",
                   all(A[k] + B[k] == DIRECT_SURVIVE[k] for k in DIRECT_SURVIVE), None))
    # 6. A/B kill split identity
    checks.append(("kill_A_plus_kill_B_identity",
                   all(kA[k] + kB[k] == kill[k] for k in kA), f"k=1..{max(kA)}"))
    checks.append(("kill_A_monotone", all(kA[k] <= kA[k + 1] for k in range(1, max(kA))), None))
    checks.append(("kill_B_monotone", all(kB[k] <= kB[k + 1] for k in range(1, max(kB))), None))
    # 7. share percentages consistent
    checks.append(("B_share_percent_consistent_k0_15",
                   all(abs(B[k] / T * 100 - sh[k]) < 5e-6 for k in sh), None))
    # 8. mixed full-singleton-ban endpoint == B_survive(14)
    mixed = None
    for c in k14["checks"]:
        if c["name"] == "mixed.k14_value":
            mixed = int(c["detail"]["full_singleton_ban_survive_k14"])
    checks.append(("mixed_k14_endpoint_equals_B_survive_14", mixed == B[14], (mixed, B[14])))
    # 9. published reproduce anchors
    rep = None
    for c in k13["checks"]:
        if c["name"] == "survival.reproduce_k1_k10":
            rep = c["detail"]
    checks.append(("k13_json_reproduces_direct_k10",
                   rep is not None and rep["k10_mine"] == rep["k10_pub"] == str(kill[10]), None))
    rep14 = None
    for c in k14["checks"]:
        if c["name"] == "reproduce_k1_13":
            rep14 = c["detail"]
    checks.append(("k14_json_reproduces_k13",
                   rep14 is not None and rep14["k13_mine"] == rep14["k13_pub"] == str(kill[13]), None))
    checks.append(("k15_json_reproduces_k1_14",
                   any(c["name"] == "reproduce_k1_14" and c["pass"] for c in k15["checks"]), None))
    # 10. k15 I-E termination anchor (all 3003 5-subsets structurally zero)
    checks.append(("k15_quints_all_zero_3003",
                   any(c["name"] == "quints.all_zero_3003" and c["pass"] for c in k15["checks"]), None))

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
