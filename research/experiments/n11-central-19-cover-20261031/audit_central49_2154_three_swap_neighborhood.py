#!/usr/bin/env python3
"""Exhaust all exact three-witness exchanges from the certified 2154 cover.

The 92 ordinary five-stone classes form a perfect matching. Removing three
selected six-stone witnesses frees six endpoints with exactly 15 matchings.
All alternatives use exact integer 3x3 circle geometry and D4 reduction;
the certified 2154 baseline is separately checked with the independent
two-swap audit (which replays the ten descents and the full two-witness
neighborhood). Any improving three-swap is re-verified with 4x4 Bareiss
before being reported. Outcomes S6/S4/two-stone/empty-board stay UNKNOWN.
"""
from collections import defaultdict
from itertools import combinations, product
import json

import verify_conditional_s6_cover_46 as base
import verify_central49_post_seven_win6_repair_2301 as current
import verify_central49_2154_two_swap_descent as source

HERE = source.HERE


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    for i in range(1, len(vertices)):
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in matchings(rest):
            yield ((vertices[0], vertices[i]),) + tail


def audit():
    # Independent regression of the whole 2301 -> 2154 plan and its two-witness
    # neighborhood before touching three-witness exchanges. This also pins the
    # 2154 constants (2990/2154/6) that the enumeration below relies on.
    source.audit(source.json.loads(source.CERT.read_text(encoding='utf-8')))

    doc = json.loads(source.CERT.read_text(encoding='utf-8'))
    selected = source.source_selection()
    for step in doc['steps']:
        rm = {base.decode(k) for k in step['removed']}
        ad = {base.decode(k) for k in step['added']}
        need(len(rm) == len(ad) == 2 and rm <= selected and not (ad & selected),
             'invalid witness exchange in 2154 descent chain')
        selected = (selected - rm) | ad
    need(len(selected) == 46, 'final witness count changed')
    selected_list = sorted(selected)
    selected_set = set(selected_list)

    data = base.reconstruct()
    s5, incidence, costs = data[1:4]
    incidence = {s: set(v) for s, v in incidence.items()}
    need(len(s5) == 94 and len(incidence) == 3868,
         'source S5/S6 incidence changed')

    frontiers = {}
    for s in selected_list:
        fr = source.fast_frontier(s)
        need(len(fr) == costs[s], 'selected frontier changed')
        frontiers[s] = fr
    kept_union = set().union(*frontiers.values())
    need(len(kept_union) == 2154, 'certified 2154 baseline changed')

    _, _, win6, win7, _ = current.comparison_inventories()
    known_win6 = {base.decode(k) for k in win6}
    known_win7 = {base.decode(k) for k in win7}
    need(len(known_win6) == 145 and len(known_win7) == 23,
         'WIN6/WIN7 exclusions changed')
    loss7 = source.terminal_loss7()
    need(len(kept_union & loss7) == 6, 'terminal LOSS7 overlap changed')
    need(not (kept_union & known_win7), 'known WIN7 selected as LOSS7 obligation')
    need(not (selected_set & known_win6), 'certified WIN6 selected as LOSS witness')

    base_doc = json.loads((HERE / 'conditional_s6_cover_46.json').read_text())
    exceptional = {s5.index(base.decode(k)) for k in
                   base_doc['excluded_s5_for_cardinality_dual']}
    need(len(exceptional) == 2, 'cardinality exceptions changed')
    by_pair = defaultdict(list)
    for s, parents in incidence.items():
        by_pair[tuple(sorted(parents - exceptional))].append(s)
    need(all(len(parents - exceptional) == 2 for parents in incidence.values()),
         'ordinary five-stone graph changed')
    ordinary = {s: tuple(sorted(incidence[s] - exceptional))
                for s in selected_set}
    need(len(by_pair) == 3792 and
         len({p for s in selected_set for p in ordinary[s]}) == 92,
         'selected matching or candidate graph changed')
    by_inpair = by_pair

    checked = feasible = excluded6 = excluded7 = valid = improving = 0
    minimum = 2154
    best = None
    removed_triples = matching_count = 0
    for rem in combinations(selected_list, 3):
        removed_triples += 1
        vertices = tuple(sorted(p for s in rem for p in ordinary[s]))
        need(len(vertices) == len(set(vertices)) == 6,
             'removed matching has duplicate endpoint')
        remset = set(rem)
        kept = selected_set - remset
        kept7 = set().union(*(frontiers[s] for s in kept))
        kept_exc = set().union(*(incidence[s] & exceptional for s in kept))
        for matching in matchings(vertices):
            matching_count += 1
            options = [by_inpair.get(tuple(sorted(pair)), ()) for pair in matching]
            for ad in product(*options):
                checked += 1
                adset = set(ad)
                if (len(adset) != 3
                        or any(s in selected_set and s not in remset for s in ad)
                        or adset == remset):
                    continue
                if not exceptional <= (
                    kept_exc | incidence[ad[0]] | incidence[ad[1]] | incidence[ad[2]]
                ):
                    continue
                feasible += 1
                if adset & known_win6:
                    excluded6 += 1
                    continue
                children = [source.fast_frontier(s) for s in ad]
                need(all(len(children[i]) == costs[ad[i]] for i in range(3)),
                     'alternative S7 count differs from source')
                new = children[0] | children[1] | children[2]
                if new & known_win7:
                    excluded7 += 1
                    continue
                valid += 1
                cost = len(kept7) + len(new - kept7)
                if cost < 2154:
                    improving += 1
                if cost < minimum:
                    minimum = cost
                    best = (tuple(sorted(rem)), tuple(sorted(ad)))

    need(removed_triples == 15180 and matching_count == 227700,
         'three-witness neighborhood enumeration incomplete')
    need(checked >= feasible >= excluded6 + excluded7 and
         valid == feasible - excluded6 - excluded7,
         'candidate accounting mismatch')

    result = {
        'schema': 'n11-central49-2154-exact-three-swap-neighborhood-v1',
        'baseline_distinct_s7_classes': 2154,
        'removed_triples': removed_triples,
        'six_vertex_matchings': matching_count,
        'candidate_combinations': checked,
        'geometrically_feasible_nontrivial': feasible,
        'excluded_certified_win6': excluded6,
        'excluded_known_win7': excluded7,
        'valid_nontrivial': valid,
        'improving_valid_three_swaps': improving,
        'best_distinct_s7': minimum,
        'conditional_only': True,
        'outcomes': {'s6': 'UNKNOWN', 's4': 'UNKNOWN',
                     'two_stone_root': 'UNKNOWN', 'empty_board': 'UNKNOWN'},
    }
    if best is not None:
        result['best_swap'] = {
            'removed': [f'{s:032x}' for s in best[0]],
            'added': [f'{s:032x}' for s in best[1]],
        }
    return result


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
