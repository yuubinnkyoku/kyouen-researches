#!/usr/bin/env python3
"""Recompute the six S5 LOSS parents' overlap with the tracked 19-root plan.

Run in a full kyouen-researches checkout; requires Python standard library only.
The certificate itself is checked by verify_s6_terminal.py (run separately).
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'n11-s7-fifth-terminal-20261015'))
from fifth_verify_standalone import canonical, children, points

PLAN = ROOT / 'research/experiments/n11-night-plan-update6-20261014/output/repaired-joint-plan-update6.json'
CACHE = ROOT / 'research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache'
S6 = int('00000000040004001004000004010000', 16)

# Known terminal-verified S5 roots (13 incorporated in update6, plus 162106 not yet reflected).
KNOWN_TERMINAL_S5 = [
    (40,48,60,72,80), (49,55,60,65,71),
    (2,5,8,49,60), (1,5,9,49,60), (23,60,61,65,89),
    (5,45,49,53,60), (1,49,59,60,61), (37,49,59,60,61),
    (49,51,59,60,71), (2,49,59,60,61),
    (4,5,6,49,60), (5,15,17,49,60), (35,38,41,60,71),
]

def read_cache():
    keys = set()
    for line in CACHE.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        parts = line.split(',')
        if len(parts) != 6 or parts[0] != 's5verdict':
            raise ValueError('unexpected cache record')
        keys.add(int(parts[1]) | (int(parts[2]) << 64))
    return keys

def main():
    plan = json.loads(PLAN.read_text())
    if plan['schema'] != 'n11-night-repaired-joint-plan-update6-v1':
        raise ValueError('plan schema changed; re-audit before proceeding')
    parents = {canonical(S6 ^ (1 << p)) for p in points(S6)}
    assert len(parents) == 6 and all(S6 in children(s5) for s5 in parents)
    cache = read_cache()
    verified = {canonical(sum(1 << p for p in positions)) for positions in KNOWN_TERMINAL_S5}
    if parents & (cache | verified):
        raise ValueError('S5 parent already known; update baseline')
    matched = Counter()
    root_hits = Counter()
    classes = set()
    for group in plan['groups']:
        lo, hi = group['s4_mask']
        s4 = int(lo) | (int(hi) << 64)
        c = children(s4)
        for s5 in parents & c:
            matched[s5] += 1
            root_hits[group['first']] += 1
            classes.add(group['s4_class_index'])
    required = set(matched)
    if len(required) != 3 or sum(matched.values()) != 24 or classes != {16397}:
        raise ValueError('plan overlap changed; re-evaluate')
    if dict(root_hits) != {24:9, 26:6, 48:9}:
        raise ValueError('unexpected root overlap')
    if plan['union_size'] != 31774 or len(plan['required_new_s5']) != 31774:
        raise ValueError('baseline union changed')
    class_groups = [g for g in plan['groups'] if g['s4_class_index'] == 16397]
    if len(class_groups) != 8 or any(g['unknown_s5_children'] != 93 for g in class_groups):
        raise ValueError('selected S4 boundary changed')
    print('PASS six new terminal-proved S5 LOSS; three are selected-plan S5 obligations')
    print('selected S4 class=16397, 8 third-move groups, root classes 24/26/48')
    print('baseline optimistic S5 union=31774, after six LOSS parents=31771')
    for mask in sorted(required):
        print(f'{mask:032x}: selected groups={matched[mask]}')

if __name__ == '__main__':
    main()
