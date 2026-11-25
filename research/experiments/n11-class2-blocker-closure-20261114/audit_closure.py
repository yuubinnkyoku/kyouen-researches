#!/usr/bin/env python3
"""Check class-2 S4 closure against published WIN7 verifier receipts.

Checks geometry, coverage, terminal-certificate identity and receipt results;
individual strategies are not replayed here. Prior receipts remain a trust
boundary. Use --determinant to cross-check legal-move generation independently.
"""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
EXP=HERE.parent
REUSE=EXP/'n11-s2-5960-ms5-s7-reuse-20261113'
OUT=REUSE/'output'
sys.path.insert(0,str(REUSE/'scripts'))
from audit_published_candidates import images, safe

TARGET=int('00000000000000003802000008000000',16)
LANES=('cost60','cost61','cost61b','cost64','cost65','cost68')
BASE=('class2-batch1-certificates-verified.json','class2-batch1b-certificates-verified.json')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--determinant',action='store_true')
    parser.add_argument('--csv',type=Path)
    args=parser.parse_args()
    if args.determinant:
        from audit_additional_geometry import safe as legal_geometry
    else:
        legal_geometry=safe
    assert legal_geometry(TARGET) and TARGET == min(images(TARGET))
    moves=[i for i in range(121) if not TARGET>>i&1 and legal_geometry(TARGET|(1<<i))]
    children={min(images(TARGET|(1<<i))) for i in moves}
    assert len(moves)==82 and len(children)==41
    sweep=json.loads((EXP/'n11-central-19-cover-20261031/output/s6sweep/sweep_results.json').read_text())
    receipts={}
    for path in BASE:
        for e in json.loads((OUT/path).read_text())['certificates']:
            if e['verdict']=='WIN7':receipts[int(e['root'],16)]=(path,e)
    for lane in LANES:
        path=f'class2-lane-{lane}-win7-certificates-20261114.json'
        for e in json.loads((OUT/path).read_text())['certificates']:
            assert e['verdict']=='WIN7'
            receipts.setdefault(int(e['root'],16),(path,e))
    prior={}
    with gzip.open(OUT/'win7-reuse-hits.csv.gz','rt',newline='') as f:
        for r in csv.DictReader(f):prior.setdefault(int(r['s6_hex'],16),r)
    coverage={}
    for root,(source,entry) in receipts.items():
        assert root.bit_count()==7
        for i in range(121):
            if root>>i&1:
                parent=min(images(root^(1<<i)))
                if parent in children:
                    coverage.setdefault(parent,(root,source,entry))
    provenance=[]
    certificate_checks={}
    for s6 in sorted(children):
        key=f'{s6:032x}'
        if key in sweep:
            item=sweep[key]
            assert item['verdict']=='WIN_for_mover'
            root=int(item['win_child'],16)
            source='s6sweep/sweep_results.json'
            # Receipt for the original sweep's chosen root exists in one of
            # the three independently audited receipt sets.
            sources=('s6sweep/verified.json','focus2154_62certs/verified.json','frontier2140/verified.json')
            found=False
            for f in sources:
                data=json.loads((EXP/'n11-central-19-cover-20261031/output'/f).read_text())
                e=data['verified'].get(f'{root:032x}')
                if e and e['type']=='WIN7':found=True;break
            assert found
        elif s6 in prior:
            row=prior[s6];root=int(row['s7_hex'],16);source='win7-reuse-hits.csv.gz'
            receipt_path=EXP/'n11-central-19-cover-20261031/output'/row['receipt_path']
            prior_receipt=json.loads(receipt_path.read_text())['verified'][f'{root:032x}']
            assert prior_receipt['type']=='WIN7' and prior_receipt['sha256']==row['certificate_sha256']
        else:
            assert s6 in coverage, f'missing WIN7 witness for {key}'
            root,source,entry=coverage[s6]
            if source in BASE:
                folder='class2-batch1-certificates' if source==BASE[0] else 'class2-batch1b-certificates'
                path=OUT/folder/(f'{root:032x}'+'-win7.cert.gz')
                raw=gzip.decompress(path.read_bytes())
                assert hashlib.sha256(raw).hexdigest()==entry['certificate_sha256']
            else:
                c=entry.get('cert_file',entry.get('certificate'))
                md5=None
                if isinstance(c,dict):
                    md5=c.get('md5'); c=c['certificate_path']
                else:md5=entry.get('md5')
                path=REUSE/c
                raw=path.read_bytes()
                if md5:assert hashlib.md5(raw).hexdigest()==md5
                verification=entry.get('verification')
                if isinstance(verification,dict):assert verification['union_diff']=='0/0'
                elif isinstance(verification,str):assert verification=='PASS'
                else:assert entry.get('all_subroots_pass') and entry.get('union_missing')==entry.get('union_extra')==0
            assert raw.startswith(('n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS\nroot '+f'{root:032x}'+'\n').encode())
            certificate_checks[f'{root:032x}']=hashlib.sha256(raw).hexdigest()
        matching=[i for i in range(121) if not s6>>i&1 and root in images(s6|(1<<i))]
        assert matching, key
        assert legal_geometry(s6|(1<<matching[0]))
        provenance.append((key,f'{root:032x}',matching[0],source))
    blockers=[]
    for stone in (27,93):
        s4=sum(1<<i for i in (59,60,61,stone))
        assert legal_geometry(s4)
        winning=[i for i in range(121) if not s4>>i&1 and legal_geometry(s4|(1<<i)) and min(images(s4|(1<<i)))==TARGET]
        assert winning
        blockers.append({'s4_move':stone,'s5_move':winning[0]})
    if args.csv:
        with args.csv.open('w',newline='') as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(('s6_hex','win7_hex','move_in_s6_coordinates','receipt_source'));w.writerows(provenance)
    result={'s5_hex':f'{TARGET:032x}','legal_s5_moves':len(moves),'distinct_s6_orbits':len(children),
            's6_source_counts':dict(sorted(Counter(r[3] for r in provenance).items())),
            'local_certificate_roots_hashed':len(certificate_checks),'blocker_moves':blockers,
            'result':'FIRST_WIN for this S5 and S4 blockers 27,93, conditional on cited verifier receipts',
            'scope':'class 2 only; class 4, S2 and empty board remain unresolved; certificate strategies not replayed'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
