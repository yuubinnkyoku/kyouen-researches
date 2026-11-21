---
id: K1189
title: "fold10（第17 WIN7 receipt fold外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold10 17th WIN7 receipt ext2 pristine re-execution third verification root00004000000000821082000000000100"
  - "WIN7 receipt fold系初の第三検証（出版byte 3点pin・W 3点2参照・検証機31 gate battery 3巡byte一致）"
  - "第三検証harness監査正本 2a97d052…（56 gate）・出版社監査正本 a62d6d50… が3実行byte一致"
relations:
  - type: depends_on
    target: K1071
    note: "検証対象の大もと。fold10（第17 WIN7-D10 receipt fold・root 00004000000000821082000000000100）の外部第二検証（K番号なしのext2出版・commit 452af0c5cc91a195dd24f4e4086af9bba11e807f・実験dir n11-seventeenth-receipt-fold-second-verification-20261120・31 gate全PASS）を第三の実行環境からpristine再実行する。出版byte 3点pin・W 3点（fold10正本/fold9正本/第17証明書）2参照・検証機pristine 4回/battery×3・出版社監査正本 a62d6d50…（5,410 bytes）のbyte一致を再確認する。"
  - type: related
    target: K1070
    note: "第17 WIN7-D10証明書（root …0100・1,791,541 bytes・SHA-256 21dd2f0e…）。本第三検証のW入力かつtamper探針t2の対象。"
  - type: related
    target: K1188
    note: "fold16 ext2第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。fold12〜16群に続き、WIN7 receipt fold系ext2では初号。"
  - type: related
    target: K1184
    note: "同系列第三検証（fold12）。本シリーズの初号で確立したstage分割・battery方式の直接の後継。"
  - type: related
    target: K1174
    note: "fold20 ext2第三検証。実験dirのREADME形式・受入条件形式の原型。"
artifacts:
  - path: research/experiments/n11-fold10-ext2-pristine-reexec-third-verification-root00000100-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実4項・再現手順・限界"
  - path: research/experiments/n11-fold10-ext2-pristine-reexec-third-verification-root00000100-20261121/scripts/verify_fold10ext2_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 cb0af4ab…・19,782 bytes）"
  - path: research/experiments/n11-fold10-ext2-pristine-reexec-third-verification-root00000100-20261121/output/fold10ext2-third-harness-audit.json
    role: audit
    note: "第三検証harness監査正本（10,980 bytes・gate 56〔pin 6・recon 15・rerun 24・tampers 11〕・all_gates_pass true・SHA-256 2a97d052bd1f0de95331f6d2b62322b61b38af326743a3dc244e4064a9abd7aa・3 battery byte一致）"
  - path: research/experiments/n11-fold10-ext2-pristine-reexec-third-verification-root00000100-20261121/output/reproduction.log
    role: record
    note: "battery 3巡の実行記録（3,483 bytes・SHA-256 7166137a…）"
  - path: research/log/2026-11-21-n11-fold10-17threceipt-ext2-pristine-reexec-third-single-owner-note.md
    role: declaration
    note: "単一オーナー宣言ノート（commit 4987c2b7…・受入条件5項目）"
  - path: research/log/2026-11-21-n11-fold10-17threceipt-ext2-pristine-reexec-third-single-owner-note-addendum.md
    role: declaration
    note: "受入条件4 t1予測の修正addendum（commit 274e3e28…・battery前に所有者が修正・宣言ノート本体byte不変）"
  - path: research/log/2026-11-21-n11-fold10-17threceipt-ext2-pristine-reexec-third-verification.md
    role: record
    note: "研究log（発見順・判断・失敗記録）"
---

# K1189（fold10=第17 WIN7 receipt ext2第三検証）

担当: n11長期レーン。単一オーナー宣言（commit `4987c2b7…`・受入条件5項目）+ t1期待値修正addendum（commit `274e3e28…`・battery前）の下で実施。

## 検証対象

fold10（root `00004000000000821082000000000100`・第17 WIN7-D10 receipt fold・K1071）の外部第二検証。
K番号をもたないext2出版（commit `452af0c5cc91a195dd24f4e4086af9bba11e807f`・2026-11-19T21:11:45Z単一コミット・
実験dir `research/experiments/n11-seventeenth-receipt-fold-second-verification-20261120/`・
README `240c8e58…`〔3,982 bytes〕/検証機 `7178fbe5…`〔11,145 bytes・純stdlib・31 gate・チェーン入力非依存〕/
出版監査正本 `a62d6d50…`〔5,410 bytes・status second-verified〕）を、出版社レーン以外の第三の実行環境（本sandbox）が
出版byteのみから再取得してpristine再実行・tamper・byte決定性を第三検査する。
n11検証ラティスの第三検証確定済み群（fold12〜16〔K1184〜K1188〕・fold20〔K1174〕・fold21〔K1168第三〕・
fold22〔K1170〕・fold24〔K1165〕・fold29 cert-extract〔K1172〕・residual23系）に続き、
**WIN7 receipt fold系ext2の第三検証はこのKが初号**。fold11/17/18/19/23/25/26 ext2は宣言済み他レーンのため対象外。

## 主結果

- pin stage（6 gate）: 対象ext2 3ファイルをpin commit `452af0c5…` からraw固定URL取得・SHA-256+byte数照合、
  3点とも出版値どおり（api.github.com非依存）。
- recon stage（15 gate）: W 3入力（fold10正本 `bed7d331…`〔12,918 bytes〕・fold9正本 `24db2352…`〔24,399 bytes〕・
  第17証明書 `21dd2f0e…`〔1,791,541 bytes〕）を2参照（ref_a = 宣言時HEAD `dcc5b962…`・ref_b = 宣言commit `4987c2b7…`）
  のraw固定URLから取得し、各SHA-256が検証機内pinと一致・2参照間byte-identical・検証機の固定絶対path配置後に再照合。
- rerun stage（24 gate）: 出版検証機を改変なしpristine再実行4回/battery×3（同一cwd 2回・隔離copytree cwd+`env -i`
  隔離HOME/TMPDIR 1回・隔離+`PYTHONHASHSEED=random` 1回）。全回 rc=0・出力監査JSON
  （gate 31・all pass・status second-verified・schema `n11-fold10-second-verification-20261120-v1`・
  `inputs_verified_by_sha256` 3点がW pinと一致）が出版正本 `a62d6d50…` とbyte-identical・battery内4回間でもbyte一致
  （検証機1回約1秒）。
- tampers stage（11 gate）: 本レーン選択offsetの1 byte XOR 0x01（既知の全レーン探針位置
  @{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/
  {7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}/{5077,28081}/{208,888,919,191}/{300,111,740,321}
  のいずれとも別位置）:
  - t1 fold10正本 @12,345 → rc≠0・監査は `status gate-failed` で書込・失敗gateはちょうど
    `fold10 正本 sha256 == published bed7d331...` の1件のみ（証明書SHA pin gate含む他30 gate全pass）。
  - t2 第17証明書 @1,234,567 → rc≠0・監査は `status gate-failed`・失敗gateはちょうど
    `cert sha256 pin matches local byte-exact file` の1件のみ（fold10 SHA pin gateはpass）。
  - いずれも実施後にW復帰・byte無改変再照合。**2種の入力pin gateが互いに独立して発火する**ことを1 battery内で実証。
- finalize: harness監査正本（10,980 bytes・gate 56〔pin 6・recon 15・rerun 24・tampers 11〕・all_gates_pass true・
  時刻/絶対path/volatile排除・解釈ガード5文+unknown guard）が3 battery（fresh base全stage・同一base全stage再実行・
  隔離base+`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`）でbyte一致（SHA-256 `2a97d052…`・battery 1巡約0.9秒）。

## 実験事実

1. **t1予測の誤りをbattery前にaddendumで修正**: 宣言ノート初版t1予測（「json load失敗・監査未書込」）は
   @12,345がfold10正本のメタデータ文字列 `_against_published_verdict_uni…` 内部でparse survivalする点で誤り
   （予備探針で判明）。実際は「対象入力のSHA-256 pin gateが単独失敗・他30 gate全pass・監査は`gate-failed`で書込」
   の精密なfail-closedであり、所有者addendum（commit `274e3e28…`）で予測を修正してからbatteryを実施した。
   誤った予測のままbatteryを実施せず、batteryは修正後のものだけを正本とした。
2. **n11検証ラティス最小級の第三検証対象**: 検証機1回約1秒・W再構成はraw pinned 3点取得のみ・
   battery 1巡約0.9秒×3巡（fold12〜16第三検証の1回約14.4〜215.3秒と対照）。
3. 監査byteの環境非依存決定性（隔離cwd/HOME/TMPDIR・`PYTHONHASHSEED=random`でbyte不変）を第三実装・第三環境から確認。

## 位置づけと限界

本検証はfold10外部第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、
receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない。
WIN7-D10証明書は当該7石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
