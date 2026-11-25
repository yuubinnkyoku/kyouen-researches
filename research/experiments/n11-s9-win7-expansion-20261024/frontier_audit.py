#!/usr/bin/env python3
"""Structural reverse closure of 385+39+12 previously certified S10 LOSS leaves.

This script does not independently reclassify its input terminal leaves;
those are proved by the earlier S8-385 and S7-loss12 experiments.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from functools import lru_cache
from itertools import combinations
from verify import HERE, EXP, need, read
from terminal_geometry import canonical, points

BASE = EXP / 'n11-s8-to-s7-lift238-20261020'
OTHER = EXP / 'n11-s7-terminal-loss12-20261024/certificate.json'
ALL = (1 << 121) - 1
BIT = [1 << i for i in range(121)]
XY = [(i % 11, i // 11) for i in range(121)]
TRANS = []
for t in range(8):
    TRANS.append([BIT[11*yy+xx] for x, y in XY for xx, yy in [(
        (x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
        (10-x, y), (10-y, 10-x), (x, 10-y), (y, x)
    )[t]]])


@lru_cache(maxsize=None)
def forbidden(a, b, c):
    x0, y0 = XY[a]
    x1, y1 = XY[b]
    x2, y2 = XY[c]
    q0 = x0*x0 + y0*y0
    q1 = x1*x1 + y1*y1
    q2 = x2*x2 + y2*y2
    A = (x1-x0)*(y2-y0)-(y1-y0)*(x2-x0)
    B = -(q1-q0)*(y2-y0)+(q2-q0)*(y1-y0)
    C = -(x1-x0)*(q2-q0)+(x2-x0)*(q1-q0)
    D = -A*q0-B*x0-C*y0
    return sum(BIT[p] for p, (x, y) in enumerate(XY)
               if A*(x*x+y*y)+B*x+C*y+D == 0)


def legal_count(board):
    blocked = board
    for triple in combinations(points(board), 3):
        blocked |= forbidden(*triple)
    return (ALL ^ blocked).bit_count()


def stabilizer(board):
    pp = points(board)
    return sum(sum(t[p] for p in pp) == board for t in TRANS)


def reverse(boards):
    return {canonical(b ^ BIT[p]) for b in boards for p in points(b)}


def audit(new_only=False):
    cert = json.loads(OTHER.read_text())
    need(len(cert['s10_loss_cover39']) == 39 and len(cert['s10_loss_cover12']) == 12,
         'prior LOSS certificate counts changed')
    newer = {int(x, 16) for x in cert['s10_loss_cover39'] + cert['s10_loss_cover12']}
    if new_only:
        leaves = newer
    else:
        raw = (BASE / 'selected385.txt').read_bytes()
        need(hashlib.sha256(raw).hexdigest() ==
             'ca487f8075c4a03a404f5d1a98e2c0c847701192d0ce37a30542fd73ea1f3f22',
             'old 385-leaf SHA mismatch')
        old = read(BASE / 'selected385.txt', 385, 10)
        leaves = old | newer
        need(len(leaves) == 427, 'union leaf count changed')
    s9 = reverse(leaves)
    covered = defaultdict(set)
    for b in s9:
        for p in points(b):
            covered[canonical(b ^ BIT[p])].add(b)
    closed = set()
    nearest = (999, None)
    for b, witnesses in covered.items():
        need(stabilizer(b) == 1, 'symmetric S8 requires canonical-child audit')
        missing = legal_count(b) - len(witnesses)
        need(missing >= 0, 'covered S9 count exceeds legal S9 count')
        if missing == 0:
            closed.add(b)
        elif (missing, b) < nearest:
            nearest = (missing, b)
    roots = {int(h, 16) for h in cert['s8_loss']}
    need(roots <= closed, 'previous three S8 LOSS roots not recovered')
    report = {'s10_loss_leaves': len(leaves), 's9_loss_reverse_parents': len(s9),
              'candidate_s8': len(covered), 'closed_s8_loss': len(closed),
              'nearest_open_s8': f'{nearest[1]:032x}',
              'nearest_open_s8_missing_s9': nearest[0], 'empty_winner': 'UNKNOWN'}
    if not new_only:
        oldroots = read(BASE / 'roots35.txt', 35, 8)
        need(closed == oldroots | roots and len(closed) == 38,
             'unexpected S8 closure from 427 leaves')
        need((len(s9), len(covered), nearest) ==
             (4161, 17338, (8, int('00000010001000001000000031100080', 16))),
             'S8 frontier regression changed')
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--new-only', action='store_true')
    args = ap.parse_args()
    print('PASS ' + json.dumps(audit(args.new_only), sort_keys=True))
