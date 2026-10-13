#!/usr/bin/env python3
"""Rank the 28 unresolved polarity conflicts without game-tree search.

Frozen historical inputs, hashes, full local geometry, and conditional plan
effects are recorded. A conditional greedy replacement is an explicit feasible
plan, not an optimality claim or a verdict prediction.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OLD = ROOT / 'research/experiments/n11-joint-s5-proof-planning-20261012/output'
WIN = ROOT / 'research/experiments/n11-proof-cost-comparison-20261012/output'
QUOT = ROOT / 'research/experiments/n11-s5-s6-quotient-20261013/output'
sys.path.insert(0, str(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts'))
sys.path.insert(0, str(ROOT / 'research/experiments/n11-central-reply-frontier-20261012/scripts'))
from independent import Board
from analyze_central_reply_frontier import load_exact_s5_cache


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(pair):
    return pair[0] | pair[1] << 64


def key(value):
    return value & ((1 << 64) - 1), value >> 64


def ident(entry):
    return entry['first'], entry['reply'], entry['third']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=EXP / 'output/ranking.json')
    args = parser.parse_args()
    sources = [OLD / 'dependency-graph.json.gz', QUOT / 'repaired-joint-plan.json',
               WIN / 'pilot-candidates.json', WIN / 'win-side-analysis.json',
               WIN / 'win-witness-masks.json', QUOT / 'pilots.json',
               QUOT / 'pilots-verification.json',
               QUOT / 'pilot-209644-terminal-verification.json',
               QUOT / 'pilot-558600-terminal-verification.json',
               ROOT / 'research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache',
               ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py']
    source_hashes = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    with gzip.open(OLD / 'dependency-graph.json.gz', 'rt') as stream:
        graph = json.load(stream)
    plan = json.loads((QUOT / 'repaired-joint-plan.json').read_text())
    pilots = json.loads((WIN / 'pilot-candidates.json').read_text())
    census = json.loads((QUOT / 'pilots.json').read_text())
    census_receipt = json.loads((QUOT / 'pilots-verification.json').read_text())
    analysis = json.loads((WIN / 'win-side-analysis.json').read_text())
    witness_receipt = json.loads((WIN / 'win-witness-masks.json').read_text())
    assert census_receipt['passed'] and census_receipt['census_sha256'] == sha(QUOT / 'pilots.json')
    for path, expected in census['source_sha256'].items():
        assert sha(ROOT / path) == expected
    for path, expected in plan['source_sha256'].items():
        assert sha(ROOT / path) == expected
    assert plan['verification']['passed']
    assert witness_receipt['passed'] and witness_receipt['analysis_sha256'] == sha(WIN / 'win-side-analysis.json')
    assert witness_receipt['cache_sha256'] == sha(sources[-2])
    assert analysis['central_graph_sha256'] == sha(OLD / 'dependency-graph.json.gz')
    assert graph['source_hashes']['independent_geometry_sha256'] == sha(sources[-1])
    assert analysis['cache_sha256'] == witness_receipt['cache_sha256']
    known = {int(i): v for i, v in plan['resolved_s5_verdicts'].items()}
    assert known == {209644: 1, 558600: 2}
    candidates = {r['s5_index']: r for r in pilots['polarity_conflicts'] if r['s5_index'] not in known}
    assert len(candidates) == 28
    required = set(plan['required_new_s5'])
    assert len(required) == 31636 and set(candidates) <= required
    first_row = next(row for row in analysis['firsts'] if row['first'] == 49)
    assert len(first_row['replies']) == 65 and first_row['and_width_fourths'] == 7519
    fixed_witnesses = {mask(m) for m in witness_receipt['witness_masks']}
    assert len(fixed_witnesses) == 1945
    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, v in known.items():
        cache[tuple(graph['s5_masks'][i])] = {'verdict': v}

    # Recompute the geometry of every unresolved candidate, including all S6
    # children and their concrete moves, and compare with independent C++-
    # verified prior output rather than trusting its ranking fields.
    prior = {row['s5_index']: row for row in census['rows']}
    geometry = {}
    predecessors = {}
    for i, rec in candidates.items():
        parent = mask(rec['mask'])
        assert rec['mask'] == graph['s5_masks'][i]
        assert parent.bit_count() == 5 and board.canonical(parent) == parent
        assert parent in fixed_witnesses
        points = board.points(parent)
        moves = board.points(board.legal(parent))
        stab = [t for t, mapping in enumerate(board.maps) if sum(mapping[p] for p in points) == parent]
        child_to_moves = defaultdict(list)
        for p in moves:
            child_to_moves[board.canonical(parent | 1 << p)].append(p)
        fixed = [sum(board.maps[t][p] == 1 << p for p in moves) for t in stab]
        assert sum(fixed) == len(stab) * len(child_to_moves)
        children = [{'mask': list(key(c)), 'moves': ps} for c, ps in sorted(child_to_moves.items())]
        assert children == prior[i]['children']
        assert len(moves) == rec['legal'] == prior[i]['legal']
        assert stab == prior[i]['stabilizer']
        geometry[i] = dict(points=list(points), legal=len(moves), stabilizer=stab,
                           stabilizer_order=len(stab), canonical_children=len(children),
                           children=children)
        predecessors[i] = board.predecessors(parent)
    known_win_mask = mask(graph['s5_masks'][209644])
    known_win_predecessors = board.predecessors(known_win_mask)
    touched = set().union(*predecessors.values(), known_win_predecessors)

    # Enumerate all 7,519 concrete AND branches of the stored chosen-third
    # strategy. Recompute children only at candidate/known-WIN predecessor
    # classes: all other branches are unaffected by these counterfactuals.
    frontier = []
    baseline_known_win_branches = 0
    touched_children = {s4: set(board.children(s4)) for s4 in touched}
    fixed_usage = defaultdict(list)
    win_free = defaultdict(list)
    loss_uncovered = defaultdict(list)
    for reply in first_row['replies']:
        stored = {mask(m) for m in reply['witness_masks']}
        s3 = (1 << 49) | (1 << reply['reply']) | (1 << reply['chosen_third'])
        fourths = board.points(board.legal(s3))
        assert len(fourths) == reply['chosen_fourths']
        for fourth in fourths:
            s4 = board.canonical(s3 | 1 << fourth)
            if s4 not in touched:
                continue
            children = touched_children[s4]
            covers = children & stored
            old_known_win = any(cache.get(key(c), {}).get('verdict') == 1 for c in children)
            assert covers or old_known_win
            node = dict(reply=reply['reply'], third=reply['chosen_third'], fourth=fourth,
                        s4_mask=list(key(s4)), stored_witness_masks=[list(key(c)) for c in sorted(covers)],
                        already_known_win=old_known_win)
            frontier.append(node)
            baseline_known_win_branches += old_known_win
            for i, pred in predecessors.items():
                if s4 not in pred:
                    continue
                candidate = mask(candidates[i]['mask'])
                assert candidate in children
                if candidate in covers:
                    fixed_usage[i].append(node)
                    if covers == {candidate} and not old_known_win:
                        loss_uncovered[i].append(node)
                if not old_known_win:
                    win_free[i].append(node)
    assert sum(r['chosen_fourths'] for r in first_row['replies']) == 7519

    # Current LOSS plan S4 boundary and the graph's complete option sets.
    known_losses = {i for i, v in known.items() if v == 2}
    cost = [set(c) - known_losses for c in graph['s4_cost']]
    selected = {ident(e): e['s4_class_index'] for e in plan['groups']}
    options = {}
    pair_masks = {}
    for root in graph['roots']:
        if root['role'] == 'known-loss-baseline':
            continue
        pair_masks[(root['origin_first'], root['origin_reply'])] = mask(root['pair_mask'])
        for row in root['thirds']:
            options[(root['origin_first'], root['origin_reply'], row['third'])] = row['options']
    assert len(selected) == len(options) == 2261
    assert set().union(*(cost[s] for s in selected.values())) == required
    selected_by_candidate = {i: {s for s in set(selected.values()) if i in cost[s]} for i in candidates}
    checked_s4 = set().union(*selected_by_candidate.values())

    def check_s4(s):
        value = mask(graph['s4_masks'][s])
        children = board.children(value)
        assert not any(cache.get(key(c), {}).get('verdict') == 1 for c in children)
        unknown = {c for c in children if key(c) not in cache}
        assert unknown == {mask(graph['s5_masks'][i]) for i in cost[s]}

    for s in checked_s4:
        check_s4(s)
    rows = []
    for i in sorted(candidates):
        invalidated = {s for s, c in enumerate(cost) if i in c}
        changed = sorted(k for k, s in selected.items() if s in invalidated)
        excluded = invalidated | set(plan['excluded_s4_classes'])
        viable = {k: [s for s in options[k] if s not in excluded] for k in changed}
        impossible = [k for k in changed if not viable[k]]
        choices = {k: s for k, s in selected.items() if k not in changed}
        union = set().union(*(cost[s] for s in choices.values()))
        assert i not in union
        replacements = []
        if not impossible:
            for k in changed:
                s = min(viable[k], key=lambda s: (len(cost[s] - union), len(cost[s]), s))
                additions = sorted(cost[s] - union)
                union |= cost[s]
                choices[k] = s
                if s not in checked_s4:
                    check_s4(s)
                    checked_s4.add(s)
                s4 = mask(graph['s4_masks'][s])
                s3 = pair_masks[k[:2]] | 1 << k[2]
                fourth = next(p for p in board.points(board.legal(s3)) if board.canonical(s3 | 1 << p) == s4)
                replacements.append(dict(first=k[0], reply=k[1], third=k[2], fourth=fourth,
                                         old_s4=selected[k], new_s4=s, added_s5=additions))
            assert len(choices) == 2261 and i not in union
            assert set().union(*(cost[s] for s in choices.values())) == union
        critical = loss_uncovered[i]
        effect_score = Fraction(len(changed) + len(critical), geometry[i]['canonical_children'])
        rows.append(dict(s5_index=i, mask=candidates[i]['mask'], **geometry[i],
                         loss_plan=dict(required=True, if_loss_union_size=len(required)-1,
                                        if_win_invalidated_s4_options=sorted(invalidated),
                                        if_win_invalidated_selected_s4=sorted(selected_by_candidate[i]),
                                        if_win_affected_choices=[list(k) for k in changed],
                                        if_win_affected_roots=sorted({k[0] for k in changed}),
                                        if_win_unrepairable_choices=[list(k) for k in impossible],
                                        if_win_greedy_repaired_union_size=None if impossible else len(union),
                                        if_win_greedy_delta=None if impossible else len(union)-len(required),
                                        if_win_greedy_replacements=replacements),
                         fixed_win_cover=dict(stored_reply_occurrences=sorted(r['reply'] for r in first_row['replies']
                                                                                 if mask(candidates[i]['mask']) in {mask(m) for m in r['witness_masks']}),
                                              witnessed_branches=fixed_usage[i],
                                              if_loss_uncovered_branches=critical,
                                              if_loss_uncovered_replies=sorted({r['reply'] for r in critical}),
                                              if_win_newly_free_branches=win_free[i],
                                              if_win_newly_free_replies=sorted({r['reply'] for r in win_free[i]})),
                         impact_score=dict(numerator=effect_score.numerator, denominator=effect_score.denominator)))
    geometry_order = sorted(rows, key=lambda r: (r['canonical_children'],
                            -len(r['loss_plan']['if_win_affected_choices']),
                            -len(r['fixed_win_cover']['if_loss_uncovered_branches']), r['s5_index']))
    impact_order = sorted(rows, key=lambda r: (-Fraction(**r['impact_score']), r['canonical_children'], r['s5_index']))
    for rank, row in enumerate(geometry_order, 1):
        row['geometry_first_rank'] = rank
    for rank, row in enumerate(impact_order, 1):
        row['impact_per_child_rank'] = rank
    def damage(row):
        return len(row['loss_plan']['if_win_affected_choices']) + len(row['fixed_win_cover']['if_loss_uncovered_branches'])
    pareto = [r['s5_index'] for r in geometry_order if not any(
        q['canonical_children'] <= r['canonical_children'] and damage(q) >= damage(r)
        and (q['canonical_children'] < r['canonical_children'] or damage(q) > damage(r))
        for q in rows)]
    child_parents = Counter(mask(c['mask']) for row in rows for c in row['children'])
    output = dict(schema='n11-unresolved-conflict-ranking-v1', source_sha256=source_hashes,
                  implementation_sha256=sha(Path(__file__)), candidates=len(rows),
                  loss_plan_union=31636, fixed_win_witnesses=1945,
                  fixed_win_witnesses_unresolved_before=1944,
                  known_verdicts=known, win_frontier_concrete_branches=7519,
                  relevant_win_frontier_branches=len(frontier),
                  relevant_win_frontier_distinct_s4=len({mask(n['s4_mask']) for n in frontier}),
                  relevant_already_known_win_branches=baseline_known_win_branches,
                  independently_checked_loss_s4_boundaries=len(checked_s4),
                  canonical_child_incidence=sum(r['canonical_children'] for r in rows),
                  distinct_s6_children=len(child_parents),
                  child_parent_multiplicity=dict(sorted(Counter(child_parents.values()).items())),
                  geometry_first_order=[r['s5_index'] for r in geometry_order],
                  impact_per_child_order=[r['s5_index'] for r in impact_order],
                  pareto_children_vs_total_affected=pareto,
                  rank_rules=dict(geometry_first='canonical S6 children ASC; invalidated current LOSS choices DESC; uncovered fixed WIN branches if LOSS DESC; S5 index ASC',
                                  impact_per_child='(invalidated current LOSS choices if WIN + uncovered fixed WIN branches if LOSS) / canonical S6 children DESC; canonical children ASC; index ASC'),
                  caveats=['All 28 S5 verdicts remain UNKNOWN. No solver search was run.',
                           'Child counts are geometric widths, not runtime predictions.',
                           'Conditional greedy repairs are feasible explicit plans, not minimum costs.',
                           'An uncovered fixed WIN cover can be repaired with other witnesses or thirds; it does not refute first-move WIN.',
                           'A WIN candidate closes its S4 incidences but does not by itself close a reply or first move.',
                           'Existing cache labels remain solver-trusted; known pilot additions use prior independently checked terminal DAG receipts.'],
                  rows=geometry_order)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, sort_keys=True, indent=2) + '\n')
    with args.output.with_suffix('.tsv').open('w', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['geometry_rank', 's5_index', 'canonical_s6_children', 'stabilizer_order', 'legal_moves',
                         'if_win_loss_choices_invalidated', 'if_loss_fixed_win_branches_uncovered',
                         'if_win_new_free_win_branches', 'if_win_greedy_loss_union',
                         'if_win_greedy_delta', 'impact_per_child_rank'])
        for row in geometry_order:
            l, w = row['loss_plan'], row['fixed_win_cover']
            writer.writerow([row['geometry_first_rank'], row['s5_index'], row['canonical_children'],
                             row['stabilizer_order'], row['legal'], len(l['if_win_affected_choices']),
                             len(w['if_loss_uncovered_branches']), len(w['if_win_newly_free_branches']),
                             l['if_win_greedy_repaired_union_size'], l['if_win_greedy_delta'], row['impact_per_child_rank']])
    print(json.dumps({k: v for k, v in output.items() if k not in ('rows', 'source_sha256', 'caveats')}, indent=2))


if __name__ == '__main__':
    main()
