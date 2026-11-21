---
id: K1181
title: "WIN8 receipt provenance census — 既刊15 receipt（folds 11-25）の IV.source_record / certificate_source 機械判定（own 12 / stale 3・fold18 stale が新規発見・コピー仮説 3/3）"
kind: computation
status: computed
topics: [verification, certificates, search-methods]
aliases:
  - "WIN8 receipt source_record census folds 11-25"
  - "15 receipt provenance census 180 gate・census正本 c801564d…（6実行byte一致）"
  - "fold18 IV.source_record stale 発見（fold17実験を誤参照）・stale 3例はすべて直前foldのIV値と一致"
relations:
  - type: related
    target: K1175
    note: "fold12外部第二検証。当censusはfold12 receipt（第19）のIV.source_record stale（fold11実験を誤参照）を機械的に再確認（同erratumの対照）。"
  - type: related
    target: K1179
    note: "fold15外部第二検証。当censusはfold15 receipt（第22）のIV.source_record stale（fold14実験を誤参照）を機械的に再確認（同erratumの対照）。"
  - type: related
    target: K1180
    note: "fold16外部第二検証。fold16 receipt（第23）のclean記載をcensus universe内で再確認し、fold17/18/19/23/25の単体ext2（他レーン宣言済み）への事前通知（fold18 stale）を位置づける。"
artifacts:
  - path: research/experiments/n11-win8-receipt-source-record-census-20261121/README.md
    role: source
    note: "対象・固定pin（宣言出版HEAD 32cb492c5b）・実施内容と結果・再現手順・限界の記録"
  - path: research/experiments/n11-win8-receipt-source-record-census-20261121/scripts/win8_receipt_source_record_census.py
    role: machine
    note: "census機械（stdlibのみ・決定的・fail-closed・SHA-256 e7cffd18…・pin 32cb492cの静的raw URL 45 fetch）"
  - path: research/experiments/n11-win8-receipt-source-record-census-20261121/output/census.json
    role: census
    note: "census正本（34,758 bytes・sha256 c801564d…・同一cwd 5回+隔離cwd/HOME+env -i+PYTHONHASHSEED=random 1回の6実行byte一致・summary: own 12/stale 3・certificate_source_blocks_correct 15）"
  - path: research/experiments/n11-win8-receipt-source-record-census-20261121/output/reproduction.log
    role: record
    note: "実行記録・summary主要値・findings discipline・出版前機械草案破棄（root末尾比較の整数→suffix修正）の実験事実"
  - path: research/log/2026-11-21-n11-win8-receipt-source-record-census-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 32cb492c5b・読み取り専用・erratum判断は記録所有者に留保）"
  - path: research/log/2026-11-21-n11-win8-receipt-source-record-census.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照・fold17/18/19/23/25単体ext2並走への事前通知"
---

# WIN8 receipt provenance census（folds 11-25・15 receipt）の機械判定

## 概要

単一オーナー宣言（commit `32cb492c5b`・読み取り専用・行は1行も閉じない）
の下、既刊 WIN8 receipt fold 11-25（第18〜第32 receipt・全15通りの
`receipt-fold` 実験）について、各receipt JSONの
`receipts[0].independent_verification.source_record`（IV）と
`certificate_source`（CS）の記載正誤を、宣言出版HEADにpinした静的raw URL
（15 receipt JSON ＋ 15 証明書 `.n11` ＋ 15 検証JSON の45 fetch）のみから
決定的に判定した。検証の本体ではなく報告（provenance census）であり、
行の閉鎖・証明書内容の検証・既存正本の変更は一切行わない。

## 主な結果

- **全180 structural gate PASS**（15 receipt × 12 gate: ordinal連続
  eighteenth..thirty-second・singleton receipts・WIN8-D10・stones=8・
  root/raw_root_hex一致・repo path形式4種・自dir証明書SHA-256一致・
  自dir検証JSON SHA-256一致）。fetch・parse・gateの全失敗はfail-closed
  （出力未書込）。census正本 `c801564d…`（34,758 bytes）は同一cwd 5回＋
  隔離cwd/HOME＋`env -i`＋`PYTHONHASHSEED=random` 1回の計6実行で
  byte-identical。1実行約1.4秒。
- **IV.source_record分類: own 12 / stale 3**。staleは fold12（第19 receipt
  `8005021`・K1175 erratum対照と同一内容の機械的再確認）・fold15
  （第22 receipt `120000038`・K1179 erratum対照と同一内容）・**fold18
  （第25 receipt `00901010`・本censusによる新規発見）**の3例のみ。
  fold18 receiptのIV.source_recordはfold17証明抽出実験
  `n11-residual55-win8-cert-extract-root22081000-20261120`を指しており、
  正しくは自rootの `n11-residual48-win8-cert-extract-root00901010-20261120`
  を指すべきである。fold17/18/19/23/25の単体ext2は他レーンが宣言済みで
  あり、fold18のstaleはそれらへの事前通知として記録した
  （erratum判断・正本改変の権限は当該記録の所有者に留保される）。
- **コピー仮説の機械的裏付け（3/3）**: stale 3例すべて
  `iv_equals_previous_fold_iv = true` かつ
  `iv_dir_equals_previous_fold_own_dir = true`（fold12←fold11・
  fold15←fold14・fold18←fold17）。直前fold receiptのIV欄を写したと
  読める挙動が3/3で成立し、偶発の誤記説とは整合しない。
  receipt templateのsource_record欄がプレフィルされたまま出版される
  陳腐化パターン（K1175の指摘と同型）が系列全体で確認された。
- **certificate_source は15/15で清潔**: 全receiptの
  `certificate_source.record` は自rootの証明抽出実験dirを指し、
  `certificate_path` の実在byteのSHA-256がreceipt記載
  `certificate_sha256` に、自dir検証JSONのSHA-256が`verification_sha256`に、
  証明書bytes数が`certificate_bytes`に、それぞれ15/15で一致
  （`certificate_source_blocks_correct_count = 15`・IV参照dirは全15件で
  universe内）。clean 12 foldは
  fold11/13/14/16/17/19/20/21/22/23/24/25。
- **実験事実（出版前機械草案の破棄）**: 初版機械はroot末尾比較を整数比較で
  実装していたため出版前にreceipt-root suffix（末尾文字列）比較へ修正し、
  batteryを実施し直した（旧2案 sha256 `fec82a94…`→`e822f45c…` は未出版破棄。
  hint欄はname-level参考値でgate不依存）。fail-closed擬陽性は旧battery・
  新batteryとも0件。

## 位置づけ

- stale判定はprovenance上の記録誤り候補の報告であり、当該rootの証明書・
  検証の成否そのものを左右しない。fold18を含む全15 certificate・verification
  SHA参照は部品単位で機械照合済みで全て正しい。行は1行も閉じない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
  nodes数・solved数・coverage数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

part1 commit `d9d1bfa8`（実験dir `n11-win8-receipt-source-record-census-20261121/`
4ファイル・fetch-back 4/4 byte一致）。（2026-11-21）
