# Profile OFF: per-root median sums (3 repeats)

| corpus | gate | scan solve ms | indexed solve ms | reduction | nodes |
|---|---:|---:|---:|---:|---:|
| saved | 0 | 6.951 | 7.094 | -2.1% | 1097 |
| saved | 6 | 37.734 | 6.308 | 83.3% | 153 |
| saved | 12 | 25.674 | 9.532 | 62.9% | 26 |
| stress | 0 | 26.198 | 26.354 | -0.6% | 15000 |
| stress | 6 | 2671.000 | 95.320 | 96.4% | 15000 |
| stress | 12 | 8668.751 | 3301.431 | 61.9% | 15000 |

gate 0 はbuilderを呼ばない。同じ処理を別時間帯に測ったばらつきの参考。
全52局面は独立期待値と一致、深い3局面は全設定・全反復UNKNOWN。
各node予算5000。UNKNOWNの探索ノードは各3局面合計15000。
setupを除いたsolve時間を比較する。各行のsolver初期化には約0.5秒が別途必要。

# Profile ON: exclusive phase sums (1 repeat)

| builder | corpus | gate | construction ms | structure ms | Grundy remainder ms |
|---|---|---:|---:|---:|---:|
| scan | saved | 6 | 32.699 | 0.351 | 0.387 |
| scan | saved | 12 | 19.638 | 2.166 | 2.971 |
| scan | stress | 6 | 2251.054 | 21.016 | 18.149 |
| scan | stress | 12 | 5594.272 | 1302.960 | 1794.708 |
| indexed | saved | 6 | 0.664 | 0.438 | 0.456 |
| indexed | saved | 12 | 1.459 | 1.991 | 3.477 |
| indexed | stress | 6 | 21.405 | 20.546 | 16.505 |
| indexed | stress | 12 | 199.819 | 1410.371 | 1913.772 |
