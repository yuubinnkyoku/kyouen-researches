"""Fast point-set action in pure Python for an independent orbit BFS.

A 73-bit mask is a Python int.  Applying a point permutation with a naive
per-bit loop is slow, so each generator is compiled into five 16-bit chunk
lookup tables: mact(m) = OR_c  TABLE_c[(m >> 16c) & 0xFFFF].  Each table entry
is the image of the 16 points of that chunk.
"""

import pg2q8 as P

NCHUNK = 5  # ceil(73/16)


def _sub8(perm):
    subs = []
    for c in range(10):
        tab = [0] * 256
        for byte in range(256):
            v = 0
            b = byte
            while b:
                low = b & -b
                j = low.bit_length() - 1
                i = 8 * c + j
                if i < 73:
                    v |= 1 << perm[i]
                b ^= low
            tab[byte] = v
        subs.append(tab)
    return subs


def chunk_tables(perm):
    subs = _sub8(perm)
    tabs = []
    for c in range(NCHUNK):
        lo = subs[2 * c]
        hi = subs[2 * c + 1] if 2 * c + 1 < 10 else [0] * 256
        tabs.append([lo[x & 255] | hi[x >> 8] for x in range(65536)])
    return tabs


def apply_tables(t, m):
    return (t[0][m & 0xFFFF]
            | t[1][(m >> 16) & 0xFFFF]
            | t[2][(m >> 32) & 0xFFFF]
            | t[3][(m >> 48) & 0xFFFF]
            | t[4][(m >> 64) & 0xFFFF])


def generator_tables():
    return [chunk_tables(P.matrix_perm(A)) for A in P.GENERATORS]


def orbit_size(tables_list, start):
    seen = {start}
    add = seen.add
    frontier = [start]
    while frontier:
        nxt = []
        push = nxt.append
        for m in frontier:
            for t in tables_list:
                x = (t[0][m & 0xFFFF]
                     | t[1][(m >> 16) & 0xFFFF]
                     | t[2][(m >> 32) & 0xFFFF]
                     | t[3][(m >> 48) & 0xFFFF]
                     | t[4][(m >> 64) & 0xFFFF])
                if x not in seen:
                    add(x)
                    push(x)
        frontier = nxt
    return len(seen)


def orbit_elements(tables_list, start):
    seen = {start}
    add = seen.add
    frontier = [start]
    while frontier:
        nxt = []
        push = nxt.append
        for m in frontier:
            for t in tables_list:
                x = (t[0][m & 0xFFFF]
                     | t[1][(m >> 16) & 0xFFFF]
                     | t[2][(m >> 32) & 0xFFFF]
                     | t[3][(m >> 48) & 0xFFFF]
                     | t[4][(m >> 64) & 0xFFFF])
                if x not in seen:
                    add(x)
                    push(x)
        frontier = nxt
    return seen


def mask_of(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m


def points_of(m):
    out = []
    b = m
    while b:
        low = b & -b
        out.append(low.bit_length() - 1)
        b ^= low
    return out
