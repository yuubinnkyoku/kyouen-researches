"""Shared helpers for the independent verification of the W_24 s-parameter game.

Independent re-implementation, Python standard library only.
Reads the board from the sibling experiment directory (read-only).
All outputs are written under this directory.
"""

from __future__ import annotations

import itertools
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
# HERE = research/experiments/witt-s-spectrum-20261125/independent
EXPERIMENTS = HERE.parents[1]                      # research/experiments
BOARD_PATH = EXPERIMENTS / "design-kyouen-witt-20261125" / "output" / "board_w24.txt"
OUT_DIR = HERE / "out"

N = 24
B = 759


def load_board(path: pathlib.Path | None = None):
    """Return (header, octads) where octads is a list of sorted 8-tuples."""
    path = BOARD_PATH if path is None else path
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    header = [int(x) for x in lines[0].split()]
    if header != [N, B]:
        raise SystemExit(f"unexpected header {header!r}")
    octads = []
    for ln in lines[1:]:
        vals = [int(x) for x in ln.split()]
        if len(vals) != 9 or vals[0] != 8:
            raise SystemExit(f"bad octad line: {ln!r}")
        pts = tuple(sorted(vals[1:]))
        if len(set(pts)) != 8 or pts[0] < 0 or pts[-1] >= N:
            raise SystemExit(f"bad octad: {ln!r}")
        octads.append(pts)
    if len(octads) != B:
        raise SystemExit(f"expected {B} octads, got {len(octads)}")
    return header, octads


def octad_masks(octads):
    return [sum(1 << p for p in o) for o in octads]


def points_of(mask):
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def thru_lists(octads):
    """thru[p] = tuple of octad indices containing p; pts[B] = tuple of points."""
    thru = [[] for _ in range(N)]
    for bi, o in enumerate(octads):
        for p in o:
            thru[p].append(bi)
    return [tuple(x) for x in thru], [tuple(o) for o in octads]


def enumerate_safe(s: int, octads, thru, pts, collect=True):
    """Enumerate every safe set (|S cap B| <= s for all octads) exactly once.

    Builds each set in increasing point order, so the DFS tree has exactly one
    node per safe set.  Incremental state: cnt[B] = |S cap B|, bad[p] = number
    of octads through p with cnt[B] == s (a saturated octad through p makes p
    unplayable).

    Returns dict with per-size mask lists and per-size maximal counts.
    """
    masks_by_size = [[] for _ in range(N + 1)]
    maximal = [0] * (N + 1)
    cnt = [0] * B
    bad = [0] * N
    S = 0

    def dfs(last: int, size: int):
        nonlocal S
        masks_by_size[size].append(S)
        m = 1
        for p in range(N):
            if not (S >> p) & 1 and bad[p] == 0:
                m = 0
                break
        if m:
            maximal[size] += 1
        for p in range(last + 1, N):
            if bad[p]:
                continue
            S |= 1 << p
            changed = []
            for bi in thru[p]:
                cnt[bi] += 1
                if cnt[bi] == s:
                    changed.append(bi)
                    for q in pts[bi]:
                        bad[q] += 1
            dfs(p, size + 1)
            S ^= 1 << p
            for bi in changed:
                for q in pts[bi]:
                    bad[q] -= 1
            for bi in thru[p]:
                cnt[bi] -= 1

    import sys
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(10000)
    try:
        dfs(-1, 0)
    finally:
        sys.setrecursionlimit(old)
    return {"by_size": masks_by_size, "maximal": maximal}


def safe_mask(mask: int, s: int, oct_masks) -> bool:
    return all((mask & om).bit_count() <= s for om in oct_masks)


def grundy_misere(by_size, s, oct_masks, max_size=None):
    """Full DP over the enumerated safe positions.

    Returns (grundy[25][?] distribution, misere distribution, root_g, root_m).
    Uses bytearrays indexed by the 24-bit mask (16 MiB each) as the value
    tables, which is independent of the original engine's data structures.
    """
    if max_size is None:
        max_size = max(k for k, v in enumerate(by_size) if v)
    gtab = bytearray(1 << N)          # grundy + 1, 0 = unsafe/unset
    mtab = bytearray(1 << N)          # misere + 1, 0 = unsafe/unset
    for k in range(max_size + 1):
        for m in by_size[k]:
            gtab[m] = 1               # placeholder (all safe positions size k)
            mtab[m] = 1
    gdist = [dict() for _ in range(max_size + 1)]
    mdist = [dict() for _ in range(max_size + 1)]
    for k in range(max_size, -1, -1):
        for m in by_size[k]:
            seen = 0
            has_child = False
            has_m0 = False
            for p in range(N):
                bit = 1 << p
                if m & bit:
                    continue
                child = m | bit
                v = gtab[child]
                if v:
                    has_child = True
                    seen |= 1 << (v - 1)
                w = mtab[child]
                if w:
                    if w == 1:
                        has_m0 = True
            # mex
            g = 0
            while (seen >> g) & 1:
                g += 1
            gtab[m] = g + 1
            gdist[k][g] = gdist[k].get(g, 0) + 1
            if not has_child:
                mv = 1                     # misere: no move wins
            elif has_m0:
                mv = 1                     # move to a misere loss for opponent
            else:
                mv = 0
            mtab[m] = mv + 1
            mdist[k][mv] = mdist[k].get(mv, 0) + 1
    return gdist, mdist, gtab[0] - 1, mtab[0] - 1, gtab, mtab


def dodecads_from_octad_pairs(octads):
    """All symmetric differences of octad pairs meeting in exactly 2 points."""
    masks = octad_masks(octads)
    out = set()
    for i in range(B):
        a = masks[i]
        for j in range(i + 1, B):
            b = masks[j]
            if (a & b).bit_count() == 2:
                out.add(a ^ b)
    return out


def golay_basis(octads):
    """F2 span of the octad incidence vectors; returns (rank, basis rows)."""
    basis = {}                        # pivot bit -> row
    for m in octad_masks(octads):
        x = m
        while x:
            piv = x.bit_length() - 1
            if piv in basis:
                x ^= basis[piv]
            else:
                basis[piv] = x
                break
    rows = list(basis.values())
    return len(rows), rows


def all_codewords(rows):
    words = [0]
    for r in rows:
        words += [w ^ r for w in words]
    return words
