#!/usr/bin/env python3
"""Check each reused witness with determinant geometry and receipt lookup."""
import csv
import gzip
import json
from pathlib import Path
from audit_additional_geometry import safe
from audit_published_candidates import images

HERE = Path(__file__).resolve().parents[1]
RECEIPTS = HERE.parent/'n11-central-19-cover-20261031/output'


def main():
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 534
    sources = {}
    for row in rows:
        parent,child = int(row['s6_hex'],16),int(row['s7_hex'],16)
        move = int(row['move_in_s6_coordinates'])
        assert parent.bit_count() == 6 and 0 <= move < 121 and not parent >> move & 1
        expanded = parent | (1 << move)
        assert safe(expanded) and child == min(images(expanded))
        path = row['receipt_path']
        if path not in sources:
            sources[path] = json.loads((RECEIPTS/path).read_text())['verified']
        receipt = sources[path][row['s7_hex']]
        assert receipt['type'] == 'WIN7' and receipt['sha256'] == row['certificate_sha256']
    assert len({r['s6_hex'] for r in rows}) == 498
    print('534 legal parent-child pairs and 498 parents agree with WIN7 receipt records')


if __name__ == '__main__':
    main()
