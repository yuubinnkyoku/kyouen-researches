"""Cone/upset enumeration and Grundy DP for the AG(2,9) s=2 cap game.

This module is written from scratch for the independent verification.  It
implements two independent enumerators:

  enumerate_cone_fast    : DFS with incremental line counters and an availability
                           bitmask (fast; used for the main cone computation)
  enumerate_upset_scratch: DFS with a from-scratch "safe(p, mask)" test and an
                           arbitrary point order (slow; used as an independent
                           cross-check and for per-cap upset DPs)

Both enumerate exactly the caps (sets with |S cap L| <= 2 for every line) that
contain a given base cap.
"""


def build_point_lines(n, block_masks):
    pl = [[] for _ in range(n)]
    for ci, m in enumerate(block_masks):
        mm = m
        while mm:
            b = mm & -mm
            pl[b.bit_length() - 1].append(ci)
            mm ^= b
    return pl


def is_cap_mask(mask, block_masks):
    return all((mask & m).bit_count() <= 2 for m in block_masks)


def enumerate_cone_fast(n, block_masks, point_lines, base):
    """All caps containing ``base`` (which must be a cap), increasing point order."""
    nlines = len(block_masks)
    cnt = [0] * nlines
    blockcnt = [0] * n
    used = base
    avail = ((1 << n) - 1) & ~base

    mm = base
    while mm:
        b = mm & -mm
        p = b.bit_length() - 1
        for c in point_lines[p]:
            cnt[c] += 1
        mm ^= b
    for c in range(nlines):
        if cnt[c] >= 2:
            qq = block_masks[c]
            while qq:
                bb = qq & -qq
                q = bb.bit_length() - 1
                blockcnt[q] += 1
                if blockcnt[q] == 1:
                    avail &= ~bb
                qq ^= bb

    out = []

    def rec(mask, start):
        nonlocal avail
        out.append(mask)
        cand = avail & ~((1 << start) - 1)
        while cand:
            b = cand & -cand
            cand ^= b
            p = b.bit_length() - 1
            avail &= ~b
            for c in point_lines[p]:
                cnt[c] += 1
                if cnt[c] == 2:
                    qq = block_masks[c]
                    while qq:
                        bb = qq & -qq
                        q = bb.bit_length() - 1
                        blockcnt[q] += 1
                        if blockcnt[q] == 1:
                            avail &= ~bb
                        qq ^= bb
            rec(mask | b, p + 1)
            for c in point_lines[p]:
                cnt[c] -= 1
                if cnt[c] == 1:
                    qq = block_masks[c]
                    while qq:
                        bb = qq & -qq
                        q = bb.bit_length() - 1
                        blockcnt[q] -= 1
                        if blockcnt[q] == 0:
                            avail |= bb
                        qq ^= bb
            avail |= b
            avail &= ~mask

    rec(base, 0)
    return out


def enumerate_upset_scratch(n, block_masks, point_lines, base, order):
    """All caps containing ``base``, using a from-scratch safety test.

    ``order`` is any permutation of range(n); the DFS adds points in that order
    (only points after the previous one) so each superset is generated once.
    """
    caps = set()

    def safe_add(mask, p):
        for c in point_lines[p]:
            if (mask & block_masks[c]).bit_count() >= 2:
                return False
        return True

    def rec(mask, start):
        caps.add(mask)
        for k in range(start, n):
            p = order[k]
            if (mask >> p) & 1:
                continue
            if safe_add(mask, p):
                rec(mask | (1 << p), k + 1)

    rec(base, 0)
    return caps


def grundy_dp(caps, n):
    """Grundy value of every position in ``caps`` (a cone/upset, closed under moves).

    Processed in decreasing size; the children of a cap are the caps obtained by
    adding one point that is safe, equivalently the supersets present in ``caps``.
    """
    capset = set(caps)
    by_size = {}
    for m in capset:
        by_size.setdefault(m.bit_count(), []).append(m)
    g = {}
    for s in sorted(by_size, reverse=True):
        for m in by_size[s]:
            seen = set()
            rest = ((1 << n) - 1) & ~m
            while rest:
                b = rest & -rest
                rest ^= b
                nm = m | b
                if nm in capset:
                    seen.add(g[nm])
            v = 0
            while v in seen:
                v += 1
            g[m] = v
    return g


def size_grundy_counts(g):
    """Counter of (size, grundy) -> count, and size -> count."""
    sizes = {}
    dist = {}
    for m, v in g.items():
        s = m.bit_count()
        sizes[s] = sizes.get(s, 0) + 1
        dist.setdefault(s, {})
        dist[s][v] = dist[s].get(v, 0) + 1
    return sizes, dist
