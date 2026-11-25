#!/usr/bin/env python3
"""Compile the fixed DRAT checker and verify the saved local proof and controls."""
import gzip
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE=Path(__file__).resolve().parent
EXP=HERE/'output/target1304-seed1303-delete2-budget300000'
CHECKER=HERE.parent/'parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp'
SIMPLE=HERE.parent/'parabola-p2207-no-equality-witness-20261107/drat_check.cpp'


def sha(data): return hashlib.sha256(data).hexdigest()


def main():
    global EXP
    ap=argparse.ArgumentParser()
    ap.add_argument('directory', nargs='?', type=Path, default=EXP)
    EXP=ap.parse_args().directory
    cnf=gzip.decompress((EXP/'input.cnf.gz').read_bytes())
    proof=gzip.decompress((EXP/'local-proof.drat.gz').read_bytes())
    meta=json.loads((EXP/'proof-generation.json').read_text())
    assert sha(cnf)==meta['cnf_sha256'] and sha(proof)==meta['proof_sha256']
    with tempfile.TemporaryDirectory(prefix='q2647-local-drat-') as td:
        root=Path(td); c=root/'input.cnf'; p=root/'proof.drat'; binary=root/'checker'; simple=root/'simple'
        c.write_bytes(cnf);p.write_bytes(proof)
        subprocess.run(['c++','-O2','-std=c++17',str(CHECKER),'-o',str(binary)],check=True)
        subprocess.run(['c++','-O2','-std=c++17',str(SIMPLE),'-o',str(simple)],check=True)
        start=time.monotonic()
        checked=subprocess.run([str(binary),str(c),str(p)],capture_output=True,text=True,timeout=180)
        assert checked.returncode==0 and checked.stdout.strip().splitlines()[-1]=='VERIFIED'
        other=subprocess.run([str(simple),str(c),str(p)],capture_output=True,text=True,timeout=180)
        assert other.returncode==0 and other.stdout.strip().splitlines()[-1]=='VERIFIED'
        bad=root/'truncated.drat'; bad.write_bytes(b'\n'.join(proof.splitlines()[:100])+b'\n')
        control=subprocess.run([str(binary),str(c),str(bad)],capture_output=True,text=True,timeout=60)
        assert control.returncode != 0 and 'VERIFIED' not in control.stdout
        other_control=subprocess.run([str(simple),str(c),str(bad)],capture_output=True,text=True,timeout=60)
        assert other_control.returncode != 0 and 'VERIFIED' not in other_control.stdout
        receipt={'cnf_sha256':sha(cnf),'proof_sha256':sha(proof),
                 'checker_source_sha256':sha(CHECKER.read_bytes()),
                 'checker_returncode':checked.returncode,'checker_stdout':checked.stdout.strip(),
                 'truncated_proof_returncode':control.returncode,
                 'simple_checker_source_sha256':sha(SIMPLE.read_bytes()),
                 'simple_checker_returncode':other.returncode,'simple_checker_stdout':other.stdout.strip(),
                 'simple_truncated_proof_returncode':other_control.returncode,
                 'elapsed_seconds':time.monotonic()-start,
                 'scope':'one fixed-pair bounded-deletion CNF; not a global upper bound'}
    (EXP/'proof-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
