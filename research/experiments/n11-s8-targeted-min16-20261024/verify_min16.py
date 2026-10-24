#!/usr/bin/env python3
"""Independent Bareiss 4x4 verification of the optimal 16-leaf S8 LOSS proof.

No cached outcomes or solver verdicts are used. The imported integer geometry
and terminal solver were independently implemented before this certificate.
"""
from pathlib import Path
from itertools import combinations
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'n11-s8-targeted-closure-20261015'))
import verify_terminal_independent as g

ROOT = '00000000000040001000044400830000'

def verify(keys, *, terminal=True, full=False):
    assert len(keys) == len(set(keys)) == 16, 'wrong/duplicate leaf count'
    assert all(len(h) == 32 and all(c in '0123456789abcdef' for c in h)
               for h in keys), 'invalid leaf key'
    root = int(ROOT, 16)
    assert g.canonical(root) == root
    assert len(g.points(root)) == 8
    assert all(not g.forbidden(*q) for q in combinations(g.points(root), 4))
    obligations = g.children(root)
    assert len(obligations) == 31
    boundary = {}
    for s9 in obligations:
        assert len(g.points(s9)) == 9 and g.canonical(s9) == s9
        for s10 in g.children(s9):
            boundary.setdefault(s10, set()).add(s9)
    assert len(boundary) == 378
    # Every candidate leaf, including WIN candidates, covers exactly two
    # canonical S9 obligations. Hence 31 obligations need >=ceil(31/2)=16.
    assert all(len(parents) == 2 for parents in boundary.values())
    selected = {int(h, 16) for h in keys}
    assert selected <= set(boundary), 'leaf outside complete boundary'
    assert set().union(*(boundary[h] for h in selected)) == obligations, 'uncovered S9'
    states = 0
    if terminal:
        for h in keys:
            m = int(h, 16)
            assert len(g.points(m)) == 10 and g.canonical(m) == m
            assert all(not g.forbidden(*q) for q in combinations(g.points(m), 4))
            win, visited, _ = g.solve10(m)
            assert not win, f'false LOSS leaf {h}'
            states += visited
        assert states == 11495, f'terminal state regression: {states}'
    if full:
        win_count = loss_count = all_states = 0
        for m in boundary:
            is_win, visited, _ = g.solve10(m)
            all_states += visited
            if is_win:
                win_count += 1
            else:
                loss_count += 1
        assert (win_count, loss_count, all_states) == (297, 81, 175066), (
            win_count, loss_count, all_states)
    return {'root': ROOT, 's9_obligations': 31, 's10_boundary': 378,
            'max_s9_covered_per_leaf': 2, 'minimum_leaves': 16,
            'selected_leaves': 16, 'terminal_verified': 16 if terminal else 0,
            'terminal_states': states if terminal else None,
            'full_boundary': {'win': 297, 'loss': 81, 'states': 175066} if full else None,
            'empty_board': 'UNKNOWN'}

def negative(keys):
    bad = [keys[:-1], keys[:-1] + keys[:1],
           keys[:-1] + ['0' * 32], keys[:-1] + [ROOT]]
    for rows in bad:
        try:
            verify(rows, terminal=False)
        except (AssertionError, ValueError):
            continue
        raise AssertionError('invalid proof accepted')

if __name__ == '__main__':
    keys = (HERE / 'leaves16.keys').read_text(encoding='ascii').split()
    print(verify(keys, full=('--full' in sys.argv)))
    if '--negative' in sys.argv:
        negative(keys)
        print('PASS four malformed certificates rejected')
