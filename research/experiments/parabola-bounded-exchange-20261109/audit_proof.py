"""Replay a saved bounded-neighborhood proof with the existing RUP-only checker."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'parabola-monotone-rup-20261109/rup_check.cpp'
SOURCE_SHA = 'a34495ed4b9ab9ae3cdfe4c372377e83dd7e1160f7552ab16942e7d8130da2a1'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=float, default=120)
    args = ap.parse_args()
    assert not args.output.exists() and sha(SOURCE.read_bytes()) == SOURCE_SHA
    receipt = json.loads((args.saved/'result.json').read_text())
    cnf = gzip.decompress((args.saved/'input.cnf.gz').read_bytes())
    proof = gzip.decompress((args.saved/'proof.drat.gz').read_bytes())
    assert sha(cnf) == receipt['input_cnf_sha256'] and sha(proof) == receipt['proof_sha256']
    assert len(proof.splitlines()) == receipt['proof_lines']
    with tempfile.TemporaryDirectory(prefix='bounded-exchange-rup-') as directory:
        directory = Path(directory)
        exe, cp, pp = directory/'checker.exe', directory/'input.cnf', directory/'proof.drat'
        subprocess.run(['g++', '-O2', '-std=c++17', str(SOURCE), '-o', str(exe)], check=True, timeout=60)
        cp.write_bytes(cnf)
        pp.write_bytes(proof)
        started = time.monotonic()
        try:
            run = subprocess.run([str(exe), str(cp), str(pp)], capture_output=True, text=True, timeout=args.timeout)
            rc, out, err = run.returncode, run.stdout, run.stderr
            timed_out = False
        except subprocess.TimeoutExpired:
            rc, out, err, timed_out = None, '', 'TimeoutExpired', True
        result = dict(returncode=rc, stdout=out, stderr=err, timed_out=timed_out,
                      seconds=time.monotonic()-started, timeout_seconds=args.timeout,
                      verified=rc == 0 and out.splitlines()[-1:] == ['RUP_VERIFIED'],
                      input_cnf_sha256=sha(cnf), proof_sha256=sha(proof), proof_lines=receipt['proof_lines'],
                      checker_source_sha256=SOURCE_SHA, checker_binary_sha256=sha(exe.read_bytes()),
                      source_sha256=sha(Path(__file__).read_bytes()),
                      scope='Deletion-erased RUP-only replay of this bounded-neighborhood CNF; no global upper bound.')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)
    if not result['verified']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
