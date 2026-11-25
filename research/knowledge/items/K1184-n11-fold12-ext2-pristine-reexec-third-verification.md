---
id: K1184
title: "K1175（fold12外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold12 ext2 pristine re-execution third verification root8005021"
  - "K1175検証機battery改変なし3巡・出版監査byte再現・隔離環境+PYTHONHASHSEED=randomでの決定性確認"
  - "第三検証harness監査正本 06750caa…・出版社監査正本 c309d693… が3実行byte一致"
relations:
  - type: depends_on
    target: K1175
    note: "検証対象。出版byte 5点pin、W再構成2参照（25 pin + fold11/fold12両chain機・27ファイル）、検証機pristine再実行4回/battery×3、出版社監査正本 c309d693…（70,149 bytes・gate 655）のbyte一致を再確認する。"
  - type: related
    target: K1174
    note: "fold20/K1173第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第一号。"
  - type: related
    target: K1172
    note: "fold29 cert-extract ext2/K1166第三検証と同一手続き系列。api.github.com枯渇時の冪等復旧設計と対照に、本batteryはraw固定commit URLのみでapi.github.com非依存。"
  - type: related
    target: K1170
    note: "fold22/K1167第三検証と同一手続き系列。"
artifacts:
  - path: research/experiments/n11-fold12-ext2-pristine-reexec-third-verification-root8005021-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実4項・再現手順・限界"
  - path: research/experiments/n11-fold12-ext2-pristine-reexec-third-verification-root8005021-20261121/scripts/verify_k1175_fold12ext2_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 c6f71b07…・18,624 bytes）"
  - path: research/experiments/n11-fold12-ext2-pristine-reexec-third-verification-root8005021-20261121/output/harness-audit.json
    role: audit
    note: "第三検証harness監査正本（6,587 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 06750caa…・3実行byte一致）"
  - path: research/experiments/n11-fold12-ext2-pristine-reexec-third-verification-root8005021-20261121/output/reproduction.log
    role: record
    note: "時系列・battery 3巡の実行記録・受入条件対照"
  - path: research/log/2026-11-21-n11-k1175-fold12-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 4c7a12f1…・宣言 2026-11-21T02:50Z・受入条件5項目）"
  - path: research/log/2026-11-21-n11-k1175-fold12-ext2-pristine-reexec-third-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照"
---

# K1175（fold12外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `4c7a12f1`・宣言 2026-11-21T02:50Z・宣言時HEAD `91f2f0f1`・受入条件5項目）の下、
K1175（fold12 receipt fold・root `00000000000000003800000008005021`・第19 receipt・2番目WIN8 receipt foldの出版byteに対する
第三実装外部第二検証・出版社監査正本 `c309d693…`〔70,149 bytes・gate 655〕）を、repo出版byteのみを素材に第三の実行環境から
完全再現し、その決定性・入力pin・fail-closed防衛を独立確認した。K1165（fold24/K1164）・K1170（fold22/K1167）・
K1172（fold29 cert-extract/K1166）・K1174（fold20/K1173）・K1168第三検証（fold21 ext2）と同一手続き系列の、
fold12〜16単体ext2第二検証群への第三検証適用の第一号である。

## 主な結果

- **出版byte再pin**: K1175実験dir 5ファイル（README `d1eae779…`・W再構成機 `caa30f34…`・第三実装検証機
  `43afc1cd…`〔53,934 bytes〕・外部監査正本 `c309d693…`・reproduction.log `d85d8c3d…`）をpin commit
  `adb1e8f605`（part1最終・5ファイル出揃いcommit）からharness pin stageが自力取得しSHA-256+byte数10 gate PASS。
- **W再構成2参照**: 改変なしの `reconstruct_fold12_inputs.py` を ref_a `91f2f0f1`（宣言時HEAD）と
  ref_b `4c7a12f1`（検証時main〔宣言commit〕）の両pinned refで実行し、W treeを2回再構成
  （12 Git blob pin + 13 SHA-256 pin = 25 pin + fold11機 `9b3e06c8…`・fold12機 `706bfa7a…`・計27ファイル・
  `diff -r W_A W_B` byte一致・fold11機入力pin 12+10の25 pin部分集合性・値一致を再構成機自身が機械確認）。
  api.github.com非依存（raw固定commit URLのみ・6回の再構成すべて待機ゼロ）。
- **出版検証機pristine 4回/battery×3 battery**: `verify_fold12_external_20261121.py` を改変せず
  同一cwd 2回・隔離copytree W/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回で再実行し、
  **全12回 rc=0・`ALL 655 GATES PASS`・出力監査JSONが出版正本 `c309d693…` とbyte-identical**・
  gate count 655（ok:true総数・all_gates_pass true）・battery内4回間でもbyte一致
  （各回fold12機4回プリ実行・fold11機独立rerun・機内tamper 2件〔出版社試験offset〕込み・1回約14〜15秒）。
- **本レーン選択offsetのtamper 2件fail-closed**（battery毎2件・計6件）: worklist `inputs/worklist.csv` @150000
  （blob pin）・K1106証明書 @654321（sha256 pin）の1 byte XOR 0x01（出版社試験位置@96,300/@456,789 と、
  fold20/21/22/24第三検証・fold13-16 ext2各レーンのoffset群とすべて別位置・W隔離複写上（worklistは360,834 bytes・
  K1106証明書は945,298 bytes））がいずれも rc=1・`GATE FAILED [i]` ・監査未書込で捕捉。
  本番Wは両実施後に無改変再照合（worklist `6d8a449e…`・証明書 `69f32661…`）。
- **第三検証harnessの決定性**: `verify_k1175_fold12ext2_third_20261121.py`（18,624 bytes・stdlibのみ・stage分割）が
  battery 3巡（同一base 2巡は全stage再実行〔pin再取得込み〕・第3巡は隔離base+隔離cwd/HOME/TMPDIR+
  `PYTHONHASHSEED=random`・各battery約60〜62秒）で監査正本 `06750caa…`（6,587 bytes・gate 53
  〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・時刻/絶対path/volatile排除）を
  **3実行byte一致** で生成。per-stage partsはwall_msを意図的に保持しbyte再現対象外（auditのみが正本）。

## 実験事実

1. **harness初版の転写誤りを自レーンpin gateが捕捉**:FILES表の検証機SHA-256に1文字の誤植
   （正 `…43afc1cd31d5d73185…` に対し `…31d5f73185…`）があり、pin stageの実測値照合が即 `STAGE FAILED [pin]`
   で捕捉した（K1158/K1160/K1164/K1170/K1174パターンの再実証・出版物は無被害・修正後にbatteryを最初からやり直し）。
2. **fold12第二検証batteryはn11検証ラティス中最軽量級**: 検証機1回約14〜15秒（fold20第三の約21秒・fold22の約34秒と
   対照）。W tree 27ファイル（fold20の53ファイルと対照的）。1 battery約60秒で、第三検証の再実行コストが低いことが
   実測確定した。
3. **出版検証機の内部scratchは絶対path固定**（`/home/user/work/f12ext/runs`）のため、harnessは検証機実行を
   厳密に逐次化した（並行実行によるscratch競合の発生条件を排除・audit byteへの影響なし・出版機の設計変更は非目標）。
4. **api.github.com枯渇の影響圏外**: 本batteryの全stage（pin・recon含む）はraw固定commit URLのみでapi.github.comを
   一度も呼ばず、K1175出版社のquota枯渇経験（監査logに記録）とは対照的に第三環境では待機ゼロで冪等完走した。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-k1175-fold12-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `4c7a12f1`・fetch-back byte一致）
- part1（実験dir 4ファイル・単一push_filesコミット）: commit `bf504135`・fetch-back 4/4 byte一致
  （harness `c6f71b07…`・監査正本 `06750caa…`）。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はK1175第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、行は1行も閉じない
（fold12時点残余68→65行は当該receiptの既出版簿記・pool P⁗ 120,416根は不変）。WIN8-D10証明書は当該8石rootの
ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのままである。**
