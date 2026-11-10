"""Independent interpretation of origin-free exact1259/deletion-at-most4 CNFs."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNTER_SOURCE = HERE.parent/'parabola-p2539-exchange-audit-20261110/schema.py'
spec = importlib.util.spec_from_file_location('no_origin_prefix', COUNTER_SOURCE)
prefix = importlib.util.module_from_spec(spec); spec.loader.exec_module(prefix)
P, H, SEED_SHA = 2539, 1269, prefix.SEED_SHA


def size(n, k):
    assert 1 <= k < n-1
    m = n-k
    return 2*m*k+m-k, m*k


def audit(raw, seed, complete_pairs):
    assert complete_pairs in (0, 1)
    assert seed == sorted(set(seed)) and len(seed) == 1258 and {0, 6, 2533} <= set(seed)
    assert all(0 <= t < P for t in seed)
    nv, clauses = prefix.parse(raw)
    both, none = [4*i-3 for i in range(1, H+1)], [4*i-2 for i in range(1, H+1)]
    expected = []
    for i in range(1, H+1):
        b, n, l, h = 4*i-3, 4*i-2, 4*i-1, 4*i
        expected.extend([[b,n,l,h],[-b,-n],[-b,-l],[-b,-h],[-n,-l],[-n,-h],[-l,-h]])
    assert clauses[:len(expected)] == expected
    at, top, counters = len(expected), 4*H, []
    def consume(inputs, bound, name):
        nonlocal at, top
        nc, na = size(len(inputs), bound)
        _, rules = prefix.counter(clauses[at:at+nc], inputs, bound, top, top+na)
        counters.append(dict(name=name, clauses=nc, bound=bound, inputs=len(inputs), domain=[top+1,top+na],rules=rules))
        at += nc; top += na
    if complete_pairs:
        assert clauses[at] == both; at += 1
        consume(both, 1, 'at-most-one-BOTH')
    else:
        assert clauses[at:at+H] == [[-v] for v in both]; at += H
    empty = H+complete_pairs-1259
    consume([-v for v in none], H-empty, 'NONE-lower-via-complement')
    consume(none, empty, 'NONE-upper')
    base, point_start = top, at
    for t in range(1, P):
        i = t if t <= H else P-t
        b, side, a = 4*i-3, 4*i-1 if t <= H else 4*i, base+t
        assert clauses[at:at+3] == [[-a,side,b],[a,-side],[a,-b]]
        at += 3
    point_end, geometry_start = base+P-1, at
    edges = []
    while at < len(clauses):
        clause = clauses[at]
        if not (len(clause) == 4 and all(-point_end <= v < -base for v in clause)):
            break
        q = tuple(sorted(-v-base for v in clause))
        assert len(set(q)) == 4 and 0 not in q and sum(q) % P == 0
        edges.append(q); at += 1
    top, loss_start = point_end, at
    # The origin already costs one deletion; only three other deletions remain.
    consume([-(base+t) for t in seed if t], 3, 'at-most-three-nonzero-deletions')
    assert at == len(clauses) and top == nv and edges
    return edges, dict(p=P, origin=0, complete_pairs=complete_pairs, target_size=1259,
         total_deletion_bound=4, origin_deletion_cost=1, nonzero_deletion_bound=3, variables=nv, clauses=len(clauses),
         onehot_clauses=len(expected), point_base=base, point_definition_clauses=geometry_start-point_start,
         geometric_clauses=loss_start-geometry_start, deletion_clauses=len(clauses)-loss_start, counters=counters,
         scope='Every origin-free safe exact1259 set in this pair class and at most4 TOTAL seed deletions extends to all clauses. Geometry is separately checked; the missing origin consumes one deletion.')
