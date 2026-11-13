#!/usr/bin/env python3
"""Recount worklist closure after locally verified WIN7 certificates."""
import csv
import gzip
import json
from collections import Counter,defaultdict
from pathlib import Path
from audit_published_candidates import images

HERE = Path(__file__).resolve().parents[1]
MS5 = HERE.parent/'n11-s2-5960-milestone5-20261112/output'


def main():
    verified = json.loads((HERE/'output/priority-certificates-verified.json').read_text())
    roots = [int(e['root'],16) for e in verified['certificates'] if e['verdict'] == 'WIN7']
    assert len(roots) == 13
    manifest = {}
    for path in sorted(MS5.glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            for row in csv.DictReader(f):
                key = int(row['hex'],16)
                assert key not in manifest
                manifest[key] = int(row['cost'])
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        old = {int(row['s6_hex'],16) for row in csv.DictReader(f)}
    new = set()
    for root in roots:
        new.update(min(images(root ^ (1<<i))) for i in range(121) if root >> i & 1)
    new = (new & manifest.keys()) - old
    assert (len(manifest),len(old),len(new)) == (7867,498,25)
    with gzip.open(HERE/'output/s5-s6-remaining-incidences.csv.gz','rt',newline='') as f:
        rows = list(csv.DictReader(f))
    s5_original = {row['s5_hex'] for row in rows}
    missing = Counter(row['s5_hex'] for row in rows if int(row['s6_hex'],16) not in new)
    closed = sorted(s5_original - set(missing))
    assert closed == ['00000000000000803082000000000000']
    solved = old | new
    assert sum(manifest.values()) == 615497
    print(json.dumps({'new_verified_win7':len(roots),'new_s6_wins':len(new),
                      'all_reused_s6_wins':len(solved),'remaining_s6_orbits':len(manifest)-len(solved),
                      'remaining_s7_edge_cost':sum(cost for key,cost in manifest.items() if key not in solved),
                      'new_first_win_s5':closed,'remaining_s5_orbits':len(missing),
                      's5_scope':'186 unresolved S5 orbits from prior worklist; existing 10 SECOND_WIN excluded',
                      'condition':'published WIN7 receipts and sweep records plus locally verified certificates'},indent=2))


if __name__ == '__main__':
    main()
