# 通常df-pnの固定比較

legal gate=6、P/N quota=128を再調整せず、OFFと比較。3反復の局面ごとの中央値合計。
work nodesはdf-pn反復 + 内部exact board nodes。P/N callsは別枠。

| corpus | node limit | setting | UNKNOWN | solve ms | work nodes | expansions | PN calls | aborted roots | watchdog runs |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| late | 20000 | off | 0 | 14.171 | 4458 | 1805 | 0 | 0 | 0 |
| late | 20000 | pn128-g6 | 0 | 6.925 | 1262 | 243 | 462 | 0 | 0 |
| late | 100000 | off | 0 | 14.038 | 4458 | 1805 | 0 | 0 | 0 |
| late | 100000 | pn128-g6 | 0 | 6.718 | 1262 | 243 | 462 | 0 | 0 |
| deep | 20000 | off | 3 | 664.375 | 60000 | 29220 | 0 | 0 | 0 |
| deep | 20000 | pn128-g6 | 3 | 687.183 | 60000 | 29220 | 0 | 0 | 0 |
| deep | 100000 | off | 3 | 2929.270 | 300000 | 142987 | 0 | 0 | 0 |
| deep | 100000 | pn128-g6 | 3 | 3095.168 | 300000 | 142987 | 0 | 0 | 0 |

| corpus | node limit | ON / OFF solve time | difference |
|---|---:|---:|---:|
| late | 20000 | 0.4887 | -51.1% |
| late | 100000 | 0.4786 | -52.1% |
| deep | 20000 | 1.0343 | +3.4% |
| deep | 100000 | 1.0566 | +5.7% |

入力はK0497の既知26局面と以前からの深い3局面。今回は新しいholdoutとは呼ばない。
29 roots × 2 settings × 2 limits × 3 repeats = 348 root solves。各processはcold solver/TT。
通常探索の既定gateはOFF。明示flagでのみ有効にする。既存exact handoffを併用しなくても残余評価が働く。
process時間には約0.5秒/根の初期化が別途含まれる。上のsolve時間は初期化を除く。
node limitはexpansion数や以前のexact replayのboard node数とは異なる指標。
単一host・固定局面の観測で、時間差の統計的有意性や他の初期局面での性能は主張しない。
