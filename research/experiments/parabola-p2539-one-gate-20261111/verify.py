"""Interpret the entire exactly-one-gate input and independently check its saved refutation."""
import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'parabola-p2539-five-pair-split-20261111'
spec=importlib.util.spec_from_file_location('one_gate_parent_schema',OLD/'schema.py');schema=importlib.util.module_from_spec(spec);spec.loader.exec_module(schema)
TRIM=HERE.parent/'parabola-drat-trim-20261109'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')


def inspect(raw):
    nv,cs=schema.prefix.parse(raw);assert nv==51570 and len(cs)==144921
    original=('p cnf 51570 144546\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs[:144546])).encode('ascii');assert sha(original)==PARENT_SHA
    seed_raw=(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes()
    prior=HERE.parent/'parabola-p2539-gate-cover-20261111';qr=(prior/'qualification.json').read_bytes();q=json.loads(qr)
    assert sha(seed_raw)==q['seed_sha256'] and sha((prior/'README.md').read_bytes())==q['argument_sha256'] and sha((prior/'qualify.py').read_bytes())==q['source_sha256']
    assert q['max_removed']==5 and q['improvement_size_at_least']==1259 and q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    seed=set(map(int,seed_raw.split()[2:]));geometry,report=schema.audit(original,sorted(seed),'retained');assert report['point_base']==36512
    excluded=q['excluded_points'];gate=q['must_add_one_of'];assert len(excluded)==221 and len(gate)==18 and set(gate).isdisjoint(seed|set(excluded))
    extra=cs[144546:];assert extra[:221]==[[-36512-u] for u in excluded]
    assert extra[221]==[36512+u for u in gate]
    expected=[[-36512-u,-36512-v] for u,v in itertools.combinations(gate,2)];assert extra[222:]==expected
    report.update(input_sha256=sha(raw),prior_qualification_sha256=sha(qr),excluded_points=excluded,gate=gate,gate_cardinality='exactly1',clauses=len(cs),
        scope='Entire retained-parent schema plus221 previously justified exclusions, positive18-point gate, and153 binary clauses forbidding every two gate points.')
    return cs,geometry,report


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    raw=gzip.decompress((a.saved/'input.cnf.gz').read_bytes());cs,geometry,report=inspect(raw);save(a.output/'schema.json',report)
    result=json.loads((a.saved/'result.json').read_bytes());launch=json.loads((a.saved/'launch.json').read_bytes())
    assert launch['returncode']==0 and not launch['timed_out'] and result['input_sha256']==sha(raw) and result['prior_qualification_sha256']==report['prior_qualification_sha256']
    assert result['source_sha256']==sha((HERE/'produce.py').read_bytes()) and result['status']=='SOLVER_UNSAT' and result['proof_complete']
    proof=gzip.decompress((a.saved/'proof.drat.gz').read_bytes());assert sha(proof)==result['proof_sha256']
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    gr=(f'2539 {len(geometry)}\n'+''.join(' '.join(map(str,q))+'\n' for q in geometry)).encode('ascii')
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-one-gate-audit-') as temporary:
        td=Path(temporary);ge=td/'geometry.exe';exe=td/'trim.exe';(td/'geometry.txt').write_bytes(gr);(td/'input.cnf').write_bytes(raw);(td/'proof.drat').write_bytes(proof)
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(ge)],check=True,timeout=60)
        g=subprocess.run([str(ge),str(td/'geometry.txt')],capture_output=True,text=True,timeout=60);assert g.returncode==0 and g.stdout.strip()==f'VERIFIED_EDGES 2539 {len(geometry)}'
        save(a.output/'geometry.json',dict(returncode=g.returncode,stdout=g.stdout,stderr=g.stderr,input_sha256=sha(gr),wrapper_source_sha256=sha(wrapper.read_bytes()),generic_source_sha256=sha(generic.read_bytes())))
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'input.cnf'),str(td/'proof.drat'),'-U','-t','120'],capture_output=True,text=True,timeout=150)
        verified=r.returncode==0 and 's VERIFIED' in r.stdout.splitlines();save(a.output/'rup.json',dict(verified=verified,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,input_sha256=sha(raw),proof_sha256=sha(proof),checker_source_sha256=provenance['files']['drat-trim.c']))
        assert verified
    save(a.output/'summary.json',dict(verified_refutation=True,restricted_gate_cardinality=1,input_sha256=sha(raw),proof_sha256=sha(proof),geometric_quadruples=len(geometry),prior_qualification_sha256=report['prior_qualification_sha256'],source_sha256=sha(Path(__file__).read_bytes()),
        scope='Exactly-one-gate restricted input independently refuted. Unrestricted parent and five-deletion improvement remain unresolved; new lower bound on necessary gate additions needs the separate mathematical argument.'))
    print('VERIFIED exactly-one-gate refutation;',len(geometry),'integer-zero quadruples')


if __name__=='__main__':main()
