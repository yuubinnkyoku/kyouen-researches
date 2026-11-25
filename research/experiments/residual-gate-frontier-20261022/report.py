#!/usr/bin/env python3
"""Render the completed fixed comparison, without rerunning searches."""
from study import HERE, read

lines = ['# Fixed gate comparison', '',
    'Times below sum per-root medians over three repeats, in milliseconds. '
    'Initialization is excluded. UNKNOWN roots retain their specified work limits.', '',
    '## Diagnostic (profile ON, excluded from timing comparison)', '',
    '| Training root | Unresolved stage-0 visits | Min legal | Max legal | Legal ≤24 | Legal ≤48 |',
    '|---|---:|---:|---:|---:|---:|']
for r in read('diagnostic.json'):
    h = {int(k): v for k, v in r['histogram'].items()}
    lines.append(f'| {r["id"]} | {sum(h.values())} | {min(h)} | {max(h)} | '
                 f'{sum(v for k,v in h.items() if k<=24)} | {sum(v for k,v in h.items() if k<=48)} |')
for name, title in [('training.json', 'Training: three reused deep roots'),
                    ('confirmation.json', 'Prospective confirmation: six seeded deep roots')]:
    lines += ['', f'## {title}', '', '| Limit / gate | Solve ms | UNKNOWN | Work nodes | Expansions | PN nodes | PN aborts | Handoffs | Watchdogs |',
              '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for label, r in read(name)['totals'].items():
        lines.append(f'| {label} | {r["solve_us"]/1000:.3f} | {r["unknown"]} | {r["nodes"]} | '
                     f'{r["expansions"]} | {r["pn_nodes"]} | {r["pn_aborts"]} | {r["residual_calls"]} | {r["watchdogs"]} |')
late = read('late.json')
assert len(late) == 78 and all(r['result'] in (1, 2) for r in late)
lines += ['', f'Training selected gate {read("selection.json")["gate"]}; the selection was committed before confirmation.', '',
    'All 26 reused late roots matched their independent known outcomes in all three settings (78 checks). '
    'These single-run checks are correctness regressions, not a timing holdout.', '',
    'Frame counts include revisits and exclude already solved TT frames. They are not unique positions. '
    'Timing differences on one host do not establish statistical superiority; identical work counts '
    'must not be described as reduced search effort. The default gate remains OFF.', '']
(HERE / 'comparison.md').write_text('\n'.join(lines))
