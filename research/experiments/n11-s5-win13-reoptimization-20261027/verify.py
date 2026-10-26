#!/usr/bin/env python3
"""Exact updated 14-root conditional matching after the terminal S8 WIN13.

This is a proof-obligation optimization, not a new S7 or S5 outcome.
"""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
import networkx as nx

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def verify(negative=False):
    # Recompute the new WIN8 terminal certificate without trusting a verdict cache.
    source = EXPERIMENTS / 'n11-s8-plan14-win13-20261026' / 'verify.py'
    spec = importlib.util.spec_from_file_location('win13_terminal_verifier', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    terminal = module.verify(negative=negative)
    assert terminal['s10_win_leaves'] == 13
    assert terminal['terminal_states_each_geometry'] == 464

    cmd = ['node', str(HERE / 'audit.js')]
    if negative:
        cmd.append('--negative')
    report = json.loads(subprocess.check_output(cmd, text=True))
    assert report['schema'] == 'n11-s5-win13-updated-matching-v1'
    assert report['newKnownWin8'] == report['oldKnownWin8'] + 1
    assert report['missingS6'] == 27
    assert report['s7Candidates'] == 853
    assert report['excluded'] == 67 and report['allowed'] == 786
    assert len(report['affectedS7Parents']) == 3
    assert len(report['pairOptions']) == 343
    assert len(report['singleOptions']) == 27
    assert report['before']['missing'] == 536
    assert report['after']['missing'] == 535

    graph = nx.Graph()
    graph.add_nodes_from(range(28))
    options = {}
    for row in report['pairOptions']:
        u, v = row['i'], row['j']
        assert 0 <= u < v < 27 and (u, v) not in options
        assert row['total'] - row['secured'] == row['cost']
        graph.add_edge(u, v, weight=row['cost'])
        options[u, v] = row
    for row in report['singleOptions']:
        u = row['i']
        assert 0 <= u < 27 and (u, 27) not in options
        assert row['total'] - row['secured'] == row['cost']
        graph.add_edge(u, 27, weight=row['cost'])
        options[u, 27] = row
    matching = nx.algorithms.matching.min_weight_matching(graph, weight='weight')
    assert len(matching) == 14
    assert {v for pair in matching for v in pair} == set(range(28))
    chosen = [options[min(u,v), max(u,v)] for u,v in matching]
    assert len({r['s7'] for r in chosen}) == 14
    optimum = sum(r['cost'] for r in chosen)
    assert 534 <= optimum <= 535, 'WIN13 sensitivity bound violated'
    assert report['emptyBoard'] == 'UNKNOWN'
    print(json.dumps({
        'updated_exact_minimum_unproved_edges':optimum,
        'fixed_plan_unproved_edges':report['after']['missing'],
        'new_s8_win':report['win8'],
        'affected_s7_candidates':report['affectedS7Parents'],
        'selected_s7_roots':sorted(r['s7'] for r in chosen),
        'selected_total_edges':sum(r['total'] for r in chosen),
        'selected_secured_edges':sum(r['secured'] for r in chosen),
        'new_s7_verdicts':0,'new_two_stone_root_closures':0,
        'empty_board':'UNKNOWN'
    },sort_keys=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative',action='store_true')
    verify(parser.parse_args().negative)
