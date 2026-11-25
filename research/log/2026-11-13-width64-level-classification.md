# 2026-11-13 幅64 level 17 分類 — P(64)=32・会計有効範囲完走（高速レーン）

## セッション概要

K0792/K0793 キャンペーン（w=60..64）の最終幅。K0793 の
classify 内蔵ノード上限チャンク機（1.2M・lastDone・2チャンク/実行・冪等再開）で
w=64 の maximal mask 3,288個を28チャンクで完走し、**P(64)=32 を決定**。
これで **P(w) は全幅 w=6..64 で決定済み**（32 プラトー w=49..64）となり、
現行 g0 会計が有効な全範囲を完走した。

## 結果

- **P(64) = 32**（leaves=0・生残0・ノード計 33,176,303・28チャンク中27本が1.2M上限）。
- 会計: convention B classMax — w64: g2 8・g3 13・g4 類サイズ 16・全て < 17。
- 下界: 2210 円 32 点（v-span 94 ≤ 2·63）。
- 制御: w=26 L=12 で S* ちょうど1生残 — 既存結果と一致。
- ノード成長: 25,418,908 → 33,176,303 = **×1.305**（×1.36 則から漸減継続）。
- mask: 3,278 → 3,288（ほぼ線形）。

## 帰結

1. P(w) 全幅決定（w=6..64）。level 17 復活点は **(64, 83]** に狭窄。
2. **現行 g0 会計の有効範囲完走**。w=65 は ⌈65/4⌉=17=L で g4 類サイズ天井が
   飽和 — **g4 形の mod 法 classMax 精密化が唯一の壁**。
   g2 は w=65 で 9・g3 は 13（w=67 まで < 17）。

## push

- research/experiments/width64-level-classification-20261113/scripts/width64_level_classify.ts
- research/experiments/width64-level-classification-20261113/output/width64_level_classify.json
- research/experiments/width64-level-classification-20261113/reports/width64-level-classification.md
- research/knowledge/items/K0794-width64-pw32-accounting-range-complete.md
- 本ログ

## レジューム（次回の実行）

1. **w ≥ 65 用 g4 形 classMax 精密化**（唯一の壁）: g4 形は
   4(y−y′)(y+y′+D) 型の剰余類ごとの QR 構造。mod 法で classMax を
   17 未満に切れるかが w ≥ 65 の level 17 分類の可否を決める。
   g2=9（w=65）/ g3=13（w=67 まで）は余裕あり。
2. M_{w,q} 表の results/ 統合。
3. (10⁷,10⁸] 34点帯掃引・σ₁₇ 直接決定。
4. 次の空き K 番号: **K0795**。
5. 11×11 空盤・二石 root {49,60} は引き続き UNKNOWN（長期レーン）。

並走レーン（n11 S7 reuse 監査・3xm q5 母函数）は主題独立・K番号重複なし。
