#!/usr/bin/env python3
"""Derive ordinary-board moves and all five-stone parents of verified P witnesses."""
from pathlib import Path
import gzip
import itertools
import json

root = Path(__file__).resolve().parent
original = {3, 169, 173, 339}
canonical_four = {73, 153, 189, 269}
maps = []
for perm in itertools.permutations(range(3)):
    for flips in itertools.product((False, True), repeat=3):
        mapping = []
        for point in range(343):
            coords = (point//49, point//7 % 7, point % 7)
            mapped = [6-coords[perm[i]] if flips[i] else coords[perm[i]] for i in range(3)]
            mapping.append((mapped[0]*7+mapped[1])*7+mapped[2])
        maps.append(mapping)
assert len(set(map(tuple, maps))) == 48


def canonical(points):
    return min((tuple(sorted(m[p] for p in points)) for m in maps),
               key=lambda points: sum(1 << p for p in points))


records = []
for line in (root/'central-known-five.txt').read_text().splitlines():
    points = list(map(int, line.split()))
    identifier = next(p for p in points if p not in canonical_four)
    checked = json.loads((root/f'central-five-{identifier}-verified.json').read_text())
    assert checked['verified'] and checked['outcome'] == 'N'
    with gzip.open(root/f'central-five-{identifier}.cert.gz', 'rt') as proof:
        header = proof.readline().split()
        assert header[:3] == ['Q5CUBE2', '7', '6']
        words = list(map(int, header[3:]))
        witness = None
        for line in proof:
            row = list(map(int, line.split()))
            if row[:6] == words:
                assert row[6] == 1
                witness = [i for i in range(343) if row[7+i//64] >> (i % 64) & 1]
                break
    assert witness is not None and len(witness) == 6
    actuals = [sorted(m[p] for p in points) for m in maps
               if {m[p] for p in canonical_four} == original]
    actual = min(actuals, key=lambda points: next(p for p in points if p not in original))
    responses = []
    for mapping in maps:
        transformed = {mapping[p] for p in witness}
        if set(actual) < transformed:
            responses.append(next(iter(transformed-set(actual))))
    assert responses
    reply = min(responses)
    records.append({'id': identifier, 'canonical_five': points,
                    'canonical_p_witness': witness, 'original_five': actual,
                    'fifth_point': next(p for p in actual if p not in original),
                    'winning_move': reply, 'original_six': sorted(actual+[reply])})
(root/'central-five-witnesses.json').write_text(json.dumps(records, indent=2)+'\n')
witnesses = sorted({tuple(row['canonical_p_witness']) for row in records})
parents = sorted({canonical(set(witness)-{point}) for witness in witnesses for point in witness})
(root/'central-five-parents.json').write_text(json.dumps({
    'verified_p_six_orbits': len(witnesses), 'n_five_parent_orbits': len(parents),
    'parents': parents,
    'justification': 'Every five-stone subset of a safe P six-stone position is N: add its missing point.',
    'directly_checked_n_five_roots': len(records),
}, indent=2)+'\n')
