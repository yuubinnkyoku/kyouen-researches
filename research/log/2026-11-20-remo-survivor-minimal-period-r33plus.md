# 2026-11-20 生存者列最小周期 r=33..48 掃引（K0925 S32拡張・K1145）

単一オーナー宣言（2026-11-20 10:22Z・fast lane）に基づく実行記録。

## 経緯

1. **宣言・現状確認**: 宣言ノートの対象（K0925 定理S32 の続編、
   K0922 補題DIV + 各真約数 1 個の小 witness 棄却を r=33..48 に
   適用、実験 dir `research/experiments/remo-survivor-minimal-
   period-r33plus-20261120/`）を確認。main に同実験の要素なし
   （衝突なし）。K0925 出版監査（SHA-256 b3733ed5…）から W5 の
   r=17..32 値を pin テーブルとして抽出。
2. **規模確定**: Q(r)=lcm(1..r) の真約数は r=33..48 の合計
   1,548,272 個（Q(48)=4.43e20 で 294,911 個）。試し割りは不可
   （√Q≈2.1e10）のため素因数分解（e_p=max{a:p^a≤r}）から約数を
   列挙し、S0 で r=2..20 の試し割り完全一致と r=33..48 の解析的
   指数パターンを機械検査。実測すると survivor 1 回 127-241µs・
   平均 1.9 回/約数で、全掃引はDelta 約 6 分。
3. **実装**: K0925 W5 の意味論をそのまま再現する専用検証器
   `survivor_witness_r33plus.py`（stdlib のみ・決定的）。
   逐語 survivor_fast、witness 最小昇順・窓[1,150]/[151,1500]。
   本環境のコマンド時間上限向けにシャード（16,384 約数単位）
   チェックポイント再開（`--budget`）と、再開後も同一になる
   チェインド chunk sha256 による witness ストリーム pin を導入。
   S1: r=17..32 の再計算が K0925 出版値と 5 項目全一致することで
   実装の意味論同一性を固定。S3: 正方向 period アンカー
   （C∈[1,1500]+錨・24,064 比較）。S4: r=33..48 での verbatim
   1石配分再帰==閉形式双対==survivor_fast の三一致を 2,400 組で
   新規 pin（K0925 TWIN は r≤24 まで）。
4. **掃引結果**: **r=33..48 の全 1,548,272 真約数がすべて
   witness C≤150 で棄却（unwitnessed 0・フォールバック窓不使用）**。
   wit_max: 33-36→25, 37-40→35, 41/42→29, 43-46→30, 47/48→39
   （すべて ≤ r−1、最大 witness の d は Q/47 型で h*=1）。
   C=1 が witness なのは 808,586 個（52.2%）。
5. **新規観察**: 等しい lcm(1..r)（等Qブロック）内では
   **witness ストリーム d→w が r 全体で同一**（ブロック
   {32..36} では r=32 の S1 再計算 sha と r=33..36 の S2 sha が
   同一 42f97831f66daaa2…）。監査のチェインド sha256 がブロック
   単一性を機械 pin。K0925 の「ブロック内集計一致」を全判定の
   r 不変性まで精緻化。観察のみで証明なし（K0926/K0928 構造に
   よる説明が可能かは次課題）。
6. **検証プロトコル**: assemble 二重実行 byte 一致必須。本金
   cwd（チャンク再開）と隔離 cwd フル再計算（別プロセス・自前
   checkpoint・チャンク再開）の 2 プロセスで監査 byte 同一
   （SHA-256 0b5ae7eb…・32,790 bytes・5/5 ok）。CI step で
   新規計算→git diff pin。
7. **採番**: 出版時点の main 最大番号は K1142（n11 fold25）。
   仮採番 K1143 で一括出版したが、15分先行で並走y11 fitting
   レーンが同名異slugの K1143-two-token-y11-parametric-closed-form-
   fit（12:15:50Z・27944a94）を出版しており K1144 も使用済み
   （n11残余72二検証・12:18:26Z）だったため、AGENTS.md再採番規則
   に従い K1145 へ再採番し、item/log/README bullet/CI step名/監査
   JSON item欄を同時更新して旧 K1143 item path を削除した
   （数値内容・検査・正本は再採番不変・監査 SHA-256 0b5ae7eb…）。

## 出版物

- `research/experiments/remo-survivor-minimal-period-r33plus-20261120/`:
  survivor_witness_r33plus.py・report.md・output/audit.json・
  output/published_run.txt
- knowledge item: `research/knowledge/items/K1145-remo-survivor-
  minimal-period-r33to48.md`（定理S48・機械確定 status: proved）
- knowledge README に K1145 bullet、knowledge.yml に CI audit step
  （監査 JSON の git diff pin）を追加（初回は仮採番K1143で出版し
  再採番コミットで修正済み）。

## 信頼境界と残課題

- Δ=0 一様盤（定理D域）限定。定理S48 は r≤48 の機械確定で、
  生存者側の全称最小性（有界witness予想）は OPEN のまま。
- 等Qブロック witness ストリーム同一観察の構造説明（K0928 pot
  縮約・K0926 E6U との接続）、r≥49 延長、h*(Q/p) 算術の
  r=33..48 範囲への拡張検証は次課題。
- 11×11 空盤の勝敗には一切言及しない。
