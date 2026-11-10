"""Interpret the frozen parent independently and bind sixty geometric hitting-tree units."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PARENT_FOLDER=HERE.parent/'parabola-p2539-five-pair-split-20261111'
OBSTRUCTIONS=HERE.parent/'parabola-p2539-five-obstructions-20261111'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
SEED_SHA='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


parent=load('p2539_pruned_parent_schema',PARENT_FOLDER/'schema.py')
hit=load('p2539_pruned_hitting_verifier',OBSTRUCTIONS/'verify.py')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def audit(raw,seed):
    seed_raw=(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes()
    assert sha(seed_raw)==SEED_SHA and list(map(int,seed_raw.split()))==[2539,1258]+seed
    cert_raw=(OBSTRUCTIONS/'output/certificate.json').read_bytes();cert=json.loads(cert_raw,object_pairs_hook=hit.no_duplicates)
    previous=json.loads((OBSTRUCTIONS/'audit-output/summary.json').read_bytes())
    assert sha(cert_raw)==previous['certificate_sha256'] and sha((OBSTRUCTIONS/'verify.py').read_bytes())==previous['verifier_source_sha256']
    assert (cert['p'],cert['fixed'],cert['max_deletions'],cert['seed_sha256'])==(2539,[0,6,2533],5,SEED_SHA)
    excluded=cert['excluded'];assert excluded==previous['excluded'] and len(excluded)==60 and excluded==sorted(set(excluded))
    nv,clauses=parent.prefix.parse(raw);assert nv==51570 and len(clauses)==144606
    body=(f'p cnf 51570 144546\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses[:-60])).encode('ascii')
    assert sha(body)==PARENT_SHA
    geometry,report=parent.audit(body,seed,'retained');base=report['point_base'];assert base==36512
    assert clauses[-60:]==[[-(base+u)] for u in excluded]
    # Replay just the negative trees needed for these sixty new units.
    eraw=gzip.decompress((HERE.parent/'parabola-p2539-pair-pilot-20261110/output/edges.txt.gz').read_bytes())
    assert sha(eraw)==cert['edge_input_sha256']==previous['edge_input_sha256']
    fixed={0,6,2533};seed_set=set(seed);families={u:[] for u in excluded}
    for q in sorted(tuple(map(int,l.split())) for l in eraw.splitlines()[1:]):
        outside=set(q)-seed_set
        if len(outside)==1 and next(iter(outside)) in families:families[next(iter(outside))].append(q)
    entries={r['point']:r for r in cert['entries']};nodes=[];obstruction_geometry=[]
    for u,qs in families.items():
        entry=entries[u];assert entry['status']=='EXCLUDED' and entry['obstructions']==len(qs)
        nodes.append(hit.check_tree([set(q)-fixed-{u} for q in qs],5,entry['refutation']));obstruction_geometry.extend(qs)
    report.update(pruned_variables=nv,pruned_clauses=len(clauses),added_units=60,excluded=excluded,
        parent_input_sha256=sha(body),input_sha256=sha(raw),obstruction_certificate_sha256=sha(cert_raw),
        parent_schema_source_sha256=sha((PARENT_FOLDER/'schema.py').read_bytes()),hitting_verifier_source_sha256=sha((OBSTRUCTIONS/'verify.py').read_bytes()),
        extra_obstruction_quadruples=len(obstruction_geometry),scope='Parent geometry plus independently replayed hitting-tree units. Geometric checks of both edge lists are still required; units are not claimed parent-only RUP consequences.')
    return geometry,obstruction_geometry,report
