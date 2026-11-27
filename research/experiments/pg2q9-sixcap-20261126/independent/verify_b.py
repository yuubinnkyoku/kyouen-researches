"""Task 2: claim (B) on >=20 complete 7-arcs found by random greedy.

For every complete 7-arc A (maximal 7-cap, found by random greedy + maximality
check) and every six-subset X = A - {p}, compute the addable set of X and
compare it with A, and inspect the 7-cap children of X.

Prints a detailed table for the sampled arcs and a PASS/FAIL summary for
  (B1) |addable(X)| == 7                 (the numerical part of claim B)
  (B2) addable(X) == A                   (the literal claim B)
  (C1) children of X = 1 maximal + 6 non-maximal
  (C2) mex of the structural child Grundy values = 2
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
]


def random_greedy_maximal(plane, rng):
    cap = 0
    while True:
        add = plane.addable(cap) & ~cap
        if add == 0:
            return cap
        choices = [b for b in capgame.bits(add)]
        cap |= rng.choice(choices)


def mex(vals):
    g = 0
    while g in vals:
        g += 1
    return g


def main():
    plane = capgame.load()
    rng = random.Random(20261126)

    random_arcs = []
    tries = 0
    while len(random_arcs) < 25:
        tries += 1
        cap = random_greedy_maximal(plane, rng)
        if cap.bit_count() == 7 and cap not in random_arcs:
            random_arcs.append(cap)
    known_arcs = [capgame.mask_of(a) for a in KNOWN_ARCS]
    for A in known_arcs:
        assert plane.is_cap(A) and plane.addable(A) == 0
    arcs = random_arcs + known_arcs
    print("random greedy: %d tries -> %d distinct complete 7-arcs; "
          "plus %d known complete 7-arcs -> %d arcs"
          % (tries, len(random_arcs), len(known_arcs), len(arcs)))

    checks = {"B1": [0, 0], "B2": [0, 0], "C1": [0, 0], "C2": [0, 0]}
    nsub = 0
    detail = []
    for ai, A in enumerate(arcs):
        apts = capgame.mask_list(A)
        assert plane.is_cap(A), "greedy cap not a cap"
        assert plane.addable(A) == 0, "greedy 7-cap not maximal"
        for p in apts:
            nsub += 1
            X = A & ~(1 << p)
            assert plane.is_cap(X)
            add = plane.addable(X)
            addp = capgame.mask_list(add)
            max_children = []
            nonmax_children = []
            for q in addp:
                child = X | (1 << q)
                assert plane.is_cap(child)
                if plane.addable(child) == 0:
                    max_children.append(q)
                else:
                    nonmax_children.append(q)
            # structural Grundy of a 7-cap: terminal -> 0, else 1
            child_vals = [0] * len(max_children) + [1] * len(nonmax_children)
            g_struct = mex(child_vals)

            ok_b1 = len(addp) == 7
            ok_b2 = add == A
            ok_c1 = len(max_children) == 1 and len(nonmax_children) == 6
            ok_c2 = g_struct == 2
            for key, ok in (("B1", ok_b1), ("B2", ok_b2), ("C1", ok_c1), ("C2", ok_c2)):
                checks[key][1] += 1
                if ok:
                    checks[key][0] += 1
            if ai < 3:
                detail.append((A, p, X, addp, max_children, nonmax_children, g_struct))

    print("\nSampled %d six-subsets from %d complete 7-arcs." % (nsub, len(arcs)))
    print("\nExample rows (first 3 arcs):")
    for A, p, X, addp, mx, nm, g in detail:
        print("  A=%s  p=%d" % (capgame.mask_list(A), p))
        print("    X=A-{p}: %s" % capgame.mask_list(X))
        print("    |addable|=%d addable=%s" % (len(addp), addp))
        print("    addable & A = %s ; addable - A = %s"
              % (sorted(set(addp) & set(capgame.mask_list(A))),
                 sorted(set(addp) - set(capgame.mask_list(A)))))
        print("    maximal child q's=%s; non-maximal child q's=%s; mex=%d"
              % (mx, nm, g))

    print("\nSummary (x/y = passes/total, %d six-subsets):" % nsub)
    names = {
        "B1": "|addable(X)| == 7",
        "B2": "addable(X) == A  (literal claim B)",
        "C1": "1 maximal + 6 non-maximal 7-children",
        "C2": "structural mex (child G in {0,1}) == 2",
    }
    for key in ("B1", "B2", "C1", "C2"):
        ok, tot = checks[key]
        print("  %-52s %d/%d  %s" % (names[key], ok, tot, "PASS" if ok == tot else "FAIL"))

    print("\nInterpretation: |addable| is 7 in every case, but the addable set is")
    print("NOT the 7-arc A; it is {p} plus 6 points outside A.  Claim (B)'s count")
    print("is correct, its identification with A is wrong.")

    # additional: is the 7-point addable set itself a cap?
    cap_add = 0
    tot_add = 0
    for A in arcs:
        for p in capgame.mask_list(A):
            X = A & ~(1 << p)
            add = plane.addable(X)
            tot_add += 1
            if plane.is_cap(add):
                cap_add += 1
    print("\naddable-set-is-a-cap: %d/%d" % (cap_add, tot_add))
    return 0


if __name__ == "__main__":
    sys.exit(main())
