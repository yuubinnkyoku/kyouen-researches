#!/usr/bin/env python3
"""Wrap the verified tetrahedron P proof with its canonical N triangle parent."""
from pathlib import Path
import gzip
import itertools
import json
import sys

root = Path(__file__).resolve().parent
destination = Path(sys.argv[1])
assert not destination.exists()
with gzip.open(root/'stage-2.cert.gz', 'rt') as proof:
    header = proof.readline().split()
    assert header[:3] == ['Q5CUBE2', '7', '6']
    tetra_words = list(map(int, header[3:]))
    tetra = [p for p in range(343) if tetra_words[p//64] >> (p % 64) & 1]
    assert tetra == [57, 89, 257, 281]
    maps = []
    for axes in itertools.permutations(range(3)):
        for flips in itertools.product((False, True), repeat=3):
            mapping = []
            for p in range(343):
                coords = (p//49, p//7 % 7, p % 7)
                mapped = [6-coords[axes[j]] if flips[j] else coords[axes[j]] for j in range(3)]
                mapping.append((mapped[0]*7+mapped[1])*7+mapped[2])
            maps.append(mapping)
    parents = set()
    for omitted in tetra:
        parent = set(tetra)-{omitted}
        images = [tuple(sorted(m[p] for p in parent)) for m in maps]
        parents.add(min(images, key=lambda points: sum(1 << p for p in points)))
    assert len(parents) == 1
    parent = list(next(iter(parents)))
    assert parent == [61, 85, 253]
    words = [sum(1 << (p % 64) for p in parent if p//64 == j) for j in range(6)]
    replies = []
    for mapping in maps:
        image = {mapping[p] for p in tetra}
        if set(parent) < image:
            replies.append(next(iter(image-set(parent))))
    assert replies
    with destination.open('x') as output:
        output.write('Q5CUBE2 7 6 '+' '.join(map(str, words))+'\n')
        output.write(' '.join(map(str, words+[1]+tetra_words))+'\n')
        root_found = False
        for line in proof:
            row = list(map(int, line.split()))
            if row[:6] == tetra_words:
                assert row[6] == 0
                root_found = True
            output.write(line)
        assert root_found
print(json.dumps({'parent_three': parent, 'winning_fourth': min(replies),
                  'p_four': tetra, 'output': str(destination)}, indent=2))
