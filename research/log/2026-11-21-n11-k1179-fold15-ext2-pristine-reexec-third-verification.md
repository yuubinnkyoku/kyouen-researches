# 2026-11-21 n11 K1179 fold15 ext2 pristine re-exec 第三検証（単一オーナー・part1〜3）

## 経緯

- 前回まで: fold12/K1184・fold13/K1185・fold14/K1186の第三検証が出版済み。fold12〜16単体ext2第二検証群
  （K1175/K1176/K1178/K1179/K1180）の第三検証は第四号のfold15が次の対象。
- K1179対象の固定値: root `00000000012000003800080009000000`〔root 120000038・第22 receipt・5番目WIN8
  receipt fold〕・pin commit `2e1bc1ea`（part1・5ファイル一括）・出版社監査正本 `6800759e…`
  （101,443 bytes・gate 981）・W15再構成機 `7757cb51…`（10,644 bytes）・第三実装検証機
  `ade19de2…`（62,390 bytes）・README `20a2d104…`（6,683 bytes）・reproduction.log `579f178a…`
  （2,106 bytes）。
- 単一オーナー宣言: `research/log/2026-11-21-n11-k1179-fold15-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `04b4ed9d…`・宣言時HEAD `b619261a`〔K1186 part3〕・受入条件5項目）を先に出版し
  fetch-back byte一致を確認。
- 実験dir: `research/experiments/n11-fold15-ext2-pristine-reexec-third-verification-root120000038-20261121/`。
- 宣言からpart1までの間に並走レーンのコミットが2件（four-row q6 band extension 3の
  `ebda281e`〔records 114→116〕・`9e0fb740`〔frontier README + K1177 item + knowledge README bullet〕）が
  mainに入ったが、いずれも本レーンの対象fileと非接触のためそのままpush（自file非接触+即時push規約）。

## 実施（受入条件対照）

宣言の受入条件5項目に対する実施結果:

1. **出版byte 5点pin** — harness pin stageがpin commit `2e1bc1ea`から実験dir 5ファイルを自力取得し
   SHA-256+byte数10 gate PASS（battery 3巡いずれも）。手動pin試行でも5点同一SHAを確認済み。
2. **W15再構成2実装参照** — ref_a `b619261a`（宣言時HEAD）・ref_b `04b4ed9d`（宣言commit）の両pinned
   refで改変なし再構成機を2回実行し、W15 tree（12 blob + 22 SHA-256 = 34 pin +
   fold11/12/13/14/15の5 chain機・39ファイル）を再構成、`diff -r` byte一致。subset-checkは
   fold11 pins 12/pin256 10・fold12 pins 12/pin256 13・fold13 pins 12/pin256 16・fold14 pins 12/pin256 19
   がfold15 12+22の部分集合として機械確認され最終行「RECONSTRUCTED W at … PINS 12 PIN256 22」。
   1参照約7.7秒（api.github.com非依存・raw固定commit URL）。
3. **出版検証機pristine 4回/battery×3** — 同一base 2巡（計8回）・隔離base+copytree W/cwd/HOME
   +`PYTHONHASHSEED=random` 1巡（4回）の計12回すべてrc=0・`ALL 981 GATES PASS`・
   出力監査JSON（101,443 bytes）が出版正本 `6800759e…` とbyte-identical。battery内4回間でもbyte一致。
   1回105.6〜106.0秒（fold14機の約2倍）・1 battery 約7分15秒（手動試行1回=13回総計）。
4. **tamper探針fail-closed** — 本レーン選択offsetのworklist @277,555（blob pin）・K1114証明書
   @877,666（sha256 pin）1 byte XOR 0x01がbattery全3巡でrc=1・`GATE FAILED [i]`・監査未書込。
   出版試験位置@208,888/@919,191はverifier自身の機内断続探索で毎battery再確認。
   手動XOR-0x20探針でも同一offsetで同一メッセージ発火を確認。本番Wは探針後に無改変再照合
   （worklist `6d8a449e…`・K1114証明書 `5a135903…`）。
5. **監査byte正本の固定** — 第三検証harnessの監査 `output/harness-audit.json` がbattery 3巡で
   byte一致（`cfb6879a…`・6,858 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・
   all_gates_pass true・時刻/絶対path/volatile排除）。per-stage partsはwall_ms保持でbyte再現対象外。

## 実験事実

1. fold15検証機はgate 981（P 12/I 64/C 863/X 26/T 16）・1回約105.6〜106.0秒でfold14機（880 gate・約53秒）の
   約2倍。W15 tree 39ファイルはfold11〜15の全5 chain機がWに含まれる初の規模で、第三検証のrecon stageは
   fold14時（35ファイル）から4ファイル増（1参照約7.7秒）。
2. worklist `inputs/worklist.csv`（`6d8a449e…`・360,834 bytes）はfold12/13/14第三レーンに続き同一series
   ファイルの4レーン目の再利用で、第三検証のtamper探針位置が4レーンで互いに別々
   （@150,000・@222,999・@333,444・@277,555）。
3. K1114証明書（`5a135903…`・1,171,958 bytes・fold15 root・合法手53・WIN8-D10）の第三検証レーンの
   tamper探針は初位置 @877,666（fold15第二検証の @919,191・fold14第三の K1109証明書 @999,111 と別位置）。
4. fold15 receiptの `independent_verification.source_record` stale参照erratum（fold14証明書抽出実験を指す・
   K1179監査JSONのobservations欄に記録済み）は本第三検証では監査byteに参照元どおり現れる
   （erratumはreceipt byte不変で放置・K1114レーンへのフォローアップのまま）。
5. 12回の検証機実行・3 batteryすべてで監査byteが出版正本とbyte一致したため、
   「fold15の外部第二検証は（監査byteとして）環境非依存に決定的である」ことが第三実装・第三環境から確認された
   （battery中の環境リセット・api.github.com枯渇・待機pollingは皆無であった）。

## 出版

- 宣言ノート: commit `04b4ed9d`（04:03Z）・fetch-back byte一致。
- part1: commit `7ed921fa`（実験dir 4ファイル・単一push_filesコミット）・fetch-back 4/4 byte一致
  （README `04c3401c…`・harness `76cb4690…`・監査正本 `cfb6879a…`・reproduction.log `c85cfc2b…`）。
- part2: 本item（K1187・K番号はpush直前3点確認で採番）＋本log。
- part3: knowledge README末尾bullet（fold16 ext2第三検証は未宣言のため次回候補）。

## 解釈規約

本検証はK1179第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、
行は1行も閉じない（fold15時点残余58→55行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのままである。**
