---
id: K0284
title: 独立memo昇順のLOSS順位改善は凍結cohortで再現、信頼境界あり
kind: proposition
status: observed
topics:
- search-methods
- statistics
aliases: []
relations:
- type: supersedes
  target: K0086
  note: 累積memo-desc改善主張を独立memo-ascの限定結果で置換
artifacts:
- path: docs/10X10_HOLDOUT_CONFIRMATION_RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/blind-probe-holdout/independent_probe_1000000.protocol.json
  role: manifest
  note: 1020行のsolver・ordered-task固定
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/blind-probe-holdout/preregistered_summary.json
  role: data
  note: V1凍結endpoint
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/clean-holdout-v2/preregistered_summary.json
  role: data
  note: 別12親V2 endpoint
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/10X10_FRESH_PARENT_HOLDOUT_V2_PREREG.md
  role: source
  note: V2原設計とparser再凍結時の開示
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 独立memo昇順のLOSS順位改善は凍結cohortで再現、信頼境界あり

fresh child-process・1M probe・memo ascendingの順位規則。既知七親で中央値1・default比5勝2敗から固定し、V1十一親1020child全probe/全exactでは10better/1tie対random、順位和16対null期待190.97、mean AUC.820。V1は既存proof familyから選び33既知LOSS証人があったため完全なchild-outcome-blindとは呼ばない。全33証人除外後の九親でも8better/1tieを記録。

別clean V2十二親1136childのsummaryでは6better/6tie/0worse、順位和12、mean AUC.770751。ただし最初の区切り形式が不正で全probeを破棄・再収集し、その診断中に一childのWINを先に見た事実を開示している。方向・cohort・endpointの変更なし。

候補内ランダム並べ替えをnullとするpは固定cohortに条件付けた手続きbenchmarkで、全十盤親への母集団一般化確率ではない。順位改善はnative solver加速を意味しない。
