#!/usr/bin/env python3
"""Independent geometry-only audit of the conditional 46-S6 n11 certificate.

No solver, SciPy, cache, or outcome inference is used. Exact integer
determinants and D4 rebuild every incidence and every dual inequality.
"""
import argparse
import collections
import copy
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 11
V = N * N


def need(condition, message):
    if not condition:
        raise ValueError(message)


def points(mask):
    return tuple(p for p in range(V) if mask & (1 << p))


D4 = []
for mode in range(8):
    row = []
    for p in range(V):
        x, y = p % N, p // N
        u, v = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[mode]
        row.append(N*v + u)
    D4.append(row)


def canonical(mask):
    ps = points(mask)
    return min(sum(1 << row[p] for p in ps) for row in D4)


def forbidden(a, b, c, d):
    """Exact determinant of [x*x+y*y, x, y, 1] for four points."""
    coords = [((p % N)**2 + (p // N)**2, p % N, p // N)
              for p in (a, b, c, d)]
    q = [tuple(coords[i][j] - coords[0][j] for j in range(3))
         for i in (1, 2, 3)]
    return (q[0][0]*(q[1][1]*q[2][2] - q[1][2]*q[2][1])
            - q[0][1]*(q[1][0]*q[2][2] - q[1][2]*q[2][0])
            + q[0][2]*(q[1][0]*q[2][1] - q[1][1]*q[2][0])) == 0


def safe(mask):
    return all(not forbidden(*q) for q in itertools.combinations(points(mask), 4))


def children(mask):
    ps = points(mask)
    triples = tuple(itertools.combinations(ps, 3))
    return [mask | (1 << p) for p in range(V)
            if not (mask & (1 << p))
            and all(not forbidden(a, b, c, p) for a, b, c in triples)]


def key(mask):
    return f'{mask:032x}'


def decode(value):
    need(isinstance(value, str) and len(value) == 32
         and all(c in '0123456789abcdef' for c in value),
         'invalid canonical hex key')
    result = int(value, 16)
    need(result >> V == 0, 'out-of-board bit')
    return result


def reconstruct():
    s4 = decode('00000000000000003800800000000000')
    need(s4.bit_count() == 4 and safe(s4) and canonical(s4) == s4,
         'invalid priority S4')
    s5 = sorted({canonical(s) for s in children(s4)})
    need(len(s5) == 94, 'priority S5 frontier changed')
    incidence = collections.defaultdict(set)
    raw_s6 = 0
    within_parent = 0
    for i, parent in enumerate(s5):
        raw = children(parent)
        raw_s6 += len(raw)
        distinct = {canonical(s) for s in raw}
        within_parent += len(distinct)
        for s6 in distinct:
            incidence[s6].add(i)
    need(raw_s6 == 7890 and within_parent == 7813,
         'S5-to-S6 incidence changed')
    need(len(incidence) == 3868, 'S6 class union changed')
    histogram = collections.Counter(map(len, incidence.values()))
    need(histogram == {2: 3791, 3: 77}, 'S6 incidence multiplicities changed')
    cost = {s6: len(children(s6)) for s6 in incidence}
    return s4, s5, incidence, cost, raw_s6, within_parent, histogram


def verify(doc, data):
    s4, s5, incidence, cost, raw_s6, within_parent, histogram = data
    need(doc['schema'] == 'n11-central49-priority-s4-conditional-s6-cover-v1'
         and doc['board'] == 11 and doc['root_stones'] == [49, 60]
         and doc['s4_key'] == key(s4), 'certificate identity changed')
    need(doc['s4_outcome'] == doc['root_outcome']
         == doc['empty_board_outcome'] == 'UNKNOWN'
         and doc['evidence_level'] == 'GEOMETRY_ONLY_CONDITIONAL_PROOF_PLAN_NOT_VERDICTS',
         'unjustified outcome or evidence level')
    need(doc['s5_count'] == len(s5) == 94
         and doc['raw_s5_s6_edges'] == raw_s6
         and doc['s5_s6_class_incidence'] == within_parent
         and doc['distinct_s6_classes'] == len(incidence)
         and doc['s6_parent_multiplicity'] == {str(k): v for k, v in histogram.items()},
         'S6 incidence summary changed')

    exceptional = [decode(k) for k in doc['excluded_s5_for_cardinality_dual']]
    need(len(exceptional) == 2 and len(set(exceptional)) == 2
         and set(exceptional) <= set(s5), 'invalid cardinality dual exception')
    exceptional_indices = {s5.index(p) for p in exceptional}
    need(all(len(parents - exceptional_indices) <= 2
             for parents in incidence.values()), 'cardinality lower bound fails')
    lower_bound = (len(s5) - 2 + 1) // 2
    need(lower_bound == doc['minimum_conditional_s6_witnesses'] == 46,
         'incorrect cardinality lower bound')

    chosen = [decode(k) for k in doc['selected_s6_classes']]
    need(len(chosen) == len(set(chosen)) == 46
         and all(s6 in incidence for s6 in chosen),
         'invalid selected S6 witness list')
    covered = set().union(*(incidence[s6] for s6 in chosen))
    need(covered == set(range(len(s5))), 'selected S6 do not cover all 94 S5')
    chosen_cost = sum(cost[s6] for s6 in chosen)
    need(chosen_cost == doc['selected_s6_total_raw_s7_edges'] == 2897,
         'selected S6 raw S7 edge count changed')

    # Dual of min sum(c_j*x_j), A*x >= 1, sum(x)=46, x>=0:
    # maximize sum(y_i)+46*lambda, y_i>=0,
    # subject to lambda+sum_{i in parents(j)} y_i <= c_j.
    # Integer feasible primal and dual values agree: exact optimum.
    dual = doc['weighted_optimality_dual']
    lam = dual['lambda_for_exactly_46']
    y = dual['s5_weights_by_sorted_key']
    need(type(lam) is int and len(y) == 94
         and all(type(v) is int and v >= 0 for v in y),
         'invalid weighted dual variables')
    need(all(lam + sum(y[i] for i in parents) <= cost[s6]
             for s6, parents in incidence.items()),
         'weighted dual infeasible')
    dual_value = lam * 46 + sum(y)
    need(dual_value == chosen_cost == 2897,
         'weighted dual bound does not match chosen primal cost')
    return {
        'schema': 'n11-central49-priority-s4-s6-cover-audit-v1',
        's4_outcome': 'UNKNOWN', 'two_stone_root_outcome': 'UNKNOWN',
        'empty_board_outcome': 'UNKNOWN',
        's5_frontier': len(s5), 'raw_s6_edges': raw_s6,
        'canonical_s6_incidence': within_parent,
        'distinct_s6_classes': len(incidence),
        's6_parent_multiplicity': {str(k): v for k, v in sorted(histogram.items())},
        'exact_minimum_conditional_s6_witnesses': lower_bound,
        'selected_s6_classes': len(chosen),
        'selected_raw_s7_edges': chosen_cost,
        'weighted_dual_bound': dual_value,
        'conditional_only': True,
        'caveat': 'No S6 LOSS is proved. A WIN among selected S6 invalidates this particular conditional LOSS4 plan.'
    }


def self_test(doc, data):
    def must_reject(bad, description):
        try:
            verify(bad, data)
        except (ValueError, KeyError, TypeError):
            return
        raise AssertionError('tampering accepted: ' + description)

    bad = copy.deepcopy(doc)
    bad['selected_s6_classes'][0] = bad['selected_s6_classes'][1]
    must_reject(bad, 'duplicate S6')
    bad = copy.deepcopy(doc)
    bad['weighted_optimality_dual']['s5_weights_by_sorted_key'][0] += 1000
    must_reject(bad, 'invalid weighted dual')
    bad = copy.deepcopy(doc)
    bad['excluded_s5_for_cardinality_dual'][0] = bad['selected_s6_classes'][0]
    must_reject(bad, 'wrong-cardinality exception')
    bad = copy.deepcopy(doc)
    bad['s4_outcome'] = 'LOSS'
    must_reject(bad, 'unproved verdict')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    doc = json.loads((HERE / 'conditional_s6_cover_46.json').read_text(encoding='utf-8'))
    data = reconstruct()
    result = verify(doc, data)
    if args.self_test:
        self_test(doc, data)
        result['negative_tests'] = 4
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
