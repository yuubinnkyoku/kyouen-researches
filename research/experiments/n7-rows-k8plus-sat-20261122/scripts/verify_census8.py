#!/usr/bin/env python3
# verify_census8.py — independent verification of the (partial) n7 k=8 census leaders.
# For every leader in the census state file (0-based cell indices, c = x + 7y):
#   1. geometry: SAFE (no concyclic/collinear quartet) and MAXIMAL (every empty
#      cell is blocked by some stone-triple's circle/line), via the SAME integer
#      4x4 determinant test as the pinned verify_witness.py (independent of SAT).
#   2. D4: the leader must be the index-lexicographic minimum of its D4 orbit
#      (indicator vector over cells), computed locally over all 8 images.
#   3. pairwise: canonical representatives pairwise distinct; orbit size and
#      stabilizer order recorded (size * stabilizer == 8).
#   4. consistency gate (not a claim): no leader contains the known 7-stone
#      maximal row models O1/O2 as subsets.
# Usage: python3 verify_census8.py <state.json> <n>
import json, sys, itertools, math
from fractions import Fraction

state = json.load(open(sys.argv[1]))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 7
leaders = state["leaders"]

def concyclic_or_collinear(a, b, c, d):
    # the 4x4 circle-equation matrix has full rank iff the 4 points share NO
    # circle (and no line: collinear points give a rank-deficient circle matrix
    # only when the quadratic term degenerates; handle lines separately)
    pts = [a, b, c, d]
    (x1, y1), (x2, y2) = pts[0], pts[1]
    for (x3, y3) in pts[2:]:
        if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1):
            break
    else:
        return True   # all four collinear
    F = [[Fraction([x*x + y*y, x, y, 1][k]) for k in range(4)] for (x, y) in pts]
    for i in range(4):
        piv = next((r for r in range(i, 4) if F[r][i] != 0), None)
        if piv is None:
            return True   # concyclic (rank deficient circle system)
        if piv != i:
            F[i], F[piv] = F[piv], F[i]
        for r in range(i + 1, 4):
            f = F[r][i] / F[i][i]
            if f:
                for c in range(i, 4):
                    F[r][c] -= f * F[i][c]
    return False   # full rank: no single circle/line through all 4

def spts(S):  # cell indices -> xy points
    return [(c % n, c // n) for c in S]

def is_safe(pts):
    bad = []
    for quad in itertools.combinations(sorted(pts), 4):
        if concyclic_or_collinear(*quad):
            bad.append(quad)
    return bad

def is_maximal(pts):
    st = set(pts)
    unc = []
    for x in range(n):
        for y in range(n):
            if (x, y) in st:
                continue
            ok = False
            for trip in itertools.combinations(sorted(st), 3):
                if concyclic_or_collinear((x, y), *trip):
                    ok = True
                    break
            if not ok:
                unc.append((x, y))
    return unc

D4 = [
    lambda x, y: (x, y),
    lambda x, y: (n - 1 - x, y),
    lambda x, y: (x, n - 1 - y),
    lambda x, y: (n - 1 - x, n - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (n - 1 - y, n - 1 - x),
    lambda x, y: (y, n - 1 - x),
    lambda x, y: (n - 1 - y, x),
]

def idx(p): return p[0] + n * p[1]

def orbit_images(S):
    pts = set(spts(S))
    return [frozenset(g(x, y) for (x, y) in pts) for g in D4]

results = []
canon_seen = set()
trips_hist, dirs_hist, stab_hist, osize_hist = {}, {}, {}, {}
O1, O2 = [10, 13, 14, 17, 19, 21, 45], [18, 21, 22, 26, 31, 32, 38]
antichain_viol = []

for i, S in enumerate(leaders):
    pts = spts(S)
    bad = is_safe(pts)
    unc = is_maximal(pts)
    imgs = orbit_images(S)
    pS = set(spts(S))
    # indicator-vector lex order over cells 0..N-1 with 0 < 1 (enc_sat2 convention:
    # A <=lex g(A) compares A_c (stone indicator) from c=0; a stone at a lower cell
    # index makes the vector LARGER, so the leader must avoid low-index cells
    # as long as possible).
    ind = lambda st: tuple(1 if (x, y) in st else 0 for y in range(n) for x in range(n))
    li = ind(pS)
    canon = min(ind(img) for img in imgs)
    lexmin = (li == canon)
    distinct = set(imgs)
    osize = len(distinct)
    stab = 8 // osize
    dup = canon in canon_seen
    canon_seen.add(canon)
    trips, dirs = 0, set()
    for t in itertools.combinations(sorted(pts), 3):
        (x1, y1), (x2, y2), (x3, y3) = t
        if (x2 - x1) * (y3 - y1) == (y2 - y1) * (x3 - x1):
            trips += 1
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy))
            if g:
                dx //= g; dy //= g
            if (dx, dy) < (0, 0) or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            dirs.add((dx, dy))
    for h, key in ((trips_hist, trips), (dirs_hist, len(dirs)), (stab_hist, stab), (osize_hist, osize)):
        h[key] = h.get(key, 0) + 1
    ss = set(S)
    for nm, O in (("O1", O1), ("O2", O2)):
        if set(O).issubset(ss):
            antichain_viol.append({"i": i, "contains": nm})
    results.append({"i": i, "safe": not bad, "nViol": len(bad), "maximal": not unc,
                    "nUnc": len(unc), "lexmin": lexmin, "dup": dup,
                    "osize": osize, "stab": stab, "trips": trips, "dirs": len(dirs)})

summary = {
    "n": n, "nLeaders": len(leaders),
    "all_safe": all(r["safe"] for r in results),
    "all_maximal": all(r["maximal"] for r in results),
    "all_orbit_lexmin": all(r["lexmin"] for r in results),
    "any_duplicate_canon": any(r["dup"] for r in results),
    "distinct_orbits": len(canon_seen),
    "orbit_size_histogram": osize_hist,
    "stabilizer_histogram": stab_hist,
    "trips_histogram": trips_hist,
    "dirs_histogram": dirs_hist,
    "config_count_among_verified": sum(r["osize"] for r in results),
    "antichain_violations": antichain_viol,
}
json.dump({"summary": summary, "per_leader": results}, open(sys.argv[3] if len(sys.argv) > 3 else '/dev/stdout', 'w'), indent=1)
print(json.dumps(summary, indent=1))
