---
id: K0418
title: 夜間層別後の共同計画の厳密双対182532671/27720は整数下界6,585
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0417
  note: 二つの終局verdictを反映した19-root共同選択問題・現行上界31,636
- type: verifies
  target: K0417
  note: 双対値の厳密再計算と31,546計画の独立再検証（失敗0）
artifacts:
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/dual_certificate.py
  role: source
  note: deg再集計・厳密有理数alpha・証明書発行と--verify再検査
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/disjoint_pool_packing.py
  role: source
  note: pool-disjoint packingによる独立整数下界（346、採用せず）
- path: research/experiments/n11-proof-cost-comparison-20261012/output/element-dual-certificate.json
  role: certificate
  note: deg 962,469要素・869群alpha・厳密総和と整数下界
- path: research/experiments/n11-proof-cost-comparison-20261012/README.md
  role: source
  note: 証明戦略比較の全体記録（課題1〜5）
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/updated_dual.py
  role: verifier
  note: 新インスタンスの全選択肢の厳密有理数最小・degree再計算・証明書検査
- path: research/experiments/n11-s5-s6-quotient-20261013/output/updated-element-dual.json
  role: certificate
  note: 現行869群alpha・厳密総和・degree hash・整数下界6577
scope: K0417の修復後インスタンス（S5 LOSS558600を費用から削除、WIN209644を含む2 S4を排除）の869有料群・選択肢別未知S5費用の最小和集合問題に対するelement-only分数双対。solver探索なし。
evidence: 現行インスタンスのdeg 962,467要素と34,447選択肢を再計算、各群の全選択肢について厳密有理数でminを取り、総和91145221/13860=6576.134271…、整数下界6,577。--verifyは869群・95,225選択肢不等式と全degreeを再計算して通過。現行上界31,636。旧cache計算の履歴として依存グラフからdegを再集計し、各群のalphaを厳密有理数で評価して総和2024529/308＝6573.1461…を得た。--verifyがdeg一致・alpha一致・総和一致を確認し、K0417公表値6573.146と整合した。最適値が和集合濃度ゆえ整数のためOPT≥6574を採用する。重み族内ではw＝1/degが単調性より最適で、重み調整の改善余地はない。pool-disjoint packingは有効だが346に留まる。上下差（6,574対31,546）は未解決。
---

## 現行下界と検証

K0423の終局証明を反映した現行インスタンスでは、総和91145221/13860、整数下界6,577が確定する。
948群のうち有料869群、degree対象962,467要素、相異なる選択肢34,447。
各有料群の全選択肢の重み和をFractionで正確に評価し、その最小をalphaとした。
beta[t,s,e]=1/deg[e]は要素容量を正確に1以下にし、95,225の群・選択肢不等式を全て満たす。
--verifyは保存certificateとの一致だけでなく、元グラフと終局追加から全degree・全重み和・全alphaを再構成する。
最適値は和集合濃度なのでceilにより6,577。現行の上界31,636との差は未解決。
旧2024529/308・6,574は旧cacheインスタンスに限る履歴値。現在の上下界と混同しない。

## 夜間バッチ反映（2026-10-14・K0424）

層別13の現行インスタンスでは厳密総和182532671/27720、整数下界6,585が確定する。
91145221/13860・6,577はK0423時点の履歴値。詳細はK0424と
`research/experiments/n11-night-plan-update6-20261014/output/updated-element-dual-update6.json` を参照。

## 旧cacheインスタンスの履歴

K0417の分数下界は厳密値2024529/308の双対実行可能点であり、整数下界6,574が確定する。element-only重み族は族内最適のため、この系統の強化は族の拡張なしにはできない。独立な整数証明書（pool packing）は346で及ばない。
