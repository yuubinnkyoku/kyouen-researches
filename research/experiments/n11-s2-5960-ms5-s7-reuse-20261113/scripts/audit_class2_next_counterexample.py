#!/usr/bin/env python3
"""Check the class-2 S5 candidate has a fully certified SECOND_WIN reply."""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
from audit_published_candidates import images, safe

HERE=Path(__file__).resolve().parents[1]
S5=int('00000000000000003800004008000000',16)
S6=int('00000000000000003800004008000008',16)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--determinant',action='store_true')
    args=parser.parse_args()
    if args.determinant:
        from audit_additional_geometry import safe as legal_geometry
    else:
        legal_geometry=safe
    records=json.loads((HERE/'output/class2-next-loss-verified.json').read_text())['certificates']
    assert len(records)==72
    proven=set()
    for entry in records:
        assert entry['verdict']=='LOSS7'
        path=HERE/'output/class2-next-loss-certificates'/f"{entry['root']}-loss7.cert.gz"
        assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest()==entry['certificate_sha256']
        root=int(entry['root'],16)
        assert root==min(images(root))
        proven.add(root)
    assert len(proven)==72 and legal_geometry(S6)
    moves=[i for i in range(121) if not S6>>i&1 and legal_geometry(S6 | (1<<i))]
    children={min(images(S6 | (1<<i))) for i in moves}
    assert len(children)==72 and children==proven
    with gzip.open(HERE/'output/s5-s6-remaining-incidences.csv.gz','rt',newline='') as f:
        incidences=list(csv.DictReader(f))
    parent_hexes=sorted({r['s5_hex'] for r in incidences if int(r['s6_hex'],16)==S6})
    assert len(parent_hexes)==2
    parent_responses=[]
    for parent_hex in parent_hexes:
        parent=int(parent_hex,16)
        responses=[i for i in range(121) if not parent>>i&1 and legal_geometry(parent | (1<<i)) and min(images(parent | (1<<i)))==S6]
        assert responses
        parent_responses.append({'s5_hex':parent_hex,'moves':responses})
    roots=[]
    for name in ('priority-certificates-verified.json','class2-certificates-verified.json','class2-next-certificates-verified.json','class2-next2-certificates-verified.json','class2-next3-certificates-verified.json','class2-next4-certificates-verified.json'):
        roots.extend(int(r['root'],16) for r in json.loads((HERE/'output'/name).read_text())['certificates'] if r['verdict']=='WIN7')
    win6={min(images(root^(1<<i))) for root in roots for i in range(121) if root>>i&1}
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        previous_win6={int(row['s6_hex'],16) for row in csv.DictReader(f)}
    assert S6 not in win6 and S6 not in previous_win6
    old_loss=int('00000000000000809202000400000000',16)
    assert old_loss not in win6 and old_loss not in previous_win6
    old_rejected={r['s5_hex'] for r in incidences if int(r['s6_hex'],16)==old_loss}
    rejected=set(parent_hexes)|old_rejected
    pending=[r for r in incidences if r['s5_hex'] not in rejected and int(r['s6_hex'],16) not in win6]
    remaining_s5={r['s5_hex'] for r in pending}
    unique_s6={r['s6_hex']:int(r['s6_s7_edge_cost']) for r in pending}
    assert len(remaining_s5)==180
    with gzip.open(HERE/'output/s5-remaining-after-reuse.csv.gz','rt',newline='') as f:
        classes={r['s5_hex']:int(r['classes']) for r in csv.DictReader(f)}
    by_s5={key:[r for r in pending if r['s5_hex']==key] for key in remaining_s5}
    best={}
    for bit in (2,4):
        ranked=sorted((len(rows),sum(int(r['s6_s7_edge_cost']) for r in rows),key)
                      for key,rows in by_s5.items() if classes[key]&bit)
        count,cost,key=ranked[0]
        best[str(bit)]={'s5_hex':key,'remaining_s6_orbits':count,'remaining_s7_edge_cost':cost}
    print(json.dumps({'s5_hex':f'{S5:032x}','s6_hex':f'{S6:032x}',
                      's5_second_win_responses':parent_responses,'s6_legal_moves':len(moves),
                      's6_distinct_s7_orbits':len(children),'verified_original_first_loss_s7':len(proven),
                      'result':'S6 first-player LOSS; two S5 positions second-player WIN',
                      'remaining_s5_orbits':len(remaining_s5),'remaining_required_s6_orbits':len(unique_s6),
                      'remaining_required_s7_edge_cost':sum(unique_s6.values()),
                      'best_remaining_by_class':best,
                      'scope':'terminal certificates reverified independently; no conclusion for the class-2 blocker or root'},indent=2))


if __name__=='__main__':
    main()
