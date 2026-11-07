---
id: K0691
title: 純三点ゲームのGrundy6と7は最少点数が八と九、最少辺数はともに六本
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0687
  note: 五本以下の三点辺ならg<=5という全称下界根拠
- type: depends_on
  target: K0108
  note: 自由点一個はxor1でg6をg7へ移す
- type: depends_on
  target: K0683
  note: 有限整数点盤での達成
- type: depends_on
  target: K0690
  note: 合法点数の最小値の下界
artifacts:
- path: research/experiments/pure-triple-six-edge-witnesses-20261108/proof.md
  role: proof
  note: 九点六辺g6の具体例、自由点付きg7、五辺以下の排除
- path: research/experiments/pure-triple-six-edge-witnesses-20261108/search.py
  role: verifier
  note: 五辺高Grundy核への一辺追加探索とC++/Python根値照合
- path: research/experiments/pure-triple-six-edge-witnesses-20261108/output/search.json
  role: certificate
  note: 831入力の探索範囲・度数と九点達成例の全初手値
- path: research/experiments/pure-triple-grundy-synthesis-20261108/audit.py
  role: verifier
  note: 八点g6・九点g7のPython原始mexと整数点盤の全共円四点組・全安全状態を検査
- path: research/experiments/pure-triple-grundy-synthesis-20261108/output/witness_audit.json
  role: certificate
  note: 最少点数達成例、全初手値、14点と15点の具体的整数座標盤
- path: research/log/2026-11-08-grundy-mobility-gap-and-hyperforests.md
  role: log
  note: 辺数最小と合法点数最小を区別した研究記録
scope: 任意個の自由点を許す純三点極小禁止族、通常プレイ。g6とg7に必要な点数と辺数の最小化。点数下界は任意rankでも成立。六辺での最大Grundyの主張ではない。
evidence: 八点六辺のg6と自由点付き九点g7をC++生subsetと独立Python再帰で検査し、整数点盤にも移して全四点組・全安全状態を検査。K0687が五辺以下を排除し、K0690が八点・九点未満を排除。
---

Grundy6および7を実現する純三点辺数の最小値は、ともに **6**。
最少合法点数はそれぞれ **8,9** で、任意rankを許しても同じ最小値となる。
八点上の辺mask族 `22,38,41,49,88,146` の根値が6で、
全初手値は頂点0..7の順に `5,1,3,4,2,0,5,0`。
自由点一個を加えた九点族は値7となる。
K0687により五辺以下なら自由点込みでもg≤5、
K0690によりg≥4を実現するには合法点がg+2個以上必要なので、両最小値が確定する。

五辺でg≥4の全七核型からの一辺追加831入力を調べ、達成例を得た。
その後、seed20261108の八点ランダム探索481番目で上記の最少点数達成例を発見。
六辺全族の完全列挙ではなく、六辺の最大値やg≤7を保証する計算ではない。

[証明・達成例・探索範囲](../../experiments/pure-triple-six-edge-witnesses-20261108/proof.md)を参照。
K0683で指定有限整数点盤へ実現できるが、全正方形格子盤での達成は未主張。
整数座標の14点盤（占有六点・合法八点）と15点盤（占有六点・合法九点）の
全共円四点組と安全状態のGrundyも、保存した座標から検査済み。
