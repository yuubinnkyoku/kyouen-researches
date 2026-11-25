"""Task 4: Grundy values of cap positions, computed by mex recursion over the
upset (all caps containing the position).

The game: a position is a cap; a move adds one point while keeping it a cap;
a position with no move is terminal.  Grundy(pos) = mex{Grundy(pos+p)}.

`upset(base)` enumerates every cap containing `base` (canonical order: points
are only ever added in increasing index order, so each cap is visited once).
`grundy_by_dp` memoises over the same DAG.
"""
import json
import sys

import core

sys.setrecursionlimit(10000)


def upset_levels(base):
    """independent level-by-level enumeration of all caps containing `base`"""
    base_mask = core.cap_mask(base)
    levels = {len(base): {base_mask}}
    cur = {base_mask}
    while cur:
        nxt = set()
        for m in cur:
            allowed = core.allowed_points(m)
            while allowed:
                b = allowed & -allowed
                allowed ^= b
                nxt.add(m | b)
        if not nxt:
            break
        levels.setdefault(bin(next(iter(nxt))).count("1"), set()).update(nxt)
        cur = nxt
    sizes = {k: len(v) for k, v in levels.items()}
    allm = set()
    for v in levels.values():
        allm |= v
    return sizes, allm


def grundy_dp(base):
    """memoised mex recursion; returns (grundy(base), memo)"""
    memo = {}

    def G(mask):
        v = memo.get(mask)
        if v is not None:
            return v
        allowed = core.allowed_points(mask)
        vals = set()
        m = allowed
        while m:
            b = m & -m
            m ^= b
            vals.add(G(mask | b))
        g = 0
        while g in vals:
            g += 1
        memo[mask] = g
        return g

    g0 = G(core.cap_mask(base))
    return g0, memo


def analyse(base, label=""):
    g0, memo = grundy_dp(base)
    sizes = {}
    for m in memo:
        k = bin(m).count("1")
        sizes[k] = sizes.get(k, 0) + 1
    dist = {}
    for m, g in memo.items():
        k = bin(m).count("1")
        dist.setdefault(k, {}).setdefault(g, 0)
        dist[k][g] += 1
    maxsz = max(sizes)
    terminal = [m for m in memo if core.allowed_points(m) == 0]
    return {
        "label": label,
        "cap": list(base),
        "is_cap": core.is_cap(base),
        "grundy": g0,
        "upset_sizes": dict(sorted(sizes.items())),
        "upset_total": sum(sizes.values()),
        "upset_total_minus_self": sum(sizes.values()) - 1,
        "n_terminal_positions": len(terminal),
        "terminal_all_maximal": all(core.allowed_points(m) == 0 for m in terminal),
        "grundy_distribution_by_size": {k: dict(sorted(v.items())) for k, v in sorted(dist.items())},
        "max_size": maxsz,
    }


def main():
    import time
    res = {}
    for base, tag in (((0, 1, 10), "3cap"), ((0, 1, 10, 20), "4cap")):
        t = time.time()
        r = analyse(base, tag)
        r["seconds"] = round(time.time() - t, 1)
        # cross-check the upset with the level-by-level enumeration
        lev, allm = upset_levels(base)
        r["upset_sizes_level_enum"] = dict(sorted(lev.items()))
        r["upset_matches_level_enum"] = (
            dict(sorted(lev.items())) == r["upset_sizes"]
            and len(allm) == r["upset_total"])
        print(json.dumps(r, indent=1))
        res[tag] = r
    with open("out_task4.json", "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)

    claims = {
        "3cap": {"3": 1, "4": 64, "5": 1344, "6": 9408, "7": 16320, "8": 4032,
                 "9": 448, "10": 64},
        "4cap": {"4": 1, "5": 42, "6": 441, "7": 1020, "8": 315, "9": 42, "10": 7},
    }
    totals = {"3cap": 31681, "4cap": 1868}
    for tag in ("3cap", "4cap"):
        got = {str(k): v for k, v in res[tag]["upset_sizes"].items()}
        want = claims[tag]
        print(tag, "upset sizes match claim:", got == want, got)
        print(tag, "total match:", res[tag]["upset_total"] == totals[tag],
              res[tag]["upset_total"], totals[tag])
    print("grundy 3cap =", res["3cap"]["grundy"], "(claim 1)")
    print("grundy 4cap =", res["4cap"]["grundy"], "(claim 0)")


if __name__ == "__main__":
    main()
