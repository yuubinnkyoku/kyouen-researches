#!/usr/bin/env python3
"""Independent Python replay of sixth N11 direct LOSS8 certificate.

Uses integer 3x3 determinant geometry and terminal recursion, no verdict cache.
--full checks all 364 ten-stone children; --negative tests actual rejection.
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

def verify(c, full=False):
    assert c['schema'] == 'n11-s8-sixth-direct-loss-v1'
    assert c['board'] == 11 and c['emptyBoard'] == 'UNKNOWN'
    assert c['verdict'] == 'LOSS'
    root = c['root']
    b = int(root, 16)
    assert len(g.points(b)) == 8 and f'{g.canonical(b):032x}' == root
    s9 = set(g.children(b))
    assert len(s9) == c['legal9'] == 32
    incidence = {}
    for p in s9:
        for h in g.children(int(p, 16)):
            incidence.setdefault(h, set()).add(p)
    assert len(incidence) == c['distinct10'] == 364
    assert all(len(pp) == 2 for pp in incidence.values())
    selected, covered = set(), set()
    selected_states = 0
    assert len(c['witnesses']) == c['selectedLoss10'] == 16
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
    assert selected_states == c['terminalStatesSelected'] == 2517
    # Every S10 child covers at most two distinct S9 children:
    # 32 vertices require >=ceil(32/2)=16 leaves.
    assert c['minimumWitnesses'] == 16
    parents = sorted(f'{g.canonical(b ^ (1 << p)):032x}' for p in g.points(b))
    assert parents == c['s7Parents'] and len(parents) == 8
    for p in parents:
        assert root in g.children(int(p, 16))
    losses = None
    if full:
        wins, states, losses = 0, 0, []
        for h in sorted(incidence):
            win, count, _ = g.solve10(h)
            states += count
            if win:
                wins += 1
            else:
                losses.append(h)
        assert wins == c['win10'] == 284
        assert len(losses) == c['loss10'] == 80
        assert states == c['terminalStatesFull'] == 48648
        assert selected <= set(losses)
        closure = sorted({f'{g.canonical(int(h,16) ^ (1 << p)):032x}'
                          for h in losses for p in g.points(int(h,16))})
        digest = hashlib.sha256(('\n'.join(closure)+'\n').encode()).hexdigest()
        assert len(closure) == c['loss9ParentClosure'] == 672
        assert digest == c['loss9ParentSha256']
        for h in losses:
            for p in g.points(int(h, 16)):
                par = f'{g.canonical(int(h,16) ^ (1 << p)):032x}'
                assert h in g.children(int(par,16))
    return {'verified': True, 'root': root, 'verdict': 'LOSS',
            'legal9': len(s9), 'selectedLoss10': len(selected),
            'terminalStatesSelected': selected_states,
            'fullScan': full, 'loss10': len(losses) if full else None,
            'emptyBoard': 'UNKNOWN'}

def negative(c):
    changes = [
        lambda x: x['witnesses'].pop(),
        lambda x: x['witnesses'][0].update(s10=x['witnesses'][1]['s10']),
        lambda x: x['witnesses'][0].update(terminalStates=0),
        lambda x: x['witnesses'][0].update(legalMoves=0),
        lambda x: x.update(root='0'*32),
        lambda x: x.update(emptyBoard='WIN'),
    ]
    for change in changes:
        forged = json.loads(json.dumps(c))
        change(forged)
        try:
            verify(forged)
        except (AssertionError, KeyError, ValueError, IndexError):
            continue
        raise AssertionError('forged certificate accepted')

if __name__ == '__main__':
    cert = read('certificate.json')
    full = '--full' in sys.argv
    result = verify(cert, full=full)
    if '--negative' in sys.argv:
        negative(cert)
    print(json.dumps(result, indent=2))
