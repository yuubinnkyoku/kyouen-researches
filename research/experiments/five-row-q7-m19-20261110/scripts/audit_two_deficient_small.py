#!/usr/bin/env python3
"""Compare both two-deficient runners to direct 5x8 exhaustive enumeration."""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
from audit_circle_census import long_circles

HERE = Path(__file__).resolve().parent


def run_search(name, first=0, second=1, index=0):
    assert 0 <= first < second < 5
    source = (HERE/name).read_text()
    replacements = [
        ('const W = 5, M = 19;', 'const W = 5, M = 8;'),
        ('const Y0 = 0, Y1 = 1;', f'const Y0 = {first}, Y1 = {second};'),
        ('const START = 0;', f'const START = {index};'),
        ('const NODE_CAP = 600_000;', 'const NODE_CAP = 10_000_000;'),
        ('const witnessList: number[][][] = [];',
         'const witnessList: number[][][] = []; const unique = new Set<string>();'),
        ('witnesses++; if (witnessList.length < 10)',
         'witnesses++; unique.add(JSON.stringify(rows)); if (witnessList.length < 10)'),
        ('while (idx >= 0 && idx < reps.length)', f'while (idx === {index} && idx < reps.length)'),
        ('maxCaseNodes, witnessList };', 'maxCaseNodes, witnessList, unique: [...unique] };'),
    ]
    for old,new in replacements:
        assert source.count(old) == 1, (name,old)
        source = source.replace(old,new)
    assert f'const START = {index};' in source and f'const Y0 = {first}, Y1 = {second};' in source
    with tempfile.TemporaryDirectory(prefix='five-row-pair-audit-') as tmp:
        script = Path(tmp)/'search.ts'
        script.write_text(source+'\nmain().then(result => console.log(JSON.stringify(result)));\n')
        result = subprocess.run(['node','--disable-warning=ExperimentalWarning',str(script)],
                                check=True, capture_output=True, text=True, timeout=120)
    data = json.loads(result.stdout)
    assert data['nC'] == 16 and data['done'] == 1 and data['nextIdx'] == index+1 and data['cappedCase'] == -1
    assert data['lastS0s'][0].startswith(f'{index}:')
    return data


def brute_force(first=0, second=1, first_stones=(0,1,2,3,4)):
    assert 0 <= first < second < 5
    width = 8
    circles = [sum(1 << (width*y+x) for x,y in circle) for circle in long_circles(width)]
    assert len(circles) == 16
    row0 = sum(1 << (width*first+x) for x in first_stones)
    row1 = [sum(1 << (width*second+x) for x in xs)
            for k in range(6) for xs in combinations(range(width),k)]
    full = [[sum(1 << (width*y+x) for x in xs) for xs in combinations(range(width),6)]
            for y in range(5) if y not in (first,second)]
    found = set()
    checked = 0
    for a,b,c,d in product(row1,*full):
        checked += 1
        state = row0 | a | b | c | d
        if any((circle & state).bit_count() > 6 for circle in circles):
            continue
        blanks = [width*y+x for y in (first,second) for x in range(width)
                  if not state & (1 << (width*y+x))]
        if not all(any((circle & (1 << p)) and (circle & state).bit_count() == 6
                       for circle in circles) for p in blanks):
            continue
        found.add(tuple(tuple(x for x in range(width) if state & (1 << (width*y+x)))
                        for y in range(5)))
    assert checked == 219*28**3
    return checked, found


def main():
    checked, expected = brute_force()
    runs = []
    for name in ('two_deficient_pair_runner.ts','two_deficient_pair_runner_flat.ts'):
        result = run_search(name)
        actual = {tuple(map(tuple,json.loads(row))) for row in result['unique']}
        assert actual == expected, (name,len(actual),len(expected))
        runs.append({'runner':name,'search_branches':result['witnesses'],
                     'nodes':result['maxCaseNodes'],'distinct_witnesses':len(actual)})
    canonical = json.dumps(sorted(expected),separators=(',',':')).encode()
    print(json.dumps({'rows':5,'columns':8,'deficient_rows':[0,1],
                      'first_row_stones':[0,1,2,3,4], 'direct_candidates':checked,
                      'distinct_witnesses':len(expected),'witness_set_sha256':sha256(canonical).hexdigest(),
                      'runs':runs},indent=2))


if __name__ == '__main__':
    main()
