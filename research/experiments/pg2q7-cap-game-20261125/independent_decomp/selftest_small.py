"""Self-test of the enumeration/Grundy machinery on the small boards AG(2,2),
AG(2,3), AG(2,4), against exhaustive subset brute force.

This is not part of the AG(2,7) claim; it validates that the DFS/forbidden-mask
code used for the big board agrees with the literal definition on cases small
enough to enumerate every subset.
"""

import json

from boardlib import Board, HERE, REPO, read_board

BOARD_PATHS = [
    REPO / "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q2.txt",
    REPO / "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q3.txt",
    REPO / "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q4.txt",
]


def brute_force(brd):
    n = brd.n
    FULL = brd.FULL
    safe = bytearray(1 << n)
    for mask in range(1 << n):
        if all((mask & lm).bit_count() <= 2 for lm in brd.line_masks):
            safe[mask] = 1
    G = [None] * (1 << n)
    safe_masks = [m for m in range(1 << n) if safe[m]]
    for mask in sorted(safe_masks, key=int.bit_count, reverse=True):
        seen = set()
        rest = FULL & ~mask
        while rest:
            b = rest & -rest
            if safe[mask | b]:
                seen.add(G[mask | b])
            rest ^= b
        g = 0
        while g in seen:
            g += 1
        G[mask] = g
    counts = {}
    maximal = {}
    dist = {}
    for mask in safe_masks:
        k = mask.bit_count()
        counts[k] = counts.get(k, 0) + 1
        dist[k] = dist.get(k, {})
        dist[k][G[mask]] = dist[k].get(G[mask], 0) + 1
        if not any(safe[mask | (1 << p)] for p in range(n) if not (mask >> p) & 1):
            maximal[k] = maximal.get(k, 0) + 1
    return counts, maximal, dist, G[0]


def dfs_enumeration(brd):
    n = brd.n
    FULL = brd.FULL
    PAIR = brd.pair_line
    caps = [[] for _ in range(n + 1)]
    counts = [0] * (n + 1)
    maximal = [0] * (n + 1)

    def dfs(S, forbidden, last):
        k = S.bit_count()
        counts[k] += 1
        caps[k].append(S)
        A = FULL & ~S & ~forbidden
        if A == 0:
            maximal[k] += 1
            return
        T = A & ~((1 << (last + 1)) - 1)
        while T:
            b = T & -T
            p = b.bit_length() - 1
            f2 = forbidden
            s = S
            pl = PAIR[p]
            while s:
                bb = s & -s
                f2 |= pl[bb.bit_length() - 1]
                s ^= bb
            dfs(S | b, f2, p)
            T ^= b

    dfs(0, 0, -1)
    # bottom-up Grundy over the enumerated caps
    max_size = max(k for k in range(n + 1) if counts[k])
    G = {}
    dist = [dict() for _ in range(max_size + 1)]
    for k in range(max_size, -1, -1):
        for S in caps[k]:
            f = brd.forbidden(S)
            A = FULL & ~S & ~f
            seen = set()
            m = A
            while m:
                b = m & -m
                seen.add(G[S | b])
                m ^= b
            g = 0
            while g in seen:
                g += 1
            G[S] = g
            dist[k][g] = dist[k].get(g, 0) + 1
    counts_d = {k: counts[k] for k in range(max_size + 1)}
    maximal_d = {k: maximal[k] for k in range(max_size + 1)}
    dist_d = {k: dist[k] for k in range(max_size + 1)}
    return counts_d, maximal_d, dist_d, G[0], max_size


results = {}
ok = True
for path in BOARD_PATHS:
    n, m, blocks = read_board(path)
    brd = Board(n, blocks)
    b_counts, b_max, b_dist, b_root = brute_force(brd)
    d_counts, d_max, d_dist, d_root, max_size = dfs_enumeration(brd)
    # brute-force dist keys are ints; compare canonical dicts
    b_dist_c = {k: {int(g): c for g, c in v.items()} for k, v in b_dist.items()}
    d_dist_c = {k: {int(g): c for g, c in v.items()} for k, v in d_dist.items()}
    # compare non-zero entries only (the DFS dicts carry explicit zero counts)
    def nz(d):
        return {int(k): v for k, v in d.items() if v}
    same = (nz(b_counts) == nz(d_counts) and nz(b_max) == nz(d_max)
            and b_dist_c == d_dist_c and b_root == d_root)
    ok = ok and same
    results[path.name] = {
        "n": n, "m": m, "max_cap_size": max_size,
        "counts": b_counts, "maximal": b_max,
        "grundy_by_size": b_dist_c,
        "dfs_matches_bruteforce": same,
    }

print(json.dumps({"all_pass": ok, "boards": results}, indent=2))
(HERE / "selftest_small.json").write_text(
    json.dumps({"all_pass": ok, "boards": results}, indent=2), encoding="utf-8")
if not ok:
    raise SystemExit(1)
