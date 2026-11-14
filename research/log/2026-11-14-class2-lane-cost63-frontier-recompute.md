# class2-lane cost-61-c + cost-63 正式frontier再計算（2026-11-14）

## 背景

cost-58 / cost-61-c / cost-63 の3 child sweepと証明書（3+1+4 WIN7）は main に反映済みだが、
frontier への効果は各 sweep record 内の推定（cost-61-c: after-cost58 基準・cost-63: through-cost61-c 基準）
にとどまっており、**全レシート込みの正式再計算が未実施**だった。本ログはその残TODOを完遂する。

## 実施内容

- `scripts/recompute_frontier_cost63.py` を新規作成（`recompute_frontier_cost75.py` のロジックを直接拡張）。
  全段階制御（baseline 638 → batch1 657 → batch2 665 → batch3 690 → cost60 724 → cost61 735 →
  cost61b 749 → cost64 779 → cost65 786 → cost68 804〔blocker S5消滅もassert〕 → cost58 814 →
  cost75 831/7016/551482/5240/411954〔cost-75 target S5消滅もassert〕）を公開値と完全一致で再現してから、
  cost-61-c（1 root）と cost-63（4 root）の covers を加算して測定した。

## 結果

- **after cost-61-c: solved 833・unique remaining 7014・sum 551,352・open 5239/411,885**
 （cost-61-cの効果: covers 7 / marginal 5 / manifest内 +2 — 公表frontier_effect（after-cost58基準）と完全一致）
- **after cost-63: solved 841・unique remaining 7006・sum 550,810・open 5236/411,675**
 （cost-63の効果: covers 25 / marginal 20 / manifest内 +8 — 公表frontier_effect（through-cost61-c基準）と完全一致）
- 重要な交叉検証: cost-63 の marginal 集合は、より大きな through-cost75+cost61c solved set に対しても
  **1つも縮小しなかった**（published_marginals_already_solved = []）。cost-60〜75 の各レシートとの
  二重カバーが存在しないことの独立確認になる。cost-61-c も同様（2 marginal とも残存）。
- best class-2 target S5 `00000000000000809082000000000000` は **33 orbit/2245 → 28 orbit/1926**。
  次点 class-2 は `00000000000000809102000000000000`（40/2850）。
  best class-4 `00000000020000003800000080000000` は 24/1934 不変。
- 出力は2回実行で byte-identical（決定性確認済み）。

## 解釈上の注意

frontier再計算は公開レシートの bookkeeping のみで、新しい勝敗判定を含まない。
REFUTED-D10 は深さ10以内のWIN7の否定のみ、WIN7証明書は7石root個別の深さ10以内のWINのみ。
**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN のまま。**

## レジューム

1. best class-2 S5 の残28 orbit の最安未sweep child（cost 63 帯 `00000000000000809082000000001000`・
   `000000000000008090a2000000000000`・`00000000000000809082000000080000` は本再計算でも未解決のまま）。
2. best class-4 `00000000020000003800000080000000` の最安 child（cost 74 `00000000020000003800000080000020`）。
