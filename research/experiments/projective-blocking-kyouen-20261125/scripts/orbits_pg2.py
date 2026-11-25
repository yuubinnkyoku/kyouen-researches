"""Structure and orbits for the minimal multiple blocking sets of PG(2,3) and PG(2,4).

(A) PG(2,3): the 234 six-point minimal blocking sets are identified as the vertex
    sets of complete quadrilaterals (4 lines in general position); we verify the
    4 three-point lines, the general position, the exact count, and the single
    PGL(3,3) orbit.
(B) PG(2,4): enumerate all 9-point maximal safe sets (equivalently 12-point
    minimal 2-fold blocking sets), classify their line profiles, and compute the
    PGL(3,4) orbits using a generator set of GL(3,4).

Usage:
    python orbits_pg2.py --q 3 4
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
sys.path.insert(0, str(HERE))

from build_pg2 import GF4, PrimeField, canon, make_field, sum_field  # noqa: E402


def field_for(q: int):
    return GF4() if q == 4 else PrimeField(q)


def point_list(q: int):
    F = make_field(q)
    vecs = [v for v in product(F.elements, repeat=3) if any(not F.zero(x) for x in v)]
    return sorted({canon(F, v, q) for v in vecs})


def apply_matrix(F, q, M, p):
    v = tuple(sum_field(F, [F.mul(M[i][j], p[j]) for j in range(3)]) for i in range(3))
    return canon(F, v, q)


def generator_matrices(q: int):
    """A small generating set of GL(3,q) (image in PGL is the full group)."""
    F = field_for(q)
    one, zero = 1, 0
    if q == 4:
        w = 2  # element w with w^2 = w+1 in the build_pg2.GF4 encoding
    else:
        w = 2 % q
    mats = []
    # transvections E_ij(a) for a = 1, and one with a = w
    for (i, j, a) in [(0, 1, one), (1, 2, one), (0, 2, one), (1, 0, w), (2, 0, one)]:
        M = [[one if i == k else zero for k in range(3)] for i2 in range(3)]
        M = [[one if r == c else zero for c in range(3)] for r in range(3)]
        M[i][j] = a
        mats.append(M)
    # diagonal diag(w,1,1) with determinant w != 1
    D = [[zero] * 3 for _ in range(3)]
    D[0][0], D[1][1], D[2][2] = w, one, one
    mats.append(D)
    # coordinate permutation (cyclic)
    P = [[zero] * 3 for _ in range(3)]
    P[0][1] = P[1][2] = P[2][0] = one
    mats.append(P)
    return mats


def enumerate_safe_sets_of_size(q: int, size: int):
    """All subsets of the given size with <=3 on every line (bitmasks)."""
    lines = (OUT / f"board_pg2q{q}.txt").read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    line_masks = [sum(1 << p for p in map(int, line.split()[1:])) for line in lines[1:]]
    out = []
    for comb in combinations(range(n), size):
        mask = 0
        for p in comb:
            mask |= 1 << p
        if all(bin(mask & L).count("1") <= 3 for L in line_masks):
            out.append(mask)
    return n, line_masks, out


def profile(mask: int, line_masks: list[int], n: int):
    comp = ((1 << n) - 1) ^ mask
    return tuple(sorted(Counter(bin(comp & L).count("1") for L in line_masks).items()))


def orbits(masks: list[int], perms: list[list[int]]):
    remaining = set(masks)
    result = []
    while remaining:
        seed = next(iter(remaining))
        orbit = set()
        stack = [seed]
        while stack:
            cur = stack.pop()
            if cur in orbit:
                continue
            orbit.add(cur)
            bits = [p for p in range(len(perms[0])) if (cur >> p) & 1]
            for perm in perms:
                new = 0
                for p in bits:
                    new |= 1 << perm[p]
                if new not in orbit:
                    stack.append(new)
        remaining -= orbit
        result.append(sorted(orbit))
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()
    data = {}
    for q in args.q:
        F = field_for(q)
        pts = point_list(q)
        index = {p: i for i, p in enumerate(pts)}
        perms = []
        for M in generator_matrices(q):
            perm = [index[apply_matrix(F, q, M, p)] for p in pts]
            # a projective matrix must act bijectively on the 21 points
            assert sorted(perm) == list(range(len(pts))), "generator is degenerate"
            perms.append(perm)
        if q == 3:
            # PG(2,3): safe sets of size 7; complements are 6-point blocking sets
            n, line_masks, safe7 = enumerate_safe_sets_of_size(q, 7)
            comps = sorted({((1 << n) - 1) ^ m for m in safe7})
            rows = []
            for X in comps:
                prof = profile(((1 << n) - 1) ^ X, line_masks, n)  # profile of X? see below
                # profile of the complement of X (the 6-set itself)
                prof = tuple(sorted(Counter(bin(X & L).count("1") for L in line_masks).items()))
                rows.append(prof)
            # identify complete quadrilaterals: the 4 lines with 3 points of X
            quads = 0
            good = 0
            for X in comps:
                three = [L for L in line_masks if bin(X & L).count("1") == 3]
                if len(three) != 4:
                    continue
                # general position: no 3 of the 4 lines concurrent
                points = [p for p in range(n) if (X >> p) & 1]
                concurrent = False
                for P in points:
                    cnt = sum(1 for L in three if (L >> P) & 1)
                    if cnt >= 3:
                        concurrent = True
                        break
                if not concurrent:
                    quads += 1
                good += 1
            orb = orbits(comps, perms)
            data["q3"] = {
                "safe7": len(safe7), "six_point_blocking_sets": len(comps),
                "profiles": {str(p): sum(1 for r in rows if r == p) for p in set(rows)},
                "sets_with_4_three_point_lines": good,
                "complete_quadrilaterals": quads,
                "orbits": [len(o) for o in orb],
                "group_generators": len(perms),
            }
            print("q=3:", json.dumps(data["q3"], indent=1), flush=True)
        else:
            # PG(2,4): safe sets of size 9 <-> 12-point minimal 2-fold blocking sets
            n, line_masks, safe9 = enumerate_safe_sets_of_size(q, 9)
            safe9 = sorted(set(safe9))
            comps = sorted({((1 << n) - 1) ^ m for m in safe9})
            profs = Counter()
            per_set_profile = {}
            for X in comps:
                p = tuple(sorted(Counter(bin(X & L).count("1") for L in line_masks).items()))
                profs[p] += 1
                per_set_profile[X] = p
            orb = orbits(comps, perms)
            orbit_info = []
            for o in orb:
                pc = Counter(per_set_profile[m] for m in o)
                orbit_info.append({"size": len(o),
                                   "profiles": {str(p): c for p, c in pc.items()}})
            data["q4"] = {
                "safe9": len(safe9), "twelve_point_blocking_sets": len(comps),
                "profile_classes": {str(p): c for p, c in profs.items()},
                "orbits": orbit_info,
                "group_order_if_full_PGL": 60480,
                "group_generators": len(perms),
            }
            print("q=4:", json.dumps(data["q4"], indent=1), flush=True)
    (OUT / "orbits.json").write_text(json.dumps(data, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
