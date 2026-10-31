#!/usr/bin/env python3
"""Rebuild the fixed-14 S8 frontier after sixth direct terminal LOSS8.

Only independently replayed terminal leaves and sealed historical proof sets
enter the verdict set. Unknown/partial df-pn states are never promoted.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
TOP = EXP / 'n11-s9-full-child-top20-loss9-20261030'
sys.path.insert(0, str(TOP))
from verify_full_incidence import historical_claims, new_claims
from verify_single import verify_terminal
import verify_python as g
sys.path.insert(0, str(EXP / 'n11-s8-direct-loss-perfect-matching-20261030'))
from audit_full_loss_closure import verify_manifest
sys.path.insert(0, str(HERE))
from verify import verify as verify_sixth

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def independent_verify(path):
    spec = importlib.util.spec_from_file_location('n11_'+path.name+'_verify', path / 'verify.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.verify(mod.read('certificate.json'), full=True)

def run():
    wins, losses = historical_claims()
    losses |= new_claims(read(TOP / 'certificate.json'))
    losses |= verify_terminal(read(TOP / 'single_s9_certificate.json'),
                              read(TOP / 'post_top20_frontier.json'))
    first = EXP / 'n11-s8-direct-loss-perfect-matching-20261030'
    first_closure, states = verify_manifest(read(first / 'full_loss_closure.json'))
    assert states == 20997 and len(first_closure) == 684
    losses |= first_closure
    second = EXP / 'n11-s8-second-direct-loss-20261030'
    third = EXP / 'n11-s8-third-direct-loss-20261030'
    losses |= set(read(second / 'full_loss_closure.json')['loss9ParentKeys'])
    assert len(wins) == 56 and len(losses) == 3996
    losses |= set(read(third / 'full_loss_closure.json')['loss9ParentKeys'])
    assert len(losses) == 4468
    fourth = EXP / 'n11-s8-fourth-direct-loss-20261030'
    _, fourth_closure, _ = independent_verify(fourth)
    assert len(fourth_closure) == 664
    losses |= set(fourth_closure)
    assert len(losses) == 4849
    fifth = EXP / 'n11-s8-fifth-direct-loss-20261030'
    _, fifth_closure, _ = independent_verify(fifth)
    assert len(fifth_closure) == 851
    losses |= set(fifth_closure)
    assert len(losses) == 5373
    assert not wins & losses

    c = read(HERE / 'certificate.json')
    proof = verify_sixth(c, full=True)
    assert proof['verdict'] == 'LOSS' and proof['loss10'] == 80
    incoming = set()
    # Reconstruct the entire 672-parent closure from independently recomputed
    # terminal verdicts. This does not trust any external cache.
    root = int(c['root'], 16)
    s9 = set(g.children(root))
    boundary = {h for p in s9 for h in g.children(int(p, 16))}
    assert len(boundary) == 364
    loss10 = []
    for h in sorted(boundary):
        if not g.solve10(h)[0]:
            loss10.append(h)
            leaf = int(h, 16)
            incoming.update(f'{g.canonical(leaf ^ (1 << p)):032x}'
                            for p in g.points(leaf))
    assert len(loss10) == 80 and len(incoming) == 672
    assert not wins & incoming, 'WIN9/LOSS9 conflict'
    fresh = incoming - losses

    audit = read(EXP / 'n11-s8-complete-child-audit-20261030' / 'incidence.json')
    before, after = set(), set()
    before_edges = after_edges = 0
    closed_before, closed_after, changed = [], [], []
    for row in audit['s8Rows']:
        children = set(g.children(int(row['h'], 16)))
        assert len(children) == row['legal9']
        assert not children & wins
        old = children - losses
        new = old - fresh
        before.update(old)
        after.update(new)
        before_edges += len(old)
        after_edges += len(new)
        if not old:
            closed_before.append(row['h'])
        if not new:
            closed_after.append(row['h'])
        if len(old) != len(new):
            changed.append({'s8':row['h'],'before':len(old),'after':len(new)})
    assert len(before) == 659 and before_edges == 664
    assert len(closed_before) == 5 and c['root'] in closed_after
    assert before_edges - after_edges == sum(x['before']-x['after'] for x in changed)
    report = {
        'schema':'n11-sixth-loss8-fixed14-frontier-v1',
        'emptyBoard':'UNKNOWN',
        'historicalWin9':len(wins),
        'priorKnownLoss9':len(losses),
        'sixthLoss10':len(loss10),
        'sixthLoss9ParentClosure':len(incoming),
        'sixthLoss9BeyondPriorProofSets':len(fresh),
        'unknown9Before':len(before),
        'unknown9After':len(after),
        'unknownEdgesBefore':before_edges,
        'unknownEdgesAfter':after_edges,
        'newlyCertifiedLossEdges':before_edges-after_edges,
        'closedS8Before':closed_before,
        'closedS8After':closed_after,
        'remainingUnprovedS8Of37':37-len(closed_after),
        'winLossConflicts':0,
        'twoStoneRootClosureChecked':False,
        'changedRows':changed,
    }
    frozen = HERE / 'frontier_result.json'
    if frozen.exists():
        assert report == read(frozen), 'frozen frontier mismatch'
    print(json.dumps(report, indent=2))
    return report

if __name__ == '__main__':
    run()
