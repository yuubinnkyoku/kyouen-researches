"""Task 4 - Grundy values of one representative per PGL(2,9) orbit of
k-subsets of C, by full upset DP over the whole board (cap game on PG(2,9)).

Game: a position is a cap S; a move adds one point keeping a cap; the terminal
positions are the maximal caps;  G(S) = mex{ G(S + p) : S + p a cap }.
"""
import json
import os
import random

import conic as K
import gf9 as F
import pg9 as P

OUT = "results_task4.json"

# one representative per C-orbit, from task 3 (board point labels)
REPS = {
    3: [(120, [0, 1, 10])],
    4: [(180, [0, 1, 10, 20]), (30, [0, 1, 10, 45])],
    5: [(180, [0, 1, 10, 20, 31]), (72, [0, 1, 10, 20, 51])],
    6: [(180, [0, 1, 10, 20, 31, 51]), (30, [0, 1, 10, 20, 31, 45])],
    7: [(120, [0, 1, 10, 20, 31, 45, 51])],
    8: [(45, [0, 1, 10, 20, 31, 45, 51, 62])],
    9: [(10, [0, 1, 10, 20, 31, 45, 51, 62, 75])],
}
CLAIM = {3: [1], 4: [0, 0], 5: [1, 1], 6: [0, 0], 7: [1], 8: [0], 9: [1]}


def popcount(m):
    return bin(m).count("1")


def upset(S):
    """All caps (bit masks) containing S."""
    seen = {S}
    stack = [S]
    while stack:
        T = stack.pop()
        a = P.allowed(T)
        while a:
            b = a & -a
            a ^= b
            U = T | b
            if U not in seen:
                seen.add(U)
                stack.append(U)
    return seen


def grundy_bottom_up(S):
    caps = upset(S)
    order = sorted(caps, key=lambda m: -popcount(m))
    g = {}
    for T in order:
        moves = set()
        a = P.allowed(T)
        while a:
            b = a & -a
            a ^= b
            moves.add(g[T | b])
        mex = 0
        while mex in moves:
            mex += 1
        g[T] = mex
    return g[S], caps


def grundy_recursive(S):
    """Independent recursive mex implementation (same recursion, other style)."""
    memo = {}

    def rec(T):
        if T in memo:
            return memo[T]
        moves = set()
        a = P.allowed(T)
        while a:
            b = a & -a
            a ^= b
            moves.add(rec(T | b))
        mex = 0
        while mex in moves:
            mex += 1
        memo[T] = mex
        return mex

    return rec(S)


def main():
    import sys
    sys.setrecursionlimit(100000)
    res = {"reps": {}, "claim": CLAIM}

    # the representatives and orbit sizes must agree with task 3
    if os.path.exists("results_task3.json"):
        with open("results_task3.json", encoding="utf-8") as fh:
            t3 = json.load(fh)
        match = True
        for k in sorted(REPS):
            mine = sorted((osz, tuple(rep)) for osz, rep in REPS[k])
            theirs = sorted(
                (int(sz), tuple(rep))
                for sz, rep in zip(t3["C_orbits"][str(k)]["sizes"],
                                   t3["C_orbits"][str(k)]["representatives_board_labels"]))
            match = match and mine == theirs
        res["reps_match_task3"] = match
        assert match, "task4 representatives disagree with task 3"
    else:
        res["reps_match_task3"] = None

    ok = True
    for k in sorted(REPS):
        entries = []
        for idx, (osz, rep) in enumerate(REPS[k]):
            S = P.mask_of(rep)
            g, caps = grundy_bottom_up(S)
            g2 = grundy_recursive(S)
            sizes = {}
            for T in caps:
                sizes[popcount(T)] = sizes.get(popcount(T), 0) + 1
            claimed = CLAIM[k][idx]
            entries.append({
                "orbit_size_per_conic": osz,
                "representative": rep,
                "is_cap": P.is_cap(S),
                "upset_positions": len(caps),
                "upset_by_size": dict(sorted(sizes.items())),
                "grundy": g,
                "grundy_recursive": g2,
                "claimed": claimed,
                "match": g == claimed == g2,
            })
            ok = ok and (g == claimed == g2)
            print("k=%d rep=%-40s orbit=%3d upset=%5d G=%d (rec %d, claim %d) %s"
                  % (k, rep, osz, len(caps), g, g2, claimed,
                     "OK" if g == claimed == g2 else "MISMATCH"))
        res["reps"][k] = entries

    # Grundy is PGL(3,9)-invariant: apply random conic-stabiliser elements
    mats = K.stabiliser(K.C_MASK, cache=K.STAB_CACHE)
    random.seed(5)
    mate_ok = True
    mate_detail = []
    for k in sorted(REPS):
        for osz, rep in REPS[k]:
            S = P.mask_of(rep)
            gS, _ = grundy_bottom_up(S)
            for _ in range(2):
                M = mats[random.randrange(len(mats))]
                T = 0
                for i in P.bits(S):
                    T |= 1 << P.LABEL[F.normalise(P.mat_vec(M, P.POINTS[i]))]
                gT = grundy_recursive(T)
                good = (gS == gT)
                mate_ok = mate_ok and good
                mate_detail.append({"k": k, "rep": rep, "mate": P.bits(T),
                                    "g_rep": gS, "g_mate": gT, "match": good})
    res["orbit_mate_check"] = {"ok": mate_ok, "detail": mate_detail}

    res["pass"] = ok and mate_ok
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print("\nTASK4:", "PASS" if res["pass"] else "FAIL")


main()
