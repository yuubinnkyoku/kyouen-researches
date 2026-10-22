#!/usr/bin/env python3
from study import HERE,read
totals=read('summary.json')['totals']
lines=['# Fixed frame child geometry comparison','',
    'Times sum per-root medians over three repeats, excluding initialization. Residual/native exact handoffs are OFF. '
    'All OFF/cache pairs have identical outcomes, stop reasons, work and expansions.','',
    '| Group / limit | OFF ms | Cache ms | Change | OFF builds | Cache builds | Saved geometry moves | Refreshes | UNKNOWN OFF/cache |',
    '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for group in ('reused','fresh','late'):
    for limit in ([20000] if group=='late' else [20000,100000]):
        off=totals[f'{group}-n{limit}-off'];on=totals[f'{group}-n{limit}-cache']
        change=(on['solve_us']/off['solve_us']-1)*100
        lines.append(f'| {group} / {limit} | {off["solve_us"]/1000:.3f} | {on["solve_us"]/1000:.3f} | {change:+.1f}% | '
            f'{off["geometry_builds"]} | {on["geometry_builds"]} | {off["geometry_moves"]-on["geometry_moves"]} | '
            f'{on["child_refreshes"]} | {off["unknown"]}/{on["unknown"]} |')
lines+=['','## Separate fresh-list audit','',
    '| Root | Work | Refreshed lists | Successful full comparisons |','|---|---:|---:|---:|']
for row in read('audits.json'):
    lines.append(f'| {row["id"]} | {row["nodes"]} | {row["child_refreshes"]} | {row["child_audits"]} |')
lines+=['','The audit rebuilds all child geometry and rereads bounds at every refresh, and is excluded from timing. '
    'Geometry-build substitution is checked exactly for all timed pairs: OFF builds = cache builds + refreshes.', '',
    'The six fresh roots were generated and committed before timing. The nine reused deep roots and 26 late roots '
    'were previously exposed; they are not new holdouts. All 336 timed evaluations and three audits are retained. '
    'One-host timing differences do not prove performance on other positions or machines. '
    'The cache remains an explicit normal-search option, and deep root outcomes remain unresolved.', '']
(HERE/'comparison.md').write_text('\n'.join(lines))
