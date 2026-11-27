"""Find a small generating set of PGL(3,8) from our elementary generators and
benchmark the cap-image kernels used by the orbit BFS."""
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import group as G
from task2_group import GENS, NAMES

rng = random.Random(20261125)


def random_element(depth=6):
    p = C.IDENT
    for _ in range(depth):
        p = G.compose(GENS[rng.randrange(len(GENS))], p)
    return p


def find_two_generators():
    pool = [GENS[0], GENS[1], GENS[2], GENS[3], GENS[4], GENS[5],
            GENS[6], GENS[7]]
    for _ in range(40):
        pool.append(random_element(rng.randint(2, 8)))
    best = None
    t0 = time.time()
    trials = 0
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            trials += 1
            order, base, levels, orbits, trans = G.schreier_sims(
                [pool[i], pool[j]], C.N)
            if order == 16482816:
                print("found pair", i, j, "after", trials, "trials",
                      "%.2fs" % (time.time() - t0))
                return pool[i], pool[j]
    print("no pair found", trials, "trials", "%.2fs" % (time.time() - t0))
    return None


def make_apply_loop(perm):
    img = [1 << perm[p] for p in range(C.N)]

    def apply(mask):
        m = 0
        while mask:
            b = mask & -mask
            m |= img[b.bit_length() - 1]
            mask ^= b
        return m
    return apply


def make_apply_bytes(perm):
    tabs = []
    for pos in range(10):
        tab = [0] * 256
        for val in range(1, 256):
            lsb = val & -val
            k = lsb.bit_length() - 1
            p = 8 * pos + k
            prev = tab[val ^ lsb]
            tab[val] = prev | ((1 << perm[p]) if p < C.N else 0)
        tabs.append(tab)
    t0, t1, t2, t3, t4, t5, t6, t7, t8, t9 = tabs

    def apply(mask):
        return (t0[mask & 255] | t1[(mask >> 8) & 255] |
                t2[(mask >> 16) & 255] | t3[(mask >> 24) & 255] |
                t4[(mask >> 32) & 255] | t5[(mask >> 40) & 255] |
                t6[(mask >> 48) & 255] | t7[(mask >> 56) & 255] |
                t8[(mask >> 64) & 255] | t9[(mask >> 72) & 255])
    return apply


def mask_of(points):
    m = 0
    for p in points:
        m |= 1 << p
    return m


if __name__ == "__main__":
    pair = find_two_generators()
    if pair is None:
        sys.exit(1)
    g1, g2 = pair
    for nm, g in [("g1", g1), ("g2", g2)]:
        print(nm, "order check via ss:",
              G.schreier_sims([g], C.N)[0])

    # benchmark transforms
    caps = [mask_of([rng.randrange(73) for _ in range(6)])
            for _ in range(20000)]
    for name, maker, perm in [("loop g1", make_apply_loop, g1),
                              ("loop g2", make_apply_loop, g2),
                              ("bytes g1", make_apply_bytes, g1)]:
        f = maker(perm)
        t0 = time.time()
        acc = 0
        reps = 20
        for _ in range(reps):
            for m in caps:
                acc ^= f(m)
        dt = time.time() - t0
        print(f"{name}: {reps*len(caps)/dt/1e6:.2f} M transforms/s "
              f"({dt*1e6/(reps*len(caps)):.3f} us each) checksum={acc & 1}")
