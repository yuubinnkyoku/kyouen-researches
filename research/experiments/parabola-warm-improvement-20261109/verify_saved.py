"""Reconstruct saved inputs, check complete SAT models and geometry receipts."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
from pysat.card import CardEnc, EncType
from encoding_snapshot import BASE, BASE_SHA, encode, parameters

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    snapshot = (HERE/'encoding_snapshot.py').read_bytes()
    assert snapshot == (HERE.parent/'parabola-ternary-selection-20261109/ternary.py').read_bytes()
    raw = BASE.read_bytes()
    assert sha(raw) == BASE_SHA
    original = [list(map(int, row.split()[:-1])) for row in raw.decode('ascii').splitlines() if row and row[0] not in 'cp']
    records = []
    for path in sorted((HERE/'output').glob('target*')):
        init = json.loads((path/'init.json').read_text())
        result = json.loads((path/'result.json').read_text())
        assert init['worker_source_sha256'] == sha((HERE/'improve.py').read_bytes())
        assert init['encoding_snapshot_sha256'] == sha(snapshot)
        assert init['base_cnf_sha256'] == BASE_SHA
        warm_raw = Path(init['warm_source']).read_bytes()
        assert sha(warm_raw) == init['warm_input_sha256']
        warm = list(map(int, warm_raw.split()))
        assert warm[1] == len(warm)-2 == init['warm_size'] < init['target']
        clauses, empties = encode(2647, 1323, original)
        card = CardEnc.atmost(empties, bound=1325-init['target'], top_id=3969, encoding=EncType.seqcounter)
        clauses += card.clauses
        nv = max(3969, card.nv)
        cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
        assert cnf == gzip.decompress((path/'input.cnf.gz').read_bytes())
        assert sha(cnf) == init['encoded_cnf_sha256'] == result['encoded_cnf_sha256']
        row = dict(case=path.name, status=result['status'], variables=nv, clauses=len(clauses), input_sha256=sha(cnf))
        if result['status'] == 'SAT':
            model = json.loads((path/'model.json').read_text())['signed_model']
            assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
            positive = {v for v in model if v > 0}
            assert all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
            points = parameters(2647, 1323, positive)
            candidate = list(map(int, (path/'candidate.txt').read_bytes().split()))
            assert candidate[:2] == [2647, len(points)] and candidate[2:] == points
            assert len(points) == result['size'] >= init['target']
            geometry = json.loads((path/'geometry.json').read_text())
            assert geometry['returncode'] == 0
            assert geometry['candidate_input_sha256'] == sha((path/'candidate.txt').read_bytes())
            assert geometry['verifier_source_sha256'] == sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes())
            p, size, covered, checked = map(int, geometry['stdout'].split())
            assert (p, size, covered) == (2647, len(points), math.comb(len(points), 4))
            row.update(size=size, all_model_clauses_satisfied=True, independent_geometry_verified=True,
                       covered_quadruples=covered, modular_candidates=checked)
        else:
            assert result['status'] == 'UNKNOWN'
            assert not (path/'candidate.txt').exists() and not (path/'model.json').exists()
            row.update(nonexistence_claim=False)
        records.append(row)
    report = dict(records=records, all_checks_passed=True,
                  unchanged_encoding_snapshot_sha256=sha(snapshot),
                  scope='Saved CNF/model/hash and independent geometry receipt validation; no solver reruns or UNSAT proof claims.')
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
