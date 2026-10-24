#!/usr/bin/env python3
"""Certificate-only reverse-closure audit; frozen verdict caches are not trusted.

The old 385 and 39+12 S10 LOSS leaves must be verified by their own
experiments. This audit verifies only the reverse geometry and coverage
changes when adding the 12 independently reclassified leaves here.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations
import json
from verify import EXP, HERE, canonical, need, points, read_keys

BASE = EXP / 'n11-s8-to-s7-lift238-20261020'
PREV = EXP / 'n11-s7-terminal-loss12-20261024/certificate.json'
PRIOR_WIN = [
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
]
XY = [(p % 11, p // 11) for p in range(121)]


def reverse(boards):
    return {canonical(b ^ (1 << p)) for b in boards for p in points(b)}


def coverage(s9):
    covered = defaultdict(set)
    for b in s9:
        for p in points(b):
            covered[canonical(b ^ (1 << p))].add(b)
    return covered


@lru_cache(None)
def forbidden(a, b, c):
    x0, y0 = XY[a]
    x1, y1 = XY[b]
    x2, y2 = XY[c]
    q0, q1, q2 = x0*x0 + y0*y0, x1*x1 + y1*y1, x2*x2 + y2*y2
    A = (x1-x0)*(y2-y0) - (y1-y0)*(x2-x0)
    B = -(q1-q0)*(y2-y0) + (q2-q0)*(y1-y0)
    C = -(x1-x0)*(q2-q0) + (x2-x0)*(q1-q0)
    D = -A*q0 - B*x0 - C*y0
    return sum(1 << p for p, (x, y) in enumerate(XY)
               if A*(x*x+y*y) + B*x + C*y + D == 0)


def legal_children(board):
    occupied = points(board)
    blocked = board
    for a, b, c in combinations(occupied, 3):
        blocked |= forbidden(a, b, c)
    return {canonical(board | (1 << p)) for p in range(121)
            if not ((blocked >> p) & 1)}


def main():
    cert = json.loads(PREV.read_text(encoding='utf-8'))
    old_keys = read_keys(BASE / 'selected385.txt')
    need(len(old_keys) == 385 and len(cert['s10_loss_cover39']) == 39
         and len(cert['s10_loss_cover12']) == 12, 'old LOSS source counts changed')
    old = {int(k, 16) for k in old_keys + cert['s10_loss_cover39']
           + cert['s10_loss_cover12']}
    extra = {int(k, 16) for k in read_keys(HERE / 's10-loss12.keys')}
    need(len(old) == 427 and len(extra) == 12 and not old & extra,
         'S10 LOSS source overlap changed')
    before9, after9 = reverse(old), reverse(old | extra)
    need((len(before9), len(after9)) == (4161, 4273), 'S9 LOSS counts changed')
    old8, new8 = coverage(before9), coverage(after9)
    need((len(old8), len(new8)) == (17338, 17798), 'S8 frontier counts changed')
    changed = {p for p, witnesses in new8.items()
               if witnesses != old8.get(p, set())}
    gain = sum(len(new8[p] - old8.get(p, set())) for p in changed)
    need((len(changed), gain) == (490, 1008), 'S8 coverage gain changed')

    known9win = {int(k, 16) for path in PRIOR_WIN
                 for k in read_keys(EXP / path)}
    known9win.update(int(k, 16) for k in cert['new_s9_win'])
    need(len(known9win) == 113 and not known9win & after9,
         'S9 WIN/LOSS conflict')
    witness_roots = {int(line.split()[0], 16) for line in
                     (HERE / 's9-loss12-witness.tsv').read_text().splitlines()}
    need(len(witness_roots) == 12 and witness_roots <= after9
         and len(witness_roots - before9) == 11, 'new S9 witness count changed')

    known8win = reverse(known9win)
    closed = []
    nearest = None
    eligible_nearest = None
    for p in changed:
        all_children = legal_children(p)
        need(new8[p] <= all_children, 'nonlegal S8->S9 coverage edge')
        missing = len(all_children - new8[p])
        if missing == 0:
            closed.append(p)
        row = (missing, -len(new8[p]), p)
        if nearest is None or row < nearest:
            nearest = row
        if p not in known8win and (eligible_nearest is None or row < eligible_nearest):
            eligible_nearest = row
    need(not closed, 'new S8 LOSS closure: needs independent certificate')
    need(nearest[0] == 6 and nearest[2] in known8win,
         'nearest S8 frontier is no longer known WIN')
    print(json.dumps({
        's10_loss_old': len(old), 's10_loss_new': len(old | extra),
        's9_loss_old': len(before9), 's9_loss_new': len(after9),
        's9_loss_new_witness_roots': len(witness_roots - before9),
        's8_candidates_old': len(old8), 's8_candidates_new': len(new8),
        's8_changed': len(changed), 's8_coverage_gain': gain,
        's8_new_loss_closed': len(closed),
        'nearest_changed_missing': nearest[0],
        'nearest_changed_is_known_win': nearest[2] in known8win,
        'nearest_eligible_changed_missing': eligible_nearest[0] if eligible_nearest else None,
        'empty_winner': 'UNKNOWN'}, sort_keys=True))


if __name__ == '__main__':
    main()
