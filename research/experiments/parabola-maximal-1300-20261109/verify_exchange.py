"""Bind the saved exchange to geometry and complete the former UNKNOWN CNF."""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
WARM = HERE.parent/'parabola-warm-improvement-20261109'
spec = importlib.util.spec_from_file_location('ternary_encoding', WARM/'encoding_snapshot.py')
encoding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(encoding)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    saved = HERE/'output/exchange-remove-at-most-two'
    proposal = json.loads((saved/'result.json').read_text())
    assert proposal['source_sha256'] == sha((HERE/'exchange.py').read_bytes())
    seed_raw = (WARM/'output/target1299-warm1298-budget500000/candidate.txt').read_bytes()
    seed = set(map(int, seed_raw.split()[2:]))
    assert sha(seed_raw) == proposal['seed_sha256']
    raw = (saved/'candidate.txt').read_bytes()
    values = list(map(int, raw.split()))
    points = values[2:]
    assert values[:2] == [2647, 1301] and points == sorted(set(points))
    assert set(points) == (seed-set(proposal['removed'])) | set(proposal['added'])
    assert len(proposal['removed']) == 2 and len(proposal['added']) == 3
    geometry = json.loads((saved/'geometry.json').read_text())
    assert geometry['returncode'] == 0 and geometry['candidate_input_sha256'] == sha(raw)
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert geometry['verifier_source_sha256'] == sha(generic.read_bytes())
    prior = WARM/'output/target1301-warm1300-budget500000'
    init = json.loads((prior/'init.json').read_text())
    cnf = gzip.decompress((prior/'input.cnf.gz').read_bytes())
    assert sha(cnf) == init['encoded_cnf_sha256']
    rows = cnf.decode('ascii').splitlines()
    nv, count = map(int, rows[0].split()[2:])
    clauses = [list(map(int, row.split()[:-1])) for row in rows[1:]]
    assert len(clauses) == count
    assumptions = encoding.phases(2647, 1323, points)
    start = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.conf_budget(10000)
        answer = solver.solve_limited(assumptions=assumptions)
        assert answer is True, 'point-fixed candidate did not extend to a CNF model'
        model = solver.get_model()
        stats = solver.accum_stats()
    assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
    positive = {v for v in model if v > 0}
    assert all(any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in clauses)
    assert encoding.parameters(2647, 1323, positive) == points
    assert all((lit > 0) == (abs(lit) in positive) for lit in assumptions)
    (args.output/'completion-model.json').write_text(json.dumps({'signed_model': model}, indent=2)+'\n', encoding='utf-8', newline='\n')
    local = json.loads((HERE/'output/exchange-from1301/result.json').read_text())
    assert local['source_sha256'] == sha((HERE/'exchange_seeded.py').read_bytes())
    assert local['seed_sha256'] == sha(raw) and local['status'] == 'NO_PROJECTED_IMPROVEMENT_FOUND'
    assert not (HERE/'output/exchange-from1301/candidate.txt').exists()
    result = dict(p=2647, size=1301, removed=proposal['removed'], added=proposal['added'],
                  candidate_input_sha256=sha(raw), input_cnf_sha256=sha(cnf), variables=nv, clauses=count,
                  all_model_clauses_satisfied=True, decoded_points_match=True, independent_geometry_verified=True,
                  geometry_receipt_sha256=sha((saved/'geometry.json').read_bytes()),
                  fully_fixed_point_assumptions=len(assumptions), statistics=stats,
                  completion_seconds=time.monotonic()-start, python_sat=importlib.metadata.version('python-sat'),
                  source_sha256=sha(Path(__file__).read_bytes()),
                  next_search_status=local['status'], next_search_nonexistence_claim=False,
                  scope='Point-fixed model completion and independent geometry receipt binding. No unrestricted SAT rerun or global upper bound.')
    (args.output/'validation.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
