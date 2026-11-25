"""k=7: the a=0 layer closes via the circle-level u-distribution.

MEASURED (q=5, a=0, 30 circles x C(6,3)=20 triples = 600):

    20 circles: u=7 -> 18 triples, u=9 -> 2 triples
    10 circles: u=6 ->  2 triples, u=8 -> 18 triples

Aggregate u counts:
    u=6: 10*2  =  20
    u=7: 20*18 = 360
    u=8: 10*18 = 180
    u=9: 20*2  =  40
    total      = 600

Now check against the six measured (w,u)-distributions:

    D1 = (0,1):1 (0,2):2 (0,3):11 (0,4):1        240
    D2 = (0,2):1 (0,3):11 (0,4):2 (0,5):1        120
    D3 = (0,2):5 (0,3):8 (0,4):2                 120
    D4 = (0,2):2 (0,3):8 (0,4):5                  60
    D5 = (0,3):6 (0,4):9                          40
    D6 = (0,2):9 (0,3):6                          20

Each distribution is over T (15 subsets), so the u-values in a distribution
are the u for each T, NOT the u for each triple.  These are different
objects!

The circle-level measurement above gives, for each TRIPLE, the value u.
The distributions D1..D6 give, for each T, the value u.

So they are dual.  Let me check the aggregate: sum over triples of (number
of T with that u) should relate to sum over T of (number of triples).

Actually the right check: the total count of (triple, T) pairs is
600 * 15 = 9000.  And sum over distributions of (count * 15) = 600*15.
Both are 9000.  Consistent but not a check.

Let me verify the aggregate u-marginal over TRIPLES against the
distributions' u-marginal over T.

Run:  python arc_k7_a0_check.py --q 5
"""

from __future__ import annotations

from collections import Counter

# the six measured distributions (over T), with their triple counts
DISTS = {
    ((0, 1), 1): 240, ((0, 2), 2): 240, ((0, 3), 11): 240, ((0, 4), 1): 240,
}

# full distributions
FULL = [
    ({1: 1, 2: 2, 3: 11, 4: 1}, 240),
    ({2: 1, 3: 11, 4: 2, 5: 1}, 120),
    ({2: 5, 3: 8, 4: 2}, 120),
    ({2: 2, 3: 8, 4: 5}, 60),
    ({3: 6, 4: 9}, 40),
    ({2: 9, 3: 6}, 20),
]

# circle-level: for each triple, u
CIRCLE_LEVEL = {6: 20, 7: 360, 8: 180, 9: 40}


def main() -> None:
    print("=== u-marginal over T (from the six distributions) ===")
    over_T = Counter()
    for dist, cnt in FULL:
        for u, n in dist.items():
            over_T[u] += n * cnt
    print(f"  {dict(sorted(over_T.items()))}")
    print(f"  total (triple,T) pairs: {sum(over_T.values())}")

    print()
    print("=== u-marginal over triples (circle-level) ===")
    print(f"  {dict(sorted(CIRCLE_LEVEL.items()))}")
    print(f"  total triples: {sum(CIRCLE_LEVEL.values())}")

    print()
    print("=== relation ===")
    print("  over_T counts (triple, T) pairs = 600*15 = 9000")
    print(f"  sum over_T = {sum(over_T.values())}")
    print("  over-triples counts triples = 600")
    print(f"  sum over triples = {sum(CIRCLE_LEVEL.values())}")
    print()
    print("  These are DIFFERENT objects (T-marginal vs triple-marginal),")
    print("  so they need not agree.  Both are consistent with 600 triples")
    print("  and 15 T-subsets.")

    print()
    print("=== the real check: does the circle-level split reproduce the")
    print("    six distributions? ===")
    print("  The circle-level split is 20 circles (u=7,9) and 10 circles")
    print("  (u=6,8).  The six distributions have u-ranges:")
    for i, (dist, cnt) in enumerate(FULL, 1):
        print(f"    D{i}: u in {sorted(dist)} (count {cnt})")
    print()
    print("  D1 has u=1..4, D2 has u=2..5, D3 has u=2..4, D4 has u=2..5,")
    print("  D5 has u=3..4, D6 has u=2..3.")
    print("  NONE has u=6..9!")
    print()
    print("  So the circle-level u (6..9) and the T-level u (1..5) are")
    print("  genuinely different quantities.  The circle-level measurement")
    print("  does NOT directly give the six distributions.")


if __name__ == "__main__":
    main()
