#!/usr/bin/env python3
"""Replay all 81 LOSS10 leaves and audit their 684 LOSS9 parents against fixed14.

Unlike the original 18-leaf proof, this uses the *entire* 480-leaf boundary.
Every claimed LOSS10 leaf is solved afresh; historical claims are reconstructed
from their sealed witness indices rather than trusting a verdict cache.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s9-full-child-top20-loss9-20261030'))
from verify_full_incidence import historical_claims, new_claims
from verify_single import verify_terminal
import verify_python as g


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(keys):
    return hashlib.sha256(('\n'.join(keys) + '\n').encode()).hexdigest()


def verify_manifest(manifest):
    assert manifest['schema'] == 'n11-s8-full-loss10-parent-closure-v1'
    assert manifest['emptyBoard'] == 'UNKNOWN'
    leaves = manifest['loss10Keys']
    claimed = manifest['loss9ParentKeys']
    assert leaves == sorted(set(leaves)) and len(leaves) == 81
    assert claimed == sorted(set(claimed)) and len(claimed) == 684
    assert digest(leaves) == manifest['loss10KeysSha256']
    assert digest(claimed) == manifest['loss9ParentSha256']
    all_parents = set()
    states = 0
    for h in leaves:
        b = int(h, 16)
        assert len(g.points(b)) == 10 and g.canonical(b) == b
        verdict, count, _ = g.solve10(h)
        assert verdict is False, 'false LOSS10: ' + h
        states += count
        for pt in g.points(b):
            parent = f'{g.canonical(b ^ (1 << pt)):032x}'
            assert h in g.children(int(parent, 16)), 'invalid parent incidence'
            all_parents.add(parent)
    assert sorted(all_parents) == claimed, 'incomplete LOSS9 parent closure'
    return all_parents, states


def run():
    manifest = read(HERE / 'full_loss_closure.json')
    new_loss9, states = verify_manifest(manifest)
    old_wins, old_losses = historical_claims()
    top20 = new_claims(read(EXP / 'n11-s9-full-child-top20-loss9-20261030/certificate.json'))
    one = verify_terminal(
        read(EXP / 'n11-s9-full-child-top20-loss9-20261030/single_s9_certificate.json'),
        read(EXP / 'n11-s9-full-child-top20-loss9-20261030/post_top20_frontier.json'))
    known = old_losses | top20 | one
    assert not old_wins.intersection(new_loss9), 'WIN9/LOSS9 conflict'
    fresh = new_loss9 - known
    audit = read(EXP / 'n11-s8-complete-child-audit-20261030/incidence.json')
    before_classes, after_classes = set(), set()
    before_edges = after_edges = gained_edges = 0
    closed = []
    rows = []
    for row in audit['s8Rows']:
        kids = set(g.children(int(row['h'], 16)))
        assert len(kids) == row['legal9']
        assert not kids.intersection(old_wins), 'certified WIN9 in unproved S8'
        before = kids - known
        after = before - fresh
        gained = len(before) - len(after)
        before_classes.update(before)
        after_classes.update(after)
        before_edges += len(before)
        after_edges += len(after)
        gained_edges += gained
        if not after:
            closed.append(row['h'])
        rows.append({'s8': row['h'], 'unknownBefore': len(before),
                     'newLoss9Edges': gained, 'unknownAfter': len(after)})
    assert len(before_classes) == 748 and before_edges == 758, (
        len(before_classes), before_edges)
    assert len(rows) == 37 and gained_edges == before_edges - after_edges
    root = manifest['s8']
    assert root == '00012010000000821080000000000020'
    assert root in closed, '81 LOSS10 leaves do not close their S8 root'
    result = {
        'schema': 'n11-s8-full-loss10-frontier-lift-v1',
        'emptyBoard': 'UNKNOWN',
        'replayedLoss10': len(manifest['loss10Keys']),
        'terminalStates': states,
        'loss9ParentClosure': len(new_loss9),
        'loss9FreshBeyondHistoricalTop20Single': len(fresh),
        'unknown9Before': len(before_classes),
        'unknown9After': len(after_classes),
        'unknownEdgesBefore': before_edges,
        'newlyCertifiedLossEdges': gained_edges,
        'unknownEdgesAfter': after_edges,
        'closedS8IncludingPreviouslyProvedRoot': len(closed),
        'closedS8Keys': sorted(closed),
        'remainingUnprovedS8OfOriginal37': 37 - len(closed),
        'winLossConflicts': 0,
        'newTwoStoneRootClosures': 0,
        's8Rows': rows
    }
    frozen = HERE / 'full_loss_closure_result.json'
    if frozen.exists():
        assert result == read(frozen), 'frozen frontier delta mismatch'
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    if '--negative' in sys.argv:
        original = read(HERE / 'full_loss_closure.json')
        for mutate in (
            lambda x: x['loss10Keys'].pop(),
            lambda x: x['loss9ParentKeys'].pop(),
            lambda x: x.update(loss10KeysSha256='0' * 64),
            lambda x: x.update(loss9ParentSha256='0' * 64),
            lambda x: x.update(emptyBoard='WIN')
        ):
            altered = json.loads(json.dumps(original))
            mutate(altered)
            try:
                verify_manifest(altered)
            except (AssertionError, KeyError, ValueError):
                pass
            else:
                raise AssertionError('forged full-boundary closure accepted')
    run()
