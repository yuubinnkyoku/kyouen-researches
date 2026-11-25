---
id: K1187
title: "K1179（fold15外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold15 ext2 pristine re-execution third verification root120000038"
  - "K1179検証機battery改変なし3巡・出版監査byte再現・隔離環境+PYTHONHASHSEED=randomでの決定性確認"
  - "第三検証harness監査正本 cfb6879a…・出版社監査正本 6800759e… が3実行byte一致"
relations:
  - type: depends_on
    target: K1179
    note: "検証対象。出版byte 5点pin、W15再構成2参照（12 Git blob + 22 SHA-256 = 34 pin + fold11/fold12/fold13/fold14/fold15の5 chain機・39ファイル）、検証機pristine再実行4回/battery×3、出版社監査正本 6800759e…（101,443 bytes・gate 981）のbyte一致を再確認する。"
  - type: related
    target: K1186
    note: "fold14 ext2第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第四号。"
  - type: related
    target: K1185
    note: "fold13 ext2第三検証と同一手続き系列。"
  - type: related
    target: K1184
    note: "fold12 ext2第三検証と同一手続き系列。"
artifacts:
  - path: research/experiments/n11-fold15-ext2-pristine-reexec-third-verification-root120000038-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実4項・再現手順・限界"
  - path: research/experiments/n11-fold15-ext2-pristine-reexec-third-verification-root120000038-20261121/scripts/verify_k1179_fold15ext2_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 76cb4690…・19,208 bytes）"
  - path: research/experiments/n11-fold15-ext2-pristine-reexec-third-verification-root120000038-20261121/output/harness-audit.json
    role: audit
    note: "第三検証harness監査正本（6,858 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 cfb6879a8f2d97d478942c33973bcd87eb774abc15fe94f591ff537747185b7f・3実行byte一致）"
  - path: research/experiments/n11-fold15-ext2-pristine-reexec-third-verification-root120000038-20261121/output/reproduction.log
    role: record
    note: "時系列・battery 3巡の実行記録・受入条件対照"
  - path: research/log/2026-11-21-n11-k1179-fold15-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 04b4ed9d…・受入条件5項目）"
  - path: research/log/2026-11-21-n11-k1179-fold15-ext2-pristine-reexec-third-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照"
---

# K1179（fold15外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `04b4ed9d`・宣言時HEAD `b619261a`・受入条件5項目）の下、
K1179（fold15 receipt fold・root `00000000012000003800080009000000`〔root 120000038〕・第22 receipt・
5番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・出版社監査正本 `6800759e…`
〔101,443 bytes・gate 981〕）を、repo出版byteのみを素材に第三の実行環境から完全再現し、
その決定性・入力pin・fail-closed防衛を独立確認した。K1184（fold12）・K1185（fold13）・K1186（fold14）と
同一手続き系列の、fold12〜16単体ext2第二検証群への第三検証適用の第四号である。

## 主な結果

- **出版byte再pin**: K1179実験dir 5ファイル（README `20a2d104…`・W15再構成機 `7757cb51…`・
  第三実装検証機 `ade19de2…`〔62,390 bytes〕・外部監査正本 `6800759e…`・reproduction.log `579f178a…`）を
  pin commit `2e1bc1ea`（K1179 part1・5ファイル一括commit）からharness pin stageが自力取得し
  SHA-256+byte数10 gate PASS。
- **W15再構成2参照**: 改変なしの `reconstruct_fold15_inputs.py` を ref_a `b619261a`（宣言時HEAD）と
  ref_b `04b4ed9d`（検証時main〔宣言commit〕）の両pinned refで実行し、W15 treeを2回再構成
  （12 Git blob pin + 22 SHA-256 pin = 34 pin + fold11機・fold12機・fold13機・fold14機・fold15機の
  5 chain機・計39ファイル・`diff -r W_A W_B` byte一致・fold11機入力pinのfold12⊂fold13⊂fold14⊂fold15
  部分集合連鎖を再構成機自身が機械確認）。api.github.com非依存（raw固定commit URLのみ・6回の再構成すべて待機ゼロ）。
- **出版検証機pristine 4回/battery×3 battery**: `verify_fold15_external_20261121.py` を改変せず
  同一cwd 2回・隔離copytree W/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回で再実行し、
  **全12回 rc=0・`ALL 981 GATES PASS`・出力監査JSONが出版正本 `6800759e…` とbyte-identical**・
  gate count 981（ok:true総数・all_gates_pass true）・battery内4回間でもbyte一致
  （各回fold15機4回プリ実行・vr14 fold14機独立rerun・fold11/12/13機rerun・機内tamper 2件〔出版社試験offset〕込み・
  1回約106秒）。
- **本レーン選択offsetのtamper 2件fail-closed**（battery毎2件・計6件+手動探針2件）:
  worklist `inputs/worklist.csv` @277555（blob pin）・K1114証明書
  `k1114/certs/win8-root-00000000012000003800080009000000-20261120.n11` @877666（sha256 pin）の
  1 byte XOR 0x01（出版社試験位置@208,888/@919,191、fold12第三レーン@150,000/@654,321、fold13第三レーン
  @222,999/@1,111,444、fold14第三レーン@333,444/@999,111、fold20/21/22/24第三検証・fold16 ext2各レーンの
  offset群とすべて別位置・W隔離複写上（worklistは360,834 bytes・K1114証明書は1,171,958 bytes））が
  いずれも rc=1・`GATE FAILED [i]`・監査未書込で捕捉。本番Wは両実施後に無改変再照合
  （worklist `6d8a449e…`・証明書 `5a135903…`）。
- **第三検証harnessの決定性**: `verify_k1179_fold15ext2_third_20261121.py`（19,208 bytes・stdlibのみ・
  stage分割）がbattery 3巡（同一base 2巡は全stage再実行〔pin再取得込み〕・第3巡は隔離base+
  隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）で監査正本 `cfb6879a…`（6,858
  bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・時刻/絶対path/volatile排除）を
  **3実行byte一致**で生成。per-stage partsはwall_msを意図的に保持しbyte再現対象外
  （auditのみが正本）。

## 実験事実

1. **fold15検証機はfold14機の約2倍**: gate 981（fold14機は880）・1回約106秒（fold14機は約53秒）。
   W15 tree 39ファイル（fold11〜15の全5 chain機がWに入る初の規模）。1 battery約7分15秒。
2. **worklistはfold12/13/14第三レーンと同一seriesファイルの4レーン目の再利用**（`6d8a449e…`・360,834 bytes）で、
   第三検証レーンのtamper探針位置が4レーンで互いに別々（@150,000・@222,999・@333,444・@277,555）。
3. **出版検証機の内部scratchは絶対path固定**（`/home/user/work/f13ext/runs15`）のため、harnessは
   検証機実行を厳密に逐次化し、隔離実行（r3/r4）でも同一scratch pathが監査byteに影響しないことを
   実測した（fold14第三検証〔K1186〕と同一設計）。
4. **api.github.com枯渇の影響圏外**: 全stage（pin・recon含む）はraw固定commit URLのみで
   api.github.comを一度も呼ばず、待機ゼロの冪等運転だった（手動探針・fetch-backもapi非依存）。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-k1179-fold15-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `04b4ed9d`・fetch-back byte一致）
- part1（実験dir 4ファイル・単一push_filesコミット）: commit `7ed921fa`・fetch-back 4/4 byte一致
  （harness `76cb4690…`・監査正本 `cfb6879a…`・reproduction.log `c85cfc2b…`）。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はK1179第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、
行は1行も閉じない（fold15時点残余58→55行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのままである。**
