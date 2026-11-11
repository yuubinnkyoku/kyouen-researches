"""Frozen retained parent augmented with the independently geometric116 point exclusions."""
import gzip
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz'
EVIDENCE=HERE.parent/'parabola-p2539-pair-obstructions-20261111'
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
SEED_SHA='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def build():
    parent=gzip.decompress(PARENT.read_bytes());assert sha(parent)==PARENT_SHA
    cert_raw=(EVIDENCE/'output/certificate.json').read_bytes();cert=json.loads(cert_raw)
    audit=json.loads((EVIDENCE/'audit-output/summary.json').read_bytes());gate=json.loads((EVIDENCE/'gate-output/receipt.json').read_bytes())
    assert sha(cert_raw)==audit['certificate_sha256'] and cert['excluded']==audit['excluded'] and len(cert['excluded'])==116
    assert audit['seed_sha256']==SEED_SHA and gate['verified_parent_only_derivation'] and gate['parent_input_sha256']==PARENT_SHA
    assert len(gate['empty_pair_points'])==26 and not set(cert['excluded'])&set(gate['empty_pair_points'])
    lines=parent.decode('ascii').splitlines();assert lines[0]=='p cnf 51570 144546'
    units=[-(36512+u) for u in cert['excluded']]
    body=('p cnf 51570 144662\n'+'\n'.join(lines[1:])+'\n'+''.join(f'{v} 0\n' for v in units)).encode('ascii')
    return body,dict(p=2539,variables=51570,clauses=144662,parent_input_sha256=PARENT_SHA,base_input_sha256=sha(body),seed_sha256=SEED_SHA,
        excluded=cert['excluded'],gate_points=gate['empty_pair_points'],obstruction_certificate_sha256=sha(cert_raw),
        encoding_source_sha256=sha(Path(__file__).read_bytes()),scope='116 units use geometric/hitting certificates; native RUP is separately available for the original60. Gate is a cover, not disjoint cases.')
