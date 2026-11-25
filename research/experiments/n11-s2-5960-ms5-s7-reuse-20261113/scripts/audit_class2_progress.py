#!/usr/bin/env python3
"""Recount S6 wins and a class-2 S5 candidate from verified certificates."""
import csv
import gzip
import hashlib
import json
from pathlib import Path
from audit_published_candidates import images

HERE = Path(__file__).resolve().parents[1]
MS5 = HERE.parent/'n11-s2-5960-milestone5-20261112/output'
S5 = '00000000000000809202000000000000'


def parents(root):
    return {min(images(root ^ (1<<i))) for i in range(121) if root >> i & 1}


def main():
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        old = {int(r['s6_hex'],16) for r in csv.DictReader(f)}
    class1 = json.loads((HERE/'output/priority-certificates-verified.json').read_text())['certificates']
    for item in class1:
        if item['verdict']=='WIN7':
            old.update(parents(int(item['root'],16)))
    manifest = {}
    for path in sorted(MS5.glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            for row in csv.DictReader(f):
                manifest[int(row['hex'],16)] = int(row['cost'])
    old &= manifest.keys()
    assert len(old)==523
    records = json.loads((HERE/'output/class2-certificates-verified.json').read_text())['certificates']
    assert len(records)==14
    newly = set()
    for item in records:
        assert item['verdict']=='WIN7'
        path=HERE/'output/class2-certificates'/f"{item['root']}-win7.cert.gz"
        assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest()==item['certificate_sha256']
        newly.update(parents(int(item['root'],16)))
    newly = (newly & manifest.keys()) - old
    with gzip.open(HERE/'output/s5-s6-remaining-incidences.csv.gz','rt',newline='') as f:
        target={int(r['s6_hex'],16) for r in csv.DictReader(f) if r['s5_hex']==S5}
    assert len(target)==18
    unresolved=sorted(target-old-newly)
    assert (len(newly),len(unresolved))==(42,1)
    all_solved = old | newly
    print(json.dumps({'s5_hex':S5,'previously_unresolved_s6':len(target),
                      'newly_verified_win7':len(records),'new_s6_wins_in_worklist':len(newly),
                      'solved_s6_in_target':len(target & all_solved),
                      'remaining_s6_in_target':[f'{x:032x}' for x in unresolved],
                      'all_reused_s6_wins':len(all_solved),'remaining_s6_orbits':len(manifest)-len(all_solved),
                      'remaining_s7_edge_cost':sum(cost for key,cost in manifest.items() if key not in all_solved),
                      'condition':'new certificates independently verified; previous receipt and sweep trust boundaries still apply',
                      'scope':'class-2 candidate remains unresolved; no S2 or empty-board verdict'},indent=2))


if __name__ == '__main__':
    main()
