#!/usr/bin/env python3
"""Minimum-weight perfect matching for the terminal-proved degree-two S9 extension."""
import argparse
import json
from pathlib import Path
import subprocess
import networkx as nx

HERE=Path(__file__).resolve().parent
EXP=HERE.parent

def verify(negative=False):
    subprocess.check_call(['node',str(EXP /
      'n11-s9-degree2-terminal-20261027'/'verify.js'),
      *(['--negative'] if negative else [])])
    raw=subprocess.check_output(['node',str(HERE/'audit.js'),
      *(['--negative'] if negative else [])],text=True)
    report=json.loads(raw)
    assert report['schema']=='n11-s5-post-degree2-matching-v1'
    assert report['missingS6']==27
    assert report['proofOnlyWin8Before']==2315
    assert report['proofOnlyWin8After']==2433
    assert report['knownLoss8']==338
    assert report['newlyProvedS8']==118
    assert report['candidates']==853 and report['allowed']==786
    assert report['excluded']==67
    assert len(report['pairOptions'])==343
    assert len(report['singleOptions'])==27
    assert report['previous']['missing']==480
    assert report['updated']['missing']==460
    graph=nx.Graph()
    graph.add_nodes_from(range(28))
    options={}
    for r in report['pairOptions']:
        u,v=r['i'],r['j']
        assert 0<=u<v<27 and (u,v) not in options
        assert r['total']-r['secured']==r['cost']
        graph.add_edge(u,v,weight=r['cost'])
        options[u,v]=r
    for r in report['singleOptions']:
        u=r['i']
        assert 0<=u<27 and (u,27) not in options
        assert r['total']-r['secured']==r['cost']
        graph.add_edge(u,27,weight=r['cost'])
        options[u,27]=r
    matching=nx.algorithms.matching.min_weight_matching(graph,weight='weight')
    assert len(matching)==14
    assert {u for edge in matching for u in edge}==set(range(28))
    selected=[options[min(u,v),max(u,v)] for u,v in matching]
    assert len({r['s7'] for r in selected})==14
    optimum=sum(r['cost'] for r in selected)
    assert optimum<=460, 'matching exceeds fixed-plan bound'
    assert optimum==sum(graph[u][v]['weight'] for u,v in matching)
    result={
      'scope':'conditional 14-S7 witness roots only',
      'minimum_unproved_edges':optimum,
      'fixed_plan_unproved_edges':460,
      'improvement_over_fixed_plan':460-optimum,
      'selected_s7_roots':sorted(r['s7'] for r in selected),
      'selected_total_edges':sum(r['total'] for r in selected),
      'selected_secured_edges':sum(r['secured'] for r in selected),
      'affected_s7_candidates':report['affectedValidS7'],
      'reduced_pair_options':report['reducedPairCosts'],
      'reduced_single_options':report['reducedSingleCosts'],
      'known_proof_only_win8':2433,
      'new_s7_verdicts':0,'new_s5_verdicts':0,
      'two_stone_root_closures':0,'empty_board':'UNKNOWN'
    }
    print(json.dumps(result,sort_keys=True))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative',action='store_true')
    verify(parser.parse_args().negative)
