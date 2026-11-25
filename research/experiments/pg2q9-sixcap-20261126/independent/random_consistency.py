"""Consistency of the structural Grundy formula against full upset DP.

For random 6-caps (uniform over 6-caps by rejection sampling) compare
  * G_struct = 0 if no addable point; 1 if every child is terminal;
               2 if some child is terminal and some child is not; 0 if no
               child is terminal (mex{1}=0),
    which uses G(7-cap) = 0 (terminal) / 1 (non-terminal), and
  * G_dp, the exact Grundy value from the full upset DP.
It also checks inside each upset that every 7-cap has G=0 (terminal) or G=1.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capgame

SAMPLES = 200


def random_6_cap(plane, rng):
    while True:
        pts = rng.sample(range(91), 6)
        m = capgame.mask_of(pts)
        if plane.is_cap(m):
            return m


def main():
    plane = capgame.load()
    game = capgame.CapGame(plane)
    rng = random.Random(424242)

    mismatches = []
    gstat = {}
    extstat = {}
    child_value_bad = 0
    child_checked = 0
    n_with_max = 0
    seen = set()
    while len(seen) < SAMPLES:
        X = random_6_cap(plane, rng)
        if X in seen:
            continue
        seen.add(X)
        add = game.addable(X)
        e = add.bit_count()
        nMax = 0
        for b in capgame.bits(add):
            if plane.addable(X | b) == 0:
                nMax += 1
        if e == 0:
            gs = 0
        elif nMax == e:
            gs = 1
        elif nMax > 0:
            gs = 2
        else:
            gs = 0
        if nMax > 0:
            n_with_max += 1

        gd, G, caps = game.grundy_upset(X)
        # inside the upset, every 7-cap must have G equal to 0/1 by terminality
        for m, gg in G.items():
            if m.bit_count() == 7:
                child_checked += 1
                want = 0 if game.maximal(m) else 1
                if gg != want:
                    child_value_bad += 1
        if gd != gs:
            mismatches.append((X, e, nMax, gs, gd))
        gstat[gs] = gstat.get(gs, 0) + 1
        extstat[e] = extstat.get(e, 0) + 1

    print("samples: %d distinct random 6-caps" % len(seen))
    print("Grundy distribution (exact upset DP): %s"
          % dict(sorted(gstat.items())))
    print("|addable| distribution: %s" % dict(sorted(extstat.items())))
    print("sampled 6-caps with a maximal 7-child: %d" % n_with_max)
    print("7-caps checked inside the upsets: %d, with wrong G: %d"
          % (child_checked, child_value_bad))
    print("structural-vs-DP mismatches: %d" % len(mismatches))
    for X, e, nMax, gs, gd in mismatches[:10]:
        print("  X=%s ext=%d nMax=%d struct=%d dp=%d"
              % (capgame.mask_list(X), e, nMax, gs, gd))
    ok = (not mismatches) and child_value_bad == 0
    print("\nconsistency: %s" % ("PASS" if ok else "FAIL"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
