# Fixed residual allocation comparison

Root quota 128, residual gate 18. Times sum per-root medians over three repeats, excluding process initialization. Normal work and P/N nodes are separate budgets.

## Training: nine reused S5 roots

| Setting | Solve ms | UNKNOWN | Work | Expansions | Calls | PN nodes | Aborts | Duplicate skips | Watchdogs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| n20000-off | 2178.086 | 9 | 180000 | 88002 | 0 | 0 | 0 | 0 | 0 |
| n20000-slice32 | 2050.668 | 9 | 180000 | 88002 | 11 | 352 | 11 | 0 | 0 |
| n20000-slice8 | 2067.671 | 9 | 180000 | 88002 | 27 | 216 | 27 | 0 | 0 |
| n20000-whole | 2115.772 | 9 | 180000 | 88002 | 4 | 512 | 4 | 0 | 0 |

## Confirmation: six fresh seeded S5 roots

| Setting | Solve ms | UNKNOWN | Work | Expansions | Calls | PN nodes | Aborts | Duplicate skips | Watchdogs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| n20000-off | 1488.856 | 6 | 120000 | 58750 | 0 | 0 | 0 | 0 | 0 |
| n20000-slice32 | 1489.420 | 6 | 120000 | 58749 | 12 | 384 | 11 | 0 | 0 |
| n20000-whole | 1518.065 | 6 | 120000 | 58748 | 5 | 384 | 3 | 0 | 0 |
| n100000-off | 7041.559 | 6 | 600000 | 287550 | 0 | 0 | 0 | 0 | 0 |
| n100000-slice32 | 6948.509 | 6 | 600000 | 287549 | 21 | 672 | 20 | 0 | 0 |
| n100000-whole | 6984.226 | 6 | 600000 | 287551 | 9 | 768 | 6 | 0 | 0 |

Training selected `slice32` before confirmation.

All 78 late checks (26 reused roots × three settings) matched their independent known outcomes. These are single-repeat correctness checks, not timing evidence.

UNKNOWN attempts never publish solved game facts. Capped mode suppresses repeat attempts on the same D4-canonical board only within one root; this suppression and all quotas reset for the next root. Symmetric orientations can use different move orders, so suppressing their retries is a search policy, not a claim that their bounded computations are identical.

One-host timing differences do not establish statistical superiority. The residual default remains OFF; omitting the attempt cap preserves the previous whole-root-quota behavior.
