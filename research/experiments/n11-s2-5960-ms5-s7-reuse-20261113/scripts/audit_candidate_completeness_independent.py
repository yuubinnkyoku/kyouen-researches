#!/usr/bin/env python3
"""Cross-check completeness using indexed four-subsets and determinant geometry."""
from collections import defaultdict
import csv
import gzip
from itertools import combinations
import json
from pathlib import Path
from audit_published_candidates import images
from audit_additional_geometry import safe

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent


def main():
    source = json.loads((EXP/'n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json').read_text())
    bases = [int(x,16) for x in source['first_win_s5']+source['second_win_s5']]
    oracle = {o for b in bases for o in images(b)}
    index = defaultdict(set)
    for o in oracle:
        for i in range(121):
            if o >> i & 1:
                index[o ^ (1 << i)].add(1 << i)
    parents = []
    for path in sorted((EXP/'n11-s2-5960-milestone5-20261112/output').glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            parents.extend(int(row['hex'],16) for row in csv.DictReader(f))
    computed = set()
    for parent in parents:
        positions = [i for i in range(121) if parent >> i & 1]
        moves = set()
        for four in combinations(positions,4):
            key = sum(1 << i for i in four)
            moves.update(bit for bit in index[key] if not bit & parent)
        for bit in moves:
            child = parent | bit
            if safe(child):
                computed.add((parent,min(images(child))))
    recorded = set()
    for path in sorted((HERE/'output').glob('ms5_s7_reuse_candidates_part*.csv')):
        with path.open(newline='') as f:
            for row in csv.reader(f):
                if row[0] != 's7_hex':
                    recorded.add((int(row[1],16),int(row[0],16)))
    with gzip.open(HERE/'output/additional-candidates.csv.gz','rt',newline='') as f:
        for row in csv.DictReader(f):
            recorded.add((int(row['s6_hex'],16),int(row['s7_hex'],16)))
    assert len(computed) == len(recorded) == 15072
    assert computed == recorded
    print(f'{len(computed)} parent-child pairs: independent subset-index and determinant audit passed')


if __name__ == '__main__':
    main()
