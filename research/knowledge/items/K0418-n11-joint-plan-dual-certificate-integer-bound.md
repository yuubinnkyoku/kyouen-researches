---
id: K0418
title: 共同証明計画のelement-only双対は厳密値2024529/308で整数下界6,574を確定する
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0417
  note: 19 root共同の選択問題と分数下界6,573.146・上界31,546
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
scope: K0417の869有料群・選択肢別未知S5費用の最小和集合問題に対するelement-only分数双対。solver探索なし。
evidence: 依存グラフからdegを再集計し、各群のalphaを厳密有理数で評価して総和2024529/308＝6573.1461…を得た。--verifyがdeg一致・alpha一致・総和一致を確認し、K0417公表値6573.146と整合した。最適値が和集合濃度ゆえ整数のためOPT≥6574を採用する。重み族内ではw＝1/degが単調性より最適で、重み調整の改善余地はない。pool-disjoint packingは有効だが346に留まる。上下差（6,574対31,546）は未解決。
---

K0417の分数下界は厳密値2024529/308の双対実行可能点であり、整数下界6,574が確定する。element-only重み族は族内最適のため、この系統の強化は族の拡張なしにはできない。独立な整数証明書（pool packing）は346で及ばない。
