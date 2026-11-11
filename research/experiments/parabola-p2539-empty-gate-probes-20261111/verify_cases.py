"""Independently close negative assumptions and derive a smaller positive gate."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import time
from audit import HERE,qualify_base,sha,save

BRIDGE=HERE.parent/'parabola-p2539-point-rup-bridge-20261111'
spec=importlib.util.spec_from_file_location('gate_case_lifting',BRIDGE/'verify.py');lifting=importlib.util.module_from_spec(spec);spec.loader.exec_module(lifting)
TRIM=HERE.parent/'parabola-drat-trim-20261109'


def run(cmd,timeout=180):
    started=time.monotonic()
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
        return dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False,elapsed_seconds=time.monotonic()-started)
    except subprocess.TimeoutExpired as exc:
        dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
        return dict(returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True,elapsed_seconds=time.monotonic()-started)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    base=gzip.decompress((HERE/'output/base.cnf.gz').read_bytes())
    seed=list(map(int,(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes().split()))[2:]
    _,_,_,schema=qualify_base(base,seed)
    audited=json.loads((HERE/'input-audit/summary.json').read_bytes());assert audited['base_input_sha256']==sha(base)
    assert sha((HERE/'audit.py').read_bytes())==audited['source_sha256']
    points=sorted(r['point'] for r in audited['cases'] if r['status']=='SOLVER_UNSAT');rows=[]
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-gate-cases-') as temporary:
        td=Path(temporary);exe=td/'trim.exe'
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        def one(u):
            source=HERE/'proof-output'/str(u);r=json.loads((source/'result.json').read_bytes());launch=json.loads((source/'launch.json').read_bytes())
            assert launch['returncode']==0 and not launch['timed_out'] and r['status']=='SOLVER_UNSAT' and r['proof_complete']
            assert r['point']==u and r['assumption']==36512+u and r['base_input_sha256']==sha(base)
            assert sha((HERE/'search.py').read_bytes())==r['source_sha256'] and sha((HERE/'encoding.py').read_bytes())==r['encoding_source_sha256']
            out=a.output/str(u);out.mkdir();work=td/str(u);work.mkdir()
            child=('p cnf 51570 144663\n'+'\n'.join(base.decode('ascii').splitlines()[1:])+f'\n{36512+u} 0\n').encode('ascii');assert sha(child)==r['child_input_sha256']
            raw=gzip.decompress((source/'proof.drat.gz').read_bytes());assert sha(raw)==r['proof_sha256']
            cp,pp=work/'child.cnf',work/'child.drat';cp.write_bytes(child);pp.write_bytes(raw);core=(out/'core.drat').resolve()
            rup=run([str(exe),str(cp),str(pp),'-U','-t','150','-l',str(core)])
            verified=rup['returncode']==0 and 's VERIFIED' in rup['stdout'].splitlines()
            save(out/'child-rup.json',dict(verified=verified,child_input_sha256=sha(child),proof_sha256=sha(raw),**rup))
            row=dict(point=u,independent_child_refutation=verified,verified_base_unit=False,base_input_sha256=sha(base))
            if verified:
                core_raw=core.read_bytes();(out/'core.drat.gz').write_bytes(gzip.compress(core_raw,mtime=0));lifted=lifting.lift(core_raw,36512+u)
                cp.write_bytes(base);pp.write_bytes(lifted);derived=run([str(exe),str(cp),str(pp),'-f','-U','-t','150'])
                accepted=not derived['timed_out'] and lifting.derivation(derived);(out/'negative-unit.rup.gz').write_bytes(gzip.compress(lifted,mtime=0))
                save(out/'unit-rup.json',dict(verified=accepted,base_input_sha256=sha(base),derived_unit=-(36512+u),core_sha256=sha(core_raw),proof_sha256=sha(lifted),**derived))
                row.update(verified_base_unit=accepted,core_sha256=sha(core_raw),negative_unit_proof_sha256=sha(lifted),derived_unit=-(36512+u))
            save(out/'manifest.json',dict(**row,source_sha256=sha(Path(__file__).read_bytes()),lifting_source_sha256=sha((BRIDGE/'verify.py').read_bytes()),checker_source_sha256=provenance['files']['drat-trim.c'],
                scope='Negative unit from base augmented with116 geometric exclusions, not a proof from the original retained CNF alone.'))
            print('CASE',u,'child',verified,'unit',row['verified_base_unit'],flush=True);return row
        with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(one,points))
        proved=sorted(r['point'] for r in rows if r['verified_base_unit']);remaining=sorted(set(schema['gate_points'])-set(proved))
        assert remaining
        reduced=(f'p cnf 51570 {144662+len(proved)}\n'+'\n'.join(base.decode('ascii').splitlines()[1:])+'\n'+''.join(f'{-(36512+u)} 0\n' for u in proved)).encode('ascii')
        proof=(' '.join(str(36512+u) for u in remaining)+' 0\n').encode('ascii')
        (a.output/'reduced-base.cnf.gz').write_bytes(gzip.compress(reduced,mtime=0));(a.output/'remaining-gate.rup.gz').write_bytes(gzip.compress(proof,mtime=0))
        cp,pp=td/'reduced.cnf',td/'gate.rup';cp.write_bytes(reduced);pp.write_bytes(proof)
        gate=run([str(exe),str(cp),str(pp),'-f','-U','-t','30'],60);assert lifting.derivation(gate) and not gate['timed_out']
        save(a.output/'remaining-gate.json',dict(remaining_gate=remaining,verified_derivation=True,parent_unsat_claimed=False,reduced_input_sha256=sha(reduced),proof_sha256=sha(proof),**gate))
    save(a.output/'summary.json',dict(requested_negative_cases=points,proved_points=proved,remaining_gate=remaining,remaining_count=len(remaining),base_input_sha256=sha(base),
        reduced_input_sha256=sha(reduced),all_excluded_points=sorted(set(schema['excluded'])|set(proved)),source_sha256=sha(Path(__file__).read_bytes()),
        cases=rows,scope='Closed point assumptions plus a reduced positive gate, conditional on independently audited116 geometric exclusions. Remaining cases are unresolved; no global UNSAT claim.'))
    print('VERIFIED',len(proved),'new exclusions; remaining gate',len(remaining),flush=True)


if __name__=='__main__':main()
