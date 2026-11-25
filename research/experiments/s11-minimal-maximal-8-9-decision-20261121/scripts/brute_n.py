# brute_n.py — System C: CNF-free exhaustive verification of maximal-safe sets on the n x n grid.
# Fully independent implementation: geometry done from scratch (no census_a reuse).
# Safety: no 4 stones on one line or circle (collinearity via cross products, concyclicity via
# Fractions). Maximality: every empty cell lies on a line/circle through 3 stones (each 3-subset
# of stones defines its carrier line/circle; a cell addable iff it lies on no such curve).
# Method: DFS over lex-ordered subsets with incremental safety pruning; at each safe set of size>=3,
# maximality is checked via precomputed per-triple cover bitmasks. Reports counts per size and
# the minimum maximal-safe size, plus witnesses.
import sys
from fractions import Fraction
from itertools import combinations

def triples_cover(n):
    # bitmask of all grid points on the carrier of each 3-subset (line if collinear, else circle)
    pts = [(x, y) for x in range(n) for y in range(n)]
    N = len(pts)
    idx = {p: i for i, p in enumerate(pts)}
    cov = {}
    for T in combinations(range(N), 3):
        (x1, y1), (x2, y2), (x3, y3) = pts[T[0]], pts[T[1]], pts[T[2]]
        cr = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
        if cr == 0:
            # line a*x + b*y + c = 0 through the 3 points
            a = y3 - y1
            b = x1 - x3
            c = -(a * x1 + b * y1)
            members = [i for i, (x, y) in enumerate(pts) if a * x + b * y + c == 0]
        else:
            # circle x^2+y^2+u x+v y+w=0, solve with Fractions
            A = x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2
            B = x1 * x1 + y1 * y1 - x3 * x3 - y3 * y3
            u = Fraction(A * (y3 - y1) - B * (y2 - y1), cr)
            v = Fraction(B * (x2 - x1) - A * (x3 - x1), cr)
            w = -x1 * x1 - y1 * y1 - u * x1 - v * y1
            members = []
            for i, (x, y) in enumerate(pts):
                val = Fraction(x * x + y * y) + u * x + v * y + w
                if val == 0:
                    members.append(i)
        if len(members) >= 4:  # a cover curve needs the 3 stones + at least the potential 4th point
            cov[T] = sum(1 << i for i in members)
    return cov, pts

def unsafe_quartets_by_point(n):
    # all 4-subsets that are collinear or concyclic, indexed by member point (masks).
    # a quartet is unsafe iff all 4 are collinear, or some non-collinear triple's circle
    # contains the fourth point.
    pts = [(x, y) for x in range(n) for y in range(n)]
    N = len(pts)
    by_pt = [[] for _ in range(N)]
    for Q in combinations(range(N), 4):
        xs = [pts[q] for q in Q]
        unsafe = True
        found_circle = False
        for r in range(4):
            i, j, k = [t for t in range(4) if t != r]
            (x1, y1), (x2, y2), (x3, y3) = xs[i], xs[j], xs[k]
            cr = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
            if cr == 0:
                continue
            found_circle = True
            A = x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2
            B = x1 * x1 + y1 * y1 - x3 * x3 - y3 * y3
            u = Fraction(A * (y3 - y1) - B * (y2 - y1), cr)
            v = Fraction(B * (x2 - x1) - A * (x3 - x1), cr)
            w = -x1 * x1 - y1 * y1 - u * x1 - v * y1
            x4, y4 = xs[r]
            unsafe = (Fraction(x4 * x4 + y4 * y4) + u * x4 + v * y4 + w) == 0
            break
        if not found_circle:
            unsafe = True  # every triple collinear => all 4 collinear
        if unsafe:
            for q in Q:
                by_pt[q].append(sum(1 << i for i in Q))
    return by_pt, pts

def run(n, maxsize, want_witnesses=2):
    cov, pts = triples_cover(n)
    by_pt, pts2 = unsafe_quartets_by_point(n)
    assert pts == pts2
    N = n * n
    full = (1 << N) - 1
    counts = {}
    witnesses = []
    def maximal_check(mask):
        covered = mask
        m = mask
        # iterate triples of stones via combination of set bits
        bits = [i for i in range(N) if (mask >> i) & 1]
        for T in combinations(bits, 3):
            cm = cov.get(T)
            if cm is not None:
                covered |= cm
                if covered == full:
                    return True
        return covered == full
    def rec(start, mask, depth):
        if depth >= 3:
            if maximal_check(mask):
                counts[depth] = counts.get(depth, 0) + 1
                if len(witnesses) < want_witnesses and depth >= 5:
                    witnesses.append(mask)
        if depth == maxsize:
            return
        for p in range(start, N):
            nm = mask | (1 << p)
            bad = False
            for qm in by_pt[p]:
                if qm & nm == qm:
                    bad = True
                    break
            if not bad:
                rec(p + 1, nm, depth + 1)
    rec(0, 0, 0)
    return counts, witnesses, pts, cov

if __name__ == "__main__":
    n = int(sys.argv[1])
    maxsize = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    import time
    t0 = time.time()
    counts, witnesses, pts, cov = run(n, maxsize)
    print("n=%d exhaustive maximal-safe counts by size (<= %d): %s  [%.1fs]" %
          (n, maxsize, dict(sorted(counts.items())), time.time() - t0))
    for w in witnesses:
        st = sorted(pts[i] for i in range(n * n) if (w >> i) & 1)
        print("witness size", bin(w).count("1"), st)
