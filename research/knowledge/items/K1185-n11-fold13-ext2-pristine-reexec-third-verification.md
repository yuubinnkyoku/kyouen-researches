---
id: K1185
title: "K1176（fold13外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold13 ext2 pristine re-execution third verification root9840004"
  - "K1176検証機battery改変なし3巡×2環境実体・計6 finalize監査byte再現・隔離環境+PYTHONHASHSEED=random"
  - "第三検証harness監査正本 701bdfeb…・出版社監査正本 4fe40fa2… が6実行byte一致"
relations:
  - type: depends_on
    target: K1176
    note: "検証対象。出版byte 5点pin、W再構成2参照（12 Git blob + 16 SHA-256 = 28 pin + fold11/fold12/fold13の3 chain機・31ファイル）、検証機pristine再実行4回/battery×3、出版社監査正本 4fe40fa2…（81,632 bytes・gate 774）のbyte一致を再確認する。"
  - type: related
    target: K1184
    note: "fold12 ext2第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第二号。"
  - type: related
    target: K1174
    note: "fold20/K1173第三検証と同一の手続き系列。"
  - type: related
    target: K1172
    note: "fold29 cert-extract ext2/K1166第三検証と同一手続き系列。"
artifacts:
  - path: research/experiments/n11-fold13-ext2-pristine-reexec-third-verification-root9840004-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実4項・再現手順・限界"
  - path: research/experiments/n11-fold13-ext2-pristine-reexec-third-verification-root9840004-20261121/scripts/verify_k1176_fold13ext2_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 3ac21493…・18,746 bytes）"
  - path: research/experiments/n11-fold13-ext2-pristine-reexec-third-verification-root9840004-20261121/output/harness-audit.json
    role: audit
    note: "第三検証harness監査正本（6,668 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 701bdfeb…・2環境実体6実行byte一致）"
  - path: research/experiments/n11-fold13-ext2-pristine-reexec-third-verification-root9840004-20261121/output/reproduction.log
    role: record
    note: "時系列・battery 3巡×2環境実体の実行記録・環境リセット事故と完全再生成の記録・受入条件対照"
  - path: research/log/2026-11-21-n11-k1176-fold13-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 48c6c2c3…・宣言 2026-11-21T03:00Z・受入条件5項目）"
  - path: research/log/2026-11-21-n11-k1176-fold13-ext2-pristine-reexec-third-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照"
---

# K1176（fold13外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `48c6c2c3`・宣言 2026-11-21T03:00Z・宣言時HEAD `0af2ac83`・受入条件5項目）の下、
K1176（fold13 receipt fold・root `00000000000000003800000009840004`・第20 receipt・3番目WIN8 receipt foldの出版byteに対する
第三実装外部第二検証・出版社監査正本 `4fe40fa2…`〔81,632 bytes・gate 774〕）を、repo出版byteのみを素材に第三の実行環境から
完全再現し、その決定性・入力pin・fail-closed防衛を独立確認した。K1184（fold12/K1175第三）と同一手続き系列の、
fold12〜16単体ext2第二検証群への第三検証適用の第二号である。

## 主な結果

- **出版byte再pin**: K1176実験dir 5ファイル（README `28e40ce3…`・W再構成機 `1b54624f…`・第三実装検証機
  `aeda41e1…`〔57,284 bytes〕・外部監査正本 `4fe40fa2…`・reproduction.log `224272ee…`）をpin commit
  `51d86169`（part1最終・5ファイル出揃いcommit）からharness pin stageが自力取得しSHA-256+byte数10 gate PASS。
- **W再構成2参照**: 改変なしの `reconstruct_fold13_inputs.py` を ref_a `0af2ac83`（宣言時HEAD）と
  ref_b `48c6c2c3`（検証時main〔宣言commit〕）の両pinned refで実行し、W treeを2回再構成
  （12 Git blob pin + 16 SHA-256 pin = 28 pin + fold11機・fold12機・fold13機の3 chain機・計31ファイル・
  `diff -r W_A W_B` byte一致・fold11機入力pinのfold12⊂fold13部分集合連鎖を再構成機自身が機械確認）。
  api.github.com非依存（raw固定commit URLのみ）。
- **出版検証機pristine 4回/battery×3 battery**: `verify_fold13_external_20261121.py` を改変せず
  同一cwd 2回・隔離copytree W/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回で再実行し、
  **全回 rc=0・`ALL 774 GATES PASS`・出力監査JSONが出版正本 `4fe40fa2…` とbyte-identical**・
  gate count 774（ok:true総数・all_gates_pass true）・battery内4回間でもbyte一致
  （各回fold13機4回プリ実行・fold11/fold12機独立rerun・機内tamper 2件〔出版社試験offset〕込み・1回約28.5〜29.1秒）。
- **本レーン選択offsetのtamper 2件fail-closed**（battery毎2件・計6件+手動探針2件）: worklist `inputs/worklist.csv` @222999
  （blob pin）・K1108証明書 @1111444（sha256 pin）の1 byte XOR 0x01（出版社試験位置@117,777/@777,777、fold12第三検証レーン
  @150,000/@654,321、fold20/21/22/24第三検証・fold14-16 ext2各レーンのoffset群とすべて別位置・W隔離複写上
  （worklistは360,834 bytes・K1108証明書は1,640,220 bytes））がいずれも rc=1・`GATE FAILED [i]` ・監査未書込で捕捉。
  本番Wは両実施後に無改変再照合（worklist `6d8a449e…`・証明書 `5b114b9e…`）。
- **第三検証harnessの決定性**: `verify_k1176_fold13ext2_third_20261121.py`（18,746 bytes・stdlibのみ・stage分割）が
  battery 3巡（同一base 2巡は全stage再実行〔pin再取得込み〕・第3巡は隔離base+隔離cwd/HOME/TMPDIR+
  `PYTHONHASHSEED=random`）で監査正本 `701bdfeb…`（6,668 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・
  all_gates_pass true・時刻/絶対path/volatile排除）をbyte一致で生成。さらに実行環境リセット後の完全再生成
  battery 3巡も同一byteで、**2環境実体・計6 finalize監査がすべてbyte-identical**。

## 実験事実

1. **実行環境リセット事故が交叉環境のbyte決定性の非意図的実証となった**: battery 3巡完了直後に実行環境がリセットされ
   全ローカル成果物（pubfetch・W tree・battery成果物・harnessファイル）を喪失。harnessを記録済みソースからbyte数照合
   （18,746 = 18,746・再入力時の24 bytes余分行はbyte数照合が捕捉）つきで再構成し、battery 3巡をfresh baseで
   ゼロから完全再実行したところ、監査正本sha256はリセット前記録値 `701bdfeb…` とbyte一致。以後の出版物は再生成側を
   正本として出版（fetch-back 4/4 byte一致）。
2. **fold13検証機はn11検証ラティス内で最重量級**: gate 774・1回約28.5〜29.1秒（fold12機の約2倍）。W tree 31ファイル
   （fold13機pin 16個に増分・worklistはfold12と同一seriesファイル〔`6d8a449e…`・360,834 bytes〕の再利用）。
   1 batteryあたり約2.5分。
3. **出版検証機の内部scratchは絶対path固定**（`/home/user/work/f13ext/runs`）のためharnessは検証機実行を厳密に逐次化
   し、隔離実行（r3/r4）でも同一scratch pathが監査byteに影響しないことを実測した。
4. **api.github.com枯渇の影響圏外**: battery全stageはraw固定commit URLのみでapi.github.comを呼ばない。
   本セッションでapi quotaは403枯渇したが、pin・再構成・fetch-backはすべて待機ゼロで冪等完走した。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-k1176-fold13-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `48c6c2c3`・fetch-back byte一致）
- part1（実験dir 4ファイル・単一push_filesコミット）: commit `7943056f`・fetch-back 4/4 byte一致
  （harness `3ac21493…`・監査正本 `701bdfeb…`・reproduction.log `1bb1ae61…`）。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はK1176第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、行は1行も閉じない
（fold13時点残余65→62行は当該receiptの既出版簿記・pool 120,416根は不変）。WIN8-D10証明書は当該8石rootの
ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのままである。**
