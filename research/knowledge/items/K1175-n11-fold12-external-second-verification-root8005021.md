---
id: K1175
title: "fold12 receipt fold（root 8005021）単体の外部第二検証（K1173系列）"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold12 external second verification root8005021"
  - "fold19番receipt・2番目WIN8 receipt foldの第三実装再検証 655 gate"
  - "監査正本 c309d693…（3実行byte一致）・fold11機独立rerun d7bf2cd5…再現・erratum記録（IV.source_recordのfold11実験参照残存）"
relations:
  - type: depends_on
    target: K1106
    note: "検証対象証明書群。root 8005021のWIN8-D10証明書（69f32661…・945,298 bytes・26,083行）と19 gate監査（0bd2dd10…）をW pin・値単位再照合・tamperの対象。"
  - type: depends_on
    target: K1097
    note: "refsolve正本（2896deb0…・27 gate・win16 footprint 49行exactly-once・残余23行）がfootprint partition再照合の対象。"
  - type: related
    target: K1173
    note: "fold20外部第二検証（K1129対象）と同一手続き系列（byte pin・W再構成・pristine 4回・tamper・決定的監査）。fold12機のrerun gate対象はfold11出版機（fold_win8_root8003180.py・9b3e06c8…）とfold11 receipt（d7bf2cd5…）。"
  - type: related
    target: K1174
    note: "K1173第三検証と同じく、外部第二検証publicationの決定性・再現性検査系列に属する。"
artifacts:
  - path: research/experiments/n11-fold12-external-second-verification-root8005021-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・erratum・再現手順・限界"
  - path: research/experiments/n11-fold12-external-second-verification-root8005021-20261121/scripts/reconstruct_fold12_inputs.py
    role: reconstruction
    note: "W12/pub12再構成機（静的raw URL固定commitのみ・api.github.com非依存・全pin fail-closed・fold11機pin表の部分集合性機械確認・SHA-256 caa30f34…）"
  - path: research/experiments/n11-fold12-external-second-verification-root8005021-20261121/scripts/verify_fold12_external_20261121.py
    role: verifier
    note: "独立第三実装検証機（fold20版からの外科手術でなく新規機: 655 gate・stdlibのみ・乱数・時刻なし・SHA-256 43afc1cd…・53,934 bytes）"
  - path: research/experiments/n11-fold12-external-second-verification-root8005021-20261121/output/external-audit.json
    role: audit
    note: "監査正本（70,149 bytes・655 gate全PASS・SHA-256 c309d693…・3実行byte一致・erratum記録欄）"
  - path: research/experiments/n11-fold12-external-second-verification-root8005021-20261121/output/reproduction.log
    role: record
    note: "実行記録（X/V/T実行matrix・gate内訳・実験注記）"
  - path: research/log/2026-11-21-n11-fold12-external-second-verification-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit de32ca57…・宣言 2026-11-21T00:41:00Z・受入条件6項目）"
  - path: research/log/2026-11-21-n11-fold12-external-second-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照・実験事実"
---

# fold12 receipt fold（root 8005021）単体の外部第二検証

## 概要

単一オーナー宣言（commit `de32ca573b`・宣言 2026-11-21T00:41:00Z・受入条件6項目）の下、
fold12 receipt fold（第十九 receipt・2番目WIN8 receipt fold・root
`00000000000000003800000008005021`・出版実験
`research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/`）の
出版byte・W入力25 pin・チェーン簿記・幾何主張・fail-closed防衛を、repo出版byteのみから
**第三実装**の検証機で独立に再検証した。K1173（fold20/K1129対象）と同一手続き系列の
fold receipt外部第二検証であり、fold13〜fold16の単体ext2（root 9840004/9090022/
120000038/8890020）より先にfold12（2番目WIN8 fold・単一WIN8 receiptとして最多の
open 8行閉鎖）を閉じた。

## 主な結果

- **全655 gate PASS**（P 12 / I 34 / C 571 / X 24 / T 14）。監査正本 `c309d693…`
  （70,149 bytes）が同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random` の3実行で
  byte-identical。検証機 `43afc1cd…` はfold12機・fold11機とコードを共有しない
  新規の第三実装（D4表・det4・合法手survival規約・chain_step集計を独自実装）。
- **W入力25 pin（12 Git blob SHA-1 + 13 SHA-256）をapi.github.comなしで再構成**:
  検証レーンの固有成果として、未解決だったworklist（`2fee1d07…`→closability-ranking実験の
  `class-frontier-remaining-s6-worklist-1410-20261116.csv`）・ledger（`e8785d50…`→
  head1410実験の `fold-chain-ledger-1410-1476-crosscheck-20261118.json`）・audit
  （`7cdc7c9e…`→head1410実験の `joint-cover-cost16-five-parent-independent-audit-20261118.json`）
  の3 blobのrepo内所在を静的パス探索で特定し、raw固定commit URL+blob/SHA-256照合で解決。
  再構成機はapi依存ゼロで全25 pin+fold11機（`9b3e06c8…`）をfail-closed配置し、
  fold11機pin表（12 blob + 10 sha256）のfold12機pin表に対する部分集合性を機械確認。
- **fold12出版機pristine再実行4回**（同一W 2回・隔離copytree W/cwd/HOME・隔離+
  `PYTHONHASHSEED=random`）すべて、receipt出力が出版正本 `0f73795c…` とbyte-identical。
  各回の機内fold11 rerun gate出力も出版fold11正本 `d7bf2cd5…` とbyte一致。
  加えてfold11出版機を隔離W複写上で検証機側から独立実行し `d7bf2cd5…` を再現
  （宣言受入条件3の外側確認）。実行環境note: 全runとも `FOLD12_W` をbyte-pinned W12
  （またはその完全複写）に明示指定（K1173の `FOLD20_W` matrixと同一形式）。
- **チェーン全段の第三実装再構成**: base worklist 6,438行（cost 509,109）→
  globalFold 6,259/495,507 → cost78c/79c → first fold → second-third → fourth →
  fifth-sixth → seventh → eighth → ninth-twelfth（4 receipt）→ windfall4 13th-16th
  （6,209/491,722・残余74・target 38）→ seventeenth fold10（6,206/491,497・target 40）→
  WIN8 fold11（6,201/491,110・solved 1,647・incidence 11,803・残余68・target 44）
  まで、8出版記録を段ごとに再計算しpublished値と照合。
- **fold12 receipt主張の値単位再導出**: 28 canonical行=2方法一致
  （8 D4像×C(8,2) 224操作とC(8,6)=28部分集合・D4同変性）、分類open 8/not-in-worklist 20、
  coverage 8行=K1106 g07主張3行＋余剰5行・closed edge cost 584・影響5親
  （c1 3: 58→56/65→63/75→72・c2 2: 44→41/25→22・完全閉鎖0・合計13 row-closings）、
  frontier_after 6,193/490,526・solved 1,655・incidence 11,790・needed 4,501/356,974、
  五親target 44→47・残余68→65（65行hex全列挙照合）、win16候補 15→14根（主張45→42行・
  残余23行不交差・rootのgreedy_selection非含有）、K1106 19 gate主要値
  （g06 probes 619,138/751,581・terminalRange [14,18]・g13 nodes 3,272,039/2,876,091・
  証明書 945,298 bytes 26,083行 sorted unique・third_method terminal 10,191/
  visited 59,594/winner 38,442/loser 10,961/応手辺 53,352）・root合法手41のsurvival規約
  独立再導出（quadruple-free・D4正準込み）、K1097 27 gate・49行exactly-once partition。
- **tamper 2件fail-closed**（本レーン選択・出版社未試験offset）: worklist @96,300
  （blob pin）・K1106証明書 @456,789（sha256 pin）の1 byte XOR 0x01がrc≠0・
  fold12/fold11出力とも未書込で捕捉。本番Wは両実施後に無改変再照合。
- **erratum記録（文書フィールドのみ・byte pin対象外）**: 出版receiptの
  `independent_verification.source_record` がfold11証明書抽出実験
  （`n11-residual72-win8-cert-extract-root8003180-20261120`・root 8003180）を指した
  ままで、K1106（root 8005021）を指していない。fold12機sourceの固定文字列由来。
  `certificate_source` ブロック・全sha pin・幾何・統計的主張はすべて正しく、
  監査JSONのobservations欄に記録した（検証の失敗ではなく出版側の記載エラー）。

## 実験事実

1. api.github.com無認証quotaの共有IP枯渇（403・01:04:10Z回復予定）がrecon中に再発したが、
   trees API依存をやめ全入力を静的raw固定commit URLで取得する設計（blob/SHA照合込み）に
   切り替えたことで待機ゼロでW12を再構成できた。quota枯渇はK1173/K1174と同型・
   「静的URL fallbackの再構成機」の価値を実証（以降のfold13-16単体ext2にそのまま適用可能）。
2. fold12 receiptのIV.source_record記載エラー（fold11実験パス残存）を第三実装検証で特定。
   機械可読な全統計値は正しく、文書1フィールドのみの stale reference。
3. fold20検証機（K1173）のC1チェーン再構成をそのまま流用するとfold12では不要な
   chain_step（fold12〜19記録を読む）まで含む設計になるため、fold11までで打ち切る
   外科手術を行った。C4の「閉鎖行はclass-1 demandゼロ」gateはfold20固有（余剰行の
   要求構成がfold12では異なる）のため、5親の分類別件数gate（c1×3/c2×2・合計13）に
   置き換えた。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-fold12-external-second-verification-single-owner-note.md`
  （commit `de32ca573b`・fetch-back byte一致）。
- part1（実験dir 5ファイル・3分割push）: commit `20e5f2f215`（README・再構成機・
  reproduction.log）→ `984c48a767`（検証機）→ `adb1e8f605`（監査正本）・fetch-back 5/5 byte一致。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はfold12出版の簿記・決定性・入力pin・fail-closed防衛の再検査であり、行は1行も
閉じない（fold12時点残余68→65行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて
UNKNOWNのままである。**
