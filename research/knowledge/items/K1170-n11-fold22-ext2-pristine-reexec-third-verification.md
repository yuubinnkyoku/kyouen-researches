---
id: K1170
title: "K1167（fold22外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold22 ext2 pristine re-execution third verification"
  - "K1167監査byte再現・W入力2回再構成・三層pin防衛の独立確認"
  - "harness監査正本 fdb72c40…・出版監査 b4b082f8… 4回byte一致"
relations:
  - type: depends_on
    target: K1167
    note: "検証対象。出版実験dir 5ファイルのbyte pin（part1 commit 4eb6cbf05）、同梱再構成機による固定ref 34c29854…でのW 2回再構成、出版検証機のpristine再実行4回と監査正本 b4b082f8…（141,752 bytes・gate 1,463）のbyte一致を再確認する。"
  - type: depends_on
    target: K1132
    note: "fold22 receipt fold正本。上流出版byte 4点（receipt f6e011f4…・機 d5721408…・builder a73995be…・出版README 0e6861bf…）は再構成機の出力した両pub copyでSHA-256照合かつ2再構成間byte一致。"
  - type: related
    target: K1165
    note: "fold24/K1164に対する第三検証と同一の手続きを fold22/K1167 に適用したもの（pristine再実行・tamper探針・harness監査の決定性・fetch-back byte検証）。"
artifacts:
  - path: research/experiments/n11-fold22-ext2-pristine-reexec-third-verification-root840500-20261120/README.md
    role: source
    note: "位置づけ・固定pin・実施内容と結果・実験事実4項・再現手順・限界（SHA-256 6f6ceb0a…・8,232 bytes）"
  - path: research/experiments/n11-fold22-ext2-pristine-reexec-third-verification-root840500-20261120/scripts/verify_k1167_fold22ext2_third_20261120.py
    role: verifier
    note: "第三検証harness（stdlibのみ・fail-closed・stage分割: pin/reconstruct-w1/w2/wcmp/rerun-r1..r4/tampers/finalize・SHA-256 2f6290bf…・19,939 bytes）"
  - path: research/experiments/n11-fold22-ext2-pristine-reexec-third-verification-root840500-20261120/output/harness-audit.json
    role: audit
    note: "harness監査正本（4,853 bytes・SHA-256 fdb72c40…・finalize 9 gate・同一cwd 2回＋隔離cwd/HOME＋PYTHONHASHSEED=randomの3実行byte-identical）"
  - path: research/experiments/n11-fold22-ext2-pristine-reexec-third-verification-root840500-20261120/output/reproduction.log
    role: record
    note: "実行記録（api.github.com 403 rate limit失敗の実験事実・post-battery 55 pin再照合込み・SHA-256 86747329…・5,150 bytes）"
---

# K1167（fold22外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `53501d73`・受入条件6項目）の下、K1167（fold22 receipt fold の
外部第二検証・出版監査正本 `b4b082f8…`・gate 1,463）を、repo出版byteのみを素材に第三者環境から
完全再現し、その決定性・入力pin・fail-closed防衛を独立確認した。K1165（fold24/K1164第三検証）と
同一手続きのfold22適用である。

## 主な結果

- **出版byte再pin**: K1167実験dir 5ファイル（README `6b32ce99…`・再構成機 `dfa50996…`・
  検証機 `ca11cbbc…`・監査正本 `b4b082f8…`・実行記録 `5059c458…`）をpinned commit
  `4eb6cbf05` から再取得しSHA-256 fail-closed照合（6 gate）。
- **W入力2回再構成**: 同梱の再構成機を固定ref `34c29854c64286bbb1792ff28dc1973aef341e20` で
  2回独立実行し、両W treeが60ファイル・14,673,721 bytesで全ファイルbyte一致、
  上流fold22出版byte 4点も両再構成間で一致（10 gate）。
- **pristine再実行4回**: 出版K1167検証機を改変なしに4回実行（同一cwd 2回・
  隔離cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回・r4はW2のfresh copytree）。
  全回 returncode 0・stderr空・出力監査SHA-256が出版正本 `b4b082f8…` とbyte一致
  （各回でgate 1,463が再パス・fold22機6回起動込み・1回実測35.0秒で出版時実測約34.4秒と整合）。
- **tamper 3件fail-closed（本レーン独自offset）**: t1 copytree W上の worklist byte offset 1234 と
  t2 K1125証明書 byte offset 17522 の1 byte XOR 0x01は出版検証機のW pin gate
  （`W blob pin`/`W sha256 pin`）が、t3 K1167出版監査 byte offset 4096（実験dir写し上）は
  本harness自身の実験dir pin gateが、それぞれreturncode 1・監査未書込で捕捉。
  機械内T-gate・検証機I-section gate・harness pin gateの三層防衛が実測で独立に作動。
- **harness監査の決定性**: 監査正本 `fdb72c40…`（4,853 bytes・finalize 9 gate）は
  同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`の3実行でbyte一致（時刻フィールドなし）。
- **post-battery再照合**: W1/W2/W4のfold22機入力55 pin（12 Git-blob + 43 SHA-256）が
  battery後にすべて無改変。

## 実験事実

1. 共有IP上のapi.github.com無認証quotaは並走レーンとの共喰いで枯渇し得る
   （403 rate limit・quota 0・21:45:19Zリセットを観測）。fail-closed設計は取得失敗を
   「部分W」ではなく「中断＋記録」に落とし、固定refからの再取得で冪等に復旧する。
   再構成機のtrees API依存は12 legacy blob pinのSHA→path写像のみ。
2. part1 push時のREADME転写1文字の打鍵タイポ（1 byte）をfetch-back byte検証が即捕捉し、
   訂正コミットで修正した（K1158/K1160/K1164のpin転写typo捕捉と同じ防衛パターンが
   出版社転写層でも作動）。テンプレートリテラルのエスケープ処理（String.rawは
   エスケープbyteを保持する）は第三検証harness出版時の新たな転写リスク源であることも
   記録する（最終的に4/4 fetch-back byte一致で確定）。

## 出版

- part1（実験dir 4ファイル）: 初回commit `41053a7d`・README訂正 `bf54c57f`/`b40f4668` を経て
  最終fetch-back 4/4 byte一致（commit `b40f4668`）。
- 宣言ノート: `research/log/2026-11-20-n11-k1167-fold22-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `53501d73`）。

## 解釈規約

本項はK1167監査の決定性・入力pin・fail-closed防衛の再検査であり、
S6行・五親target行を1行も閉じない。fold22 receiptの6行閉鎖（残余35→32行）は
Publisherの成果簿記であり、K1167はその外部第二検証、本項はその第三検証である。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は
すべてUNKNOWNのままである。**
