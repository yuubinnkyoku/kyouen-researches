"""Lift assumption refutations and check RUP-only partial derivations against the parent alone."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE=Path(__file__).resolve().parent
TRIM=HERE.parent/'parabola-drat-trim-20261109'
PARENT=HERE.parent/'parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def run(cmd,timeout=120):
    started=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
    return dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,elapsed_seconds=time.monotonic()-started)


def derivation(r):
    # Upstream returns1 for DERIVATION because only final UNSAT returns0.
    return r['returncode']==1 and 's DERIVATION' in r['stdout'].splitlines() and 'c VERIFIED derivation: all lemmas preserve satisfiability' in r['stdout'].splitlines() and 's NOT VERIFIED' not in r['stdout'].splitlines() and 'failed at proof line' not in r['stdout']


def lift(raw,assumption):
    assert 0<assumption<=51570;out=[];empty=False
    for line in raw.decode('ascii').splitlines():
        vals=line.split();assert vals
        if vals[0]=='d':continue
        clause=list(map(int,vals));assert clause[-1]==0 and all(0<abs(v)<=51570 for v in clause[:-1]);clause=clause[:-1]
        if not clause:empty=True
        if assumption in clause:continue # Lifted tautology cannot be used by propagation.
        lifted=list(dict.fromkeys(clause+[-assumption]));out.append(lifted)
    assert empty and out and out[-1]==[-assumption]
    return ''.join(' '.join(map(str,c))+' 0\n' for c in out).encode('ascii')


def controls(exe,td):
    cnf=td/'control.cnf';proof=td/'control.drat';rows=[]
    cases=[('valid-unit',b'p cnf 2 2\n1 2 0\n1 -2 0\n',b'1 0\n',True),
           ('false-unit',b'p cnf 2 1\n1 2 0\n',b'-1 0\n',False),
           ('false-binary',b'p cnf 3 1\n1 2 0\n',b'-1 -2 0\n',False),
           ('rat-only',b'p cnf 2 1\n1 2 0\n',b'-2 1 0\n',False),
           ('valid-nonunit',b'p cnf 3 1\n1 2 0\n',b'1 2 3 0\n',True)]
    for name,f,p,expected in cases:
        cnf.write_bytes(f);proof.write_bytes(p);r=run([str(exe),str(cnf),str(proof),'-f','-U','-t','30']);assert derivation(r)==expected,(name,r)
        rows.append(dict(name=name,expected_derivation=expected,**r))
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--points',type=int,nargs='*')
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    body=gzip.decompress(PARENT.read_bytes());assert sha(body)==PARENT_SHA
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    points=sorted(int(p.name) for p in a.saved.iterdir() if p.is_dir()) if a.points is None else a.points;rows=[];combined=[]
    with tempfile.TemporaryDirectory(prefix='p2539-rup-bridge-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        save(a.output/'controls.json',dict(cases=controls(exe,td),checker_source_sha256=provenance['files']['drat-trim.c']))
        cp,pp=td/'parent.cnf',td/'lifted.drat';cp.write_bytes(body)
        for u in points:
            d=a.saved/str(u);r=json.loads((d/'result.json').read_bytes());launch=json.loads((d/'launch.json').read_bytes())
            assert launch['returncode']==0 and not launch['timed_out'] and r['status']=='SOLVER_UNSAT' and r['proof_complete']
            assert r['point']==u and r['assumption']==36512+u and r['parent_input_sha256']==PARENT_SHA
            assert sha((HERE/'produce.py').read_bytes())==r['source_sha256']
            raw=gzip.decompress((d/'child-proof.drat.gz').read_bytes());assert sha(raw)==r['proof_sha256']
            lifted=lift(raw,r['assumption']);pp.write_bytes(lifted)
            checked=run([str(exe),str(cp),str(pp),'-f','-U','-t','120']);assert derivation(checked),(u,checked)
            out=a.output/str(u);out.mkdir();(out/'lifted.rup.gz').write_bytes(gzip.compress(lifted,mtime=0))
            rec=dict(point=u,derived_unit=-(36512+u),parent_input_sha256=PARENT_SHA,child_proof_sha256=sha(raw),lifted_raw_sha256=sha(lifted),lifted_lines=lifted.count(b'\n'),
                checker_source_sha256=provenance['files']['drat-trim.c'],driver_source_sha256=sha(Path(__file__).read_bytes()),verified_parent_only_derivation=True,
                scope='A RUP-only derivation of one negative point unit from the retained parent CNF alone; no empty clause and no parent UNSAT claim.',**checked)
            save(out/'receipt.json',rec);rows.append(rec);combined.append(lifted);print('DERIVED',u,len(lifted),flush=True)
        all_raw=b''.join(combined);pp.write_bytes(all_raw);checked=run([str(exe),str(cp),str(pp),'-f','-U','-t','120']);assert derivation(checked)
        (a.output/'all-units.rup.gz').write_bytes(gzip.compress(all_raw,mtime=0));save(a.output/'combined.json',checked)
    save(a.output/'summary.json',dict(points=points,derived_units=[-(36512+u) for u in points],all_verified=True,parent_input_sha256=PARENT_SHA,
        combined_raw_sha256=sha(all_raw),combined_lines=all_raw.count(b'\n'),source_sha256=sha(Path(__file__).read_bytes()),checker_source_sha256=provenance['files']['drat-trim.c'],
        scope='Independent parent-only RUP unit derivations; forward DERIVATION is not an UNSAT refutation.'))


if __name__=='__main__':main()
