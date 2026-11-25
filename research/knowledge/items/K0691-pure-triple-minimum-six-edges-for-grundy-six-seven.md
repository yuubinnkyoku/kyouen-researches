---
id: K0691
title: 純三点のGrundy6と7は最少点数八と九・最少辺数六で、辺数最小核は全十型
kind: proposition
status: proved
topics:
- grundy
- residual-games
- geometry
- variants
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
- path: research/experiments/pure-triple-six-edge-complete-20261108/proof.md
  role: proof
  note: 六辺完全表と任意個自由点の全称分類
- path: research/experiments/pure-triple-six-edge-complete-20261108/catalog.py
  role: verifier
  note: 全十高値核の抽出と独立補助値再評価
- path: research/experiments/pure-triple-six-edge-complete-20261108/output/maximal_six_kernels.json
  role: certificate
  note: 八点三型・九点六型・十点一型の全十核と補助値
scope: 任意個の自由点を許す純三点極小禁止族、通常プレイ。g6/g7の最少合法点数と最少辺数、六辺での全高値核分類。点数下界は任意rankでも成立。
evidence: 八点六辺g6と自由点付き九点g7を独立再帰・subset・整数座標で検査。六辺全4279核の完全表でg6は十型だけ、核g7以上はゼロ。自由点xor則で任意点数の六辺高値族を分類。
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
この先行探索自体は六辺全族の完全列挙ではない。その後、全六辺核4,279型の計算が完了した。

[証明・達成例・探索範囲](../../experiments/pure-triple-six-edge-witnesses-20261108/proof.md)を参照。
K0683で指定有限整数点盤へ実現できるが、全正方形格子盤での達成は未主張。
整数座標の14点盤（占有六点・合法八点）と15点盤（占有六点・合法九点）の
全共円四点組と安全状態のGrundyも、保存した座標から検査済み。


## 最少辺数の全高値核

全六辺核のgは6以下で、g=6はちょうど十型。点数別には **八点三型、九点六型、十点一型**。
従って任意点数の六辺族について、g=6となるのはこの十核のいずれかに偶数個の自由点を加えた場合、
g=7となるのは奇数個を加えた場合に限る。八点g6・九点g7で点数と辺数の最小を同時達成する核は三型。
[全十型と各辺mask](../../experiments/pure-triple-six-edge-complete-20261108/output/maximal_six_kernels.json)を保存する。

八点三型の補助値は全てh=6、自由点一個でh=7だが、十型全体にはhが1/0や0/1の型もある。
この通常値分類をhの高値族分類と同一視しない。
[完全生成・独立検査・自由点分類の証明](../../experiments/pure-triple-six-edge-complete-20261108/proof.md)を参照。
