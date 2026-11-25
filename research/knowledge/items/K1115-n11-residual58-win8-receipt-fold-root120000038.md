---
id: K1115
title: 残余58行のWIN8-D10 receipt fold root 120000038（fold15・第22 receipt・5番目のWIN8 receipt fold・初の53手mobility候補fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold15 WIN8 receipt fold root 120000038
  - K1114証明書の五親frontierチェーンへのfoldと残余58→55行
relations:
  - type: depends_on
    target: K1114
    note: WIN8-D10証明書（root 00000000012000003800080009000000・32,470行・SHA-256 5a135903…・loser初手53手・主張3行の候補抽出・三重検証）と19 gate監査正本（ab8cd535…）
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1111
    note: fold14正本（SHA-256 ed3159fd…）。fold15機械はfold14出版機械を隔離W複写でbyte-identical再実行した上でfold14レコードをchainingした
  - type: depends_on
    target: K1086
    note: addtwo-greedy23掃引のroot 120000038 probe記録（両AND順序uncapped 825,127/657,152・loss=true・terminal石数[14,18]）とgreedy被覆3行の主張源（g01 master SHA pin 3045e152…）
artifacts:
  - path: research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/scripts/fold_win8_root120000038.py
    role: verifier
    note: 純Python・乱数なし・825行。チェーン全段frontier再計算・fold11/fold12/fold13/fold14再実行gate・K1114/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/output/win8-root120000038-receipt-fold-20261120.json
    role: data
    note: fold15正本（status fold-complete・SHA-256 bae2b3c1…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold15-win8-root120000038-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold15-win8-root120000038-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 3f149dc3・先行出版）
---

# 残余58行のWIN8-D10 receipt fold root 120000038（fold15・第22 receipt）

K1114のWIN8-D10証明書（root `00000000012000003800080009000000`・32,470行・SHA-256 `5a135903…`・K1086掃引由来の53手mobility・主張3行候補・三重検証・19 gate）を、五親S6 frontier receiptチェーンの第22 receiptとしてfoldした。

## 主要結果

- **receipt は open 6 行を閉じた**（初の53手mobility候補の fold）: K1114/K1086/K1097 主張 3 行（5親target内）+ target 外 open 行 3 行（同じ root の C(8,6) 28 部分集合幾何に内在・unswept）を併閉。宣言ノートの事前計算は target 交差（主張3行ちょうど）しか見ておらず、宣言の閉鎖予測「主張3行のみ」は target 外 open 3 行を見落としていた。機械が open frontier 全体との交差で 6 行を閉じ、余剰 3 行を正確に記録した（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 486・5親 112 行 target 54 → 57・残余 58 → 55 行・frontier 6,179/489,440 → 6,173/488,954・solved S6 1,669 → 1,675・parent 行 incidence 11,765 → 11,753（影響 4 parent・全 c2・完全閉鎖 0）・s6_needed_by_open_classes 4,487 → 4,481・cost_needed 355,888 → 355,402。
- fold14 出版機械を隔離 W 複写（FOLD14_W）で byte-identical 再実行してから接続した（published 正本 SHA-256 `ed3159fd…` と一致 gate・fold13→fold12→fold11 再帰 rerun 含め 5 機連鎖 rerun）。
- K1114 監査の root 固有定数を gate 名ごと差し替え: g07 3行版（`g07_k1086_root_claimed_coverage_3rows`・`== 3` 定数・`recorded.k1086_claimed_coverage_rows` 二重照合）・g05 mobility 53・g06 uncapped probes 825,127/657,152 に terminal 石数範囲 [14,18] を追加固定・g01 K1086 master SHA pin・g16 miss 0/extra 0 を新規固定・g13 nodes 2,723,200/2,141,807・g19 footprint 3 行。
- 正本（SHA-256 `bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef`）は同一 cwd 2 回 + 別 cwd・別プロセス・別 HOME 1 回の 3 実行で byte-identical（GATE FAILED 0・約 23 秒/実行）。
- win16 候補は 12 → 11 根（主張 35 → 32 行）。残余23行掃引計画は不変。残り候補には K1113 root `…889002`（並走出版済み・fold16 候補・着手時に宣言必要）と K1086 第 7 候補 `…8180000`（並走が抽出宣言済み）を含む。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残り 11 WIN8 候補の証明書抽出・残余 55 行の refsolve・fold16（K1113 root）は着手時に単一オーナー宣言を要する未着手領域。
