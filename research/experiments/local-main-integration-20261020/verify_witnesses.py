"""Check the two supplied witnesses; this does not search for new sets."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path


def forbidden(points):
    x0, y0 = points[0]
    q0 = x0*x0 + y0*y0
    a, b, c = [(x*x+y*y-q0, x-x0, y-y0) for x, y in points[1:]]
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0])) == 0


def verify(n, ids):
    assert len(ids) == len(set(ids)) == n
    assert all(0 <= p < n*n for p in ids)
    stones = [(p % n, p // n) for p in ids]
    assert not any(forbidden(q) for q in combinations(stones, 4))
    triples = list(combinations(stones, 3))
    counts = [sum(forbidden([*t, p]) for t in triples)
              for p in ((x, y) for y in range(n) for x in range(n)) if p not in stones]
    assert len(counts) == n*n-n and min(counts) > 0
    return dict(n=n, ids=ids, forbidden_quads=0, unblocked_points=0,
                blocking_triple_histogram=dict(sorted(Counter(counts).items())))


if __name__ == "__main__":
    results = [verify(12, [5,50,56,57,61,66,68,72,77,88,98,107]),
               verify(13, [25,28,35,55,84,85,90,99,107,108,119,130,140])]
    output = json.dumps(results, indent=2) + "\n"
    Path(__file__).with_name("witness-validation.json").write_text(output, encoding="utf-8")
    print(output, end="")
