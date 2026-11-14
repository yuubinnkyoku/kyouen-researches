---
id: K0811
title: SA探索による行欠損極大witness — M_{6,5}≥28・M_{6,6}≥21・M_{5,6}≥19（K0810の下界3件を更新）
kind: proposition
status: proved
topics: [rectangles, variants]
aliases: []
relations:
- type: generalizes
  target: K0810
  note: SATで解けた m 帯の先の witness を SA で発見し (6,5)/(6,6)/(5,6) 下界を更新
- type: depends_on
  target: K0808
  note: census・census不使用独立検証器の verbatim 移植
- type: depends_on
  target: K0806
  note: 上界（K0318代入）は不変
artifacts:
- path: research/experiments/sa-row-deficient-witnesses-20261114/scripts/sa_machine.js
  role: source
  note: K0808 census・独立検証器の機械移植＋SA探索部（Metropolis・冷却・再シード）
- path: research/experiments/sa-row-deficient-witnesses-20261114/output/sa_results.jsonl
  role: data
  note: 全26実行・witness座標・独立検証詳細・抵抗（非発見）の記録
- path: research/experiments/sa-row-deficient-witnesses-20261114/report.md
  role: proof
  note: 手法・制御・計算コスト対比・6行blocker構造分析
- path: research/experiments/sa-frontier2-20261114/scripts/run2.js
  role: source
  note: パラメータ多様化ドライバ（同一機を T0/maxRemoveFrac/sampleK 巡回で使用・1ケースごとJSONL永続化）
- path: research/experiments/sa-frontier2-20261114/output/sa_frontier2.jsonl
  role: data
  note: 全33実行・6×26/6×27 の新witness・最前線5件の抵抗記録
- path: research/experiments/sa-frontier2-20261114/report.md
  role: proof
  note: M_{6,5}≥28 の根拠・抵抗 m の一覧
solution:
  board: 6×m・5×m（q=5,6,8・q=6）
  level: weak
  outcome: conditional
  classification: [root]
  coverage: (6,5) m=22..27・(6,6) m=17..20・(5,6) m=16..18・(6,8) m=12..15 の各盤
  conditions: q点共円・共線禁止・標準整数格子
  verification: [independent-enumeration]
  certificate: witness座標（全witnessがcensus不使用独立検証で safe+maximal PASS）
  independent_check: 別アルゴリズム（石ペア直線・石3点組円の全列挙・整数演算のみ）による安全性・極大性の直接判定
  note: 下界更新のみ。抵抗した m（(6,5) m=28・(6,6) m=21・(5,6) m=19・(6,8) m=16・(5,7) m=20）は未解決であり不在証明ではない
---

# SA探索による行欠損極大witness — 下界更新と第2弾の前線拡大（2026-11-14）

K0808 の汎用 (w,m,q) 欠損極大配置探索機の census・census 不使用独立検証器を
機械移植し、探索部をシミュレーテッド・アニーリング
（状態は常に極大・石の部分除去→再極大化を Metropolis 受理・幾何冷却・停滞時ベスト再シード）
に置換した機械で、K0810（SAT）の直後の未解決 m 帯を含む witness を発見した。
すべての witness は census 不使用の独立検証器で safe・maximal ともに PASS している。

- **M_{6,5} ≥ 28**: 23石@6×22・6×23・6×24・6×25・**6×26・6×27**（満容量24・6盤連続）。
  6×26（4.4秒）・6×27（47秒）は第2弾（sa-frontier2-20261114・パラメータ多様化）
  で発見。6×27 は T0=3.4・maxRemoveFrac=0.45・sampleK=12 構成。
- **M_{6,6} ≥ 21**: 29石@6×17・6×18・6×19・6×20（満容量30・4盤連続）。
  K0810 が未解決として残した m=18, m=20 は実在。
- **M_{5,6} ≥ 19**: 24石@5×16・5×17・5×18（満容量25）。K0810 が未解決として残した m=18 は実在。
- (6,8) m=12..15 の41石witness は K0810 SAT の m=12..17 を補強する（下界18は不変）。

現在の境界: M_{6,5} ∈ [28,658]・M_{6,6} ∈ [21,495]・M_{6,8} ∈ [18,371]・
M_{5,6} ∈ [19,249]・M_{5,7} ∈ [19,158]・M_{6,7} ∈ [20,402]。

制御: 2×8 q=4→5石（K0796 再発見）・6×19 q=5→23石（K0808 一致）・
5×19 q=7→30石=満容量（K0759 完全列挙と一致）・6×15 q=6→29石（K0808 一致）。
第2弾でも機材再構築後に 2×8 q=4 制御を再確認。

貪欲（K0808/K0809）・SAT（K0810）・SA のいずれでも非発見 m と実際の不在は
系統的にズレており、探索系の非発見から M の確定値を予想することはできない。
(6,5) では m=26 が SA で4秒で発見された直後に m=27 も発見された一方、
m=28 は6実行（計~5.5分）で抵抗 — コストの m 非単調性が SA でも同一に観測される。
抵抗の記録（非発見・不在証明ではない）: (6,5) m=28（6実行×50-60秒）・
(6,6) m=21（第1弾3シード×90秒＋第2弾10実行×40-50秒）・
(5,6) m=19（120秒×2＋6実行×45秒）・(6,8) m=16（90〜120秒×3＋4実行×70秒）・
(5,7) m=20（90秒＋7実行×40秒）。

副産物: K0332 の五行 q=7 上界158手法の六行移植分析で、
mod9 補題の6行拡張（81組中0・五行制御も0）は成立する一方、
blocker 円の 2+2+1+1 型・2+1+1+1 型が mod9 で除去できず、
弦対会計 C(5,2)×29=290 と Melchior y≤36b のみの上界は最大 585 となり
K0318 の一般上界 402 を下回らないことが確定した（実験 report.md・Log 参照）。
