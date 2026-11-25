"""Shared utilities for the independent verification of K1336.

Only the Python standard library is used.  All outputs stay inside this
directory (independent_g2/).

Game (s = 2 "cap game"):
  positions  = caps S (no line contains 3 points of S)
  move       = add one point while staying a cap
  normal play: a player with no move loses
  Grundy     G(S) = mex { G(S + p) : p addable }
"""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BOARDS = {
    "PG(2,9)": REPO / "research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt",
    "AG(2,7)": REPO / "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt",
    "AG(2,5)": REPO / "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q5.txt",
}

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_board(path: Path):
    """Return (n, blocks) with blocks a list of tuples of 0-based points."""
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = []
    for line in lines[1:]:
        if not line.strip():
            continue
        vals = list(map(int, line.split()))
        k = vals[0]
        pts = tuple(vals[1:])
        if len(pts) != k:
            raise ValueError(f"{path}: header k={k} but {len(pts)} points: {line!r}")
        blocks.append(pts)
    if len(blocks) != b:
        raise ValueError(f"{path}: header b={b} but {len(blocks)} lines")
    return n, blocks


def validate_board(n: int, blocks) -> dict:
    """Full incidence validation, independent of how the board was built."""
    b = len(blocks)
    checks: dict[str, object] = {"n": n, "b": b}

    # --- local format checks -------------------------------------------------
    lens = Counter(len(B) for B in blocks)
    checks["line_size_histogram"] = dict(sorted(lens.items()))
    flat_ok = all(0 <= p < n for B in blocks for p in B)
    no_dupes = all(len(set(B)) == len(B) for B in blocks)
    checks["point_labels_in_range"] = flat_ok
    checks["no_repeated_point_within_line"] = no_dupes

    # --- pair multiplicity ---------------------------------------------------
    pair_count: dict[int, int] = {}
    for B in blocks:
        m = len(B)
        for i in range(m):
            pi = B[i]
            for j in range(i + 1, m):
                pj = B[j]
                key = pi * n + pj if pi < pj else pj * n + pi
                pair_count[key] = pair_count.get(key, 0) + 1
    mult_hist = Counter(pair_count.values())
    n_pairs = n * (n - 1) // 2
    checks["pairs_seen"] = len(pair_count)
    checks["pairs_possible"] = n_pairs
    checks["pair_multiplicity_histogram"] = dict(sorted(mult_hist.items()))
    checks["each_pair_at_most_one_line"] = max(pair_count.values(), default=0) <= 1
    checks["each_pair_exactly_one_line"] = (
        len(pair_count) == n_pairs and set(pair_count.values()) == {1}
    )

    # --- point degrees -------------------------------------------------------
    deg = [0] * n
    for B in blocks:
        for p in B:
            deg[p] += 1
    checks["point_degree_histogram"] = dict(sorted(Counter(deg).items()))
    checks["point_degree_constant"] = len(set(deg)) == 1
    checks["point_degree"] = deg[0] if deg else None

    # --- intersections of distinct lines ------------------------------------
    inter_hist = Counter()
    for i in range(b):
        Si = set(blocks[i])
        for j in range(i + 1, b):
            inter_hist[len(Si.intersection(blocks[j]))] += 1
    checks["line_intersection_size_histogram"] = dict(sorted(inter_hist.items()))
    checks["any_two_lines_meet_in_at_most_one_point"] = (
        max(inter_hist, default=0) <= 1
    )

    # --- design arithmetic ---------------------------------------------------
    k = lens.most_common(1)[0][0] if lens else 0
    checks["uniform_line_size"] = len(lens) == 1
    checks["k"] = k
    if k >= 2:
        checks["design_b_formula"] = n * (n - 1) // (k * (k - 1))
        checks["design_b_matches"] = checks["design_b_formula"] == b
        checks["replication_formula"] = (n - 1) // (k - 1)
        checks["replication_matches"] = checks["replication_formula"] == checks["point_degree"]

    # --- parallel classes (affine boards) -----------------------------------
    # Two lines are parallel iff disjoint.  For AG(2,q) the disjointness graph
    # on lines must split into q+1 cliques of q lines (parallel classes).
    if inter_hist.get(0, 0) > 0:
        parent = list(range(b))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry:
                parent[ry] = rx

        for i in range(b):
            Si = set(blocks[i])
            for j in range(i + 1, b):
                if not Si.intersection(blocks[j]):
                    union(i, j)
        classes = Counter(find(i) for i in range(b))
        sizes = Counter(classes.values())
        checks["parallel_class_count"] = len(classes)
        checks["parallel_class_size_histogram"] = dict(sorted(sizes.items()))
        checks["parallel_classes_are_cliques"] = all(s == k for s in classes.values())
        checks["parallel_class_count_is_k_plus_1"] = len(classes) == k + 1
    else:
        checks["parallel_class_count"] = 0
        checks["parallel_classes_are_cliques"] = True
        checks["parallel_class_count_is_k_plus_1"] = False

    # --- line-pair meet (projective boards) ---------------------------------
    checks["every_two_lines_meet"] = (
        b > 1 and set(inter_hist) == {1}
    )

    # --- s = 2 game sanity ---------------------------------------------------
    # A safe set is exactly a cap.  With all lines of size >= 3 this is the
    # standard "no 3 collinear" condition.
    checks["all_lines_have_at_least_3_points"] = all(len(B) >= 3 for B in blocks)
    checks["s"] = 2
    checks["valid_s2_incidence_structure"] = bool(
        checks["point_labels_in_range"]
        and checks["no_repeated_point_within_line"]
        and checks["each_pair_at_most_one_line"]
        and checks["all_lines_have_at_least_3_points"]
    )
    return checks


def incidence(blocks, n):
    pc = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            pc[p].append(c)
    return pc


def line_masks(blocks):
    return [sum(1 << p for p in B) for B in blocks]


def enumerate_all_caps(n, blocks, size_limit=None):
    """All caps grouped by cardinality (masks).  DFS in increasing point order.

    With size_limit=k only sizes 0..k are enumerated (no recursion beyond k).
    """
    pc = incidence(blocks, n)
    counts = [0] * len(blocks)
    used = [False] * n
    by_size = [[] for _ in range(n + 1)]

    def rec(mask, size, start):
        by_size[size].append(mask)
        if size_limit is not None and size >= size_limit:
            return
        for p in range(start, n):
            if used[p]:
                continue
            ok = True
            for c in pc[p]:
                if counts[c] >= 2:
                    ok = False
                    break
            if ok:
                used[p] = True
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in pc[p]:
                    counts[c] -= 1
                used[p] = False

    rec(0, 0, 0)
    return by_size


def enumerate_upset(n, blocks, seed_mask):
    """All caps that contain seed_mask, grouped by cardinality (incl. seed)."""
    pc = incidence(blocks, n)
    counts = [0] * len(blocks)
    used = [False] * n
    seed = []
    m = seed_mask
    while m:
        low = m & -m
        p = low.bit_length() - 1
        seed.append(p)
        used[p] = True
        for c in pc[p]:
            counts[c] += 1
        m ^= low
    by_size = [[] for _ in range(n + 1)]

    def rec(mask, size, start):
        by_size[size].append(mask)
        for p in range(start, n):
            if used[p]:
                continue
            ok = True
            for c in pc[p]:
                if counts[c] >= 2:
                    ok = False
                    break
            if ok:
                used[p] = True
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in pc[p]:
                    counts[c] -= 1
                used[p] = False

    rec(seed_mask, len(seed), 0)
    return by_size


def addable_mask(mask, n, lmasks):
    """Points that can be added to the cap `mask` while staying a cap."""
    saturated = 0
    for lm in lmasks:
        if (mask & lm).bit_count() == 2:
            saturated |= lm
    return ((1 << n) - 1) & ~mask & ~saturated


def grundy_all(n, blocks, by_size, want_addable=False):
    """Descending-size DP over a supplied complete list of caps.

    Returns (g, maximal_by_size, addable_by_mask, max_size).
    """
    lmasks = line_masks(blocks)
    g = {}
    maximal = Counter()
    addables = {}
    max_size = max((s for s, v in enumerate(by_size) if v), default=0)
    for size in range(max_size, -1, -1):
        for mask in by_size[size]:
            add = addable_mask(mask, n, lmasks)
            if want_addable:
                addables[mask] = add
            if add == 0:
                maximal[size] += 1
            seen = set()
            a = add
            while a:
                low = a & -a
                seen.add(g[mask | low])
                a ^= low
            mex = 0
            while mex in seen:
                mex += 1
            g[mask] = mex
    return g, maximal, addables, max_size


def bits(mask):
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def mask_of(points):
    m = 0
    for p in points:
        m |= 1 << p
    return m
