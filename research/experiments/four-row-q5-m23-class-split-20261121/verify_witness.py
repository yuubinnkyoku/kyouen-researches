#!/usr/bin/env python3
"""Independent witness verifier (no census): exact Fraction geometry.

Usage: verify_witness.py w m q < stones.json   (JSON: [[x,y],...])
Checks (all must hold):
  (1) safety: no line/circle contains >= q stones;
  (2) maximality: every empty cell lies on some line/circle with >= q-1 stones;
  (3) deficiency: some row has <= q-2 stones.
Prints JSON {ok, n, rows, min_row}; exit code 0 (output has ok flag).
"""
import json, sys, math
from fractions import Fraction

def line_key(p, r):
    x1, y1 = p; x2, y2 = r
    a, b, c = y2 - y1, x1 - x2, x2 * y1 - x1 * y2
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c))
    if g: a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0): a, b, c = -a, -b, -c
    return (a, b, c)

def on_line(key, p):
    a, b, c = key
    return a * p[0] + b * p[1] + c == 0

def circle_key(p, r, s):
    """Circle through 3 points as (D, E, F) rationals with x^2+y^2+Dx+Ey+F=0.
    Returns None for collinear triples (infinite radius)."""
    x1, y1 = p; x2, y2 = r; x3, y3 = s
    det = (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if det == 0: return None
    b1, b2, b3 = -(x1 * x1 + y1 * y1), -(x2 * x2 + y2 * y2), -(x3 * x3 + y3 * y3)
    Dx = (b1 * (y2 - y3) + b2 * (y3 - y1) + b3 * (y1 - y2))
    Dy = (x1 * (b2 - b3) + x2 * (b3 - b1) + x3 * (b1 - b2))
    D, E = Fraction(Dx, det), Fraction(Dy, det)
    F = Fraction(-(x1 * x1 + y1 * y1)) - D * x1 - E * y1
    return (D, E, F)

def on_circle(key, p):
    D, E, F = key
    return p[0] * p[0] + p[1] * p[1] + D * p[0] + E * p[1] + F == 0

def main():
    w, m, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    stones = json.load(sys.stdin)
    st = [(int(x), int(y)) for x, y in stones]
    assert len(set(st)) == len(st)
    S = set(st)
    assert all(0 <= x < m and 0 <= y < w for x, y in st)
    N = len(st)

    def count_on_line(key):
        return sum(1 for p in st if on_line(key, p))

    def count_on_circle(key):
        return sum(1 for p in st if on_circle(key, p))

    # --- safety ---
    seen_l, seen_c = set(), set()
    for i in range(N):
        for j in range(i + 1, N):
            lk = line_key(st[i], st[j])
            if lk not in seen_l:
                seen_l.add(lk)
                if count_on_line(lk) >= q:
                    print(json.dumps({"ok": False, "why": "unsafe-line", "co": lk})); return
            for k in range(j + 1, N):
                ck = circle_key(st[i], st[j], st[k])
                if ck is None: continue
                if ck not in seen_c:
                    seen_c.add(ck)
                    if count_on_circle(ck) >= q:
                        print(json.dumps({"ok": False, "why": "unsafe-circle", "co": [str(v) for v in ck]})); return

    # --- maximality ---
    unblocked = []
    for y in range(w):
        for x in range(m):
            if (x, y) in S: continue
            cell = (x, y)
            blocked = False
            seen_l2, seen_c2 = set(), set()
            for i in range(N):
                lk = line_key(cell, st[i])
                if lk not in seen_l2:
                    seen_l2.add(lk)
                    if count_on_line(lk) >= q - 1: blocked = True; break
                for j in range(i + 1, N):
                    ck = circle_key(cell, st[i], st[j])
                    if ck is None: continue
                    if ck not in seen_c2:
                        seen_c2.add(ck)
                        if count_on_circle(ck) >= q - 1: blocked = True; break
                if blocked: break
            if not blocked: unblocked.append(cell)
    if unblocked:
        print(json.dumps({"ok": False, "why": "not-maximal", "cells": unblocked[:10]})); return

    # --- deficiency ---
    rows = [sum(1 for x, y in st if y == r) for r in range(w)]
    assert min(rows) <= q - 2, "not deficient"
    print(json.dumps({"ok": True, "n": N, "rows": rows, "min_row": min(rows)}))

main()
