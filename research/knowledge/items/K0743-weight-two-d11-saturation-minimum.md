---
id: K0743
title: 二値立方体重み2層の11次元最小極大配置は14石
kind: computation
status: computed
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0715
  note: 重み2層のC4対応と一般下界
- type: depends_on
  target: K0742
  note: 葉を持つ11頂点C4飽和グラフは14辺以上
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tricyclic-n11-proof.md
  role: proof
  note: 次数2の道の縮約による全候補の有限核への帰着
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_tricyclic_cores.py
  role: verifier
  note: ループと平行辺を許す核および道長の全候補を列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tricyclic-n11-result.json
  role: data
  note: 10408候補・C4禁止4452候補・極大0件
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_tricyclic_cores.py
  role: verifier
  note: 6・7頂点の全対象グラフの核被覆と11頂点全候補の四角形マスク照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tricyclic-n11-audit.json
  role: data
  note: 小次元被覆および11頂点候補の独立判定結果
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-odd-dimension-improved-saturation-20261110.md
  role: certificate
  note: 11頂点14辺の明示構成
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/d11-c4-saturation-sat-20261111/result.json
  role: data
  note: 固定辺SATの50万衝突試行はUNKNOWN
scope: 二値立方体11次元の重み2層、共面四点禁止、包含極大安全配置の最小サイズ。有限計算に依存し、全立方体や正方形格子には適用しない。
evidence: 葉あり13辺を理論的に排除し、葉なし候補を1..4分岐頂点の核と道長10408通りに帰着。C4禁止4452通りに極大候補がないことを2判定法で照合。14辺の明示構成が存在。
---

# 11次元重み2層の最小極大配置

二値立方体 `{0,1}^11` の重み2層で共面四点を禁止すると、包含極大安全配置の最小サイズは **14石**。構造縮約と有限全数検査に依存する結論である。

一般下界は13石。13辺のC4飽和グラフに葉があればK0742により14辺以上となるため、13辺候補は最小次数2以上。次数2の道を縮約すると、次数3以上の分岐頂点1〜4個、辺数が分岐頂点数より2多い連結多重グラフの核に帰着する。ループ・平行辺を含む核と、単純グラフへの道長を列挙すると10408通りある。

うちC4を含まない4452通りについて極大候補は0件。独立の四角形マスク判定でも一致し、6・7頂点では全対象ラベル付きグラフを直接縮約して核生成の被覆を確認した。奇数次元の構成は14石を与えるため、最小値は14。通常・misèreの勝敗や一般次元の厳密値は示さない。固定辺SATの50万衝突試行はUNKNOWNであり、この結論はSATによるUNSAT証明には依存しない。
