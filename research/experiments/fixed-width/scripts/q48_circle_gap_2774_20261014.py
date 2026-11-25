#!/usr/bin/env python3
"""Exact finite classification of 4-row 8-point lattice circles up to width 2774."""
from math import isqrt
import json

BOUND = 2773

def chord_types(bound=BOUND):
    ans = []
    for a in range(1, bound + 1):
        for b in range(1, bound + 1):
            c2 = 2*b*b - a*a - 8
            if c2 <= 0:
                continue
            c = isqrt(c2)
            if c*c != c2 or c > bound:
                continue
            d2 = 2*c*c - b*b - 8
            if d2 <= 0:
                continue
            d = isqrt(d2)
            if d*d != d2 or d > bound:
                continue
            if (a-b)%2 or (b-c)%2 or (c-d)%2:
                continue
            ans.append((a,b,c,d))
    return sorted(ans)

def circles_via_pair_products(m):
    """Independent enumeration from integer root sums/products, not chord squares."""
    circles = []
    for s in range(2*m - 1):
        products = {a*(s-a):(a,s-a) for a in range(m) if a < s-a < m}
        for p0 in products:
            for p1 in products:
                p2 = 2*p1 - p0 + 2
                p3 = 3*p1 - 2*p0 + 6
                if p2 in products and p3 in products:
                    pairs = tuple(products[p] for p in (p0,p1,p2,p3))
                    B = p1-p0-1
                    assert all(x*x+y*y-s*x+B*y+p0 == 0
                               for y,(a,b) in enumerate(pairs) for x in (a,b))
                    circles.append((s,pairs))
    return circles

def circle_count(m):
    assert 1 <= m <= 2774
    return max(0,m-3) + 2*max(0,m-73) + 2*(m == 2774)

def main():
    patterns = chord_types()
    expected = [(1,3,3,1), (35,51,63,73), (73,63,51,35),
                (1331,1935,2391,2773), (2773,2391,1935,1331)]
    assert patterns == expected, patterns
    for m in range(1,75):
        assert len(circles_via_pair_products(m)) == circle_count(m), m
    result = {
        "scope":"1 <= m <= 2774; exact finite enumeration, not all lengths",
        "chord_patterns_span_at_most_2773":patterns,
        "independent_product_enumeration_checked_all_m":"1..74",
        "circle_counts":{str(m):circle_count(m) for m in (4,73,74,100,2773,2774)},
        "forbidden_8sets_formula":"4*C(m,8)+C(m)",
        "first_new_type_after_m74":2774
    }
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
