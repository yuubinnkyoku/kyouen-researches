"""Standalone verifier for a k-stone maximal safe set on an n x n board.

Fresh implementation: exact integer arithmetic, no repository imports.

Safety is checked twice:
  (a) translated 3x3 concyclicity determinant (zero iff concyclic/collinear);
  (b) integer curve coefficients through the first three points evaluated at
      the fourth (exact rational-free check).
Maximality: every grid point p outside S admits a 3-subset T of S lying with
p on a common circle or line, verified by evaluating the integer curve
coefficients of T at p.
"""
import itertools
import json
import sys


def det_origin(pts):
    """Zero iff the four distinct points are concyclic or collinear."""
    (x0, y0), rest = pts[0], pts[1:]
    (a1, b1, c1), (a2, b2, c2), (a3, b3, c3) = [
        (x - x0, y - y0, (x - x0) ** 2 + (y - y0) ** 2) for x, y in rest]
    return (a1 * (b2 * c3 - b3 * c2)
            - b1 * (a2 * c3 - a3 * c2)
            + c1 * (a2 * b3 - a3 * b2))


def curve_through(p1, p2, p3):
    """(A, B, C, D): A(x^2+y^2) + Bx + Cy + D = 0 through the three points.

    A == 0 for a line. D is fixed by p1, so evaluation is exact everywhere.
    """
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    dx2, dy2, dx3, dy3 = x2 - x1, y2 - y1, x3 - x1, y3 - y1
    cross = dx2 * dy3 - dy2 * dx3
    if cross == 0:
        A, B, C = 0, -dy2, dx2
    else:
        f2 = dx2 * dx2 + dy2 * dy2
        f3 = dx3 * dx3 + dy3 * dy3
        A = cross
        B = f3 * dy2 - f2 * dy3
        C = f2 * dx3 - f3 * dx2
        B -= 2 * A * x1
        C -= 2 * A * y1
    D = -(A * (x1 * x1 + y1 * y1) + B * x1 + C * y1)
    return A, B, C, D


def on_curve(coeffs, p):
    A, B, C, D = coeffs
    x, y = p
    return A * (x * x + y * y) + B * x + C * y + D == 0


def main():
    path = sys.argv[1]
    data = json.loads(open(path, encoding="utf-8").read())
    ids = data["witness"]
    n = data.get("n", 10)
    grid = [(x, y) for y in range(n) for x in range(n)]
    S = [grid[i] for i in ids]
    assert len(set(ids)) == len(ids), "duplicate points"
    assert all(0 <= i < n * n for i in ids), "out of range"
    report = {"n": n, "size": len(S), "points": S}

    bad = [list(quad) for quad in itertools.combinations(S, 4)
           if det_origin(list(quad)) == 0]
    report["safety_bad_quads_det"] = bad
    assert not bad, f"unsafe: {bad[0]}"

    for quad in itertools.combinations(S, 4):
        c = curve_through(quad[0], quad[1], quad[2])
        assert not on_curve(c, quad[3]), quad

    blockers = {}
    for p in grid:
        if p in S:
            continue
        found = None
        for trio in itertools.combinations(S, 3):
            if on_curve(curve_through(*trio), p):
                found = trio
                break
        assert found is not None, f"point {p} not blocked"
        blockers[p] = found
    report["blocker_count"] = len(blockers)
    report["all_blocked"] = len(blockers) == n * n - len(S)
    report["blockers"] = {f"{p[0]},{p[1]}": [[t[0], t[1]] for t in trio]
                          for p, trio in sorted(blockers.items())}
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
