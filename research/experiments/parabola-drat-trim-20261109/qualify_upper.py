"""Bind four proof receipts to the repaired shape inputs and clause schemas."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-size1323-drat-20261109'
RUP = HERE.parent/'parabola-monotone-rup-20261109'
ROOT = HERE.parents[2]
SHAPES = ('000', '011', '101', '112')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lrat-result', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    schema_raw = (RUP/'output/encoding-audit-reservation.json').read_bytes()
    schema = json.loads(schema_raw)
    assert schema['p'] == 2647 and schema['excluded_size'] == 1323
    assert schema['all_four_clause_schemas_match']
    assert {r['shape'] for r in schema['records']} == set(SHAPES) and len(schema['records']) == 4
    edge_raw = gzip.decompress((HERE.parent/'parabola-hplus1-drat-20261109/input/verified_edges.txt.gz').read_bytes())
    edge = schema['provided_edges_geometry']
    assert edge['returncode'] == 0 and edge['stdout'].strip() == 'VERIFIED_EDGES 2647 53886'
    assert edge['edge_input_sha256'] == sha(edge_raw)
    assert edge['wrapper_sha256'] == sha((HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp').read_bytes())
    assert edge['included_verifier_sha256'] == sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes())
    regression = json.loads((RUP/'output/regression.json').read_text())
    assert regression['source_sha256'] == sha((RUP/'rup_check.cpp').read_bytes())
    assert regression['passed'] == len(regression['cases']) == 516
    assert all((c['returncode'] == 0) == c['expected'] for c in regression['cases'])
    controls = json.loads((HERE/'output/lrat-controls.json').read_text())
    assert controls['source_sha256']['empty-fixed'] == sha((HERE/'lrat-check-empty-fixed.c').read_bytes())
    assert all(c['results']['empty-fixed']['accepted'] == c['expected'] for c in controls['cases'])
    records = []
    for key in SHAPES:
        location = PRIOR/'output'/('fixed' if key in ('000', '101') else '')/f'shape-{key}'
        cnf = gzip.decompress((location/'input.cnf.gz').read_bytes())
        solver = json.loads((location/'solver.json').read_text())
        shape_schema = next(r for r in schema['records'] if r['shape'] == key)
        assert sha(cnf) == solver['input_sha256'] == shape_schema['input_sha256']
        assert shape_schema['full_clause_schema_match'] and shape_schema['auxiliary_ranges_disjoint_and_reserved']
        if key != '112':
            receipt_path = RUP/'output'/f'audit-shape-{key}.json'
            receipt = json.loads(receipt_path.read_text())
            proof = gzip.decompress((location/'proof.drat.gz').read_bytes())
            assert receipt['input_sha256'] == sha(cnf)
            assert receipt['proof_sha256'] == solver['proof_sha256'] == sha(proof)
            assert receipt['checker_source_sha256'] == regression['source_sha256']
            good = (receipt['verified'] is True and receipt['returncode'] == 0
                    and not receipt['timed_out'] and receipt['stdout'].splitlines()[-1:] == ['RUP_VERIFIED'])
            proof_hash = receipt['proof_sha256']
            method = 'deletion-erased RUP, RAT forbidden'
        else:
            receipt_path = args.lrat_result
            receipt = json.loads(receipt_path.read_text())
            assert (receipt['p'], receipt['excluded_size'], receipt['shape']) == (2647, 1323, '112')
            assert receipt['input_sha256'] == sha(cnf)
            assert receipt['checker_source_sha256'] == controls['source_sha256']['empty-fixed']
            assert receipt['schema_receipt_sha256'] == sha(schema_raw)
            assert receipt['driver_source_sha256'] == sha((HERE/'replay_lrat_stream.py').read_bytes())
            manifest = json.loads((HERE/'output/lrat-core-preserved-manifest.json').read_text())
            assert manifest['receipt_sha256'] == sha(receipt_path.read_bytes())
            for field in ('proof_raw_sha256', 'proof_raw_bytes', 'proof_lines'):
                assert receipt[field] == manifest[field]
            preflight = json.loads((receipt_path.parent/'preflight.json').read_text())
            for field, value in preflight.items():
                assert receipt[field] == value
            good = (receipt['verified'] is True and receipt['returncode'] == 0
                    and not receipt['timed_out'] and 'c VERIFIED' in receipt['stdout'].splitlines())
            proof_hash = receipt['proof_raw_sha256']
            method = 'LRAT hints, K0714 empty-clause fix'
        records.append(dict(shape=key, input_sha256=sha(cnf), method=method, verified=good,
                            proof_sha256=proof_hash, receipt_path=receipt_path.resolve().relative_to(ROOT).as_posix(),
                            receipt_sha256=sha(receipt_path.read_bytes())))
    complete = all(r['verified'] for r in records)
    result = dict(p=2647, excluded_size=1323, all_four_verified=complete,
                  independent_upper_bound=1322 if complete else None, records=records,
                  schema_receipt_sha256=sha(schema_raw),
                  encoding_audit_source_sha256=sha((RUP/'encoding_audit.py').read_bytes()),
                  scope='Receipt/hash/schema qualification, not a replay of all four proofs or a Lean proof.',
                  availability='The 112 LRAT proof is local evidence, not distributed in Git; see the proof manifest.')
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
