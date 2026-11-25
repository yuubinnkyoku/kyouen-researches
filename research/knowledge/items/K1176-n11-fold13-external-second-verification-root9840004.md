---
id: K1176
title: "fold13 receipt fold（root 9840004）単体の外部第二検証（K1173系列）"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold13 external second verification root9840004"
  - "第20 receipt・3番目WIN8 receipt foldの第三実装再検証 774 gate"
  - "監査正本 4fe40fa2…（3実行byte一致）・fold11/fold12出版機独立rerun再現・単一WIN8 receiptとして最多のopen 9行閉鎖の値単位確認"
relations:
  - type: depends_on
    target: K1108
    note: "検証対象証明書群。root 9840004のWIN8-D10証明書（5b114b9e…・1,640,220 bytes・45,286行・n11-terminal-strategy-v1全証明書中最大行数）と19 gate監査（2e453a76…）をW pin・値単位再照合・tamperの対象。"
  - type: depends_on
    target: K1097
    note: "refsolve正本（2896deb0…・27 gate・win16 footprint 49行exactly-once・残余23行）がfootprint partition再照合の対象。"
  - type: related
    target: K1175
    note: "fold12外部第二検証（K1106対象）と同一手続き系列。K1175が確立したapi.github.com非依存の静的raw URL再構成機設計を直接適用。fold13機のrerun gate対象はfold12出版機（706bfa7a…）とfold12 receipt（0f73795c…）、機内fold11 rerun gate対象はfold11機（9b3e06c8…）とfold11 receipt（d7bf2cd5…）。"
  - type: related
    target: K1173
    note: "fold20外部第二検証（K1129対象）で確立したbyte pin・W再構成・pristine 4回・tamper・決定的監査の手続き系列に属する。"
artifacts:
  - path: research/experiments/n11-fold13-external-second-verification-root9840004-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・再現手順・限界"
  - path: research/experiments/n11-fold13-external-second-verification-root9840004-20261121/scripts/reconstruct_fold13_inputs.py
    role: reconstruction
    note: "W13/pub13再構成機（静的raw URL固定commitのみ・api.github.com非依存・全pin fail-closed・fold11/fold12機pin表の部分集合性機械確認・SHA-256 1b54624f…）"
  - path: research/experiments/n11-fold13-external-second-verification-root9840004-20261121/scripts/verify_fold13_external_20261121.py
    role: verifier
    note: "第三実装検証機（K1175検証機を土台にfold13固有の外科手術と定数差替で構成: 774 gate・stdlibのみ・乱数・時刻なし・SHA-256 aeda41e1…・57,284 bytes）"
  - path: research/experiments/n11-fold13-external-second-verification-root9840004-20261121/output/external-audit.json
    role: audit
    note: "監査正本（81,632 bytes・774 gate全PASS・SHA-256 4fe40fa2…・3実行byte一致・observations欄にfold12 erratumとの対照記録）"
  - path: research/experiments/n11-fold13-external-second-verification-root9840004-20261121/output/reproduction.log
    role: record
    note: "実行記録（X/V/T実行matrix・gate内訳・findings・解釈ガード）"
  - path: research/log/2026-11-21-n11-fold13-external-second-verification-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 5a9e8142…・宣言 2026-11-21T01:00:00Z想定・受入条件6項目）"
  - path: research/log/2026-11-21-n11-fold13-external-second-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照・実験事実"
---

# fold13 receipt fold（root 9840004）単体の外部第二検証

## 概要

単一オーナー宣言（commit `5a9e814294`・宣言 2026-11-21T01:00:00Z想定・受入条件6項目）の下、
fold13 receipt fold（第20 receipt・3番目WIN8 receipt fold・root
`00000000000000003800000009840004`・出版実験
`research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/`）の
出版byte・W入力28 pin・チェーン簿記・幾何主張・fail-closed防衛を、repo出版byteのみから
**第三実装**の検証機で独立に再検証した。K1173（fold20/K1129対象）・K1175（fold12/K1106対象）
と同一手続き系列のfold receipt外部第二検証であり、単一WIN8 receiptとして最多を更新する
open 9行閉鎖（余剰6行も単一receiptとして最多）の値単位確認を完了した。

## 主な結果

- **全774 gate PASS**（P 12 / I 44 / C 673 / X 29 / T 16）。監査正本 `4fe40fa2…`
  （81,632 bytes）が同一cwd 2回＋隔離cwd/HOME＋`env -i`＋`PYTHONHASHSEED=random` の
  3実行でbyte-identical。検証機 `aeda41e1…`（57,284 bytes）は1実行約29秒。
- **W入力28 pin（12 Git blob SHA-1 + 16 SHA-256）をapi.github.com非依存で再構成**:
  K1175で確立した静的raw URL固定commit設計を直接適用し、fold13 receiptから機械読み取りした
  pin表（12 blob + 16 SHA-256 = 28件）全件をfail-closed照合（quota待機ゼロ）。
  fold11機pin表（12+10=22件）⊂fold12機pin表（12+13=25件）⊂fold13機pin表（28件）の
  部分集合性を機械確認。
- **fold13出版機pristine再実行4回**（同一W 2回・隔離copytree W/cwd/HOME・隔離+
  `PYTHONHASHSEED=random`）すべて、receipt出力が出版正本 `c2bf8051…`（20,416 bytes）と
  byte-identical。各回の機内fold11 rerun gate出力（`d7bf2cd5…`）・隔離W複写上の
  fold12 rerun gate出力（`0f73795c…`）も出版正本とbyte一致。加えてfold11・fold12出版機を
  隔離W複写上で検証機側から独立実行し、`d7bf2cd5…`/`0f73795c…` を再現
  （宣言受入条件3の外側確認）。
- **チェーン全段の第三実装再構成**: base worklist 6,438行（cost 509,109）から
  globalFold 6,259/495,507 → cost78c/79c → first → second-third → fourth →
  fifth-sixth → seventh → eighth → ninth-twelfth（4 receipt）→ windfall4 13th-16th →
  seventeenth fold10 → WIN8 fold11（6,201/491,110）→ fold12
  （6,193/490,526・solved 1,655・incidence 11,790・残余65・target 47）までの
  9出版記録連鎖を段ごとに再計算しpublished値と照合（fold4〜fold12）。
- **fold13 receipt主張の値単位再導出**: 28 canonical行=2方法一致
  （8 D4像×C(8,2) 224操作とC(8,6)=28部分集合・D4同変性）、分類open 9/not-in-worklist 19、
  coverage 9行=K1108 g07主張3行＋余剰6行・closed edge cost 713・影響5親
  （c4 3: 87→84/90→87/75→72・c2 2: 61→58/16→13・各3行closing・完全閉鎖0・
  合計15 row-closings）、frontier_after 6,184/489,813・solved 1,664・
  incidence 11,775・needed 4,492/356,261、五親target 47→50・残余65→62
  （62行hex全列挙照合）、win16候補 14→13根（主張42→39行・retired root `…9840004`
  3行・残余23行不交差）、root合法手57のsurvival規約独立再導出
  （quadruple-free・D4正準込み）、K1108 19 gate主要値
  （g06 uncapped probes nodes 1,143,198/1,528,656・g13 nodes 4,109,768/3,075,922・
  証明書 1,640,220 bytes 45,286行 sorted unique・third_method terminal 17,333/
  visited 103,531/winner 66,627/loser 19,571/応手辺 91,337・terminalRange [14,18]）と
  K1097 27 gate・49行exactly-once partition。
- **tamper 2件fail-closed**（本レーン選択・出版社未試験offset・K1175レーンと別位置）:
  worklist @117,777（blob pin）・K1108証明書 @777,777（sha256 pin）の1 byte XOR 0x01が
  rc≠0・fold13/fold11出力とも未書込・WT内pinned fold12 record無改変で捕捉。
  本番Wは実施後に無改変再照合。
- **fold12 erratumパターンの対照確認**: fold13 receiptの
  `independent_verification.source_record` はK1108証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9840004-20261120`・root 9840004）を正しく指す。
  K1175の監査で発見したfold12 receiptのstale参照erratum（fold11実験パス残存）とは対照的に
  記載エラーなし。この対照を監査JSONのobservations欄に記録した（文書フィールドの検査で
  あり、fold12 receiptのbyteは変更しない）。

## 実験事実

1. W13再構成はK1175レーンの成果であるapi.github.com非依存の静的raw URL設計の
   直接適用で、quota枯渇条件下でも待機ゼロで完了した。fold13 receiptの
   `source_blob_pins`/`source_sha256_pins` から機械読み取りした28 pinに加え、
   rerun gate対象（fold11機・fold12機・fold12 receipt・K1108監査・K1108証明書）を
   配置SHA照合込みで再構成。
2. K1175検証機（655 gate）を土台にしたfold13固有の外科手術で、チェーン再構成を
   fold12レコードまでの9段に拡張し、coverage照合を余剰6行（主張3＋余剰6の計9行）に、
   5親影響gateをc4×3/c2×2・合計15 row-closingsに、レシート定数群
   （合法手57・root 9840004・証明書45,286行）を差し替えた。
3. tamper offset（@117,777/@777,777）はfold12 ext2レーンのもの（@96,300/@456,789）と
   独立に選んだ。いずれも出版社が未試験の位置である。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-fold13-external-second-verification-single-owner-note.md`
  （commit `5a9e814294`・fetch-back byte一致）。
- part1（実験dir 5ファイル・3分割push）: commit `f2fe7d58e9`（README・再構成機・
  reproduction.log）→ `dffc4af0c1`（検証機）→ `51d86169c1`（監査正本）・
  fetch-back 5/5 byte一致。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はfold13出版の簿記・決定性・入力pin・fail-closed防衛の再検査であり、行は1行も
閉じない（fold13時点残余65→62行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて
UNKNOWNのままである。**
