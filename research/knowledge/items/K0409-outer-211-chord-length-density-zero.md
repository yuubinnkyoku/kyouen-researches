---
id: K0409
title: 外側二重点型の共円完成弦長は無限に存在するが自然密度0
kind: proposition
status: proved
topics:
- geometry
- statistics
- rectangles
aliases: []
relations:
- type: depends_on
  target: K0408
  note: 外側二次形式とPell族を利用
artifacts:
- path: research/experiments/geometry/reports/outer-211-two-point-chord-density-20261011.md
  role: proof
  note: 密度0とPell族の全称証明
- path: research/experiments/geometry/scripts/verify_outer_211_two_point_density_20261011.py
  role: verifier
  note: 合同障害・再帰の有限監査
- path: research/experiments/geometry/output/outer-211-two-point-chord-density-20261011.txt
  role: data
  note: 監査記録
- path: research/experiments/geometry/reports/outer-211-pell-norm-criterion-20261011.md
  role: proof
  note: Z[sqrt(2)]ノルムによる必要十分条件
- path: research/experiments/geometry/scripts/verify_outer_211_norm.py
  role: verifier
  note: 素因数判定と行列式照合
- path: research/experiments/geometry/output/outer_211_norm_audit_20261011.txt
  role: data
  note: 3000条件の監査
scope: 各固定h>=1の外側2+1+1型共円完成弦長集合D_h
evidence: 合同障害・素数逆数和発散による密度0とPell再帰による無限構成。
---

固定h>=1で行y=0の二点とy=h,2hの各一点が共円に完成できる弦長dの集合D_hは自然密度0だが無限である。共円条件は `2X²−Y²=d²+8h²`。

無限性はPell再帰から幅内に収まる整数格子四点族を構成する。密度0は `p≡3 (mod8)`, p∤h の素数に対して、`p | d²+8h²` ならp進付値が偶数である必要条件を使う。各素数で一定割合の剰余類を除外し、該当素数の逆数和発散から上密度0を得る。算術級数の逆数和発散は標準整数論定理として使用する。

有限監査は証明と区別する。結論はこの外側二重点型に限定され、全禁止四点組やゲーム安定化へ一般化しない。
