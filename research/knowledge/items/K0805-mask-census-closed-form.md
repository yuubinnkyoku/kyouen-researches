---
id: K0805
title: "マスクセンサスの全幅閉形式決定 — level 17 窓マスク掃引の (unique(w), maximal(w)) が交叉統計と区間支配判定で全 w≧17 に決定（unique 3630 到達は w=96 が鋭い・初出現 w=37・maximal=3300 は全 w≧66 で厳密・小パターン参入窓 265..286/309..363/529..561）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "level 17 標準形掃引 harness（mod 9×11・(a,u) 全列挙窓マスク・L=17）のセンサス関数: (1) unique(w) = #{P≠∅: k|P|+|P∩[0,rem)|≧17}（k=⌊w/99⌋）の交叉統計で全 w≧17 を閉形式決定・big は w*=s17(P)+1∈[37,96]・(2) maximal(w)=3300 がちょうど全整数 w≧66 で成立（66..98 は区間支配判定で幅ごとに厳密計算・≧99 は反鎖+K0803 支配補題）・(3) w=37..65 では maximal=unique・w≧73 の unique 増分は既存パターンの真部分集合"
evidence: "数学的証明（単射補題 + 閉形式通過条件 + 包含判定 + 13,173,270 ordered pair の区間支配完全走査）。骨子: (1) 相違パターン 3,994 個（K0803 と同一の生成・ヒストグラム一致）、(2) w<99 では mask=prefix で passing big 上単射（w=17..98 全幅で衝突 0 を機械確認）・w≧99 では第1周期から P が復元可能（単射）、(3) |T_P(w)|=k|P|+|P∩[0,rem)| により各パターンの最小通過幅 w*(P) が決定 → unique(w) は w* の交叉統計（changePoints 表が全幅の増分を与える）、(4) w<99 の包含 ⟺ min(P\\P')≧w（P\\P'=∅ を含む）により maximal(w) が ordered pair ごとの区間支配で決定、(5) w≧99 の包含 ⟺ P⊆P' により maximal 集合 = passing パターンの反鎖（big 反鎖 = 3300 を実算）。制御: census 18 点・K0804 dual-run 14 点・広幅 296/396・maximal(99)=3300 が全一致"
solution:
  board: level 17 標準形掃引 harness（mod 9×11・(a,u) 全列挙窓マスク）
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: 全幅 w≧17（センサス関数 unique(w)/maximal(w) に関する全称・上限なし）
  conditions: L=17・mod 9×11 窓マスク生成・連続整数行
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: prefix 単射（w=17..98 衝突 0）+ 通過条件の閉形式 + 区間支配判定（ordered pair 完全走査）+ w≧99 反鎖 3300 + 全既知観測点との一致
  independent_check: 検証器は K0803/K0804 の全 published 制御点（census 18 点・dual-run unique 14 点・unique(296)=3663・unique(396)=3960・maximal(99..132)=3300）を内部 assert で照合・w=73 の非 maximal 13 mask の支配例を直接検出（|P|=21 ⊂ |P'|=35）し per-width 直接 pairwise 計算と一致
  note: "K0803 は maximal=3300 を w≧99 で証明したが 66..98 は有限測定（サンプル点）だった。本項目は 66..98 の全整数幅を区間支配判定で厳密化し、unique の全幅閉形式（K0803 note の予告を実現）と 3 つの鋭い閾値（unique 3630 は w=96・初出現 w=37・maximal 3300 は w=66 から）を確定。小パターン参入窓 [265,286]/[309,363]/[529,561] により広幅帯の unique が一括ではなく段階的増加であることも確定（unique(265)=3632・unique(561)=3993=3,994−1〔空〕）。L≠17 は K0803 と同じく未検証"
relations:
- type: depends_on
  target: K0803
  note: パターン構造（3,994 相違・popcount ギャップ・小パターン支配補題）と w≧99 の包含⟺P⊆P' の源泉。本項目は K0803 の 66..98 有限測定を全幅厳密化
- type: depends_on
  target: K0804
  note: dual-run unique（w=69..82・14 点）が閉形式の制御値
- type: supports
  target: K0794
  note: level 17 掃引キャンペーンの mask ワークロードが全 w≧66 で 3,300（K0803 は w≧99 とサンプル点のみをカバー → 全 w≧66 に拡張完了）
artifacts:
- path: research/experiments/mask-census-closed-form-20261114/scripts/mask_census_closed_form.ts
  role: verifier
  note: 交叉統計 + prefix 単射確認 + 区間支配判定による全幅 table 計算・published 制御点の内部 assert 付き依存なし単一ファイル
- path: research/experiments/mask-census-closed-form-20261114/output/mask_census_closed_form_output.json
  role: data
  note: 完全表 w=17..98・changePoints（交叉統計の増分表）・s17 ヒストグラム・小パターン参入窓・制御照合結果
- path: research/experiments/mask-census-closed-form-20261114/report.md
  role: proof
  note: 定理・証明骨子・制御・限定の本文
- path: research/experiments/mask-census-closed-form-20261114/audit/audit_plateau_boundaries.py
  role: verifier
  note: 合同式の直接列挙とビット集合によるunique境界の独立監査
- path: research/experiments/mask-census-closed-form-20261114/audit/plateau-boundaries.json
  role: data
  note: 幅95・96・197・198・264・265のunique件数
---

## 命題（証明済み・全称）

1. **unique(w) は交叉統計で完全決定**（全 w ≥ 17）:
   unique(w) = #{P ≠ ∅ : k·|P| + |P∩[0,rem)| ≥ 17}（k = ⌊w/99⌋・rem = w−99k）。
   big（|P| ≥ 18）の最小通過幅は w*(P) = s17(P)+1 ∈ [37,96]
   （17 番目の点の位置+1）。小パターンは
   [265,286]（|P|=6・33 個）・[309,363]（|P|=5・297 個）・
   [529,561]（|P|=3・33 個）に参入。
2. **maximal(w) = 3300 がちょうど全整数 w ≥ 66 で成立**。
   w=37..65 では maximal = unique、w ≤ 36 では 0。
   w ≥ 73 の unique 増分は全て既存パターンの真部分集合で
   maximal を増やさない。
3. **鋭い閾値**（新規）:
   - unique(w) = 3630（big 全参入）に到達するのは **w = 96**
     （従来の「w=99 以降」は真だが鋭くない）。
   - マスク初出現は **w = 37**（26 mask）。
   - 広幅帯の unique は一括増加ではなく w*(P) ごとの段階的増加
     （unique(265)=3632 → unique(286)=3663 → unique(363)=3960 →
     unique(561)=3993 = 3,994 − 1〔空〕）。

独立な合同式列挙でも unique(95)=3615、unique(96)=3630、unique(264)=3630、unique(265)=3632 を確認した。幅を広げると各通過マスクは同じパラメータから拡張され、異なるマスクは制限先で区別できるため、unique は非減少。よって **unique=3630 となる整数幅はちょうど96〜264** である。K0803初版の「ちょうど99〜197」は十分範囲を必要条件と誤認したもの。

## 証明の骨子

- 単射: w<99 では mask = prefix（P∩[0,w)）で passing big 上単射
  （w=17..98 全幅で衝突 0）。w≥99 では第 1 周期が完全に含まれ
  mask から P が復元可能。
- 閉形式通過条件: |T_P(w)| = k|P| + |P∩[0,rem)| ≥ 17。
- 包含判定: w<99 では T_P(w) ⊆ T_P'(w) ⟺ min(P\P') ≥ w
  （P\P' = ∅ を含む）。各 ordered pair (P,P') は区間
  [max(37, s17(P')+1), min(98, min(P\P'))] で P を支配
  （13,173,270 ordered pair を完全走査）。
  w≥99 では包含 ⟺ P ⊆ P'（第 1 周期が完全）→ maximal は
  passing パターンの反鎖（big で 3300）+ 小パターンは常に
  big に支配（K0803）→ 全 w ≥ 99 で 3300。

## 制御と限定

- 全制御 PASS: census（maximal-mask-saturation-20261113・18 点）・
  K0804 dual-run unique（w=69..82・14 点）・unique(296)=3663・
  unique(396)=3960（K0803 プローブ）・maximal(99..132)=3300。
- w=73 の非 maximal 13 mask の支配を直接検出
  （|P|=21 ⊂ |P'|=35・s17(P)=72）し、per-width 直接 pairwise
  計算（verbatim harness アルゴリズム）とも一致。
- L=17 に限る。L≠17 は未検証（K0803 と同一の限定）。
