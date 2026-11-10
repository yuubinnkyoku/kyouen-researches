"""Replay adopted changed-pair exact-five CNF/DRAT and independent schema without SAT or local LRAT."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from schema import audit as qualify, COUNTER_SOURCE, SEED_SHA
CASES={"changed":(1,1)}
from verify import HERE, TRIM, sha, save, run


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();assert not args.output.exists()
    provenance=json.loads((TRIM/'vendor/provenance.json').read_text())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    seed_raw=(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes()
    assert sha(seed_raw)==SEED_SHA;seed=list(map(int,seed_raw.split()))[2:]
    regression=json.loads((HERE/'regression.json').read_text())
    assert sha((HERE/'schema.py').read_bytes())==regression['schema_source_sha256']
    assert sha(COUNTER_SOURCE.read_bytes())==regression['prefix_source_sha256']
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
    generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp';rows=[]
    with tempfile.TemporaryDirectory(prefix='p2539-five-replay-') as temporary:
        td=Path(temporary);trim,ge=td/'trim.exe',td/'geometry.exe'
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(trim)],check=True,timeout=60)
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(ge)],check=True,timeout=60)
        for case,(x,c) in CASES.items():
            source=args.saved/case;m=json.loads((source/'manifest.json').read_text());s=json.loads((source/'schema.json').read_text())
            assert sha((HERE/'schema.py').read_bytes())==m['schema_source_sha256']
            assert sha(COUNTER_SOURCE.read_bytes())==m['prefix_source_sha256']
            assert sha((HERE/'verify.py').read_bytes())==m['driver_source_sha256']
            body=gzip.decompress((source/'input.cnf.gz').read_bytes());packed=(source/'verified-proof.drat.gz').read_bytes();proof=gzip.decompress(packed)
            assert sha(body)==m['input_sha256'] and sha(packed)==m['drat_gzip_sha256'] and sha(proof)==m['drat_raw_sha256']
            edges,report=qualify(body,seed,case);assert all(s[k]==v for k,v in report.items())
            edge_raw=(f'2539 {len(edges)}\n'+''.join(' '.join(map(str,q))+'\n' for q in edges)).encode('ascii')
            assert edge_raw==gzip.decompress((source/'edges.txt.gz').read_bytes())
            prior=json.loads((source/'geometry.json').read_text());assert sha(wrapper.read_bytes())==prior['wrapper_source_sha256']
            assert sha(generic.read_bytes())==prior['generic_source_sha256']
            cp,pp,ep=td/'input.cnf',td/'proof.drat',td/'edges.txt';cp.write_bytes(body);pp.write_bytes(proof);ep.write_bytes(edge_raw)
            geometry=run([str(ge),str(ep)],60);assert geometry['returncode']==0 and geometry['stdout'].strip()==f'VERIFIED_EDGES 2539 {len(edges)}'
            rup=run([str(trim),str(cp),str(pp),'-U','-t','120'],150);assert rup['returncode']==0 and 's VERIFIED' in rup['stdout'].splitlines()
            rows.append(dict(case=case,complete_pairs=c,origin=x,input_sha256=sha(body),drat_raw_sha256=sha(proof),schema_verified=True,geometry=geometry,rup=rup))
            print('ADOPTED REPLAY',case,'PASS',flush=True)
    save(args.output,dict(cases=rows,changed_verified=True,seed_sha256=SEED_SHA,schema_source_sha256=sha((HERE/'schema.py').read_bytes()),prefix_source_sha256=sha(COUNTER_SOURCE.read_bytes()),replay_source_sha256=sha(Path(__file__).read_bytes()),scope='Adopted compressed CNF/DRAT and independent semantics replayed without SAT library or local LRAT.'))


if __name__=='__main__':main()
