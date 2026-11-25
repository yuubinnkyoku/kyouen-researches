---
id: K1118
title: 残余51行のWIN8-D10 receipt fold root 22081000（fold17・第24 receipt・7番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold17 WIN8 receipt fold root 22081000
  - K1117証明書の五親frontierチェーンへのfoldと残余51→48行
relations:
  - type: depends_on
    target: K1117
    note: WIN8-D10証明書（root 00000000000000801202000022081000・9,460行・SHA-256 f62f6704…・loser初手39手=歴代最小mobility・主張3行の候補抽出・三重検証・並走レーン出版）と19 gate監査正本（3d97ac6d…）
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1116
    note: fold16正本（SHA-256 edd55258…・残余55→51）。fold17機械はfold16出版機械を隔離W複写でbyte-identical再実行した上でfold16レコードをchainingした
  - type: depends_on
    target: K1095
    note: 掃引のroot 22081000 probe記録（両AND順序uncapped 126,683/137,565・loss=true・terminal石数[14,18]）と主張3行の主張源（g01 master SHA pin 335eca5e…）
artifacts:
  - path: research/experiments/n11-residual51-win8-receipt-fold-root22081000-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual51-win8-receipt-fold-root22081000-20261120/scripts/fold_win8_root22081000.py
    role: verifier
    note: 純Python・乱数なし・943行。チェーン全段frontier再計算・fold11〜16再実行gate・K1117/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual51-win8-receipt-fold-root22081000-20261120/output/win8-root22081000-receipt-fold-20261120.json
    role: data
    note: fold17正本（status fold-complete・SHA-256 1175244d…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold17-win8-root22081000-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold17-win8-root22081000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 7f824364・先行出版）
---

# 残余51行のWIN8-D10 receipt fold root 22081000（fold17・第24 receipt）

K1117のWIN8-D10証明書（root `00000000000000801202000022081000`・9,460行・SHA-256 `f62f6704…`・K1095掃引由来の39手mobility=歴代抽出根最小・主張3行候補・K1097 win16 footprint intrinsic == claimed == 3行・三重検証・19 gate・並走レーン出版）を、五親S6 frontier receiptチェーンの第24 receiptとしてfoldした。

## 主要結果

- **receipt は open 7 行を閉じた**（単一 WIN8 receipt としては fold10 の 9 行に次ぐ規模）: K1117/K1095/K1097 主張 3 行（5親target内・cost 73/66/74）+ target 外 open 4 行（`00000000000000801002000002081000` cost 64・`00000000000000801002000002102000` cost 64・`00000000000000801002000022002000` cost 70・`00000000000000801202000020080000` cost 70・同じ root の C(8,6) 28 部分集合幾何に内在・unswept・余剰4行はWIN8 receipt史上最多）を併閉。余剰 4 行は `extra_s6_rows_not_in_target` として機械が分離記録（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 481・5親 112 行 target 61 → 64・残余 51 → 48 行・frontier 6,168/488,575 → 6,161/488,094・solved S6 1,680 → 1,687・parent 行 incidence 11,743 → 11,729（影響 6 parent: c2/c4/c6〔18→15・79→76・49→48・67→64・50→48・37→35〕・完全閉鎖 0）・s6_needed_by_open_classes 4,476 → 4,469・cost_needed 355,023 → 354,542。
- fold16 出版機械を隔離 W 複写（FOLD16_W）で byte-identical 再実行してから接続した（published 正本 SHA-256 `edd55258…` と一致 gate・fold15→fold14→…→fold11 再帰 rerun 含め 7 機連鎖 rerun）。
- K1117 監査の root 固有定数を gate 名ごと差し替え: g07 3行版（`g07_k1095_root_claimed_coverage_3rows`・`== 3` 定数・`recorded.k1095_claimed_coverage_rows` 二重照合）・g05 mobility 39・g06 uncapped probes 126,683/137,565 と terminal 石数範囲 [14,18]・g01 K1095 master SHA pin・g16 miss 0/extra 0・g13 nodes 731,232/534,121・g19 footprint 3 行。
- 正本（SHA-256 `1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674`）は同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical（GATE FAILED 0・約 95 秒/実行・43 input pin 全て初回実行で一度に検証）。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 7（本 receipt で閉鎖）・not-in-worklist 21・closed-before-this-receipt 0（初めて 0 になった root）。
- win16 候補は 10 → 9 根（主張 28 → 25 行）。残余23行掃引計画は不変。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残り 9 WIN8 候補の証明書抽出・残余 48 行の refsolve は着手時に単一オーナー宣言を要する未着手領域。
