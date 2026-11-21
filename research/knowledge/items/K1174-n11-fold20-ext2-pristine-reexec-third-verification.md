---
id: K1174
title: "K1173（fold20外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold20 ext2 pristine re-execution third verification root08d10000"
  - "K1173検証機battery改変なし3巡・出版監査byte再現・隔離環境+PYTHONHASHSEED=randomでの決定性確認"
  - "第三検証harness監査正本 24fac0b9…・出版社監査正本 5a9bb98f… が3実行byte一致"
relations:
  - type: depends_on
    target: K1173
    note: "検証対象。出版byte 5点pin、W再構成2参照（49 pin + chain機4台）、検証機pristine再実行4回、出版社監査正本 5a9bb98f…（128,175 bytes・gate 1,317）のbyte一致を再確認する。"
  - type: depends_on
    target: K1129
    note: "fold20 receipt fold正本（receipt 76fd255b…・出版機 9e141d4a…・生成機 4ba91cd0…・README 637841d2…）がpin・rerun gate・独立再計算の対象。"
  - type: depends_on
    target: K1121
    note: "K1121証明書本体（8513e366…・1,026,202 bytes）と19 gate監査（0088ebab…）がW pin・tamper・監査値再照合の対象。"
  - type: related
    target: K1165
    note: "fold24/K1164第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。"
  - type: related
    target: K1170
    note: "fold22/K1167第三検証と同一の手続き系列。"
  - type: related
    target: K1172
    note: "fold29 cert-extract ext2/K1166第三検証と同一の手続き系列。api.github.com quota枯渇の冪等復旧事例も共有。"
artifacts:
  - path: research/experiments/n11-fold20-ext2-pristine-reexec-third-verification-root08d10000-20261120/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実5項・再現手順・限界"
  - path: research/experiments/n11-fold20-ext2-pristine-reexec-third-verification-root08d10000-20261120/scripts/verify_k1173_fold20ext2_third_20261120.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 9cf2e6f9…・17,424 bytes）"
  - path: research/experiments/n11-fold20-ext2-pristine-reexec-third-verification-root08d10000-20261120/output/harness-audit.json
    role: audit
    note: "第三検証harness監査正本（6,213 bytes・gate 49〔pin 10・recon 12・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 24fac0b9…・3実行byte一致）"
  - path: research/experiments/n11-fold20-ext2-pristine-reexec-third-verification-root08d10000-20261120/output/reproduction.log
    role: record
    note: "時系列・battery 3巡の実行記録・実験事実（SHA-256 6ccf0ac7…・4,813 bytes）"
  - path: research/log/2026-11-20-n11-k1173-fold20-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 1d68addb…・宣言 2026-11-20T23:45:26Z・受入条件5項目）"
  - path: research/log/2026-11-21-n11-k1173-fold20-ext2-pristine-reexec-third-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照"

---

# K1173（fold20外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `1d68addb`・宣言 2026-11-20T23:45:26Z・宣言時HEAD `992851e2`・受入条件5項目）の下、
K1173（fold20 receipt fold・root `00000000000000003800000008d10000`・K1129出版byteの第三実装外部第二検証・
出版社監査正本 `5a9bb98f…`〔128,175 bytes・gate 1,317〕）を、repo出版byteのみを素材に第三の実行環境から
完全再現し、その決定性・入力pin・fail-closed防衛を独立確認した。K1165（fold24/K1164）・K1170（fold22/K1167）・
K1172（fold29 cert-extract/K1166）と同一手続き系列の、fold receipt外部第二検証への適用である。

## 主な結果

- **出版byte再pin**: K1173実験dir 5ファイル（README `66511c69…`・W再構成機 `bf21d042…`・第三実装検証機
  `30877bef…`〔52,131 bytes〕・外部監査正本 `5a9bb98f…`・reproduction.log `e3422428…`）をpin commit
  `cf453602`（part1修正commit）からharness pin stageが自力取得しSHA-256+byte数10 gate PASS。
- **W再構成2参照**: 改変なしの `reconstruct_fold20_inputs.py` を ref_a `992851e2`（宣言時HEAD）と
  ref_b `bb4d147b`（検証時main）の両pinned refで実行し、W treeを2回再構成（12 Git blob pin + 37
  SHA-256 pin = 49 pin + chain機4台・計53ファイル・`diff -r W_A W_B` byte一致・fold19機入力pin
  12+34の49 pin部分集合性を再構成機自身が機械確認）。
- **出版検証機pristine 4回**: `verify_fold20_external_20261120.py` を改変せず同一cwd 2回・隔離
  copytree W/cwd/HOME 1回（`env -i`・隔離HOME/TMPDIR）・隔離+`PYTHONHASHSEED=random` 1回で再実行し、
  **全回 rc=0・`ALL 1317 GATES PASS`・出力監査JSONが出版正本 `5a9bb98f…` とbyte-identical**・
  gate count 1,317（ok:true総数）・4回間でもbyte一致（各回fold19機pristine rerun gate→fold18
  preverified→K1120 gate群の推移的再検証込み・1回約20〜21秒）。
- **本レーン選択offsetのtamper 2件fail-closed**: worklist `inputs/worklist.csv` @7777（blob pin）・
  K1121証明書 @500000（sha256 pin）の1 byte XOR 0x01（出版社試験位置@5077/@28081と別位置・W隔離複写上）が
  いずれも rc=1・`GATE FAILED [i]` ・監査未書込で捕捉。本番Wは両実施後に無改変再照合
  （worklist `6d8a449e…`・証明書 `8513e366…`）。
- **第三検証harnessの決定性**: `verify_k1173_fold20ext2_third_20261120.py`（17,424 bytes・stdlibのみ・
  stage分割）がbattery 3巡（同一base 2巡は全stage再実行・第3巡は隔離base+隔離cwd/HOME+
  `PYTHONHASHSEED=random`）で監査正本 `24fac0b9…`（6,213 bytes・gate 49・all_gates_pass true・
  時刻/絶対path/volatile排除）を **3実行byte一致** で生成。per-stage partsはwall_msを意図的に保持し
  byte再現対象外（auditのみが正本）。

## 実験事実

1. api.github.com無認証quotaの共有IP枯渇がbattery中に再発（403 rate limit・battery 2巡目の recon ref_b
   中断）したが、参照は固定refのため再実行は冪等で、quota復旧後にbatteryを最初から3巡完走させた
   （K1167第三検証レーンの21:45Z枯渇と同じ失敗モード・出版物は再実行後のbatteryのみ）。
2. harness開発中に出版監査正本SHA-256の1文字誤挿入転写（`…ff27f4dc…`→`…ff277f4dc…`）を自pin stageが
   実行1回目で捕捉（打鍵定数はfail-closed pinで防ぐというK1158/K1160/K1164/K1170パターンの再実証）。
3. 初版finalizeがpartsを丸ごとauditに写し、毎回変動するwall_msフィールドが3実行byte一致を壊す設計に
   なっていたのを出版前に捕捉し、`*_not_in_audit` 接尾辞の再帰的除外で修正した。
4. 予備実行後に待機pollingが300秒bash上限を超過して実行環境がリセットされ、出版前の作業dir（予備
   4回・draft類）が消失した。宣言は出版済みでrepoが正本のため無被害。batteryは固定refから全成果を
   再取得・再実行する設計なので、復旧後にbattery 3巡を最初から完走させた（待機pollingは240秒以内に
   区切る教訓）。

## 出版

- 宣言ノート: `research/log/2026-11-20-n11-k1173-fold20-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `1d68addb`・宣言 2026-11-20T23:45:26Z・fetch-back byte一致）。
- part1（実験dir 4ファイル）: commit `a853b533`・fetch-back 4/4 byte一致。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はK1173第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、行は1行も
閉じない（fold20時点残余41→38行はK1129の既出版簿記・pool 120,416根は不変）。WIN8-D10証明書は当該
8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのままである。**
