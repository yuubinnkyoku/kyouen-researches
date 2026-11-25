---
id: K0376
title: 11×11 `{60,27}` の現行117手被覆には既知LOSS class 31個が全て必要
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0372
  note: 現行frontier、第三手証明書、独立証拠の信頼境界
- type: depends_on
  target: K0355
  note: 3,384 S4 classとexact S5 frontierの正本
- type: supports
  target: K0372
  note: 117/119被覆の全31 LOSS classがcoverに必要なことを幾何から再構成
artifacts:
- path: research/experiments/n11-proof-compact-20261011/README.md
  role: source
  note: 有限結果、意味の範囲、再現手順
- path: research/experiments/n11-proof-compact-20261011/scripts/analyze_class_cover.py
  role: verifier
  note: D4向きと合法第四手からLOSS classの第三手被覆を再構成
- path: research/experiments/n11-proof-compact-20261011/tests/test_class_cover.py
  role: verifier
  note: 最新mainの117/119・残り{100,108}・最小31 classを回帰検査
- path: research/experiments/n11-proof-compact-20261011/output/class-cover-minimization.json
  role: data
  note: 入力hash、31 class incidence、唯一証人による最小性
scope: K0372の凍結frontierにおける、二石root {60,27}からの119合法第三手のうち既知LOSS S4 classが覆う117手。
evidence: 3,384 canonical S4 classの状態を再読み込みし、31 LOSS classそれぞれのD4向き・第三手・合法第四手を整数幾何で検査した。coverageは保存frontierと一致し、112手は唯一のLOSS classにしか覆われず、その唯一証人31件は全31 classを含む。よってこの固定された117手の被覆では最小class数は31。
---

# 現行の117/119被覆に必要なLOSS class

最新mainのK0372由来frontierから3,384個のS4 classを読み、各classのcoverageを整数幾何から再構成した。既知LOSSは31 classで、その和集合が117個の第三手を覆う。100と108は、既知LOSS classでは覆われない。

117手中112手は候補classが一つだけであり、これらの唯一証人を集めると全31 classが含まれる。したがって、現行の既知LOSS class集合から117手を覆うには31 class全てが必要である。残る5手の候補数は2, 2, 2, 2, 13。

これはclass数だけの有限最小化である。K0372の独立証拠監査でraw-rooted evidenceが全子を支えるLOSS classは1件であり、他30 classのsolver/cache verdictを独立minimax証明に昇格させない。31というclass最小値は証明DAGの節点最小値や生成計算費用を表さず、`{60,27}` のroot verdictも変えない。rootはUNKNOWNのままである。
