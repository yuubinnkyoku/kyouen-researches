#!/usr/bin/env python3
"""Independent Python replay of fifth N11 direct LOSS8 terminal certificate.

Uses integer 3x3 geometry and terminal recursion; no solver verdict cache.
All 449 ten-stone children are recomputed in --full mode.
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
    assert c['schema'] == 'n11-s8-fifth-direct-loss-v1'
    assert c['board'] == 11 and c['emptyBoard'] == 'UNKNOWN'
    assert c['verdict'] == 'LOSS'
    root = c['root']
    b = int(root, 16)
    assert len(g.points(b)) == 8 and f'{g.canonical(b):032x}' == root
    s9 = set(g.children(b))
    assert len(s9) == c['legal9'] == 35
    incidence = {}
    for p in s9:
        for h in g.children(int(p, 16)):
            incidence.setdefault(h, set()).add(p)
    assert len(incidence) == c['distinct10'] == 449
    assert all(len(pp) == 2 for pp in incidence.values())

    selected = set()
    covered = set()
    selected_states = 0
    assert len(c['witnesses']) == c['selectedLoss10'] == 18
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
    assert selected_states == c['terminalStatesSelected'] == 4271
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
        assert wins == c['win10'] == 347
        assert len(losses) == c['loss10'] == 102
        assert states == c['terminalStatesFull'] == 98136

    closure = None
    if losses is not None:
        assert len(losses) == c['loss10'] == 102
        assert len(set(losses)) == len(losses)
        assert set(losses) <= incidence.keys()
        assert selected <= set(losses)
        # Every LOSS10 edge has exactly two S9 parents; 35 vertices need >=18 edges.
        assert c['minimumWitnesses'] == 18
        closure = sorted({f'{g.canonical(int(h,16) ^ (1 << p)):032x}'
                          for h in losses for p in g.points(int(h,16))})
        digest = hashlib.sha256(('\n'.join(closure) + '\n').encode()).hexdigest()
        assert len(closure) == c['loss9ParentClosure'] == 851
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
                              'minimumLoss10Witnesses': 18}
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
    reject(lambda x: x.update(loss9ParentSha256='0'*64))
    reject(lambda x: x.update(emptyBoard='WIN'))


if __name__ == '__main__':
    cert = read('certificate.json')
    full = '--full' in sys.argv
    result, _, losses = verify(cert, full=full)
    if '--negative' in sys.argv:
        assert full, 'negative tests require --full'
        negative(cert, losses)
    print(json.dumps(result, indent=2))
