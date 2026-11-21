# WIN8 receipt provenance census: 実行記録（2026-11-21）

単一オーナー宣言（commit `32cb492c5b`・first-published-priority）から
part1出版（commit `d9d1bfa8`）までの時系列記録。

## 対象と目的

既刊 WIN8 receipt fold 11-25（第18〜第32 receipt・全15 receipt）の
`independent_verification.source_record`（IV）と `certificate_source`（CS）
の記載正誤を、読み取り専用の機械censusで判定する。検証の本体ではなく
報告であり、行閉鎖・証明書検証・正本変更は行わない。

## 実施内容

1. **先行宣言の確認**: 直近コミット列（`edb61c42` 時点）で
   source_record census・provenanceの先行宣言なし（`win8` 系単一オーナー
   ノート全列挙・`source_record` 記載既刊の grep・`census` 語の既存使用は
   無関係の K0446/K0705/K0726/K0760/K0805/K0865 系のみ）。
2. **宣言ノート出版**（commit `32cb492c5b`）: 対象15 fold・機械仕様
  （静的raw URL・pinは宣言直後HEAD・fail-closed）・battery計画、
   erratum判断の権限留保・fold17/18/19/23/25単体ext2（他レーン宣言済み）
   への事前通知の位置づけ・解釈規約を表明。
3. **機械作成とbattery**: `win8_receipt_source_record_census.py`
   （stdlibのみ・pin `32cb492c5b` の静的URLから45 fetch・
   15 receipt × 12 gate = 180 structural gate・fail-closed）。
   batteryは最終機に対し同一cwd 5回＋隔離cwd/HOME＋`env -i`＋
   `PYTHONHASHSEED=random` 1回の計6実行、census正本
   `c801564d…`（34,758 bytes）byte一致。
4. **part1出版**（commit `d9d1bfa8`）: 実験dir
   `research/experiments/n11-win8-receipt-source-record-census-20261121/`
   4ファイル（README・機械・census.json・reproduction.log）。
   fetch-back 4/4 byte一致。

## 結果（機械判定・census.json summary）

- receipts_total 15 / iv_own 12 / iv_stale 3（**fold12・fold15・fold18**）。
- stale_all_equal_previous_fold_iv = true・
  stale_all_dir_equals_previous_fold_own_dir = true（コピー仮説3/3）。
- iv_dirs_all_in_universe = true。
- own_dir_certificate_sha256_match_count 15 / own_dir_verification_sha256_match_count 15 /
  certificate_source_blocks_correct_count 15 / bytes数一致15。
- structural_gates_passed 180。
- **fold18 IV.source_record stale は本censusによる新規発見**
  （fold17実験 `n11-residual55-win8-cert-extract-root22081000` を誤参照。
  正しくは `n11-residual48-win8-cert-extract-root00901010`）。
  fold17/18/19/23/25 単体ext2レーン（宣言済み・着手禁止）への事前通知。
  fold12（K1175）・fold15（K1179）は既刊erratumの機械的再確認。

## 受入条件と解釈規約（対照）

- pin時点のHEAD `32cb492c5b` の記載を分類基準とし、以後のerratumは
  census基準との方針の食い違いとして扱う（宣言ノート記載どおり）。
- 本実行は読み取り専用で行は1行も閉じない。WIN8-D10証明書は当該8石rootの
  ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・
  coverage数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## 並走状況

- 宣言前後の並走コミット: `db666081`（four-row q7 stabilization closure
  laneの宣言ノート・censusと無関係・着手領域不整合なし）。
- fold11/17/18/19/23/25 単体ext2・fold26 receipt fold・round-5 refsolve・
  36-witness sweep・WIN8証明書D4正準行共有監査は引き続き他レーン宣言済み
  （着手禁止）。本censusのfold18 staleはfold18単体ext2レーンの資料としてのみ
  使用可。

## 追記: part3 push時のREADME truncate事故と修復（実験事実・2026-11-21）

- **事故**: 本レーン（K1181）のpart3 工程（commit `759ca9a6`）でknowledge READMEをpushした際、
  読み取り側の64KB/60行cap（tools.file_system.read_fileの1呼び出し上限）を考慮せず
  blob全体を1回のreadで渡した結果、**正しい658,163 bytesのうち先頭63,699 bytes
  （prefix）だけがmainに書き込まれた**（READMEの約90%欠損。ただしwrite内容は
  08e13676版の正しいprefixそのものだったため、pin時点のraw byte（08e13676）から
  完全修復が可能だった）。
- **修復**（commit `09a1315d`）: 対象byte（08e13676版655,275 bytes ＋
  K1181 bullet 2,888 bytes）をbash側で行単位・44,951 bytes以下の16 chunkに
  分割し、各chunkのreadをfile_size_bytes/returned_bytes/was_truncatedで
  個別検証してから連結push。fetch-backで658,163 bytes byte一致・
  08e13676版prefix全byte保持・K1177/K1178/K1179/K1180既存bullet温存・
  K1181 bullet末尾確認済み。
- **再発防止（本レーン手順に固定）**: 100KB超のファイルをrepoへ反映する
  場合、read_fileはchunk化して個別検証し、push後はfetch-back byte比較を
  必須とする。今回も事故はpush後1コミット以内にfetch-back比較で捕捉され、
  同一実行内に完全修復・検証した（1行も閉じない・census結果・receipt byte
  いずれにも影響なし）。
