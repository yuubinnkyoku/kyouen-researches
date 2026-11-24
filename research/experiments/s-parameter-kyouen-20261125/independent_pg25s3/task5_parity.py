#!/usr/bin/env python3
"""Task 5: parity characterization (K1298) checks.

(a) Reproduce the small counterexample from K1298:
    n=5, s=2, blocks {(0,2),(0,4),(1,2),(2,4),(1,3,4),(0,2,3,4)}, S={}
    -- maximal extensions have mixed parity, yet Grundy(S)=0.
(b) Independently verify the local form of the theorem on the small board
    for all 32 positions (uniform extension parity <=> Grundy formula and
    "Grundy>=2 appears above S" <=> parity mixed).
(c) Big board consistency: maximal sizes 9/10/11 mixed parity implies
    Grundy >= 2 occurs; check all K1298 counters reported by the C DP.
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_task5.json")


def popcount(x):
    return int(x).bit_count()


def solve_board(n, blocks, s):
    """Return dict mask -> (grundy, misere_win), maximal masks, and parity sets."""
    bm = [sum(1 << p for p in B) for B in blocks]
    safe = [False] * (1 << n)
    for mask in range(1 << n):
        safe[mask] = all(popcount(mask & m) <= s for m in bm)

    # children within safe sets
    add = [0] * (1 << n)
    for mask in range(1 << n):
        if not safe[mask]:
            continue
        a = 0
        for p in range(n):
            if (mask >> p) & 1:
                continue
            if safe[mask | (1 << p)]:
                a |= 1 << p
        add[mask] = a

    grundy = {}
    misere = {}
    for mask in range((1 << n) - 1, -1, -1):
        if not safe[mask]:
            continue
        seen = 0
        nch = 0
        anyL = False
        av = add[mask]
        while av:
            p = (av & -av).bit_length() - 1
            av &= av - 1
            g = grundy[mask | (1 << p)]
            seen |= 1 << g
            nch += 1
            if not misere[mask | (1 << p)]:
                anyL = True
        g = 0
        while (seen >> g) & 1:
            g += 1
        grundy[mask] = g
        misere[mask] = 1 if (nch == 0 or anyL) else 0

    maximal = [m for m in range(1 << n) if safe[m] and add[m] == 0]
    par = {}  # mask -> set of parities of maximal extensions
    for mask in range((1 << n) - 1, -1, -1):
        if not safe[mask]:
            continue
        if add[mask] == 0:
            par[mask] = {popcount(mask) & 1}
        else:
            acc = set()
            av = add[mask]
            while av:
                p = (av & -av).bit_length() - 1
                av &= av - 1
                acc |= par[mask | (1 << p)]
            par[mask] = acc
    return safe, add, grundy, misere, maximal, par


def solve_board_sets(n, blocks, s):
    """Second, independent implementation using frozensets and lru_cache."""
    from functools import lru_cache
    B = [frozenset(b) for b in blocks]

    def is_safe(S):
        return all(len(S & b) <= s for b in B)

    @lru_cache(None)
    def gset(S):
        vals = []
        for p in range(n):
            if p in S:
                continue
            T = S | frozenset((p,))
            if is_safe(T):
                vals.append(gset(T))
        g = 0
        while g in vals:
            g += 1
        return g

    allsets = []
    for r in range(n + 1):
        for c in itertools.combinations(range(n), r):
            S = frozenset(c)
            if is_safe(S):
                allsets.append(S)
    maximal_sets = [
        S for S in allsets
        if not any(is_safe(S | frozenset((p,))) for p in range(n) if p not in S)
    ]
    return {
        "safe": set(allsets),
        "grundy": {S: gset(S) for S in allsets},
        "maximal": set(maximal_sets),
    }


def main():
    # ---------- (a)+(b) small counterexample board ----------
    n = 5
    s = 2
    blocks = [(0, 2), (0, 4), (1, 2), (2, 4), (1, 3, 4), (0, 2, 3, 4)]
    safe, add, grundy, misere, maximal, par = solve_board(n, blocks, s)

    empty = 0
    max_ext = sorted(maximal)
    parities = sorted({popcount(m) & 1 for m in max_ext})
    small = {
        "n": n, "s": s, "blocks": [list(B) for B in blocks],
        "n_safe_positions": sum(safe),
        "grundy_empty": grundy[empty],
        "misere_empty": misere[empty],
        "maximal_sets": [[i for i in range(n) if (m >> i) & 1] for m in max_ext],
        "n_maximal": len(max_ext),
        "maximal_sizes": sorted({popcount(m) for m in max_ext}),
        "parities_of_maximal_extensions_of_empty": parities,
        "mixed_parity": len(parities) > 1,
        "grundy_distribution": {
            str(g): sum(1 for m in grundy if grundy[m] == g)
            for g in sorted(set(grundy.values()))},
        "max_grundy": max(grundy.values()),
        "has_grundy_ge_2": any(g >= 2 for g in grundy.values()),
    }

    # local theorem check on every small-board position
    formula_bad = []
    equiv_bad = []
    misere_bad = []
    desc2 = {}
    for mask in range(1 << n):
        if not safe[mask]:
            continue
        g = grundy[mask]
        # desc2: exists T >= S with Grundy(T) >= 2
        d = False
        for t in range(1 << n):
            if safe[t] and (t & mask) == mask and grundy[t] >= 2:
                d = True
                break
        desc2[mask] = d
        p = par[mask]
        if len(p) == 1:
            pp = next(iter(p))
            if g != ((pp - popcount(mask)) & 1):
                formula_bad.append([mask, g, pp])
            if misere[mask] != (1 if g == 0 else 0):
                misere_bad.append([mask, g, misere[mask]])
        if d != (len(p) > 1):
            equiv_bad.append([mask, d, sorted(p)])
    small["local_formula_checked"] = len(grundy)
    small["local_formula_violations"] = formula_bad
    small["local_misere_violations"] = misere_bad
    small["local_mixed_equiv_checked"] = len(grundy)
    small["local_mixed_equiv_violations"] = equiv_bad

    # independent second implementation on the small board (frozensets + lru_cache)
    sets_res = solve_board_sets(n, blocks, s)
    mask_to_set = {m: frozenset(i for i in range(n) if (m >> i) & 1)
                   for m in grundy}
    cross_bad = []
    for m, gv in grundy.items():
        if sets_res["grundy"][mask_to_set[m]] != gv:
            cross_bad.append([m, gv, sets_res["grundy"][mask_to_set[m]]])
    cross_max = {frozenset(i for i in range(n) if (m >> i) & 1) for m in maximal}
    small["second_impl"] = {
        "same_safe_count": len(sets_res["safe"]) == len(grundy),
        "same_grundy": not cross_bad,
        "same_maximal": sets_res["maximal"] == cross_max,
        "grundy_empty": sets_res["grundy"][frozenset()],
        "mismatches": cross_bad,
    }

    small["k1298_stated_grundy_empty"] = 0
    small["matches_k1298_stated_value"] = (small["grundy_empty"] == 0)
    small["caution_holds"] = (small["grundy_empty"] < 2)
    small["ok"] = (small["caution_holds"] and small["n_maximal"] == 6
                   and small["mixed_parity"] and small["has_grundy_ge_2"]
                   and not formula_bad and not equiv_bad and not misere_bad
                   and small["second_impl"]["same_safe_count"]
                   and small["second_impl"]["same_grundy"]
                   and small["second_impl"]["same_maximal"])

    # ---------- (c) big board summary ----------
    big = {}
    cl = os.path.join(HERE, "grundy_level_out.txt")
    rec = os.path.join(HERE, "grundy_rec_out.txt")
    if os.path.exists(cl) and os.path.exists(rec):
        def parse(path, prefix, root_key, with_max):
            d = {"sizes": {}, "grundy": {}, "size_grundy": {}, "size_misere": {}}
            with open(path) as f:
                for line in f:
                    t = line.split()
                    if not t:
                        continue
                    if t[0] == prefix + "SIZE" and len(t) >= 3:
                        if with_max:
                            d["sizes"][int(t[1])] = (int(t[2]), int(t[3]))
                        else:
                            d["sizes"][int(t[1])] = int(t[2])
                    elif t[0] == prefix + "GRUNDY":
                        d["grundy"][int(t[1])] = int(t[2])
                    elif t[0] == root_key:
                        d["root"] = (int(t[1]), int(t[2]))
                    elif t[0] == prefix + "SIZE_GRUNDY":
                        d["size_grundy"][int(t[1])] = [int(x) for x in t[2:]]
                    elif t[0] == prefix + "SIZE_MISERE":
                        d["size_misere"][int(t[1])] = (int(t[2]), int(t[3]))
                    elif t[0] == "K1298_UNIFORM_CHECKED":
                        d["uniform_checked"] = int(t[1]); d["uniform_viol"] = int(t[3])
                    elif t[0] == "K1298_DESC_CHECKED":
                        d["desc_checked"] = int(t[1]); d["desc_viol"] = int(t[3])
            return d
        lv = parse(cl, "", "ROOT", True)
        rv = parse(rec, "REC_", "REC_ROOTS", False)
        sizes = lv["sizes"]
        maximal_sizes = sorted(s for s, (c, m) in sizes.items() if m > 0)
        max_par = sorted({s & 1 for s in maximal_sizes})
        rec_counts = {s: v for s, v in rv["sizes"].items()}
        lv_counts = {s: v[0] for s, v in sizes.items()}
        big = {
            "maximal_sizes": maximal_sizes,
            "maximal_counts": {s: sizes[s][1] for s in maximal_sizes},
            "maximal_parities": max_par,
            "mixed_parity": len(max_par) > 1,
            "grundy_distribution": lv["grundy"],
            "grundy_ge_2_total": sum(v for g, v in lv["grundy"].items() if g >= 2),
            "root": lv["root"],
            "k1298_uniform_checked": lv["uniform_checked"],
            "k1298_uniform_violations": lv["uniform_viol"],
            "k1298_desc_checked": lv["desc_checked"],
            "k1298_desc_violations": lv["desc_viol"],
            "level_and_recursive_match": (
                lv["grundy"] == rv["grundy"]
                and lv_counts == rec_counts
                and lv["root"] == rv["root"]
                and lv["size_grundy"] == rv["size_grundy"]
                and lv["size_misere"] == rv["size_misere"]),
        }
        if not big["level_and_recursive_match"]:
            for key in ("grundy", "size_grundy", "size_misere"):
                if lv[key] != rv[key]:
                    big.setdefault("mismatch_fields", []).append(key)
            if lv_counts != rec_counts:
                big.setdefault("mismatch_fields", []).append("sizes")
            if lv["root"] != rv["root"]:
                big.setdefault("mismatch_fields", []).append("root")
        big["ok"] = (big["mixed_parity"] and big["grundy_ge_2_total"] > 0
                     and big["k1298_uniform_violations"] == 0
                     and big["k1298_desc_violations"] == 0
                     and big["level_and_recursive_match"])

    res = {"small_board": small, "big_board": big}
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
    sys.exit(0 if small["ok"] and big.get("ok", False) else 1)


if __name__ == "__main__":
    main()
