"""Shared pure-stdlib helpers for the independent decomposition check.

Board: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt
Game:  s=2 cap game on AG(2,7).  A set S is safe iff |S cap L| <= 2 for every
board line L.  Points are 0..48, lines are given explicitly.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENT = HERE.parent
REPO = HERE.parents[3]
BOARD_PATH = REPO / "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt"
REFERENCE_PATH = EXPERIMENT / "output/grundy_ag2q7_s2.txt"
STATS_PATH = REPO / "research/experiments/s-parameter-kyouen-20261125/output/stats_ag2q7_s2.txt"


def read_board(path=BOARD_PATH):
    """Return (n, m, blocks); validate the literal file shape."""
    raw = Path(path).read_text(encoding="utf-8").splitlines()
    rows = [ln.strip() for ln in raw if ln.strip()]
    n, m = (int(t) for t in rows[0].split())
    blocks = []
    for ln in rows[1:]:
        vals = [int(t) for t in ln.split()]
        assert vals[0] == len(vals) - 1, f"bad block header: {ln}"
        blocks.append(vals[1:])
    assert len(blocks) == m, f"header says {m} lines, file has {len(blocks)}"
    return n, m, blocks


class Board:
    """Bitmask representation of the affine plane and its line system."""

    def __init__(self, n, blocks):
        self.n = n
        self.blocks = [tuple(b) for b in blocks]
        self.m = len(blocks)
        self.FULL = (1 << n) - 1
        self.line_masks = [sum(1 << p for p in B) for B in self.blocks]
        # pair_line[a][b] = mask of the unique line through a and b
        self.pair_line = [[0] * n for _ in range(n)]
        for lm, B in zip(self.line_masks, self.blocks):
            for i, a in enumerate(B):
                for b in B[i + 1:]:
                    self.pair_line[a][b] = lm
                    self.pair_line[b][a] = lm
        self.lines_through = [[] for _ in range(n)]
        for li, B in enumerate(self.blocks):
            for p in B:
                self.lines_through[p].append(li)

    def forbidden(self, mask):
        """Points p such that mask + p is unsafe (some line through p has 2 of mask)."""
        f = 0
        pl = self.pair_line
        bits = []
        m = mask
        while m:
            b = m & -m
            bits.append(b.bit_length() - 1)
            m ^= b
        for i, a in enumerate(bits):
            pa = pl[a]
            for b in bits[i + 1:]:
                f |= pa[b]
        return f

    def addable(self, mask, forbidden=None):
        if forbidden is None:
            forbidden = self.forbidden(mask)
        return self.FULL & ~mask & ~forbidden

    def extend_forbidden(self, forbidden, mask, p):
        """forbidden for mask | 1<<p given forbidden of mask (p addable)."""
        f = forbidden
        pl = self.pair_line
        m = mask
        while m:
            b = m & -m
            f |= pl[p][b.bit_length() - 1]
            m ^= b
        return f

    def is_safe(self, mask):
        """Direct definition: every line meets mask in at most 2 points."""
        return all((mask & lm).bit_count() <= 2 for lm in self.line_masks)


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def popcount(x):
    return x.bit_count()
