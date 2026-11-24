"""Independent verification library for the projective blocking Kyouen experiment.

Written from scratch for the independent audit.  Standard library only; this
module does not import anything from the experiment's own ``scripts/`` and does
not call ``grundy_full.exe``.

Model
-----
A *board* is a finite hypergraph: points ``0..n-1`` and a list of blocks (each a
tuple of points).  For the Kyouen game with the "at most 3 points per block"
rule a set ``S`` of points is *safe* iff ``|S & B| <= cap`` for every block
``B`` (``cap = 3``).

* Normal play: a move adds one point to a safe set; a player with no move loses.
  ``grundy(S) = mex { grundy(S + x) : S + x safe }`` (0 if no move).
* Misere play: a player with no move *wins*.  ``win(S)`` is True iff the player
  to move wins; terminal positions are True by definition.

The module is deliberately small and literal so that the audit is easy to read.
"""

from __future__ import annotations


def bits(mask):
    """Yield the indices of the set bits of ``mask`` (ascending)."""
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def read_board(path):
    """Parse ``<n> <b>`` then ``b`` rows ``<k> p1 ... pk`` (0-based points)."""
    with open(path, "r", encoding="utf-8") as fh:
        rows = [line.split() for line in fh if line.strip()]
    if not rows:
        raise ValueError(f"{path}: empty file")
    n, b = int(rows[0][0]), int(rows[0][1])
    body = rows[1:]
    if len(body) != b:
        raise ValueError(f"{path}: header b={b} but {len(body)} block rows")
    blocks = []
    for row in body:
        k = int(row[0])
        if k != len(row) - 1:
            raise ValueError(f"{path}: malformed block row {row}")
        blocks.append(tuple(int(x) for x in row[1:]))
    return n, blocks


class Board:
    """A finite hypergraph board with the ``<= cap`` safety rule."""

    def __init__(self, n, blocks, cap=3):
        self.n = int(n)
        self.cap = int(cap)
        self.block_masks = []
        seen = set()
        for blk in blocks:
            mask = 0
            for p in blk:
                if not (0 <= p < self.n):
                    raise ValueError(f"point {p} out of range 0..{self.n - 1}")
                mask |= 1 << p
            if mask in seen:          # duplicate block: irrelevant for safety
                continue
            seen.add(mask)
            self.block_masks.append(mask)
        self.blocks = [tuple(bits(m)) for m in self.block_masks]
        self.point_blocks = [[] for _ in range(self.n)]
        for bi, mask in enumerate(self.block_masks):
            for p in bits(mask):
                self.point_blocks[p].append(bi)
        self._counts = [0] * len(self.block_masks)

    # -- basic predicates -------------------------------------------------
    def safe(self, mask):
        cap = self.cap
        for bm in self.block_masks:
            if (mask & bm).bit_count() > cap:
                return False
        return True

    def block_load(self, mask):
        """Popcount of ``mask`` on every block (list indexed like block_masks)."""
        return [(mask & bm).bit_count() for bm in self.block_masks]

    def max_block_load(self, mask):
        best = 0
        for bm in self.block_masks:
            c = (mask & bm).bit_count()
            if c > best:
                best = c
        return best

    # -- exhaustive enumeration of all safe sets --------------------------
    def enumerate_safe(self, collect=False):
        """DFS over safe sets, each generated exactly once.

        Returns ``(sizes, by_size, maximal)`` where ``sizes[k]`` is the number of
        safe sets of size ``k``, ``by_size[k]`` the list of their masks (only if
        ``collect``), and ``maximal`` the list of inclusion-maximal safe sets.
        """
        n, cap = self.n, self.cap
        point_blocks, counts = self.point_blocks, self._counts
        sizes = [0] * (n + 1)
        by_size = [[] for _ in range(n + 1)] if collect else None
        maximal = []

        def can_add(p):
            for bi in point_blocks[p]:
                if counts[bi] >= cap:
                    return False
            return True

        def dfs(mask, start):
            sz = mask.bit_count()
            sizes[sz] += 1
            if collect:
                by_size[sz].append(mask)
            # maximal here means: no point at all can be added
            extendable = False
            for p in range(n):
                if not (mask >> p) & 1 and can_add(p):
                    extendable = True
                    break
            if not extendable:
                maximal.append(mask)
            for p in range(start, n):
                if (mask >> p) & 1:
                    continue
                if can_add(p):
                    for bi in point_blocks[p]:
                        counts[bi] += 1
                    dfs(mask | (1 << p), p + 1)
                    for bi in point_blocks[p]:
                        counts[bi] -= 1

        dfs(0, 0)
        return sizes, by_size, maximal

    # -- brute force over all 2**n subsets ---------------------------------
    def brute_force(self):
        """Return ``(sizes, safe_masks)`` by testing every subset (small n)."""
        sizes = [0] * (self.n + 1)
        safe_masks = []
        for mask in range(1 << self.n):
            if self.safe(mask):
                sizes[mask.bit_count()] += 1
                safe_masks.append(mask)
        return sizes, safe_masks


def grundy_and_misere(board, by_size):
    """Exact Grundy values (normal play) and misere win/lose, all safe sets.

    ``by_size`` must come from :meth:`Board.enumerate_safe` with
    ``collect=True``.  Safe sets are processed by decreasing size so every
    child (a safe superset of size + 1) is already known.
    """
    n, cap = board.n, board.cap
    block_masks, point_blocks = board.block_masks, board.point_blocks
    full = (1 << n) - 1
    grundy = {}
    win = {}
    for k in range(n, -1, -1):
        for mask in by_size[k]:
            load = [(mask & bm).bit_count() for bm in block_masks]
            free = full ^ mask
            child_values = 0          # bit set of Grundy values of the children
            has_move = False
            child_losing = False
            rest = free
            while rest:
                low = rest & -rest
                rest ^= low
                p = low.bit_length() - 1
                ok = True
                for bi in point_blocks[p]:
                    if load[bi] >= cap:
                        ok = False
                        break
                if not ok:
                    continue
                has_move = True
                child = mask | low
                child_values |= 1 << grundy[child]
                if not win[child]:
                    child_losing = True
            g = 0
            while (child_values >> g) & 1:
                g += 1
            grundy[mask] = g
            # misere: terminal position (no move) is a win for the mover
            win[mask] = True if not has_move else child_losing
    return grundy, win


def size_histogram(masks):
    hist = {}
    for mask in masks:
        k = mask.bit_count()
        hist[k] = hist.get(k, 0) + 1
    return dict(sorted(hist.items()))


def complement_profiles(board, maximal):
    """Group maximal safe sets by size and by the line profile of the complement.

    Returns ``{size: {profile: count}}`` where ``profile`` is a tuple of
    ``(intersection_size, number_of_blocks)`` pairs, sorted.
    """
    full = (1 << board.n) - 1
    result = {}
    for s in maximal:
        complement = full ^ s
        hist = {}
        for bm in board.block_masks:
            c = (complement & bm).bit_count()
            hist[c] = hist.get(c, 0) + 1
        profile = tuple(sorted(hist.items()))
        entry = result.setdefault(s.bit_count(), {})
        entry[profile] = entry.get(profile, 0) + 1
    return result


def is_inclusion_minimal_d_fold(board, complement, d):
    """Check a complement set is an inclusion-minimal ``d``-fold blocking set.

    ``d``-fold: every block meets the set in at least ``d`` points.
    Inclusion-minimal: for every point x of the set some block meets the set in
    exactly ``d`` points and contains x.
    """
    block_masks = board.block_masks
    loads = [(complement & bm).bit_count() for bm in block_masks]
    if any(c < d for c in loads):
        return False, "not a d-fold blocking set"
    for p in bits(complement):
        critical = False
        for bi in board.point_blocks[p]:
            if loads[bi] == d:
                critical = True
                break
        if not critical:
            return False, f"point {p} is not critical (not inclusion-minimal)"
    return True, "ok"
