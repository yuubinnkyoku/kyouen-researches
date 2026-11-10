"""Certify explicit blockers for the already audited best exchange witness."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-p2539-pair-pilot-20261110'
sys.path.insert(0, str(PRIOR))
from augment import blocker
from verify_saved import parse


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit', type=Path, required=True)
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    summary_raw = (args.audit/'summary.json').read_bytes()
    summary = json.loads(summary_raw)
    best = summary['best']
    case_raw = (args.audit/(best['case']+'.json')).read_bytes()
    assert json.loads(case_raw) == best and best['geometry_verified']
    generic = HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    assert sha(generic.read_bytes()) == summary['generic_source_sha256']
    candidate = (args.saved/best['case']/'candidate.txt').read_bytes()
    assert sha(candidate) == best['candidate_sha256']
    values = list(map(int, candidate.split()))
    p, n = values[:2]
    selected = set(values[2:])
    assert p == 2539 and n == len(selected)
    raw = gzip.decompress(args.edges.read_bytes())
    edges = [tuple(map(int, row.split())) for row in raw.decode('ascii').splitlines()[1:]]
    incidence = [[] for _ in range(p)]
    for q in edges:
        for t in q:
            incidence[t].append(q)
    rows = [(t, blocker(t, selected, incidence)) for t in range(p) if t not in selected]
    assert all(q is not None for t, q in rows), 'Witness has an unblocked addition; investigate it'
    proof = (f'{p} {n} {len(rows)}\n'+''.join(str(t)+' '+' '.join(map(str, q))+'\n' for t, q in rows)).encode('ascii')
    assert parse(candidate, proof)[:2] == (p, n)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'candidate.txt').write_bytes(candidate)
    (args.output/'blockers.txt').write_bytes(proof)
    report = dict(p=p, size=n, verified_safe_by_bound_receipt=True, verified_inclusion_maximal=True,
                  candidate_sha256=sha(candidate), blockers_sha256=sha(proof), missing_points=len(rows),
                  blocker_bareiss_zero_count=len(rows), geometry_summary_sha256=sha(summary_raw),
                  geometry_case_sha256=sha(case_raw), geometry_stdout=best['geometry_stdout'],
                  generic_source_sha256=sha(generic.read_bytes()), generator_source_sha256=sha((PRIOR/'augment.py').read_bytes()),
                  blocker_verifier_source_sha256=sha((PRIOR/'verify_saved.py').read_bytes()),
                  source_sha256=sha(Path(__file__).read_bytes()),
                  scope='Fixed witness safety bound to a fresh generic integer geometry receipt; all missing-point blockers checked by independent Bareiss. No exchange optimality or global maximum.')
    with (args.output/'verification.json').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(report, indent=2)+'\n')
    print('PASS maximal', n, 'with', len(rows), 'independent Bareiss blockers')


if __name__ == '__main__':
    main()
