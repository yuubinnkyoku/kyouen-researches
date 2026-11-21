---
id: K1179
title: "fold15 receipt fold（root 120000038）単体の外部第二検証（K1173系列）"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold15 external second verification root120000038"
  - "第22 receipt・5番目WIN8 receipt foldの第三実装再検証 981 gate"
  - "監査正本 6800759e…（3実行byte一致）・53-mobility root初のreceipt fold検証・target外余剰3行の初事例確認・source_record stale参照erratum（fold12型）記録"
relations:
  - type: depends_on
    target: K1115
    note: "検証対象receipt fold。fold15 receipt（root 120000038・第22 receipt・5番目WIN8 receipt fold・出版実験 n11-residual58-win8-receipt-fold-root120000038-20261120・receipt sha256 bae2b3c1…・machine 03000c14…）の出版byte・pin表・frontier bookkeepingを第三実装で再導出・照合。"
  - type: depends_on
    target: K1114
    note: "検証対象証明書群。root 120000038のWIN8-D10証明書（5a135903…・1,171,958 bytes・32,470行・loser初手53手はn11全抽出root中初の50手超）と19 gate監査（ab8cd535…）をW pin・値単位再照合・tamperの対象。"
  - type: depends_on
    target: K1097
    note: "refsolve正本（2896deb0…・27 gate・win16 footprint 16根49行exactly-once・残余23行）がfootprint partition・retired/remaining候補構成の再照合の対象。"
  - type: related
    target: K1178
    note: "fold14外部第二検証（K1109対象）と同一手続き系列。出版済みfold14検証機（d966dad5…）を土台にfold15固有の外科手術と定数差替で本検証機を構成。fold15機のrerun gate対象はfold14出版機（7b88a565…）・fold14 receipt（ed3159fd…）、機内fold11 rerun gate対象はfold11機（9b3e06c8…）とfold11 receipt（d7bf2cd5…）。"
  - type: related
    target: K1173
    note: "fold20外部第二検証で確立したbyte pin・api.github.com非依存W再構成・pristine 4回・tamper・決定的監査（3実行byte一致）の手続き系列に属する。"
artifacts:
  - path: research/experiments/n11-fold15-external-second-verification-root120000038-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・再現手順・限界・erratum記録"
  - path: research/experiments/n11-fold15-external-second-verification-root120000038-20261121/scripts/reconstruct_fold15_inputs.py
    role: reconstruction
    note: "W15/pub15f再構成機（静的raw URL固定commitのみ・api.github.com非依存・全pin fail-closed・fold11/fold12/fold13/fold14機pin表の部分集合性機械確認・SHA-256 7757cb51…）"
  - path: research/experiments/n11-fold15-external-second-verification-root120000038-20261121/scripts/verify_fold15_external_20261121.py
    role: verifier
    note: "第三実装検証機（fold14検証機を土台にfold15固有の外科手術と定数差替で構成: 981 gate・stdlibのみ・乱数・時刻なし・SHA-256 ade19de2…・62,390 bytes）"
  - path: research/experiments/n11-fold15-external-second-verification-root120000038-20261121/output/external-audit.json
    role: audit
    note: "監査正本（101,443 bytes・981 gate全PASS〔P12/I64/C863/X26/T16〕・SHA-256 6800759e…・同一cwd 2回+隔離cwd/HOME+PYTHONHASHSEED=random の3実行byte一致・observations欄にsource_record stale参照erratum・53-mobility初・余剰3行の記録）"
  - path: research/experiments/n11-fold15-external-second-verification-root120000038-20261121/output/reproduction.log
    role: record
    note: "実行記録（X/V/T実行matrix・gate内訳・環境リセット後のW15再構成panic-recoveryの記録・解釈ガード）"
  - path: research/log/2026-11-21-n11-fold15-external-second-verification-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 0a1a52d4…・受入条件）"
  - path: research/log/2026-11-21-n11-fold15-external-second-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照・実験事実"
---

# fold15 receipt fold（root 120000038）単体の外部第二検証

## 概要

単一オーナー宣言（commit `0a1a52d4`・受入条件）の下、
fold15 receipt fold（第22 receipt・5番目WIN8 receipt fold・root
`00000000012000003800080009000000`・K1114証明書・出版実験
`research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/`）の
出版byte・W入力34 pin・チェーン簿記・幾何主張・fail-closed防衛を、repo出版byteのみから
**第三実装**の検証機で独立に再検証した。K1173（fold20）・K1175（fold12）・
K1176（fold13）・K1178（fold14）と同一手続き系列のfold receipt外部第二検証であり、
**53-mobility rootとして初のreceipt fold検証**（K1086 addtwo-greedy23 sweep起点・
winner初手53手の独立再導出）、および**closed coverage 6行中3行のtarget外余剰行**
（複数余剰行の初事例）・**28 canonical行分類でclosed-before-this-receipt 0行**
（fold14 subgeometryの1行対照）の値単位確認を完了した。
また出版receiptの `independent_verification.source_record` がfold14証明書抽出実験
（residual65系）へのstale参照を担っていることを検出し、fold12 receipt erratum
（K1175）と同型のfield-convention erratumとして監査observationsに記録した
（receipt byteは変更しない）。

## 主な結果

- **全981 gate PASS**（P 12 / I 64 / C 863 / X 26 / T 16）。監査正本 `6800759e…`
  （101,443 bytes）が同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random` の
  3実行でbyte-identical。検証機 `ade19de2…`（62,390 bytes）は1実行約105秒
  （fold15出版機単体pristine runは約23秒・機内fold11 rerun gate込み）。
- **W入力34 pin（12 Git blob SHA-1 + 22 SHA-256）をapi.github.com非依存で再構成**:
  K1175/K1176/K1178で確立した静的raw URL固定commit設計を直接適用し、
  fold15 receiptから機械読み取りしたpin表全件をfail-closed照合。
  fold11機pin表（12+10=22件）⊂fold12機pin表（12+13=25件）⊂fold13機pin表
  （12+16=28件）⊂fold14機pin表（12+19=31件）⊂fold15機pin表
  （12+22=34件）の部分集合性を機械確認。
- **実行環境リセットを跨いだpanic-recoveryの実証**: 検証中に沙緒環境がリセットされ
  ローカルファイルを全喪失したが、再構成機（HEAD pin `0a1a52d4`）がW15入力tree・
  pub15f出版byteを出版repo byteのみから約8.6秒で完全再構築し、
  12 blob+22 SHA-256全pin照合・fold15機pristine runのreceipt byte一致
  （23.1秒）まで再現。検証機とバッテリを再構築して3実行byte一致を再確認した。
  （中間状態をローカルaloneに残さない本レーン設計の実地検証。）
- **fold15出版機pristine再実行4回**（同一W 2回・隔離copytree W/cwd/HOME・隔離+
  `PYTHONHASHSEED=random`）すべて、receipt出力が出版正本 `bae2b3c1…` と
  byte-identical。各回の機内fold11 rerun gate出力（`d7bf2cd5…`）も出版正本と
  byte一致。加えてfold14出版機を隔離W複写上で検証機側から独立実行し
  `ed3159fd…` を再現・機内fold11 rerun `d7bf2cd5…` byte一致（V vr14段）。
- **チェーン全段の第三実装再構成**: base worklist 6,438行（cost 509,109）から
  fold13適用後 frontier 6,184/489,813・solved 1,664・incidence 11,775・
  残余62行を経て、fold14適用後 frontier 6,179/489,440・solved 1,669・
  incidence 11,765・needed 4,487/355,888・残余58行・五親target 54/112まで
  （fold4/56/7/8/9-12/fs13(13-16)/fold10/fold11/fold12/fold13/fold14の
  11出版記録を段ごとに再計算しpublished値と照合）。
- **fold15 receipt主張の値単位再導出**: 28 canonical行は2方法（224 D4像2石除去操作と
  C(8,6)=28部分集合）で再導出し一致・coverage 6行（K1114 g07主張3行＋target外余剰3行・
  closed edge cost 486）・影響4親（全c2: 13→10/62→59/54→51/40→37・計12
  row-closings・完全閉鎖0）・frontier_after 6,173/488,954・solved 1,675・
  incidence 11,753・needed 4,481/355,402・五親target 54→57・残余58→55行
  （55行hex全列挙照合）・win16候補 12→11根（残32行はfold15閉鎖行・
  fold11/fold12/fold13/fold14 retire行と不交差）・残余23行不交差。
  28行分類 open-frontier 6行/not-in-worklist 22行/closed-before-this-receipt 0行。
- **K1114 19 gate主要値の再照合**: probes nodes 825,127/657,152（uncapped）・
  extraction nodes 2,723,200/2,141,807・証明書 `5a135903…` 1,171,958 bytes
  32,470行 sorted unique・third_method terminal 11,338/visited 69,115/
  winner 44,580/loser 13,197/応手辺 61,058/[14,18]・subroot mobility 53の
  survival規約再実装による独立再導出。root合法手53（初の50超mobility）の
  独立再導出を含む。K1097 27 gate・win16 footprint 16根49行exactly-once
  partitionを再照合。
- **tamper 2件fail-closed**（worklist `inputs/worklist.csv` @208,888・K1114証明書
  @919,191・1 byte XOR・fold14レーン 200,222/888,222と独立の本レーン固有offset・
  期待メッセージ 'input blob mismatch'/'input sha256 mismatch'・fold15/fold11
  両出力とも未書込・WT内pinned fold14 recordは無改変）。
- **source_record stale参照erratum（fold12型・再発）**: 出版fold15 receiptの
  `independent_verification.source_record` はfold14証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9090022-20261120`）を指しており、
  K1114実験dir（`n11-residual58-win8-cert-extract-root120000038-20261120`）の
  stale参照となっている。fold13/fold14 receiptは正しく記載した直後の再発で、
  receipt生成側のテンプレート陳腐化が示唆される。receipt byteは変更せず、
  監査JSON observationsにerratumとして記録しK1114フォローアップに回す。
  `certificate_source`・`verdict_join_summary`・`experiment`各欄と
  `receipt.single_owner_note` は正しくK1114系を指す。

## 位置づけ

- 本項は行を1行も閉じない: 検証の検証（簿記・決定性・入力pin・fail-closed防衛の
  再検査）である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
  REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を
  勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

part1 commit `2e1bc1ea`（実験dir 5ファイル・fetch-back 5/5 byte一致）。
（2026-11-21）
