---
id: K1180
title: "fold16 receipt fold（root 8890020）単体の外部第二検証（K1173系列）"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold16 external second verification root8890020"
  - "第23 receipt・6番目WIN8 receipt foldの第三実装再検証 1061 gate"
  - "監査正本 09f80902…（3実行byte一致）・closed-before-this-receipt 1行を含む2例目WIN8 root・IV.source_record清潔記載の維持（fold12/fold15 erratum対照）"
relations:
  - type: depends_on
    target: K1116
    note: "検証対象receipt fold。fold16 receipt（root 8890020・第23 receipt・6番目WIN8 receipt fold・出版実験 n11-residual55-win8-receipt-fold-root8890020-20261120・receipt sha256 edd55258…・machine ecaef742…）の出版byte・pin表・frontier bookkeepingを第三実装で再導出・照合。"
  - type: depends_on
    target: K1113
    note: "検証対象証明書群。root 8890020のWIN8-D10証明書（105e1e2a…・775,317 bytes・21,446行・loser初手50手）と19 gate監査（b8c264e6…）をW pin・値単位再照合・tamperの対象。"
  - type: depends_on
    target: K1097
    note: "refsolve正本（2896deb0…・27 gate・win16 footprint 16根49行exactly-once・残余23行）がfootprint partition・retired/remaining候補構成の再照合の対象。"
  - type: related
    target: K1179
    note: "fold15外部第二検証（K1114対象）と同一手続き系列。出版済みfold14検証機（d966dad5…）を土台にfold16固有の外科手術と定数差替で本検証機を構成。fold16機のrerun gate対象はfold15出版機（03000c14…）・fold15 receipt（bae2b3c1…）、機内fold11 rerun gate対象はfold11機（9b3e06c8…）とfold11 receipt（d7bf2cd5…）。"
  - type: related
    target: K1173
    note: "fold20外部第二検証で確立したbyte pin・api.github.com非依存W再構成・pristine 4回・tamper・決定的監査（3実行byte一致）の手続き系列に属する。"
artifacts:
  - path: research/experiments/n11-fold16-external-second-verification-root8890020-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・再現手順・限界・erratum対照の記録"
  - path: research/experiments/n11-fold16-external-second-verification-root8890020-20261121/scripts/reconstruct_fold16_inputs.py
    role: reconstruction
    note: "W16/pub16f再構成機（静的raw URL固定commitのみ・api.github.com非依存・全pin fail-closed・fold11/fold12/fold13/fold14/fold15機pin表の部分集合性機械確認・SHA-256 c70cbc45…）"
  - path: research/experiments/n11-fold16-external-second-verification-root8890020-20261121/scripts/verify_fold16_external_20261121.py
    role: verifier
    note: "第三実装検証機（fold14検証機を土台にfold16固有の外科手術と定数差替で構成: 1061 gate・stdlibのみ・乱数・時刻なし・SHA-256 32917945…・61,627 bytes）"
  - path: research/experiments/n11-fold16-external-second-verification-root8890020-20261121/output/external-audit.json
    role: audit
    note: "監査正本（108,139 bytes・1061 gate全PASS〔P12/I75/C932/X26/T16〕・SHA-256 09f80902…・同一cwd 2回+隔離cwd/HOME+env -i+PYTHONHASHSEED=random の3実行byte一致・observations欄にclosed-before 1行2例目・source_record清潔記載の記録）"
  - path: research/experiments/n11-fold16-external-second-verification-root8890020-20261121/output/reproduction.log
    role: record
    note: "実行記録（X/V/T実行matrix・gate内訳・W16ローカル破損からの静的URL完全復旧の記録・解釈ガード）"
  - path: research/log/2026-11-21-n11-fold16-external-second-verification-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit c6a55000…・受入条件）"
  - path: research/log/2026-11-21-n11-fold16-external-second-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照・実験事実"
---

# fold16 receipt fold（root 8890020）単体の外部第二検証

## 概要

単一オーナー宣言（commit `c6a55000`・受入条件）の下、
fold16 receipt fold（第23 receipt・6番目WIN8 receipt fold・root
`00000000010000889002000080100000`・K1113証明書・出版実験
`research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/`）の
出版byte・W入力37 pin・チェーン簿記・幾何主張・fail-closed防衛を、repo出版byteのみから
**第三実装**の検証機で独立に再検証した。K1173（fold20）・K1175（fold12）・
K1176（fold13）・K1178（fold14）・K1179（fold15）と同一手続き系列のfold receipt
外部第二検証であり、**closed-before-this-receipt 1行を含むWIN8 rootとして2例目**
（fold14 rootに次ぐ2例目。二重閉鎖の構造的除外を28 canonical行分類・
closed_history全履歴・worklist/residual55の三方で機械確認）、
および**fold12（K1175）・fold15（K1179）続きのsource_record stale参照erratum
とは対照的な清潔記載の維持**（fold16 receiptは自実験dir
`n11-residual58-win8-cert-extract-root8890020-20261120`を正しく指す）の
値単位確認を完了した。

## 主な結果

- **全1061 gate PASS**（P 12 / I 75 / C 932 / X 26 / T 16）。監査正本 `09f80902…`
  （108,139 bytes）が同一cwd 2回＋隔離cwd/HOME＋`env -i`＋`PYTHONHASHSEED=random`
  の3実行でbyte-identical。検証機 `32917945…`（61,627 bytes）は1実行約210秒
  （fold16出版機単体pristine runは約46秒・機内fold11 rerun gate込み）。
- **W入力37 pin（12 Git blob SHA-1 + 25 SHA-256）をapi.github.com非依存で再構成**:
  K1175/K1176/K1178/K1179の静的raw URL固定commit設計を直接適用し、
  fold16 receiptから機械読み取りしたpin表全件をfail-closed照合。
  fold11機pin表（12+10）⊂fold12機pin表（12+13）⊂fold13機pin表（12+16）⊂
  fold14機pin表（12+19）⊂fold15機pin表（12+22）⊂fold16機pin表
  （12 blob+25 SHA-256）の部分集合性を機械確認（pin表鎖がここで閉じた）。
- **W16ローカル破損からの完全復旧の実証（実験事実）**: 中間作業中に誤って
  広すぎるcleanup globがW16のpinned record群（fold11-15 receipt・K系監査・証明書等
  約20ファイル）を削除したが、再構成機（HEAD pin `c6a55000`）の再実行が
  出版repo byteのみからW16入力tree 43ファイル（37 pin全照合）を完全復旧し、
  pin表部分集合鎖・fold16機pristine runのreceipt byte一致（46秒）まで再現した。
  中間状態をローカルaloneに残さない本レーン設計の実地検証
  （K1179の実行環境リセットpanic-recoveryと同種・本件はオペレーションミス由来）。
- **fold16出版機pristine再実行4回**（同一W 2回・隔離copytree W/cwd/HOME・隔離+
  `PYTHONHASHSEED=random`）すべて、receipt出力が出版正本 `edd55258…` と
  byte-identical。各回の機内fold11 rerun gate出力（`d7bf2cd5…`）も出版正本と
  byte一致。加えてfold15出版機を隔離W複写上で検証機側から独立実行し
  `bae2b3c1…` を再現・機内fold11 rerun `d7bf2cd5…` byte一致（V vr15段）。
- **チェーン全段の第三実装再構成**: base worklist 6,438行（cost 509,109）から
  fold14適用後 frontier 6,179/489,440・solved 1,669・incidence 11,765・
  needed 4,487/355,888・残余58行を経て、fold15適用後 frontier 6,173/488,954・
  solved 1,675・incidence 11,753・needed 4,481/355,402・残余55行・
  五親target 57/112まで（fold4/56/7/8/9-12/fs13(13-16)/fold10/fold11/
  fold12/fold13/fold14/fold15の12出版記録を段ごとに再計算しpublished値と照合）。
- **fold16 receipt主張の値単位再導出**: 28 canonical行は2方法（224 D4像2石除去操作と
  C(8,6)=28部分集合）で再導出し一致・coverage 5行（K1113 g07主張4行＋target外
  余剰1行 `00000000000000801222000100000000`・closed edge cost 379）・
  影響4親（全c2: 20→18/21→19/42→39/60→57・計10 row-closings・完全閉鎖0）・
  frontier_after 6,168/488,575・solved 1,680・incidence 11,743・
  needed 4,476/355,023・五親target 57→61・残余55→51行（51行hex全列挙照合）・
  win16候補16根のうち6根retire（fold11 4行+fold12 3行+fold13 3行+fold14 4行+
  fold15 3行+fold16主張4行=21行retire・残10根28行はfold16閉鎖行・retire各行と
  不交差）・残余23行掃引計画不交差。
  28行分類 open-frontier 5行/not-in-worklist 22行/closed-before-this-receipt 1行
  （`00000000000000003800000008003000`・fold13 receipt閉鎖済み。二重閉鎖は
  coverage再導出から構造的に除外）。
- **K1113 19 gate主要値の再照合**: probes nodes 575,570/409,407（uncapped）・
  extraction nodes 4,424,758/4,424,758・証明書 `105e1e2a…` 775,317 bytes
  21,446行 sorted unique・third_method terminal 7,653/visited 48,855/
  winner 31,320/loser 9,882/応手辺 43,837/[14,18]・subroot mobility 50の
  survival規約再実装による独立再導出。K1097 27 gate・win16 footprint
  16根49行exactly-once partitionを再照合。
- **tamper 2件fail-closed**（worklist `inputs/worklist.csv` @300,111・K1113証明書
  @740,321・1 byte XOR・fold14レーン 200,222/888,222・fold15レーン
  208,888/919,191と独立の本レーン固有offset・期待メッセージ
  'input blob mismatch'/'input sha256 mismatch'・fold16/fold11両出力とも
  未書込・WT内pinned fold15 recordは無改変）。
- **IV.source_record清潔記載の維持（erratum対照）**: 出版fold16 receiptの
  `independent_verification.source_record` はK1113証明書抽出実験
  （`n11-residual58-win8-cert-extract-root8890020-20261120`）を正しく指す。
  fold12（K1175）・fold15（K1179）のstale参照erratumの直後であるが、
  fold16 receiptは自実験dirを記載し、`certificate_source`・
  `verdict_join_summary`・`schema`/`experiment`各欄も正しい
  （publish時点のfold11-16 receiptでclean・stale・clean・clean・stale・cleanの系列）。
  receipt byteは変更しない。

## 位置づけ

- 本項は行を1行も閉じない: 検証の検証（簿記・決定性・入力pin・fail-closed防衛の
  再検査）である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
  REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を
  勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

part1 commit `056b8470`（実験dir 5ファイル・fetch-back 5/5 byte一致）。
（2026-11-21）

