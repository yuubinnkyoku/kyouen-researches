#!/usr/bin/env python3
"""Recount the remaining work after four more verified WIN7 strategies."""
import csv
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from audit_published_candidates import images

HERE=Path(__file__).resolve().parents[1]
TARGET='00000000000000003800004008000000'
LOSS6=int('00000000000000809202000400000000',16)


def covers(root):
    return {min(images(root^(1<<i))) for i in range(121) if root>>i&1}


def main():
    prior=[]
    for name in ('priority-certificates-verified.json','class2-certificates-verified.json'):
        prior.extend(int(r['root'],16) for r in json.loads((HERE/'output'/name).read_text())['certificates'] if r['verdict']=='WIN7')
    records=json.loads((HERE/'output/class2-next-certificates-verified.json').read_text())['certificates']
    assert len(records)==4
    for row in records:
        path=HERE/'output/class2-next-certificates'/f"{row['root']}-win7.cert.gz"
        assert row['verdict']=='WIN7' and hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest()==row['certificate_sha256']
    old=set().union(*(covers(r) for r in prior))
    new=set().union(*(covers(int(r['root'],16)) for r in records)) - old
    with gzip.open(HERE/'output/win7-reuse-hits.csv.gz','rt',newline='') as f:
        baseline={int(row['s6_hex'],16) for row in csv.DictReader(f)}
    manifest=set()
    for path in sorted((HERE.parent/'n11-s2-5960-milestone5-20261112/output').glob('ms5_s6_manifest_part*.csv')):
        with path.open(newline='') as f:
            manifest.update(int(row['hex'],16) for row in csv.DictReader(f))
    solved_before=(baseline|old)&manifest
    assert len(solved_before)==565
    with gzip.open(HERE/'output/s5-s6-remaining-incidences.csv.gz','rt',newline='') as f:
        incidences=list(csv.DictReader(f))
    rejected={r['s5_hex'] for r in incidences if int(r['s6_hex'],16)==LOSS6}
    remaining=defaultdict(list)
    for row in incidences:
        if row['s5_hex'] not in rejected and int(row['s6_hex'],16) not in old|new:
            remaining[row['s5_hex']].append(row)
    unique={r['s6_hex']:int(r['s6_s7_edge_cost']) for rs in remaining.values() for r in rs}
    newly_in_worklist=new & {int(r['s6_hex'],16) for r in incidences}
    assert (len(newly_in_worklist),len(remaining),len(unique),len(remaining[TARGET]))==(9,182,7288,27)
    print(json.dumps({'new_win7_certificates':len(records),'new_worklist_s6_wins':len(newly_in_worklist),
                      'all_reused_s6_wins':len(solved_before | (new & manifest)),'remaining_s5_orbits':len(remaining),
                      'remaining_s6_orbits':len(unique),'remaining_s7_edge_cost':sum(unique.values()),
                      'class2_candidate':TARGET,'class2_candidate_remaining_s6':len(remaining[TARGET]),
                      'condition':'prior sweep and verifier receipts plus newly verified terminal strategies',
                      'scope':'class 2 and class 4 blockers, S2 and empty board remain unresolved'},indent=2))


if __name__=='__main__':
    main()
