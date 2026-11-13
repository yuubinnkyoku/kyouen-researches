#!/usr/bin/env python3
"""Match published WIN7 audit receipts to the milestone-5 S6 worklist.

WIN7 denotes original-first-player win. Certificate bodies are not included;
this audit checks receipt records and geometry, not the strategies themselves.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path
from audit_published_candidates import images, safe

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent
SOURCE = EXP/'n11-central-19-cover-20261031/output'
FILES = ('s6sweep/verified.json','focus2154_62certs/verified.json','frontier2140/verified.json')
MANIFEST = EXP/'n11-s2-5960-milestone5-20261112/output'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path)
    args = parser.parse_args()
    certificates = defaultdict(list)
    loss = set()
    for path in FILES:
        data = json.loads((SOURCE/path).read_text())
        assert not data['fails']
        for key,entry in data['verified'].items():
            child = int(key,16)
            assert child.bit_count() == 7 and child == min(images(child))
            if entry['type'] == 'WIN7':
                digest = entry['sha256']
                assert len(digest) == 64 and all(c in '0123456789abcdef' for c in digest)
                certificates[child].append((path,digest))
            elif entry['type'] == 'LOSS7':
                loss.add(child)
            else:
                raise ValueError('unknown receipt type')
    assert not (set(certificates) & loss)
    parents = {}
    for path in sorted(MANIFEST.glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            for row in csv.DictReader(f):
                key = int(row['hex'],16)
                assert key not in parents and key.bit_count() == 6
                parents[key] = row
    assert len(parents) == 7867
    hits = {}
    for child in certificates:
        for position in range(121):
            if not child >> position & 1:
                continue
            parent = min(images(child ^ (1 << position)))
            if parent not in parents:
                continue
            assert safe(child)
            moves = [i for i in range(121) if not parent >> i & 1 and child in images(parent | (1 << i))]
            assert moves
            hits[parent,child] = (min(moves),sorted(certificates[child]))
    winners = {parent for parent,_ in hits}
    assert (len(certificates),len(hits),len(winners)) == (4052,534,498)
    result = {'worklist_parents':len(parents),'verified_win7_keys':len(certificates),
              'matched_parent_child_pairs':len(hits),'parents_with_verified_win7_child':len(winners),
              'remaining_parents_after_reuse':len(parents)-len(winners),
              'removed_worklist_legal_child_cost':sum(int(parents[p]['cost']) for p in winners),
              'remaining_worklist_legal_child_cost':sum(int(r['cost']) for p,r in parents.items() if p not in winners),
              'worklist_classes':dict(sorted(Counter(parents[p]['classes'] for p in winners).items())),
              'certificate_source_sha256':{path:hashlib.sha256((SOURCE/path).read_bytes()).hexdigest() for path in FILES},
              'scope':'published WIN7 verifier receipts and S6 worklist; strategy bodies not rechecked; no root verdict'}
    if args.csv:
        with args.csv.open('w',newline='') as f:
            w = csv.writer(f,lineterminator='\n')
            w.writerow(('s6_hex','s7_hex','move_in_s6_coordinates','cost','classes','receipt_path','certificate_sha256'))
            for (parent,child),(move,receipts) in sorted(hits.items()):
                receipt,digest = receipts[0]
                w.writerow((f'{parent:032x}',f'{child:032x}',move,parents[parent]['cost'],parents[parent]['classes'],receipt,digest))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
