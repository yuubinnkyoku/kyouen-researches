# Fixed expand-list ownership comparison

Times sum per-root medians over three repeats, excluding initialization. All logical work is identical across modes.

| Group / limit | OFF ms | Cache ms | Expand ms | vs cache | vs OFF | Cache builds | Expand builds | Initial rebuilds avoided |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| reused / 20000 | 628.173 | 459.822 | 377.301 | -17.9% | -39.9% | 59226 | 30006 | 29220 |
| reused / 100000 | 3232.592 | 2497.325 | 1438.116 | -42.4% | -55.5% | 292993 | 150006 | 142987 |
| fresh / 20000 | 1437.309 | 1035.383 | 681.310 | -34.2% | -52.6% | 118629 | 60011 | 58618 |
| fresh / 100000 | 6903.759 | 4961.591 | 2944.253 | -40.7% | -57.4% | 586554 | 300012 | 286542 |
| late / 20000 | 13.695 | 10.802 | 8.247 | -23.7% | -39.8% | 4047 | 2242 | 1805 |

Separate first-use/revisit audits: 3 roots, 5949 refreshed lists rebuilt and matched. Excluded from timing.

All 396 timed root evaluations and three audits are archived. Six fresh S5 roots were fixed before measurement; the other roots were reused. Across every three-way comparison, result, reason, work and expansions match exactly. Cache builds = expand builds + initial reuse count; expand refreshes = cache refreshes + initial reuse count.

The moved list has a unique owner and is never shared with parent/child frames. Its bounds are refreshed before first use because expansion can evict child TT entries and native exact can change them. The deep roots remain unresolved within these budgets. Timings are single-host observations; defaults remain OFF.
