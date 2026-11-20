# fold24外部第二検証（K1164）のpristine再実行第三検証: 実行記録（2026-11-20）

## 経緯

- **宣言（2026-11-20T19:15:00Z・commit `3c88de5ce4`）**:
  単一オーナー宣言ノート
  [宣言ノート](2026-11-20-n11-k1164-fold24-ext2-pristine-reexec-third-single-owner-note.md)
  を先行出版した。宣言時点のmain HEADは `118e1b3d23`。受入条件は6項目
  （出版byte pin照合・W二回再構成byte一致・検証機pristine再実行4回×3のbyte-identity・
  出版社未使用offsetのtamper fail-closed・harness監査正本3実行byte一致・解釈ガード文言の監査同梱）。
  fold23外部第二検証宣言（`90ac8eed`・18:55Z）・fold25外部第二検証宣言（`aad3b71c`）・
  WIN8証明書行共有監査宣言（`c403614f`・18:28Z）との範囲分離を宣言どおり維持した。
- **着手の選定**: 前回レジュームの最優先（fold26 receipt fold・round-5 refsolve・
  WIN8-D10 root `00000000010000809002000040002001` 証明書抽出の着地後第二検証）は
  本実行開始時点（19:03Z HEAD `118e1b3d23`）でいずれも未着地・宣言済みのため着手不能。
  直前18:52Zに着地したK1164（fold24外部第二検証）の第三検証が未宣言・未着手であったため、
  本レーンの既存系譜（第三検証一式）として最も価値の高い対象として選定した。
- **出版byte取得（bash curl・pinned commit）**: K1164実験dir 4点
  （README `ff429479…`・検証機 `9bc24e38…`・監査正本 `c7e10332…`・実行記録 `16b7678e…`）と
  K1140出版実験dir 8点（receipt `c4ab76d3…`・出版機 `f462733d…`・同梱監査正本 `49f330c6…`・
  再現log `cb01749a…`・reconstruct_inputs.py `f4e1fa8e…`・同梱監査機 `e0dbebe4…`・
  build_fold24.py `3c1e07fb…`・README `77c4ee40…`）を取得。計12点すべてが
  README/item/検証機定数に書かれた出版pinとbyte一致。
- **W再構成（2回）**: 出版済み `reconstruct_inputs.py`（固定Git参照 `b91e85a9…`）で
  W-A・W-Bを独立に再構成（各約19秒・61 pin fail-closed検証込み）。
  `diff -r` で全70ファイルbyte一致。harness正準manifest digest `1426b676…`。
- **smoke実行**: K1164検証機を本環境で単体実行。PASS・gate 800・監査JSONが出版正本と
  byte-identical・実測49.8秒（出版社環境の49.5秒と同等）。
- **harness初期不具合のfail-closed捕捉（実験事実）**:
  (a) 初版はW manifest digest定数をshell側正準形（`./`接頭辞）で計った値
  （`a94bd7d7…`）で埋めており、harness正準形（接頭辞なし）との不一致を
  harness自身の `W-tree-digest-pinned` gateがbattery前に捕捉。定数を正準形で再導出。
  (b) 二版目のstaging feed検査はverifierに供給しない2ファイル（実験README/build_fold24.py）
  までpinしようとしてFileNotFoundErrorで停止。供給6ファイルのみをgateするよう修正。
  いずれも出版byteは無傷で、修正版harnessが出版的byte。pin gate体系の防御が
  第三検証harness側でも作動した（K1158・K1160・K1164出版時と同じパターン）。
- **battery実行（3回）**: いずれもPASS・gate 66・監査正本 `efffaab8…` byte-identical。
  battery1 同一cwd（実測3m17.3s）・battery2 同一cwd fresh process（3m18.9s）・
  battery3 隔離HOME/cwd＋`PYTHONHASHSEED=random`（3m18.5s）。
  battery内訳: staged pin 12/12・W 2回再構成一致・検証機pristine再実行4回
  （同一cwd2・隔離cwd/HOME・隔離+PYTHONHASHSEED=random）の全出力が出版監査 `c7e10332…`
  とbyte-identical・stdout 4回同一・harness tamper 3件 fail-closed。
  セッション全体では検証機13回（smoke 1＋battery 3×4）＝fold24出版機52回の
  fresh再実行（fold23隔離rerun chain込み）と同梱独立監査13回の再実行を機械計算した。

## 結果

harness `verify_k1164_pristine_third_20261120.py`（SHA-256
`f45aa1ac1d022c6517dd49f5e9bf151c0834ea82545410349fccb41d1ccd6d31`・14,351 bytes）は
出版byteとW再構成だけからK1164監査正本のbyte再生を完全に再現し、
残余20行・pool P⁗ 120,416根に変更を与えない。監査正本
`output/harness-audit.json`（3,184 bytes・gate 66）のtamper 3件のoffsetは
出版社T-gateのworklist 777・K1136証明書 12345と完全に別
（W worklist 404・W fold23記録 3456・pub receipt 2024）で、いずれも
returncode 1・監査未書込・GATE FAILED。K1164の実験dirが輸送・転写・ローカル記憶に
依存せず第三者環境から再現可能であることが確定した。

## 出版

3部構成でmainに直接出版（AGENTS.mdに従いbranch/PRは作らない）。K番号はpush直前に
3点確認（item 404・README bullet `items/K1165-` grep 0件・items pathへの新規commit確認）で
**K1165**を取得した（宣言ノートはK番号を確定しない設計で先行出版済み）。

- part1: 実験dir 16ファイル `research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/`
  （commit `1c1d97aac7`・fetch-back curl + cmp 16/16 byte-identical）。
  self-contained構成: harness・harness監査正本・実行記録・staged出版byte 12点
  （K1164 4点＋K1140 8点・harness側pin内蔵）。Wは17MBのため未収録で、
  出版reconstruct_inputs.py＋固定Git参照からの再構成手順をREADMEに明記
  （再構成の2回byte一致はharnessのgateとして機械検証済み）。
- part2: K1165 item＋本log（このcommit）。
- part3: knowledge README末尾へのK1165 bullet追記。

## 解釈上の制限

本検証で行を1行も閉じない。残余20行・pool P⁗ 120,416根は不変。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
