#!/usr/bin/env python3
"""Rebuild fixed-14 S8 frontier after the fourth terminal-only LOSS8 proof.

Historical sealed proof sets are used only as previously certified inputs.
No UNKNOWN is promoted from a partial df-pn search.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s9-full-child-top20-loss9-20261030'))
from verify_full_incidence import historical_claims, new_claims
from verify_single import verify_terminal
import verify_python as g
sys.path.insert(0, str(EXP / 'n11-s8-direct-loss-perfect-matching-20261030'))
from audit_full_loss_closure import verify_manifest
sys.path.insert(0, str(HERE))
from verify import verify as verify_fourth


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def run():
    top = EXP / 'n11-s9-full-child-top20-loss9-20261030'
    first = EXP / 'n11-s8-direct-loss-perfect-matching-20261030'
    second = EXP / 'n11-s8-second-direct-loss-20261030'
    third = EXP / 'n11-s8-third-direct-loss-20261030'
    wins, losses = historical_claims()
    losses |= new_claims(read(top / 'certificate.json'))
    losses |= verify_terminal(read(top / 'single_s9_certificate.json'),
                              read(top / 'post_top20_frontier.json'))
    first_closure, states = verify_manifest(read(first / 'full_loss_closure.json'))
    assert states == 20997 and len(first_closure) == 684
    losses |= first_closure
    losses |= set(read(second / 'full_loss_closure.json')['loss9ParentKeys'])
    assert len(wins) == 56 and len(losses) == 3996
    third_closure = set(read(third / 'full_loss_closure.json')['loss9ParentKeys'])
    assert len(third_closure) == 703
    losses |= third_closure
    assert len(losses) == 4468
    assert not wins & losses

    c = read(HERE / 'certificate.json')
    proof, incoming, loss10 = verify_fourth(c, full=True)
    assert proof['s8Verdict'] == 'LOSS'
    assert proof['fullScan']['loss9Parents'] == 664
    incoming = set(incoming)
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
        if len(new) != len(old):
            changed.append({'s8': row['h'], 'before': len(old), 'after': len(new)})
    assert len(before) == 684 and before_edges == 690
    assert len(closed_before) == 3
    assert c['root'] in closed_after
    assert before_edges - after_edges == sum(x['before'] - x['after'] for x in changed)
    report = {
        'schema': 'n11-fourth-loss8-fixed14-frontier-v1',
        'emptyBoard': 'UNKNOWN',
        'historicalWin9': len(wins),
        'priorKnownLoss9': len(losses),
        'fourthLoss10': len(loss10),
        'fourthLoss9ParentClosure': len(incoming),
        'fourthLoss9BeyondPriorProofSets': len(fresh),
        'unknown9Before': len(before),
        'unknown9After': len(after),
        'unknownEdgesBefore': before_edges,
        'unknownEdgesAfter': after_edges,
        'newlyCertifiedLossEdges': before_edges - after_edges,
        'closedS8Before': closed_before,
        'closedS8After': closed_after,
        'remainingUnprovedS8Of37': 37 - len(closed_after),
        'winLossConflicts': 0,
        'twoStoneRootClosureChecked': False,
        'changedRows': changed,
    }
    frozen = HERE / 'frontier_result.json'
    if frozen.exists():
        assert report == read(frozen), 'frozen frontier mismatch'
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    run()
