#!/usr/bin/env python3
"""Check minimum S10-LOSS leaf count across *all* three S8-LOSS replies.

Run after verify.py's complete S7 boundary/terminal audit. No solver cache is
read. The 12-leaf minimum is for the fixed S7->S8->S9->S10 proof form only.
"""
import json
from collections import defaultdict
from math import ceil
from pathlib import Path

from verify import children, terminal

HERE = Path(__file__).resolve().parent
FIRST = '00000000100000021081004020000020'
EXPECTED = {
    FIRST: (22, 181, 12),
    '00000100100000021081000020000020': (23, 198, 12),
    '00008000100000021081000020000020': (31, 346, 16),
}


def require(test, message):
    if not test:
        raise ValueError(message)


def main():
    cert = json.loads((HERE / 'certificate.json').read_text())
    s7 = int(cert['s7'], 16)
    require(len(children(s7)) == 36, 'S7 legal S8 boundary changed')
    require(set(cert['s8_loss']) == set(EXPECTED), 'S8 LOSS roots changed')
    require({int(s, 16) for s in cert['s8_loss']} <= children(s7),
            'S8 LOSS is not a legal S7 child')
    dual = {int(k, 16): v for k, v in cert['dual_half_units'].items()}
    require(len(dual) == 14 and sum(dual.values()) == 23 and
            all(type(v) is int and v in (1, 2) for v in dual.values()),
            'first-root dual weights changed')
    selected = {int(k, 16) for k in cert['s10_loss_cover12']}
    require(len(selected) == 12, '12-leaf certificate changed')

    bounds = []
    for name, (n9, n10, claimed_bound) in EXPECTED.items():
        s9 = children(int(name, 16))
        parents = defaultdict(set)
        for p in s9:
            for c in children(p):
                parents[c].add(p)
        require((len(s9), len(parents)) == (n9, n10),
                f'{name}: legal S9/S10 boundary changed')
        degree = max(map(len, parents.values()))
        require(degree <= 2, f'{name}: a S10 leaf covers >2 S9 obligations')
        bound = ceil(n9 / degree)  # valid even if *every* candidate were LOSS

        if name == FIRST:
            require(set(dual) <= s9, 'dual weight outside first-root S9')
            require(selected <= set(parents), '12-leaf set contains unrelated key')
            require(all(any(c in selected for c in children(p)) for p in s9),
                    '12-leaf set does not cover every first-root S9')
            wins = losses = 0
            for c, covered in parents.items():
                is_win, _states = terminal(c)
                if is_win:
                    wins += 1
                else:
                    losses += 1
                    require(sum(dual.get(p, 0) for p in covered) <= 2,
                            f'dual constraint violated by {c:032x}')
            require((wins, losses) == (132, 49),
                    'first-root exhaustive S10 terminal verdicts changed')
            require(all(not terminal(c)[0] for c in selected),
                    'selected leaf is not terminal LOSS')
            # Weights are in half-units. Dual objective 23/2 = 11.5.
            bound = max(bound, ceil(sum(dual.values()) / 2))
        require(bound == claimed_bound, f'{name}: lower bound changed')
        bounds.append(bound)
        print(f'{name}: S9={n9}, S10={n10}, max_coverage={degree}, '
              f'certified_lower_bound={bound}')

    require(min(bounds) == 12, 'global minimum lower bound changed')
    print('PASS: 12 LOSS leaves are attainable and minimal across all three '
          'S8 LOSS children in this fixed proof form; empty=UNKNOWN')


if __name__ == '__main__':
    main()
