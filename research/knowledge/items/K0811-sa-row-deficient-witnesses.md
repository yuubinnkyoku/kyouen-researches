---
id: K0811
title: SA探索による行欠損極大witness — M_{6,5}≥29・M_{6,6}≥22・M_{5,6}≥19（K0810の下界を更新・第2弾/第3弾で延長）
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
- path: research/experiments/sa-frontier-extension-20261114/output/results.jsonl
  role: data
  note: 第2弾29実行・6×26/6×27/6×21 witness座標・独立検証・抵抗run（SAパラメータ多様化込み）
- path: research/experiments/sa-frontier-extension-20261114/report.md
  role: proof
  note: 第2弾（同一機械・シード/予算/パラメータ多様化のみ）の下界更新と抵抗の記録
- path: research/experiments/sa-frontier3-20261114/output/results.jsonl
  role: data
  note: 第3弾23実行・6×28の22石（2石欠損）witness座標・独立検証・reverify別プロセス再検証・新前線の抵抗run
- path: research/experiments/sa-frontier3-20261114/report.md
  role: proof
  note: 第3弾（同一機械・ドライバのみ追加）の下界更新・パラメータ帯による発見難度差・SAT単発予算の非決着の記録
solution:
  board: 6×m・5×m（q=5,6,8・q=6）
  level: weak
  outcome: conditional
  classification: [root]
  coverage: (6,5) m=22..28・(6,6) m=17..21・(5,6) m=16..18・(6,8) m=12..15 の各盤
  conditions: q点共円・共線禁止・標準整数格子
  verification: [independent-enumeration]
  certificate: witness座標（全witnessがcensus不使用独立検証で safe+maximal PASS）
  independent_check: 別アルゴリズム（石ペア直線・石3点組円の全列挙・整数演算のみ）による安全性・極大性の直接判定
  note: 下界更新のみ。抵抗した m（(6,5) m=29,30・(6,6) m=22・(5,6) m=19・(6,8) m=16・(5,7) m=19,20）は未解決であり不在証明ではない
---

# SA探索による行欠損極大witness — 3組の下界更新（2026-11-14）

K0808 の汎用 (w,m,q) 欠損極大配置探索機の census・census 不使用独立検証器を
機械移植し、探索部をシミュレーテッド・アニーリング
（状態は常に極大・石の部分除去→再極大化を Metropolis 受理・幾何冷却・停滞時ベスト再シード）
に置換した機械で、K0810（SAT）の直後の未解決 m 帯を含む witness を発見した。
すべての witness は census 不使用の独立検証器で safe・maximal ともに PASS している。

- **M_{6,5} ≥ 29**: 22石@6×28（満容量24・2石欠損・行構成 4,4,4,4,2,4）が第3弾
 （sa-frontier3-20261114）で最新。23石@6×22..6×27（1石欠損・6盤連続）に続き、
  (6,5) 初の2石欠損witness。第2弾で 6×26（2座標）・6×27 を追加（6×27 は5シード抵抗後に発見）。
  6×28 は第2弾（T0≥2.0 系・10 run）で抵抗した m だが、第3弾の T0=1.5/mrf=0.45/sK=36
  構成が74秒で突破 — 非発見は不在を意味しない最も直接的な再実証。
- **M_{6,6} ≥ 22**: 29石@6×17..6×21（満容量30・5盤連続）。
  K0810 が未解決として残した m=18, m=20 は実在し、第2弾で m=21 も実在が確定。
- **M_{5,6} ≥ 19**: 24石@5×16・5×17・5×18（満容量25）。K0810 が未解決として残した m=18 は実在。
- (6,8) m=12..15 の41石witness は K0810 SAT の m=12..17 を補強する（下界18は不変）。

現在の境界: M_{6,5} ∈ [29,658]・M_{6,6} ∈ [22,495]・M_{6,8} ∈ [18,371]・
M_{5,6} ∈ [19,249]・M_{5,7} ∈ [19,158]・M_{6,7} ∈ [20,402]。

制御: 2×8 q=4→5石（K0796 再発見）・6×19 q=5→23石（K0808 一致）・
5×19 q=7→30石=満容量（K0759 完全列挙と一致）・6×15 q=6→29石（K0808 一致）。
第3弾は 2×8 q=4 制御に加え 6×28 census（240直線+4,274円）が SA 機と SAT 機
（独立実装2系統）で一致したことを追加検証している。

貪欲（K0808/K0809）・SAT（K0810）・SA のいずれでも非発見 m と実際の不在は
系統的にズレており、探索系の非発見から M の確定値を予想することはできない。
抵抗の記録（非発見・不在証明ではない・累計）: (6,5) m=29（8 run・SAパラメータ多様化込み）・
m=30（2 run）・(6,6) m=22（7 run）・(5,6) m=19（5 run）・(6,8) m=16（5 run）・
(5,7) m=19,20（各2 run・第3弾）。
第1弾で抵抗した (6,5) m=26,27・(6,6) m=21 は第2弾で、(6,5) m=28 は第3弾で
全て witness が発見された。SA の抵抗記録にはパラメータ構成の併記が必須
（同一 m でも T0≥2.0 系10 run 非発見→T0=1.5/mrf=0.45/sK=36 が74秒で発見）。

副産物: K0332 の五行 q=7 上界158手法の六行移植分析で、
mod9 補題の6行拡張（81組中0・五行制御も0）は成立する一方、
blocker 円の 2+2+1+1 型・2+1+1+1 型が mod9 で除去できず、
弦対会計 C(5,2)×29=290 と Melchior y≤36b のみの上界は最大 585 となり
K0318 の一般上界 402 を下回らないことが確定した（実験 report.md・Log 参照）。
