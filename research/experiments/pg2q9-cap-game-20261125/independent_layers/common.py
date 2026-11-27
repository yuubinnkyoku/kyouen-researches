"""Shared utilities for the independent verification of K1351 (PG(2,9) cap layers).

Everything here is written from scratch for this verification.  Python stdlib
only.  The only external inputs are the board / census / conic-layer / results
files of the parent experiments, which are read (never written).

Board convention: a file with first line "n b", then b lines "10 p1 ... p10"
(0-based point labels).  A position is an n-bit integer mask.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# GF(9) = GF(3)[i]/(i^2+1), elements as integers 3*a+b for a + b*i.
# ---------------------------------------------------------------------------

ELEMS = list(range(9))
ZERO = 0
ONE = 3  # 3 encodes 1 + 0*i (elements are 3*a+b for a + b*i)
TWO = 6  # 6 encodes 2 + 0*i (also -1)


def gf_add(a: int, b: int) -> int:
    return 3 * (((a // 3) + (b // 3)) % 3) + (((a % 3) + (b % 3)) % 3)


def gf_neg(a: int) -> int:
    return 3 * ((-(a // 3)) % 3) + ((-(a % 3)) % 3)


def gf_mul(a: int, b: int) -> int:
    a0, a1 = a // 3, a % 3
    b0, b1 = b // 3, b % 3
    return 3 * ((a0 * b0 - a1 * b1) % 3) + ((a0 * b1 + a1 * b0) % 3)


def gf_inv(a: int) -> int:
    for b in ELEMS:
        if gf_mul(a, b) == ONE:
            return b
    raise ZeroDivisionError(a)


ADD = [[gf_add(a, b) for b in ELEMS] for a in ELEMS]
MUL = [[gf_mul(a, b) for b in ELEMS] for a in ELEMS]
NEG = [gf_neg(a) for a in ELEMS]
INV = [0] + [gf_inv(a) for a in ELEMS[1:]]
SUB = [[ADD[a][NEG[b]] for b in ELEMS] for a in ELEMS]


# Standard homogeneous coordinates used by the parent construction, mapping the
# board point labels to vectors of GF(9)^3.  The identity map on labels is
# verified below to be an incidence isomorphism to the standard PG(2,9).
def standard_points():
    pts = [None] * 91
    pts[0] = (ZERO, ZERO, ONE)
    for j in range(9):
        pts[1 + j] = (ZERO, ONE, j)
    for p in range(9):
        for j in range(9):
            pts[10 + 9 * p + j] = (ONE, p, j)
    return pts


def canon_vec(v):
    for x in v:
        if x != ZERO:
            ix = INV[x]
            return tuple(MUL[ix][z] for z in v)
    return None


def standard_pg():
    """Build PG(2,9) from GF(9): 91 points, 91 lines (as point masks).

    Returns (pts, line_masks) where pts maps the board point labels to the
    standard homogeneous coordinate vectors.
    """
    pts = standard_points()
    # the coordinate labelling must be a bijection
    assert len({canon_vec(v) for v in pts}) == 91
    assert all(canon_vec(v) == v for v in pts)
    forms: list[tuple[int, int, int]] = []
    for a in ELEMS:
        for b in ELEMS:
            for c in ELEMS:
                if (a, b, c) == (ZERO, ZERO, ZERO):
                    continue
                if next(x for x in (a, b, c) if x != ZERO) != ONE:
                    continue
                forms.append((a, b, c))
    assert len(forms) == 91
    lines = []
    for a, b, c in forms:
        mask = 0
        for i, (x, y, z) in enumerate(pts):
            val = ADD[ADD[MUL[a][x]][MUL[b][y]]][MUL[c][z]]
            if val == ZERO:
                mask |= 1 << i
        lines.append(mask)
    assert len(set(lines)) == 91
    assert all(m.bit_count() == 10 for m in lines)
    return pts, lines


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------

class Board:
    def __init__(self, n: int, blocks: list[tuple[int, ...]]):
        self.n = n
        self.blocks = blocks
        self.full = (1 << n) - 1
        self.line_masks = []
        for B in blocks:
            m = 0
            for p in B:
                m |= 1 << p
            self.line_masks.append(m)
        self.point_lines: list[list[int]] = [[] for _ in range(n)]
        for c, B in enumerate(blocks):
            for p in B:
                self.point_lines[p].append(c)
        self.line_of = [[-1] * n for _ in range(n)]
        for c, B in enumerate(blocks):
            for p in B:
                row = self.line_of[p]
                for q in B:
                    row[q] = c
        self.adj_line_union = [[0] * n for _ in range(n)]
        for p in range(n):
            row = self.adj_line_union[p]
            for q in range(n):
                if p != q:
                    row[q] = self.line_masks[self.line_of[p][q]]

    # -- basic predicates ---------------------------------------------------
    def is_cap(self, mask: int) -> bool:
        for L in self.line_masks:
            if (mask & L).bit_count() > 2:
                return False
        return True

    def blocked_mask(self, mask: int) -> int:
        """Points lying on a secant line of ``mask`` (includes mask points)."""
        blocked = 0
        pts = bits(mask)
        for i in range(len(pts)):
            p = pts[i]
            row = self.adj_line_union[p]
            for j in range(i + 1, len(pts)):
                blocked |= row[pts[j]]
        return blocked

    def addable_mask(self, mask: int) -> int:
        return self.full & ~(mask | self.blocked_mask(mask))

    def addable_points(self, mask: int) -> list[int]:
        return bits(self.addable_mask(mask))

    # -- upset / Grundy -----------------------------------------------------
    def upset(self, mask: int) -> list[int]:
        """All caps containing ``mask`` (each exactly once), including itself."""
        n = self.n
        pc = self.point_lines
        counts = [0] * len(self.blocks)
        used = [False] * n
        for p in bits(mask):
            used[p] = True
            for c in pc[p]:
                counts[c] += 1
        order: list[int] = []

        def rec(m: int, start: int) -> None:
            order.append(m)
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
                    rec(m | (1 << p), p + 1)
                    for c in pc[p]:
                        counts[c] -= 1
                    used[p] = False

        rec(mask, 0)
        return order

    def grundy_analysis(self, mask: int) -> dict:
        """Full Grundy value of ``mask`` by DP over its upset.

        Also records the maximal elements of the upset (the maximal caps that
        contain ``mask``) and their sizes, and the Grundy values of the
        immediate children.
        """
        assert self.is_cap(mask)
        order = self.upset(mask)
        ss = set(order)
        g: dict[int, int] = {}
        for m in sorted(order, key=lambda x: -x.bit_count()):
            avail = self.full ^ m
            vals = set()
            while avail:
                b = avail & -avail
                nm = m | b
                if nm in ss:
                    vals.add(g[nm])
                avail ^= b
            v = 0
            while v in vals:
                v += 1
            g[m] = v
        # immediate children of the root
        child_vals = []
        child_caps = []
        avail = self.full ^ mask
        while avail:
            b = avail & -avail
            nm = mask | b
            if nm in ss:
                child_caps.append(nm)
                child_vals.append(g[nm])
            avail ^= b
        # maximal elements of the upset
        maximal = []
        for m in order:
            avail = self.full ^ m
            ismax = True
            while avail:
                b = avail & -avail
                if (m | b) in ss:
                    ismax = False
                    break
                avail ^= b
            if ismax:
                maximal.append(m)
        sizes = sorted({m.bit_count() for m in maximal})
        parities = sorted({s % 2 for s in sizes})
        return {
            "grundy": g[mask],
            "upset_size": len(order),
            "child_count": len(child_caps),
            "child_grundy_values": sorted(child_vals),
            "maximal_sizes": sizes,
            "maximal_counts": {
                str(s): sum(1 for m in maximal if m.bit_count() == s) for s in sizes
            },
            "maximal_grundy_values": sorted({g[m] for m in maximal}),
            "parities": parities,
            "parity_uniform": len(parities) == 1,
            "terminal": not child_caps,
            "cap_size": mask.bit_count(),
            "cap": bits(mask),
        }


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def bits(mask: int) -> list[int]:
    out = []
    while mask:
        b = mask & -mask
        out.append(b.bit_length() - 1)
        mask ^= b
    return out


def load_board(path: Path) -> Board:
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = [tuple(map(int, ln.split()[1:])) for ln in lines[1:]]
    assert len(blocks) == b
    return Board(n, blocks)
