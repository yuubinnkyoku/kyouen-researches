#!/usr/bin/env python3
"""Audit a saved model and geometry receipt without rerunning the solver."""
import argparse
import gzip
import hashlib
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'parabola-ternary-selection-20261109'
VERIFIER = HERE.parent / 'parabola-local-repair-20261109/verify_subset.cpp'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check(directory):
    result = json.loads((directory / 'result.json').read_text())
    init = json.loads((directory / 'init.json').read_text())
    for key, value in init.items():
        assert result[key] == value, key
    assert result['p'] == 2647 and result['d'] == 1323 and result['status'] == 'SAT'
    if result['worker_sha256'] == digest((HERE / 'probe.py').read_bytes()):
        warm = PREVIOUS / 'output/target1293-budget100000/candidate.txt'
    elif result['worker_sha256'] == digest((HERE / 'probe_1298.py').read_bytes()):
        warm = HERE / 'output/control-target1296/candidate.txt'
    elif result['worker_sha256'] == digest((HERE / 'probe_from_witness.py').read_bytes()):
        repo = HERE.parents[2].resolve()
        warm = (repo / result['warm_source']).resolve()
        assert warm.is_relative_to(repo)
    else:
        raise AssertionError('unknown worker hash')
    assert result['encoder_sha256'] == digest((PREVIOUS / 'ternary.py').read_bytes())
    assert result['warm_input_sha256'] == digest(warm.read_bytes())
    raw = gzip.decompress((directory / 'input.cnf.gz').read_bytes())
    assert result['encoded_cnf_sha256'] == digest(raw)
    lines = raw.decode('ascii').splitlines()
    head = lines[0].split()
    assert head == ['p', 'cnf', str(result['variables']), str(result['clauses'])]
    model = json.loads((directory / 'model.json').read_text())['signed_model']
    assert len(model) == result['variables']
    assert {abs(v) for v in model} == set(range(1, result['variables'] + 1))
    positive = {v for v in model if v > 0}
    assert len(lines) - 1 == result['clauses']
    for row in lines[1:]:
        lits = list(map(int, row.split()))
        assert lits[-1] == 0 and all(0 < abs(v) <= result['variables'] for v in lits[:-1])
        assert any((lit > 0) == (abs(lit) in positive) for lit in lits[:-1])
    raw_candidate = (directory / 'candidate.txt').read_bytes()
    candidate = list(map(int, raw_candidate.split()))
    p, n, *selected = candidate
    assert p == 2647 and n == result['size'] and n == len(selected) and n >= result['target']
    assert selected == sorted(set(selected)) and all(0 <= x < p for x in selected)
    assert {0, 1323, 1324} <= set(selected)
    expected = {0, 1323, 1324}
    empties = []
    for i in range(1, 1323):
        low, high, empty = (i in positive, 1323 + i in positive, 2646 + i in positive)
        assert sum((low, high, empty)) == 1
        if low: expected.add(i)
        if high: expected.add(p - i)
        if empty: empties.append(i)
    assert expected == set(selected) and empties == result['empty_pairs']
    assert n == 1325-len(empties) and len(empties) <= result['empty_bound']
    geometry = json.loads((directory/'geometry.json').read_text())
    assert geometry['returncode'] == 0
    assert geometry['candidate_input_sha256'] == digest(raw_candidate)
    assert geometry['verifier_source_sha256'] == digest(VERIFIER.read_bytes())
    output = list(map(int, geometry['stdout'].split()))
    assert output[:3] == [2647, n, comb(n, 4)] and 0 <= output[3] <= output[2]
    print(f'PASS: {n} points, {len(empties)} empty pairs, {result["clauses"]} clauses, '
          f'{output[2]} covered quadruples, {output[3]} integer determinants')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    check(parser.parse_args().directory)
