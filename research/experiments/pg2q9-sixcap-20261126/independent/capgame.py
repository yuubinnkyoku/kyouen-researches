"""Cap-game primitives and full upset Grundy DP (independent)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardlib


def bits(mask):
    while mask:
        b = mask & -mask
        yield b
        mask ^= b


def mask_of(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m


def mask_list(mask):
    out = []
    while mask:
        b = mask & -mask
        out.append(b.bit_length() - 1)
        mask ^= b
    return out


class CapGame:
    """Normal-play cap game: a move adds one point while keeping a cap.

    A position with no addable point is terminal (Grundy 0).
    """

    def __init__(self, plane):
        self.plane = plane

    def addable(self, mask):
        return self.plane.addable(mask) & ~mask

    def is_cap(self, mask):
        return self.plane.is_cap(mask)

    def maximal(self, mask):
        return self.addable(mask) == 0

    def children(self, mask):
        return [mask | b for b in bits(self.addable(mask))]

    def upset(self, root):
        """All caps (as masks) that contain `root`, including root itself."""
        seen = {root}
        stack = [root]
        while stack:
            m = stack.pop()
            for child in self.children(m):
                if child not in seen:
                    seen.add(child)
                    stack.append(child)
        return seen

    def grundy_upset(self, root):
        """Exact Grundy value of `root` and of the whole upset.

        All positions of the upset are enumerated first, then evaluated in
        decreasing size order.  This is the full game-tree DP on the upset; it
        uses no structural shortcut.
        """
        caps = self.upset(root)
        order = sorted(caps, key=lambda m: -m.bit_count())
        G = {}
        for m in order:
            vals = set()
            for child in self.children(m):
                if child in caps:
                    vals.add(G[child])
            g = 0
            while g in vals:
                g += 1
            G[m] = g
        return G[root], G, caps

    def maximal_extensions(self, G, caps):
        """Maximal caps in the upset with their size and Grundy value."""
        out = []
        for m in caps:
            if self.maximal(m):
                out.append((m.bit_count(), G[m], m))
        out.sort()
        return out


def load(path=None):
    here = os.path.dirname(os.path.abspath(__file__))
    if path is None:
        path = os.path.normpath(os.path.join(here, boardlib.BOARD_REL))
    n, lines = boardlib.load_board(path)
    return boardlib.Plane(n, lines)
