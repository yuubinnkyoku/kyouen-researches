"""Exact cap-game machinery: caps, secant masks, upsets, Grundy DP, census."""

from __future__ import annotations

import itertools
from collections import Counter

import pg

ALL_POINTS = 0
N_POINTS = 91


def mex(values):
    g = 0
    while g in values:
        g += 1
    return g


class CapGame:
    def __init__(self, n, blocks):
        self.n = n
        self.blocks = [tuple(B) for B in blocks]
        self.all_mask = (1 << n) - 1
        # line index of a point pair
        self.line_of_pair = {}
        for li, B in enumerate(self.blocks):
            for a, b in itertools.combinations(B, 2):
                self.line_of_pair[(a, b) if a < b else (b, a)] = li
        # line bit masks
        self.line_mask = []
        for B in self.blocks:
            m = 0
            for p in B:
                m |= 1 << p
            self.line_mask.append(m)
        # pair -> line mask, as a full symmetric table for speed
        self.pair_mask = [[0] * n for _ in range(n)]
        self.pair_line = [[-1] * n for _ in range(n)]
        for (a, b), li in self.line_of_pair.items():
            cm = self.line_mask[li]
            self.pair_mask[a][b] = cm
            self.pair_mask[b][a] = cm
            self.pair_line[a][b] = li
            self.pair_line[b][a] = li

    # -- basic cap operations ------------------------------------------------
    def is_cap(self, mask):
        # every pair of cap points spans a distinct line
        pts = bits(mask)
        seen = set()
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                li = self.pair_line[pts[i]][pts[j]]
                if li in seen:
                    return False
                seen.add(li)
        return True

    def secant_union(self, mask):
        pts = bits(mask)
        u = 0
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                u |= self.pair_mask[pts[i]][pts[j]]
        return u

    def available(self, mask):
        return self.all_mask & ~self.secant_union(mask) & ~mask

    def available_fast(self, mask, union):
        return self.all_mask & ~union & ~mask

    # -- enumeration of all caps containing a base cap ----------------------
    def enumerate_upset(self, base_mask):
        """Return levels[k] = list of (cap_mask, secant_union_mask).

        Every cap containing base_mask is produced exactly once: the added
        points are chosen in strictly increasing point order.  The secant
        union is maintained incrementally.
        """
        base = tuple(bits(base_mask))
        assert self.is_cap(base_mask), "base is not a cap"
        base_union = self.secant_union(base_mask)
        levels = {len(base): [(base_mask, base_union)]}

        def rec(mask, union, last):
            k = mask.bit_count()
            avail = self.all_mask & ~union & ~mask
            # canonical order: only points greater than the last added one
            if last + 1:
                avail &= ~((1 << (last + 1)) - 1)
            while avail:
                b = avail & -avail
                avail ^= b
                p = b.bit_length() - 1
                # union of the new secants p-q for q in current cap
                add = 0
                mm = mask
                pm = self.pair_mask[p]
                while mm:
                    qb = mm & -mm
                    mm ^= qb
                    q = qb.bit_length() - 1
                    add |= pm[q]
                nm = mask | b
                nu = union | add
                levels.setdefault(k + 1, []).append((nm, nu))
                rec(nm, nu, p)

        rec(base_mask, base_union, -1)
        return levels

    # -- full Grundy DP over an enumerated upset ----------------------------
    def grundy_dp(self, base_mask):
        levels = self.enumerate_upset(base_mask)
        return self.grundy_from_levels(levels), levels

    def grundy_from_levels(self, levels):
        g = {}
        maxk = max(levels)
        for k in range(maxk, -1, -1):
            for mask, union in levels.get(k, ()):
                avail = self.all_mask & ~union & ~mask
                vals = set()
                while avail:
                    b = avail & -avail
                    avail ^= b
                    child = mask | b
                    vals.add(g[child])
                g[mask] = mex(vals)
        return g

    def child_grundy_counts(self, mask, union, g):
        """Counter of Grundy values of the immediate children of a cap."""
        avail = self.all_mask & ~union & ~mask
        c = Counter()
        while avail:
            b = avail & -avail
            avail ^= b
            c[g[mask | b]] += 1
        return c

    # -- random caps ---------------------------------------------------------
    def random_cap(self, k, rng):
        mask = 0
        union = 0
        for _ in range(k):
            avail = self.all_mask & ~union & ~mask
            if not avail:
                break
            pts = bits(avail)
            p = pts[rng.randrange(len(pts))]
            b = 1 << p
            # update union
            mm = mask
            pm = self.pair_mask[p]
            while mm:
                qb = mm & -mm
                mm ^= qb
                q = qb.bit_length() - 1
                union |= pm[q]
            mask |= b
        return mask


def bits(mask):
    out = []
    while mask:
        b = mask & -mask
        mask ^= b
        out.append(b.bit_length() - 1)
    return out


# ---------------------------------------------------------------------------
# Frame census and Grundy global distribution
# ---------------------------------------------------------------------------


def frame_census(game, frame, expected_sizes=None):
    """Enumerate all caps containing the 4-cap `frame`.

    Returns a dict with:
      levels: {k: [(mask, union), ...]}
      T: {k: number of caps containing frame}
      maximal: {k: number of maximal caps containing frame}
      G: {mask: grundy} for every cap in the cone
      grundy_dist: {k: Counter({g: count})}
      child_dist: {k: Counter({(child_g, count)})} summed over caps
    """
    frame_mask = 0
    for p in frame:
        frame_mask |= 1 << p
    assert frame_mask.bit_count() == 4
    assert game.is_cap(frame_mask)
    levels = game.enumerate_upset(frame_mask)
    g = game.grundy_from_levels(levels)
    T = {}
    maximal = {}
    grundy_dist = {}
    child_dist = {}
    for k, states in levels.items():
        T[k] = len(states)
        maximal[k] = 0
        grundy_dist[k] = Counter()
        child_dist[k] = Counter()
        for mask, union in states:
            grundy_dist[k][g[mask]] += 1
            avail = game.all_mask & ~union & ~mask
            if not avail:
                maximal[k] += 1
            else:
                c = game.child_grundy_counts(mask, union, g)
                for cg, cnt in c.items():
                    child_dist[k][cg] += cnt
    return {
        "frame": list(frame),
        "levels": levels,
        "T": T,
        "maximal": maximal,
        "G": g,
        "grundy_dist": grundy_dist,
        "child_dist": child_dist,
    }


def double_count(through_f, n_frames, k, choose4_table=None):
    """Global count from a per-frame count, via frame double counting."""
    import math

    c = math.comb(k, 4)
    assert through_f * n_frames % c == 0, (through_f, n_frames, k, c)
    return through_f * n_frames // c
