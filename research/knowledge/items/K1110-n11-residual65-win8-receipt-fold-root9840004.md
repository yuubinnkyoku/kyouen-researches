---
id: K1110
title: 残余65行のWIN8-D10 receipt fold root 9840004（fold13・第20 receipt・3番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold13 WIN8 receipt fold root 9840004
  - K1108証明書の五親frontierチェーンへのfoldと残余65→62行
relations:
  - type: depends_on
    target: K1108
    note: WIN8-D10証明書（root 00000000000000003800000009840004・45,286行・SHA-256 5b114b9e…・n11最大）と19 gate監査正本（2e453a76…）。証明自体は本項で再実行せずhash pin・gate再検証のみ
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1107
    note: fold12正本（SHA-256 0f73795c…）。fold13機械はfold12出版機械を隔離W複写でbyte-identical再実行した上でfold12レコードをchainingした
  - type: depends_on
    target: K1086
    note: addtwo-greedy23掃引のroot 9840004 probe記録（両AND順序uncapped 1,143,198/1,528,656・loss=true）とgreedy被覆3行の主張源
artifacts:
  - path: research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/scripts/fold_win8_root9840004.py
    role: verifier
    note: 純Python・乱数なし・701行。チェーン全段frontier再計算・fold11/fold12再実行gate・K1108/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/output/win8-root9840004-receipt-fold-20261120.json
    role: data
    note: fold13正本（status fold-complete・SHA-256 c2bf8051…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold13-win8-root9840004-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold13-win8-root9840004-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit d2521aa4・先行出版）
---

# 残余65行のWIN8-D10 receipt fold root 9840004（fold13・第20 receipt）

K1108のWIN8-D10証明書（root `00000000000000003800000009840004`・45,286行・SHA-256 `5b114b9e…`・n11-terminal-strategy-v1全証明書中最大行数・三重検証・19 gate）を、五親S6 frontier receiptチェーンの第20 receiptとしてfoldした。

## 主要結果

- **receipt は open 9 行を閉じた**（単一 WIN8 receipt として最多を更新）: K1108/K1097 主張 3 行（5親 target 内）+ target 外 open 行 6 行（同じ root の C(8,6)=28 部分集合幾何に内在）を併閉。
- closed edge cost 713・5親 112 行 target 47 → 50・残余 65 → 62 行・frontier 6,193/490,526 → 6,184/489,813・solved S6 1,655 → 1,664・parent 行 incidence 11,790 → 11,775（影響 5 parent・完全閉鎖 0）・s6_needed_by_open_classes 4,501 → 4,492・cost_needed 356,974 → 356,261。
- fold12 出版機械を隔離 W 複写（FOLD12_W）で byte-identical 再実行してから接続した（published 正本 SHA-256 `0f73795c…` と一致 gate）。
- 正本（SHA-256 `c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae`）は同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical。
- win16 候補は 14 → 13 根（主張 39 行）。残余23行掃引計画（並走宣言済み）は不変。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残り 13 WIN8 候補の証明書抽出・root 9090022 の receipt fold（fold14）・残余 62 行の refsolve は着手時に単一オーナー宣言を要する未着手領域。
