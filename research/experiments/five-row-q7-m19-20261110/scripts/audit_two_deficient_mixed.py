#!/usr/bin/env python3
"""Compare mixed deficient-row sizes for the 5x8 pair {0,1}."""
from hashlib import sha256
import json
from audit_class1_mixed import representatives
from audit_two_deficient_small import brute_force, run_search


def main():
    reps = representatives()
    indices = [0,27,28,66,94,110,114]
    results = []
    for index in indices:
        stones = reps[index]
        checked, expected = brute_force(0,1,stones)
        runs = []
        for name in ('two_deficient_pair_runner.ts','two_deficient_pair_runner_flat.ts'):
            result = run_search(name,0,1,index)
            assert result['lastS0s'][0].split('(')[0] == f"{index}:{','.join(map(str,stones))}"
            actual = {tuple(map(tuple,json.loads(row))) for row in result['unique']}
            assert actual == expected, (index,stones,name,len(actual),len(expected))
            runs.append({'runner':name,'search_branches':result['witnesses'],
                         'nodes':result['maxCaseNodes']})
        canonical = json.dumps(sorted(expected),separators=(',',':')).encode()
        results.append({'index':index,'first_row_stones':stones,'candidates_checked':checked,
                        'distinct_witnesses':len(expected),'witness_set_sha256':sha256(canonical).hexdigest(),
                        'runs':runs})
    assert {len(r['first_row_stones']) for r in results} == set(range(6))
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
