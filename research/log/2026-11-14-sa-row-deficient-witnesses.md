# 2026-11-14 高速レーン: SA探索機による欠損witness連続発見 — K0810の下界3件更新と6行blocker構造分析

## セッション概要

- 開始時 HEAD 03755205。最新 main・AGENTS.md・research/knowledge/README.md・
  K0808〜K0810 を確認してから着手（K0810 は並走SATレーンが直前に反映済み）。
- K0808 の `deficient_maximal_machine.ts` の census・census不使用独立検証器を
  Node 機械移植し、探索部を SA に置換した `sa_machine.js` を開発。
  census・検証器は verbatim（接線二重追加防止・r²/g² 修正済み版）。

## 成果

1. **下界3件の更新**（全witness・census不使用独立検証で safe+maximal PASS・
   `output/sa_results.jsonl` に全記録）:
   - M_{6,5}: 23 ≥ → **26**（23石@6×22..6×25 の4盤連続）
   - M_{6,6}: 20 → **21**（29石@6×17..6×20。K0810未解決の m=18,20 を解決）
   - M_{5,6}: 18 → **19**（24石@5×16..5×18。K0810未解決の m=18 を解決）
   - (6,8) m=12..15 の41石witnessで K0810 SAT（m=12..17）を補強（下界18不変）
2. **制御全PASS**: 2×8 q=4→5石（K0796再発見）・6×19 q=5→23石（K0808一致）・
   5×19 q=7→30石満容量（K0759一致・欠損witnessなし）・6×15 q=6→29石（K0808一致）。
3. **抵抗の記録（非発見・不在証明ではない）**:
   (6,5) m=26（2シード×90秒）・(6,6) m=21（3シード×90秒）・
   (5,6) m=19（120秒×2）・(6,8) m=16（90〜120秒×3）・(5,7) m=20（90秒）。
4. **K0332 六行移植の構造分析（M_{6,7} 上界402の算術縮小の事前検討・未完）**:
   - mod9 補題は6行にそのまま拡張（(C,N) 81組中 6行すべてを満たす組 0・五行制御も 0）。
   - 六行盤の blocker 円の行分布は対象行0石: {2+2+2, 2+2+1+1}、1石: {2+2+1, 2+1+1+1}。
     2+1+1+1（6行占有）は mod9 で除去できるが **2+2+1+1（5行占有）と 2+1+1+1（5行占有・弦対0本）**
     は五行版の議論では落ちない。
   - 弦対予算 C(5,2)×29=290・Melchior（n≤30 → 5点直線 ≤36/石・y≤36b≤180）で
     最適化すると利用不能点の上界は b+2·290 で最大 **585** —
     **K0318 の U=402 より悪い**。弦対会計の naive 移植では (6,7) 上界は改善しない。
     改善には 2+2+1+1 型・2+1+1+1 型への追加予算（singleton 点対の会計・
     K0318 の三つ組/点対予算との併用）が必要。

## 実装・運用の記録

- SA設計: 状態は常に極大（maximalize は K0808 の q−2カウント評価greedy verbatim）。
  move = 石を ≤30% 乱数除去→再極大化、Metropolis（拒否時は前状態復帰）・
  T: 2.5→0.02 幾何冷却→再加熱・30万iter停滞でベスト再シード。seedは全実行で記録済み。
- 実行環境: 実行環境リセット（300秒timeout）で2回 workspace を喪失。
  → 機械・JSONL は永続領域に置き、`runbatch.sh` が1ケース完了ごとに
  JSONL へ追記する方式に変更。結果は seed 指定で完全再現（制御・witnessとも再取得済み）。
- (6,8) m=12 は 12ms/216 iter、(6,5) m=22 は数十秒で発見。
  K0809 ハンディキャップ貪欲の1500 restart 非発見帯を一掃した。

## 反映（1コミット1ファイル・反映前にHEAD 03755205 を再取得）

- `research/experiments/sa-row-deficient-witnesses-20261114/scripts/sa_machine.js`
- `research/experiments/sa-row-deficient-witnesses-20261114/output/sa_results.jsonl`
- `research/experiments/sa-row-deficient-witnesses-20261114/report.md`
- `research/knowledge/items/K0811-sa-row-deficient-witnesses.md`
- `results/fixed-width/mwq_stabilization.csv`（(6,5)(6,6)(5,6) の3行更新 +(6,8)注記）
- 本log

## レジューム

1. 最前線 (6,5) m=26・(6,6) m=21・(5,6) m=19・(6,8) m=16 の追加攻撃
   （SA シード多様化・長時間予算、または K0810 SAT機の timeout 延長）。
2. 2+2+1+1 型 blocker への追加予算の設計 → (6,7) 上界 402 の本格的縮小。
3. (5,7) m=20,21 のSA再攻撃（今回は90秒×1のみ）。
4. 次の空きK番号はK0812（push直前に再確認）。
