#!/usr/bin/env python3
"""Exhaustive one/two-witness neighborhood of the conditional 2092-S7 cover.

Geometry-only LOCAL optimality, not a LOSS certificate. The excluded WIN6
classes come from three separately terminal-audited seven-stone strategies.
"""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
V = 121
BITS = [1 << i for i in range(V)]
XY = [(i % 11, i // 11) for i in range(V)]
Q = [(x*x + y*y, x, y) for x, y in XY]
D4 = []
for t in range(8):
    row = []
    for x, y in XY:
        u, v = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[t]
        row.append(11*v + u)
    D4.append(row)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def points(m):
    return [i for i in range(V) if m & BITS[i]]


def canonical(m):
    p = points(m)
    return min(sum(BITS[row[i]] for i in p) for row in D4)


def det(a, b, c, d):
    """3x3 difference determinant, separate from the 2092 Bareiss auditor."""
    u = Q[a]
    v, w, z = ([Q[p][i] - u[i] for i in range(3)] for p in (b, c, d))
    return (v[0]*(w[1]*z[2]-w[2]*z[1])
            - v[1]*(w[0]*z[2]-w[2]*z[0])
            + v[2]*(w[0]*z[1]-w[1]*z[0]))


def children(m):
    p = points(m)
    triples = list(combinations(p, 3))
    return [m | BITS[x] for x in range(V)
            if not (m & BITS[x]) and all(det(*q, x) for q in triples)]


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def digest(selected):
    s = ''.join(f'{m:032x}\n' for m in sorted(selected))
    return hashlib.sha256(s.encode('ascii')).hexdigest()


def reconstruct():
    selected = {int(k, 16) for k in read(
        'conditional_s6_cover_46_exclude_certified_win6.json')['selected_s6_classes']}
    for line in (HERE / 'conditional_s6_cover_46_repaired_1980_swaps.txt').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        fields = line.split()
        need(len(fields) == 6, 'bad historical swap row')
        rm, ad = ({int(x, 16) for x in fields[i:i+2]} for i in (0, 2))
        need(len(rm) == len(ad) == 2 and rm <= selected and not (ad & selected),
             'bad historical two-for-two swap')
        selected = (selected - rm) | ad
    for name in ('conditional_s6_cover_46_after_shared58_win6_repair_2089.json',
                 'conditional_s6_cover_46_after_terminal_s6_55_repair_2097.json',
                 'conditional_s6_cover_46_after_second_s7_repair_2207.json'):
        doc = read(name)
        rm = {int(k, 16) for k in doc.get('removed_certified_win6', doc.get('removed', []))}
        ad = {int(k, 16) for k in doc.get('added_s6_classes', doc.get('added', []))}
        need(len(rm) == len(ad) == 2 and rm <= selected and not (ad & selected),
             'invalid repair ' + name)
        selected = (selected - rm) | ad
    doc = read('conditional_s6_cover_46_after_second_s7_repair_2092_swaps.json')
    need(digest(selected) == doc['source_selected_s6_sha256'], '2092 source changed')
    for step in doc['steps']:
        rm, ad = ({int(k, 16) for k in step[f]} for f in ('removed', 'added'))
        need(len(rm) == len(ad) == 2 and rm <= selected and not (ad & selected),
             'invalid 2092 swap')
        selected = (selected - rm) | ad
    need(len(selected) == 46 and digest(selected) == doc['final_selected_s6_sha256']
         == 'afb2a19dc297e87b4d803526277b08f0f9be8c69f533bd02d318865a9533b8f8',
         'final 2092 selection identity changed')
    return sorted(selected)


def certified_win6():
    # CI replays all three parent inventories against their terminal strategies.
    import verify_shared_s7_seven_win6 as a
    import verify_terminal_s7_seven_win6 as b
    import verify_terminal_s7_second_seven_win6 as c
    win = {int(k, 16) for keys in (a.EXPECTED, b.EXPECTED_KEYS, c.EXPECTED_KEYS)
           for k in keys}
    need(len(win) == 21, 'terminal WIN6 inventory changed')
    return win


def audit():
    selected = reconstruct()
    original = read('conditional_s6_cover_46.json')
    s4 = int(original['s4_key'], 16)
    s5 = sorted({canonical(c) for c in children(s4)})
    need(len(s5) == 94, 'priority S5 frontier changed')
    exception = {int(k, 16) for k in original['excluded_s5_for_cardinality_dual']}
    need(len(exception) == 2 and exception <= set(s5), 'dual exceptions changed')
    incidence = defaultdict(set)
    for p in s5:
        for c in children(p):
            incidence[canonical(c)].add(p)
    need(len(incidence) == 3868 and all(len(v-exception) == 2 for v in incidence.values()),
         'dual-tight S6 incidence changed')
    pair = lambda k: tuple(sorted(incidence[k] - exception))
    by_pair = defaultdict(list)
    for k in incidence:
        by_pair[pair(k)].append(k)
    need(len(by_pair) == 3792, 'ordinary-S5 graph changed')
    need(len(set().union(*(incidence[k] for k in selected))) == 94,
         'incomplete S5 coverage')
    ordinary = [v for k in selected for v in pair(k)]
    need(len(ordinary) == len(set(ordinary)) == 92,
         '46 witnesses must perfectly match the 92 ordinary S5')
    win6 = certified_win6()
    need(not win6.intersection(selected), 'selected known WIN6')
    memo = {}
    def frontier(k):
        if k not in memo:
            memo[k] = {canonical(c) for c in children(k)}
        return memo[k]
    counts = Counter(q for k in selected for q in frontier(k))
    need(len(counts) == 2092, '2092 S7 frontier changed')
    selected_set = set(selected)
    combinations_seen = feasible = rejected_win = improvements = ties = 0
    raw_improvements = 0
    best_raw = best_valid = 2092
    for i, j in combinations(range(46), 2):
        a, b = pair(selected[i]); c, d = pair(selected[j])
        need(len({a, b, c, d}) == 4, 'not a matching')
        kept = selected_set - {selected[i], selected[j]}
        kept_ex = set().union(*(incidence[k] & exception for k in kept))
        old = counts.copy()
        for k in (selected[i], selected[j]):
            for q in frontier(k):
                old[q] -= 1
        kept_s7 = {q for q, n in old.items() if n > 0}
        for xpair, ypair in (((a, b), (c, d)), ((a, c), (b, d)),
                             ((a, d), (b, c))):
            for x in by_pair.get(tuple(sorted(xpair)), ()):
                for y in by_pair.get(tuple(sorted(ypair)), ()):
                    combinations_seen += 1
                    if x == y or x in kept or y in kept or {x, y} == {selected[i], selected[j]}:
                        continue
                    if not exception <= (kept_ex | incidence[x] | incidence[y]):
                        continue
                    feasible += 1
                    n = len(kept_s7 | frontier(x) | frontier(y))
                    best_raw = min(best_raw, n)
                    if n < 2092:
                        raw_improvements += 1
                    if x in win6 or y in win6:
                        rejected_win += 1
                        continue
                    best_valid = min(best_valid, n)
                    if n < 2092:
                        improvements += 1
                    if n == 2092:
                        ties += 1
    need((combinations_seen, feasible, rejected_win, raw_improvements,
          best_raw, best_valid, improvements, ties)
         == (5149, 3968, 89, 50, 2037, 2092, 0, 47),
         'two-swap neighborhood results changed')
    return {
        'schema': 'n11-central49-2092-two-swap-local-optimum-v1',
        'conditional_selected_s6': 46, 'ordinary_s5': 92,
        'exceptional_s5': 2, 'candidate_s6': 3868,
        'distinct_ordinary_pairs': 3792, 'distinct_s7': 2092,
        'two_swap_candidate_combinations': combinations_seen,
        'geometrically_feasible_nontrivial_combinations': feasible,
        'excluded_combinations_containing_certified_win6': rejected_win,
        'unfiltered_improving_combinations': raw_improvements,
        'unfiltered_best_distinct_s7': best_raw,
        'valid_improving_combinations': improvements,
        'valid_tied_combinations': ties,
        'valid_neighborhood_minimum_distinct_s7': best_valid,
        'known_terminal_win6_classes_used': len(win6),
        'two_stone_root': 'UNKNOWN', 'empty_board': 'UNKNOWN',
        'scope': 'Exact <=2 witness replacements of this fixed 46-S6 matching; not global optimality or any game verdict.'
    }


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
