#!/usr/bin/env python3
"""Direct occupied-subset mex audit of the exact two-forbidden-edge theorem.

No count-state recurrence is used by this verifier. A position is a bitmask;
a move is legal iff it does not contain either entire forbidden edge.
"""
from collections import Counter
from functools import lru_cache
import json


def closed_form(a, b, c, f):
    assert a >= 1 and b >= 1 and c >= 0 and f >= 0
    n = a + b + c + f
    if c > 0 and c == min(a, b):
        return 2 + ((max(a, b) - c + f) & 1)
    if c > min(a, b):
        return (n - 1) & 1
    return (n - 2) & 1


def subset_grundy(a, b, c, f):
    n = a + b + c + f
    edge1 = ((1 << a) - 1) | (((1 << c) - 1) << (a + b))
    edge2 = (((1 << b) - 1) << a) | (((1 << c) - 1) << (a + b))
    # The edges are incomparable since a,b >= 1.
    assert (edge1 & ~edge2) and (edge2 & ~edge1)
    @lru_cache(None)
    def grundy(mask):
        children = set()
        for i in range(n):
            if mask >> i & 1:
                continue
            nxt = mask | (1 << i)
            if (nxt & edge1) == edge1 or (nxt & edge2) == edge2:
                continue
            children.add(grundy(nxt))
        x = 0
        while x in children:
            x += 1
        return x
    return grundy(0)


def run(max_n=14):
    cases = 0
    by_value = Counter()
    by_relation = Counter()
    witnesses = {}
    for a in range(1, max_n + 1):
        for b in range(1, max_n + 1):
            for c in range(max_n + 1):
                for f in range(3):
                    n = a + b + c + f
                    if n > max_n:
                        continue
                    actual = subset_grundy(a, b, c, f)
                    predicted = closed_form(a, b, c, f)
                    assert actual == predicted, (a, b, c, f, actual, predicted)
                    cases += 1
                    by_value[str(actual)] += 1
                    relation = 'equal' if c == min(a, b) and c > 0 else ('greater' if c > min(a, b) else 'smaller')
                    by_relation[relation] += 1
                    witnesses.setdefault(str(actual), [a, b, c, f])
    return {'max_vertices': max_n, 'tested_labeled_type_parameters': cases,
            'grundy_counts': dict(sorted(by_value.items())),
            'relation_counts': dict(sorted(by_relation.items())),
            'first_witnesses_a_b_c_f': witnesses,
            'method': 'independent occupied-subset mex over all safe subsets for each type'}


if __name__ == '__main__':
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
