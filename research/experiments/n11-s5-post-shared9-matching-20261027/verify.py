#!/usr/bin/env python3
"""Exact minimum of unproved S7->S8 edges after five shared S9 WIN proofs.

An independently re-solved terminal certificate precedes the structural
audit. Minimum-weight perfect matching is exact only for the stated
14-S7-root conditional strategy, not for the game outcome.
"""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
import networkx as nx

HERE = Path(__file__).resolve().parent
EXP = HERE.parent

def terminal_verify(negative):
    source = EXP / 'n11-s9-shared-plan14-20261027' / 'verify.py'
    spec = importlib.util.spec_from_file_location('shared_s9_terminal', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cert = json.loads((source.parent / 'certificate.json').read_text('utf-8'))
    result = module.verify(cert, negative=negative)
    assert result['s9_win_witnesses'] == 5
    assert result['s10_win_leaves'] == 85
    assert result['terminal_states_per_geometry'] == 4269

def verify(negative=False):
    terminal_verify(negative)
    cmd = ['node', str(HERE / 'audit.js')]
    if negative:
        cmd.append('--negative')
    report = json.loads(subprocess.check_output(cmd, text=True))
    assert report['schema'] == 'n11-s5-post-shared9-matching-v1'
    assert report['proofOnlyWin8Before'] == 2177
    assert report['proofOnlyWin8After'] == 2221
    assert report['knownLoss8'] == 338
    assert report['derivedS8'] == 45
    assert report['missingS6'] == 27
    assert report['s7Candidates'] == 853
    assert report['excluded'] == 67 and report['allowed'] == 786
    assert len(report['pairOptions']) == 343
    assert len(report['singleOptions']) == 27
    assert report['before']['missing'] == 535
    assert report['after']['missing'] == 516
    graph = nx.Graph()
    graph.add_nodes_from(range(28))
    options = {}
    for row in report['pairOptions']:
        u, v = row['i'], row['j']
        assert 0 <= u < v < 27 and (u,v) not in options
        assert row['total'] - row['secured'] == row['cost']
        assert 0 <= row['cost'] <= row['total'] <= 121
        graph.add_edge(u, v, weight=row['cost'])
        options[u,v] = row
    for row in report['singleOptions']:
        u = row['i']
        assert 0 <= u < 27 and (u,27) not in options
        assert row['total'] - row['secured'] == row['cost']
        graph.add_edge(u, 27, weight=row['cost'])
        options[u,27] = row
    matching = nx.algorithms.matching.min_weight_matching(graph, weight='weight')
    assert len(matching) == 14
    assert {u for edge in matching for u in edge} == set(range(28))
    selected = [options[min(u,v), max(u,v)] for u,v in matching]
    assert len({r['s7'] for r in selected}) == 14
    optimum = sum(r['cost'] for r in selected)
    assert optimum <= 516
    assert optimum == sum(graph[u][v]['weight'] for u,v in matching)
    if negative:
        assert all((min(u,v),max(u,v)) in options for u,v in matching)
        assert report['newS7Verdicts'] == 0
    result = {
        'scope':'conditional 14-S7 witness-root matching only',
        'minimum_unproved_edges':optimum,
        'fixed_plan_unproved_edges':report['after']['missing'],
        'improvement_over_fixed_plan':516-optimum,
        'selected_s7_roots':sorted(r['s7'] for r in selected),
        'selected_total_edges':sum(r['total'] for r in selected),
        'selected_secured_edges':sum(r['secured'] for r in selected),
        'affected_s7_candidates':report['affectedValidS7'],
        'reduced_pair_options':report['reducedPairCosts'],
        'reduced_single_options':report['reducedSingleCosts'],
        'known_proof_only_win8':report['proofOnlyWin8After'],
        'new_s7_verdicts':0,'new_s5_verdicts':0,
        'two_stone_root_closures':0,'empty_board':'UNKNOWN',
    }
    print(json.dumps(result, sort_keys=True))
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--negative', action='store_true')
    verify(p.parse_args().negative)
