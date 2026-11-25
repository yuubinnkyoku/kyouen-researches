#!/usr/bin/env python3
"""Independent Python audit of the fixed-14 N11 S8->S9 proof delta.

Rebuilds historical round-9..27 WIN9/LOSS9 sets from sealed witness indices,
then recomputes all 37 S8 rows and the top20 LOSS10 parent closure. Does not
import Node or verdict caches. Historical terminal leaves retain their prior
independent-verification trust boundary; the 20 new leaves are re-solved.
"""
import base64
import hashlib
import json
from pathlib import Path

import verify_python as geometry

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest_lines(lines):
    return hashlib.sha256(('\n'.join(lines) + '\n').encode()).hexdigest()


def historical_claims():
    wins, losses = set(), set()
    for n in range(9, 28):
        day = '20261028' if n <= 12 else '20261029'
        plan_dir = ('n11-s9-post-s10-reuse-round8-20261028' if n == 9 else
                    f'n11-s9-post-round{n - 1}-replan-{day}')
        cert_dir = f'n11-s9-post-round{n - 1}-round{n}-{day}'
        plan = read(EXPERIMENTS / plan_dir / 'next-plan.json')
        cert = read(EXPERIMENTS / cert_dir / 'certificate.json')
        keys = plan['newSelectedKeys']
        witnesses = base64.b64decode(cert['witnessBase64'], validate=True)
        assert len(keys) == len(witnesses) == cert['win9'] + cert['loss9'], n
        assert digest_lines(keys) == cert['selectionSha256'], n
        assert hashlib.sha256(witnesses).hexdigest() == cert['witnessSha256'], n
        assert plan['newSelectionSha256'] == cert['sourcePlanSha256'], n
        batch_wins = []
        batch_losses = set()
        for h, w in zip(keys, witnesses):
            if w == 255:
                batch_wins.append(h)
                wins.add(h)
                continue
            kids = geometry.children(int(h, 16))
            assert w < len(kids), (n, h, w)
            leaf = int(kids[w], 16)
            for pt in geometry.points(leaf):
                parent = f'{geometry.canonical(leaf ^ (1 << pt)):032x}'
                batch_losses.add(parent)
        assert batch_wins == cert['win9Keys'], n
        assert len(batch_losses) == cert['loss9ParentClosure'], n
        assert digest_lines(sorted(batch_losses)) == cert['loss9ParentSha256'], n
        losses.update(batch_losses)
    assert not wins.intersection(losses), 'historical WIN9/LOSS9 conflict'
    return wins, losses


def new_claims(cert):
    losses = set()
    for row in cert['s9LossWitnesses']:
        s9 = int(row['s9'], 16)
        kids = geometry.children(s9)
        assert kids[row['index']] == row['s10LossWitness']
        leaf = int(row['s10LossWitness'], 16)
        for pt in geometry.points(leaf):
            parent = f'{geometry.canonical(leaf ^ (1 << pt)):032x}'
            assert row['s10LossWitness'] in geometry.children(int(parent, 16))
            losses.add(parent)
    assert len(losses) == cert['s9LossParentClosure']
    assert digest_lines(sorted(losses)) == cert['s9LossParentSha256']
    return losses


def incidence_delta(audit, cert, result, old_wins, old_losses, new_losses):
    assert not old_wins.intersection(new_losses), 'new LOSS9 conflicts with WIN9'
    assert len(old_wins) == audit['certifiedWin9'] == 56
    assert len(old_losses) == audit['certifiedLoss9'] == 2669
    fresh = new_losses - old_losses
    assert len(fresh) == result['distinctNewLoss9'] == 184
    old_unknown, new_unknown, removed = set(), set(), set()
    old_edges = added_edges = unknown_edges = total_edges = 0
    fully_closed = 0
    for row in audit['s8Rows']:
        kids = set(geometry.children(int(row['h'], 16)))
        assert len(kids) == row['legal9'], row['h']
        assert not kids.intersection(old_wins), 'missing S8 has certified WIN9'
        old = kids.intersection(old_losses)
        added = kids.intersection(fresh)
        unknown_before = kids - old
        unknown_after = unknown_before - added
        assert len(old) == row['certifiedLoss9'], row['h']
        assert len(unknown_before) == row['unknown9'], row['h']
        old_edges += len(old)
        added_edges += len(added)
        unknown_edges += len(unknown_after)
        total_edges += len(kids)
        old_unknown.update(unknown_before)
        new_unknown.update(unknown_after)
        removed.update(added)
        fully_closed += not unknown_after
    computed = {
        'oldUnknown9': len(old_unknown),
        'unknown9After': len(new_unknown),
        'distinctNewUnknown9': len(removed),
        'oldUnknownEdges': total_edges - old_edges,
        'newlyCertifiedLossEdges': added_edges,
        'unknownEdgesAfter': unknown_edges,
        'fullyClosedS8': fully_closed,
    }
    for key, value in computed.items():
        assert result[key] == value, (key, result[key], value)
    assert len(audit['s8Rows']) == result['fixedPlanUnprovedS8'] == 37
    assert old_edges == audit['certifiedLoss9Edges'] == 259
    assert total_edges == audit['completeS8ToS9Edges'] == 1088
    assert len(old_unknown) == audit['distinctUnknown9'] == 799
    assert len(new_unknown) == 750 and added_edges == 69
    assert result['winLossConflicts'] == 0
    assert result['emptyBoard'] == audit['emptyBoard'] == 'UNKNOWN'
    return computed


def verify():
    geometry.verify(negative=True)
    audit = read(EXPERIMENTS / 'n11-s8-complete-child-audit-20261030' / 'incidence.json')
    cert = read(HERE / 'certificate.json')
    result = read(HERE / 'result.json')
    old_wins, old_losses = historical_claims()
    new_losses = new_claims(cert)
    computed = incidence_delta(audit, cert, result, old_wins, old_losses, new_losses)
    altered = dict(result, newlyCertifiedLossEdges=result['newlyCertifiedLossEdges'] + 1)
    try:
        incidence_delta(audit, cert, altered, old_wins, old_losses, new_losses)
    except AssertionError:
        pass
    else:
        raise AssertionError('tampered delta accepted')
    print(json.dumps({'verified': True, 'language': 'Python',
                      'historicalBatches': 19, 'oldWin9': len(old_wins),
                      'oldLoss9': len(old_losses), 'newLoss9': len(new_losses),
                      **computed, 'emptyBoard': 'UNKNOWN'}, indent=2))


if __name__ == '__main__':
    verify()
