#!/usr/bin/env python3
"""forbidgen_write.py — write the canonical forbidden-quartet catalog text
(system B: independent Leibniz 4x4 determinant / cross-product implementation,
copied verbatim in geometry from scripts/forbidgen.py of the n7 catalog
experiment, plus the ability to save the canonical text to a file).

Canonical text format: "n=<n>\\n" + "<a> <b> <c> <d>\\n" per quartet,
quartets ascending, lexicographically sorted. The sha256 of this text is
pinned for n=4..6 by the n7 catalog experiment (n=5, n=6) and the s12-s13
anchors; n=4 is recorded here.

Usage: python3 forbidgen_write.py <n> <out.txt>
Prints the metadata JSON (same fields as forbidgen.py) on stdout.
"""
import hashlib
import itertools
import json
import sys


def det4(m):
    """Exact integer determinant of a 4x4 matrix (Leibniz, 24 terms)."""
    import itertools as it
    total = 0
    for perm in it.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j])
        sign = -1 if inv % 2 else 1
        prod = 1
        for r in range(4):
            prod *= m[r][perm[r]]
        total += sign * prod
    return total


def collinear4(pts):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = pts
    def cross(ax, ay, bx, by, cx, cy):
        return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    return (cross(x1, y1, x2, y2, x3, y3) == 0
            and cross(x1, y1, x2, y2, x4, y4) == 0)


def concyclic4(pts):
    m = [[x, y, x * x + y * y, 1] for (x, y) in pts]
    return det4(m) == 0


def main():
    n = int(sys.argv[1])
    outpath = sys.argv[2]
    cells = [(x, y) for y in range(n) for x in range(n)]  # c = x + n*y
    quarts = []
    for combo in itertools.combinations(range(n * n), 4):
        pts = [cells[c] for c in combo]
        if collinear4(pts) or concyclic4(pts):
            quarts.append(list(combo))
    quarts.sort()
    text = "n=%d\n" % n + "".join(" ".join(map(str, q)) + "\n" for q in quarts)
    with open(outpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    h = hashlib.sha256(text.encode()).hexdigest()
    print(json.dumps({
        "n": n,
        "cells": n * n,
        "count": len(quarts),
        "sha256_quartetlist_text": h,
        "first": quarts[:3],
        "last": quarts[-3:],
    }))


if __name__ == "__main__":
    main()
