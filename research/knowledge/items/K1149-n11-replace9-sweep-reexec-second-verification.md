---
id: K1149
kind: computation
status: computed
title: K1146代替9根depth-10掃引の全probe再実行による独立第二検証: 24/24 gate PASS・passA/passB双方18/18 probe完全一致・pristine再assemble byte-identical・knowledge READMEのSHA-256転写ミス1件をfail-closed pinが捕捉（行閉鎖0）
topics: [search-methods, certificates, verification]
aliases:
  - full re-execution second verification of the K1146 replace-9 depth-10 sweep (the K1144 protocol applied to the replace-9 lane): all 18 published probes (9 roots x both AND orderings) re-run with the repo-pinned runner v17 (git blob c132cc64…) in two passes — pass A in this tree, pass B in an isolated cwd/HOME/input-copy tree
  - both passes match the published records 18/18 on nodes/loss/capped/terminalStoneRange (nodes totals 3,574,172 == published in each pass); fresh classification reproduces WIN8-D10 candidate 00000000010000809002000040002001 plus REFUTED-D10 8 roots with zero inter-ordering conflicts; pilot_d6 control passes 36/36 probes
  - pristine re-assembly: the published K1146 sweep machine re-executed in an isolated tree on the published probe records reproduces the published volume JSON byte-identically (SHA-256 e8f5d674…bf3eebf…, 20/20 gates); the audit master itself is byte-identical across 3 assembly runs in 2 environments
relations:
  - type: verifies
    target: K1146
    note: 代替9根掃引の出版probe事実（18 probes・分類pin・nodes総計3,574,172・terminal石数union [14,18]）の全件再実行と、出版掃引機械pristine再assembleによるbyte-identical確認
  - type: depends_on
    target: K1097
    note: scope1 greedy_selection（9根・gained/covered rows）からのprobe計画再導入とK1097帳簿crosscheck（per_row_residual23・scope1==scope2同一選定）の入力
  - type: depends_on
    target: K1095
    note: 残余23行（WIN3根主張7行+REFUTED9根主張23行）の連鎖再導入元
  - type: depends_on
    target: K1091
    note: 残余30行の連鎖再導入元
  - type: depends_on
    target: K1089
    note: 残余40行の連鎖再導入元
  - type: depends_on
    target: K1086
    note: 残余49行の連鎖再導入元
  - type: depends_on
    target: K1085
    note: 残余72行base state・入力正本pin鎖の起点
artifacts:
  - path: research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/README.md
    role: document
    note: 実験README（目的・プロトコル・24 gate・pristine再assemble・入力pin・解釈規約）
  - path: research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/scripts/verify_replace9_reexec_20261120.py
    role: verifier
    note: 検証機（41,175 bytes・SHA-256 77cdd9e3…・run/assemble・24 gate・乱数・時刻・環境依存出力なし・resume-safe）
  - path: research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/runner_v17.ts
    role: verifier
    note: runner v17 repo原本固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・出版実験と同一byte）
  - path: research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/output/probe-records-reexec-passA.jsonl
    role: data
    note: pass A再実行18 probe記録（8,336 bytes・pilot_d6制御つき）
  - path: research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/output/probe-records-reexec-passB.jsonl
    role: data
    note: pass B再実行18 probe記録（8,337 bytes・隔離tree実行）
  - path: research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/output/replace9-sweep-reexec-second-verification-20261120.json
    role: data
    note: 監査正本（SHA-256 27fc420c…・11,242 bytes・24/24 gate PASS・3実行byte-identical・interpretation_guard 6文言同梱）
  - path: research/log/2026-11-20-n11-replace9-sweep-reexec-second-verification.md
    role: log
    note: 実行記録（宣言参照・実行経緯・SHA転写ミス捕捉の記録・次回への引継ぎ）
  - path: research/log/2026-11-20-n11-residual72-replace9-d10-sweep-reexec-second-verification-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit 3f340466218bb47a08d1f7421947ff720bc52b85・先行出版）
scope: >-
  K1146代替9根depth-10掃引（commit e9ea153bc4出版）の出版probe事実のみを対象とする
  全件再実行第二検証。出版spot-check 4 probesを18 probes（9根×両AND順序）へ拡張し、
  runner v17（git blob pin）・depth 10・cap 30M・timeout 280s・pilot_d6制御必須で
  pass A（本tree）とpass B（隔離cwd/HOME/入力複写tree）を再実行、決定性字段
  （nodes/loss/capped/terminalStoneRange）を出版記録・出版正本per_rootと全件照合する。
  残余23行宇宙はK1085→K1086→K1089→K1091→K1095の連鎖から本検証機内の独立実装で
  再導入し、9根被覆幾何（popcount8・quadruple-free Bareiss・D4 min-canonical・
  exactly-once被覆・gains {3:6,2:2,1:1}・child=root−最小セットビット）を再検査する。
  出版掃引機械のpristine再assemble byte一致を含む。行の閉鎖claim・receipt fold・
  証明書抽出・新規probeは対象外。REFUTED-D10はLOSS証明ではなく、node数・solved数を
  勝敗として読まない。
evidence: >-
  （1）入力pin鎖: 上流6正本（K1085 5fdd342d…・K1086 3045e152…・K1089 808fbda1…・
  K1091 edd7ac84…・K1095 335eca5e…・K1097 2896deb0…）とK1146出版2正本
  （掃引volume e8f5d674…・probe-records JSONL bdacf0e7…）の計8 SHA-256 pinと
  掃引機械pin（d163b2a1…）・runner git blob pin（c132cc64…）が全て実byteと一致。
  （2）pass A: 18/18 probeでnodes/loss/capped/terminalStoneRangeが出版記録と全件一致
  （nodes総計3,574,172==出版値・capped 0・error 0・pilot_d6 18/18 PASS）。
  fresh再分類はWIN8-D10 candidate `00000000010000809002000040002001` ただ1根
  （両順序uncapped loss=true・nodes 608,293/691,784）+REFUTED-D10 8根・
  順序間矛盾0で出版分類pin全てと一致（実行約13.0秒・4 worker）。
  （3）pass B: 隔離cwd/HOME・入力複写の別treeで同一18 probes（約12.7秒）。
  passA vs passBの決定性字段不一致0・出版との18/18一致もpass Aと同一。
  （4）残余23行連鎖再導入: 72→49→40→30→23の各段でdistinct/disjoint/union partition
  検査全PASS・K1097帳簿crosscheck（per_row_residual23一致・scope1==scope2同一選定）PASS。
  9根被覆幾何（popcount8・4x4 Bareiss exact行列式によるquadruple-free・D4 min-canonical・
  23行exactly-once・gains {3:6,2:2,1:1}・gained==len covered・child=root−最小セットビット）
  再実装で全数検査PASS。
  （5）pristine再assemble: 出版掃引機械を隔離treeで出版probe-records入力により再実行し
  20/20 gate・出力が出版正本とbyte-identical（出版機械・出版記録・入力pin鎖の健全性を
  隔離環境で全再検証）。
  （6）監査正本: 24/24 gate PASS・同一cwd 2回＋隔離cwd/HOME別tree 1回の3実行で
  byte-identical（SHA-256 27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072・
  11,242 bytes）。
  （7）転写ミス捕捉: knowledge READMEのK1146 bulletに掃引正本SHA-256の1文字転写
  （…bf3eefbf…・正しくは…bf3eebf…）があったのを、本検証機のfail-closed pin
  （SHAを正本実byteから再計算して突き合わせ）が捕捉した。出版実験README・K1146 item・
  監査正本の値は正しく、誤りはREADME bulletの転写のみ（本次回のREADME更新で修正）。
  本検証は行を1行も閉じない。REFUTED-D10 は LOSS 証明ではなく、nodes数・solved数を勝敗と
  して読まない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。残余23行は全行open。

---

## 詳細

単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-d10-sweep-reexec-second-verification-single-owner-note.md`
（commit `3f340466218bb47a08d1f7421947ff720bc52b85`・先行出版）の下で、
[K1146代替9根depth-10掃引実験](../../experiments/n11-residual72-replace9-d10-sweep-20261120/README.md)
の出版probe事実の全件再実行第二検証を実施した。K1144が上流4掃引（132 probes）に対して確立した
プロトコルの replace9 版である: 出版時spot-checkは18 probes中4件だったため、残り14件を含む
全18 probesを、出版実験と同一byteのrunner v17（git blob pin）でdepth 10・cap 30M・
timeout 280s・pilot_d6制御必須・両AND順序で再実行し、決定性字段を出版記録・出版正本と
全件照合した。pass Aは本tree、pass Bは隔離cwd/HOME・入力複写の別treeで実行した。

残余23行の宇宙はK1097やK1095の結論から取らず、K1085→K1086→K1089→K1091→K1095の
連鎖を検証機内の独立実装（fresh D4正準形表・Bareiss行列式）で再導入した。さらに出版
掃引機械そのものを隔離treeでpristine再実行し、出力が出版正本とbyte-identicalであることを
確認した（24 gate中の1 gateで固定）。

検証過程で、knowledge READMEのK1146 bulletにおける掃引正本SHA-256の1文字転写ミス
（`…bf3eefbf…`・正しくは `…bf3eebf…`）をfail-closed pinが捕捉した。正 bodyのbyteから
再計算して確定し、実験README・K1146 item・監査正本の正本値との断層がREADME bulletの
転写のみであることを確認した。出版機のfail-closed設計の実証として記録する。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
残余23行は全行open。本検証で行は1行も閉じない。

詳細は[検証実験](../../experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/README.md)・
[監査正本](../../experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/output/replace9-sweep-reexec-second-verification-20261120.json)・
[研究ログ](../log/2026-11-20-n11-replace9-sweep-reexec-second-verification.md)。
