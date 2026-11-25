#!/usr/bin/env python3
"""Independent Python terminal replay of the third 11x11 LOSS8 proof.

Reuses only the Python integer 3x3 geometry/terminal recursion, not JS or a
verdict cache. --full checks all 548 ten-stone children and 703 LOSS9 parents.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'n11-s9-full-child-top20-loss9-20261030'))
import verify_python as g


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def verify(c, full=None):
    assert c['schema'] == 'n11-s8-third-direct-loss-v1'
    assert c['board'] == 11 and c['emptyBoard'] == 'UNKNOWN'
    assert c['verdict'] == 'LOSS'
    root = c['root']
    b = int(root, 16)
    assert len(g.points(b)) == 8 and f'{g.canonical(b):032x}' == root
    s9 = set(g.children(b))
    assert len(s9) == c['legal9'] == 39
    incidence = {}
    for p in s9:
        for h in g.children(int(p, 16)):
            incidence.setdefault(h, set()).add(p)
    assert len(incidence) == c['distinct10'] == 548
    assert all(len(parents) == 2 for parents in incidence.values())

    selected, covered, selected_states = set(), set(), 0
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
    assert covered == s9 and selected_states == c['terminalStatesSelected'] == 7364
    parents = sorted(f'{g.canonical(b ^ (1 << p)):032x}' for p in g.points(b))
    assert parents == c['s7Parents'] and len(parents) == 8
    for p in parents:
        assert root in g.children(int(p, 16))

    out = {'verified': True, 's8': root, 's8Verdict': 'LOSS',
           'legal9': 39, 'selectedLoss10': 21,
           'terminalStatesSelected': selected_states, 'emptyBoard': 'UNKNOWN'}
    if full is not None:
        assert full['schema'] == 'n11-s8-third-full-loss10-closure-v1'
        assert full['board'] == 11 and full['emptyBoard'] == 'UNKNOWN'
        assert full['root'] == root and full['distinct10'] == 548
        losses, wins, states = [], 0, 0
        for h in sorted(incidence):
            win, count, _ = g.solve10(h)
            states += count
            if win:
                wins += 1
            else:
                losses.append(h)
        assert wins == c['win10'] == full['win10'] == 465
        assert losses == full['loss10Keys'] and len(losses) == c['loss10'] == full['loss10'] == 83
        assert states == c['terminalStatesFull'] == full['terminalStatesFull'] == 114792
        closure = sorted({f'{g.canonical(int(h,16) ^ (1 << p)):032x}'
                          for h in losses for p in g.points(int(h, 16))})
        assert closure == full['loss9ParentKeys'] and len(closure) == 703
        for h in losses:
            for p in g.points(int(h, 16)):
                parent = f'{g.canonical(int(h, 16) ^ (1 << p)):032x}'
                assert h in g.children(int(parent, 16))
        U = set(c['matchingUpperBoundIndependentSet'])
        assert len(U) == len(c['matchingUpperBoundIndependentSet']) == 14
        assert U <= s9
        neighbors = set()
        for h in losses:
            pp = incidence[h]
            assert len(pp & U) <= 1
            if pp & U:
                neighbors.update(pp - U)
        assert len(neighbors) == 11 and not neighbors & U
        # Matching <= (39 - (14-11)) / 2 = 18; edge cover >= 21.
        assert c['minimumWitnesses'] == c['selectedLoss10'] == 21
        out['fullScan'] = {'win10': wins, 'loss10': len(losses),
                           'loss9Parents': len(closure), 'states': states,
                           'independentSet': 14, 'neighbors': 11,
                           'minimumLoss10Witnesses': 21}
    return out


def negative(c, full):
    def reject(mutate):
        forged = json.loads(json.dumps(c))
        mutate(forged)
        try:
            verify(forged, full)
        except (AssertionError, KeyError, IndexError, ValueError):
            return
        raise AssertionError('forged certificate accepted')
    reject(lambda x: x['witnesses'].pop())
    reject(lambda x: x['witnesses'][0].update(s10=x['witnesses'][1]['s10']))
    reject(lambda x: x['witnesses'][0].update(terminalStates=0))
    reject(lambda x: x['witnesses'][0].update(legalMoves=0))
    reject(lambda x: x.update(root='0'*32))
    reject(lambda x: x['matchingUpperBoundIndependentSet'].pop())
    reject(lambda x: x.update(emptyBoard='WIN'))


if __name__ == '__main__':
    cert = read('certificate.json')
    full = read('full_loss_closure.json') if '--full' in sys.argv else None
    result = verify(cert, full)
    if '--negative' in sys.argv:
        negative(cert, full)
    print(json.dumps(result, indent=2))
