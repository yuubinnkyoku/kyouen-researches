#!/usr/bin/env python3
"""Render the fixed allocation comparison without running any solver."""
from study import HERE, read
lines = ['# Fixed residual allocation comparison', '',
    'Root quota 128, residual gate 18. Times sum per-root medians over three repeats, '
    'excluding process initialization. Normal work and P/N nodes are separate budgets.', '']
for name, title in [('training.json', 'Training: nine reused S5 roots'), ('confirmation.json', 'Confirmation: six fresh seeded S5 roots')]:
    lines += [f'## {title}', '',
        '| Setting | Solve ms | UNKNOWN | Work | Expansions | Calls | PN nodes | Aborts | Duplicate skips | Watchdogs |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for key, row in read(name)['totals'].items():
        values = [f'{row["solve_us"]/1000:.3f}'] + [str(row[k]) for k in
            ('unknown', 'nodes', 'expansions', 'residual_calls', 'pn_nodes', 'pn_aborts', 'pn_attempt_skips', 'watchdogs')]
        lines.append('| ' + key + ' | ' + ' | '.join(values) + ' |')
    lines += ['']
late = read('late.json')['records']
assert len(late) == 78 and all(r['result'] in (1, 2) for r in late)
lines += [f'Training selected `{read("selection.json")["setting"]}` before confirmation.', '',
    'All 78 late checks (26 reused roots × three settings) matched their independent known outcomes. '
    'These are single-repeat correctness checks, not timing evidence.', '',
    'UNKNOWN attempts never publish solved game facts. Capped mode suppresses repeat attempts on the '
    'same D4-canonical board only within one root; this suppression and all quotas reset for the next root. '
    'Symmetric orientations can use different move orders, so suppressing their retries is a search policy, '
    'not a claim that their bounded computations are identical.', '',
    'One-host timing differences do not establish statistical superiority. The residual default remains OFF; '
    'omitting the attempt cap preserves the previous whole-root-quota behavior.', '']
(HERE / 'comparison.md').write_text('\n'.join(lines))
