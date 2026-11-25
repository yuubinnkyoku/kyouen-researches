"""Independently project saved edges and bind LRAT receipts and coverage."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRIM = HERE.parent/'parabola-drat-trim-20261109'
OLD = HERE.parent/'parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2531_34249932790a9e9d.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    coverage = json.loads((args.saved/'coverage.json').read_text())
    baseline_raw = OLD.read_bytes()
    old = {r['d'] for r in json.loads(baseline_raw)['records']
           if r['verified'] and r['checker_rc'] == 0 and r['solver'] == 'UNSAT'}
    assert len(old) == 143 and sha(baseline_raw) == coverage['baseline_sha256']
    edge_raw = gzip.decompress((args.saved/'edges.txt.gz').read_bytes())
    rows = edge_raw.decode('ascii').splitlines()
    p, n = map(int, rows[0].split())
    edges = [tuple(map(int, row.split())) for row in rows[1:]]
    assert p == 2531 and len(edges) == n == 837640
    geometric = json.loads((args.saved/'geometry.json').read_text())
    assert geometric['returncode'] == 0 and geometric['input_sha256'] == sha(edge_raw)
    assert geometric['stdout'].strip() == f'VERIFIED_EDGES {p} {n}'
    assert geometric['wrapper_sha256'] == sha((HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp').read_bytes())
    assert geometric['generic_sha256'] == sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes())
    records = []
    for d in coverage['new_lrat_verified_d']:
        directory = args.saved/f'd{d}'
        receipt = json.loads((directory/'result.json').read_text())
        assert receipt['verified'] and receipt['solver'] == 'UNSAT' and receipt['d'] == d
        assert receipt['source_sha256'] == sha((HERE/'audit.py').read_bytes())
        cnf = gzip.decompress((directory/'input.cnf.gz').read_bytes())
        proof = gzip.decompress((directory/'proof.drat.gz').read_bytes())
        lrat = gzip.decompress((directory/'core.lrat.gz').read_bytes())
        assert sha(cnf) == receipt['input_sha256'] and sha(proof) == receipt['proof_sha256']
        assert sha(lrat) == receipt['lrat_sha256'] and len(lrat) == receipt['lrat_raw_bytes']
        lines = cnf.decode('ascii').splitlines()
        assert lines[0] == f"p cnf 1265 {receipt['clauses']}"
        actual = set()
        for line in lines[1:]:
            literals = tuple(map(int, line.split()))
            assert literals[-1] == 0 and all(0 < abs(v) <= 1265 and abs(v) != d for v in literals[:-1])
            actual.add(tuple(sorted(literals[:-1])))
        assert len(actual) == len(lines)-1 == receipt['clauses']
        expected = set()
        fixed = {0, d, p-d}
        for edge in edges:
            signs = set()
            for t in edge:
                if t not in fixed:
                    signs.add(t if t <= 1265 else t-p)
            if not any(-v in signs for v in signs):
                expected.add(tuple(sorted(signs)))
        assert actual == expected
        for name, marker in [('trim','s VERIFIED'), ('lrat','c VERIFIED')]:
            assert receipt[name]['returncode'] == 0 and receipt[name]['verified']
            assert marker in receipt[name]['stdout'].splitlines()
        assert receipt['trim_source_sha256'] == sha((TRIM/'vendor/drat-trim.c').read_bytes())
        assert receipt['fixed_lrat_source_sha256'] == sha((TRIM/'lrat-check-empty-fixed.c').read_bytes())
        records.append(dict(d=d, variables=1265, clauses=len(actual), lrat_sha256=sha(lrat), verified=True))
    new = {r['d'] for r in records}
    assert new == {82,83,84,85} and not old & new
    assert coverage['verified_d_union'] == sorted(old|new) and coverage['verified_union_count'] == 147
    assert coverage['remaining'] == 1118
    result = dict(p=p, checked_edges=n, independent_projection_schema=True, all_saved_hashes_match=True,
                  baseline_fixed_count=143, new_lrat_d=sorted(new), verified_union_count=147, remaining=1118,
                  records=records, source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Stored proof/receipt and independent projection-schema verification. Geometry and LRAT were executed by audit.py. Mixed methods, not a completed all-d audit.')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
