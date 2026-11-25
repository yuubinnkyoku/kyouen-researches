#!/usr/bin/env python3
"""Independent complete finite mex check of the even-r, all-m closed formula."""
from functools import lru_cache
from itertools import combinations_with_replacement
import json
from pathlib import Path

if not __debug__:
    raise SystemExit('Assertions must remain enabled.')


def audit(w, r, m):
    @lru_cache(None)
    def grundy(x):
        children = set()
        for i, count in enumerate(x):
            if count == m:
                continue
            child = list(x)
            child[i] += 1
            child.sort(reverse=True)
            if child[0] + child[1] <= r:
                children.add(grundy(tuple(child)))
        result = 0
        while result in children:
            result += 1
        return result

    count = 0
    histogram = [0, 0, 0, 0]
    for asc in combinations_with_replacement(range(min(m, r) + 1), w):
        x = tuple(reversed(asc))
        a, b = x[:2]
        if a + b > r:
            continue
        total = sum(x)
        expected = ((total + m) % 2 if b < r-m else
                    2*((a-b) % 2)+(total-a) % 2)
        value = grundy(x)
        assert value == expected, (w, r, m, x, value, expected)
        histogram[value] += 1
        count += 1
    assert count == grundy.cache_info().currsize
    return dict(w=w, r=r, m=m, canonical_safe_states=count,
                grundy_histogram=histogram, root_grundy=grundy((0,) * w))


def main():
    rows = [audit(w, r, m) for w in (3, 5, 7, 9)
            for r in range(2, 21, 2) for m in range(1, r+3)]
    count = sum(row['canonical_safe_states'] for row in rows)
    result = dict(
        scope='Odd w, even r, common finite m; occupancy game, not 2D standard game.',
        evidence='Complete finite mex checks; universal proof is ../prism-two-maxima-20261005/audit.md.',
        parameter_cases=len(rows), canonical_safe_states=count, cases=rows,
    )
    target = Path(__file__).with_name('independent-even-finite-output.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(f'{len(rows)} complete finite cases; {count} states; all matched.')


if __name__ == '__main__':
    main()
