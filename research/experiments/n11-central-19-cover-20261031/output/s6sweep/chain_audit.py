#!/usr/bin/env python3
"""Chain audit (oracle-only, no generation): using the 78 first-win S5
verdicts (K0675) as the only proven oracle, check the W4 predicate
(S4 has a first-win S5 child) and propagate: S3 proven-first iff ALL legal
S4 children are W4; S2 proven-first iff some S3 child is proven-first;
empty-board first-win iff ALL S2 replies are proven first-win.
Three-valued: unproven != second-win. Memoized."""
import json, sys, pathlib
from collections import Counter
sys.path.insert(0, str(pathlib.Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')))
import verify_five_terminal_loss7 as vf

WORK = pathlib.Path('/mnt/d/kyouen-focus-certs/chain_audit')
WORK.mkdir(parents=True, exist_ok=True)
sv = json.load(open('/mnt/d/kyouen-focus-certs/s6_sweep/s5_verdicts.json'))
FIRSTWIN78 = {int(k, 16) for k in sv['first_win_s5']}
SECONDWIN16 = {int(k, 16) for k in sv['second_win_s5']}
CACHE = WORK / 'audit_cache.json'
w4 = {}
s3v = {}
s2v = {}
if CACHE.exists():
    j = json.load(open(CACHE))
    w4 = {int(k, 16): v for k, v in j.get('w4', {}).items()}
    s3v = {int(k, 16): v for k, v in j.get('s3', {}).items()}
    s2v = {int(k, 16): v for k, v in j.get('s2', {}).items()}


def save():
    CACHE.write_text(json.dumps({'w4': {f'{k:032x}': v for k, v in w4.items()},
                                 's3': {f'{k:032x}': v for k, v in s3v.items()},
                                 's2': {f'{k:032x}': v for k, v in s2v.items()}}))


def W4(s4):
    """True = proven first-win (has a first-win S5 child). False = proven
    second-win (no children outside SECONDWIN16... wait: proven second
    requires every child to be a proven second-win S5, i.e. all children in
    SECONDWIN16 AND no unclassified children. We never claim False here:
    False means 'no first-win child among the 78' = NOT proven-first.
    For the S3 universal we need PROVEN-first, so treat non-W4 as fail."""
    if s4 in w4:
        return w4[s4]
    kids = {s4 | (1 << v) for v in range(121) if (vf.legal(s4) & (1 << v))}
    r = bool(kids & FIRSTWIN78)
    w4[s4] = r
    return r


def s3_proven_first(s3):
    """True iff every legal S4 child is proven first-win."""
    if s3 in s3v:
        return s3v[s3]
    kids = [s3 | (1 << v) for v in range(121) if (vf.legal(s3) & (1 << v))]
    r = bool(kids) and all(W4(k) for k in kids)
    s3v[s3] = r
    return r


def s2_proven_first(s2):
    if s2 in s2v:
        return s2v[s2]
    kids = [s2 | (1 << v) for v in range(121) if (vf.legal(s2) & (1 << v))]
    r = any(s3_proven_first(k) for k in kids)
    s2v[s2] = r
    return r


if __name__ == '__main__':
    s1 = 1 << 60
    s2s = [s1 | (1 << v) for v in range(121) if (vf.legal(s1) & (1 << v))]
    print('S2 replies to {60}:', len(s2s))
    results = {}
    for i, r in enumerate(s2s):
        results[f'{r:032x}'] = s2_proven_first(r)
        if (i + 1) % 20 == 0:
            print('progress', i + 1, '/', len(s2s),
                  'S2 proven first:', sum(results.values()),
                  'W4 cache:', len(w4), 'S3 cache:', len(s3v), flush=True)
            save()
    save()
    n_first = sum(results.values())
    print(json.dumps({'s2_proven_first': n_first, 's2_unproven': len(s2s) - n_first,
                      'empty_board_first_win': n_first == len(s2s)}, indent=2))
    (WORK / 's2_audit.json').write_text(json.dumps(
        {'proven_first': n_first, 'unproven': len(s2s) - n_first,
         's2_first_win': sorted(k for k, v in results.items() if v),
         's2_unproven': sorted(k for k, v in results.items() if not v)}, indent=2))
