---
id: K0796
title: 2×m・q=4の真の満容量安定化長はM_{2,4}=9 — K0069の十分長さ9が最小であることが確定
kind: proposition
status: proved
topics: [rectangles, variants, grundy]
aliases: []
scope: "標準二行整数長方形盤（2×m・q点共円・共線禁止・通常プレイ）の真の満容量安定化長 M_{2,4}=9（全称・等号付き）。全m≥9で全極大安全集合は6石・g(S)=(6−|S|) mod2（K0069と同一）。m=8には5石の極大安全集合が存在し9の最小性が確定。K0068の十分長さT_2=9と一致"
evidence: "下界: 2×8 witness（行0={0,2}・行1={1,2,5}）の安全性（pairsum {2}∩{3,6,7}=∅・各行≤3）と極大性（行0への全追加x∈{1,3,4,5,6,7}が必ずpairsum衝突・行1満杯）の明示検証。上界: K0069の一般定理（m≥9全極大6石）。幾何モデル（K0069 B214圧縮と同一: 4共線は水平行内のみ・4共円は弦和一致x₁+x₂=x₃+x₄）によるm=1..12の全極大分類でm≥9は不足極大0。独立制御: m=1..5を外心整数演算の直接幾何実装（全4組共線・共円判定）で再列挙し極大総数1/4/12/24/78がモデルと完全一致"
solution:
  board: 2×m・q=4（標準整数格子・全m≥1）
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: m≥9の全安全局面（安定化）
  conditions: q=4, w=2
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: m=8 witness下界 + K0069全称上界 + モデル列挙（m≤12）+ 独立幾何制御（m≤5）
  independent_check: 外心直接幾何実装との極大数完全一致（1/4/12/24/78）
  note: "K0069/K0068は十分長さ9のみ主張（最小性は明示せず）。本項目が最小性を閉じた。確定閾値は8件目"
relations:
- type: depends_on
  target: K0069
  note: 上界（m≥9全極大6石）と幾何モデル（B214圧縮・弦和同値）の出典
- type: supports
  target: K0068
  note: 十分長さT_2=9が最小であることを確定（真の安定化長と一致）
- type: supports
  target: K0795
  note: results表の(2,4)行をbounds（≤9・最小性未検証）からexact-threshold（9・proved）へ昇格
- type: depends_on
  target: K0302
  note: 確定閾値リスト（5件）に続き2行盤の確定値を追加
artifacts:
- path: research/experiments/two-row-m24-stabilization-20261113/scripts/two_row_m24.ts
  role: verifier
  note: pair-sumモデルによるm=1..12全極大分類の単独再現
- path: research/experiments/two-row-m24-stabilization-20261113/output/two_row_m24.json
  role: data
  note: 全数値・witness・独立制御の機械出力
- path: research/experiments/two-row-m24-stabilization-20261113/reports/two-row-m24.md
  role: proof
  note: 主張・証明・分類表・制御・限界
---

# K0796: 2×m・q=4の真の満容量安定化長 M_{2,4}=9

## 命題（証明済み・全称・等号付き）

**M_{2,4} = 9**。全 m ≥ 9 で全極大安全集合はちょうど6石（各行3石）で
g(S) = (6 − |S|) mod 2。m = 8 には5石の極大安全集合が存在する。

- 上界: K0069（m ≥ 9 全極大6石・全局面偶奇式）。
- 下界: 2×8 witness 行0 = {0, 2}・行1 = {1, 2, 5}。
  安全: pairsum(行0) = {2} と pairsum(行1) = {3, 6, 7} は交わらない・各行 ≤ 3。
  極大: 行1は満杯。行0への追加 x ∈ {1,3,4,5,6,7} はいずれも
  新ペア和が {3,6,7} と衝突（1→3・3→3・4→6・5→7・6→6・7→7）。

## 幾何モデルと機械検証

K0069 の B214 圧縮と同一: 4点共線は水平行内のみ（非水平直線は2行に2点）、
4点共円（各行2点）は弦中心条件 x₁+x₂ = x₃+x₄。安全 ⟺ 各行 ≤ 3 石かつ
pairsum(行0) ∩ pairsum(行1) = ∅。

m = 1..12 の全極大分類: 不足極大は m ≤ 8 のみ（m=8 で16個・最大5石）で
m ≥ 9 は0（m=9..12・2,846/6,564/13,650/26,086 は全て満容量）。

**独立幾何制御**: m = 1..5 を pair-sum モデル不使用の直接実装
（全セル4組の共線・共円を外心の整数演算で判定）で再列挙し、
極大総数 1 / 4 / 12 / 24 / 78 が完全一致（m=5 は 78 = 6満 + 72不足）。

## 帰結

- K0068 の十分長さ T_2 = 9 は最小（真の安定化長と一致）。
- K0795 の results 表で (2,4) は exact-threshold に昇格（確定閾値8件目）。

## 限界

- 2行・q=4 限定。m ≥ 9 の不在証明は K0069 に依存（本項目の列挙は再現資料）。
- モデル列挙は m ≤ 12。
