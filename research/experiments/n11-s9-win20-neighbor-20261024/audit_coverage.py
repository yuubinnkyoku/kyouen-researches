#!/usr/bin/env python3
"""Coverage gain relative to named prior terminal certificates and frozen comparison cache."""
import json
from verify import EXP, HERE, canonical, children, fmt, need, points, read_keys

PRIOR = [
    ('n11-s9-win29-lift-20261023/s9-win29.keys', 29),
    ('n11-s9-win27-expansion-20261024/s9-win27.keys', 27),
    ('n11-s9-win2-followup-20261024/s9-win2.keys', 2),
    ('n11-s9-win10-20261024/s9-win10.keys', 10),
    ('n11-s9-win7-expansion-20261024/s9-win7.keys', 7),
]
BASE = EXP / 'n11-targeted-terminal-lift-20261015/data'


def parents(boards):
    return {canonical(b ^ (1 << p)) for b in boards for p in points(b)}


def main():
    roots = read_keys(HERE / 's9-win20.keys', 20, 9)
    prior9 = set().union(*(read_keys(EXP / path, n, 9) for path, n in PRIOR))
    extra = json.loads((EXP / 'n11-s7-terminal-loss12-20261024/certificate.json').read_text())
    prior9 |= {int(x, 16) for x in extra['new_s9_win']}
    need(len(prior9) == 93 and not prior9 & roots, 'previous 93 S9 roots changed')
    old8, new8 = parents(prior9), parents(roots)
    need((len(old8), len(new8), len(old8 & new8)) == (750, 167, 13),
         'prior/new S8 certificate overlap changed')
    frozen_win = read_keys(BASE / 'lifted_s8_win_51571.txt', 13501, 8)
    frozen_loss = read_keys(BASE / 'all_s8_loss_294.txt', 294, 8)
    need(not new8 & (frozen_win | frozen_loss), 'frozen S8 WIN/LOSS overlap')
    before = old8 | frozen_win
    added = new8 - before
    need(len(added) == 154, 'new certified S8 gain changed')
    after = before | new8
    s7 = parents(added)
    gain = changed = closed = terminal_closed = 0
    for p in s7:
        cs = children(p)
        old, now = len(cs & before), len(cs & after)
        gain += now - old
        changed += now > old
        closed += now == len(cs)
        terminal_closed += len(cs & (old8 | new8)) == len(cs)
    need((len(s7), gain, changed, closed, terminal_closed) == (600, 1232, 600, 0, 0),
         'S7 coverage audit changed')
    print('PASS 154 new S8 WIN vs named prior/frozen sets; '
          '600 S7 candidates, +1232 covered edges, 0 S7 closures; empty=UNKNOWN')


if __name__ == '__main__':
    main()
