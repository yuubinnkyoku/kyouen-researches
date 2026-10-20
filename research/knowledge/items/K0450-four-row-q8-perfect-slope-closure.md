---
id: K0450
title: 四行8点円の実現傾きは非空な完全閉包を持ち集積点が非可算個存在する
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0432
  note: 傾き正規形と固定傾きPell延長を使用
artifacts:
- path: research/experiments/fixed-width/reports/q48-perfect-slope-closure-20261016.md
  role: proof
  note: 任意の奇数分子・偶数分母・3と互いに素な実現傾きへの双対Pell構成と完全閉包の全称証明
- path: research/experiments/fixed-width/scripts/q48_perfect_slope_closure_verify_20261016.py
  role: verifier
  note: 2種類の種・4世代の法6保存、560件の独立共円行列式検算
- path: research/experiments/fixed-width/output/q48_perfect_slope_closure_audit_20261016.txt
  role: data
  note: 有限整数監査の実行結果
scope: 標準4行q=8非局所円の実現既約正傾き集合。A奇数、B偶数、3∤Aの部分集合とその実数閉包。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


実現可能な既約正傾きのうち `A` 奇数、`B` 偶数、`3∤A` を満たす集合 `S0` は、各点の直下に同じ集合の相異なる傾きが無限に存在して収束する。したがって `S0` は孤立点を持たず、その実数閉包は非空な完全集合。実現傾き全体の集積点は非可算無限個である。

任意の有限 `j>=1` について `S0` は `j` 回集積点集合を取った集合に含まれる。固定傾きPellで弦長を大きくし、双対Pell行列の24乗で法6合同類を保ったまま傾きを動かす全称証明による。既知の47/6と53/12を有限独立検証し、560件の4点共円行列式が一致。閉包が区間を含むか、傾きの増加次数は未解決。
