#!/usr/bin/env python3
"""Candidate 03 from research/log/2026-10-23-ten-minute-hypotheses.md:

Do the 207 forbidden-family types of the 3x3 two-parameter quadratic pencil
det[x^2 + lambda*y^2 + mu*x*y, x, y, 1] = 0 collapse into few hypergraph
isomorphism classes?

Method (exact, stdlib only):
  1. Rebuild the 31 lines / 175 intersection points / 207 families from
     integer determinants, using the 4x4 permutation expansion.  A second,
     independent determinant route (3x3 row-reduction, as in the original
     classify.py) must agree on every coefficient.
  2. Regression-check the rebuilt strata against the published aggregates
     of research/experiments/quadratic-pencil-20261023 (line table, strata
     counts, root Grundy frequencies, spot case profiles).
  3. Classify the 207 families up to isomorphism of 4-uniform hypergraphs
     on the 9 labelled points: invariant bucketing (edge count, degree
     sequence, pair/triple codegree sequences), then exhaustive backtracking
     isomorphism search with codegree pruning.  Every claimed isomorphism is
     certified by a witness permutation that is re-checked by direct
     substitution.
  4. Cross-validate the partition with an independent canonical-form
     computation (colour refinement + minimum encoding over colour-
     preserving permutations).
  5. Report class counts, automorphism orders, and whether Grundy profiles
     are constant on classes (they must be) vs. how many distinct Grundy
     profiles exist (Grundy equality alone must not be called isomorphism).
"""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
import json

POINTS = [(x, y) for y in range(3) for x in range(3)]  # index = y*3 + x
N = 9


# ---------- determinants: two independent routes ----------

def det_perm(matrix):
    """4x4 determinant by the 24-term permutation expansion."""
    total = 0
    for perm in permutations(range(4)):
        inversions = sum(1 for i in range(4) for j in range(i + 1, 4)
                         if perm[i] > perm[j])
        term = 1
        for i in range(4):
            term *= matrix[i][perm[i]]
        total += -term if inversions % 2 else term
    return total


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def coefficients(ids):
    """(a, b, c) with det = a*lambda + b*mu + c for the 4 points `ids`.

    Route 1: 4x4 permutation determinants with first columns y^2, x*y, x^2.
    Route 2: subtract the last point and take 3x3 determinants (original
    classify.py / two_parameter.py construction).  They must agree.
    """
    sel = [POINTS[i] for i in ids]
    out1 = []
    for f in (lambda u, v: v * v, lambda u, v: u * v, lambda u, v: u * u):
        out1.append(det_perm([[f(u, v), u, v, 1] for u, v in sel]))
    x, y = sel[-1]
    out2 = []
    for f in (lambda u, v: v * v, lambda u, v: u * v, lambda u, v: u * u):
        out2.append(det3(*[(f(u, v) - f(x, y), u - x, v - y)
                           for u, v in sel[:-1]]))
    assert out1 == out2, (ids, out1, out2)
    return tuple(out1)


# ---------- rebuild the 207 families ----------

def build_families():
    universal, lines = [], {}
    for ids in combinations(range(N), 4):
        a, b, c = coefficients(ids)
        mask = sum(1 << i for i in ids)
        if a == b == c == 0:
            universal.append(mask)
        elif a or b:
            divisor = gcd(gcd(a, b), c)
            sign = 1 if next(v for v in (a, b, c) if v) > 0 else -1
            key = tuple(sign * v // divisor for v in (a, b, c))
            lines.setdefault(key, []).append(mask)
        # a == b == 0, c != 0: never forbidden; contributes nothing.

    vertices = set()
    for (a, b, c), (d, e, f) in combinations(sorted(lines), 2):
        det = a * e - b * d
        if det:
            vertices.add((Fraction(b * f - c * e, det),
                          Fraction(c * d - a * f, det)))

    def on(line, point):
        a, b, c = line
        x, y = point
        return a * x + b * y + c == 0

    strata = []  # (kind, representative point or None, active lines)
    generic = next((Fraction(x), Fraction(y))
                   for x in range(30) for y in range(30)
                   if all(not on(line, (Fraction(x), Fraction(y)))
                          for line in lines))
    strata.append(('generic', generic, []))
    for line in sorted(lines):
        a, b, c = line
        for t in range(len(vertices) + 2):
            point = ((Fraction(t), Fraction(-c - a * t, b)) if b
                     else (Fraction(-c, a), Fraction(t)))
            if point not in vertices:
                break
        else:
            raise AssertionError('no line representative')
        assert [o for o in lines if on(o, point)] == [line]
        strata.append(('line', point, [line]))
    for point in sorted(vertices):
        strata.append(('intersection', point,
                       sorted(line for line in lines if on(line, point))))

    families = []
    for kind, point, active in strata:
        edges = frozenset(universal + [m for line in active
                                       for m in lines[line]])
        families.append({'kind': kind,
                         'representative': [str(v) for v in point],
                         'active_lines': [list(line) for line in active],
                         'edges': edges})
    return universal, lines, vertices, families


# ---------- Grundy by subset DP (independent re-implementation) ----------

def solve(edges):
    size = 1 << N
    safe = bytearray([1]) * size
    for edge in edges:
        complement = (size - 1) ^ edge
        sub = complement
        while True:
            safe[edge | sub] = 0
            if not sub:
                break
            sub = (sub - 1) & complement
    values = bytearray(size)
    histogram, terminal = Counter(), Counter()
    for state in range(size - 1, -1, -1):
        if not safe[state]:
            continue
        options = 0
        remaining = (size - 1) ^ state
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            child = state | bit
            if safe[child]:
                options |= 1 << values[child]
        g = 0
        while options >> g & 1:
            g += 1
        values[state] = g
        histogram[g] += 1
        if not options:
            terminal[state.bit_count()] += 1
    return {'edges': len(edges), 'safe_states': sum(safe),
            'root_grundy': values[0],
            'first_move_grundy': [values[1 << i] for i in range(N)],
            'maximum_safe_size': max(terminal) if terminal else 0,
            'terminal_size_histogram': dict(sorted(terminal.items())),
            'grundy_histogram': dict(sorted(histogram.items()))}


# ---------- hypergraph isomorphism ----------

def subsets_of(mask):
    return [i for i in range(N) if mask >> i & 1]


def codegrees(edges):
    deg = [0] * N
    pair = Counter()
    triple = Counter()
    for e in edges:
        vs = subsets_of(e)
        for v in vs:
            deg[v] += 1
        for p in combinations(vs, 2):
            pair[p] += 1
        for t in combinations(vs, 3):
            triple[t] += 1
    return deg, pair, triple


def invariant(edges):
    deg, pair, triple = codegrees(edges)
    return (len(edges), tuple(sorted(deg)),
            tuple(sorted(pair.get(p, 0) for p in combinations(range(N), 2))),
            tuple(sorted(triple.get(t, 0)
                         for t in combinations(range(N), 3))))


def find_iso(edges_f, edges_g):
    """Witness permutation pi (image of each vertex of F) with pi(F) = G,
    or None.  Exhaustive backtracking; pruning uses only necessary
    conditions (degree, pair/triple codegrees), so the search is complete.
    """
    if len(edges_f) != len(edges_g):
        return None
    deg_f, pair_f, triple_f = codegrees(edges_f)
    deg_g, pair_g, triple_g = codegrees(edges_g)
    if sorted(deg_f) != sorted(deg_g):
        return None
    set_g = set(edges_g)
    by_deg_g = defaultdict(list)
    for v in range(N):
        by_deg_g[deg_g[v]].append(v)
    order = sorted(range(N), key=lambda v: -deg_f[v])
    mapping = [-1] * N
    used = [False] * N

    def consistent(v, w):
        # pair and triple codegrees against already-mapped vertices
        for u in range(N):
            if mapping[u] < 0 or u == v:
                continue
            key_f = (min(u, v), max(u, v))
            key_g = (min(mapping[u], w), max(mapping[u], w))
            if pair_f.get(key_f, 0) != pair_g.get(key_g, 0):
                return False
            for t in range(N):
                if mapping[t] < 0 or t in (u, v):
                    continue
                tf = tuple(sorted((u, v, t)))
                tg = tuple(sorted((mapping[u], w, mapping[t])))
                if triple_f.get(tf, 0) != triple_g.get(tg, 0):
                    return False
        return True

    def full_check():
        image = set()
        for e in edges_f:
            m = 0
            for v in subsets_of(e):
                m |= 1 << mapping[v]
            image.add(m)
        return image == set_g

    def backtrack(k):
        if k == N:
            return full_check()
        v = order[k]
        for w in by_deg_g[deg_f[v]]:
            if used[w] or not consistent(v, w):
                continue
            mapping[v] = w
            used[w] = True
            if backtrack(k + 1):
                return True
            mapping[v] = -1
            used[w] = False
        return False

    return list(mapping) if backtrack(0) else None


def count_automorphisms(edges):
    """|Aut(F)| by counting all witnesses from F to itself."""
    deg, pair, triple = codegrees(edges)
    by_deg = defaultdict(list)
    for v in range(N):
        by_deg[deg[v]].append(v)
    order = sorted(range(N), key=lambda v: -deg[v])
    mapping = [-1] * N
    used = [False] * N
    edge_set = set(edges)
    count = 0

    def consistent(v, w):
        for u in range(N):
            if mapping[u] < 0 or u == v:
                continue
            if (pair.get((min(u, v), max(u, v)), 0)
                    != pair.get((min(mapping[u], w), max(mapping[u], w)), 0)):
                return False
            for t in range(N):
                if mapping[t] < 0 or t in (u, v):
                    continue
                if (triple.get(tuple(sorted((u, v, t))), 0)
                        != triple.get(tuple(sorted((mapping[u], w,
                                                    mapping[t]))), 0)):
                    return False
        return True

    def backtrack(k):
        nonlocal count
        if k == N:
            image = set()
            for e in edges:
                m = 0
                for v in subsets_of(e):
                    m |= 1 << mapping[v]
                image.add(m)
            if image == edge_set:
                count += 1
            return
        v = order[k]
        for w in by_deg[deg[v]]:
            if used[w] or not consistent(v, w):
                continue
            mapping[v] = w
            used[w] = True
            backtrack(k + 1)
            mapping[v] = -1
            used[w] = False

    backtrack(0)
    return count


def apply_perm(edges, perm):
    out = set()
    for e in edges:
        m = 0
        for v in subsets_of(e):
            m |= 1 << perm[v]
        out.add(m)
    return frozenset(out)


# ---------- independent canonical form (colour refinement) ----------

def refine_colors(edges):
    deg, _, _ = codegrees(edges)
    colors = list(deg)
    edge_list = [tuple(subsets_of(e)) for e in edges]
    while True:
        signatures = []
        for v in range(N):
            patterns = []
            for e in edge_list:
                if v in e:
                    patterns.append(tuple(sorted(colors[u] for u in e
                                                 if u != v)))
            signatures.append((colors[v], tuple(sorted(patterns))))
        uniq = sorted(set(signatures))
        rank = {s: i for i, s in enumerate(uniq)}
        new = [rank[s] for s in signatures]
        if len(uniq) == len(set(colors)):
            return new
        colors = new


def canonical_form(edges):
    """Minimum encoding over all colour-preserving permutations.
    Returns (encoding, largest colour cell)."""
    colors = refine_colors(edges)
    cells = defaultdict(list)
    for v, c in enumerate(colors):
        cells[c].append(v)
    largest = max(len(vs) for vs in cells.values())
    ordered_cells = [cells[c] for c in sorted(cells)]
    best = None

    # Canonical relabelling: colour cells, in colour order, receive the
    # consecutive new labels; every assignment of a cell's vertices to its
    # label slots is tried and the minimum edge encoding is kept.  (Simply
    # permuting within cells while keeping the original labels would NOT
    # be canonical: the numeric encoding would still depend on where the
    # colours happen to sit.)
    def rec(idx, offset, perm):
        nonlocal best
        if idx == len(ordered_cells):
            image = apply_perm(edges, perm)
            enc = tuple(sorted(image))
            if best is None or enc < best:
                best = enc
            return
        cell = ordered_cells[idx]
        for assignment in permutations(cell):
            for j, v in enumerate(assignment):
                perm[v] = offset + j
            rec(idx + 1, offset + len(cell), perm)

    rec(0, 0, [0] * N)
    return best, largest


# ---------- published aggregates for regression ----------

PUBLISHED_LINES = {
    (0, 1, -2): 2, (0, 1, -1): 5, (0, 1, 0): 9, (0, 1, 1): 5, (0, 1, 2): 2,
    (0, 2, -1): 2, (0, 2, 1): 2, (1, -2, -2): 2, (1, -2, 0): 2,
    (1, -2, 1): 2, (1, -1, -2): 2, (1, -1, 0): 5, (1, -1, 1): 6,
    (1, 0, -1): 5, (1, 0, 0): 18, (1, 0, 2): 2, (1, 1, -2): 2,
    (1, 1, 0): 5, (1, 1, 1): 6, (1, 2, -2): 2, (1, 2, 0): 2, (1, 2, 1): 2,
    (2, -2, -1): 2, (2, -1, -1): 2, (2, -1, 0): 2, (2, -1, 2): 2,
    (2, 0, 1): 2, (2, 1, -1): 2, (2, 1, 0): 2, (2, 1, 2): 2, (2, 2, -1): 2,
}

SPOT_CASES = {  # by active line; values from two-parameter.json
    (): {'edges': 0, 'safe_states': 512, 'root_grundy': 1,
         'grundy_histogram': {'0': 256, '1': 256}},
    ((0, 1, 0),): {'edges': 9, 'safe_states': 334, 'root_grundy': 1,
                   'grundy_histogram': {'0': 144, '1': 109, '2': 81},
                   'terminal_size_histogram': {'5': 45, '6': 6}},
    ((1, 0, 0),): {'edges': 18, 'safe_states': 346, 'root_grundy': 0,
                   'grundy_histogram': {'0': 166, '1': 171, '2': 9},
                   'terminal_size_histogram': {'3': 3, '6': 27}},
    ((1, -1, 1),): {'edges': 6, 'safe_states': 449, 'root_grundy': 0,
                    'grundy_histogram': {'0': 222, '1': 224, '2': 3},
                    'terminal_size_histogram': {'3': 1, '8': 3}},
    ((1, 0, -1),): {'edges': 5, 'safe_states': 392, 'root_grundy': 0,
                    'grundy_histogram': {'0': 148, '1': 148, '2': 48, '3': 48},
                    'terminal_size_histogram': {'6': 24, '7': 2}},
}


def main():
    universal, lines, vertices, families = build_families()

    # --- regression against the published classification ---
    assert universal == [], universal
    assert {k: len(v) for k, v in lines.items()} == PUBLISHED_LINES
    assert len(lines) == 31 and len(vertices) == 175
    assert Counter(f['kind'] for f in families) == {
        'generic': 1, 'line': 31, 'intersection': 175}
    assert len({f['edges'] for f in families}) == 207, 'families not distinct'

    for f in families:
        f['profile'] = solve(f['edges'])
    root_counts = Counter(f['profile']['root_grundy'] for f in families)
    assert root_counts == {0: 31, 1: 142, 2: 16, 3: 18}, root_counts
    for f in families:
        key = tuple(tuple(line) for line in f['active_lines'])
        if key in SPOT_CASES:
            for field, want in SPOT_CASES[key].items():
                got = f['profile'][field]
                got = {str(k): v for k, v in got.items()} \
                    if isinstance(got, dict) else got
                assert got == want, (key, field, got, want)

    # --- isomorphism classes (method 1: invariant buckets + backtracking) ---
    buckets = defaultdict(list)
    for i, f in enumerate(families):
        buckets[invariant(f['edges'])].append(i)
    classes = []  # each: {'rep': family index, 'members': [(idx, witness)]}
    for bucket in buckets.values():
        for i in bucket:
            placed = False
            for cls in classes:
                if cls['rep'] not in bucket:
                    continue
                witness = find_iso(families[i]['edges'],
                                   families[cls['rep']]['edges'])
                if witness is not None:
                    # certificate check by direct substitution
                    assert apply_perm(families[i]['edges'], witness) == \
                        families[cls['rep']]['edges']
                    cls['members'].append((i, witness))
                    placed = True
                    break
            if not placed:
                classes.append({'rep': i, 'members': [(i, list(range(N)))]})

    # --- cross-validation (method 2: canonical forms) ---
    canon_groups = defaultdict(list)
    max_cell = 0
    for i, f in enumerate(families):
        enc, largest = canonical_form(f['edges'])
        max_cell = max(max_cell, largest)
        canon_groups[enc].append(i)
    partition1 = sorted(sorted(i for i, _ in cls['members'])
                        for cls in classes)
    partition2 = sorted(sorted(v) for v in canon_groups.values())
    assert partition1 == partition2, 'canonical-form partition disagrees'

    # --- per-class data ---
    def invariant_profile(f):
        # first_move_grundy is a labelled list; only its multiset is an
        # isomorphism invariant, so compare profiles through this summary.
        p = f['profile']
        return json.dumps({**p, 'first_move_grundy': sorted(
            p['first_move_grundy'])}, sort_keys=True)

    report_classes = []
    for cls in classes:
        rep = families[cls['rep']]
        members = [families[i] for i, _ in cls['members']]
        profiles = {invariant_profile(m) for m in members}
        assert len(profiles) == 1, 'Grundy profile not constant on a class'
        report_classes.append({
            'size': len(members),
            'kinds': dict(Counter(m['kind'] for m in members)),
            'representative': rep['representative'],
            'active_lines': rep['active_lines'],
            'edges': len(rep['edges']),
            'root_grundy': rep['profile']['root_grundy'],
            'profile': rep['profile'],
            'automorphisms': count_automorphisms(rep['edges']),
            'members': [{'kind': m['kind'],
                         'representative': m['representative'],
                         'active_lines': m['active_lines'],
                         'witness_to_representative': w}
                        for m, (_, w) in zip(members, cls['members'])],
        })
    report_classes.sort(key=lambda c: (-c['size'], c['edges']))

    distinct_profiles = len({invariant_profile(f) for f in families})
    report = {
        'question': 'candidate 03: isomorphism classes of the 207 '
                    'two-parameter 3x3 quadratic-pencil types',
        'families': 207,
        'isomorphism_classes': len(classes),
        'class_size_distribution': dict(sorted(Counter(
            c['size'] for c in report_classes).items())),
        'classes_by_kind_mix': dict(Counter(
            json.dumps(c['kinds'], sort_keys=True) for c in report_classes)),
        'distinct_grundy_profiles': distinct_profiles,
        'largest_refinement_cell_seen': max_cell,
        'verification': {
            'determinant_routes_agree': True,
            'published_line_table_reproduced': True,
            'root_grundy_counts_reproduced': dict(root_counts),
            'witnesses_rechecked_by_substitution': True,
            'canonical_form_partition_agrees': True,
            'grundy_profile_constant_on_classes': True,
        },
        'classes': report_classes,
    }
    print(json.dumps({k: v for k, v in report.items() if k != 'classes'},
                     indent=2, ensure_ascii=False))
    destination = Path(__file__).with_name('isomorphism-results.json')
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False)
                           + '\n')


if __name__ == '__main__':
    main()
