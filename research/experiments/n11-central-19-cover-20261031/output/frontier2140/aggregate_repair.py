#!/usr/bin/env python3
"""Aggregate S7 verdicts for the repaired 46-set (K0673 repair swap).
Base = the true 2091 46-set, derived the same way as the repair audit
(certified context -> 2097 step -> 2091 step). Frontiers via fast_frontier.
Joins verdicts from the focus62 + frontier_classify verified.json files and
reports each witness S6's verdict: LOSS iff all S7 children are LOSS7,
WIN_for_player_to_move iff any child is WIN7, else UNKNOWN.
"""
import json, sys
from pathlib import Path
HERE = Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')
sys.path.insert(0, str(HERE))
import verify_conditional_s6_cover_46 as base
import verify_central49_2097_three_swap as s97
import verify_central49_2091_descent_three_swap as vd
import verify_central49_2154_two_swap_descent as source

D1 = Path('/mnt/d/kyouen-focus-certs')
D2 = D1 / 'frontier_classify'


def load_verdicts():
    v = {}
    for d in (D1, D2):
        p = d / 'verified.json'
        if p.exists():
            j = json.load(open(p))
            for k, rec in j.get('verified', {}).items():
                v[int(k, 16)] = rec['type']
    return v


def base_2091():
    sel = s97.context()[0]
    swap97 = json.loads(open(HERE / 'conditional_s6_cover_46_post_seven_win6_2097_three_swap.json').read())
    step97 = swap97['steps'][0]
    sel2097 = (sel - {base.decode(k) for k in step97['removed']}) | {base.decode(k) for k in step97['added']}
    cert = json.load(open(HERE / 'conditional_s6_cover_46_post_seven_win6_2091_descent_three_swap.json'))
    step = cert['steps'][0]
    selected = (sel2097 - {base.decode(k) for k in step['removed']}) | {base.decode(k) for k in step['added']}
    assert len(selected) == 46, len(selected)
    return selected


def main():
    selected = base_2091()
    rep = json.load(open(HERE / 'output' / 'repair_focus_neighborhood.json'))
    swap = rep['repair_best_swap']
    removed = {base.decode(k) for k in swap['removed']}
    added = {base.decode(k) for k in swap['added']}
    assert removed <= selected, 'repair removed set not in 2091 base'
    repaired = (selected - removed) | added
    assert len(repaired) == 46, len(repaired)
    fr = {s: source.fast_frontier(s) for s in repaired}
    union = set().union(*fr.values())
    print('repaired frontier total', len(union), flush=True)
    verdicts = load_verdicts()
    print('verdicts loaded', len(verdicts), flush=True)
    missing = set()
    report = {}
    for s in sorted(repaired):
        ch = fr[s]
        cvs = {c: verdicts.get(c) for c in ch}
        unknown = [c for c, vv in cvs.items() if vv is None]
        win7 = [c for c, vv in cvs.items() if vv == 'WIN7']
        loss7 = [c for c, vv in cvs.items() if vv == 'LOSS7']
        missing.update(unknown)
        if win7:
            verdict = 'WIN_for_player_to_move'
        elif not unknown:
            verdict = 'LOSS_for_player_to_move'
        else:
            verdict = 'UNKNOWN'
        report[f'{s:032x}'] = {'children': len(ch), 'loss7': len(loss7),
                                'win7': len(win7), 'unknown': len(unknown),
                                'verdict': verdict}
    out = {'repaired_frontier': len(union), 'witness_verdicts': report,
           'missing_classes': sorted(f'{c:032x}' for c in missing)}
    (D2 / 'repair_aggregation.json').write_text(json.dumps(out, indent=2))
    summary = {}
    for r in report.values():
        summary[r['verdict']] = summary.get(r['verdict'], 0) + 1
    print(json.dumps({'witness_summary': summary, 'missing_total': len(missing)}, indent=2))
    for k, r in sorted(report.items()):
        if r['verdict'] != 'LOSS_for_player_to_move':
            print('NON-LOSS WITNESS', k, r, flush=True)


if __name__ == '__main__':
    main()
