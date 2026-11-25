#!/usr/bin/env python3
"""Region test: do the 94 S5 positions share one common legal S4 parent R,
and are they exactly R's legal five-stone children? Reported with the count
of first-win S5 children (s5_verdicts.json)."""
import json, sys
from collections import Counter
from itertools import combinations
from pathlib import Path
HERE = Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')
sys.path.insert(0, str(HERE))
import verify_conditional_s6_cover_46 as base
import verify_five_terminal_loss7 as vf

data = base.reconstruct()
s5 = data[1]
assert len(s5) == 94, len(s5)
sv = json.load(open('/mnt/d/kyouen-focus-certs/s6_sweep/s5_verdicts.json'))
first_win_masks = {int(k, 16) for k in sv['first_win_s5']}
print('first-win S5 count:', len(first_win_masks))

counts = Counter()
for m in s5:
    pts = [i for i in range(121) if m & (1 << i)]
    assert len(pts) == 5
    for keep in combinations(pts, 4):
        r = 0
        for p in keep:
            r |= 1 << p
        counts[r] += 1

s5set = set(s5)
for r, c in counts.most_common(5):
    pts = [i for i in range(121) if r & (1 << i)]
    # S4 legality: its single 4-subset must not be forbidden
    safe = (vf.det4(tuple(pts)) != 0)
    kids = {r | (1 << v) for v in range(121) if (vf.legal(r) & (1 << v))}
    print(f'S4 {r:032x} count={c} safe={safe} kids={len(kids)} '
          f'94 subset of kids={s5set <= kids} kids==94={kids == s5set} '
          f'first-win children={len(kids & first_win_masks)}')
