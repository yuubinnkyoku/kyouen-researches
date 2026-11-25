#!/usr/bin/env python3
"""Standalone N11 round26 boundary audit: independent integer geometry and D4.

Reads frozen next-plan.json; optionally checks preflight.json. No shared game code,
solver cache, certificate verdicts or network access are needed.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 11
XY = [(i % N, i // N) for i in range(N*N)]
PERM4 = [(p, (-1) ** sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4)))
         for p in itertools.permutations(range(4))]


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def difference_det(ids):
    a, *rest = [XY[i] for i in ids]
    def row(p):
        x, y = p
        return (x*x+y*y-a[0]*a[0]-a[1]*a[1], x-a[0], y-a[1])
    return det3(*(row(p) for p in rest))


def full_det(ids):
    rows = []
    for i in ids:
        x, y = XY[i]
        rows.append((x*x+y*y, x, y, 1))
    return sum(sign*rows[0][p[0]]*rows[1][p[1]]*
               rows[2][p[2]]*rows[3][p[3]] for p, sign in PERM4)


def canonical(mask):
    indices = [i for i in range(121) if (mask >> i) & 1]
    choices = []
    for flip in range(2):
        for turns in range(4):
            m = 0
            for i in indices:
                x, y = XY[i]
                if flip:
                    x = N-1-x
                for _ in range(turns):
                    x, y = N-1-y, x
                m |= 1 << (y*N+x)
            choices.append(m)
    return min(choices)


def audit():
    plan = json.loads((HERE/'next-plan.json').read_text(encoding='utf-8'))
    keys = plan['newSelectedKeys']
    assert plan['schema'] == 'n11-post-round25-proof-only-replan-v1'
    assert plan['emptyBoard'] == 'UNKNOWN'
    assert plan['conditionalUnprovedEdges'] == 37
    assert plan['proofOnlyWin8After'] == 5859
    assert plan['winLossConflicts'] == 0
    assert len(keys) == plan['selectedCount'] and len(keys) > 0
    assert len(set(keys)) == len(keys)
    assert hashlib.sha256(('\n'.join(keys)+'\n').encode()).hexdigest() == plan['newSelectionSha256']
    for four in ((0, 1, 2, 3), (0, 2, 22, 24)):
        assert difference_det(four) == full_det(four) == 0

    children, counts, comparisons = [], [], 0
    for key in keys:
        mask = int(key, 16)
        occupied = [i for i in range(121) if mask >> i & 1]
        assert len(occupied) == 9 and canonical(mask) == mask, key
        for four in itertools.combinations(occupied, 4):
            a, b = difference_det(four), full_det(four)
            assert a == -b and a != 0, (key, four, a, b)
            comparisons += 1
        legal = 0
        for p in range(121):
            if mask >> p & 1:
                continue
            allowed = True
            for three in itertools.combinations(occupied, 3):
                four = (*three, p)
                a, b = difference_det(four), full_det(four)
                assert a == -b, (key, four, a, b)
                comparisons += 1
                if a == 0:
                    allowed = False
            if allowed:
                legal += 1
                children.append(canonical(mask | (1 << p)))
        counts.append(legal)

    assert len(children) == plan['legal10Children']
    return {
        'schema': 'n11-post-round25-independent-boundary-preflight-v1',
        'emptyBoard': 'UNKNOWN',
        'selectionSha256': plan['newSelectionSha256'],
        'roots': len(keys),
        'legalS10Edges': len(children),
        'distinctS10Classes': len(set(children)),
        'repeatedS10Classes': len(children)-len(set(children)),
        'crossRootSavings': len(children)-len(set(children)),
        'legalChildrenPerRoot': counts,
        'geometryChecks': ['3x3-difference-determinant',
                           '4x4-permutation-integer-determinant'],
        'fourPointGeometryComparisons': comparisons,
        'terminalVerdicts': 0,
        'newTwoStoneClosures': 0,
    }


if __name__ == '__main__':
    result = audit()
    if (HERE/'preflight.json').exists():
        expected = json.loads((HERE/'preflight.json').read_text(encoding='utf-8'))
        assert result == expected, 'frozen independent preflight mismatch'
    print(json.dumps(result, indent=2))
