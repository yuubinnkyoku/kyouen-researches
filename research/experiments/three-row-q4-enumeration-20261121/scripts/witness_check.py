#!/usr/bin/env python3
"""Independent exact-integer SAFE+MAXIMAL witness verifier (stdlib only).

Circle test: 4 points concyclic/collinear iff det[[x^2+y^2,x,y,1]] == 0.
Line test: det[[x,y,1]] == 0 for 3 points. All integer, exact.
SAFE: no curve (line or circle) carries >= q stones.
MAXIMAL: every empty cell is blocked by some curve carrying >= q-1 stones.
Usage: witness_check.py <w> <m> <q> <json-stones>
"""
import json, sys
from itertools import combinations

def det3(p0, p1, p2):
    return (p1[0]-p0[0])*(p2[1]-p0[1]) - (p1[1]-p0[1])*(p2[0]-p0[0])

def concyclic(p0, p1, p2, p3):
    if det3(p0, p1, p2) == 0:  # collinear triple lies on lines, not a circle; handled by line test
        return False
    m = [[x*x + y*y, x, y, 1] for (x, y) in (p0, p1, p2, p3)]
    d = (m[0][0]*(m[1][1]*(m[2][2]*m[3][3]-m[2][3]*m[3][2])
                 -m[1][2]*(m[2][1]*m[3][3]-m[2][3]*m[3][1])
                 +m[1][3]*(m[2][1]*m[3][2]-m[2][2]*m[3][1]))
        -m[0][1]*(m[1][0]*(m[2][2]*m[3][3]-m[2][3]*m[3][2])
                 -m[1][2]*(m[2][0]*m[3][3]-m[2][3]*m[3][0])
                 +m[1][3]*(m[2][0]*m[3][2]-m[2][2]*m[3][0]))
        +m[0][2]*(m[1][0]*(m[2][1]*m[3][3]-m[2][3]*m[3][1])
                 -m[1][1]*(m[2][0]*m[3][3]-m[2][3]*m[3][0])
                 +m[1][3]*(m[2][0]*m[3][1]-m[2][1]*m[3][0]))
        -m[0][3]*(m[1][0]*(m[2][1]*m[3][2]-m[2][2]*m[3][1])
                 -m[1][1]*(m[2][0]*m[3][2]-m[2][2]*m[3][0])
                 +m[1][2]*(m[2][0]*m[3][1]-m[2][1]*m[3][0])))
    return d == 0

def main():
    w, m, q = map(int, sys.argv[1:4])
    stones = [tuple(p) for p in json.loads(sys.argv[4])]
    S = set(stones)
    assert len(S) == len(stones), "duplicate stone"
    for (x, y) in stones:
        assert 0 <= x < m and 0 <= y < w, f"stone {x},{y} outside {w}x{m}"
    # SAFE: lines
    for trio in combinations(stones, 3):
        if det3(*trio) == 0:
            extra = [p for p in stones if p not in trio and det3(trio[0], trio[1], p) == 0]
            if len(trio) + len(extra) >= q:
                print(json.dumps({"ok": False, "why": "unsafe-line", "pts": [trio[0], trio[1]]})); return
    # SAFE: circles
    for quad in combinations(stones, 4):
        if concyclic(*quad):
            print(json.dumps({"ok": False, "why": "unsafe-circle", "pts": list(quad)})); return
    # MAXIMAL
    for y in range(w):
        for x in range(m):
            if (x, y) in S: continue
            blocked = False
            # line through new cell + >= q-1 stones collinear with it
            for others in combinations([p for p in stones if p != (x, y)], q - 1):
                if all(det3((x, y), others[0], p) == 0 for p in others[1:]):
                    blocked = True; break
            if blocked: continue
            # circle through new cell + >= q-1 stones: circle determined by new cell + 2 stones,
            # check remaining stones
            for pair in combinations(stones, 2):
                a, b = pair
                if det3((x, y), a, b) == 0: continue  # collinear -> line case
                cnt = 2
                for p in stones:
                    if p in pair: continue
                    if concyclic((x, y), a, b, p): cnt += 1
                if cnt >= q - 1:
                    blocked = True; break
            if not blocked:
                print(json.dumps({"ok": False, "why": "not-maximal", "cell": [x, y]})); return
    rows = [sum(1 for (_, yy) in stones if yy == ry) for ry in range(w)]
    print(json.dumps({"ok": True, "size": len(stones), "rows": rows, "minRow": min(rows)}))

main()
