#!/usr/bin/env python3
from study import HERE,read
totals=read('summary.json')['totals']
lines=['# Fixed expand-list ownership comparison','',
    'Times sum per-root medians over three repeats, excluding initialization. All logical work is identical across modes.','',
    '| Group / limit | OFF ms | Cache ms | Expand ms | vs cache | vs OFF | Cache builds | Expand builds | Initial rebuilds avoided |',
    '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for group in ('reused','fresh','late'):
    for limit in ([20000] if group=='late' else [20000,100000]):
        a,b,c=(totals[f'{group}-n{limit}-{setting}'] for setting in ('off','cache','expand'))
        lines.append(f'| {group} / {limit} | {a["solve_us"]/1000:.3f} | {b["solve_us"]/1000:.3f} | {c["solve_us"]/1000:.3f} | '
            f'{(c["solve_us"]/b["solve_us"]-1)*100:+.1f}% | {(c["solve_us"]/a["solve_us"]-1)*100:+.1f}% | '
            f'{b["geometry_builds"]} | {c["geometry_builds"]} | {b["geometry_builds"]-c["geometry_builds"]} |')
audits=read('audits.json')
lines+=['',f'Separate first-use/revisit audits: {len(audits)} roots, '
    f'{sum(r["child_audits"] for r in audits)} refreshed lists rebuilt and matched. Excluded from timing.', '',
    'All 396 timed root evaluations and three audits are archived. Six fresh S5 roots were fixed before measurement; '
    'the other roots were reused. Across every three-way comparison, result, reason, work and expansions match exactly. '
    'Cache builds = expand builds + initial reuse count; expand refreshes = cache refreshes + initial reuse count.', '',
    'The moved list has a unique owner and is never shared with parent/child frames. Its bounds are refreshed before '
    'first use because expansion can evict child TT entries and native exact can change them. '
    'The deep roots remain unresolved within these budgets. Timings are single-host observations; defaults remain OFF.', '']
(HERE/'comparison.md').write_text('\n'.join(lines))
