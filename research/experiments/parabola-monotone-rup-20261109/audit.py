"""Replay saved certificates with deletion-erased RUP-only checking, no SAT."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-size1323-drat-20261109'
sys.path.insert(0, str(PRIOR))
from corrected import encode, dimacs, SHAPES


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shape', choices=SHAPES, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=float, default=900)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    key = args.shape
    location = PRIOR/'output'/('fixed' if key in ('000', '101') else '')/f'shape-{key}'
    solver = json.loads((location/'solver.json').read_text())
    cnf = gzip.decompress((location/'input.cnf.gz').read_bytes())
    edges_raw = gzip.decompress((HERE.parent/'parabola-hplus1-drat-20261109/input/verified_edges.txt.gz').read_bytes())
    edges = [tuple(map(int, row.split())) for row in edges_raw.decode('ascii').splitlines()[1:]]
    clauses, nv, _, _ = encode(2647, key, edges)
    assert dimacs(clauses, nv) == cnf and sha(cnf) == solver['input_sha256']
    with tempfile.TemporaryDirectory(prefix=f'monotone-rup-{key}-') as directory:
        directory = Path(directory)
        cp, pp, exe = directory/'input.cnf', directory/'proof.drat', directory/'checker.exe'
        cp.write_bytes(cnf)
        digest, lines = hashlib.sha256(), 0
        with gzip.open(location/'proof.drat.gz', 'rb') as src, pp.open('wb') as dst:
            for block in iter(lambda: src.read(8*1024*1024), b''):
                dst.write(block)
                digest.update(block)
                lines += block.count(b'\n')
        assert digest.hexdigest() == solver['proof_sha256'] and lines == solver['proof_lines']
        subprocess.run(['g++', '-O2', '-std=c++17', str(HERE/'rup_check.cpp'), '-o', str(exe)], check=True, timeout=60)
        start = time.monotonic()
        timed_out = False
        try:
            run = subprocess.run([str(exe), str(cp), str(pp)], capture_output=True, text=True, timeout=args.timeout)
            rc, out, err = run.returncode, run.stdout, run.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            rc = None
            out = (exc.stdout or b'').decode() if isinstance(exc.stdout, bytes) else (exc.stdout or '')
            err = (exc.stderr or b'').decode() if isinstance(exc.stderr, bytes) else (exc.stderr or '')
        result = dict(p=2647, target_size=1323, shape=key,
                      method='deletion-erased-RUP-only; RAT forbidden',
                      input_matches_repaired_encoder=True,
                      input_sha256=sha(cnf), proof_sha256=digest.hexdigest(), proof_lines=lines,
                      original_proof_git_tracked=key != '112',
                      checker_source_sha256=sha((HERE/'rup_check.cpp').read_bytes()),
                      checker_binary_sha256=sha(exe.read_bytes()),
                      driver_source_sha256=sha(Path(__file__).read_bytes()),
                      encoder_source_sha256=sha((PRIOR/'encoding_fixed.py').read_bytes()),
                      returncode=rc, stdout=out, stderr=err, seconds=time.monotonic()-start,
                      timeout_seconds=args.timeout, timed_out=timed_out,
                      verified=rc == 0 and out.splitlines()[-1:] == ['RUP_VERIFIED'])
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
