"""Derive that an improvement must occupy at least one originally empty-pair point."""
import argparse
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from verify import HERE,checker,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    seed_raw=checker.SEED.read_bytes();assert sha(seed_raw)==checker.SEED_SHA;seed=set(map(int,seed_raw.split()[2:]))
    empty=sorted(t for t in range(1,2539) if t not in seed and 2539-t not in seed);assert len(empty)==26
    pairs=[i for i in range(1,1270) if i not in seed and 2539-i not in seed];assert len(pairs)==13
    assert [i for i in range(1,1270) if i in seed and 2539-i in seed]==[6]
    raw=gzip.decompress((HERE.parent/'parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz').read_bytes())
    assert sha(raw)=='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
    proof=(' '.join(str(36512+u) for u in empty)+' 0\n').encode('ascii');(a.output/'empty-pair-clause.rup.gz').write_bytes(gzip.compress(proof,mtime=0))
    trim=HERE.parent/'parabola-drat-trim-20261109';provenance=json.loads((trim/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((trim/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-empty-pair-gate-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';(td/'input.cnf').write_bytes(raw);(td/'proof.rup').write_bytes(proof)
        subprocess.run(['gcc',str(trim/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'input.cnf'),str(td/'proof.rup'),'-f','-U','-t','30'],capture_output=True,text=True,timeout=60)
        assert r.returncode==1 and 's DERIVATION' in r.stdout.splitlines() and 'c VERIFIED derivation: all lemmas preserve satisfiability' in r.stdout.splitlines()
        assert 's NOT VERIFIED' not in r.stdout.splitlines() and 'failed at proof line' not in r.stdout
    save(a.output/'receipt.json',dict(empty_pair_points=empty,empty_pair_representatives=pairs,derived_positive_clause=[36512+u for u in empty],verified_parent_only_derivation=True,parent_unsat_claimed=False,
        parent_input_sha256=sha(raw),proof_sha256=sha(proof),source_sha256=sha(Path(__file__).read_bytes()),checker_source_sha256=provenance['files']['drat-trim.c'],
        returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,scope='One positive26-point clause is a RUP consequence of the exact1259 retained parent. It is not a global UNSAT refutation.'))
    print('DERIVED at least one of26 originally empty-pair points; one-clause parent-only RUP')


if __name__=='__main__':main()
