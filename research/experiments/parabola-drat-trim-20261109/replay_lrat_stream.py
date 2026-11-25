"""Replay a raw/gzip LRAT without whole-proof buffers; persist preflight first."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
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


def write_new(path, result):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--proof', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--timeout', type=float, default=600)
    args = ap.parse_args()
    driver_sha = sha(Path(__file__).read_bytes())
    args.output.mkdir(parents=True, exist_ok=False)
    source = HERE/'lrat-check-empty-fixed.c'
    source_sha = sha(source.read_bytes())
    controls = json.loads((HERE/'output/lrat-controls.json').read_text())
    assert source_sha == controls['source_sha256']['empty-fixed']
    assert all(c['results']['empty-fixed']['accepted'] == c['expected'] for c in controls['cases'])
    cnf = gzip.decompress((PRIOR/'output/shape-112/input.cnf.gz').read_bytes())
    saved_solver = json.loads((PRIOR/'output/shape-112/solver.json').read_text())
    schema_path = HERE.parent/'parabola-monotone-rup-20261109/output/encoding-audit-reservation.json'
    schema = json.loads(schema_path.read_text())
    shape_schema = next(r for r in schema['records'] if r['shape'] == '112')
    assert sha(cnf) == saved_solver['input_sha256'] == shape_schema['input_sha256']
    assert shape_schema['full_clause_schema_match'] and shape_schema['auxiliary_ranges_disjoint_and_reserved']
    assert schema['provided_edges_geometry']['returncode'] == 0
    with tempfile.TemporaryDirectory(prefix='lrat-stream-replay-') as directory:
        directory = Path(directory)
        cp, exe = directory/'input.cnf', directory/'lrat-check.exe'
        cp.write_bytes(cnf)
        proof_path = args.proof.resolve()
        compressed = proof_path.suffix == '.gz'
        digest, size, lines = hashlib.sha256(), 0, 0
        if compressed:
            proof_path = directory/'proof.lrat'
            with gzip.open(args.proof, 'rb') as src, proof_path.open('xb') as dst:
                for block in iter(lambda: src.read(8*1024*1024), b''):
                    dst.write(block)
                    digest.update(block)
                    size += len(block)
                    lines += block.count(b'\n')
        else:
            with proof_path.open('rb') as src:
                for block in iter(lambda: src.read(8*1024*1024), b''):
                    digest.update(block)
                    size += len(block)
                    lines += block.count(b'\n')
        flags = ['-std=c99', '-O2', '-DLONGTYPE', '-Dgetc_unlocked=getc']
        subprocess.run(['gcc', str(source), *flags, '-o', str(exe)], check=True, timeout=60)
        preflight = dict(p=2647, excluded_size=1323, shape='112', started_utc=datetime.now(timezone.utc).isoformat(),
                         method='LRAT hints; empty clause requires RUP conflict (K0714 local fix)',
                         input_sha256=sha(cnf), proof_raw_sha256=digest.hexdigest(), proof_raw_bytes=size,
                         proof_lines=lines, source_path=str(args.proof.resolve()), source_compressed=compressed,
                         checker_source_sha256=source_sha, checker_binary_sha256=sha(exe.read_bytes()),
                         driver_source_sha256=driver_sha, build_flags=flags, timeout_seconds=args.timeout,
                         schema_receipt_sha256=sha(schema_path.read_bytes()),
                         proof_availability='Local evidence; not assumed to exist in another checkout.')
        write_new(args.output/'preflight.json', preflight)
        print('PREFLIGHT saved; starting fixed LRAT checker', flush=True)
        start = time.monotonic()
        timed_out = False
        try:
            run = subprocess.run([str(exe), str(cp), str(proof_path)], capture_output=True, text=True, timeout=args.timeout)
            rc, out, err = run.returncode, run.stdout, run.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            rc = None
            out = (exc.stdout or b'').decode() if isinstance(exc.stdout, bytes) else (exc.stdout or '')
            err = (exc.stderr or b'').decode() if isinstance(exc.stderr, bytes) else (exc.stderr or '')
        result = dict(**preflight, returncode=rc, stdout=out, stderr=err, seconds=time.monotonic()-start,
                      timed_out=timed_out, verified=rc == 0 and 'c VERIFIED' in out.splitlines())
        write_new(args.output/'result.json', result)
        print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
