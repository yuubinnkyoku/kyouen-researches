"""Task 5: 6-caps WITHOUT a complete 7-arc extension, full upset DP.

Samples >=20 6-caps that have no maximal 7-cap extension (equivalently no
maximal 7-child), plus some maximal 6-caps (which have no children at all), and
verifies with the full upset DP that
  * G = 0 (in particular, never 2),
  * every maximal cap in the upset has even size (8 or 10; size 6 for a maximal
    6-cap itself),
  * every maximal cap in the upset has Grundy 0.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capgame

TARGET_NONMAX = 25
TARGET_MAX6 = 10


def random_6_cap(plane, rng):
    while True:
        pts = rng.sample(range(91), 6)
        m = capgame.mask_of(pts)
        if plane.is_cap(m):
            return m


def random_maximal_6_cap(plane, rng):
    while True:
        m = random_6_cap(plane, rng)
        if plane.addable(m) == 0:
            return m


def main():
    plane = capgame.load()
    game = capgame.CapGame(plane)
    rng = random.Random(20261126)

    nonmax_noext = []
    seen = set()
    tries = 0
    while len(nonmax_noext) < TARGET_NONMAX:
        tries += 1
        X = random_6_cap(plane, rng)
        assert game.is_cap(X)
        ext = game.addable(X)
        if ext == 0:
            continue          # maximal 6-cap: handled separately
        has_max_child = any(plane.addable(X | b) == 0 for b in capgame.bits(ext))
        if not has_max_child and X not in seen:
            seen.add(X)
            nonmax_noext.append(X)
    print("non-maximal 6-caps without a complete 7-arc extension: %d "
          "(from %d random 6-cap draws)" % (len(nonmax_noext), tries))

    max6 = []
    while len(max6) < TARGET_MAX6:
        m = random_maximal_6_cap(plane, rng)
        if m not in max6:
            max6.append(m)
    print("random maximal 6-caps: %d\n" % len(max6))

    def check(X, kind):
        g, G, caps = game.grundy_upset(X)
        ext = game.maximal_extensions(G, caps)
        sizes = sorted(s for s, gg, m in ext)
        even = all(s % 2 == 0 for s in sizes)
        zero = all(gg == 0 for s, gg, m in ext)
        ok = (g == 0) and even and zero
        print("  %s X=%-34s |X|=%d  upset=%3d  G=%d  max-ext sizes=%-10s "
              "all even=%s all G=0=%s  %s"
              % (kind, str(capgame.mask_list(X)), X.bit_count(), len(caps), g,
                 str(sizes), even, zero, "OK" if ok else "FAIL"))
        return ok, g, sizes

    results = []
    print("Non-maximal 6-caps without a complete 7-arc extension:")
    for X in nonmax_noext:
        results.append(check(X, "nonmax"))
    print("\nMaximal 6-caps (no addable point at all):")
    for X in max6:
        results.append(check(X, "max6  "))

    allok = all(r[0] for r in results)
    gs = sorted(set(r[1] for r in results))
    print("\nSummary:")
    print("  sampled caps: %d (25 no-7-extension non-maximal + %d maximal)"
          % (len(results), len(max6)))
    print("  G values observed: %s" % gs)
    print("  every sampled cap has G=0: %s" % ("PASS" if gs == [0] else "FAIL"))
    print("  every maximal extension even-sized and G=0: %s"
          % ("PASS" if allok else "FAIL"))
    print("  => no 6-cap without a complete 7-arc extension has G=2: PASS"
          if allok and gs == [0] else "  => FAIL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
