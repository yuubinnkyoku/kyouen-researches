#!/usr/bin/env python3
"""Audit published S7 rows, not the unprovided candidate-generation source."""
import csv
import hashlib
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
MANIFEST = HERE.parent / 'n11-s2-5960-milestone5-20261112' / 'output'


def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x,y), (y,10-x), (10-x,10-y), (10-y,x),
                      (10-x,y), (x,10-y), (y,x), (10-y,10-x))
            for i, (a,b) in enumerate(coords):
                result[i] |= 1 << (11*b+a)
    return result


def safe(mask):
    points = [(p % 11, p // 11) for p in range(121) if mask >> p & 1]
    for (a,b,c,d) in combinations(points, 4):
        (x1,y1),(x2,y2),(x3,y3),(x4,y4) = a,b,c,d
        cross = lambda x,y: (x2-x1)*(y-y1)-(y2-y1)*(x-x1)
        area = cross(x3,y3)
        if area == 0:
            if cross(x4,y4) == 0:
                return False
            continue
        q1, q2, q3 = (x*x+y*y for x,y in (a,b,c))
        den = 2*area
        ux = q1*(y2-y3)+q2*(y3-y1)+q3*(y1-y2)
        uy = q1*(x3-x2)+q2*(x1-x3)+q3*(x2-x1)
        if (den*x4-ux)**2+(den*y4-uy)**2 == (den*x1-ux)**2+(den*y1-uy)**2:
            return False
    return True


def main():
    rows = []
    for f in sorted(MANIFEST.glob('ms5_s6_manifest_part*.csv')):
        with f.open(newline='') as source:
            rows.extend(csv.DictReader(source))
    assert len(rows) == 7867
    manifest = {int(r['hex'],16) for r in rows}
    assert len(manifest) == len(rows)
    digest = hashlib.md5(('\n'.join(sorted(','.join((r['hex'],r['cost'],r['classes'])) for r in rows))+'\n').encode()).hexdigest()
    assert digest == '0e95a438dbcb486368393de9c73fc21e'
    candidates = []
    for f in sorted((HERE/'output').glob('ms5_s7_reuse_candidates_part*.csv')):
        with f.open(newline='') as source:
            for row in csv.reader(source):
                if row[0] != 's7_hex':
                    assert len(row) == 4
                    candidates.append(row)
    seen, parents, by_category = set(), set(), Counter()
    category_parents = {'1':set(),'2':set()}
    occupied_in_canonical_parent = direct_move_mismatch = 0
    for child_hex, parent_hex, move_text, category in candidates:
        child, parent, move = int(child_hex,16), int(parent_hex,16), int(move_text)
        assert parent in manifest and parent.bit_count() == 6 and child.bit_count() == 7
        assert 0 <= move < 121
        assert child == min(images(child))
        assert any(not (image >> move & 1) and child in images(image | (1 << move)) for image in images(parent))
        occupied_in_canonical_parent += bool(parent >> move & 1)
        direct_move_mismatch += bool(parent >> move & 1) or child not in images(parent | (1 << move))
        assert safe(child)
        assert child not in seen and category in category_parents
        seen.add(child)
        parents.add(parent)
        by_category[category] += 1
        category_parents[category].add(parent)
    with (HERE/'output/ms5_s7_knownloss_candidates.csv').open(newline='') as source:
        loss_rows = list(csv.reader(source))[1:]
    assert sorted(loss_rows) == sorted(r for r in candidates if r[3] == '1')
    result = {'manifest_rows':len(rows), 'manifest_md5':digest, 'candidate_rows':len(candidates),
              'distinct_children':len(seen), 'distinct_parents':len(parents),
              'category_counts':dict(sorted(by_category.items())),
              'category_parent_counts':{k:len(v) for k,v in sorted(category_parents.items())},
              'move_occupied_in_canonical_parent':occupied_in_canonical_parent,
              'move_does_not_directly_produce_child':direct_move_mismatch,
              'scope':'published rows only; no completeness or category-verdict verification'}
    assert (len(candidates),len(parents),by_category['1'],by_category['2']) == (8763,6276,396,8367)
    assert (len(category_parents['1']),len(category_parents['2'])) == (374,6073)
    assert (occupied_in_canonical_parent,direct_move_mismatch) == (119,7158)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
