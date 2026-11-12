---
id: K0777
title: 二値立方体重み2層の13次元最小極大配置は17石
kind: computation
status: computed
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0744
  note: 重み2層のC4対応とn+3下界
- type: depends_on
  target: K0742
  note: 葉を持つ13頂点C4飽和グラフは17辺以上
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-n13-proof.md
  role: proof
  note: 葉なし16辺候補を核・道長の有限ケースへ帰着
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_tetracyclic_cores.cpp
  role: verifier
  note: 同型を除いた多重グラフの核と道長を列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-n13-candidates.txt.gz
  role: data
  note: 55822候補の核と道長。異なる候補が同型の場合を含む
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_tetracyclic_cores.py
  role: verifier
  note: 核・道長の被覆を独立生成で照合し四角形マスクで全候補を検査
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-n13-audit.json
  role: data
  note: 独立監査の候補数・C4禁止数・飽和数と入力hash
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_tetracyclic_positive.py
  role: verifier
  note: 8頂点11辺の陽性例を全辺集合列挙と自己同型による軌道数で照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-positive-control.json
  role: data
  note: 8頂点陽性対照の5同型類と90720配置の照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-odd-dimension-improved-saturation-20261110.md
  role: certificate
  note: 13頂点17辺の明示構成
scope: 二値立方体13次元の重み2層、共面四点禁止、包含極大安全配置の最小サイズ。有限計算に依存し、全立方体や正方形格子には適用しない。
evidence: 葉あり16辺を理論的に排除し、葉なし候補を最大6分岐頂点の核と道長55822通りに帰着。核・道長の被覆と全候補の四角形マスク判定を独立に照合。17辺構成が存在。
---

# 13次元重み2層の最小極大配置

二値立方体 `{0,1}^13` の重み2層で共面四点を禁止すると、包含極大安全配置の最小サイズは **17石**。これは構造縮約と有限全数検査に依存する結論である。

K0744の下界は16石。16辺候補に葉があればK0742により少なくとも17辺必要なので、候補は葉を持たない。次数2の道を縮約すると、次数3以上の分岐頂点1〜6個と、その頂点数より3本多い辺からなる連結多重グラフの核に帰着する。ループ・平行辺を含む核と、単純グラフに展開可能な道長の候補は55822通り。

うちC4を含まない19567候補に飽和グラフはなかった。核の同型類と道長の被覆を別実装で照合し、全候補のC4不在・欠辺追加を四角形マスクで再検査して一致した。8頂点11辺の陽性対照では5同型類を検出し、軌道の総数90720が全辺集合の別列挙と一致した。奇数次元の明示構成は17石を与えるため、最小値は17。

これは13次元に限る結果で、一般次元での厳密値やゲームの勝敗は示さない。先行する固定辺SATの50万衝突試行はUNKNOWNであり、本結果はSATによるUNSAT証明に依存しない。
