# census_a.py — System A curve census for the kyouen game (standard n x n grid, coords 0..n-1).
# Counts lines (>=4 collinear grid pts, maximal) and circles (>=4 concyclic grid pts,
# non-degenerate). A "curve" is maximal. Every unsafe quartet (4 grid pts on one curve)
# lies on exactly one maximal curve.
from fractions import Fraction
from math import gcd

def line_census(n):
    lines = {}
    pts = [(x, y) for x in range(n) for y in range(n)]
    N = len(pts)
    for i in range(N):
        xi, yi = pts[i]
        for j in range(i + 1, N):
            xj, yj = pts[j]
            dx, dy = xj - xi, yj - yi
            g = gcd(abs(dx), abs(dy))
            if g == 0:
                continue
            a, b = dy // g, -dx // g
            if a < 0 or (a == 0 and b < 0):
                a, b = -a, -b
            c = -(a * xi + b * yi)
            gg = gcd(gcd(abs(a), abs(b)), abs(c))
            if gg:
                a, b, c = a // gg, b // gg, c // gg
            if (a, b, c) in lines:
                continue
            on = [p for p in pts if a * p[0] + b * p[1] + c == 0]
            if len(on) >= 4:
                lines[(a, b, c)] = frozenset(on)
    return lines

def circle_of(p3):
    (x1, y1), (x2, y2), (x3, y3) = p3
    det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    if det == 0:
        return None, None
    A = (x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2)
    B = (x1 * x1 + y1 * y1 - x3 * x3 - y3 * y3)
    u = Fraction(A * (y3 - y1) - B * (y2 - y1), det)
    v = Fraction(B * (x2 - x1) - A * (x3 - x1), det)
    w = -x1 * x1 - y1 * y1 - u * x1 - v * y1
    lcm_ = u.denominator * v.denominator // gcd(u.denominator, v.denominator)
    lcm_ = lcm_ * w.denominator // gcd(lcm_, w.denominator)
    D = lcm_
    U = int(u * D); V = int(v * D); W = int(w * D)
    g = gcd(gcd(abs(D), abs(U)), gcd(abs(V), abs(W)))
    if g:
        D, U, V, W = D // g, U // g, V // g, W // g
    if D < 0:
        D, U, V, W = -D, -U, -V, -W
    return (D, U, V, W), (u, v, w)

def census(n):
    lines = line_census(n)
    pts = [(x, y) for x in range(n) for y in range(n)]
    circles = {}
    N = len(pts)
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                key, _ = circle_of((pts[i], pts[j], pts[k]))
                if key is None:
                    continue
                if key in circles:
                    continue
                (D, U, V, W) = key
                on = [p for p in pts if D * (p[0] * p[0] + p[1] * p[1]) + U * p[0] + V * p[1] + W == 0]
                if len(on) >= 4:
                    circles[key] = frozenset(on)
    info = {
        "n": n,
        "lines": len(lines),
        "circles": len(circles),
        "line_size_hist": hist(lines.values()),
        "circle_size_hist": hist(circles.values()),
    }
    return info, lines, circles

def quartets(d):
    tot = 0
    for s in d.values():
        m = len(s)
        tot += m * (m - 1) * (m - 2) * (m - 3) // 24
    return tot

def hist(sets):
    h = {}
    for s in sets:
        h[len(s)] = h.get(len(s), 0) + 1
    return dict(sorted(h.items()))

if __name__ == "__main__":
    import sys
    ns = [int(a) for a in sys.argv[1:]] or [5, 6]
    for n in ns:
        info, lines, circles = census(n)
        D = quartets(lines); C = quartets(circles)
        print("n=%d curves: lines=%d circles=%d  quartets: D=%d C=%d F=%d" %
              (n, info["lines"], info["circles"], D, C, D + C))
        print("  line hist ", info["line_size_hist"])
        print("  circle hist", info["circle_size_hist"])
