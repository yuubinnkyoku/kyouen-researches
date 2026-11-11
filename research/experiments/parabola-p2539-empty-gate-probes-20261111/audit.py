"""Interpret all point-assumption inputs and verify saved models without importing search/encoding."""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


parent=load('empty_gate_parent_schema',HERE.parent/'parabola-p2539-five-pair-split-20261111/schema.py')
obstructions=load('empty_gate_obstructions',HERE.parent/'parabola-p2539-pair-obstructions-20261111/verify.py')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def qualify_base(raw,seed):
    nv,cs=parent.prefix.parse(raw);assert nv==51570 and len(cs)==144662
    original=('p cnf 51570 144546\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs[:-116])).encode('ascii')
    assert sha(original)=='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
    geo,report=parent.audit(original,seed,'retained');assert report['point_base']==36512
    folder=HERE.parent/'parabola-p2539-pair-obstructions-20261111';cr=(folder/'output/certificate.json').read_bytes();cert=json.loads(cr)
    receipt=json.loads((folder/'audit-output/summary.json').read_bytes());assert sha(cr)==receipt['certificate_sha256'] and cert['excluded']==receipt['excluded']
    excluded=cert['excluded'];assert len(excluded)==116 and cs[-116:]==[[-36512-u] for u in excluded]
    eraw=gzip.decompress((HERE.parent/'parabola-p2539-pair-pilot-20261110/output/edges.txt.gz').read_bytes())
    assert sha(eraw)==cert['edge_input_sha256'];edges=[tuple(map(int,l.split())) for l in eraw.splitlines()[1:]]
    fs,added=obstructions.families(seed,edges);entries={r['point']:r for r in cert['entries']};extra=[]
    for u in excluded:
        qs=fs[u];r=entries[u];assert r['status']=='EXCLUDED' and r['obstructions']==len(qs)
        obstructions.checker.check_tree([set(q)-{u,0,6,2533} for q in qs],5,r['refutation']);extra.extend(qs)
    gate=json.loads((folder/'gate-output/receipt.json').read_bytes())
    assert gate['parent_input_sha256']==sha(original) and gate['verified_parent_only_derivation'] and len(gate['empty_pair_points'])==26
    assert 's DERIVATION' in gate['stdout'].splitlines()
    report.update(base_input_sha256=sha(raw),base_clauses=len(cs),excluded=excluded,gate_points=gate['empty_pair_points'],obstruction_certificate_sha256=sha(cr),
        scope='Independent retained-parent schema plus replayed116 geometric/hitting exclusions. Twenty-six overlapping point cases cover all safe improvements; no solver status promoted here.')
    return cs,geo,extra,report


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    seed_raw=(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes()
    assert sha(seed_raw)=='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb';seed=list(map(int,seed_raw.split()))[2:]
    body=gzip.decompress((a.saved/'base.cnf.gz').read_bytes());cs,geo,extra,report=qualify_base(body,seed);save(a.output/'schema.json',report)
    assert sorted(int(d.name) for d in a.saved.iterdir() if d.is_dir())==report['gate_points']
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp';rows=[];geometries=[]
    with tempfile.TemporaryDirectory(prefix='p2539-gate-audit-') as temporary:
        td=Path(temporary);ge=td/'geometry.exe';subset=td/'subset.exe'
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(ge)],check=True,timeout=60)
        for name,edges in [('parent',geo),('exclusion-trees',extra)]:
            eraw=(f'2539 {len(edges)}\n'+''.join(' '.join(map(str,q))+'\n' for q in edges)).encode('ascii');(td/'edges.txt').write_bytes(eraw)
            r=subprocess.run([str(ge),str(td/'edges.txt')],capture_output=True,text=True,timeout=60)
            assert r.returncode==0 and r.stdout.strip()==f'VERIFIED_EDGES 2539 {len(edges)}'
            geometries.append(dict(kind=name,quadruples=len(edges),returncode=r.returncode,stdout=r.stdout,input_sha256=sha(eraw)))
        for u in report['gate_points']:
            d=a.saved/str(u);init=json.loads((d/'init.json').read_bytes());r=json.loads((d/'result.json').read_bytes());launch=json.loads((d/'launch.json').read_bytes())
            assert launch['returncode']==0 and not launch['timed_out'] and all(r[k]==v for k,v in init.items())
            assert sha((HERE/'search.py').read_bytes())==r['source_sha256'] and sha((HERE/'encoding.py').read_bytes())==r['encoding_source_sha256']
            child=('p cnf 51570 144663\n'+'\n'.join(body.decode('ascii').splitlines()[1:])+f'\n{36512+u} 0\n').encode('ascii')
            assert sha(child)==r['child_input_sha256'] and sha(body)==r['base_input_sha256'] and r['point']==u and r['assumption']==36512+u
            row=dict(point=u,status=r['status'],child_input_sha256=sha(child),input_schema_verified=True,verified_safe=False,independent_unsat_proof=False)
            if r['status']=='SAT':
                model=json.loads((d/'model.json').read_bytes())['signed_model'];assert len(model)==51570 and {abs(v) for v in model}==set(range(1,51571));pos={v for v in model if v>0}
                assert all(any((v>0)==(abs(v) in pos) for v in c) for c in cs+[[36512+u]])
                points=[0]+[t for t in range(1,2539) if 36512+t in pos];candidate=(d/'candidate.txt').read_bytes()
                assert list(map(int,candidate.split()))==[2539,1259]+points and len(points)==1259 and {0,6,2533,u}<=set(points)
                assert len(set(seed)-set(points))==5 and not set(points)&set(report['excluded']) and sha(candidate)==r['candidate_sha256']
                if not subset.exists():subprocess.run(['g++','-O2','-std=c++17',str(generic),'-o',str(subset)],check=True,timeout=60)
                checked=subprocess.run([str(subset),'--modular-filter'],input=candidate,capture_output=True,timeout=180)
                assert checked.returncode in [0,4]
                row.update(verified_safe=checked.returncode==0,generic_returncode=checked.returncode,generic_stdout=checked.stdout.decode(),generic_stderr=checked.stderr.decode(),candidate_sha256=sha(candidate))
                if checked.returncode==0:assert list(map(int,checked.stdout.split()))[:3]==[2539,1259,math.comb(1259,4)]
            else:assert not (d/'candidate.txt').exists() and not (d/'model.json').exists()
            save(a.output/(str(u)+'.json'),row);rows.append(row);print('AUDIT',u,r['status'],'safe',row['verified_safe'],flush=True)
    save(a.output/'summary.json',dict(cases=rows,status_counts=dict(Counter(r['status'] for r in rows)),verified_safe_count=sum(r['verified_safe'] for r in rows),
        base_input_sha256=sha(body),overlapping_cover=True,geometry_checks=geometries,source_sha256=sha(Path(__file__).read_bytes()),
        generic_source_sha256=sha(generic.read_bytes()),scope='All26 assumption inputs and any positive models checked. UNKNOWN and solver UNSAT remain distinct from independent negative proofs.'))


if __name__=='__main__':main()
