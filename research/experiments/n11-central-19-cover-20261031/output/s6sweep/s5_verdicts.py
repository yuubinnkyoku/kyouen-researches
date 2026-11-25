#!/usr/bin/env python3
"""S5 verdicts from the S6 sweep: second-win iff some S6 child is
LOSS-for-mover; else first-win. (All 3,868 sweep verdicts are conclusive:
no timeouts.)"""
import json, sys
from pathlib import Path
HERE = Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')
sys.path.insert(0, str(HERE))
import verify_conditional_s6_cover_46 as base

data = base.reconstruct()
s5, incidence, costs = data[1:4]
sweep = json.load(open('/mnt/d/kyouen-focus-certs/s6_sweep/sweep_results.json'))
children_by_s5 = [[] for _ in range(len(s5))]
for s6, parents in incidence.items():
    for i in parents:
        children_by_s5[i].append(s6)

records = []
first_win_s5 = []
second_win_s5 = []
loss_covers = {}
for i, s5m in enumerate(s5):
    chs = sorted(children_by_s5[i])
    losses = [c for c in chs if sweep.get(f'{c:032x}', {}).get('verdict') == 'LOSS_for_mover']
    wins = [c for c in chs if sweep.get(f'{c:032x}', {}).get('verdict') == 'WIN_for_mover']
    verdict = 'SECOND_WIN' if losses else 'FIRST_WIN'
    if verdict == 'SECOND_WIN':
        second_win_s5.append(i)
        for c in losses:
            loss_covers.setdefault(f'{c:032x}', []).append(i)
    else:
        first_win_s5.append(i)
    records.append({'s5_index': i, 's5': f'{s5m:032x}', 'children': len(chs),
                    'loss_children': len(losses), 'win_children': len(wins), 'verdict': verdict})
out = {'s5_count': len(s5), 'second_win': len(second_win_s5), 'first_win': len(first_win_s5),
       'first_win_s5': [f'{s5[i]:032x}' for i in first_win_s5],
       'second_win_s5': [f'{s5[i]:032x}' for i in second_win_s5],
       'loss_s6_covers': loss_covers, 'records': records}
Path('/mnt/d/kyouen-focus-certs/s6_sweep/s5_verdicts.json').write_text(json.dumps(out, indent=2))
print(json.dumps({'s5_count': len(s5), 'second_win': len(second_win_s5), 'first_win': len(first_win_s5)}, indent=2))
print('loss S6 coverage:', loss_covers)
