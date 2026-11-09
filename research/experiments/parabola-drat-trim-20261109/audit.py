"""Check a saved shape proof with pinned upstream DRAT-trim and extract cores."""
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
    ap.add_argument('--timeout', type=float, default=600)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    provenance = json.loads((HERE/'vendor/provenance.json').read_text())
    for name, digest in provenance['files'].items():
        assert sha((HERE/'vendor'/name).read_bytes()) == digest
    location = PRIOR/'output'/('fixed' if args.shape in ('000', '101') else '')/f'shape-{args.shape}'
    original = json.loads((location/'solver.json').read_text())
    cnf = gzip.decompress((location/'input.cnf.gz').read_bytes())
    edges_raw = gzip.decompress((HERE.parent/'parabola-hplus1-drat-20261109/input/verified_edges.txt.gz').read_bytes())
    edges = [tuple(map(int, row.split())) for row in edges_raw.decode('ascii').splitlines()[1:]]
    clauses, nv, _, _ = encode(2647, args.shape, edges)
    assert dimacs(clauses, nv) == cnf and sha(cnf) == original['input_sha256']
    with tempfile.TemporaryDirectory(prefix='shape-upstream-drat-') as td:
        td = Path(td)
        cp, pp, exe = td/'input.cnf', td/'proof.drat', td/'drat-trim.exe'
        cp.write_bytes(cnf)
        digest, lines = hashlib.sha256(), 0
        with gzip.open(location/'proof.drat.gz', 'rb') as src, pp.open('wb') as dst:
            for block in iter(lambda: src.read(8*1024*1024), b''):
                dst.write(block)
                digest.update(block)
                lines += block.count(b'\n')
        assert digest.hexdigest() == original['proof_sha256'] and lines == original['proof_lines']
        flags = provenance['build_flags']
        subprocess.run(['gcc', str(HERE/'vendor/drat-trim.c'), *flags, '-o', str(exe)], check=True, timeout=60)
        command = [str(exe), str(cp), str(pp), '-U', '-t', str(int(args.timeout)),
                   '-l', str(td/'core.drat'), '-L', str(td/'core.lrat')]
        start = time.monotonic()
        timed_out = False
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout+30)
            rc, out, err = run.returncode, run.stdout, run.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            rc = None
            out = (exc.stdout or b'').decode() if isinstance(exc.stdout, bytes) else (exc.stdout or '')
            err = (exc.stderr or b'').decode() if isinstance(exc.stderr, bytes) else (exc.stderr or '')
        artifacts = {}
        for name in ('core.drat', 'core.lrat'):
            if (td/name).exists():
                raw = (td/name).read_bytes()
                (args.output/(name+'.gz')).write_bytes(gzip.compress(raw, mtime=0))
                artifacts[name] = dict(raw_bytes=len(raw), raw_sha256=sha(raw), lines=raw.count(b'\n'))
        result = dict(p=2647, target_size=1323, shape=args.shape, upstream=provenance,
                      method='DRAT-trim backward check, -U RUP-only; DRAT and LRAT cores extracted',
                      input_sha256=sha(cnf), original_proof_sha256=digest.hexdigest(), original_proof_lines=lines,
                      checker_binary_sha256=sha(exe.read_bytes()), driver_source_sha256=sha(Path(__file__).read_bytes()),
                      returncode=rc, stdout=out, stderr=err, seconds=time.monotonic()-start,
                      timed_out=timed_out, artifacts=artifacts,
                      verified=rc == 0 and 's VERIFIED' in out.splitlines())
    (args.output/'audit.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
