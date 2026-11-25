---
id: K1111
title: 残余62行のWIN8-D10 receipt fold root 9090022（fold14・第21 receipt・4番目のWIN8 receipt fold・初の4主張行候補fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold14 WIN8 receipt fold root 9090022
  - K1109証明書の五親frontierチェーンへのfoldと残余62→58行
relations:
  - type: depends_on
    target: K1109
    note: WIN8-D10証明書（root 00000000000000909002200080100000・29,942行・SHA-256 b8a15f9a…・主張4行の候補初抽出）と19 gate監査正本（00836a6e…）
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張4行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1110
    note: fold13正本（SHA-256 c2bf8051…）。fold14機械はfold13出版機械を隔離W複写でbyte-identical再実行した上でfold13レコードをchainingした
  - type: depends_on
    target: K1086
    note: addtwo-greedy23掃引のroot 9090022 probe記録（両AND順序uncapped 512,590/614,246・loss=true）とgreedy被覆4行の主張源
artifacts:
  - path: research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/scripts/fold_win8_root9090022.py
    role: verifier
    note: 純Python・乱数なし・752行。チェーン全段frontier再計算・fold11/fold12/fold13再実行gate・K1109/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/output/win8-root9090022-receipt-fold-20261120.json
    role: data
    note: fold14正本（status fold-complete・SHA-256 ed3159fd…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold14-win8-root9090022-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold14-win8-root9090022-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 48ad9c7d・先行出版）
---

# 残余62行のWIN8-D10 receipt fold root 9090022（fold14・第21 receipt）

K1109のWIN8-D10証明書（root `00000000000000909002200080100000`・29,942行・SHA-256 `b8a15f9a…`・主張4行の候補として初の抽出・三重検証・19 gate）を、五親S6 frontier receiptチェーンの第21 receiptとしてfoldした。

## 主要結果

- **receipt は open 5 行を閉じた**（初の 4 主張行候補の fold）: K1109/K1097 主張 4 行（5親 target 内）+ target 外 open 行 1 行（同じ root の C(8,6) 28 部分集合幾何に内在）を併閉。
- closed edge cost 373・5親 112 行 target 50 → 54・残余 62 → 58 行・frontier 6,184/489,813 → 6,179/489,440・solved S6 1,664 → 1,669・parent 行 incidence 11,775 → 11,765（影響 4 parent・全 c2・完全閉鎖 0）・s6_needed_by_open_classes 4,492 → 4,487・cost_needed 356,261 → 355,888。
- fold13 出版機械を隔離 W 複写（FOLD13_W）で byte-identical 再実行してから接続した（published 正本 SHA-256 `c2bf8051…` と一致 gate）。
- root の 6 石部分幾何 28 canonical 行の分類で初めて closed-before-this-receipt 行（`00000000000000003800000008003000`）が現れた。
- 正本（SHA-256 `ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71`）は同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical。
- win16 候補は 13 → 12 根（主張 35 行）。残余23行掃引計画（並走宣言済み）は不変。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残り 12 WIN8 候補の証明書抽出・残余 58 行の refsolve は着手時に単一オーナー宣言を要する未着手領域。
