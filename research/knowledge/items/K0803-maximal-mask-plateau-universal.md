---
id: K0803
title: "maximal mask 3,300 プラトーの全称化 — 窓マスク掃引の maximal=3,300 が全幅 w≧99で成立（周期性+順序同型+popcountギャップ+支配補題の全称証明・unique=3,630は99≦w<198に限定・level 17 掃引ワークロードはw=66以降不変）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "level 17 標準形掃引 harness（mod 9×11・(a,u) 全列挙窓マスク・L=17）の mask 構造: (1) 任意の幅 w≧99で maximal=3,300（全称・等号付き・上限なし）・(2) unique=3,630 はちょうど 99≦w<198（w≧198 では小パターン参入で増加: w=296→3,663・w=396→3,960）。帰結: level 17 掃引の mask ワークロード数は w=66 以降常に 3,300（66..98 は有限測定・99 以上は本定理）"
evidence: "数学的証明（有限計算からの全称昇格）。骨子: (1) 窓条件 cond(i)=m9[x][i mod 9]∧m11[y][i mod 11] は 99 周期（全 (x,y)・i<99 機械確認）、(2) w≧99 で T(w)∩[0,99)=P によりパターン→T(w) は単射かつ T1(w)⊆T2(w)⟺P1⊆P2 の順序同型（w によらない）、(3) CRT により |P|=c9·c11（全 81×121 対で不一致 0）、(4) c9∈{0,3,5,6}・c11∈{1,6,7} の完全列挙→|P|∈{0,3,5,6,18,21,30,35,36,42} で相違パターン 3,994 個のヒストグラムは [7,17] に空き、(5) |P|≧18 は全 w≧99 でフィルタ通過、(6) 支配補題: 非空小パターン（|P|≦6）はすべて点順序上位の big パターン（|P|≧18）に支配される（完全判定・例外 0）→ 小パターンは w 依存で参入しても常に非 maximal、(7) ゆえに maximal は全 w≧99 で w=99 の値 3,300 と一致。unique=3,630 は 99≦w<198 では |T|≦2|P|≦12<17 で小パターン不参入により成立。制御: sampled 9 幅（99..197）の直接 exhaustive が全て 3,630/3,300・広幅プローブ w=296→3,663/3,300・w=396→3,960/3,300・**w=396 の unique 3,960=3,994−1（空）−33（|P|=3・4周期で不通過）と理論値完全一致**"
solution:
  board: level 17 標準形掃引 harness（mod 9×11・(a,u) 全列挙窓マスク）
  level: strong
  outcome: unconditional
  classification: [all-safe-grundy]
  coverage: 全幅 w≧99（掃引 mask 構造に関する全称・上限なし）
  conditions: L=17・mod 9×11 窓マスク生成・連続整数行
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: 周期性補題 + パターン順序同型 + CRT popcount 積 + popcount ギャップ [7,17] 空き + big パターン全通過 + 小パターン支配補題（w=99 exhaustive 計算 3,630/3,300 が基底）
  independent_check: 4 機械検査（periodicity99・CRT 不一致 0・gap7to17Empty・dominationCheck 例外 0）PASS・sampled 9 幅の直接 exhaustive が理論値と完全一致・広幅プローブ w=296/396（unique 増加と maximal 不変の両面を実証・w=396 は unique の理論会計と完全一致）
  note: "maximal-mask-saturation-20261113 の有限観測（w=62..132・maximal 3,300 プラトー）の予想『w<198 まで維持』を支配補題で全 w≧99 に拡張して全称定理に昇格。L≠17 は未検証（L≦12 では小パターンが早期参入し要再検証）。w≧198 帯の unique の増加様式は |T(w)|=k|P|+|P∩[0,rem)|≧17 の会計で完全に決定可能（閉形式）"
relations:
- type: depends_on
  target: K0799
  note: w=66 完走（unique=maximal 3,300）・harness の窓マスク生成の直接の源泉
- type: depends_on
  target: K0801
  note: w=67 完走（3,300）・saturation 実験の制御値の供給源
- type: supports
  target: K0794
  note: level 17 掃引キャンペーンの mask ワークロードが w=66 以降常に 3,300 であることの理論的裏付け（コスト増は per-mask 加重のみ・前処理は w=99 の 1 回で定数化可能）
artifacts:
- path: research/experiments/maximal-mask-plateau-universal-20261113/scripts/maximal_mask_plateau_universal.ts
  role: verifier
  note: 周期性・CRT・popcount ギャップ・支配補題の機械検査 + sampled/広幅の exhaustive 再現 + 境界プローブ
- path: research/experiments/maximal-mask-plateau-universal-20261113/output/plateau_universal_output.json
  role: data
  note: 検査結果・サンプル幅・広幅プローブの機械出力（maximal 全幅 3,300・w=396 unique 会計一致）
- path: research/experiments/maximal-mask-plateau-universal-20261113/report.md
  role: report
  note: 定理・証明・制御・限定の本文（全 w≧99 拡張版）
- path: research/log/2026-11-13-maximal-mask-plateau-universal.md
  role: log
  note: 判断・経緯・レジューム
---

## 命題（証明済み・全称）

1. **任意の幅 w ≥ 99 に対し、level 17 窓マスク掃引の maximal = 3,300 が
   ちょうど成り立つ**（上限なし・全称・等号付き）。
2. **unique = 3,630 が成り立つのはちょうど 99 ≤ w < 198**。
   w ≥ 198 では小パターン（|P| ∈ {5,6}・十分な周期数で |P|=3 も）が
   フィルタに参入し unique は増加する（w=296: 3,663・w=396: 3,960）が、
   maximal は 3,300 のまま。
3. **帰結**: level 17 掃引キャンペーンの mask ワークロード数（maximal）は
   **w = 66 以降常に 3,300**（66..98 は有限測定・99 以上は本定理）。
   コスト増（~×1.35/w）は per-mask ノード加重のみ。
   掃引機の maximalMasks 前処理は理論上 w=99 の 1 回で定数化できる。

## 証明の骨子

- 窓条件は 99 周期 → w ≥ 99 で mask はパターン P ⊆ [0,99) と 1 対 1
  （T(w)∩[0,99) = P）で、包含関係も含めて w によらない順序同型。
- CRT により |P| = c9·c11・完全列挙で c9∈{0,3,5,6}・c11∈{1,6,7} →
  |P| ∈ {0,3,5,6,18,21,30,35,36,42} で [7,17] に空き。
- |P| ≥ 18（big）は全 w ≥ 99 でフィルタ通過。**非空の小パターン（|P| ≤ 6）は
  すべて点順序上位の big パターンに支配される（完全判定・例外 0）** →
  参入しても常に非 maximal → maximal は全 w ≥ 99 で w=99 の値 3,300。
- 99 ≤ w < 198 では |T| ≤ 2|P| ≤ 12 < 17 で小パターンが不参入 →
  unique も 3,630。

## 制御と限定

- sampled 9 幅（99・133・140・150・160・170・180・190・197）の直接 exhaustive
  計算が全て 3,630/3,300。広幅プローブ w=296 → 3,663/3,300・
  w=396 → 3,960/3,300。
- **w=396 の unique 3,960 = 3,994（相違パターン総数）− 1（空パターン）−
  33（|P|=3・4 周期で |T| = 12 < 17 不通過）** と理論会計が完全一致
  （拡張理論の強い相互検証）。
- L = 17 に限る。L ≤ 12 では小パターンが w=66 以前から参入し、
  フィルタ同値と支配補題の効果は要再検証（未検証）。
- w ≥ 198 帯の unique は |T(w)| = k·|P| + |P∩[0, rem)| ≥ 17 の会計で
  決定可能（閉形式）。
