# verify_geom.py — System C: CNF-free witness verification by pure geometry (Fraction arithmetic).
# Checks: (1) safety: no 4 stones on one line/circle; (2) maximality: every empty cell lies on
# the carrier line/circle of some 3-stone triple; (3) |S| <= k.
# Complexity is polynomial in stones only (C(|S|,4) quartet tests + C(|S|,3) carrier scans of
# n^2 board points), so n=11 is fast. Fully independent of census_a.py / gen_cnf.py.
import sys, json
from fractions import Fraction
from itertools import combinations

def carrier_members(n, T):
    # all grid points on the line (if collinear) or circle through the 3 points T
    xs = list(T)
    (x1, y1), (x2, y2), (x3, y3) = xs[0], xs[1], xs[2]
    cr = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    if cr == 0:
        a = y3 - y1
        b = x1 - x3
        c = -(a * x1 + b * y1)
        return [(x, y) for x in range(n) for y in range(n) if a * x + b * y + c == 0]
    A = x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2
    B = x1 * x1 + y1 * y1 - x3 * x3 - y3 * y3
    u = Fraction(A * (y3 - y1) - B * (y2 - y1), cr)
    v = Fraction(B * (x2 - x1) - A * (x3 - x1), cr)
    w = -x1 * x1 - y1 * y1 - u * x1 - v * y1
    return [(x, y) for x in range(n) for y in range(n)
            if Fraction(x * x + y * y) + u * x + v * y + w == 0]

def quartet_unsafe(Q4):
    xs = list(Q4)
    for r in range(4):
        i, j, kk = [t for t in range(4) if t != r]
        (x1, y1), (x2, y2), (x3, y3) = xs[i], xs[j], xs[kk]
        cr = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
        if cr == 0:
            continue
        A = x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2
        B = x1 * x1 + y1 * y1 - x3 * x3 - y3 * y3
        u = Fraction(A * (y3 - y1) - B * (y2 - y1), cr)
        v = Fraction(B * (x2 - x1) - A * (x3 - x1), cr)
        w = -x1 * x1 - y1 * y1 - u * x1 - v * y1
        x4, y4 = xs[r]
        return (Fraction(x4 * x4 + y4 * y4) + u * x4 + v * y4 + w) == 0
    return True  # every triple collinear => all 4 collinear

def verify(n, stones, k=None, verbose=True):
    S = set(map(tuple, stones))
    assert all(0 <= x < n and 0 <= y < n for x, y in S), "stone off board"
    assert len(S) == len(stones), "duplicate stone"
    if k is not None:
        assert len(S) <= k, "stone count exceeds k"
    st = sorted(S)
    unsafe = [Q for Q in combinations(st, 4) if quartet_unsafe(Q)]
    covered = set(S)
    cells = set((x, y) for x in range(n) for y in range(n))
    for T in combinations(st, 3):
        covered |= set(carrier_members(n, T))
    uncovered = sorted(cells - covered)
    ok = (not unsafe) and (not uncovered)
    if verbose:
        print("n=%d stones=%d safety_violations=%d uncovered_cells=%d %s" %
              (n, len(S), len(unsafe), len(uncovered), "VALID" if ok else "INVALID"))
        if unsafe:
            print("  unsafe quartets:", unsafe[:3])
        if uncovered:
            print("  uncovered:", uncovered[:10])
    return ok

def decode_kissat(out_path, n):
    lits = []
    with open(out_path) as f:
        for line in f:
            if line.startswith("v "):
                lits.extend(int(x) for x in line.split()[1:])
    N = n * n
    stones = []
    for l in sorted(x for x in lits if x > 0):
        if l <= N:
            stones.append(((l - 1) // n, (l - 1) % n))
    return stones

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "model":
        n, k, out_path = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        stones = decode_kissat(out_path, n)
        print("decoded %d stones:" % len(stones))
        print(json.dumps(sorted(stones)))
        ok = verify(n, stones, k)
        sys.exit(0 if ok else 1)
    else:
        n, k = int(sys.argv[2]), int(sys.argv[3])
        stones = json.loads(sys.argv[4])
        sys.exit(0 if verify(n, stones, k) else 1)
