"""Independent extension-property audit; imports no search code or SAT library."""
from collections import Counter
from itertools import combinations

P, D, TARGET, REMOVED = 2539, 6, 1259, 4
SEED_SHA = '454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'


def parse(raw):
    lines = raw.decode('ascii').splitlines()
    head = lines[0].split()
    assert len(head) == 4 and head[:2] == ['p', 'cnf']
    nv, nc = map(int, head[2:])
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        assert values and values[-1] == 0 and all(0 < abs(v) <= nv for v in values[:-1])
        assert len(values[:-1]) == len(set(values[:-1]))
        clauses.append(values[:-1])
    assert len(clauses) == nc
    return nv, clauses


def counter(clauses, inputs, bound, top, end):
    # Aux variable (i,j) means >=j true inputs among positions 0..i.
    assert 1 <= bound < len(inputs) and len(set(map(abs, inputs))) == len(inputs)
    assert all(0 < abs(v) <= top for v in inputs)
    positions = {-v: i for i, v in enumerate(inputs)}
    labels, counts = {}, Counter()
    def assign(v, label):
        i, j = label
        assert top < v <= end and 0 <= i < len(inputs) and 1 <= j <= min(bound, i+1)
        assert v not in labels or labels[v] == label
        labels[v] = label
    for clause in clauses:
        base = [v for v in clause if abs(v) <= top]
        aux = [v for v in clause if abs(v) > top]
        assert all(v in positions for v in base)
        shape = (len(base), len(aux), tuple(v > 0 for v in aux))
        if shape == (1, 1, (True,)):
            assign(aux[0], (positions[base[0]], 1))
            counts['input'] += 1
        elif shape == (0, 2, (False, True)):
            i, j = labels[-aux[0]]
            assign(aux[1], (i+1, j))
            counts['carry'] += 1
        elif shape == (1, 2, (False, True)):
            i, j = labels[-aux[0]]
            at = positions[base[0]]
            assert i == at-1
            assign(aux[1], (at, j+1))
            counts['increment'] += 1
        elif shape == (1, 1, (False,)):
            at = positions[base[0]]
            assert labels[-aux[0]] == (at-1, bound)
            counts['overflow'] += 1
        else:
            raise AssertionError(('unsupported counter clause', clause))
    assert set(labels) == set(range(top+1, end+1))
    return labels, dict(counts)


def audit(raw, seed):
    p, d, h = P, D, (P-1)//2
    assert seed == sorted(set(seed)) and len(seed) == 1258 and {0, d, p-d} <= set(seed)
    assert all(0 <= t < p for t in seed)
    assert all(not (i in seed and p-i in seed) for i in range(1, h+1) if i != d)
    nv, clauses = parse(raw)
    empty_inputs = [2*h+i for i in range(1, h+1) if i != d]
    k = h+2-TARGET
    cap_end = 3*h+(len(empty_inputs)-k)*k
    lost_inputs = [-(t if t <= h else h+p-t) for t in seed if t not in (0, d, p-d)]
    end = cap_end+(len(lost_inputs)-REMOVED)*REMOVED
    assert nv == end == 23883 and cap_end == 18879
    first = next(i for i, c in enumerate(clauses) if any(abs(v) > 3*h for v in c))
    second = next(i for i, c in enumerate(clauses) if any(abs(v) > cap_end for v in c))
    start = first-4*(h-1)
    assert start >= 0 and first < second
    expected = []
    for i in range(1, h+1):
        if i != d:
            a, b, c = i, h+i, 2*h+i
            expected.extend([[a, b, c], [-a, -b], [-a, -c], [-b, -c]])
    assert clauses[start:first] == expected
    fixed = {0, d, p-d}
    edges = []
    for clause in clauses[:start]:
        assert 1 <= len(clause) <= 4 and all(-2*h <= v < 0 for v in clause)
        required = []
        for lit in clause:
            v = -lit
            i = v if v <= h else v-h
            assert i != d
            required.append(i if v <= h else p-i)
        assert len(set(required)) == len(required)
        candidates = [tuple(sorted(required+list(extra)))
                      for extra in combinations(sorted(fixed), 4-len(required))
                      if len(set(required+list(extra))) == 4 and (sum(required)+sum(extra)) % p == 0]
        assert len(candidates) == 1
        edges.append(candidates[0])
    labels1, counts1 = counter(clauses[first:second], empty_inputs, k, 3*h, cap_end)
    labels2, counts2 = counter(clauses[second:], lost_inputs, REMOVED, cap_end, end)
    return edges, dict(p=p, d=d, target=TARGET, max_removed=REMOVED, variables=nv, clauses=len(clauses),
                      geometric_clauses=start, onehot_clauses=first-start,
                      empty_counter_clauses=second-first, removal_counter_clauses=len(clauses)-second,
                      empty_bound=k, empty_inputs=len(empty_inputs), removal_inputs=len(lost_inputs),
                      first_aux_domain=[3*h+1, cap_end], second_aux_domain=[cap_end+1, end],
                      empty_counter_rules=counts1, removal_counter_rules=counts2,
                      scope='Every safe fixed-origin/fixed-pair set meeting size and deletion bounds extends to all audited clauses via prefix-count auxiliary assignments. Geometry still requires actual integer determinant checks.')
