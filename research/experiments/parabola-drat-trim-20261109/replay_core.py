"""Check saved extracted DRAT and LRAT cores against the original CNF."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-size1323-drat-20261109'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shape', default='112')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=float, default=600)
    ap.add_argument('--checker', choices=('both', 'rup', 'lrat'), default='both')
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    location = HERE/'output'/f'shape-{args.shape}'
    original = PRIOR/'output'/('fixed' if args.shape in ('000', '101') else '')/f'shape-{args.shape}'
    audit = json.loads((location/'audit.json').read_text())
    cnf = gzip.decompress((original/'input.cnf.gz').read_bytes())
    assert sha(cnf) == audit['input_sha256']
    flags = ['-std=c99', '-O2', '-Dgetc_unlocked=getc']
    records = []
    with tempfile.TemporaryDirectory(prefix='core-replay-') as td:
        td = Path(td)
        cp = td/'input.cnf'
        cp.write_bytes(cnf)
        # Two separate algorithms: watched RUP without hints, and LRAT hints.
        sources = [('monotone-RUP', HERE.parent/'parabola-monotone-rup-20261109/rup_check.cpp', 'core.drat', 'RUP_VERIFIED'),
                   ('empty-fixed-LRAT', HERE/'lrat-check-empty-fixed.c', 'core.lrat', 'c VERIFIED')]
        for name, source, proof_name, marker in sources:
            if args.checker == 'rup' and name != 'monotone-RUP':
                continue
            if args.checker == 'lrat' and name != 'empty-fixed-LRAT':
                continue
            proof = gzip.decompress((location/(proof_name+'.gz')).read_bytes())
            assert sha(proof) == audit['artifacts'][proof_name]['raw_sha256']
            pp, exe = td/proof_name, td/(name+'.exe')
            pp.write_bytes(proof)
            command = (['g++', '-std=c++17', '-O2'] if name == 'monotone-RUP' else ['gcc', *flags, '-DLONGTYPE'])
            subprocess.run([*command, str(source), '-o', str(exe)], check=True, timeout=60)
            start = time.monotonic()
            run = subprocess.run([str(exe), str(cp), str(pp)], capture_output=True, text=True, timeout=args.timeout)
            record = dict(checker=name, source_sha256=sha(source.read_bytes()), binary_sha256=sha(exe.read_bytes()),
                          input_sha256=sha(cnf), proof_sha256=sha(proof), proof_lines=proof.count(b'\n'),
                          returncode=run.returncode, stdout=run.stdout, stderr=run.stderr,
                          seconds=time.monotonic()-start,
                          verified=run.returncode == 0 and marker in run.stdout.splitlines())
            records.append(record)
    result = dict(p=2647, excluded_size=1323, shape=args.shape, requested_checker=args.checker, records=records,
                  all_verified=all(r['verified'] for r in records))
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
