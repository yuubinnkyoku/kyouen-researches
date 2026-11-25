# 所属被覆重みによるGrundy上界

2026-11-07の一次資料。現在の命題はK0688。

```sh
uv run --locked python research/experiments/incidence-weighted-grundy-bound-20261107/verify.py
```

標準ライブラリのみ。全rank・5点以下の全7020clutterと全安全状態を原始subset再帰で監査する。
一般定理・次数のみの系・局所重みの系の全称証明は`proof.md`。
`output/audit.json`は有限監査集計で、solverの速度測定ではない。
