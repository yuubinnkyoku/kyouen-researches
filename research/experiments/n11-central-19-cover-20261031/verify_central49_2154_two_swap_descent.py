#!/usr/bin/env python3
"""Independently audit the 2301 -> 2154 N11 conditional seven-stone frontier.

Source and selected swaps: exact 4x4 Bareiss geometry. Complete one/two
witness neighborhood: exact independent 3x3 difference determinant.
All S6, S4, two-stone and empty-board outcomes remain UNKNOWN.
"""
import argparse
from collections import defaultdict
from functools import lru_cache
from itertools import combinations
import copy
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_central49_post_seven_win6_repair_2301 as current
import verify_five_terminal_loss7 as terminal

HERE = Path(__file__).resolve().parent
CERT = HERE / 'conditional_s6_cover_46_post_seven_win6_2154_swaps.json'
SOURCE = 'conditional_s6_cover_46_post_seven_win6_repair_2301.json'
EXPECTED = ((2997, 2256), (3008, 2218), (3005, 2168),
            (3002, 2166), (2999, 2163), (2994, 2158),
            (2993, 2157), (2992, 2156), (2991, 2155),
            (2990, 2154))
FIRST_MOVES = {
    '00000000000000203808000000000120': 115,
    '0000000000000020380a000000004000': 76,
    '00000000000000a03808100000000000': 114,
    '00000000000002043800800000040000': 49,
    '00000000000200801082008100000000': 65,
}
UNKNOWN = {'s6': 'UNKNOWN', 's4': 'UNKNOWN',
           'two_stone_root': 'UNKNOWN', 'empty_board': 'UNKNOWN'}
FULL = (1 << 121) - 1


def need(ok, message):
    if not ok:
        raise ValueError(message)


def key(s):
    return f'{s:032x}'


def source_selection():
    source = json.loads(current.CERT.read_text(encoding='utf-8'))
    current.verify(source)  # Independently audit the entire old 2301 plan.
    historical = json.loads(current.repaired.CERT.read_text(encoding='utf-8'))
    selected = {base.decode(s) for s in historical['selected_s6_classes']}
    for row in current.historical.load_rows():
        rm, ad = ({base.decode(s) for s in row[i:i+2]} for i in (0, 2))
        need(len(rm) == len(ad) == 2 and rm <= selected and not (ad & selected),
             'historical repair chain invalid')
        selected = (selected - rm) | ad
    rm = {base.decode(s) for s in current.REMOVED}
    ad = {base.decode(s) for s in current.ADDED}
    need(len(rm) == len(ad) == 7 and rm <= selected and not (ad & selected),
         'post-seven-WIN6 repair changed')
    selected = (selected - rm) | ad
    need(len(selected) == 46, 'old selected witness count changed')
    return selected


def terminal_loss7():
    # K0644 separately replays the five SHA256-pinned complete strategies.
    # This checks their 40 geometric parent restorations independently.
    need(set(FIRST_MOVES) == set(terminal.EXPECTED),
         'K0644 terminal source inventory changed')
    G = current.geometry
    loss = set()
    for k, move in FIRST_MOVES.items():
        root = base.decode(k)
        eight = root | (1 << move)
        need(eight in G.children(root), 'certified strategy first move illegal')
        for p in G.points(eight):
            parent = eight ^ (1 << p)
            need(eight in G.children(parent), 'LOSS8 parent restoration illegal')
            loss.add(G.canonical(parent))
    need(len(loss) == 23, 'K0644 lifted LOSS7 class count changed')
    return loss


@lru_cache(maxsize=None)
def forbidden_triple(a, b, c):
    # Fast exact 3x3 determinant, distinct from the 4x4 verifier.
    return sum(1 << p for p in range(121) if base.forbidden(a, b, c, p))


@lru_cache(maxsize=None)
def fast_frontier(s):
    banned = s
    for triple in combinations(base.points(s), 3):
        banned |= forbidden_triple(*triple)
    return frozenset(base.canonical(s | (1 << p))
                     for p in base.points(FULL & ~banned))


def audit(doc):
    need(type(doc) is dict and doc.get('schema') ==
         'n11-central49-2301-to-2154-ten-two-swaps-v1'
         and doc.get('source_certificate') == SOURCE
         and doc.get('outcomes') == UNKNOWN
         and doc.get('evidence_level') ==
         'GEOMETRY_ONLY_CONDITIONAL_COVER_WITH_TERMINAL_BACKED_S7_HITS',
         'incorrect plan identity or unproved verdict')
    steps = doc.get('steps')
    need(type(steps) is list and len(steps) == 10, 'expected ten two-swaps')
    selected = source_selection()
    data = base.reconstruct()
    s5, incidence, costs = data[1:4]
    need(len(s5) == 94 and len(incidence) == 3868,
         'source S5/S6 incidence changed')
    _, _, win6, win7, _ = current.comparison_inventories()
    known_win6 = {base.decode(k) for k in win6}
    known_win7 = {base.decode(k) for k in win7}
    need(len(known_win6) == 145 and len(known_win7) == 23,
         'known WIN exclusions changed')
    loss7 = terminal_loss7()
    need(not (loss7 & known_win7), 'terminal LOSS7 conflicts with known WIN7')
    memo = {}

    def four_frontier(s):
        if s not in memo:
            need(s in incidence and s.bit_count() == 6 and
                 current.geometry.canonical(s) == s,
                 'noncanonical or out-of-scope S6 witness')
            raw = current.geometry.children(s)
            children = {current.geometry.canonical(c) for c in raw}
            need(len(raw) == len(children) == costs[s],
                 '4x4 S6-to-S7 geometry disagrees with 3x3 source')
            memo[s] = children
        return memo[s]

    def measure(selection):
        need(len(selection) == 46 and
             set().union(*(incidence[s] for s in selection)) == set(range(94)),
             'selected witnesses do not cover all 94 S5 classes')
        need(not (selection & known_win6), 'certified WIN6 selected as LOSS')
        children = {s: four_frontier(s) for s in selection}
        union = set().union(*children.values())
        need(not (union & known_win7),
             'known WIN7 selected as LOSS7 obligation')
        return sum(map(len, children.values())), union, children

    raw, union, children = measure(selected)
    need((raw, len(union)) == (2992, 2301),
         '2301 source frontier unexpectedly changed')
    for i, step in enumerate(steps):
        need(type(step) is dict and
             set(step) == {'removed', 'added', 'raw_s7_edges',
                           'distinct_s7_classes', 'secured_loss7_classes'},
             'unexpected swap fields')
        removed, added = step['removed'], step['added']
        need(type(removed) is list and type(added) is list and
             len(removed) == len(added) == 2 and
             removed == sorted(set(removed)) and added == sorted(set(added)),
             'invalid two-for-two encoding')
        rm = {base.decode(k) for k in removed}
        ad = {base.decode(k) for k in added}
        need(rm <= selected and not (ad & selected),
             'two-for-two witness replacement invalid')
        selected = (selected - rm) | ad
        raw, union, children = measure(selected)
        need((raw, len(union)) == EXPECTED[i] ==
             (step['raw_s7_edges'], step['distinct_s7_classes']) and
             len(union & loss7) == step['secured_loss7_classes'] == 6,
             f'swap {i+1} count or secured coverage changed')

    secured = union & loss7
    secured_edges = sum(len(ch & loss7) for ch in children.values())
    secured_witnesses = sum(bool(ch & loss7) for ch in children.values())
    need((len(secured), secured_edges, secured_witnesses) == (6, 6, 3),
         'K0644 secured overlap changed')
    need(doc['selected_s6_count'] == 46 and doc['s5_covered'] == 94
         and doc['raw_s7_edges'] == 2990 and doc['distinct_s7_classes'] == 2154
         and doc['saved_s7_classes'] == 147
         and doc['known_win6_conflicts'] == doc['known_win7_conflicts'] == 0
         and doc['terminal_backed_loss7_hits_from_k0644'] == 6
         and doc['terminal_backed_loss7_keys_from_k0644'] ==
             [key(s) for s in sorted(secured)]
         and doc['terminal_backed_loss7_edges'] == secured_edges
         and doc['terminal_backed_loss7_witnesses'] == secured_witnesses,
         'final plan manifest differs from independent geometry')

    # 92 ordinary S5 are perfectly matched by 46 witnesses. Any replacement
    # of two witnesses must match their four endpoints in one of 3 pairings.
    base_doc = json.loads((HERE / 'conditional_s6_cover_46.json').read_text())
    exceptional = {s5.index(base.decode(k)) for k in
                   base_doc['excluded_s5_for_cardinality_dual']}
    need(len(exceptional) == 2 and
         all(len(parents - exceptional) == 2 for parents in incidence.values()),
         'two-exception matching invariant changed')
    ordinary = [v for s in selected for v in incidence[s] - exceptional]
    need(len(ordinary) == len(set(ordinary)) == 92,
         'selected witnesses are not an ordinary-S5 perfect matching')
    by_pair = defaultdict(list)
    for s, parents in incidence.items():
        by_pair[tuple(sorted(parents - exceptional))].append(s)
    need(len(by_pair) == 3792, 'candidate matching graph changed')
    checked = feasible = valid = rejected_win6 = rejected_win7 = improving = 0
    for a, b in combinations(sorted(selected), 2):
        four = tuple(sorted((incidence[a] | incidence[b]) - exceptional))
        need(len(four) == 4, 'removed witnesses overlap ordinary S5')
        kept = selected - {a, b}
        kept7 = set().union(*(four_frontier(s) for s in kept))
        kept_exceptional = set().union(*(incidence[s] & exceptional for s in kept))
        pairings = ((four[:2], four[2:]),
                    ((four[0], four[2]), (four[1], four[3])),
                    ((four[0], four[3]), (four[1], four[2])))
        for pair1, pair2 in pairings:
            for x in by_pair.get(pair1, ()):
                for y in by_pair.get(pair2, ()):
                    checked += 1
                    if x == y or x in kept or y in kept or {x, y} == {a, b}:
                        continue
                    if not exceptional <= (kept_exceptional | incidence[x] | incidence[y]):
                        continue
                    feasible += 1
                    if x in known_win6 or y in known_win6:
                        rejected_win6 += 1
                        continue
                    cx, cy = fast_frontier(x), fast_frontier(y)
                    need(len(cx) == costs[x] and len(cy) == costs[y],
                         '3x3 alternative S7 count differs from source')
                    candidate = kept7 | cx | cy
                    if candidate & known_win7:
                        rejected_win7 += 1
                        continue
                    valid += 1
                    if len(candidate) < 2154:
                        improving += 1
    need((checked, feasible, valid, rejected_win6,
          rejected_win7, improving) == (4915, 3736, 3728, 8, 0, 0),
         'exact two-swap neighborhood changed')
    return {
        'schema': 'n11-central49-2154-independent-two-swap-audit-v1',
        'source_s7_classes': 2301, 'final_s7_classes': len(union),
        'saved_s7_classes': 2301 - len(union),
        'raw_s7_edges': raw, 'selected_s6': len(selected), 'covered_s5': 94,
        'known_win6_excluded': len(known_win6),
        'known_win7_excluded': len(known_win7),
        'secured_loss7_from_k0644': len(secured),
        'unsecured_by_k0644': len(union - secured),
        'two_swap_candidate_combinations': checked,
        'geometrically_feasible_nontrivial_combinations': feasible,
        'valid_nontrivial_combinations': valid,
        'excluded_win6_combinations': rejected_win6,
        'excluded_win7_combinations': rejected_win7,
        'improving_valid_two_swaps': improving,
        'two_swap_local_minimum': len(union),
        'conditional_only': True, 's6_outcome': 'UNKNOWN',
        's4_outcome': 'UNKNOWN', 'two_stone_root': 'UNKNOWN',
        'empty_board': 'UNKNOWN',
    }


def negative_tests(doc):
    for mode in ('verdict', 'source', 'swap_count', 'bad_add', 'secured'):
        bad = copy.deepcopy(doc)
        if mode == 'verdict':
            bad['outcomes']['s6'] = 'LOSS'
        elif mode == 'source':
            bad['source_certificate'] = 'superseded_1985.json'
        elif mode == 'swap_count':
            bad['steps'][0]['distinct_s7_classes'] -= 1
        elif mode == 'bad_add':
            bad['steps'][0]['added'][0] = bad['steps'][0]['removed'][0]
        else:
            bad['terminal_backed_loss7_hits_from_k0644'] += 1
        try:
            audit(bad)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError('tampered manifest accepted: ' + mode)
    return 5


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    doc = json.loads(CERT.read_text(encoding='utf-8'))
    result = audit(doc)
    if args.negative:
        result['negative_tests'] = negative_tests(doc)
    print(json.dumps(result, indent=2, ensure_ascii=False))
