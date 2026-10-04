#!/usr/bin/env python3
"""Extract the 255 unchanged finite exclusions needed by the tail bound101.

No SAT solver or DRAT checker is run here. Each selected CNF is regenerated
and hash-checked against the previously independently verified 510-case
manifest and its full integration recheck receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Certificate validation requires assertions; do not use -O.')

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parents[1]
OLD=ROOT/'research/experiments/fixed-width-frontier-20261005'
SAT_GENERATOR=OLD/'scripts'/'q58_sat.py'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pysat-path',default='/workspace/research-tools/python-sat')
    ap.add_argument('--output',type=Path,default=HERE/'output/reduced-manifest.json')
    args=ap.parse_args()
    sys.path.insert(0,args.pysat_path)
    sys.path.insert(0,str(OLD/'scripts'))
    import pysat
    from q58_sat import encode
    source=OLD/'output/q58_finite_certificate_manifest.json'
    recheck=OLD/'output/q58_integration_recheck.json'
    original=json.loads(source.read_text())
    receipt=json.loads(recheck.read_text())
    assert original['all_finite_cases_verified'] is True
    assert original['finite_scope']=={'m':[16,185],'target_rows':[0,1,2]}
    assert receipt['source_manifest_sha256']==sha(source)
    assert receipt['status']=='VERIFIED'
    assert receipt['records']==receipt['cnf_hash_matches']==receipt['independent_drat_verified']==510
    assert pysat.__version__==original['python_sat_version']
    assert original['source_sha256'][str(SAT_GENERATOR.relative_to(OLD))]==sha(SAT_GENERATOR)
    keys=[(r['m'],r['target_row']) for r in original['records']]
    assert len(keys)==510 and len(set(keys))==510
    assert set(keys)=={(m,t) for m in range(16,186) for t in range(3)}
    selected=[r for r in original['records'] if 16<=r['m']<=100]
    assert len(selected)==255
    for record in selected:
        m,target=record['m'],record['target_row']
        assert record['status']=='UNSAT' and record['drat_status']=='VERIFIED'
        clauses,nv,curves=encode(m,target)
        cnf=f'p cnf {nv} {len(clauses)}\n'+''.join(
            ' '.join(map(str,c))+' 0\n' for c in clauses)
        assert hashlib.sha256(cnf.encode()).hexdigest()==record['cnf_sha256']
        assert record['variables']==nv and record['clauses']==len(clauses) and record['circles']==len(curves)
    out=dict(schema=1,statement='M_{5,8}=16',finite_scope={'m':[16,100],'target_rows':[0,1,2]},
             universal_tail=dict(first_length=101,proof='research/experiments/q58-chord-tail-20261005/proof.md',
                                 chord_energy=47,external_chord_pair_budget=282,
                                 maximum_blocker_circles=94,maximum_unavailable_points=100),
             source_manifest='research/experiments/fixed-width-frontier-20261005/output/q58_finite_certificate_manifest.json',
             source_manifest_sha256=sha(source),
             source_full_recheck='research/experiments/fixed-width-frontier-20261005/output/q58_integration_recheck.json',
             source_full_recheck_sha256=sha(recheck),
             evidence='Extracted previously independently DRAT-verified records; no fresh SAT or DRAT execution',
             regenerated_cnf_hash_matches=255,python_sat_version=pysat.__version__,
             records=selected,all_selected_cases_previously_verified=True,
             source_generator_sha256=sha(SAT_GENERATOR))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'selected_cases':len(selected),'cnf_hash_matches':255,'universal_tail':101}))


if __name__=='__main__':
    main()
