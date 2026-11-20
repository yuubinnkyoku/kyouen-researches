---
id: K1096
title: 残余72行 WIN8-D10 root 00000000000000003800000008003180 の完全勝利戦略証明書抽出・三重独立検証（34,529行・3実行byte-identical・18/18監査gate PASS）
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases: []
relations:
- type: depends_on
  target: K1086
  note: 対象rootのWIN8-D10 verdict（両順序uncapped loss=true・nodes 903,977/1,146,417）と主張被覆4行の出典。正本SHA-256 3045e152…を入力pinし、本項はprobe再現で同値を確認した
- type: depends_on
  target: K1069
  note: runner v17（git blob c132cc…・pilot_d6 3,402制御）と証明書形式 n11-terminal-strategy-v1 の流用元
- type: see_also
  target: K1070
  note: 17枚目のWIN7証明書に対する三重検証の体裁（BigInt 3x3 + Bareiss 4x4 + 第三方法）
artifacts:
- path: research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11
  role: certificate
  note: 証明書本体（1,251,923 bytes・34,529行・SHA-256 1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c・抽出3実行でbyte-identical）
- path: research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/scripts/cert_extractor_win8_root8003180.ts
  role: verifier
  note: 抽出器（WIN7 repo正本抽出器にv17 fbtOR修復・recordRow衝突検出・8石root駆動を適用した盲抽出・自己検査付き）
- path: research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/scripts/verify_win8_certificate_bigint_independent.mjs
  role: verifier
  note: 独立検証器1（BigInt 3x3余因子・全53 sub-root走査・被覆union）
- path: research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/scripts/verify_win8_cert_bareiss.ts
  role: verifier
  note: 独立検証器2（Bareiss 4x4整数行列式・sub-root 9石・consumed union）
- path: research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/scripts/assemble_win8_audit_20261120.py
  role: verifier
  note: 監査機械（python第三方法として独自全木走査+簿記18 gate・fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/output/win8-cert-extract-verification-20261120.json
  role: data
  note: 監査正本（SHA-256 ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da・18/18 PASS・別cwd再実行byte-identical）
scope: >-
  K1086 のWIN8-D10 candidate 00000000000000003800000008003180（greedy第一位・
  主張被覆4行）に対する n11-terminal-strategy-v1 original_first_WIN8
  second_to_move_LOSS 証明書の盲抽出と独立検証。8石receipt被覆幾何・fold・
  行閉鎖・他rootの抽出は含まない。
evidence: >-
  （1）verdict基盤: runner v17で両AND順序depth-10 probe再現がK1086出版値と
  node-exact一致（903,977/1,146,417・loss=true uncapped・terminal [14,18]・
  pilot_d6 3,402×4回）。（2）抽出: 初手ごと53プロセス（A1総nodes 3,394,332・
  fbt_drops 0・fatal/conflict 0）と同一cwd再実行（A2・初手単位nodes完全一致）、
  別cwd全一括単一プロセス（B・総nodes 2,608,236）の3実行で証明書bytes完全一致
  （SHA-256 1393128972…）。root mobility 53は純Python整数行列式で独立再導出。
  （3）検証: BigInt 3x3とBareiss 4x4とpython第三方法が、winner-to-move
  49,509・loser-to-move 14,082・応手辺 67,420・終端 13,364（全てloser-stuck）・
  終端石数 [14,18]・consumed union == 34,529行（missing 0 / extra 0）で
  全数値一致。（4）監査: 18/18 gate PASS（K1086 SHA pin・probe再現照合・
  root形状/mobility再導出・summary整合・証明書形式）・別cwd別プロセス再実行で
  audit JSON byte-identical。（5）解釈: 本証明書は当該8石rootのゲーム木のみを
  証明する。S6親行の閉鎖には8石receipt被覆・foldが別途必要で、本項では行を
  1行も閉じない。REFUTED-D10・nodes数・solved数を勝敗として読まない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit 0360f21a）の下、K1086 WIN8-D10 candidate 7根の
うち `00000000000000003800000008003180` の戦略証明書を盲抽出した
（3実行byte-identical・34,529行・1,251,923 bytes）。
BigInt 3×3余因子・Bareiss 4×4・python第三方法の3独立走査が全数値で一致し、
監査機械は18/18 gate PASS（別cwd再実行でも監査正本はbyte-identical）。
並走レーンが宣言済みの root `…8180000` 抽出に対する独立第二導出としても
機能する。行閉鎖・fold・勝敗判定は含まない。
詳細は[実験](../../experiments/n11-residual72-win8-cert-extract-root8003180-20261120/README.md)・
[証明書](../../experiments/n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11)・
[監査正本](../../experiments/n11-residual72-win8-cert-extract-root8003180-20261120/output/win8-cert-extract-verification-20261120.json)・
[研究ログ](2026-11-20-n11-residual72-win8-cert-extract-root8003180.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべてUNKNOWNのまま。**
