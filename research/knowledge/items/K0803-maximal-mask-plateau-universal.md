---
id: K0803
title: "maximal mask 3,300 プラトーの全称化 — 窓マスク掃引の unique=3,630・maximal=3,300 が全幅 w∈[99,198) でちょうど成り立つ（周期性+順序同型+popcountギャップの全称証明・level 17 掃引ワークロードは w=66..197 で一定）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "level 17 標準形掃引 harness（mod 9×11・(a,u) 全列挙窓マスク・L=17）の mask 構造: 任意の幅 w（99 ≤ w < 198）で unique=3,630・maximal=3,300（全称・等号付き）。帰結: level 17 掃引の mask ワークロード数は w=66..197 の全範囲で一定 3,300（66..98 は有限測定・99..197 は本定理）。w ≥ 198 帯は小パターン参入で別問題（w=296 で |P|=6 パターンのフィルタ参入を実証・未解決）"
evidence: "数学的証明（有限計算からの全称昇格）。骨子: (1) 窓条件 cond(i)=m9[x][i mod 9]∧m11[y][i mod 11] は 99 周期（99≡0 mod 9・mod 11・全 (x,y)・i<99 機械確認）、(2) w≥99 で T(w)∩[0,99)=P によりパターン→T(w) は単射かつ T1(w)⊆T2(w)⟺P1⊆P2 の順序同型、(3) CRT により |P|=c9·c11（全 81×121 対で不一致 0）、(4) c9∈{0,3,5,6}・c11∈{1,6,7} の完全列挙→|P|∈{0,3,5,6,18,21,30,35,36,42} で相違パターン 3,994 個のヒストグラムは [7,17] に空き、(5) 99≤w<198 では |T(w)|=|P|+|P∩[0,w−99)|≤2|P| なので |T|≥17 フィルタは「|P|≥18」と w=99 で完全同値→poset 同型により全 w∈[99,198) で w=99 の値 3,630/3,300 と一致。制御: sampled w=99/133/140/150/160/170/180/190/197 の直接 exhaustive 計算が全て 3,630/3,300（w=99 は saturation 実験の公表値と完全一致）。否定的制御: w=296 で |P|=6 パターンが |T|=18≥17 に届き新規参入（フィルタ同値の破壊を実証）→ 全 w への安易な拡大を排除し定理の量化範囲を正当に限定"
solution:
  board: level 17 標準形掃引 harness（mod 9×11・(a,u) 全列挙窓マスク）
  level: strong
  outcome: unconditional
  classification: [all-safe-grundy]
  coverage: 全幅 99 ≤ w < 198（掃引 mask 構造に関する全称）
  conditions: L=17・mod 9×11 窓マスク生成・連続整数行
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: 周期性補題 + パターン順序同型 + CRT popcount 積 + popcount ギャップ [7,17] 空き + フィルタ同値（w=99 exhaustive 計算 3,630/3,300 が基底）
  independent_check: 3 機械検査（periodicity99・CRT 不一致 0・gap7to17Empty）PASS・sampled 9 幅の直接 exhaustive が理論値と完全一致・w=296 境界プローブ（フィルタ破壊の実証）
  note: "maximal-mask-saturation-20261113 の有限観測（w=62..132・maximal 3,300 プラトー）の予想部分『w<198 まで維持』を全称定理に昇格。w≥198 帯の maximal 3,300 維持は未解決（小パターンが c9=6×c11∈{6,7} の点順序上位パターンの真部分集合なら非maximal のまま維持されるが未検証）。L≠17 は未検証"
relations:
- type: depends_on
  target: K0799
  note: w=66 完走（unique=maximal 3,300）・harness の窓マスク生成の直接の源泉
- type: depends_on
  target: K0801
  note: w=67 完走（3,300）・saturation 実験の制御値の供給源
- type: supports
  target: K0794
  note: level 17 掃引キャンペーンの mask ワークロードが w=66..197 で一定 3,300 であることの理論的裏付け（コスト増は per-mask 加重のみ）
artifacts:
- path: research/experiments/maximal-mask-plateau-universal-20261113/scripts/maximal_mask_plateau_universal.ts
  role: verifier
  note: 周期性・CRT・popcount ギャップの機械検査 + sampled 幅の exhaustive 再現 + w=296 境界プローブ
- path: research/experiments/maximal-mask-plateau-universal-20261113/output/plateau_universal_output.json
  role: data
  note: 検査結果とサンプル幅の機械出力（全 3,630/3,300・境界プローブ true）
- path: research/experiments/maximal-mask-plateau-universal-20261113/report.md
  role: report
  note: 定理・証明・制御・限定の本文
- path: research/log/2026-11-13-maximal-mask-plateau-universal.md
  role: log
  note: 判断・経緯・レジューム
---

## 命題（証明済み・全称）

1. **任意の幅 w（99 ≤ w < 198）に対し、level 17 窓マスク掃引の
   unique = 3,630・maximal = 3,300 がちょうど成り立つ**
   （L=17・mod 9×11・(a,u) 全列挙・標準形掃引 harness と同一の生成）。
2. **帰結**: level 17 掃引キャンペーンの mask ワークロード数は
   **w = 66..197 の全範囲で一定 3,300**
   （66..98 は saturation 実験の有限測定・99..197 は本定理）。
   コスト増（~×1.35/w）は per-mask ノード加重のみ。
   11×11 レーン（w ≤ 121）でも harness ワークロードは全域で一定。

## 証明の骨子

- 窓条件は 99 周期 → w ≥ 99 で mask はパターン P ⊆ [0,99) と 1 対 1
  （T(w)∩[0,99) = P）で、包含関係も含めて順序同型。
- CRT により |P| = c9·c11・完全列挙で c9∈{0,3,5,6}・c11∈{1,6,7} →
  |P| は [7,17] に空き（相違パターン 3,994 個のヒストグラムで機械確認）。
- 99 ≤ w < 198 では |T(w)| ≤ 2|P| なので |T|≥17 フィルタは
  「|P|≥18」と同値で w=99 と一致 → poset 同型により全幅で 3,630/3,300。

## 制御と限定

- sampled 9 幅（99・133・140・150・160・170・180・190・197）の直接 exhaustive
  計算が全て 3,630/3,300 で理論値と完全一致。w=99 は既往公表値と一致。
- **w ≥ 198 帯では成立しない**: w=296 で |P|=6 の小パターンが
  |T| = 18 ≥ 17 に届きフィルタに新規参入する（機械実証）。
  この帯の maximal 3,300 維持は未解決の別問題。
- L = 17 に限る。popcount ギャップとフィルタ域の位置関係は L 依存
  （L ≤ 12 なら |P|≤6 でも参入し得る）で未検証。
