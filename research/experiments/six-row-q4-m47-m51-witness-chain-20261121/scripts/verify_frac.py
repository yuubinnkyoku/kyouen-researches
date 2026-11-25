#!/usr/bin/env python3
r"""Independent verifier family 2: Fraction center-radius arithmetic.

Deliberately different codepath from engine_v2.verify_config:
- safety: for each triple of stones, build the exact curve as a
  perp-bisector-solved Fraction circle (center + r^2) or a cross-product
  line, then test every other stone for membership. No determinants, no
  integer circle equations, no bitmasks.
- blocking: for each empty cell, scan triples with early exit using the
  same Fraction/line descriptors.
- tamper control: adding one stone at any maximality-blocked empty cell
  must break safety (that is what maximality means), and is checked.

Usage: verify_frac.py <bank.json>   -> results JSON on stdout
bank.json: {w, q, items: [{tag, m, stones}, ...]}
"""
import itertools, json, sys
from fractions import Fraction

def line_of(p1, p2):
    # a*x + b*y = c with integer a,b,c, a>=0 canonical, gcd 1
    (x1, y1), (x2, y2) = p1, p2
    a, b = y2 - y1, x1 - x2
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    g = 1
    import math
    g = math.gcd(abs(a), abs(b)) or 1
    a //= g; b //= g
    c = a * x1 + b * y1
    return (a, b, c)

def on_line(ln, p):
    a, b, c = ln
    return a * p[0] + b * p[1] == c

def circle_of(p1, p2, p3):
    """Fraction center (h, k) and r^2 such that all three points lie on
    (x-h)^2 + (y-k)^2 = r^2. Raises ValueError if collinear."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if d == 0:
        raise ValueError("collinear")
    h = Fraction(
        (x1*x1 + y1*y1) * (y2 - y3) +
        (x2*x2 + y2*y2) * (y3 - y1) +
        (x3*x3 + y3*y3) * (y1 - y2), d)
    k = Fraction(
        (x1*x1 + y1*y1) * (x3 - x2) +
        (x2*x2 + y2*y2) * (x1 - x3) +
        (x3*x3 + y3*y3) * (x2 - x1), d)
    r2 = (x1 - h) ** 2 + (y1 - k) ** 2
    if r2 <= 0:
        raise ValueError("degenerate")
    return (h, k, r2)

def on_circle(cc, p):
    h, k, r2 = cc
    return (p[0] - h) ** 2 + (p[1] - k) ** 2 == r2

def verify(stones, w, m, q):
    st = sorted((int(x), int(y)) for (x, y) in stones)
    res = dict(tag=None, safe=True, maximal=True, rows=[0]*w, ok=None,
               uncovered=[], notes=[])
    rowcount = [0] * w
    for (_, y) in st:
        rowcount[y] += 1
    res["rows"] = rowcount
    res["rowDeficient"] = min(rowcount) < q - 1
    descs = []
    for tri in itertools.combinations(st, 3):
        if on_line(line_of(tri[0], tri[1]), tri[2]):
            descs.append(("L", line_of(tri[0], tri[1])))
        else:
            descs.append(("C", circle_of(*tri)))
    # safety: no 4th stone on any triple curve
    stset = set(st)
    for (kind, dsc) in descs:
        cnt = 0
        for s in st:
            if (kind == "L" and on_line(dsc, s)) or \
               (kind == "C" and on_circle(dsc, s)):
                cnt += 1
        if cnt > 3:
            res["safe"] = False
            res["notes"].append("unsafe: curve with %d stones" % cnt)
            break
    # blocking
    unc = []
    for x in range(m):
        for y in range(w):
            c = (x, y)
            if c in stset:
                continue
            blocked = False
            for (kind, dsc) in descs:
                if (kind == "L" and on_line(dsc, c)) or \
                   (kind == "C" and on_circle(dsc, c)):
                    blocked = True
                    break
            if not blocked:
                unc.append([x, y])
    res["uncovered"] = unc
    res["maximal"] = not unc
    res["ok"] = bool(res["safe"] and res["maximal"] and res["rowDeficient"])
    # negative control: adding a stone at the first empty cell must fail
    if unc:  # witness claim already failed; tamper meaningless
        res["tamperAddFails"] = None
    else:
        cells = [(x, y) for x in range(m) for y in range(w)]
        empty = [c for c in cells if c not in stset]
        fails = 0
        checked = 0
        # deterministic sample of up to 5 blocked cells across the board
        step = max(1, len(empty) // 5)
        for c in empty[::step][:5]:
            s2 = sorted(st + [c])
            sub = verify_light(s2, w, m, q)
            checked += 1
            if not sub:
                fails += 1
        res["tamperAddFails"] = bool(checked and fails == checked)
        res["tamperChecked"] = checked
    return res

def verify_light(stones, w, m, q):
    """safe-only light check for tamper tests."""
    st = sorted(stones)
    for quad in itertools.combinations(st, 4):
        if on_line(line_of(quad[0], quad[1]), quad[2]) and on_line(line_of(quad[0], quad[1]), quad[3]):
            return False
        try:
            cc = circle_of(*quad[:3])
        except ValueError:
            continue
        if on_circle(cc, quad[3]):
            return False
    return True

def main():
    bank = json.load(open(sys.argv[1]))
    out = []
    for it in bank["items"]:
        r = verify(it["stones"], bank["w"], it["m"], bank["q"])
        r["tag"] = it["tag"]
        out.append(r)
    print(json.dumps(dict(w=bank["w"], q=bank["q"], results=out),
                     sort_keys=True, indent=1))

if __name__ == "__main__":
    main()
