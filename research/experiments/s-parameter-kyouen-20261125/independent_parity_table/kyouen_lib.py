"""Independent re-computation of the s-parameter Kyouen (co-occupancy) game.

Game definition (matching K1058/K1298): a board is a finite point set together
with a family of blocks (lines).  Fix s >= 1.  A position is a set S of points
with |S & B| <= s for every block B.  A move adds one point so that the result
is still a position.  Normal play: the player with no move loses.  The Grundy
value is G(S) = mex{ G(S+p) : p addable }.

This module deliberately shares no code with the experiment solvers.  It only
uses the board files (incidence data) as input.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict


# ---------------------------------------------------------------- board input

def load_board(path):
    """Read a board file: first line '<n> <b>', then '<k> p1 ... pk' per block."""
    with open(path, "r", encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh if ln.strip()]
    n, b = map(int, lines[0].split())
    blocks = []
    for ln in lines[1:]:
        vals = list(map(int, ln.split()))
        k = vals[0]
        pts = tuple(vals[1:])
        if len(pts) != k:
            raise ValueError(f"block declares {k} points but has {len(pts)}")
        if any(p < 0 or p >= n for p in pts):
            raise ValueError("point index out of range")
        if len(set(pts)) != k:
            raise ValueError("repeated point in block")
        blocks.append(pts)
    if len(blocks) != b:
        raise ValueError(f"declared {b} blocks, found {len(blocks)}")
    return n, blocks


def validate_board(n, blocks):
    """Incidence sanity checks and design statistics."""
    b = len(blocks)
    sizes = Counter(len(B) for B in blocks)
    deg = [0] * n
    for B in blocks:
        for p in B:
            deg[p] += 1
    pair = Counter()
    for B in blocks:
        m = len(B)
        for i in range(m):
            for j in range(i + 1, m):
                a, c = B[i], B[j]
                pair[(a, c) if a < c else (c, a)] += 1
    expected_pairs = n * (n - 1) // 2
    pair_hist = Counter(pair.values())
    # every point used?
    unused = sum(1 for d in deg if d == 0)
    return {
        "n": n,
        "b": b,
        "block_size_hist": {str(k): v for k, v in sorted(sizes.items())},
        "point_degree_hist": {str(k): v for k, v in sorted(Counter(deg).items())},
        "pairs_covered": len(pair),
        "pairs_expected": expected_pairs,
        "pair_coverage_hist": {str(k): v for k, v in sorted(pair_hist.items())},
        "unused_points": unused,
        "valid_2design": (len(pair) == expected_pairs
                          and set(pair.values()) == {1}
                          and unused == 0),
    }


# --------------------------------------------------------- safe-set enumeration

def enumerate_safe(n, blocks, s, start_mask=0, start_points=()):
    """DFS enumeration of all safe sets containing start_points.

    Returns {size: [mask, ...]}.  Every safe superset of a safe set is reached
    by adding its points in increasing index order, so each set appears once.
    """
    nb = len(blocks)
    point_blocks = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            point_blocks[p].append(c)
    counts = [0] * nb
    used = [False] * n
    mask0 = start_mask
    for p in start_points:
        if used[p]:
            raise ValueError("duplicate start point")
        used[p] = True
        for c in point_blocks[p]:
            counts[c] += 1
            if counts[c] > s:
                raise ValueError("start set is not safe")
    by_size = defaultdict(list)

    def rec(mask, size, start):
        by_size[size].append(mask)
        for p in range(start, n):
            if used[p]:
                continue
            ok = True
            for c in point_blocks[p]:
                if counts[c] >= s:
                    ok = False
                    break
            if ok:
                used[p] = True
                for c in point_blocks[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in point_blocks[p]:
                    counts[c] -= 1
                used[p] = False

    rec(mask0, len(start_points), 0)
    return dict(by_size)


# ------------------------------------------------------------ Grundy layer DP

def grundy_layers(n, layers, use_array):
    """Descending-size DP over the enumerated positions.

    Returns (g, maximal, gdist, max_size).  `g` is a bytearray (use_array) or
    dict mapping position mask -> Grundy value.
    """
    if use_array:
        if n > 25:
            raise ValueError("array DP too large")
        g = bytearray([255]) * (1 << n)
    else:
        g = {}
    maximal = Counter()
    gdist = Counter()
    max_size = max(layers)
    for size in range(max_size, -1, -1):
        for mask in layers.get(size, ()):  # missing layers are empty
            ch = set()
            is_max = True
            for p in range(n):
                if (mask >> p) & 1:
                    continue
                nm = mask | (1 << p)
                if use_array:
                    v = g[nm]
                    if v != 255:
                        is_max = False
                        ch.add(v)
                else:
                    v = g.get(nm)
                    if v is not None:
                        is_max = False
                        ch.add(v)
            if is_max:
                maximal[size] += 1
            m = 0
            while m in ch:
                m += 1
            g[mask] = m
            gdist[m] += 1
    return g, maximal, gdist, max_size


def solve_positions(n, blocks, s, start_mask=0, start_points=(), use_array=False):
    """Full solve over all positions on the board (start = empty set)."""
    layers = enumerate_safe(n, blocks, s, start_mask, start_points)
    g, maximal, gdist, max_size = grundy_layers(n, layers, use_array)
    size_counts = {size: len(v) for size, v in sorted(layers.items())}
    tag = "all" if not start_points else "cone"
    return {
        "method": tag,
        "n": n,
        "s": s,
        "positions": sum(size_counts.values()),
        "size_counts": size_counts,
        "maximal_by_size": dict(sorted(maximal.items())),
        "grundy_dist": dict(sorted(gdist.items())),
        "root_grundy": g[start_mask],
        "max_size": max_size,
    }


# --------------------------------------------------- cone / frame double count

def cone_distribution(n, blocks, s, F, t=None):
    """Complete solve on the cone of all safe sets containing the safe set F.

    Returns counts by size and Grundy value (T_m(g)) and maximal counts.
    """
    F = tuple(F)
    fmask = sum(1 << p for p in F)
    layers = enumerate_safe(n, blocks, s, fmask, F)
    g, maximal, gdist, max_size = grundy_layers(n, layers, False)
    per = defaultdict(Counter)
    for mask, val in g.items():
        per[mask.bit_count()][val] += 1
    size_counts = {size: len(v) for size, v in sorted(layers.items())}
    return {
        "F": list(F),
        "cone_size": len(g),
        "T": {str(m): sum(c.values()) for m, c in sorted(per.items())},
        "T_g": {str(m): {str(v): c for v, c in sorted(cnt.items())}
                for m, cnt in sorted(per.items())},
        "T_max": {str(m): int(maximal.get(m, 0)) for m in sorted(per)},
        "grundy_dist": dict(sorted(gdist.items())),
        "maximal_by_size": dict(sorted(maximal.items())),
        "root_grundy": g[fmask],
        "size_counts": size_counts,
        "max_size": max_size,
    }


def inflate(dist, Nt, t):
    """N_m(g) = Nt * T_m(g) / C(m,t); returns counts and divisibility issues."""
    out = defaultdict(Counter)
    issues = []
    for m, ctr in dist.items():
        m = int(m)
        C = math.comb(m, t)
        for g, v in ctr.items():
            g = int(g)
            num = Nt * v
            if num % C:
                issues.append({"m": m, "g": g, "num": num, "C": C,
                               "remainder": num % C})
            out[m][g] = num // C
    return out, issues


def inflate_counts(dist, Nt, t):
    """N_m = Nt * T_m / C(m,t) for a simple size -> count map."""
    out = {}
    issues = []
    for m, v in dist.items():
        m = int(m)
        C = math.comb(m, t)
        num = Nt * int(v)
        if num % C:
            issues.append({"m": m, "num": num, "C": C,
                           "remainder": num % C})
        out[m] = num // C
    return out, issues


def inflate_counts_multi(dists, Nts, t):
    out = {}
    issues = []
    all_m = set()
    for d in dists:
        all_m.update(int(m) for m in d)
    for m in sorted(all_m):
        C = math.comb(m, t)
        num = sum(Nt * int(d.get(str(m), 0)) for d, Nt in zip(dists, Nts))
        if num % C:
            issues.append({"m": m, "num": num, "C": C, "remainder": num % C})
        out[m] = num // C
    return out, issues


def inflate_multi(dists, Nts, t):
    """Combined double counting over several 3-subset orbits (same t)."""
    out = defaultdict(Counter)
    issues = []
    all_m = set()
    for d in dists:
        all_m.update(int(m) for m in d)
    for m in sorted(all_m):
        C = math.comb(m, t)
        vals = Counter()
        for d, Nt in zip(dists, Nts):
            for g, v in d.get(str(m), {}).items():
                vals[int(g)] += Nt * v
        for g, num in vals.items():
            if num % C:
                issues.append({"m": m, "g": g, "num": num, "C": C,
                               "remainder": num % C})
            out[m][g] = num // C
    return out, issues


def collapse(inflated):
    """(m,g) counts -> ({m: total}, {g: total})."""
    by_size = Counter()
    by_g = Counter()
    for m, ctr in inflated.items():
        for g, v in ctr.items():
            by_size[m] += v
            by_g[g] += v
    return dict(sorted(by_size.items())), dict(sorted(by_g.items()))


def unit_sizes(inflated):
    """Sizes m with at least one position of that size (positive count)."""
    return sorted(m for m, ctr in inflated.items() if sum(ctr.values()) > 0)


def max_grundy(inflated):
    vals = [g for ctr in inflated.values() for g, v in ctr.items() if v > 0]
    return max(vals) if vals else None
