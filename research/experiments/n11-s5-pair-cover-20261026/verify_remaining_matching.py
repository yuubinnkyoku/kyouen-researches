#!/usr/bin/env python3
"""Re-optimize the conditional 14-S7 plan for *unproved* S8 children.

The JavaScript auditor reconstructs all S6/S7 incidences, removes candidates
refuted by a certified S8 LOSS, and counts terminal-proved S8 WIN children.
A 28-vertex minimum-weight perfect matching is exact for 14 distinct S7
witness roots covering 27 S6 obligations. This does not prove any S7 WIN.
"""
import argparse
import json
import subprocess
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


def verify(negative=False):
    cmd = ['node', str(HERE / 'audit_remaining_matching.js')]
    if negative:
        cmd.append('--negative')
    report = json.loads(subprocess.run(cmd, capture_output=True, text=True,
                                       check=True).stdout)
    assert report['schema'] == 'n11-s5-remaining-proof-only-matching-v1'
    assert len(report['missingS6']) == 27
    assert report['candidates'] == 853
    assert report['excluded'] == 67 and report['allowed'] == 786
    assert len(report['pairOptions']) == 343
    assert len(report['singleOptions']) == 27
    assert report['baseline']['total'] == 546
    assert report['baseline']['distinct'] == 545

    graph = nx.Graph()
    graph.add_nodes_from(range(28))
    options = {}
    for row in report['pairOptions']:
        i, j = row['i'], row['j']
        assert 0 <= i < j < 27 and (i, j) not in options
        assert 0 <= row['missing'] <= row['total'] <= 121
        assert row['total'] - row['secured'] == row['missing']
        graph.add_edge(i, j, weight=row['missing'])
        options[i, j] = row
    for row in report['singleOptions']:
        i = row['i']
        assert 0 <= i < 27 and (i, 27) not in options
        assert 0 <= row['missing'] <= row['total'] <= 121
        assert row['total'] - row['secured'] == row['missing']
        graph.add_edge(i, 27, weight=row['missing'])
        options[i, 27] = row

    matching = nx.algorithms.matching.min_weight_matching(graph, weight='weight')
    assert len(matching) == 14
    selected = [options[min(u, v), max(u, v)] for u, v in matching]
    selected.sort(key=lambda row: row['s7'])
    assert len({row['s7'] for row in selected}) == 14
    assert {i for u, v in matching for i in (u, v)} == set(range(28))
    optimum = sum(row['missing'] for row in selected)
    assert optimum == sum(graph[u][v]['weight'] for u, v in matching)
    assert optimum <= report['baseline']['missing']
    assert report['emptyBoard'] == 'UNKNOWN'
    result = {
        'scope': 'conditional proof-only 14-S7 matching, not a WIN certificate',
        'known_s8_win': report['knownWin8'],
        'known_s8_loss_exclusion': report['knownLoss8'],
        's7_candidates': report['allowed'],
        'baseline_total_s8_edges': report['baseline']['total'],
        'baseline_secured_s8_edges': report['baseline']['secured'],
        'baseline_unproved_s8_edges': report['baseline']['missing'],
        'optimal_unproved_s8_edges': optimum,
        'improvement_in_unproved_edges': report['baseline']['missing'] - optimum,
        'optimized_total_s8_edges': sum(row['total'] for row in selected),
        'optimized_secured_s8_edges': sum(row['secured'] for row in selected),
        'optimized_roots': [row['s7'] for row in selected],
        'matching': selected,
        'new_winner_proofs': 0,
        'empty_board': 'UNKNOWN',
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    verify(parser.parse_args().negative)
