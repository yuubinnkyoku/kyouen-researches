#!/usr/bin/env python3
"""Reconstruct the complete class-1 blocker proof from verified S7 receipts."""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
from audit_published_candidates import images, safe

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent
S5 = int('00000000000000803082000000000000',16)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path)
    parser.add_argument('--determinant',action='store_true')
    args=parser.parse_args()
    if args.determinant:
        from audit_additional_geometry import safe as legal_geometry
    else:
        legal_geometry = safe
    verification = json.loads((HERE/'output/priority-certificates-verified.json').read_text())
    certs = {}
    for entry in verification['certificates']:
        root = int(entry['root'],16)
        suffix = 'win7' if entry['verdict'] == 'WIN7' else 'loss7'
        path = HERE/'output/priority-certificates'/f"{entry['root']}-{suffix}.cert.gz"
        assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == entry['certificate_sha256']
        if entry['verdict'] == 'WIN7':
            certs[root] = entry
    assert len(certs) == 13
    sweep = json.loads((EXP/'n11-central-19-cover-20261031/output/s6sweep/sweep_results.json').read_text())
    verified_win7 = set()
    for name in ('s6sweep/verified.json','focus2154_62certs/verified.json','frontier2140/verified.json'):
        data = json.loads((EXP/'n11-central-19-cover-20261031/output'/name).read_text())
        assert not data['fails']
        verified_win7.update(int(k,16) for k,v in data['verified'].items() if v['type'] == 'WIN7')
    old = {}
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        for row in csv.DictReader(f):
            old.setdefault(int(row['s6_hex'],16),row)
    assert len(old) == 498
    concrete = [i for i in range(121) if not S5 >> i & 1 and legal_geometry(S5 | 1<<i)]
    s6s = {min(images(S5 | (1<<i))) for i in concrete}
    assert len(s6s) == 40
    records = []
    for s6 in sorted(s6s):
        key = f'{s6:032x}'
        entry = sweep.get(key)
        if entry:
            assert entry['verdict'] == 'WIN_for_mover'
            witness = int(entry['win_child'],16)
            assert witness in verified_win7
            assert any(not s6>>i&1 and witness in images(s6 | (1<<i)) for i in range(121))
            records.append((key,'sweep',entry['win_child']))
            continue
        if s6 in old:
            witness = int(old[s6]['s7_hex'],16)
            assert witness in verified_win7
            assert any(not s6>>i&1 and witness in images(s6 | (1<<i)) for i in range(121))
            records.append((key,'prior_receipt',old[s6]['s7_hex']))
            continue
        witnesses = [root for root in certs if any(not (s6>>i&1) and root in images(s6 | (1<<i)) for i in range(121))]
        assert witnesses
        records.append((key,'new_verified_certificate',f'{min(witnesses):032x}'))
    from collections import Counter
    counts=Counter(r[1] for r in records)
    assert counts == {'sweep':2,'prior_receipt':25,'new_verified_certificate':13}
    blockers=[]
    for move4 in (5,115):
        s4 = sum(1<<i for i in (59,60,61,move4))
        assert legal_geometry(s4)
        moves = [i for i in range(121) if not s4>>i&1 and legal_geometry(s4 | (1<<i)) and min(images(s4 | (1<<i))) == S5]
        assert moves
        blockers.append({'s4_move':move4,'s5_move':moves[0]})
    if args.csv:
        with args.csv.open('w',newline='') as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(('s6_hex','source','win7_hex'));w.writerows(records)
    print(json.dumps({'s5_hex':f'{S5:032x}','legal_s5_moves':len(concrete),'distinct_s6_orbits':len(s6s),
                      's6_source_counts':dict(sorted(counts.items())),'blocker_moves':blockers,
                      'result':'FIRST_WIN for this S5 and S4 blockers 5,115, conditional on published sweep and prior verifier receipts',
                      'scope':'class 1 only; remaining blockers, S2 and empty board not decided'},indent=2))


if __name__ == '__main__':
    main()
