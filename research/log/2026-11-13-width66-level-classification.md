# 2026-11-13 高速レーン: w=66 キャンペーン開始（K0798 P(65)=32 の直接続編）

K0798 完走直後に着手。K0797 会計は w ≤ 84 で有効なので P(66) 決定に必要な
前提は level 17 全滅掃引のみ（下界は 2210 円 32 点・v-span 94 ≤ 130）。

## 実行記録

1. **機械**: w=65 完走で確立した REST6 2フェーズ機を最初から使用
   （survivors(REST6) ⊇ survivors(REST16)・phase2 は生残が出た mask のみ）。
   窓マスクは66ビット・ワード数 ceil(w/32) で自動化。
2. **窓マスク**: unique = maximal = **3,300**（w=65 の 3,296 から +4）。
3. **chunks 1-2（本セッション）**: mask 0..487 完了
   （chunk1: 0→223〔~10.8k/mask〕・chunk2: 223→488〔~9.1k/mask〕・
   計 4.8M nodes・leaves=0・生残0・フェーズ2必要 mask 0件）。軽い帯から開始
   （w=65 と同様に heavy band は後半に局在する見込み）。
   resume from=489（残り 2,812 mask）。

## 意味論（P(66) は OPEN）

- 完走時（leaves=0・生残0）で **P(66) = 32 が等号付き・全称で確定**する。
  それまでは P(66) ∈ [32, 128] open。
- ノード見込み: w=65 実績 42.6M × 成長則 ~1.35 → ~55M 前後
  （heavy band の局在性次第で大きく変わる・w=65 では外挿の1/3だった）。

## レジューム（次回の実行）

1. **w=66 キャンペーン継続**: output/width66_progress.json の chunks に追記
   （CFG.from=489・REST6 2フェーズ・cap 2.4M/chunk・1実行1..2チャンクが安定）。
2. 完走時は K0799（P(66)=32）に昇格・results/fixed-width/ 追従
   （pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0799**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
