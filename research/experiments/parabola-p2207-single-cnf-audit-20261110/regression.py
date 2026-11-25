"""Exhaustive small semantic checks and corruption controls for the schema."""
import argparse
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile
from schema import structural, parse, audit as audit_schema
from audit import HERE, SAVED, save, sha


def dimacs(variables, clauses):
    return (f'p cnf {variables} {len(clauses)}\n'+''.join(
        ' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    rows = []
    for p in (5, 7, 11):
        h = (p-1)//2
        clauses, nv, base = structural(p)
        cases = accepted = 0
        for states in product(range(4), repeat=h):
            fixed = {4*i+state+1 for i, state in enumerate(states)}
            fixed.update(base+t for t in range(1, p)
                         if states[min(t, p-t)-1] in (0, 2 if t <= h else 3))
            expected = states.count(0) == 1 and 1 not in states
            possible = False
            for bits in range(1 << (h-1)):
                positive = fixed | {4*h+i+1 for i in range(h-1) if bits >> i & 1}
                if all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses):
                    possible = True
                    break
            assert possible == expected, (p, states)
            cases += 1
            accepted += possible
        assert accepted == h*2**(h-1)
        rows.append(dict(p=p, state_assignments=cases, accepted_classes=accepted))
    raw = (SAVED/'a2207_1105.cnf').read_bytes()
    nv, clauses = parse(raw)
    edges, schema = audit_schema(raw)
    mutants = {'missing-one-hot': dimacs(nv, clauses[1:]),
               'stray-positive-unit': dimacs(nv, clauses+[(nv,)]),
               'bad-selector-geometry': dimacs(nv, clauses[:-1]+[(-1, -2, -3)]),
               'duplicate-point-geometry': dimacs(nv, clauses[:-1]+[(-7720, -7720, -7719)]),
               'truncated-clause-count': raw.rsplit(b'\n', 2)[0]+b'\n'}
    point_clause = next(i for i, c in enumerate(clauses) if 5515 in c and -1 in c)
    altered = list(clauses)
    altered[point_clause] = tuple(4412 if x == 5515 else x for x in altered[point_clause])
    mutants['point-selector-alias'] = dimacs(nv, altered)
    rejected = []
    for name, candidate in mutants.items():
        try:
            audit_schema(candidate)
        except (AssertionError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError(name)
    altered = list(clauses)
    altered[-1] = (-5515, -5516, -5517)
    changed_edges, _ = audit_schema(dimacs(nv, altered))
    assert (0, 1, 2, 3) in changed_edges
    wrapper = HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp'
    with tempfile.TemporaryDirectory(prefix='p2207-schema-controls-') as directory:
        directory = Path(directory)
        exe = directory/'geometry.exe'
        subprocess.run(['g++', '-O2', '-std=c++17', str(wrapper), '-o', str(exe)], check=True, timeout=60)
        geometry_rows = []
        for name, edge, expected in [('real-edge', edges[0], 0), ('nonedge', (0, 1, 2, 3), 4)]:
            path = directory/(name+'.txt')
            path.write_text('2207 1\n'+' '.join(map(str, edge))+'\n', encoding='ascii')
            r = subprocess.run([str(exe), str(path)], capture_output=True, text=True, timeout=10)
            assert r.returncode == expected
            geometry_rows.append(dict(name=name, edge=edge, returncode=r.returncode, stdout=r.stdout, stderr=r.stderr))
    save(args.output, dict(small_semantics=rows, rejected_schema_mutants=rejected,
         geometry_controls=geometry_rows, input_sha256=sha(raw), schema_source_sha256=sha((HERE/'schema.py').read_bytes()),
         source_sha256=sha(Path(__file__).read_bytes()),
         scope='Small exhaustive state/auxiliary projection and six schema corruptions; a syntactically accepted nonedge must fail independent geometry. Not a general formal soundness theorem.'))
    print('PASS semantic states=1104 schema negatives=6 geometry controls=2')


if __name__ == '__main__':
    main()
