---
id: K1116
title: 残余55行のWIN8-D10 receipt fold root 8890020（fold16・第23 receipt・6番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold16 WIN8 receipt fold root 8890020
  - K1113証明書の五親frontierチェーンへのfoldと残余55→51行
relations:
  - type: depends_on
    target: K1113
    note: WIN8-D10証明書（root 00000000010000889002000080100000・21,446行・SHA-256 105e1e2a…・loser初手50手・主張4行の候補抽出・三重検証）と19 gate監査正本（b8c264e6…）
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張4行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1115
    note: fold15正本（SHA-256 bae2b3c1…・残余58→55）。fold16機械はfold15出版機械を隔離W複写でbyte-identical再実行した上でfold15レコードをchainingした
  - type: depends_on
    target: K1086
    note: 掃引のroot 8890020 probe記録（両AND順序uncapped 575,570/409,407・loss=true・terminal石数[14,18]）と主張4行の主張源（g01 master SHA pin 3045e152…）
artifacts:
  - path: research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/scripts/fold_win8_root8890020.py
    role: verifier
    note: 純Python・乱数なし・883行。チェーン全段frontier再計算・fold11〜15再実行gate・K1113/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/output/win8-root8890020-receipt-fold-20261120.json
    role: data
    note: fold16正本（status fold-complete・SHA-256 edd55258…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold16-win8-root8890020-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold16-win8-root8890020-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit d6a65fff・先行出版）
---

# 残余55行のWIN8-D10 receipt fold root 8890020（fold16・第23 receipt）

K1113のWIN8-D10証明書（root `00000000010000889002000080100000`・21,446行・SHA-256 `105e1e2a…`・K1086掃引由来の50手mobility・主張4行候補・K1097 win16 footprint intrinsic == claimed == 4行・三重検証・19 gate）を、五親S6 frontier receiptチェーンの第23 receiptとしてfoldした。

## 主要結果

- **receipt は open 5 行を閉じた**: K1113/K1086/K1097 主張 4 行（5親target内・cost 74/67/81/75）+ target 外 open 1 行（`00000000000000801222000100000000`・cost 82・同じ root の C(8,6) 28 部分集合幾何に内在・unswept）を併閉。余剰 1 行は `extra_s6_rows_not_in_target` として機械が分離記録（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 379・5親 112 行 target 57 → 61・残余 55 → 51 行・frontier 6,173/488,954 → 6,168/488,575・solved S6 1,675 → 1,680・parent 行 incidence 11,753 → 11,743（影響 4 parent・全 c2・完全閉鎖 0）・s6_needed_by_open_classes 4,481 → 4,476・cost_needed 355,402 → 355,023。
- fold15 出版機械を隔離 W 複写（FOLD15_W）で byte-identical 再実行してから接続した（published 正本 SHA-256 `bae2b3c1…` と一致 gate・fold14→fold13→fold12→fold11 再帰 rerun 含め 6 機連鎖 rerun）。
- K1113 監査の root 固有定数を gate 名ごと差し戻し: g07 4行版（`g07_k1086_root_claimed_coverage_4rows`・`== 4` 定数・`recorded.k1086_claimed_coverage_rows` 二重照合）・g05 mobility 50・g06 uncapped probes 575,570/409,407 と terminal 石数範囲 [14,18]・g01 K1086 master SHA pin・g16 miss 0/extra 0・g13 nodes 4,424,758/4,424,758・g19 footprint 4 行。
- 正本（SHA-256 `edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b`）は同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical（GATE FAILED 0・約 47 秒/実行）。
- 実装中の転写ミス 1 件（fold15 正本 SHA の一文字取り違え `da0`→`da6`）は初回実行の `input sha256 mismatch` fail-close が即座に捕捉し、raw 再取得で修正した（fail-closed 実効性の実証記録）。
- win16 候補は 11 → 10 根（主張 32 → 28 行）。残余23行掃引計画は不変。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残り 10 WIN8 候補の証明書抽出・残余 51 行の refsolve は着手時に単一オーナー宣言を要する未着手領域。
