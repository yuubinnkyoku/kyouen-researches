# 2026-11-25 C-SUM 多重トークン tail collapse 実行 log（K1312）

高速レーン定例実行。publish-then-execute chain の全体記録。

## 経緯

1. **最新 main・未解決事項の確認**: 着手時 HEAD `e92542fd`（K1311 kit）。
   その直後に K1311 スロットが並走レーンに取得されたことを確認:
   宣言ノート `7653a639` + kit `e92542fd`（境界帯全多重度パッケージ
   T-DB/L-SDB・K0832 予想 B 回収）。内容は本レーンが準備していた
   tail 方向の成果と**完全に補完的・重複なし**（彼らは境界行 k=z+n−2、
   本レーンは tail k≥z+n−1 を主張）。K0832 垂直ファイバー総合 item
   （K0832）で公刊 tail 系（R≥2k+z−1 系）が all-ones 族のみであること、
   K1308 に一般多重集合の tail 法則が census 予想 O3/F1 として
   未解決登録されていること（1380 番台の未解決事項）を再確認し、
   **K1312 として一般多重集合 tail の全称証明パッケージ**に回転。
2. **探索（宣言前・凍結）**: `explore_csum.py/.out`（E-wave）:
   E6 境界行 k=z+n−2 の反 T-CSUM witness 149 セル（n3 80 / n4 49 /
   n5 1 / n6 11 / n7 8）、E7 境界行値分布（n3 z=0..10 / n4 z=0..8）、
   E8 純族 (a,…,a) の非単調安定化 bad パターン（n3..n5）。全セルが
   公刊 T-DB 則 D(E,k) と一致することを 149/149 で確認（インターロック）。
   ヘッダ修正（K1311→K1312 名義）後の再実行で .out が byte-identical
   再現（sha `4467429d…`）。
3. **機体構築**: `verify_k1312.py`（sha `eba59473…`）。設計段階の監査が
   本機体のバグ 2 件（typed_kids A 手の同値グループ全体置換誤り・E7 比較の
   str/int キー不整合）を機械検出し修正（宣言ノート §6 に正直記録）。
4. **predry 4 走**: 同一 cwd（PYTHONHASHSEED=random/1）+ 隔離 tree
   `env -i`（99/7）。全走 rc=0・stdout byte-identical
   `b22b9b02…`・約 8.2 秒/走。run3 の初回で seed 99 指定漏れがあり
   取り直し（両実行とも bad 0・同一 sha・§6 記録）。

## publish-then-execute chain

- **宣言** `13e5f611`: `research/log/2026-11-25-csum-multitoken-single-owner-note.md`
  （§1 主張・§2 手証明全文〔L-2 mex{1}=0 帰納・L-1 四分枝スライス・
  T-CSUM 二重帰納: 子3型 A/B/C すべて値 1−c・opts={1−c} 均一・C-SHARP
  2 構成家族〕・§3 探索凍結・§4 機体宣言〔counts 26,302・変異表 13 種〕・
  §4.5 主張の区別・§5 open 登録・§6 honest 経緯）。
  push 前に repo 全域 commit 検索で **K1312 空きを確認**（対抗宣言なし）。
  fetch-back: blob sha `027ea893…` がローカル git blob sha と一致。
- **kit** `f74ead63`: `research/experiments/csum-multitoken-20261125/`
  13 ファイル（README・verify_k1312.py・engine_block.py・explore_csum.py/.out・
  predry/dryrun1-4 (+.info)）。1 回目の push が Part EB レーン（11×11
  canonical cache 採用系列・HEAD `6f280e0b`）との **non-FF 競合**で失敗、
  最新 main 再取得後に再 push で成立（内容に影響なし・本 log に記録）。
  fetch-back: 13/13 ファイルの blob sha がローカル git blob sha と完全一致
  （bytes 忠実・全サイズ一致）。
- **公式監査・成果物** `69be721c`: fetch-back と同一 bytes から公式 4 走
  （同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree `env -i`×2 99/7）。
  全走 rc=0・stdout byte-identical sha `b22b9b02…`（宣言・predry と同一）。
  elapsed 8.1 / 8.2 / 8.1 / 8.3 秒。総比較 26,302・overall_bad 0・
  engine_gate PASS（pin `bd5f22e4…`）。変異電池 13 種すべて宣言どおり
  fail-closed: engine rc=2（`0ea47a80…` ≠ pin）・c3 2,184・c4 2,310・
  c5 3,024・c67 1,748・ty 24,648・lm 920・ps 8,388・ce 616・sw 149・
  ob 1・db 149・sc 140（全 rc=1・単一電池 bad）。
  `output/` 36 ファイル出版（official_run1-4.out+.info・tamper レコード
  13・detcheck.json **OFFICIAL-PASS**・MANIFEST-sha256 50 行）。

## 電池（総計 26,302・bad 0）

D1 census n3 2,184 / D2 census n4 + far n3 2,310 / D3 census n5 3,024 /
D4 census n6/n7 + far n4 1,748 / D5 typed self-check 6,642 / D6 基底補題
(L-2・L-1・n=1 均一性) 920 / D7 公刊アンカー転写 8,388（K1308 D8 C-SUM 箱
2,364〔同紙では予想観測・本項では定理インスタンス〕+ T-UH tail 箱 5,760 +
L-SB spot 264）/ D8 cross-engine 616 / D9 sharpness witnesses 149 /
D10 OBS 表 32 / D11 T-DB interlock 149 / D12 sharp construction 140。

## 主張の区分

- 定理（手証明が正本）: T-CSUM・L-1・L-2。系（公刊 T-DB から従う）: C-SHARP。
- 有限 witness 認証: D9/D11/D12。OBS（無主張）: E7/E8。
- census は証明ではない。下帯 k≤z+n−3（n≥3）は open のまま
  （K1311 O-BBL と同一 open・本項は不消費）。
- 11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費。

## 知識反映

- K item `K1312-csum-multitoken-tail-collapse.md`（relations:
  resolves/extends K1308〔O3/F1・T-UH〕・extends K1311〔tail 層の全称証明
  供給・インターロック〕・depends_on K0832〔閉形式・all-ones 整合〕・
  related K1282〔engine pin chain〕）。
- knowledge README に K1311 bullet の直後に K1312 bullet を挿入。

## 次課題

1. 下帯 k≤z+n−3（n≥3）の真の法則（E7/E8 の OBS が入力データ・
   K1311 の OBS-BBL 凍結表と連結）。
2. 純族非単調パターン（n5 koff2 で 63/72 に再上昇）の全称説明。
3. r 人対戦版・d 次元版への tail collapse 一般化の可否。
