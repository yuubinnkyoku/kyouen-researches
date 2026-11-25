---
id: K0436
title: 異方整数格子の全幅で3進付値条件下の円点数は2ceil(2w/3)以下
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0001
  note: q点完全指摘ルール
- type: depends_on
  target: K0002
  note: Grundy値と通常プレイの定義
artifacts:
- path: research/experiments/fixed-width/reports/anisotropic-mod9-all-widths-20261016.md
  role: proof
  note: 3進二階差商と法9の81組分類を用いた無界の全称証明
- path: research/experiments/fixed-width/scripts/mod9_anisotropic_rows_20261016.py
  role: verifier
  note: 81組の完全剰余検査と二通りの計算式の照合
- path: research/experiments/fixed-width/scripts/anisotropic_circle_independent_20261016.cpp
  role: verifier
  note: 非共線三点から整数円を構成する独立有限盤検証
- path: research/experiments/fixed-width/output/mod9_anisotropic_rows_20261016.txt
  role: data
  note: 81剰余組の全分類と周期帰納の基底値
- path: research/experiments/fixed-width/output/anisotropic_circle_independent_20261016.txt
  role: data
  note: 17種類の有限盤の全円列挙結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
solution:
  board: 異方格子w×m・q点版
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: w≥5、h,d≥1、v₃(d)≤v₃(h)、q>2ceil(2w/3)
  verification:
  - mathematical-proof
  - independent-enumeration
  certificate: 3進二階差商・法9剰余の81組完全分類と9周期帰納
  independent_check: 17種類の有限盤の全非共線三点から整数円を独立列挙
  note: M=q−1、g(S)=(w min(m,q−1)−|S|) mod2
evidence: '2026-10-21監査。3進補間・法9の81組・9周期の全幅帰納を確認。Python合同検査と17有限盤の独立C++を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 異方格子全幅の共円点数上界と全長強解決

整数 `w≥5`、正整数の水平格子間隔 `h`・垂直行間隔 `d` に対し、`v₃(d)≤v₃(h)` なら、任意の円が連続する `w` 本の無限水平格子から取る点数は高々 `2ceil(2w/3)`。特に幅5・6では最大8点、幅7では最大10点、幅8・9では最大12点となる。この上界は `h=d=1` の幅5〜9で同一円 `x²+y²+x−7y=0` により達成される。

従って `q>2ceil(2w/3)` のq点共線・共円禁止版では、任意の有限横幅 `m≥1` で各行が独立な容量 `min(m,q−1)` を持ち、全安全局面 `S` について `g(S)=(w min(m,q−1)−|S|) mod 2`。満容量安定化長は厳密に `M=q−1`。

全称性の根拠は、二重点行があるとき全占有行の水平二根和が整数になること、3進付値が不等なら占有行番号は法3の高々二剰余類に限られること、3進付値が等しいなら法9の平方剰余81組分類から占有行が高々 `ceil(2w/3)` となることによる。剰余補題の有限完全検査と、独立した17有限盤の整数円全列挙を実施した。

`v₃(d)>v₃(h)` は対象外。`w≥10` で点数上界が最適とは主張しない。既存の標準格子専用のより鋭い上界は置き換えない。詳細な証明と検証境界は上記proof artifactに記録した。
