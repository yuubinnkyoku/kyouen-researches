#!/usr/bin/env python3
"""Independent Python replay of fourth N11 direct LOSS8 terminal certificate.

Uses integer 3x3 geometry and terminal recursion; no solver verdict cache.
All 573 ten-stone children are recomputed in --full mode.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'n11-s9-full-child-top20-loss9-20261030'))
import verify_python as g


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def verify(c, full=False, known_losses=None):
    assert c['schema'] == 'n11-s8-fourth-direct-loss-v1'
    assert c['board'] == 11 and c['emptyBoard'] == 'UNKNOWN'
    assert c['verdict'] == 'LOSS'
    root = c['root']
    b = int(root, 16)
    assert len(g.points(b)) == 8 and f'{g.canonical(b):032x}' == root
    s9 = set(g.children(b))
    assert len(s9) == c['legal9'] == 40
    incidence = {}
    for p in s9:
        for h in g.children(int(p, 16)):
            incidence.setdefault(h, set()).add(p)
    assert len(incidence) == c['distinct10'] == 573
    assert all(len(pp) == 2 for pp in incidence.values())

    selected = set()
    covered = set()
    selected_states = 0
    assert len(c['witnesses']) == c['selectedLoss10'] == 21
    for row in c['witnesses']:
        h = row['s10']
        assert h in incidence and h not in selected
        selected.add(h)
        win, states, moves = g.solve10(h)
        assert not win and states == row['terminalStates']
        assert moves == row['legalMoves']
        selected_states += states
        covered.update(incidence[h])
    assert covered == s9
    assert selected_states == c['terminalStatesSelected'] == 6070
    parents = sorted(f'{g.canonical(b ^ (1 << p)):032x}' for p in g.points(b))
    assert parents == c['s7Parents'] and len(parents) == 8
    for p in parents:
        assert root in g.children(int(p, 16))

    losses = known_losses
    wins = None
    states = None
    if full:
        losses = []
        wins = states = 0
        for h in sorted(incidence):
            win, count, _ = g.solve10(h)
            states += count
            if win:
                wins += 1
            else:
                losses.append(h)
        assert wins == c['win10'] == 495
        assert len(losses) == c['loss10'] == 78
        assert states == c['terminalStatesFull'] == 110563

    closure = None
    if losses is not None:
        assert len(losses) == c['loss10'] == 78
        assert len(set(losses)) == len(losses)
        assert set(losses) <= incidence.keys()
        assert selected <= set(losses)
        removed = set(c['matchingBarrierRemovedVertices'])
        isolated = set(c['matchingBarrierIsolatedVertices'])
        assert len(removed) == 3 and len(isolated) == 5
        assert removed <= s9 and isolated <= s9 and not removed & isolated
        for v in isolated:
            edges = [incidence[h] for h in losses if v in incidence[h]]
            assert edges  # no isolated vertices in the original LOSS10 graph
            assert all((pp - {v}) <= removed for pp in edges)
        # Removing 3 vertices leaves 5 isolated vertices. Any matching
        # leaves at least 2 of them unmatched; matching <= (40-2)/2 = 19.
        # Thus an edge cover needs >= 40-19 = 21 edges, attained above.
        assert c['minimumWitnesses'] == 21
        closure = sorted({f'{g.canonical(int(h,16) ^ (1 << p)):032x}'
                          for h in losses for p in g.points(int(h,16))})
        digest = hashlib.sha256(('\n'.join(closure) + '\n').encode()).hexdigest()
        assert len(closure) == c['loss9ParentClosure'] == 664
        assert digest == c['loss9ParentSha256']
        if full:
            for h in losses:
                for p in g.points(int(h, 16)):
                    par = f'{g.canonical(int(h,16) ^ (1 << p)):032x}'
                    assert h in g.children(int(par,16))

    result = {'verified': True, 's8': root, 's8Verdict': 'LOSS',
              'legal9': len(s9), 'selectedLoss10': len(selected),
              'terminalStatesSelected': selected_states, 'emptyBoard': 'UNKNOWN'}
    if full:
        result['fullScan'] = {'win10': wins, 'loss10': len(losses),
                              'loss9Parents': len(closure), 'states': states,
                              'minimumLoss10Witnesses': 21}
    return result, closure, losses


def negative(c, losses):
    def reject(mutate):
        forged = json.loads(json.dumps(c))
        mutate(forged)
        try:
            verify(forged, known_losses=losses)
        except (AssertionError, KeyError, IndexError, ValueError):
            return
        raise AssertionError('forged certificate accepted')
    reject(lambda x: x['witnesses'].pop())
    reject(lambda x: x['witnesses'][0].update(s10=x['witnesses'][1]['s10']))
    reject(lambda x: x['witnesses'][0].update(terminalStates=0))
    reject(lambda x: x['witnesses'][0].update(legalMoves=0))
    reject(lambda x: x.update(root='0'*32))
    reject(lambda x: x['matchingBarrierIsolatedVertices'].pop())
    reject(lambda x: x['matchingBarrierRemovedVertices'].pop())
    reject(lambda x: x.update(loss9ParentSha256='0'*64))
    reject(lambda x: x.update(emptyBoard='WIN'))


if __name__ == '__main__':
    cert = read('certificate.json')
    full = '--full' in sys.argv
    result, _, losses = verify(cert, full=full)
    if '--negative' in sys.argv:
        assert full, 'negative barrier tests require --full'
        negative(cert, losses)
    print(json.dumps(result, indent=2))
