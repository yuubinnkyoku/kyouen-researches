#!/usr/bin/env python3
"""Per-key cross-check of all 378 S10 terminal verdicts, moves and state counts.

JavaScript uses an integer 3x3 circle determinant; Python independently uses
Bareiss 4x4 elimination. Neither reads the other's cached verdicts.
"""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'n11-s8-targeted-closure-20261015'))
import verify_terminal_independent as g


def main():
    root = int('00000000000040001000044400830000', 16)
    boundary = set().union(*(g.children(s9) for s9 in g.children(root)))
    assert len(boundary) == 378
    result = subprocess.run(['node', str(HERE / 'verify_min16.js'), '--dump'],
                            check=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert len(lines) == 378
    assert lines == sorted(lines)
    total = wins = losses = 0
    seen = set()
    for line in lines:
        h, verdict, states, moves = line.split('\t')
        m = int(h, 16)
        assert m in boundary and m not in seen
        seen.add(m)
        pywin, pystates, pymoves = g.solve10(m)
        assert (verdict, int(states), int(moves)) == (
            'WIN' if pywin else 'LOSS', pystates, pymoves), h
        wins += pywin
        losses += not pywin
        total += pystates
    assert seen == boundary
    assert (wins, losses, total) == (297, 81, 175066)
    print('PASS 378/378 exact Python-vs-JavaScript verdict, legal count, state count; '
          'WIN 297, LOSS 81, states 175066; S8 16-leaf optimum unchanged')


if __name__ == '__main__':
    main()
