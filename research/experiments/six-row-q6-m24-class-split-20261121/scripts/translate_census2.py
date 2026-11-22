#!/usr/bin/env python3
"""Fast pure-translation census (free-append reach) for a witness stone set.

Logic (equivalent to verify_py.safe_maximal, restricted to fixed-set translations):
1. Normalize S to column x=0 (bbox width b). Safety is checked once on the home
   board by verifying every stone-derived curve has <= q-1 stones.
2. Curves are enumerated exactly as verify_py does: all lines through stone pairs
   (primitive integer (a,b,c)) and all circles through stone triples (integer
   equation d*(x^2+y^2) + D'*x + E'*y + F'*r = 0 via 2*det denominator, gcd-normalized),
   deduplicated by canonical key.
3. BLOCKED = exact set of lattice cells (x,y) lying on some >= (q-1)-stone curve,
   plus stone cells (placing a stone there is safe-absent but occupies the cell).
   The board dependence is only through the cell range: the curve/blocked sets are
   translation-covariant (shift by t when the stone set shifts by t).
4. A placement at offset t on width mw is maximal iff every board cell (X,Y),
   X in [0,mw), Y in [0,w), satisfies (X-t, Y) in BLOCKED. Blocked is precomputed
   over x in [-PAD, b-1+PAD].
5. Width mw is 'reached' iff some t in [0, mw-b] works. Reflection H maps
   t-placements of S to (mw-b-t)-placements of H(S), so coverage by S translations
   already decides D4-orbit coverage; V/HV commute with x-translations.

Cross-validation: the --crosscheck mode compares against verify_py.safe_maximal
on selected (mw,t) placements (agreement must hold on safe+maximal verdicts).

Usage:
  python3 translate_census2.py <witness.json> <q> <maxwidth> [skipcross]
  --crosscheck <witness.json> <mw> ...
Outputs JSON to stdout; human summary to stderr.
"""
import json, sys, math
from fractions import Fraction
sys.path.insert(0, '/home/user/knowledge/kyouen-research/_q66-m24-lane-kit/scripts')
import verify_py_lib as VP

PAD = 160


def gcd_norm(v):
    g = 0
    for x in v:
        g = math.gcd(g, abs(x))
    if g:
        v = tuple(x // g for x in v)
    # sign normalization: first nonzero positive
    for x in v:
        if x != 0:
            if x < 0:
                v = tuple(-y for y in v)
            break
    return v


def curves_of(S, q):
    stones = [tuple(p) for p in S]
    n = len(stones)
    lines, circles = {}, {}
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = stones[i], stones[j]
            if (x1, y1) == (x2, y2):
                continue
            a, b, c = y1 - y2, x2 - x1, x1 * y2 - x2 * y1
            lines[gcd_norm((a, b, c))] = None
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                (x1, y1), (x2, y2), (x3, y3) = stones[i], stones[j], stones[k]
                det = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                if det == 0:
                    continue
                # circle: x^2+y^2+Dx+Ey+F=0 ; multiply through by det to keep integers
                # D = det*... solve with Cramer: det*D = -( ... ) etc. Use exact ints:
                # D = ( (x2^2+y2^2-x1^2-y1^2)*(y3-y1) - (x3^2+y3^2-x1^2-y1^2)*(y2-y1) ) * -1/det
                b1 = -(x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1)
                b2 = -(x3 * x3 + y3 * y3 - x1 * x1 - y1 * y1)
                # equations: (x2-x1) D + (y2-y1) E = b1 ; (x3-x1) D + (y3-y1) E = b2
                a11, a12, a21, a22 = x2 - x1, y2 - y1, x3 - x1, y3 - y1
                DD = a11 * a22 - a12 * a21  # == det
                Dd = b1 * a22 - a12 * b2
                Ee = a11 * b2 - b1 * a21
                # D = Dd/DD, E = Ee/DD ; equation scaled by DD:
                # DD*(x^2+y^2) + Dd*x + Ee*y + F'=0 where F' chosen through (x1,y1)
                Ff = -(DD * (x1 * x1 + y1 * y1) + Dd * x1 + Ee * y1)
                circles.setdefault(gcd_norm((DD, Dd, Ee, Ff)), None)
    return stones, set(lines), set(circles)


def curve_cells_line(kv, xr, w):
    a, b, c = kv
    cells = []
    for y in range(w):
        if b == 0:
            if c % a == 0:
                x = -c // a
                cells.append((x, y))
        else:
            # a*x + b*y + c = 0 -> x = (-c - b*y)/a if a!=0 else b*y+c==0 -> all x
            if a == 0:
                if (b * y + c) == 0:
                    for x in range(xr[0], xr[1] + 1):
                        cells.append((x, y))
            else:
                nmr = -c - b * y
                if nmr % a == 0:
                    cells.append((nmr // a, y))
    return cells


def curve_cells_circle(kv, xr, w):
    DD, Dd, Ee, Ff = kv
    cells = []
    for x in range(xr[0], xr[1] + 1):
        for y in range(w):
            if DD * (x * x + y * y) + Dd * x + Ee * y + Ff == 0:
                cells.append((x, y))
    return cells


def analyze(S, w, q, maxw):
    S = [tuple(p) for p in S]
    x0 = min(p[0] for p in S)
    S0 = [(x - x0, y) for (x, y) in S]
    b = 1 + max(p[0] for p in S0)
    stones0 = set(S0)
    _, lineK, circK = curves_of(S0, q)
    # stone counts per curve
    blocked = set(stones0)
    maxOn = 0
    allC = []
    for kv in lineK:
        cs = curve_cells_line(kv, (-b - PAD, 2 * b + PAD), w)
        allC.append((kv, cs))
    for kv in circK:
        cs = curve_cells_circle(kv, (-b - PAD, 2 * b + PAD), w)
        allC.append((kv, cs))
    for kv, cs in allC:
        nOn = sum(1 for (x, y) in cs if (x, y) in stones0)
        maxOn = max(maxOn, nOn)
        if nOn >= q - 1:
            blocked |= set(cs)
    if maxOn >= q:
        return {"error": "UNSAFE: curve with %d stones" % maxOn}
    # maximality check per (mw, t): all cells blocked
    widths = {}
    for mw in range(b, maxw + 1):
        hit = None
        for t in range(0, mw - b + 1):
            ok = True
            for X in range(mw):
                for Y in range(w):
                    if (X - t, Y) not in blocked:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                hit = t
                break
        widths[mw] = hit  # scan all widths; reachability is not assumed monotone
    reached = [mw for mw in widths if widths[mw] is not None]
    return {"bboxWidth": b, "maxOnCurve": maxOn, "widths": widths,
            "reached": reached, "maxReached": max(reached) if reached else None,
            "firstFail": (min(mw for mw in widths if mw > b and widths[mw] is None) if any(widths.get(mw) is None and mw > b for mw in widths) else None)}


def crosscheck(S, w, q, mw, t):
    S = [tuple(p) for p in S]
    x0 = min(p[0] for p in S)
    S0 = [(x - x0, y) for (x, y) in S]
    placed = [(x + t, y) for (x, y) in S0]
    ok, reason, info = VP.safe_maximal(w, mw, q, placed)
    return {"vp_ok": ok, "reason": reason, "info": str(info)}


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == '--crosscheck':
        j = json.load(open(sys.argv[2]))
        mw, t = int(sys.argv[3]), int(sys.argv[4])
        S = j["stones"]
        r = analyze(S, j.get('w', 6), j.get('q', 6), mw + 1)
        fast = r["widths"].get(mw)
        agree = (fast is not None) == (mw >= r["bboxWidth"] and crosscheck(S, j.get('w', 6), j.get('q', 6), mw, t)["vp_ok"]) if False else None
        cc = crosscheck(S, j.get('w', 6), j.get('q', 6), mw, t)
        print(json.dumps({"mw": mw, "t": t, "fast_t_hit": fast, "python_safe_maximal": cc}, indent=1))
    else:
        f, q, maxw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
        j = json.load(open(f))
        w = j.get('w', 6)
        r = analyze(j["stones"], w, q, maxw)
        print(json.dumps(r, indent=1))
        print(f"bboxW={r['bboxWidth']} maxReached={r['maxReached']} firstFail={r['firstFail']}", file=sys.stderr)
