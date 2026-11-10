"""Independent four-state/point/prefix interpretation of the two frozen CNFs."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNTER_SOURCE = HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py'
spec = importlib.util.spec_from_file_location('independent_prefix_rules', COUNTER_SOURCE)
prefix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prefix)
P, H, SEED_SHA = 2539, 1269, prefix.SEED_SHA


def size(n, k):
    assert 1 <= k < n-1
    m = n-k
    return 2*m*k+m-k, m*k


def audit(raw, seed, case):
    assert case in ('changed-pair', 'no-pair')
    assert seed == sorted(set(seed)) and len(seed) == 1258 and {0, 6, 2533} <= set(seed)
    assert all(0 <= t < P for t in seed)
    nv, clauses = prefix.parse(raw)
    both = [4*i-3 for i in range(1, H+1)]
    none = [4*i-2 for i in range(1, H+1)]
    c, e = (1, 12) if case == 'changed-pair' else (0, 11)
    expected = []
    for i in range(1, H+1):
        b, n, l, h = 4*i-3, 4*i-2, 4*i-1, 4*i
        expected.extend([[b, n, l, h], [-b, -n], [-b, -l], [-b, -h], [-n, -l], [-n, -h], [-l, -h]])
    assert clauses[:len(expected)] == expected
    at, top = len(expected), 4*H
    counters = []
    def consume(inputs, bound, label):
        nonlocal at, top
        count, variables = size(len(inputs), bound)
        labels, rules = prefix.counter(clauses[at:at+count], inputs, bound, top, top+variables)
        counters.append(dict(name=label, clauses=count, bound=bound, inputs=len(inputs),
                             domain=[top+1, top+variables], rules=rules))
        at += count; top += variables
    if c:
        assert clauses[at] == both
        at += 1
        consume(both, 1, 'at-most-one-BOTH')
    else:
        assert clauses[at:at+H] == [[-v] for v in both]
        at += H
    consume([-v for v in none], H-e, 'at-least-E-NONE-via-complement')
    consume(none, e, 'at-most-E-NONE')
    point_base = top
    point_start = at
    for t in range(1, P):
        i = t if t <= H else P-t
        b = 4*i-3
        side = 4*i-1 if t <= H else 4*i
        a = point_base+t
        assert clauses[at:at+3] == [[-a, side, b], [a, -side], [a, -b]]
        at += 3
    point_end = point_base+P-1
    # All geometric clauses use only negative point variables. The remaining
    # tail starts with the explicit old-pair exclusion or the loss counter.
    edges = []
    geometry_start = at
    while at < len(clauses):
        clause = clauses[at]
        if not (len(clause) in (3, 4) and all(-point_end <= v <= -point_base-1 for v in clause)):
            break
        q = sorted(-v-point_base for v in clause)
        if len(q) == 3:
            q = [0]+q
        assert len(set(q)) == 4 and sum(q) % P == 0
        edges.append(tuple(q))
        at += 1
    geometry_end = at
    if c:
        assert clauses[at] == [-both[5]]
        at += 1
    top = point_end
    loss_start = at
    consume([-(point_base+t) for t in seed if t], 4, 'at-most-four-seed-deletions')
    assert at == len(clauses) and top == nv
    assert len(edges) == 38868
    return edges, dict(case=case, p=P, origin=1, complete_pairs=c, empty_pairs=e, target_size=1259,
                      max_removed=4, variables=nv, clauses=len(clauses), onehot_clauses=len(expected),
                      point_base=point_base, point_definition_clauses=geometry_start-point_start,
                      geometric_clauses=geometry_end-geometry_start, deletion_clauses=len(clauses)-loss_start,
                      counters=counters,
                      scope='Every safe exact1259 set in this origin-retaining class and at most4 seed deletions extends via four-state, point-definition and prefix-count assignments. All derived geometric quadruples require separate integer checks.')
