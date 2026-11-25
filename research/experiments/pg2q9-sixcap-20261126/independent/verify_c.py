"""Task 3: full Grundy value of six-subsets of complete 7-arcs by upset DP.

For several six-subsets X = A - {p} (A a complete 7-arc) the whole upset
({caps containing X}) is enumerated and its Grundy values are computed bottom-up
(size descending).  This uses no structural shortcut for 7-/8-/9-/10-caps: the
legality of every move is recomputed from the board incidence.

Also evaluates the parent repository's earlier Grundy-2 witness
X = {0,1,10,20,32,39}.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capgame

KNOWN_ARCS = [
    [3, 25, 26, 31, 37, 39, 75],
    [16, 47, 51, 56, 60, 80, 82],
    [33, 39, 57, 70, 74, 80, 89],
    [10, 20, 29, 32, 64, 66, 76],   # found by random greedy in verify_b.py
]
WITNESS = [0, 1, 10, 20, 32, 39]


def mex(vals):
    g = 0
    while g in vals:
        g += 1
    return g


def random_greedy_maximal(plane, rng):
    cap = 0
    while True:
        add = plane.addable(cap) & ~cap
        if add == 0:
            return cap
        cap |= rng.choice(list(capgame.bits(add)))


def report(game, X, label):
    plane = game.plane
    root_g, G, caps = game.grundy_upset(X)
    children = [X | b for b in capgame.bits(game.addable(X))]
    child_vals = sorted(G[c] for c in children)
    ext = game.maximal_extensions(G, caps)
    sizes = [s for s, g, m in ext]
    all_terminal_g0 = all(g == 0 for s, g, m in ext)
    print("  %s" % label)
    print("    X = %s   is_cap=%s  |X|=%d  maximal=%s"
          % (capgame.mask_list(X), game.is_cap(X), X.bit_count(), game.maximal(X)))
    print("    upset positions = %d   G(X) = %d" % (len(caps), root_g))
    print("    child Grundy values = %s   (mex = %d)" % (child_vals, mex(child_vals)))
    print("    maximal caps in upset: %d, sizes=%s, all G=0? %s"
          % (len(ext), sorted(set(sizes)), all_terminal_g0))
    return root_g, len(caps), sorted(set(sizes)), all_terminal_g0


def main():
    plane = capgame.load()
    game = capgame.CapGame(plane)
    rng = random.Random(777)

    arcs = []
    for arc in KNOWN_ARCS:
        A = capgame.mask_of(arc)
        assert game.is_cap(A) and game.maximal(A)
        arcs.append(A)
    while len(arcs) < 6:
        cap = random_greedy_maximal(plane, rng)
        if cap.bit_count() == 7 and cap not in arcs:
            arcs.append(cap)

    print("Full upset Grundy DP for six-subsets of complete 7-arcs")
    print("(%d complete 7-arcs, all 7 six-subsets for the first 3 arcs," % len(arcs))
    print(" plus one six-subset for each further arc)\n")

    results = []
    for ai, A in enumerate(arcs):
        apts = capgame.mask_list(A)
        picks = apts if ai < 3 else apts[:1]
        for p in picks:
            X = A & ~(1 << p)
            g, nup, sizes, ok = report(
                game, X, "A=%s  p=%d" % (apts, p))
            results.append((g, nup, sizes, ok))

    print("\nParent's earlier Grundy-2 witness:")
    Xw = capgame.mask_of(WITNESS)
    gw, nupw, sizesw, okw = report(game, Xw, "witness %s" % WITNESS)
    results.append((gw, nupw, sizesw, okw))

    print("\nSummary:")
    print("  six-subsets evaluated: %d" % len(results))
    print("  G==2 for every six-subset of a complete 7-arc: %s"
          % ("PASS" if all(r[0] == 2 for r in results[:-1]) else "FAIL"))
    print("  G(witness)==2: %s" % ("PASS" if gw == 2 else "FAIL (G=%d)" % gw))
    print("  maximal extensions are {7,8} (mixed parity) in every case: %s"
          % ("PASS" if all(r[2] == [7, 8] for r in results) else "FAIL"))
    print("  all maximal caps in the upsets have G=0: %s"
          % ("PASS" if all(r[3] for r in results) else "FAIL"))
    print("\nNote: for X = A-{p} the maximal extensions are A itself (size 7,")
    print("G=0) and three maximal 8-caps (G=0); the 7- vs 8-parity is mixed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
