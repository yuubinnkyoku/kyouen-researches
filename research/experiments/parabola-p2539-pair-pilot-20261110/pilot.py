"""Bounded fixed-pair pilot; only independently checked SAT establishes equality."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
GEN = HERE.parent/'structural-lemmas-2026-10-02/checks/parabola_half_bound.py'
sys.path.insert(0, str(GEN.parent))
from parabola_half_bound import clauses_for_pair


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2)+'\n')


def candidate(d, positive, p=2539):
    return sorted([0, d, p-d]+[p-i if i in positive else i for i in range(1, (p+1)//2) if i != d])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', type=Path)
    ap.add_argument('--edges', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--ds', default='1,127,253,379,505,631,757,883,1009,1135,1203,1237')
    ap.add_argument('--budget', type=int, default=100000)
    args = ap.parse_args()
    assert (args.cache is None) != (args.edges is None)
    ds = list(map(int, args.ds.split(',')))
    assert ds and len(ds) == len(set(ds)) and all(1 <= d <= 1269 for d in ds) and args.budget > 0
    if args.cache:
        raw = args.cache.read_bytes()
        full = [tuple(map(int, row.split())) for row in raw.decode('ascii').splitlines()]
        assert len(full) == 843414 and all(len(q) == 4 and tuple(sorted(set(q))) == q and 0 <= q[0] < q[-1] < 2539 for q in full)
        edges = sorted({q for q in full if len({min(t, 2539-t) for t in q}) == 4})
        origin = dict(cache_path=str(args.cache), cache_sha256=sha(raw), original_edges=len(full))
        del full, raw
    else:
        raw = gzip.decompress(args.edges.read_bytes()); lines = raw.decode('ascii').splitlines()
        assert lines[0] == '2539 38868'
        edges = [tuple(map(int, row.split())) for row in lines[1:]]
        origin = dict(reused_edge_artifact=str(args.edges), reused_sha256=sha(raw))
    assert len(edges) == 38868 and edges == sorted(set(edges))
    args.output.mkdir(parents=True, exist_ok=False)
    edge_input = ('2539 38868\n'+''.join(' '.join(map(str, q))+'\n' for q in edges)).encode('ascii')
    (args.output/'edges.txt.gz').write_bytes(gzip.compress(edge_input, mtime=0))
    save(args.output/'plan.json', dict(p=2539, h=1269, target_size=1271, requested_d=ds, conflict_budget=args.budget,
         edge_input_sha256=sha(edge_input), source_sha256=sha(Path(__file__).read_bytes()),
         projection_source_sha256=sha(GEN.read_bytes()), python_sat=importlib.metadata.version('python-sat'), origin=origin,
         scope='Bounded fixed-pair cases. UNKNOWN and absent witnesses do not establish nonattainment.'))
    from pysat.solvers import Cadical195
    results, attained = [], False
    with tempfile.TemporaryDirectory(prefix='p2539-pair-pilot-') as directory:
        directory = Path(directory)
        wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
        generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
        ge, subset = directory/'edges.exe', directory/'subset.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(ge)], check=True, timeout=60)
        subprocess.run(['g++', '-O2', '-std=c++17', str(generic), '-o', str(subset)], check=True, timeout=60)
        ep = directory/'edges.txt'; ep.write_bytes(edge_input)
        r = subprocess.run([str(ge), str(ep)], capture_output=True, text=True, timeout=60)
        save(args.output/'geometry-edges.json', dict(returncode=r.returncode, stdout=r.stdout, stderr=r.stderr,
             edge_input_sha256=sha(edge_input), wrapper_source_sha256=sha(wrapper.read_bytes()), generic_source_sha256=sha(generic.read_bytes())))
        assert r.returncode == 0 and r.stdout.strip() == 'VERIFIED_EDGES 2539 38868'
        for name, raw, rc in [('three', b'5 3\n0 1 2\n', 0), ('two-pairs', b'5 4\n1 2 3 4\n', 4)]:
            r = subprocess.run([str(subset), '--modular-filter'], input=raw, capture_output=True, timeout=10)
            assert r.returncode == rc, name
        for d in ds:
            folder = args.output/f'd{d}'; folder.mkdir()
            clauses = sorted({tuple(sorted(c)) for c in clauses_for_pair(2539, edges, d)})
            cnf = (f'p cnf 1269 {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
            (folder/'input.cnf.gz').write_bytes(gzip.compress(cnf, mtime=0))
            started = time.monotonic()
            with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
                solver.conf_budget(args.budget)
                answer = solver.solve_limited()
                model = solver.get_model() if answer is True else None
                proof = solver.get_proof()
                statistics = solver.accum_stats()
            record = dict(p=2539, d=d, solver='SAT' if answer is True else 'UNSAT' if answer is False else 'UNKNOWN',
                          elapsed_seconds=time.monotonic()-started, statistics=statistics, input_sha256=sha(cnf),
                          clauses=len(clauses), independently_safe=False)
            if proof:
                raw = ('\n'.join(proof)+'\n').encode('ascii')
                (folder/'solver-proof.drat.gz').write_bytes(gzip.compress(raw, mtime=0))
                record.update(proof_sha256=sha(raw), proof_lines=len(proof), proof_complete=answer is False,
                              proof_status='SOLVER_OUTPUT_NOT_INDEPENDENTLY_CHECKED')
            if model is not None:
                positive = {lit for lit in model if lit > 0}
                assert all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
                save(folder/'model.json', dict(signed_model=model, full_clause_check=True))
                points = candidate(d, positive)
                assert len(points) == len(set(points)) == 1271
                raw = ('2539 1271\n'+' '.join(map(str, points))+'\n').encode('ascii')
                (folder/'candidate.txt').write_bytes(raw)
                started = time.monotonic()
                r = subprocess.run([str(subset), '--modular-filter'], input=raw, capture_output=True, timeout=120)
                accepted = r.returncode == 0
                if accepted:
                    values = list(map(int, r.stdout.split()))
                    assert len(values) == 4 and values[:3] == [2539, 1271, math.comb(1271, 4)]
                save(folder/'geometry.json', dict(returncode=r.returncode, stdout=r.stdout.decode(), stderr=r.stderr.decode(),
                     elapsed_seconds=time.monotonic()-started, candidate_sha256=sha(raw),
                     generic_source_sha256=sha(generic.read_bytes()), verified=accepted,
                     scope='Generic integer 4x4 with complete modular filter; no CNF or cached edge dependence.'))
                record.update(independently_safe=accepted, candidate_sha256=sha(raw))
                attained = attained or accepted
            save(folder/'result.json', record)
            results.append(record)
            print('d', d, record['solver'], 'geometry', record['independently_safe'], flush=True)
            if attained:
                break
    save(args.output/'summary.json', dict(p=2539, target_size=1271, attained=attained,
         completed_d=[r['d'] for r in results], pending_d=ds[len(results):],
         solver_unsat_d=[r['d'] for r in results if r['solver']=='UNSAT'], unknown_d=[r['d'] for r in results if r['solver']=='UNKNOWN'],
         independently_safe_d=[r['d'] for r in results if r['independently_safe']],
         scope='Only independently checked SAT establishes attainment. UNSAT remains solver-only; no all-d exclusion claimed.'))


if __name__ == '__main__':
    main()
