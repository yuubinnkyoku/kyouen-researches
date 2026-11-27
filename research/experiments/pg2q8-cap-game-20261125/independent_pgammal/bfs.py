"""Orbit BFS for caps under a verified 2-generator set of PGL(3,8).

Caps are 73-bit integers.  A cap image under a generator is computed with
byte lookup tables (OR of per-point image bits), which is considerably faster
than sorting a 6-tuple in pure Python.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import group as G
from task2_group import GENS

# explicit word for the second generator (from a fixed-seed random search;
# the pair was verified to generate PGL(3,8) by Schreier-Sims)
WORD = [0, 5, 7, 3, 0, 6, 2, 7]


def build_pair():
    g1 = GENS[0]
    g2 = C.IDENT
    for idx in WORD:
        g2 = G.compose(GENS[idx], g2)
    order, base, levels, orbits, trans = G.schreier_sims([g1, g2], C.N)
    assert order == 16482816, order
    return g1, g2


PAIR = build_pair()


def mask_of(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m


def points_of(m):
    out = []
    while m:
        b = m & -m
        out.append(b.bit_length() - 1)
        m ^= b
    return out


def make_apply(perm):
    tabs = []
    for pos in range(10):
        tab = [0] * 256
        for val in range(1, 256):
            lsb = val & -val
            k = lsb.bit_length() - 1
            p = 8 * pos + k
            tab[val] = tab[val ^ lsb] | ((1 << perm[p]) if p < C.N else 0)
        tabs.append(tab)
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9 = tabs

    def apply(m):
        return (t0[m & 255] | t1[(m >> 8) & 255] |
                t2[(m >> 16) & 255] | t3[(m >> 24) & 255] |
                t4[(m >> 32) & 255] | t5[(m >> 40) & 255] |
                t6[(m >> 48) & 255] | t7[(m >> 56) & 255] |
                t8[(m >> 64) & 255] | t9[(m >> 72) & 255])
    return apply


APPLIES = [make_apply(PAIR[0]), make_apply(PAIR[1])]
# the point permutations of the two generators, for collineation checks
GEN_PERMS = [PAIR[0], PAIR[1]]


def apply_perm(perm, m):
    out = 0
    while m:
        b = m & -m
        out |= 1 << perm[b.bit_length() - 1]
        m ^= b
    return out


def orbit_bfs(start_pts, applies=None, progress=0, label=""):
    if applies is None:
        applies = APPLIES
    start = mask_of(start_pts)
    seen = {start}
    orbit = [start]
    add = seen.add
    append = orbit.append
    i = 0
    t0 = time.time()
    while i < len(orbit):
        m = orbit[i]
        i += 1
        for f in applies:
            n = f(m)
            if n not in seen:
                add(n)
                append(n)
        if progress and len(orbit) % progress < 2:
            print(f"    {label}: {len(orbit)} caps  ({time.time()-t0:.1f}s)",
                  flush=True)
    return seen, orbit


def verify_collineation(perm):
    """Check that a point permutation maps every board line to a line."""
    for L in C.LINES:
        img = frozenset(perm[p] for p in L)
        if img not in set(C.LINES):
            return False
    return True


if __name__ == "__main__":
    print("pair orders:",
          [G.schreier_sims([g], C.N)[0] for g in PAIR])
    # check byte table against direct permutation application on random caps
    import random
    rng = random.Random(7)
    for _ in range(200):
        pts = rng.sample(range(C.N), 6)
        m = mask_of(pts)
        for g, f in zip(PAIR, APPLIES):
            assert f(m) == apply_perm(g, m)
    print("byte-table transform matches permutation action")
    print("generators are collineations:",
          [verify_collineation(g) for g in PAIR])
    # small orbit sanity check k=3 (expected 56064)
    t0 = time.time()
    seen, orb = orbit_bfs([2, 3, 10])
    print("k3 orbit size", len(seen), "expected 56064", "%.2fs" % (time.time() - t0))
