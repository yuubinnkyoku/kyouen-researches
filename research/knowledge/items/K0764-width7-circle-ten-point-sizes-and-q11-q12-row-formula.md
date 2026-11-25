---
id: K0764
title: "幅7整数格子の円は全mでP(7)=10・可能サイズ{7,8,10} — 9・11・12点円の全称不在とq=11..12の行分離公式"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "7つの連続整数行（7×m・全m≥1）上の円の格子点数は高々10で、可能な点数は7,8,10のみ（9・11・12は全mで不存在）。10点円は5二重行+2空行のプロファイルのみ。系として幅7・q≥11で g(S)=(7·min(m,q−1)−|S|) mod2・M_{7,q}=q−1"
evidence: "数学的証明（mod9剰余分類 d≤5 + K0763接点補題のw=7拡張・(5,6) mod3排除・(1,4)一意分解）。witness (2x−7)²+(2y−7)²=50 は10点を持ち等号成立"
solution:
  board: 幅7固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: 幅7・q≥11は全m≥1・全安全局面
  conditions: 連続整数行・q≥11（円の構造定理はqに依らず全称）
  verification: [mathematical-proof]
  certificate: mod9剰余分類 + mod3排除((1,3),(2,3),(3,4),(3,5),(5,6)) + (a−u)(a+u)=3一意分解
  independent_check: witness円の直接列挙・census(7×13/16/19)・Pell個数の厳密一致
  note: "q=11..14が新規確定（w=7ではK0025のq>2wはq≥15から）"
relations:
- type: depends_on
  target: K0072
  note: 二重行数上界のmod9枠組み（7連続行版を本項目で独立計算）
- type: depends_on
  target: K0763
  note: 接点補題（f|t・符号論・(1,4)一意分解）のw=7拡張。P(6)=8との対比でw依存性を分離
- type: depends_on
  target: K0001
  note: 行分離帰結の行公式はK0072と同一の行ゲーム導出
- type: supports
  target: K0332
  note: 幅7の安定化長はq≥11で確定。M_{7,q}(q≤10)はopen
- type: generalizes
  target: K0025
  note: q>2w（w=7ではq≥15）をq=11..14まで拡張
artifacts:
- path: research/experiments/width7-circle-ten-point-20261112/reports/width7-circle-ten-point.md
  role: proof
  note: 定理・系・証明・witness・w=6との対比の記録
- path: research/experiments/width7-circle-ten-point-20261112/scripts/width7_circle_bound.ts
  role: verifier
  note: witness列挙・接点補題制御・2接点プロファイル・mod9分類・censusの機械検証
- path: research/experiments/width7-circle-ten-point-20261112/output/width7_circle_bound.json
  role: data
  note: 全制御の実行結果
- path: research/log/2026-11-12-width6-circle-eight-point-proof.md
  role: log
  note: 本セッションの判断・教訓・レジューム（幅6と共用）
---

## 命題（証明済み・全称）

1. **P(7) = 10**: 7つの連続整数行からなる任意の整数格子（7×m、全 m ≥ 1）上で、
   円の格子点数は高々 10。可能な点数は 7, 8, 10 のみで、
   **9点・11点・12点円は全 m で存在しない**。
2. **10点円のプロファイル**: 10 = 2d + s の実現は (d,s) = (5,0) のみ
   （(4,2) は排除）。幅7の10点円はすべて **5二重行 + 2空行・接点なし**。
   witness: (2x−7)²+(2y−7)²=50、行占有 {0,1,3,4,6} が各2点・m ≥ 8 で実在。
3. **系（q ≥ 11）**: 円 ≤ 10 < q、非水平直線 ≤ 7 < q により行を跨ぐ禁止 q 点集合なし。
   全 m ≥ 1・全安全局面 S で

   g(S) = (7·min(m, q−1) − |S|) mod 2,　M_{7,q} = q−1（q = 11..14 が新規。q ≥ 15 は K0025 と重複整合）。

## 証明の骨子（K0763 機械の w=7 拡張）

- d ≤ 5: mod9 剰余分類（9³ 通り、7連続行 worst 5）。
- 接点補題: 接点 → C 偶 → disc(y)/4 = t(y₀+y+D) = s²、f | t。5二重行 → f ∈ {1,2}。
  - f=2: 同符号で {2,4,6} の3つのみ。
  - f=1: t ∈ {1..6}。非両立ペア (1,3),(2,3),(3,4),(3,5)〔mod 3〕・
    (1,4)〔g=5 強制〕・**(5,6)**〔5v²−6z²=1 → v² ≡ 2 (mod 3)〕。
    t=6 は (3,6) として Pell w²−2z²=1 で両立し得るが（g=30,870,29406,…）、
    11点に必要な5-集合・9点に必要な4-集合はすべて上記ペアを含む。
- 12点: d=6 は mod9 で不可。2接点（t=0,g、|g|≤6）間の二重行は g=±5 で {1,4}・
  g=±6 で {3} のみで 5 に届かない。

## 機械検証

witness 10点直接列挙、|g| ≤ 10⁶ の接点条件で最大3（t=3 の共存 8 件 = Pell 4 解+鏡映の厳密一致、
t=5∧t=6 共存 0 件）、f=2 最大 2、2接点プロファイル {1,4}/{3}、mod9 worst 5、
census 7×13/16/19 = 201/321/457 本でサイズ集合 {7,8,10}・9/11/12 は 0。

## 幅6との対比・限界

- P(6)=8（K0763）に対し P(7)=10。**9点円は w=6,7 ともに全 m で不在**。
  10点円は w=7 から「5二重行・接点なし」形で登場。同一 witness 円は8行版で12点を持ち
  **P(8) ≥ 12**。w = 8..14 の P(w) 正確値は open（K0072 の w ≥ 15 上界と接続する中間帯）。
- 幅7では非水平7点直線（傾き ±1 など）が初めて危険曲線になる（w ≤ 6 では非水平直線 ≤ w ≤ 6 点）。
  幅7・q ≤ 10 の occupancy プログラムは本項目では解いていない。
