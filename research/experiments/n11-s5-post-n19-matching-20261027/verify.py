#!/usr/bin/env python3
"""Exact conditional matching after 55 independently terminal-proved S9 WINs.

This minimizes outstanding S7->S8 proof edges for the conditional 14-root
scheme, not proof runtime and not the 11x11 empty-board outcome.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import networkx as nx

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s5-post-short46-matching-20261027'))
from alternating_cycle_check import verify_optimality, self_test


def verify(negative=False):
    subprocess.check_call([
        'node', str(EXP / 'n11-s9-n19-terminal-20261027' / 'verify.js'),
        *(['--negative'] if negative else []),
    ])
    raw = subprocess.check_output([
        'node', str(HERE / 'audit.js'),
        *(['--negative'] if negative else []),
    ], text=True)
    r = json.loads(raw)
    assert r['schema'] == 'n11-s5-post-n19-matching-v1'
    assert r['missingS6'] == 27
    assert r['proofOnlyWin8Before'] == 2968
    assert r['proofOnlyWin8After'] == 3394
    assert r['newlyProvedS8'] == 426
    assert r['knownLoss8'] == 338
    assert (r['candidates'], r['excluded'], r['allowed']) == (853, 67, 786)
    assert len(r['pairOptions']) == 343
    assert len(r['singleOptions']) == 27
    assert r['previous']['missing'] == 384
    assert r['updated'] == {
        'total': 548, 'secured': 215, 'missing': 333,
        'distinctMissing': 333,
    }
    graph = nx.Graph()
    graph.add_nodes_from(range(28))
    options = {}
    for row in r['pairOptions']:
        u, v = row['i'], row['j']
        assert 0 <= u < v < 27 and (u, v) not in options
        assert row['total'] - row['secured'] == row['cost'] >= 0
        graph.add_edge(u, v, weight=row['cost'])
        options[u, v] = row
    for row in r['singleOptions']:
        u = row['i']
        assert 0 <= u < 27 and (u, 27) not in options
        assert row['total'] - row['secured'] == row['cost'] >= 0
        graph.add_edge(u, 27, weight=row['cost'])
        options[u, 27] = row
    matching = nx.algorithms.matching.min_weight_matching(graph, weight='weight')
    assert len(matching) == 14
    assert {u for e in matching for u in e} == set(range(28))
    selected = [options[min(u, v), max(u, v)] for u, v in matching]
    roots = sorted(row['s7'] for row in selected)
    assert len(set(roots)) == 14
    optimum = sum(row['cost'] for row in selected)
    assert optimum <= 333, 'minimum cannot exceed saved feasible plan'
    self_test()
    edge_costs = {(min(u, v), max(u, v)): data['weight']
                  for u, v, data in graph.edges(data=True)}
    independently_verified_cost, minimum_cycle_delta, dp_states = (
        verify_optimality(edge_costs, matching))
    assert independently_verified_cost == optimum
    assert minimum_cycle_delta is None or minimum_cycle_delta >= 0
    result = {
        'scope': 'conditional 14-S7 witness roots only',
        'minimum_unproved_edges': optimum,
        'alternating_cycle_exact_check': True,
        'minimum_alternating_cycle_delta': minimum_cycle_delta,
        'alternating_cycle_dp_states': dp_states,
        'fixed_plan_unproved_edges': 333,
        'improvement_over_fixed_plan': 333 - optimum,
        'saved_plan_is_optimal': optimum == 333,
        'selected_s7_roots': roots,
        'saved_s7_roots': sorted(r['savedPlan']),
        'selected_total_edges': sum(row['total'] for row in selected),
        'selected_secured_edges': sum(row['secured'] for row in selected),
        'affected_s7_candidates': r['affectedValidS7'],
        'reduced_pair_options': r['reducedPairCosts'],
        'reduced_single_options': r['reducedSingleCosts'],
        'known_proof_only_win8': 3394,
        'new_s7_verdicts': 0,
        'new_s5_verdicts': 0,
        'two_stone_root_closures': 0,
        'empty_board': 'UNKNOWN',
    }
    print(json.dumps(result, sort_keys=True))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    verify(parser.parse_args().negative)
