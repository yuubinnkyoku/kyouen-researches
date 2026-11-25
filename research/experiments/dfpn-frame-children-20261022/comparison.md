# Fixed frame child geometry comparison

Times sum per-root medians over three repeats, excluding initialization. Residual/native exact handoffs are OFF. All OFF/cache pairs have identical outcomes, stop reasons, work and expansions.

| Group / limit | OFF ms | Cache ms | Change | OFF builds | Cache builds | Saved geometry moves | Refreshes | UNKNOWN OFF/cache |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| reused / 20000 | 2077.811 | 1491.117 | -28.2% | 268002 | 178020 | 6567532 | 89982 | 9/9 |
| reused / 100000 | 9269.068 | 6966.678 | -24.8% | 1330630 | 880648 | 27324641 | 449982 | 9/9 |
| fresh / 20000 | 1486.324 | 1061.362 | -28.6% | 178644 | 118655 | 4421536 | 59989 | 6/6 |
| fresh / 100000 | 6954.096 | 4514.078 | -35.1% | 887014 | 587026 | 18315642 | 299988 | 6/6 |
| late / 20000 | 13.305 | 9.799 | -26.4% | 6263 | 4047 | 18092 | 2216 | 0/0 |

## Separate fresh-list audit

| Root | Work | Refreshed lists | Successful full comparisons |
|---|---:|---:|---:|
| reused-0 | 2000 | 999 | 999 |
| reused-1 | 2000 | 998 | 998 |
| reused-2 | 2000 | 998 | 998 |

The audit rebuilds all child geometry and rereads bounds at every refresh, and is excluded from timing. Geometry-build substitution is checked exactly for all timed pairs: OFF builds = cache builds + refreshes.

The six fresh roots were generated and committed before timing. The nine reused deep roots and 26 late roots were previously exposed; they are not new holdouts. All 336 timed evaluations and three audits are retained. One-host timing differences do not prove performance on other positions or machines. The cache remains an explicit normal-search option, and deep root outcomes remain unresolved.
