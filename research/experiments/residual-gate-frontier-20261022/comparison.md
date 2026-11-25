# Fixed gate comparison

Times below sum per-root medians over three repeats, in milliseconds. Initialization is excluded. UNKNOWN roots retain their specified work limits.

## Diagnostic (profile ON, excluded from timing comparison)

| Training root | Unresolved stage-0 visits | Min legal | Max legal | Legal ≤24 | Legal ≤48 |
|---|---:|---:|---:|---:|---:|
| train-26 | 50002 | 17 | 93 | 396 | 24470 |
| train-27 | 50002 | 17 | 86 | 436 | 28442 |
| train-28 | 50002 | 18 | 95 | 114 | 20009 |

## Training: three reused deep roots

| Limit / gate | Solve ms | UNKNOWN | Work nodes | Expansions | PN nodes | PN aborts | Handoffs | Watchdogs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| n20000-g0 | 674.304 | 3 | 60000 | 29220 | 0 | 0 | 0 | 0 |
| n20000-g6 | 671.819 | 3 | 60000 | 29220 | 0 | 0 | 0 | 0 |
| n20000-g12 | 645.608 | 3 | 60000 | 29220 | 0 | 0 | 0 | 0 |
| n20000-g18 | 638.019 | 3 | 60000 | 29220 | 256 | 2 | 2 | 0 |
| n20000-g24 | 657.070 | 3 | 60000 | 29220 | 384 | 3 | 3 | 0 |
| n20000-g32 | 680.121 | 3 | 60000 | 29220 | 384 | 3 | 3 | 0 |
| n20000-g48 | 677.396 | 3 | 60000 | 29220 | 384 | 3 | 3 | 0 |
| n20000-g64 | 691.382 | 3 | 60000 | 29220 | 384 | 3 | 3 | 0 |

## Prospective confirmation: six seeded deep roots

| Limit / gate | Solve ms | UNKNOWN | Work nodes | Expansions | PN nodes | PN aborts | Handoffs | Watchdogs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| n20000-g0 | 1636.312 | 6 | 120000 | 58782 | 0 | 0 | 0 | 0 |
| n20000-g6 | 1564.214 | 6 | 120000 | 58782 | 0 | 0 | 0 | 0 |
| n20000-g18 | 1575.638 | 6 | 120000 | 58782 | 256 | 2 | 2 | 0 |
| n100000-g0 | 6993.853 | 6 | 600000 | 287643 | 0 | 0 | 0 | 0 |
| n100000-g6 | 7141.079 | 6 | 600000 | 287643 | 0 | 0 | 0 | 0 |
| n100000-g18 | 7388.822 | 6 | 600000 | 287641 | 768 | 6 | 8 | 0 |

Training selected gate 18; the selection was committed before confirmation.

All 26 reused late roots matched their independent known outcomes in all three settings (78 checks). These single-run checks are correctness regressions, not a timing holdout.

Frame counts include revisits and exclude already solved TT frames. They are not unique positions. Timing differences on one host do not establish statistical superiority; identical work counts must not be described as reduced search effort. The default gate remains OFF.
