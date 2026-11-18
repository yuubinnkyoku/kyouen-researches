#!/usr/bin/env python3
"""K0944 verification suite. All checks are pure deterministic arithmetic.

Checks (all must be 0-mismatch / all_ok):
  PIN       composite_core.py / sievegen_core.py byte-identical to the
            committed K0941/K0937 versions (sha256 pins).
  FASTEQ    sigma_E_fast == pinned sigma_E on
              (i)  tail family E(3; a, 3u), a in 0..3, u <= 800
              (ii) general E-states: P in 2..10, k in 2..150, all alpha
              (iii) sigma_Z_fast(M,K) == pinned for M in {2,3,5,9}, K<=100
              (iv) sigma_Z3(K) == pinned sigma_Z(3,K) for K <= 1500
  FOLD      K <= 4000: pinned sigma_Z(3,K) == sigma_Z3(K)
            (fast tail + fold4 trichotomy/cascade). Same loop reports:
            ONECHAR iff both directions, A2NEVER census (K=4u+2 has no 1).
  CENSUS    tail table u <= 10000, a in 0..3 (fast):
              - fold4-table value-1 set for K <= 40000 equals the
                ONE-CHAR prediction {4u+a : tail(a,u) == a+1}
              - mod-4 census of value-1 positions
              - U stats (a=0, tail==1) incl. first elements
              - a>=1 hit census (tail==a+1) and a=0 tail in {0,2} census
"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sigmaz3_core as C
from composite_core import sigma_E, sigma_Z

HERE = os.path.dirname(os.path.abspath(__file__))

COMPOSITE_SHA = "3990d67ff3a89f480bd92ae784a9efa763d76264e2b8e4a2d1752507a4740f40"
SIEVEGEN_SHA = "a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499"

def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_checks():
    R = {}

    # ---------------- PIN ----------------
    R["pin_composite_core_ok"] = _sha(os.path.join(HERE, "composite_core.py")) == COMPOSITE_SHA
    R["pin_sievegen_core_ok"] = _sha(os.path.join(HERE, "sievegen_core.py")) == SIEVEGEN_SHA

    # ---------------- FASTEQ ----------------
    bad = 0
    for a in range(4):
        for u in range(1, 801):
            if C.sigma_E_fast(3, a, 3 * u) != sigma_E(3, a, 3 * u):
                bad += 1
    R["fasteq_tail800_mismatch"] = bad
    R["fasteq_tail800_games"] = 3200

    bad = 0
    n = 0
    for P in range(2, 11):
        for k in range(2, 151):
            for alpha in range(0, k + 1):
                n += 1
                if C.sigma_E_fast(P, alpha, k - alpha) != sigma_E(P, alpha, k - alpha):
                    bad += 1
    R["fasteq_general_mismatch"] = bad
    R["fasteq_general_states"] = n

    bad = 0
    for M in (2, 3, 5, 9):
        for K in range(2, 101):
            if C.sigma_Z_fast(M, K) != sigma_Z(M, K):
                bad += 1
    R["fasteq_sigmaZ_mismatch"] = bad
    R["fasteq_sigmaZ_states"] = 4 * 99

    bad = 0
    for K in range(2, 1501):
        if C.sigma_Z3(K) != sigma_Z(3, K):
            bad += 1
    R["fasteq_sigmaZ3_K1500_mismatch"] = bad

    # ---------------- FOLD / ONECHAR / A2NEVER ----------------
    fold_bad = onechar_bad = 0
    ones_direct = ones_pred = 0
    a2_ones = 0
    for K in range(4, 4001):
        u, a = divmod(K, 4)
        stail_p = sigma_E(3, a, 3 * u)          # pinned tail
        v_dir = sigma_Z(3, K)                  # pinned full value
        v_fol = C.fold4(K, stail_p)             # fold prediction
        if v_dir != v_fol:
            fold_bad += 1
        d_one = (v_dir == 1)
        p_one = (stail_p == a + 1)
        if d_one != p_one:
            onechar_bad += 1
        ones_direct += d_one
        ones_pred += p_one
        if K % 4 == 2 and d_one:
            a2_ones += 1
    R["fold_K4000_mismatch"] = fold_bad
    R["onechar_K4000_mismatch"] = onechar_bad
    R["fold_K4000_games"] = 3997
    R["onechar_K4000_ones_direct"] = ones_direct
    R["onechar_K4000_ones_pred"] = ones_pred
    R["a2never_K4000_ones"] = a2_ones

    # ---------------- CENSUS ----------------
    UMAX = 10000
    KMAX = 4 * UMAX
    table = {a: [None] + [C.sigma_E_fast(3, a, 3 * u) for u in range(1, UMAX + 1)]
             for a in range(4)}
    # value-1 set via fold4 on the table vs ONE-CHAR prediction from the table
    ones_fold = [K for K in range(4, KMAX + 1)
                 if C.fold4(K, table[K % 4][K // 4]) == 1]
    ones_pred2 = [4 * u + a for a in range(4) for u in range(1, UMAX + 1)
                  if table[a][u] == a + 1]
    R["census_umax"] = UMAX
    R["census_fold_ones"] = len(ones_fold)
    R["census_pred_ones"] = len(ones_pred2)
    R["census_sets_equal"] = ones_fold == ones_pred2
    mod4 = {r: 0 for r in range(4)}
    for K in ones_fold:
        mod4[K % 4] += 1
    R["census_mod4"] = mod4
    U = [u for u in range(1, UMAX + 1) if table[0][u] == 1]
    R["census_U_count"] = len(U)
    R["census_U_first10"] = U[:10]
    R["census_U_last5"] = U[-5:]
    R["census_a0_tail0"] = sum(1 for u in range(1, UMAX + 1) if table[0][u] == 0)
    R["census_a0_tail2"] = sum(1 for u in range(1, UMAX + 1) if table[0][u] == 2)
    R["census_a123_hits"] = {a: sum(1 for u in range(1, UMAX + 1)
                                    if table[a][u] == a + 1) for a in (1, 2, 3)}

    R["all_ok"] = (
        R["pin_composite_core_ok"] and R["pin_sievegen_core_ok"]
        and R["fasteq_tail800_mismatch"] == 0
        and R["fasteq_general_mismatch"] == 0
        and R["fasteq_sigmaZ_mismatch"] == 0
        and R["fasteq_sigmaZ3_K1500_mismatch"] == 0
        and R["fold_K4000_mismatch"] == 0
        and R["onechar_K4000_mismatch"] == 0
        and R["a2never_K4000_ones"] == 0
        and R["census_sets_equal"]
        and R["census_fold_ones"] == R["census_pred_ones"]
        and R["census_mod4"] == {0: R["census_U_count"], 1: 0, 2: 0, 3: 0}
        and all(v == 0 for v in R["census_a123_hits"].values())
        and R["census_a0_tail0"] == 0 and R["census_a0_tail2"] == 0
    )
    return R

def main():
    r1 = run_checks()
    r2 = run_checks()
    s1 = json.dumps(r1, sort_keys=True, separators=(",", ":"))
    s2 = json.dumps(r2, sort_keys=True, separators=(",", ":"))
    assert s1 == s2, "non-deterministic run_checks"
    print(s1)

if __name__ == "__main__":
    main()
