# 2026-11-13 高速レーン: maximal mask 数の飽和検証 — w=66..132 でちょうど 3,300 プラトー

width68 キャンペーン（research/log/2026-11-13-width68-level-classification.md）の
観察「maximal mask 数は w≥66 で 3,300 に飽和か（要 w≥69 検証）」への回答。

1. **結論（exhaustive-enumeration・有限確定事実）**: maximal mask 数は
   w=66..132 の全測定点（66..72, 75, 80, 90, 99, 105, 110, 121, 132）で
   **ちょうど 3,300**。unique は単調増加し w=99 以降 3,630 で固定
   （超過 330 個は全て既存 maximal の真部分集合）。
2. **帰結**: level 17 掃引キャンペーンは w≥66 で mask ワークロード数が一定。
   コスト増 ~×1.35/w は per-mask ノード加重のみ。11×11（w≤121）でも同様。
   w>132 は未計算（99 周期構造から w<198 まで維持予想・予想の域を出ない）。
3. 制御: w=64→3,288・w=65→3,296・w=66/67→3,300 が K0794/K0798/K0799/K0801
   既往値と完全一致（width68 progress JSON harnessControl と相互検証）。
4. 実験dir: research/experiments/maximal-mask-saturation-20261113/
   （scripts/maximal_mask_saturation.ts + output/maximal_mask_census.json + report.md）。
5. 次の課題: (1) w=133..198 の有限検証、(2) 3,300 maximal の構造説明
   （3,630 unique のうち 330 個が非maximal になる理由）、
   (3) w≥66 全キャンペーンの maximalMasks 前処理共通化
   （mask 列挙を w=99 の 1 回に定数化できるかの厳密化）。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
