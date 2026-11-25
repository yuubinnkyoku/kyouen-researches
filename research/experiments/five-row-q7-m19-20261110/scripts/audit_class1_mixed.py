#!/usr/bin/env python3
"""Compare six different deficient-row sizes against direct 5x8 enumeration."""
from itertools import combinations
import json
from audit_class1_small import brute_force, run_search


def representatives():
    result = []
    for k in range(5,-1,-1):
        for row in combinations(range(8),k):
            mirror = tuple(sorted(7-x for x in row))
            # Match the runner's comma-separated string comparison.
            if ','.join(map(str,row)) <= ','.join(map(str,mirror)):
                result.append(row)
    return result


def main():
    reps = representatives()
    assert len(reps) == 115
    indices = [0,27,28,66,94,110,114]
    results = []
    for index in indices:
        row = reps[index]
        search = run_search(index)
        checked, expected = brute_force(row)
        actual = {tuple(map(tuple,json.loads(value))) for value in search['unique']}
        assert actual == expected, (index,row,len(actual),len(expected))
        results.append({'index':index, 'deficient_stones':row, 'candidates_checked':checked,
                        'search_branches':search['witnesses'], 'distinct_witnesses':len(actual)})
    assert {len(r['deficient_stones']) for r in results} == set(range(6))
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
