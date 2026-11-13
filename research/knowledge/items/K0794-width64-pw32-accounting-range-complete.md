# K0794: 幅64の円点数の決定 P(64)=32 — 現行g0会計の有効全範囲完走

- id: K0794
- status: proved
- date: 2026-11-13
- scope: 幅64の連続整数行（全 m ≥ 1・標準整数格子）の円点数 P(64) の完全決定
- statement: P(64) = 32

## 主張

幅 64 の行の円点数は **P(64) = 32**。さらに、これにより **P(w) は全幅
w = 6..64 で決定済み**となり（32 プラトー w=49..64）、現行 g0 会計
（convention B classMax・g4 類サイズ天井）が有効な範囲が完走した。

## 証明の骨格

K0792/K0793 と同一機械（K0790 の 16法 bit-set streaming level-17
分類機を classify 内蔵ノード上限チャンク 1.2M・lastDone 返却・
2チャンク/実行・冪等再開に拡張）による完全掃引。

- 上界: maximal mask 3,288個を28チャンク（27本はノード上限 1.2M）で
  完走し level 17 生残 0（ノード計 33,176,303・leaves=0）。
  ⟹ 全配置で d+s ≤ 16 ⟹ P(64) ≤ 32。
  会計: convention B classMax（w64: g2 8・g3 13・g4 類サイズ 16・全て < 17）。
- 下界: 2210 円の全 32 点（v-span 94 ≤ 2·(64−1)）。
- 制御: w=26 L=12 で S* ちょうど1生残（既存 K0782–K0793 と一致）。
- ノード成長: 25,418,908 (w63) → 33,176,303 (w64) = **×1.305**。
  （×1.36 則からの漸減傾向は K0793 と同じく継続。）
- maximal mask 数: 3,278 → 3,288。

## 帰結

1. **P(w) は全幅 w=6..64 で決定済み**。P=32 プラトーは w=49..64。
2. level 17 復活点は **(64, 83]** に狭窄（K0785: P(83) ≥ 34）。
3. **現行 g0 会計の有効範囲（w ≤ 64）を完走**。w=65 は
   ⌈65/4⌉ = 17 = L で g4 類サイズ天井引数が飽和し、level 17 分類の
   前提として **g4 形の mod 法 classMax 精密化が唯一の壁**となる。
   （g2 は w=65 で 9・g3 は 13 のまま w=67 まで < 17。）

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(65)..P(82) は open（P ∈ [32, 2⌈w/2⌉−4]）。w ≥ 65 は g4 精密化が前提。

## relations

- depends_on: K0793（K0792・K0790 の機械拡張とキャンペーン）
- supports: K0785（level 17 復活点の狭窄）

## artifacts

- research/experiments/width64-level-classification-20261113/scripts/width64_level_classify.ts
- research/experiments/width64-level-classification-20261113/output/width64_level_classify.json
- research/experiments/width64-level-classification-20261113/reports/width64-level-classification.md
- research/log/2026-11-13-width64-level-classification.md

## resume

1. w ≥ 65 用の g4 形 classMax 精密化（唯一の壁・g2=9/g3=13 は w=67 まで余裕）。
2. M_{w,q} 表の results/ 統合。
3. (10⁷,10⁸] の 34 点帯掃引・σ₁₇ 直接決定。
4. 次の空き K 番号: K0795。
