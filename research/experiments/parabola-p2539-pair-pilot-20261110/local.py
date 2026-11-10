"""Construct a large safe subset from bounded local search and geometric repair."""
import argparse
from collections import Counter
import gzip
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time
from pilot import HERE, candidate, save, sha


def repair(points, edges):
    selected = set(points)
    bad = [set(q) for q in edges if set(q) <= selected]
    remaining = list(bad)
    removed = []
    while remaining:
        counts = Counter(t for q in remaining for t in q)
        t = min(counts, key=lambda v: (-counts[v], v))
        removed.append(t)
        remaining = [q for q in remaining if t not in q]
    for t in list(reversed(removed)):
        trial = set(removed)-{t}
        if all(q & trial for q in bad):
            removed.remove(t)
    safe = sorted(selected-set(removed))
    assert all(not set(q) <= set(safe) for q in edges)
    return safe, removed, len(bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--ds', default='1,631,1237')
    ap.add_argument('--steps', type=int, default=1000000)
    args = ap.parse_args()
    assert args.steps > 0
    plan = json.loads((args.saved/'plan.json').read_text())
    edge_raw = gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    assert sha(edge_raw) == plan['edge_input_sha256']
    edges = [tuple(map(int, s.split())) for s in edge_raw.decode('ascii').splitlines()[1:]]
    assert len(edges) == 38868
    ds = list(map(int, args.ds.split(',')))
    assert ds and len(ds) == len(set(ds)) and all(d in plan['requested_d'] for d in ds)
    args.output.mkdir(parents=True, exist_ok=False)
    walk_source = HERE.parent/'parabola-local-repair-20261109/walk.cpp'
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    rows = []
    with tempfile.TemporaryDirectory(prefix='p2539-local-repair-') as directory:
        directory = Path(directory)
        exe, verifier = directory/'walk.exe', directory/'geometry.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(walk_source), '-o', str(exe)], check=True, timeout=60)
        subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(verifier)], check=True, timeout=60)
        for d in ds:
            out = args.output/f'd{d}'; out.mkdir()
            raw = gzip.decompress((args.saved/f'd{d}/input.cnf.gz').read_bytes())
            receipt = json.loads((args.saved/f'd{d}/result.json').read_text())
            assert sha(raw) == receipt['input_sha256']
            cnf = directory/f'd{d}.cnf'; cnf.write_bytes(raw)
            started = time.monotonic()
            r = subprocess.run([str(exe), str(cnf), str(out/'model.json'), str(args.steps), str(20261110+d)], capture_output=True, text=True, timeout=180)
            (out/'stdout.txt').write_text(r.stdout, encoding='ascii', newline='\n')
            assert r.returncode == 0, r.stderr
            model = json.loads((out/'model.json').read_text())
            positive = set(model['positive'])
            assert len(positive) == len(model['positive']) and all(1 <= v <= 1269 for v in positive)
            clauses = [list(map(int, line.split()))[:-1] for line in raw.decode('ascii').splitlines()[1:]]
            violations = sum(not any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
            assert violations == model['violations']
            full = candidate(d, positive)
            points, removed, bad = repair(full, edges)
            (out/'candidate.txt').write_bytes((f'2539 {len(points)}\n'+' '.join(map(str, points))+'\n').encode('ascii'))
            row = dict(d=d, local_elapsed_seconds=time.monotonic()-started, violations=violations,
                       bad_provided_edges=bad, removed=removed, size=len(points), input_sha256=sha(raw),
                       candidate_sha256=sha((out/'candidate.txt').read_bytes()), walk_source_sha256=sha(walk_source.read_bytes()))
            save(out/'repair.json', row)
            rows.append(row)
            print('d', d, 'violations', violations, 'repaired size', len(points), flush=True)
        best = max(rows, key=lambda r: (r['size'], -r['d']))
        raw = (args.output/f'd{best["d"]}/candidate.txt').read_bytes()
        (args.output/'candidate.txt').write_bytes(raw)
        started = time.monotonic()
        r = subprocess.run([str(verifier), '--modular-filter'], input=raw, capture_output=True, timeout=120)
        verified = r.returncode == 0
        if verified:
            values = list(map(int, r.stdout.split()))
            assert len(values) == 4 and values[:3] == [2539, best['size'], math.comb(best['size'], 4)]
        report = dict(p=2539, size=best['size'], from_d=best['d'], verified=verified,
                      returncode=r.returncode, stdout=r.stdout.decode(), stderr=r.stderr.decode(),
                      elapsed_seconds=time.monotonic()-started, candidate_sha256=sha(raw),
                      generic_source_sha256=sha(generic.read_bytes()), driver_source_sha256=sha(Path(__file__).read_bytes()),
                      scope='Only the repaired fixed subset, checked by generic integer 4x4 with complete modular filter; not maximum or maximality.')
        save(args.output/'geometry.json', report)
        save(args.output/'summary.json', dict(p=2539, trials=rows, best_size=best['size'], independently_safe=verified,
             upper_bound=1271, scope='A safe lower bound if geometry accepts; neither UNKNOWN pilot results nor local-search failure establishes nonattainment.'))
        print('GEOMETRY', verified, 'lower', best['size'], flush=True)
        if not verified:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
