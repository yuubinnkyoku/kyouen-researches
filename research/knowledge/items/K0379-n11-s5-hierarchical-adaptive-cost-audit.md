---
id: K0379
title: 11×11 S5階層分割の費用比較と証拠対応ルーティング
kind: computation
status: computed
topics: [square-outcomes, search-methods, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元の先手固定視点におけるS5 AND・S6 ORの勝敗伝播
- type: depends_on
  target: K0371
  note: K0372による固定先手伝播と隔離規則の維持
- type: depends_on
  target: K0372
  note: solver-trusted exact葉とterminal-only独立証明の信頼分離
- type: depends_on
  target: K0374
  note: 同じ90子S6全WINの保存rawとS5導出
- type: supports
  target: K0378
  note: 最新mainの最有力S4境界40/0/66をcacheと独立幾何から再確認
artifacts:
- path: research/experiments/n11-s5-hierarchical-adaptive-20261011/README.md
  role: source
  note: 階層分割の費用、適応方式、限界、再現手順
- path: research/experiments/n11-s5-hierarchical-adaptive-20261011/scripts/strategy.py
  role: source
  note: exact evidence reuseとA–E方式選択、固定先手AND/OR集約
- path: research/experiments/n11-s5-hierarchical-adaptive-20261011/scripts/analyze.py
  role: verifier
  note: 保存raw hash、90子geometry、予算prefix、最新S4境界の再監査
- path: research/experiments/n11-s5-hierarchical-adaptive-20261011/tests/test_strategy.py
  role: verifier
  note: 極性、途中境界、trusted leaf、raw改ざん、同node-cap比較の回帰
- path: research/experiments/n11-s5-hierarchical-adaptive-20261011/output/strategy-audit.json
  role: data
  note: 15M直接UNKNOWNと29.79M全S6分割の比較および現行境界
- path: research/experiments/n11-s5-hierarchical-adaptive-20261011/output/source-manifest.json
  role: manifest
  note: 複写raw、source audit、current cacheのSHA-256照合
scope: K0374のS5一局面の保存済みraw再構成と現行最有力S4境界の再確認。新たなsolver探索やterminal-only proof DAGの追加は行っていない。
evidence: 直接S5は15,000,000 nodesでUNKNOWN、完全S6分割は90/90 WINに29,794,287 nodesを要した。同じ15M-node上限で再構成した分割prefixもS5 UNKNOWNであり、節点削減は実証されない。直接rawにsolver binary/source hashと実行hostがないため、wall time・RSSの同一環境比較は成立しない。最新mainの `(1297036692683752448,0)` はLOSS40 / WIN0 / UNKNOWN66で、追加探索は行わなかった。
---

# S5階層分割の保存raw比較

K0374対象のS5 `(1188950301626859520,603979776)` を、直接15M replayと完全S6分割の保存rawで再構成した。90個のS6子は初回85 WIN・5 UNKNOWNで、5子の15M retryがすべてWIN。S5の固定先手視点AND則からS5 WINを導くには全90子が必要だった。

分割runは全群合計29,794,287 nodesで、15M直接runの1.986倍である。15M-nodeで止める分割順序のprefixでは60子exact、2 UNKNOWN run、30子が未観測または未確定となりS5 UNKNOWN。これは保存rawを使った予算prefix再構成であって追加探索ではない。従って、難S5を解決した例ではあるが、直接法より少ない計算量で解決した例ではない。

S6 rawのhostはDebian / Intel i5-9400Tとして記録される一方、直接rawにhost・binary SHA-256・source SHA-256がなく、直接raw時間47秒と分割raw時間合計83秒を比較できない。どちらも最大RSS未記録である。S6の90 exact値はsolver-trustedであり、terminal-only独立証明ではない。

最新mainの最有力S4 `(1297036692683752448,0)` は独立幾何と追跡済みexact cacheから106子のLOSS40 / WIN0 / UNKNOWN66として再確認した。node削減が実証できず、別作業のrawを上書きせず、現行S4のS5探索はdispatchしていない。
