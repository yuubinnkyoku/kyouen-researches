---
id: K1186
title: "K1178（fold14外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold14 ext2 pristine re-execution third verification root9090022"
  - "K1178検証機battery改変なし3巡・出版監査byte再現・隔離環境+PYTHONHASHSEED=randomでの決定性確認"
  - "第三検証harness監査正本 717b7c9b…・出版社監査正本 fe6370f7… が3実行byte一致"
relations:
  - type: depends_on
    target: K1178
    note: "検証対象。出版byte 5点pin、W再構成2参照（12 Git blob + 19 SHA-256 = 31 pin + fold11/fold12/fold13/fold14の4 chain機・35ファイル）、検証機pristine再実行4回/battery×3、出版社監査正本 fe6370f7…（91,543 bytes・gate 880）のbyte一致を再確認する。"
  - type: related
    target: K1185
    note: "fold13 ext2第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的監査）。fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180)の第三検証の第三号。"
  - type: related
    target: K1184
    note: "fold12 ext2第三検証と同一手続き系列。"
  - type: related
    target: K1174
    note: "fold20/K1173第三検証と同一の手続き系列。"
artifacts:
  - path: research/experiments/n11-fold14-ext2-pristine-reexec-third-verification-root9090022-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・実験事実4項・再現手順・限界"
  - path: research/experiments/n11-fold14-ext2-pristine-reexec-third-verification-root9090022-20261121/scripts/verify_k1178_fold14ext2_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 2caa5516…・18,921 bytes）"
  - path: research/experiments/n11-fold14-ext2-pristine-reexec-third-verification-root9090022-20261121/output/harness-audit.json
    role: audit
    note: "第三検証harness監査正本（6,723 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 717b7c9b…・3実行byte一致）"
  - path: research/experiments/n11-fold14-ext2-pristine-reexec-third-verification-root9090022-20261121/output/reproduction.log
    role: record
    note: "時系列・battery 3巡の実行記録・受入条件対照"
  - path: research/log/2026-11-21-n11-k1178-fold14-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 369b0c30…・受入条件5項目）"
  - path: research/log/2026-11-21-n11-k1178-fold14-ext2-pristine-reexec-third-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照"
---

# K1178（fold14外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `369b0c30`・宣言時HEAD `eda86d47`・受入条件5項目）の下、
K1178（fold14 receipt fold・root `00000000000000909002200080100000`〔root 9090022〕・第21 receipt・
4番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・出版社監査正本 `fe6370f7…`
〔91,543 bytes・gate 880〕）を、repo出版byteのみを素材に第三の実行環境から完全再現し、
その決定性・入力pin・fail-closed防衛を独立確認した。K1184（fold12）・K1185（fold13）と
同一手続き系列の、fold12〜16単体ext2第二検証群への第三検証適用の第三号である。

## 主な結果

- **出版byte再pin**: K1178実験dir 5ファイル（README `0d3b4e06…`・W再構成機 `62a72b36…`・
  第三実装検証機 `d966dad5…`〔58,352 bytes〕・外部監査正本 `fe6370f7…`・reproduction.log `5d28aa0e…`）を
  pin commit `23de00dc`（K1178 part1・5ファイル一括commit）からharness pin stageが自力取得し
  SHA-256+byte数10 gate PASS。
- **W再構成2参照**: 改変なしの `reconstruct_fold14_inputs.py` を ref_a `eda86d47`（宣言時HEAD）と
  ref_b `369b0c30`（検証時main〔宣言commit〕）の両pinned refで実行し、W treeを2回再構成
  （12 Git blob pin + 19 SHA-256 pin = 31 pin + fold11機・fold12機・fold13機・fold14機の4 chain機・
  計35ファイル・`diff -r W_A W_B` byte一致・fold11機入力pinのfold12⊂fold13⊂fold14部分集合連鎖を
  再構成機自身が機械確認）。api.github.com非依存（raw固定commit URLのみ・6回の再構成すべて待機ゼロ）。
- **出版検証機pristine 4回/battery×3 battery**: `verify_fold14_external_20261121.py` を改変せず
  同一cwd 2回・隔離copytree W/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回で再実行し、
  **全12回 rc=0・`ALL 880 GATES PASS`・出力監査JSONが出版正本 `fe6370f7…` とbyte-identical**・
  gate count 880（ok:true総数・all_gates_pass true）・battery内4回間でもbyte一致
  （各回fold14機4回プリ実行・fold11/12/13機独立rerun・機内tamper 2件〔出版社試験offset〕込み・
  1回約53.1〜53.4秒）。
- **本レーン選択offsetのtamper 2件fail-closed**（battery毎2件・計6件+手動探針2件）:
  worklist `inputs/worklist.csv` @333444（blob pin）・K1109証明書
  `k1109/certs/win8-root-00000000000000909002200080100000-20261120.n11` @999111（sha256 pin）の
  1 byte XOR 0x01（出版社試験位置@200,222/@888,222、fold12第三レーン@150,000/@654,321、fold13第三レーン
  @222,999/@1,111,444、fold20/21/22/24第三検証・fold15/16 ext2各レーンのoffset群とすべて別位置・
  W隔離複写上（worklistは360,834 bytes・K1109証明書は1,082,873 bytes））がいずれも rc=1・
  `GATE FAILED [i]`・監査未書込で捕捉。本番Wは両実施後に無改変再照合
  （worklist `6d8a449e…`・証明書 `b8a15f9a…`）。
- **第三検証harnessの決定性**: `verify_k1178_fold14ext2_third_20261121.py`（18,921 bytes・stdlibのみ・
  stage分割）がbattery 3巡（同一base 2巡は全stage再実行〔pin再取得込み〕・第3巡は隔離base+
  隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）で監査正本 `717b7c9b…`（6,723 bytes・gate 53
  〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・時刻/絶対path/volatile排除）を
  **3実行byte一致**で生成。per-stage partsはwall_msを意図的に保持しbyte再現対象外
  （auditのみが正本）。

## 実験事実

1. **fold14検証機はfold13機の約1.8倍**: gate 880・1回53.1〜53.4秒（fold13機は774 gate・約29秒）。
   W tree 35ファイル（fold11〜14の全4 chain機がWに入る初の規模）。1 battery約4分20秒。
2. **worklistはfold12/13/14の3レーン連続同一series再利用**（`6d8a449e…`・360,834 bytes）で、
   第三検証レーンのtamper探針位置が3レーンで互いに別々（@150,000・@222,999・@333,444）。
3. **出版検証機の内部scratchは絶対path固定**（`/home/user/work/f13ext/runs14`）のため、harnessは
   検証機実行を厳密に逐次化し、隔離実行（r3/r4）でも同一scratch pathが監査byteに影響しないことを
   実測した。
4. **api.github.com枯渇の影響圏外**: 全stage（pin・recon含む）はraw固定commit URLのみで
   api.github.comを一度も呼ばず、待機ゼロの冪等運転だった（手動探針・fetch-backもapi非依存）。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-k1178-fold14-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `369b0c30`・fetch-back byte一致）
- part1（実験dir 4ファイル・単一push_filesコミット）: commit `4f869535`・fetch-back 4/4 byte一致
  （harness `2caa5516…`・監査正本 `717b7c9b…`・reproduction.log `608a7674…`）。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はK1178第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、
行は1行も閉じない（fold14時点残余62→58行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのままである。**
