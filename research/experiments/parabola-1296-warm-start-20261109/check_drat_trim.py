#!/usr/bin/env python3
"""Recheck the archived five-deletion proof using the pinned DRAT-trim source."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
FOLDER = HERE / 'output/target1304-seed1303-delete5-budget1m'
SOURCE_HASH = 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path, help='pinned drat-trim.c')
    parser.add_argument('--timeout', type=int, default=1200)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    source = args.source.read_bytes()
    if digest(source) != SOURCE_HASH:
        raise ValueError('DRAT-trim source hash mismatch')
    receipt = json.loads((FOLDER / 'drat-trim-check.json').read_text())
    generated = json.loads((FOLDER / 'proof-generation.json').read_text())
    cnf = gzip.decompress((FOLDER / 'input.cnf.gz').read_bytes())
    proof = gzip.decompress((FOLDER / 'local-proof.drat.gz').read_bytes())
    for key, data in (('cnf_sha256', cnf), ('proof_sha256', proof)):
        if digest(data) != receipt[key] or digest(data) != generated[key]:
            raise ValueError(f'{key} mismatch')
    if receipt['checker_source_sha256'] != SOURCE_HASH:
        raise ValueError('receipt source hash mismatch')
    with tempfile.TemporaryDirectory(prefix='q2647-drat-trim-') as tmp:
        folder = Path(tmp)
        (folder / 'checker.c').write_bytes(source)
        (folder / 'input.cnf').write_bytes(cnf)
        (folder / 'proof.drat').write_bytes(proof)
        (folder / 'truncated.drat').write_bytes(b'\n'.join(proof.splitlines()[:100]) + b'\n')
        executable = folder / 'drat-trim'
        subprocess.run(['gcc', '-D_GNU_SOURCE', '-O2', '-std=c99', str(folder / 'checker.c'),
                        '-o', str(executable)], check=True)
        good = subprocess.run([str(executable), str(folder / 'input.cnf'), str(folder / 'proof.drat')],
                              capture_output=True, text=True, timeout=args.timeout)
        if good.returncode != 0 or 's VERIFIED' not in good.stdout.splitlines():
            raise RuntimeError(f'proof was not verified: {good.returncode}\n{good.stdout}\n{good.stderr}')
        bad = subprocess.run([str(executable), str(folder / 'input.cnf'), str(folder / 'truncated.drat')],
                             capture_output=True, text=True, timeout=args.timeout)
        if bad.returncode == 0 or 's NOT VERIFIED' not in bad.stdout.splitlines():
            raise RuntimeError(f'truncated proof was not rejected: {bad.returncode}\n{bad.stdout}\n{bad.stderr}')
    print(json.dumps({'cnf_sha256': digest(cnf), 'proof_sha256': digest(proof),
                      'source_sha256': digest(source), 'proof': 'VERIFIED',
                      'truncated_proof': 'NOT VERIFIED',
                      'scope': 'fixed pair and at most five deletions; not a global upper bound'}, indent=2))


if __name__ == '__main__':
    main()
