#!/usr/bin/env python3
"""Read a five-row q=7 witness as JSON on stdin and verify it directly."""
import json
import sys
from audit_circle_census import long_circles


def main():
    data = json.load(sys.stdin)
    width, deficient, rows = data['columns'], data['deficient_row'], data['rows']
    assert width >= 6 and 0 <= deficient < 5 and len(rows) == 5
    assert all(row == sorted(set(row)) and all(0 <= x < width for x in row) for row in rows)
    assert all(len(row) == 6 if y != deficient else len(row) <= 5 for y,row in enumerate(rows))
    selected = {(x,y) for y,row in enumerate(rows) for x in row}
    circles = [set(c) for c in long_circles(width)]
    counts = [len(c & selected) for c in circles]
    assert all(k <= 6 for k in counts)
    blocked = 0
    for y in range(5):
        for x in range(width):
            if (x,y) in selected:
                continue
            assert len(rows[y]) == 6 or any((x,y) in c and k == 6 for c,k in zip(circles,counts)), (x,y)
            blocked += 1
    print(json.dumps({'stones':len(selected), 'blocked_empty_points':blocked, 'circles':len(circles)}))


if __name__ == '__main__':
    main()
