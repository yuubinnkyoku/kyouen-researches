"""Independent clause schemas and threshold interpretations, without CardEnc."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-size1323-drat-20261109'
SHAPES = {'000': (0, 0, 0), '011': (0, 1, 1), '101': (1, 0, 1), '112': (1, 1, 2)}


def bag(clauses):
    return Counter(tuple(sorted(c)) for c in clauses)


def atmost_size(n, k):
    if k == 0:
        return n
    if k == n-1:
        return 1
    return (n-k)*(2*k+1)-k


def atmost_schema(flags, k, actual):
    """Infer only auxiliary names, then compare every independent grid clause.

    S[i,j] has interpretation sum(flags[0:i+1]) >= j. Grid cells exist for
    j-1 <= i <= n-k+j-2. Assigning these thresholds extends EVERY input of
    weight <= k to a model; no completeness assumption about CardEnc is used.
    """
    n = len(flags)
    if k == 0:
        expected = [[-x] for x in flags]
    elif k == n-1:
        expected = [[-x for x in flags]]
    else:
        inputs = set(map(abs, flags))
        by_literal = defaultdict(list)
        for c in actual:
            for lit in c:
                by_literal[lit].append(c)
        grid = {}
        def cell(i, j, premises):
            candidates = []
            for c in by_literal[premises[0]]:
                if len(c) != len(premises)+1 or not set(premises) <= set(c):
                    continue
                remainder = set(c)-set(premises)
                if len(remainder) == 1:
                    v = next(iter(remainder))
                    if v > 0 and v not in inputs:
                        candidates.append(v)
            assert len(candidates) == 1, (i, j, candidates)
            grid[i, j] = candidates[0]
        for i in range(n-k):
            cell(i, 1, [-flags[i]])
        for j in range(2, k+1):
            for i in range(j-1, n-k+j-1):
                cell(i, j, [-flags[i], -grid[i-1, j-1]])
        used = set(grid.values())
        assert len(used) == len(grid) == k*(n-k)
        assert used == {abs(lit) for c in actual for lit in c if abs(lit) not in inputs}
        expected = [[-flags[i], grid[i, 1]] for i in range(n-k)]
        for j in range(1, k+1):
            expected += [[-grid[i, j], grid[i+1, j]] for i in range(j-1, n-k+j-2)]
        for j in range(2, k+1):
            expected += [[-flags[i], -grid[i-1, j-1], grid[i, j]]
                         for i in range(j-1, n-k+j-1)]
        expected += [[-flags[i], -grid[i-1, k]] for i in range(k, n)]
    assert bag(expected) == bag(actual), (n, k)
    return expected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    source = HERE.parent/'parabola-hplus1-drat-20261109'
    edges_raw = gzip.decompress((source/'input/verified_edges.txt.gz').read_bytes())
    p, m = map(int, edges_raw.splitlines()[0].split())
    edges = [list(map(int, row.split())) for row in edges_raw.splitlines()[1:]]
    assert p == 2647 and m == len(edges) == 53886
    with tempfile.TemporaryDirectory(prefix='shape-geometry-') as td:
        td = Path(td)
        edge_file, exe = td/'edges.txt', td/'geometry.exe'
        edge_file.write_bytes(edges_raw)
        subprocess.run(['g++', '-O2', '-std=c++17', str(source/'verify_edges.cpp'), '-o', str(exe)], check=True, timeout=60)
        geometry = subprocess.run([str(exe), str(edge_file)], capture_output=True, text=True, timeout=60)
        assert geometry.returncode == 0 and geometry.stdout.strip() == 'VERIFIED_EDGES 2647 53886'
    h = (p-1)//2
    records = []
    for key, (x, cb, ce) in SHAPES.items():
        location = PRIOR/'output'/('fixed' if key in ('000', '101') else '')/f'shape-{key}'
        init = json.loads((location/'init.json').read_text())
        raw = gzip.decompress((location/'input.cnf.gz').read_bytes())
        rows = raw.decode('ascii').splitlines()
        head = rows[0].split()
        assert head[:2] == ['p', 'cnf'] and int(head[3]) == len(rows)-1
        actual = []
        for row in rows[1:]:
            c = list(map(int, row.split()))
            assert c[-1] == 0 and 0 not in c[:-1]
            actual.append(c[:-1])
        expected = []
        for i in range(h):
            group = list(range(4*i+1, 4*i+5))
            expected.append(group)
            expected.extend([[-a, -b] for a, b in combinations(group, 2)])
        offset = 7*h
        assert bag(expected) == bag(actual[:offset])
        counters = []
        all_counter_aux = set()
        for state_offset, count in ((1, cb), (2, ce)):
            flags = [4*i+state_offset for i in range(h)]
            # Equals(k) is AtMost(n-k) over negated flags, then AtMost(k).
            for literals, bound in (([-f for f in flags], h-count), (flags, count)):
                if bound == h:
                    continue
                length = atmost_size(h, bound)
                cs = actual[offset:offset+length]
                auxiliary = {abs(lit) for c in cs for lit in c} - set(map(abs, flags))
                assert all(v > 4*h for v in auxiliary), 'counter overlaps a pair selector'
                assert not auxiliary & all_counter_aux, 'two counters share auxiliary variables'
                all_counter_aux.update(auxiliary)
                expected += atmost_schema(literals, bound, cs)
                counters.append(dict(bound=bound, clauses=length, complemented=literals[0] < 0))
                offset += length
        base = init['point_base']
        assert all_counter_aux == set(range(4*h+1, base+1))
        assert {abs(lit) for c in expected for lit in c} == set(range(1, base+1))
        for t in range(1, p):
            i = min(t, p-t)
            both, side = 4*i-3, 4*i-1 if t <= h else 4*i
            point = base+t
            expected.extend([[-point, side, both], [point, -side], [point, -both]])
        expected += [[-base-t for t in e if t] for e in edges if x or 0 not in e]
        assert bag(expected) == bag(actual) and int(head[2]) == base+p-1
        records.append(dict(shape=key, clauses=len(actual), variables=int(head[2]), counters=counters,
                            input_sha256=hashlib.sha256(raw).hexdigest(), full_clause_schema_match=True,
                            auxiliary_ranges_disjoint_and_reserved=True))
    result = dict(p=p, excluded_size=h, all_four_clause_schemas_match=True, records=records,
                  provided_edges_geometry=dict(returncode=geometry.returncode, stdout=geometry.stdout,
                      edge_input_sha256=hashlib.sha256(edges_raw).hexdigest(),
                      wrapper_sha256=hashlib.sha256((source/'verify_edges.cpp').read_bytes()).hexdigest(),
                      included_verifier_sha256=hashlib.sha256((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes()).hexdigest()),
                  scope='Independent complete clause schemas and threshold-extension interpretation; no SAT solver or CardEnc called.')
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print('PASS four full clause schemas, threshold counters, and 53886 independently checked forbidden edges')


if __name__ == '__main__':
    main()
