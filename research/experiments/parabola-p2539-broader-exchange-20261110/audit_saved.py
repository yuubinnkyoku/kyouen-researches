"""Validate frozen inputs and any positive witness; do not certify negative search results."""
import argparse
import gzip
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import tempfile
from change_pair import HERE, FROZEN, build as changed_build, sha, save
from no_pair import build as no_pair_build

OLD = HERE.parent/'parabola-p2539-exchange-20261110/search.py'
spec = importlib.util.spec_from_file_location('previous_bounded_exchange', OLD)
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    edge_raw = gzip.decompress(args.edges.read_bytes())
    edges = [tuple(map(int, row.split())) for row in edge_raw.decode('ascii').splitlines()[1:]]
    rows = []
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-broader-input-audit-') as temporary:
        exe = Path(temporary)/'geometry.exe'
        for folder in sorted(args.saved.iterdir()):
            if not folder.is_dir():
                continue
            init = json.loads((folder/'init.json').read_text())
            result = json.loads((folder/'result.json').read_text())
            assert all(result[k] == value for k, value in init.items())
            assert sha(edge_raw) == init['edge_input_sha256']
            seed_raw = Path(init['seed_path']).read_bytes()
            assert sha(seed_raw) == init['seed_sha256']
            values = list(map(int, seed_raw.split()))
            p, n, seed = values[0], values[1], values[2:]
            assert p == 2539 and n == len(seed) and seed == sorted(set(seed))
            if 'd' in init:
                assert sha(OLD.read_bytes()) == init['source_sha256']
                assert sha(previous.TERNARY.read_bytes()) == init['ternary_source_sha256']
                assert sha(previous.PROJECTION.read_bytes()) == init['projection_source_sha256']
                clauses, nv, prior, _ = previous.build(p, init['d'], edges, seed, init['target'], init['max_removed'])
                assert prior == init['prior_top']
                mode, point_base = 'fixed-pair', None
            else:
                assert sha(FROZEN.read_bytes()) == init['frozen_source_sha256']
                if init['complete_pairs']:
                    assert sha((HERE/'change_pair.py').read_bytes()) == init['source_sha256']
                    builder, mode = changed_build, 'changed-pair'
                else:
                    assert sha((HERE/'no_pair.py').read_bytes()) == init['source_sha256']
                    assert sha((HERE/'change_pair.py').read_bytes()) == init['helper_source_sha256']
                    builder, mode = no_pair_build, 'no-pair'
                clauses, nv, point_base, base_nv, kept = builder(p, seed, edges, init['target'], init['max_removed'])
                assert (point_base, base_nv, kept) == (init['point_base'], init['base_nv'], init['geometric_clauses'])
            regenerated = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
            raw = gzip.decompress((folder/'input.cnf.gz').read_bytes())
            assert raw == regenerated and sha(raw) == init['input_sha256']
            assert (nv, len(clauses)) == (init['variables'], init['clauses'])
            row = dict(case=folder.name, mode=mode, status=result['status'], input_byte_rebuild=True,
                       input_sha256=sha(raw), verified_safe=False, independent_negative_proof='NOT_RUN')
            if result['status'] == 'SAT':
                signed = json.loads((folder/'model.json').read_text())['signed_model']
                assert len(signed) == nv and {abs(v) for v in signed} == set(range(1, nv+1))
                positive = {v for v in signed if v > 0}
                assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
                if mode == 'fixed-pair':
                    h, d = (p-1)//2, init['d']
                    points = sorted([0, d, p-d]+[t for i in range(1, h+1) if i != d
                                    for var, t in ((i, i), (h+i, p-i)) if var in positive])
                else:
                    points = [0]+[t for t in range(1, p) if point_base+t in positive]
                    pairs = [i for i in range(1, (p+1)//2) if i in points and p-i in points]
                    assert len(pairs) == init['complete_pairs']
                    if pairs:
                        assert pairs[0] != init['excluded_complete_pair']
                candidate = (folder/'candidate.txt').read_bytes()
                tokens = list(map(int, candidate.split()))
                assert tokens[:2] == [p, len(points)] and tokens[2:] == points
                assert len(set(seed)-set(points)) <= init['max_removed']
                assert len(points) >= init['target'] and sha(candidate) == result['candidate_sha256']
                if not exe.exists():
                    subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(exe)], check=True, timeout=60)
                r = subprocess.run([str(exe), '--modular-filter'], input=candidate, capture_output=True, timeout=120)
                assert r.returncode == 0 and list(map(int, r.stdout.split()))[:3] == [p, len(points), math.comb(len(points), 4)]
                row.update(verified_safe=True, size=len(points), geometry_stdout=r.stdout.decode(),
                           candidate_sha256=sha(candidate), generic_source_sha256=sha(generic.read_bytes()))
            else:
                assert not (folder/'model.json').exists() and not (folder/'candidate.txt').exists()
                if result['status'] == 'UNKNOWN' or init.get('proof_enabled') is False:
                    assert not (folder/'proof.drat.gz').exists()
            save(args.output/(folder.name+'.json'), row)
            rows.append(row)
            print('INPUT AUDIT', folder.name, row['status'], 'independently safe', row['verified_safe'], flush=True)
    positives = [r for r in rows if r['verified_safe']]
    save(args.output/'summary.json', dict(rows=rows, verified_best_size=max((r['size'] for r in positives), default=None),
         source_sha256=sha(Path(__file__).read_bytes()),
         scope='Frozen input and result provenance; negative solver results remain unaudited. Only positive witnesses passing integer geometry can strengthen a safe lower bound.'))


if __name__ == '__main__':
    main()
