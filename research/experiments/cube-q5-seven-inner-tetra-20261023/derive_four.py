#!/usr/bin/env python3
"""Wrap the inner tetrahedron + centre P proof with its N four-stone parent."""
from pathlib import Path
import gzip
import sys

root = Path(__file__).resolve().parent
destination = Path(sys.argv[1])
assert not destination.exists()
points = [114, 130, 214, 226]
words = [sum(1 << (p % 64) for p in points if p//64 == j) for j in range(6)]
with gzip.open(root/'five-p.cert.gz', 'rt') as proof, destination.open('x') as output:
    header = proof.readline().split()
    assert header[:3] == ['Q5CUBE2', '7', '6']
    child = list(map(int, header[3:]))
    output.write('Q5CUBE2 7 6 '+' '.join(map(str, words))+'\n')
    output.write(' '.join(map(str, words+[1]+child))+'\n')
    for line in proof:
        output.write(line)
