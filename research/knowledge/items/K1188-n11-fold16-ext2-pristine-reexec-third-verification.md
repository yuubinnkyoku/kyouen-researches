---
id: K1188
title: "K1180（fold16外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold16 ext2 pristine re-execution third verification root8890020"
  - "K1180検証機battery改変なし3巡・出版監査byte再現・隔離環境+PYTHONHASHSEED=randomでの決定性確認"
  - "第三検証harness監査正本 37154fa9…・出版社監査正本 09f80902… が3実行byte一致"
relations:
  - type: depends_on
    target: K1180
    note: "検証対象。出版byte 5点pin、W16再構成2参照（12 Git blob + 25 SHA-256 = 37 pin + fold11/fold12/fold13/fold14/fold15/fold16の6 chain機・43ファイル）、検証機pristine再実行4回/battery×3、出版社監査正本 09f80902…（108,139 bytes・gate 1061）のbyte一致を再確認する。"
  - type: related
    target: K1187
    note: "fold15 ext2第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第五号。"
  - type: related
    target: K1186
    note: "fold14 ext2第三検証と同一手続き系列。"
  - type: related
    target: K1185
    note: "fold13 ext2第三検証と同一手続き系列。"
  - type: related
    target: K1184
    note: "fold12 ext2第三検証と同一手続き系列。"
artifacts:
  - path: research/experiments/n11-fold16-ext2-pristine-reexec-third-verification-root8890020-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実5項・再現手順・限界"
  - path: research/experiments/n11-fold16-ext2-pristine-reexec-third-verification-root8890020-20261121/scripts/verify_k1180_fold16ext2_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 c0b0aec7…・19,261 bytes）"
  - path: research/experiments/n11-fold16-ext2-pristine-reexec-third-verification-root8890020-20261121/output/harness-audit.json
    role: audit
    note: "第三検証harness監査正本（6,958 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 37154fa95b75d4c2e2c1ff822bd996640540d48907d370799ca5d295da3f3475・3実行byte一致）"
  - path: research/experiments/n11-fold16-ext2-pristine-reexec-third-verification-root8890020-20261121/output/reproduction.log
    role: record
    note: "時系列・battery 3巡の実行記録・受入条件対照"
  - path: research/log/2026-11-21-n11-k1180-fold16-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 65653082…・受入条件5項目）"
  - path: research/log/2026-11-21-n11-k1180-fold16-ext2-pristine-reexec-third-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照"
---

# K1180（fold16外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `65653082`・宣言時HEAD `4cf3144e`・受入条件5項目）の下、
K1180（fold16 receipt fold・root `00000000010000889002000080100000`〔root 8890020〕・第23 receipt・
6番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証）の出版byte 5点を
第三の実行環境でpristine再実行し、入力pin・byte決定性・fail-closed防衛を第三検査した。
fold12〜16単体ext2第二検証群の第三検証の第五号（K1184/K1185/K1186/K1187に続く）であり、
fold12〜16で全5号が完了した。

## 主結果

- 出版実験dir 5ファイルのpin stage（10 gate）: pin commit `056b8470`（K1180 part1・5ファイル一括）
  からraw固定URL取得・SHA-256+byte数照合、5点とも出版値どおり。
- W16再構成2参照（recon stage 16 gate）: 再構成機 `c70cbc45…` をref_a `4cf3144e`（宣言時HEAD）・
  ref_b `65653082`（宣言commit）の両参照で改変なし実行。W16 treeは各回43ファイル
  （12 Git blob + 25 SHA-256 = 37 pin + fold11〜fold16の6 chain機）で
  fold11機pin（12+10）⊂fold12機（12+13）⊂fold13機（12+16）⊂fold14機（12+19）⊂fold15機（12+22）⊂
  fold16機（12+25）の部分集合連鎖が機械確認され、`diff -r` byte一致。
  api.github.com非依存（raw固定commit URLのみ）。
- 検証機pristine再実行4回/battery×3（rerun stage 19 gate）: 第三実装検証機
  `32917945…`（61,627 bytes・gate 1061）をbattery 3巡で各4回・計12回
  （同一cwd 2回・隔離copytree W/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回）pristine実行。
  全回 rc=0・`ALL 1061 GATES PASS` 行・出力監査JSONが出版正本 `09f80902…`（108,139 bytes）と
  byte-identical・4回間でもbyte一致。1回約209.0〜215.3秒
  （機内のfold16機4回プリ実行・vr15 fold15機独立rerun・fold11/12/13/14機rerun・
  機内tamper 2件〔出版社試験offset @300,111/@740,321〕込み）。
- 本レーン選択offset tamper 2件（tampers stage 8 gate）: worklist `inputs/worklist.csv`
  @351,111（blob pin gate）・K1113証明書
  `k1113/certs/win8-root-00000000010000889002000080100000-20261120.n11` @611,222（sha256 pin gate）
  の1 byte XOR 0x01が、出版社試験位置 @300,111/@740,321・fold12/13/14/15第三検証レーン
  @{150,000,654,321}/@{222,999,1,111,444}/@{333,444,999,111}/@{277,555,877,666}・
  fold20/21/22/24第三検証群 @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}
  とすべて別位置で、いずれもreturncode≠0・`GATE FAILED [i]`・監査未書込でfail-closed捕捉
  （本番Wは無改変を事後再照合）。
- 第三検証harness監査正本のbyte決定性: finalize stage（gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・
  all_gates_pass true・解釈ガード5文）が3実行（同一base全stage再実行2回+隔離base/隔離cwd/HOME/TMPDIR+
  `PYTHONHASHSEED=random` 1回）でbyte一致（SHA-256 `37154fa9…`）。
  時刻・絶対path・実行時間（volatile）を含まない設計。

## 位置づけと限界

本検証はK1180第二検証の再現性・入力pin・監査byteの第三検査であり、receiptの再発行・
行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない
（fold16時点残余55→51行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
