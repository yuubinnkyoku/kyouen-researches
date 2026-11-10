"""Rebuild inputs, check full models, independently decode, and verify integer geometry."""
import argparse
import gzip
import json
import math
from pathlib import Path
import subprocess
import tempfile
from search import HERE, TERNARY, PROJECTION, build, save, sha


def check_model(nv, clauses, model):
    assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
    assert all(type(v) is int for v in model)
    positive = {v for v in model if v > 0}
    assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
    return positive


def decode(p, d, positive):
    h = (p-1)//2
    points = [0, d, p-d]
    for i in range(1, h+1):
        if i != d:
            low, high, empty = [v in positive for v in (i, h+i, 2*h+i)]
            assert sum((low, high, empty)) == 1
            if low:
                points.append(i)
            if high:
                points.append(p-i)
    return sorted(points)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    edge_raw = gzip.decompress(args.edges.read_bytes())
    edges = [tuple(map(int, row.split())) for row in edge_raw.decode('ascii').splitlines()[1:]]
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    rows = []
    with tempfile.TemporaryDirectory(prefix='p2539-exchange-audit-') as directory:
        exe = Path(directory)/'subset.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(exe)], check=True, timeout=60)
        for folder in sorted(args.saved.glob('target*-remove*')):
            init = json.loads((folder/'init.json').read_text())
            result = json.loads((folder/'result.json').read_text())
            assert all(result[k] == v for k, v in init.items())
            assert sha((HERE/'search.py').read_bytes()) == init['source_sha256']
            assert sha(TERNARY.read_bytes()) == init['ternary_source_sha256']
            assert sha(PROJECTION.read_bytes()) == init['projection_source_sha256']
            assert sha(edge_raw) == init['edge_input_sha256']
            seed_raw = Path(init['seed_path']).read_bytes()
            assert sha(seed_raw) == init['seed_sha256']
            seed_tokens = list(map(int, seed_raw.split()))
            p, d = init['p'], init['d']
            assert seed_tokens[:2] == [p, len(seed_tokens)-2]
            seed = seed_tokens[2:]
            clauses, nv, prior_top, seed_vars = build(p, d, edges, seed, init['target'], init['max_removed'])
            regenerated = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
            cnf = gzip.decompress((folder/'input.cnf.gz').read_bytes())
            assert cnf == regenerated and sha(cnf) == init['input_sha256']
            assert (nv, prior_top, len(seed_vars)) == (init['variables'], init['prior_top'], init['seed_literals'])
            row = dict(case=folder.name, p=p, d=d, status=result['status'], input_sha256=sha(cnf),
                       input_byte_rebuild=True, geometry_verified=False)
            if result['status'] == 'SAT':
                model_raw = (folder/'model.json').read_bytes()
                model = json.loads(model_raw)['signed_model']
                positive = check_model(nv, clauses, model)
                points = decode(p, d, positive)
                raw = (folder/'candidate.txt').read_bytes()
                tokens = list(map(int, raw.split()))
                assert tokens[:2] == [p, len(points)] and tokens[2:] == points
                assert len(points) >= init['target'] and len(set(points)) == len(points)
                removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
                assert len(removed) <= init['max_removed'] and removed == result['removed'] and added == result['added']
                assert sha(raw) == result['candidate_sha256']
                run = subprocess.run([str(exe), '--modular-filter'], input=raw, capture_output=True, timeout=120)
                assert run.returncode == 0, run.stdout+run.stderr
                values = list(map(int, run.stdout.split()))
                assert len(values) == 4 and values[:3] == [p, len(points), math.comb(len(points), 4)]
                row.update(size=len(points), geometry_verified=True, geometry_stdout=run.stdout.decode(),
                           candidate_sha256=sha(raw), model_sha256=sha(model_raw), all_clauses_checked=True,
                           removed=removed, added=added)
            else:
                assert not (folder/'model.json').exists() and not (folder/'candidate.txt').exists()
                if (folder/'proof.drat.gz').exists():
                    raw = gzip.decompress((folder/'proof.drat.gz').read_bytes())
                    assert sha(raw) == result['proof_sha256']
                row['independent_proof_audit'] = 'NOT_RUN'
            save(args.output/(folder.name+'.json'), row)
            rows.append(row)
            print('AUDIT', folder.name, result['status'], row.get('size'), flush=True)
        controls = []
        for name, raw, code in [('safe-three', b'5 3\n0 1 2\n', 0),
                                ('forbidden', b'5 4\n1 2 3 4\n', 4),
                                ('duplicate', b'5 3\n0 1 1\n', 3)]:
            run = subprocess.run([str(exe), '--modular-filter'], input=raw, capture_output=True, timeout=10)
            assert run.returncode == code
            controls.append(dict(name=name, expected=code, actual=run.returncode))
    positives = [row for row in rows if row['geometry_verified']]
    assert positives
    best = max(positives, key=lambda row: row['size'])
    save(args.output/'summary.json', dict(rows=rows, best=best, upper_bound=1271,
         generic_source_sha256=sha(generic.read_bytes()), audit_source_sha256=sha(Path(__file__).read_bytes()),
         search_source_sha256=sha((HERE/'search.py').read_bytes()), controls=controls,
         scope='Independently geometrically verified fixed positive witnesses; negative results are solver-only and restricted. No maximality or maximum is inferred.'))


if __name__ == '__main__':
    main()
