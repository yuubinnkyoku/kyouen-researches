#!/usr/bin/env python3
"""Compare all class-1 search results with direct 5x8 brute force."""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
from audit_circle_census import long_circles

HERE = Path(__file__).resolve().parent


def run_search(index=0):
    source = (HERE/'slice_runner_class1.ts').read_text()
    replacements = [
        ('const W = 5, M = 19;', 'const W = 5, M = 8;'),
        ('const START = 79;', f'const START = {index};'),
        ('const NODE_CAP = 600_000;', 'const NODE_CAP = 5_000_000;'),
        ('const witnessList: number[][][] = [];',
         'const witnessList: number[][][] = []; const unique = new Set<string>();'),
        ('witnesses++; if (witnessList.length < 20)',
         'witnesses++; unique.add(JSON.stringify(rows)); if (witnessList.length < 20)'),
        ('while (idx >= 0 && idx < reps.length)', f'while (idx === {index} && idx < reps.length)'),
        ('cappedCase, witnesses, leaves, perKDone, lastS0s, witnessList };',
         'cappedCase, witnesses, leaves, perKDone, lastS0s, witnessList, unique: [...unique] };'),
    ]
    for old, new in replacements:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    with tempfile.TemporaryDirectory(prefix='five-row-class1-audit-') as tmp:
        script = Path(tmp)/'search.ts'
        script.write_text(source + '\nmain().then(result => console.log(JSON.stringify(result)));\n')
        result = subprocess.run(['node', '--disable-warning=ExperimentalWarning', str(script)],
                                check=True, text=True, capture_output=True, timeout=60)
    data = json.loads(result.stdout)
    assert data['nC'] == 16 and data['done'] == 1 and data['cappedCase'] == -1
    assert data['nextIdx'] == index + 1
    return data


def brute_force(deficient_stones=(0,1,2,3,4)):
    width = 8
    circles = [sum(1 << (width*y+x) for x,y in circle) for circle in long_circles(width)]
    assert len(circles) == 16
    deficient = sum(1 << (width+x) for x in deficient_stones)
    blanks = [width+x for x in range(width) if x not in deficient_stones]
    options = [[sum(1 << (width*y+x) for x in xs) for xs in combinations(range(width),6)]
               for y in (0,2,3,4)]
    found = set()
    checked = 0
    for pieces in product(*options):
        checked += 1
        state = deficient | pieces[0] | pieces[1] | pieces[2] | pieces[3]
        if any((circle & state).bit_count() > 6 for circle in circles):
            continue
        if not all(any((circle & (1 << p)) and (circle & state).bit_count() == 6
                       for circle in circles) for p in blanks):
            continue
        found.add(tuple(tuple(x for x in range(width) if state & (1 << (width*y+x)))
                        for y in range(5)))
    assert checked == 28**4
    return checked, found


def main():
    result = run_search()
    checked, expected = brute_force()
    actual = {tuple(map(tuple, json.loads(row))) for row in result['unique']}
    assert actual == expected
    canonical = json.dumps(sorted(actual), separators=(',',':')).encode()
    print(json.dumps({'rows':5, 'columns':8, 'deficient_row':1,
                      'deficient_stones':[0,1,2,3,4], 'direct_candidates':checked,
                      'search_branches':result['witnesses'], 'distinct_witnesses':len(actual),
                      'witness_set_sha256':sha256(canonical).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
