"""Check the stored full model without SAT or the encoding generator."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check_model(model, nv, clauses, points):
    assert len(model) == nv
    assert {abs(v) for v in model} == set(range(1, nv+1))
    positive = {v for v in model if v > 0}
    assert all(any((v > 0) == (abs(v) in positive) for v in clause) for clause in clauses)
    selected = {0, 1323, 1324}
    for i in range(1, 1323):
        states = (i in positive, 1323+i in positive, 2646+i in positive)
        assert sum(states) == 1
        if states[0]:
            selected.add(i)
        if states[1]:
            selected.add(2647-i)
    assert selected == set(points)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    saved = HERE/'output/exchange-remove-at-most-two'
    raw = (saved/'candidate.txt').read_bytes()
    values = list(map(int, raw.split()))
    assert values[:2] == [2647, 1301] and values[2:] == sorted(set(values[2:]))
    assert sha(raw) == '1e02ea20ab61516d267887a7a31fa1b2aefd4aa9c305da403c60468da9bfc27b'
    assert raw == (HERE/'output/regression-seeded-1300/candidate.txt').read_bytes()
    cnf_path = HERE.parent/'parabola-warm-improvement-20261109/output/target1301-warm1300-budget500000/input.cnf.gz'
    cnf = gzip.decompress(cnf_path.read_bytes())
    assert sha(cnf) == '68ce0d6ace7d4a7ba59eebcd0ad63ab9dc35470fd12aae81e166f237b0139cf7'
    rows = cnf.decode('ascii').splitlines()
    nv, count = map(int, rows[0].split()[2:])
    assert [nv, count] == [35121, 122752]
    clauses = [list(map(int, row.split()[:-1])) for row in rows[1:]]
    assert len(clauses) == count
    model_raw = (HERE/'output/exchange-validation/completion-model.json').read_bytes()
    model = json.loads(model_raw)['signed_model']
    check_model(model, nv, clauses, values[2:])
    flipped = [-v if abs(v) == 1 else v for v in model]
    bad_models = [model[:-1], [model[1]]+model[1:], flipped]
    for bad in bad_models:
        try:
            check_model(bad, nv, clauses, values[2:])
        except AssertionError:
            pass
        else:
            raise AssertionError('invalid model accepted')
    geometry_raw = (saved/'geometry.json').read_bytes()
    geometry = json.loads(geometry_raw)
    assert geometry['returncode'] == 0 and geometry['candidate_input_sha256'] == sha(raw)
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert geometry['verifier_source_sha256'] == sha(generic.read_bytes())
    assert geometry['stdout'].split() == ['2647', '1301', '118821013025', '44971096']
    for folder, source in [('exchange-remove-at-most-two', 'exchange.py'),
                           ('exchange-from1301', 'exchange_seeded.py'),
                           ('regression-seeded-1300', 'exchange_seeded.py'),
                           ('exchange-validation', 'verify_exchange.py')]:
        name = 'validation.json' if folder == 'exchange-validation' else 'result.json'
        receipt = json.loads((HERE/'output'/folder/name).read_text())
        assert receipt['source_sha256'] == sha((HERE/source).read_bytes())
    result = dict(candidate_sha256=sha(raw), input_cnf_sha256=sha(cnf),
                  saved_model_sha256=sha(model_raw), geometry_receipt_sha256=sha(geometry_raw),
                  variables=nv, clauses=count, all_clauses_satisfied=True,
                  decoded_points=1301, seeded_regression_byte_equal=True,
                  invalid_model_controls_rejected=len(bad_models),
                  source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Stored model evaluation without solver/encoding imports; geometry receipt binding, not geometric replay.')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
