#!/usr/bin/env python3
"""Compare all six row-pair representatives on a fixed 5x8 case."""
from hashlib import sha256
import json
from audit_two_deficient_small import brute_force, run_search


def main():
    results = []
    for first,second in ((0,1),(0,2),(0,3),(0,4),(1,2),(1,3)):
        checked, expected = brute_force(first,second)
        runs = []
        for name in ('two_deficient_pair_runner.ts','two_deficient_pair_runner_flat.ts'):
            result = run_search(name,first,second)
            actual = {tuple(map(tuple,json.loads(row))) for row in result['unique']}
            assert actual == expected, (first,second,name,len(actual),len(expected))
            runs.append({'runner':name,'search_branches':result['witnesses'],
                         'nodes':result['maxCaseNodes']})
        canonical = json.dumps(sorted(expected),separators=(',',':')).encode()
        results.append({'deficient_rows':[first,second],'first_row_stones':[0,1,2,3,4],
                        'candidates_checked':checked,'distinct_witnesses':len(expected),
                        'witness_set_sha256':sha256(canonical).hexdigest(),'runs':runs})
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
