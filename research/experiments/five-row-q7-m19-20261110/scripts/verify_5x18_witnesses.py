#!/usr/bin/env python3
"""Check two 5x18 configurations against independently generated long circles."""
import json
from pathlib import Path
from audit_circle_census import long_circles

ROOT = Path(__file__).resolve().parents[2]
FIRST = ROOT/'fixed-width-frontier-20261005/output/q57_independent_witness.json'
SECOND = [[0,1,2,6,14],[4,7,9,11,13,16],[2,4,7,11,13,16],
          [3,5,7,10,11,15],[7,8,10,12,13,17]]


def verify(rows, circles):
    assert len(rows) == 5 and [len(r) for r in rows] == [5,6,6,6,6]
    assert all(r == sorted(set(r)) and all(0 <= x < 18 for x in r) for r in rows)
    chosen = {(x,y) for y,row in enumerate(rows) for x in row}
    assert len(chosen) == 29
    circle_sets = [set(c) for c in circles]
    counts = [len(c & chosen) for c in circle_sets]
    assert all(k <= 6 for k in counts)
    blocked = 0
    for y in range(5):
        for x in range(18):
            point = (x,y)
            if point in chosen:
                continue
            assert len(rows[y]) == 6 or any(point in c and k == 6 for c,k in zip(circle_sets,counts)), point
            blocked += 1
    return {'stones':len(chosen),'blocked_empty_points':blocked}


def main():
    circles = long_circles(18)
    assert len(circles) == 84
    first = json.loads(FIRST.read_text())['lower_bound_witness']['rows']
    print(json.dumps({'circles':len(circles),'witnesses':[verify(first,circles),verify(SECOND,circles)]},indent=2))


if __name__ == '__main__':
    main()
