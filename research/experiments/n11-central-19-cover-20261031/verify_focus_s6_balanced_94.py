#!/usr/bin/env python3
"""Independently verify the exact legal-sixth-edge-balanced S5 focus partition.

This checks only geometry and scheduling. It does not prove an S5 verdict.
"""
import hashlib
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = HERE / 'focus_s6_balanced_94.json'
FOCUS_S4 = '00000000000000003800800000000000'


def points(key):
    bits = int(key, 16)
    assert len(key) == 32 and bits >> 121 == 0
    return tuple(p for p in range(121) if bits >> p & 1)


def determinant(quad):
    rows = []
    for p in quad:
        x, y = p % 11, p // 11
        rows.append((x*x + y*y, x, y))
    a, b, c = (tuple(rows[i][j] - rows[0][j] for j in range(3))
               for i in (1, 2, 3))
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def safe(pts):
    return all(determinant(quad) != 0 for quad in combinations(pts, 4))


def canonical(pts):
    variants = []
    for t in range(8):
        bits = 0
        for p in pts:
            x, y = p % 11, p // 11
            u, v = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                    (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[t]
            bits |= 1 << (11*v + u)
        variants.append(bits)
    return f'{min(variants):032x}'


def legal_sixth_count(s5):
    used = set(s5)
    triples = tuple(combinations(s5, 3))
    return sum(all(determinant((*triple, p)) != 0 for triple in triples)
               for p in range(121) if p not in used)


def verify():
    raw = CERT.read_bytes()
    doc = json.loads(raw)
    assert doc['schema'] == 'n11-central49-priority-s4-exact-s6-edge-balance-v1'
    assert doc['root_stones'] == [49, 60]
    assert doc['focus_s4'] == FOCUS_S4
    assert doc['root_outcome'] == doc['empty_board_outcome'] == 'UNKNOWN'
    assert doc['evidence_level'] == 'SCHEDULING_ONLY_NOT_A_CERTIFICATE'
    s4 = points(FOCUS_S4)
    assert s4 == (47, 59, 60, 61) and safe(s4)
    frontier = sorted({canonical((*s4, p)) for p in range(121)
                       if p not in s4 and safe((*s4, p))})
    assert len(frontier) == 94
    assignment = doc['assignment_by_sorted_s5']
    assert len(assignment) == len(frontier) and set(assignment) == set('0123')
    worklists = [[key for key, worker in zip(frontier, assignment)
                  if worker == str(i)] for i in range(4)]
    assert [len(group) for group in worklists] == doc['worker_s5_counts'] == [24, 24, 23, 23]
    weights = {key: legal_sixth_count(points(key)) for key in frontier}
    assert min(weights.values()) == 68 and max(weights.values()) == 92
    baseline = [sum(weights[key] for key in frontier[i::4]) for i in range(4)]
    balanced = [sum(weights[key] for key in group) for group in worklists]
    assert baseline == doc['old_worker_s6_edges'] == [2021, 1998, 1909, 1962]
    assert balanced == doc['balanced_worker_s6_edges'] == [1973, 1972, 1972, 1973]
    assert sum(weights.values()) == doc['total_s6_edges'] == 7890
    # A partition's maximum load cannot be smaller than ceil(total/4).
    lower = (sum(weights.values()) + 3) // 4
    assert lower == doc['max_load_lower_bound'] == max(balanced) == 1973
    return worklists, hashlib.sha256(raw).hexdigest()


if __name__ == '__main__':
    lists, sha = verify()
    print('EXACT_S6_EDGE_BALANCE_OK', [len(x) for x in lists], sha)
