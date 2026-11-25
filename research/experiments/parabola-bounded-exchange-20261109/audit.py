"""Regression for the deletion counter and evaluation of the saved SAT model."""
import argparse
import gzip
from itertools import product
import json
from pathlib import Path
from pysat.solvers import Cadical195
from search import build, encoding, removal_counter, sha, save, SNAPSHOT

HERE = Path(__file__).resolve().parent


def model_check(model, nv, clauses):
    assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
    positive = {v for v in model if v > 0}
    assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
    return positive


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    cases = 0
    for n in range(1, 7):
        variables = list(range(1, n+1))
        for bound in range(n+1):
            clauses, top = removal_counter(variables, bound, 100)
            assert top >= 100
            assert all(abs(v) in variables or abs(v) > 100 for c in clauses for v in c)
            with Cadical195(bootstrap_with=clauses) as solver:
                for flags in product((False, True), repeat=n):
                    assumptions = [v if flag else -v for v, flag in zip(variables, flags)]
                    assert solver.solve(assumptions=assumptions) == (flags.count(False) <= bound)
                    cases += 1
    saved = args.saved
    receipt = json.loads((saved/'result.json').read_text())
    seed_raw = Path(receipt['seed_path']).read_bytes()
    seed = list(map(int, seed_raw.split()[2:]))
    assert receipt['seed_sha256'] == sha(seed_raw)
    assert receipt['source_sha256'] == sha((HERE/'search.py').read_bytes())
    assert receipt['encoding_snapshot_sha256'] == sha(SNAPSHOT.read_bytes())
    clauses, nv, prior_top, point_vars = build(seed, receipt['target'], receipt['max_removed'])
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    assert cnf == gzip.decompress((saved/'input.cnf.gz').read_bytes())
    assert sha(cnf) == receipt['input_cnf_sha256']
    # Check reservation on actual appended clauses independently of worker's guard.
    base_len = len(encoding.encode(2647, 1323, [list(map(int, row.split()[:-1]))
        for row in encoding.BASE.read_text().splitlines() if row and row[0] not in 'cp'])[0])
    extra, extra_top = removal_counter(point_vars, receipt['max_removed'], prior_top)
    assert clauses[-len(extra):] == extra and extra_top == nv
    allowed = set(point_vars)
    assert all(abs(v) in allowed or prior_top < abs(v) <= nv for c in extra for v in c)
    assert all(abs(v) <= 3969 for c in clauses[:base_len] for v in c)
    model_raw = (saved/'model.json').read_bytes()
    model = json.loads(model_raw)['signed_model']
    positive = model_check(model, nv, clauses)
    points = sorted({0, 1323, 1324} | {i for i in range(1, 1323) if i in positive}
                    | {2647-i for i in range(1, 1323) if 1323+i in positive})
    raw = (saved/'candidate.txt').read_bytes()
    assert list(map(int, raw.split())) == [2647, len(points), *points]
    assert points == encoding.parameters(2647, 1323, positive)
    removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
    assert removed == receipt['removed'] and added == receipt['added']
    assert len(points) >= receipt['target'] and len(removed) <= receipt['max_removed']
    assert sum(v not in positive for v in point_vars) == len(removed)
    for bad in (model[:-1], [model[1]]+model[1:], [-v if abs(v) == 1 else v for v in model]):
        try:
            model_check(bad, nv, clauses)
        except AssertionError:
            pass
        else:
            raise AssertionError('invalid model accepted')
    # A fully fixed replay tests the same proof-enabled API without searching again.
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(100)
        assert solver.solve_limited(assumptions=model) is True
        replay = solver.get_model()
        model_check(replay, nv, clauses)
    geometry_raw = (saved/'geometry.json').read_bytes()
    geometry = json.loads(geometry_raw)
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert geometry['returncode'] == 0 and geometry['candidate_input_sha256'] == sha(raw)
    assert geometry['verifier_source_sha256'] == sha(generic.read_bytes())
    result = dict(counter_cases=cases, counter_reserved_top_verified=True, saved_input_byte_equal=True,
                  variables=nv, clauses=len(clauses), all_saved_model_clauses_satisfied=True,
                  decoded_points=len(points), removed=removed, added=added,
                  invalid_model_controls_rejected=3, fully_fixed_proof_enabled_replay=True,
                  input_cnf_sha256=sha(cnf), model_sha256=sha(model_raw), candidate_sha256=sha(raw),
                  geometry_receipt_sha256=sha(geometry_raw), source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Small deletion counter truth table; saved model evaluation and geometry receipt binding, not geometric replay or a global upper bound.')
    save(args.output/'audit.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
