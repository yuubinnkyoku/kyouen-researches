#!/usr/bin/env python3
"""Exact 14-root conditional minimum-edge proof by weighted matching.

The JS auditor independently rebuilds legal boundaries, rejects S8 LOSS
children, and checks the proposed 14-root plan. NetworkX's blossom algorithm
then optimizes the complete 28-vertex weighted matching problem: the 27
uncovered S6 classes plus a dummy vertex for the one singleton.
This does NOT prove that any candidate S7 root is WIN.
"""
import argparse
import json
import subprocess
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def verify(negative=False):
    cmd = ['node', str(HERE / 'audit_minimum_matching.js')]
    if negative:
        cmd.append('--negative')
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    report = json.loads(proc.stdout)
    assert report['schema'] == 'n11-s5-conditional-minimum-edge-matching-v1'
    assert report['uncoveredS6'] == 27
    assert report['candidateS7'] == 853
    assert report['independentGeometryChecked'] == 42
    assert len(report['selectedS7']) == 14
    assert report['selectedCost'] == 546
    assert report['selectedDistinct'] == 545
    assert report['oldCost'] == 554
    assert report['oldDistinct'] == 553

    graph = nx.Graph()
    graph.add_nodes_from(range(28))
    for i, cost in enumerate(report['singleCosts']):
        assert isinstance(cost, int) and 0 < cost < 121
        graph.add_edge(i, 27, weight=cost)
    seen = set()
    for row in report['pairEdges']:
        i, j, cost = row['i'], row['j'], row['cost']
        assert 0 <= i < j < 27 and (i, j) not in seen
        assert isinstance(cost, int) and 0 < cost < 121
        seen.add((i, j))
        graph.add_edge(i, j, weight=cost)

    matching = nx.algorithms.matching.min_weight_matching(graph, weight='weight')
    assert len(matching) == 14, 'incomplete minimum-weight matching'
    optimum = sum(graph[u][v]['weight'] for u, v in matching)
    assert optimum == report['selectedCost'] == 546, (
        f'conditional plan not minimum: {optimum} vs {report["selectedCost"]}')
    assert report['emptyBoard'] == 'UNKNOWN'
    assert report['newS7Verdicts'] == report['newS5Verdicts'] == 0
    assert report['newTwoStoneClosures'] == 0
    print(json.dumps({
        'matching_vertices': 28, 'matching_edges': len(matching),
        'pair_options': len(seen), 'loss_excluded_candidates': report['rejectedS7'],
        'candidate_s7_after_exclusion': report['allowedS7'],
        'conditional_minimum_s7_roots': 14,
        'minimum_s7_s8_class_edges': optimum,
        'old_edges': report['oldCost'], 'new_edges': report['selectedCost'],
        'old_distinct_s8': report['oldDistinct'],
        'new_distinct_s8': report['selectedDistinct'],
        'new_winner_proofs': 0, 'empty_board': 'UNKNOWN'
    }, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    verify(parser.parse_args().negative)
