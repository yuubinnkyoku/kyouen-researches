"""Canonical-curve analysis of the enumerated n=9 minimum-maximal sets.

For each maximal size-9 safe set S it builds every line/circle determined by a
triple of S, marks the empty points lying on a curve that already carries three
stones of S, and reports min_p b_S(p) (the least number of blocking curves at an
empty point).  K0297 asks whether this minimum is always 1.

Reads state_root*.json produced by enumerate_n9.py from this directory.
Writes ../output/maximal_sets_n9.json and ../output/n9_canonical_minb.json.
"""
import glob
import json
import os
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "output"))
N = 9
P = N * N


def pt(i):
    return (i % N, i // N)


def line_id(a, b, c):
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    if g:
        a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return ("L", a, b, c)


def circle_id(D, E, F, scale):
    vals = [scale, D, E, F]
    g = 0
    for v in vals:
        g = gcd(g, abs(v))
    if g:
        vals = [v // g for v in vals]
    for v in vals:
        if v != 0:
            if v < 0:
                vals = [-x for x in vals]
            break
    return ("C",) + tuple(vals)


def curve_of_triple(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    if cross == 0:
        a = y2 - y1
        b = x1 - x2
        return "line", line_id(a, b, a * x1 + b * y1)
    A1, B1 = x1 - x2, y1 - y2
    C1 = (x2 * x2 + y2 * y2) - (x1 * x1 + y1 * y1)
    A2, B2 = x1 - x3, y1 - y3
    C2 = (x3 * x3 + y3 * y3) - (x1 * x1 + y1 * y1)
    det = A1 * B2 - A2 * B1
    Dn = C1 * B2 - C2 * B1
    En = A1 * C2 - A2 * C1
    Fn = -(x1 * x1 + y1 * y1) * det - Dn * x1 - En * y1
    return "circle", circle_id(Dn, En, Fn, det)


def on_line(a, b, c, p):
    return a * p[0] + b * p[1] == c


def on_circle(scale, D, E, F, p):
    return scale * (p[0] * p[0] + p[1] * p[1]) + D * p[0] + E * p[1] + F == 0


def load_sets():
    sets = []
    seen = set()
    for f in sorted(glob.glob(os.path.join(OUT, "state_root*.json"))):
        d = json.load(open(f))
        if not d["complete"]:
            raise SystemExit("incomplete state file: %s" % f)
        for s in d["sets"]:
            key = tuple(sorted(s))
            if key not in seen:
                seen.add(key)
                sets.append(list(key))
    return sets


def main():
    points = [pt(i) for i in range(P)]
    sets = load_sets()
    hist = {}
    nonsafe = 0
    nonmax = 0
    for S in sets:
        Sp = [pt(i) for i in S]
        Sset = set(Sp)
        curves = {}
        for a in range(len(Sp)):
            for b in range(a + 1, len(Sp)):
                for c in range(b + 1, len(Sp)):
                    kind, cid = curve_of_triple(Sp[a], Sp[b], Sp[c])
                    if cid not in curves:
                        curves[cid] = kind
        blocked = {}
        curveS = {}
        for cid, kind in curves.items():
            if kind == "line":
                a, b, c = cid[1], cid[2], cid[3]
                members = [p for p in points if on_line(a, b, c, p)]
            else:
                sc, Dn, En, Fn = cid[1], cid[2], cid[3], cid[4]
                members = [p for p in points if on_circle(sc, Dn, En, Fn, p)]
            scnt = sum(1 for p in members if p in Sset)
            curveS[cid] = scnt
            if scnt >= 3:
                for p in members:
                    if p not in Sset:
                        blocked[p] = blocked.get(p, 0) + 1
        if any(v >= 4 for v in curveS.values()):
            nonsafe += 1
        empt = [p for p in points if p not in Sset]
        vals = [blocked.get(p, 0) for p in empt]
        mn = min(vals)
        if mn == 0:
            nonmax += 1
        hist[mn] = hist.get(mn, 0) + 1

    json.dump({"n": 9, "k": 9, "distinct_sets": len(sets),
               "min_b_histogram": {str(k): v for k, v in sorted(hist.items())},
               "nonmaximal": nonmax, "unsafe": nonsafe,
               "sets": sets},
              open(os.path.join(OUT, "maximal_sets_n9.json"), "w"))
    json.dump({"n": 9, "k": 9, "distinct_sets": len(sets),
               "min_b_histogram": {str(k): v for k, v in sorted(hist.items())},
               "nonmaximal": nonmax, "unsafe": nonsafe},
              open(os.path.join(OUT, "n9_canonical_minb.json"), "w"))
    print("distinct maximal size-9 sets:", len(sets))
    print("canonical min-b histogram:", dict(sorted(hist.items())))
    print("non-maximal:", nonmax, "unsafe:", nonsafe)


if __name__ == "__main__":
    main()
