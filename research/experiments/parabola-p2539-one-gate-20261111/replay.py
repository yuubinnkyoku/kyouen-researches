"""Check the adopted CNF/proof in a fresh process without invoking the producer or a SAT solver."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from verify import HERE,TRIM,inspect,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    d=HERE/'output';audit=json.loads((HERE/'audit-final/summary.json').read_bytes());raw=gzip.decompress((d/'input.cnf.gz').read_bytes());proof=gzip.decompress((d/'proof.drat.gz').read_bytes())
    _,_,report=inspect(raw);assert audit['verified_refutation'] and sha(raw)==audit['input_sha256'] and sha(proof)==audit['proof_sha256'] and sha((HERE/'verify.py').read_bytes())==audit['source_sha256']
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-one-gate-replay-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';(td/'input.cnf').write_bytes(raw);(td/'proof.drat').write_bytes(proof)
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'input.cnf'),str(td/'proof.drat'),'-U','-t','120'],capture_output=True,text=True,timeout=150)
        assert r.returncode==0 and 's VERIFIED' in r.stdout.splitlines()
    save(a.output,dict(verified_refutation=True,input_sha256=sha(raw),proof_sha256=sha(proof),source_sha256=sha(Path(__file__).read_bytes()),checker_source_sha256=provenance['files']['drat-trim.c'],
        returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,scope='Fresh schema and RUP replay of the exactly-one-gate restricted input; no unrestricted UNSAT claim.'))
    print('REPLAY verified exactly-one-gate refutation')


if __name__=='__main__':main()
