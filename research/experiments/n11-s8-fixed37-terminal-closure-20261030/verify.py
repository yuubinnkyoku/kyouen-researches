#!/usr/bin/env python3
"""Independent Python verification of all 37 fixed-plan N11 eight-stone roots.

Certificate stores indices, not trusted verdict-cache values. WIN8 requires
one S9 child with ALL S10 children WIN; LOSS8 requires LOSS10 replies covering
EVERY S9 child. The S10 games are solved recursively from integer geometry.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'n11-s9-full-child-top20-loss9-20261030'))
import verify_python as g

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def verify(c, full=False):
    assert c['schema'] == 'n11-fixed14-37-s8-direct-terminal-v1'
    assert c['board'] == 11 and c['emptyBoard'] == 'UNKNOWN'
    audit = read(HERE.parent / 'n11-s8-complete-child-audit-20261030' / 'incidence.json')
    roots = [r['h'] for r in audit['s8Rows']]
    assert len(roots) == 37
    assert [r[0] for r in c['rows']] == roots
    selected, selected_states, wins, losses = 0, 0, 0, 0
    full_boundary, full_states = 0, 0
    for root, verdict, indices in c['rows']:
        b = int(root,16)
        assert len(g.points(b)) == 8 and f'{g.canonical(b):032x}' == root
        s9 = g.children(b)
        incidence = {}
        for p in s9:
            for h in g.children(int(p,16)):
                incidence.setdefault(h,set()).add(p)
        s10 = sorted(incidence)
        if verdict == 'W':
            assert isinstance(indices,int) and 0 <= indices < len(s9)
            target = s9[indices]
            witnesses = g.children(int(target,16))
            assert witnesses and set(witnesses) <= set(s10)
            for h in witnesses:
                result, states, _ = g.solve10(h)
                assert result, ('false WIN10',root,h)
                selected += 1
                selected_states += states
            wins += 1
        else:
            assert verdict == 'L' and isinstance(indices,list) and indices
            assert len(set(indices)) == len(indices)
            covered = set()
            for i in indices:
                assert isinstance(i,int) and 0 <= i < len(s10)
                h = s10[i]
                result, states, _ = g.solve10(h)
                assert not result, ('false LOSS10',root,h)
                covered.update(incidence[h])
                selected += 1
                selected_states += states
            assert covered == set(s9), ('uncovered S9',root)
            losses += 1
        if full:
            leaf_verdicts = {}
            for h in s10:
                result, states, _ = g.solve10(h)
                leaf_verdicts[h] = result
                full_states += states
            full_boundary += len(s10)
            has_loss9 = any(all(leaf_verdicts[h] for h in
                                   g.children(int(p,16))) for p in s9)
            assert has_loss9 == (verdict == 'W'), ('full-scan disagreement',root)
    assert (wins,losses) == (c['win8'],c['loss8']) == (8,29)
    assert selected == c['terminalWitnesses'] == 612
    assert selected_states == c['terminalStatesSelected'] == 92603
    if full:
        assert full_boundary == c['fullScanDistinct10WithMultiplicity'] == 11884
        assert full_states == c['fullScanTerminalStatesWithMultiplicity'] == 1625006
    return {'verified':True,'fixedPlanRoots':len(roots),'win8':wins,
            'loss8':losses,'selectedTerminalLeaves':selected,
            'selectedTerminalStates':selected_states,
            'fullScan':full,'emptyBoard':'UNKNOWN'}

def negative(c):
    def reject(change):
        forged = json.loads(json.dumps(c))
        change(forged)
        try:
            verify(forged)
        except (AssertionError,KeyError,IndexError,ValueError,TypeError):
            return
        raise AssertionError('forged certificate accepted')
    reject(lambda x: x['rows'][0].__setitem__(1,'L'))
    reject(lambda x: x['rows'][1].__setitem__(1,'W'))
    reject(lambda x: x['rows'][1][2].pop())
    reject(lambda x: x['rows'][1][2].__setitem__(0,100000))
    reject(lambda x: x['rows'][0].__setitem__(2,100000))
    reject(lambda x: x['rows'][0].__setitem__(0,'0'*32))
    reject(lambda x: x.update(terminalStatesSelected=0))
    reject(lambda x: x.update(emptyBoard='WIN'))

if __name__ == '__main__':
    cert = read(HERE/'certificate.json')
    result = verify(cert,full='--full' in sys.argv)
    if '--negative' in sys.argv:
        negative(cert)
    print(json.dumps(result,indent=2))
