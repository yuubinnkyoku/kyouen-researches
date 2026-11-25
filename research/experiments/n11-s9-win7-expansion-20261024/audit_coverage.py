#!/usr/bin/env python3
"""S9 WIN -> S8 WIN -> S7 coverage, with explicit frozen-cache boundary."""
import argparse
import json
from verify import HERE, EXP, need, read
from terminal_geometry import canonical, children, points, safe

PRIOR = [
    EXP / 'n11-s9-win29-lift-20261023/s9-win29.keys',
    EXP / 'n11-s9-win27-expansion-20261024/s9-win27.keys',
    EXP / 'n11-s9-win2-followup-20261024/s9-win2.keys',
    EXP / 'n11-s9-win10-20261024/s9-win10.keys',
]
EXTRA = EXP / 'n11-s7-terminal-loss12-20261024/certificate.json'
FROZEN = EXP / 'n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt'
FROZEN_LOSS = EXP / 'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'


def parents_of(boards):
    return {canonical(b ^ (1 << p)) for b in boards for p in points(b)}


def audit(new_only=False):
    roots = read(HERE / 's9-win7.keys', 7, 9)
    new8 = parents_of(roots)
    s7 = parents_of(new8)
    edges = {(p, b) for b in new8 for p in parents_of([b])}
    need((len(new8), len(s7), len(edges)) == (63, 247, 504),
         'new terminal reverse coverage changed')
    need(all(b in children(p) for p, b in edges), 'invalid S7->S8 edge')
    report = {'new_s9_win': 7, 'new_s8_win': 63, 's7_candidates': 247,
              'new_terminal_s7_edges': 504, 'empty_winner': 'UNKNOWN'}
    if not new_only:
        prior9 = set().union(*(read(path, n, 9)
                               for path, n in zip(PRIOR, (29, 27, 2, 10))))
        extra = json.loads(EXTRA.read_text())['new_s9_win']
        need(len(extra) == 18, 'previous terminal S9 certificate changed')
        prior9 |= {int(h, 16) for h in extra}
        need(len(prior9) == 86 and not prior9 & roots and
             all(b.bit_count() == 9 and canonical(b) == b and safe(b)
                 for b in prior9), 'previous S9 provenance conflict')
        prior8 = parents_of(prior9)
        need(len(prior8) == 687 and not prior8 & new8,
             'new S8 WIN duplicates prior terminal S8')
        frozen_win = read(FROZEN, 13501, 8)
        frozen_loss = read(FROZEN_LOSS, 294, 8)
        need(not new8 & (frozen_win | frozen_loss),
             'new S8 WIN duplicates/conflicts with frozen cache')
        before = prior8 | frozen_win
        after = before | new8
        gain = improved = closed = terminal_closed = 0
        for p in s7:
            cs = children(p)
            old = len(cs & before)
            now = len(cs & after)
            gain += now - old
            improved += now > old
            closed += now == len(cs)
            terminal_closed += len(cs & (prior8 | new8)) == len(cs)
        need((gain, improved, closed, terminal_closed) == (504, 247, 0, 0),
             'conditional S7 coverage changed')
        report.update({'prior_terminal_s9': 86, 'terminal_s8_win_union': 750,
                       'new_s8_vs_frozen_win': 63,
                       's8_win_loss_conflicts': 0,
                       's7_conditional_gain_edges': gain,
                       's7_improved_candidates': improved,
                       's7_conditional_closed': closed,
                       's7_terminal_closed': terminal_closed})
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--new-only', action='store_true')
    args = ap.parse_args()
    print('PASS ' + json.dumps(audit(args.new_only), sort_keys=True))
