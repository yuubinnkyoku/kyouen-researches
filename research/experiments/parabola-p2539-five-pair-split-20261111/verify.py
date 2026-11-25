"""Independent schema, integer geometry, RUP and fixed-LRAT verification of frozen inputs."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
from schema import audit as qualify, COUNTER_SOURCE, SEED_SHA
from check_inputs import SEED
CASES={"changed":(1,1)}

HERE=Path(__file__).resolve().parent
TRIM=HERE.parent/'parabola-drat-trim-20261109'
FIXED_SHA='ca64680b89dde26ff2ea96b05c0fb926972eb307b74ffa18453e89a5da2988c8'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def run(cmd,timeout):
    started=time.monotonic()
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
        return dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False,elapsed_seconds=time.monotonic()-started)
    except subprocess.TimeoutExpired as exc:
        dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
        return dict(returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True,elapsed_seconds=time.monotonic()-started)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--timeout',type=int,default=120)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    provenance=json.loads((TRIM/'vendor/provenance.json').read_text())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    fixed=TRIM/'lrat-check-empty-fixed.c';assert sha(fixed.read_bytes())==FIXED_SHA
    prior=json.loads((HERE.parent/'parabola-p2539-exchange-audit-20261110/regression.json').read_text())
    assert sha(COUNTER_SOURCE.read_bytes())==prior['schema_source_sha256']
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
    generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    manifests=[]
    with tempfile.TemporaryDirectory(prefix='p2539-five-proof-') as temporary:
        td=Path(temporary);ge,trim,lr=td/'geometry.exe',td/'trim.exe',td/'lrat.exe'
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(ge)],check=True,timeout=60)
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(trim)],check=True,timeout=60)
        subprocess.run(['gcc',str(fixed),*provenance['build_flags'],'-DLONGTYPE','-o',str(lr)],check=True,timeout=60)
        for case,(x,c) in CASES.items():
            source=HERE/'output'/case;produced=HERE/'proof-output'/case;out=args.output/case;out.mkdir()
            init=json.loads((source/'init.json').read_text());original=json.loads((source/'result.json').read_text());result=json.loads((produced/'result.json').read_text())
            body=gzip.decompress((source/'input.cnf.gz').read_bytes())
            assert sha(body)==init['input_sha256']==original['input_sha256']==result['input_sha256']
            assert sha((HERE/'search.py').read_bytes())==init['source_sha256']
            assert sha((HERE/'search.py').read_bytes())==result['source_sha256']
            seed_raw=SEED.read_bytes();assert sha(seed_raw)==SEED_SHA==init['seed_sha256']==result['seed_sha256']
            seed=list(map(int,seed_raw.split()));assert seed[:2]==[2539,1258] and len(seed)==1260
            edges,schema=qualify(body,seed[2:],case)
            assert original['status']=='SOLVER_UNSAT' and result['status']=='SOLVER_UNSAT' and result['proof_complete']
            packed=(produced/'proof.drat.gz').read_bytes();proof=gzip.decompress(packed)
            assert sha(proof)==result['proof_sha256'] and proof.count(b'\n')==result['proof_lines']
            edge_raw=(f'2539 {len(edges)}\n'+''.join(' '.join(map(str,q))+'\n' for q in edges)).encode('ascii')
            (out/'input.cnf.gz').write_bytes(gzip.compress(body,mtime=0));(out/'edges.txt.gz').write_bytes(gzip.compress(edge_raw,mtime=0))
            schema.update(input_sha256=sha(body),seed_sha256=SEED_SHA,edge_input_sha256=sha(edge_raw),schema_source_sha256=sha((HERE/'schema.py').read_bytes()),prefix_source_sha256=sha(COUNTER_SOURCE.read_bytes()),driver_source_sha256=sha(Path(__file__).read_bytes()))
            save(out/'schema.json',schema)
            cp,pp,ep=td/'input.cnf',td/'proof.drat',td/'edges.txt';cp.write_bytes(body);pp.write_bytes(proof);ep.write_bytes(edge_raw)
            geometry=run([str(ge),str(ep)],60);geometry.update(generic_source_sha256=sha(generic.read_bytes()),wrapper_source_sha256=sha(wrapper.read_bytes()))
            save(out/'geometry.json',geometry);assert geometry['returncode']==0 and geometry['stdout'].strip()==f'VERIFIED_EDGES 2539 {len(edges)}'
            core=(out/'core.lrat').resolve()
            rup=run([str(trim),str(cp),str(pp),'-U','-t',str(args.timeout),'-L',str(core)],args.timeout+30)
            rup.update(verified=rup['returncode']==0 and 's VERIFIED' in rup['stdout'].splitlines(),input_sha256=sha(body),proof_sha256=sha(proof),checker_source_sha256=provenance['files']['drat-trim.c'])
            save(out/'rup.json',rup);print(case,'RUP',rup['verified'],flush=True);assert rup['verified']
            lrat=run([str(lr),str(cp),str(core)],args.timeout)
            lrat.update(verified=lrat['returncode']==0 and 'c VERIFIED' in lrat['stdout'].splitlines(),input_sha256=sha(body),checker_source_sha256=FIXED_SHA)
            save(out/'lrat.json',lrat);print(case,'LRAT',lrat['verified'],flush=True);assert lrat['verified']
            raw=core.read_bytes();gz=gzip.compress(raw,compresslevel=1,mtime=0);(out/'core.lrat.gz').write_bytes(gz)
            (out/'verified-proof.drat.gz').write_bytes(packed)
            manifest=dict(case=case,p=2539,origin=x,complete_pairs=c,target_size=1259,removed_exactly=5,nonzero_removed_exactly=5-(1-x),excluded_complete_pair=6,split_unit=-21,seed_sha256=SEED_SHA,input_sha256=sha(body),drat_raw_sha256=sha(proof),drat_gzip_sha256=sha(packed),drat_lines=proof.count(b'\n'),lrat_raw_sha256=sha(raw),lrat_gzip_sha256=sha(gz),lrat_lines=raw.count(b'\n'),lrat_storage='Raw and compressed LRAT retained locally and Git-ignored; adopted DRAT gzip Git-managed',schema_geometry_rup_lrat_verified=True,schema_source_sha256=schema['schema_source_sha256'],prefix_source_sha256=schema['prefix_source_sha256'],driver_source_sha256=sha(Path(__file__).read_bytes()),fixed_lrat_source_sha256=FIXED_SHA,scope='No safe exact1259 set losing exactly5 seed points can retain origin and have one complete pair different from {6,2533}. The retained original-pair class remains UNKNOWN.')
            save(out/'manifest.json',manifest);manifests.append(manifest);del raw,gz
    save(args.output/'summary.json',dict(cases=manifests,changed_verified=True,scope='Changed complete pair excluded independently at exact-five loss; the retained pair remains UNKNOWN and the global upper bound is unchanged.'))


if __name__=='__main__':main()
