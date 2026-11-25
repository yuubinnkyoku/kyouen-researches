---
id: K0452
title: 四行8点円の実現傾きには少なくとも三つの集積点があり種類数は対数以上
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0432
  note: 既約傾きとPell正規形の定義を使用
artifacts:
- path: research/experiments/fixed-width/reports/q48-dual-pell-three-accumulation-points-20261016.md
  role: proof
  note: 固定弦長係数・可変傾きの双対Pell構成、三集積点、定量的対数下界
- path: research/experiments/fixed-width/scripts/q48_dual_pell_three_limits_20261016.py
  role: verifier
  note: 三族各5世代の整数監査と1050件の4点行列式検査
- path: research/experiments/fixed-width/output/q48_dual_pell_three_limits_20261016.txt
  role: data
  note: 独立検算の実行記録
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 標準4連続整数行の非局所8点円。既約傾きA/Bの集合の集積点とA,B<=Hの種類数下界。
evidence: '2026-10-21監査。三つの双対Pell族のノルム・正値性・区間分離と固有値計数を確認。1050行列式を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


実現可能な既約傾きには少なくとも三つの異なる集積点
`3 sqrt(325/37)`, `sqrt(2429205392/39588680)`, `sqrt(5244481808/268852040)`
が存在する。対応する相異なる無限列は初期傾き `9/1`, `47/6`, `53/12` からそれぞれ厳密に減少する。

`R(H)=#{実現傾きA/B:1<=A,B<=H}` について

```
liminf R(H)/log(H) >= sum_{i=0}^2 1/log(lambda_i) > 0
```

が成り立つ。`lambda_i` は報告書に明示した各整数Pell自己同型の正固有値。下界は無界の全称証明であり、5世代の有限検査を証明の代わりにしていない。正確な増加次数、全集積点の分類、合同篩を通過する任意の傾きの実現可能性は未解決。
