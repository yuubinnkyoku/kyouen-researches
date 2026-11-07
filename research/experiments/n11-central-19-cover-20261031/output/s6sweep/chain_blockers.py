#!/usr/bin/env python3
"""Diagnostic: for each S2 {60,q}, the best S3 child minimizes the number of
legal S4 children not proven first-win (W4). Reports the distribution."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')))
import verify_five_terminal_loss7 as vf

WORK = pathlib.Path('/mnt/d/kyouen-focus-certs/chain_audit')
sv = json.load(open('/mnt/d/kyouen-focus-certs/s6_sweep/s5_verdicts.json'))
FIRSTWIN78 = {int(k, 16) for k in sv['first_win_s5']}
cache = json.load(open(WORK / 'audit_cache.json'))
w4 = {int(k, 16): v for k, v in cache['w4'].items()}


def W4(s4):
    if s4 in w4:
        return w4[s4]
    kids = {s4 | (1 << v) for v in range(121) if (vf.legal(s4) & (1 << v))}
    r = bool(kids & FIRSTWIN78)
    w4[s4] = r
    return r


def blockers_of(s3):
    kids = [s3 | (1 << v) for v in range(121) if (vf.legal(s3) & (1 << v))]
    return [k for k in kids if not W4(k)]


s1 = 1 << 60
s2s = [s1 | (1 << v) for v in range(121) if (vf.legal(s1) & (1 << v))]
best_per_s2 = {}
all_blockers = set()
for r in s2s:
    best = None
    for s3 in sorted([r | (1 << v) for v in range(121) if (vf.legal(r) & (1 << v))]):
        bl = blockers_of(s3)
        if best is None or len(bl) < best[0]:
            best = (len(bl), s3, tuple(bl))
            if best[0] == 0:
                break
    best_per_s2[f'{r:032x}'] = best[0]
    all_blockers.update(best[2])
import collections
dist = collections.Counter(best_per_s2.values())
print('best blocker count distribution over 120 S2:', dict(sorted(dist.items())))
print('distinct blocking S4s (best-S3 per S2):', len(all_blockers))
(WORK / 'blockers.json').write_text(json.dumps(
    {'best_per_s2': best_per_s2,
     'blocking_s4s': sorted(f'{k:032x}' for k in all_blockers)}, indent=2))
