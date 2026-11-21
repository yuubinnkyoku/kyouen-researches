---
id: K1114
title: 残余58行のWIN8-D10証明書抽出 root 120000038（三重検証・19 gate・mobility 53）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 120000038
  - 残余58行WIN8候補未宣言次安価8石rootの完全勝利戦略32,470行
relations:
  - type: depends_on
    target: K1085
    note: K1086 addtwo-greedy23掃引の入力census。本項ではK1086正本（SHA-256 3045e152…）のper_root記録を直接pin
  - type: depends_on
    target: K1086
    note: 両AND順序uncapped probe（657,152/825,127・loss=true）の出版値を本環境でnode-exact再現
  - type: depends_on
    target: K1096
    note: 抽出器・BigInt検証器・Bareiss検証器・監査機械の機材はK1096実験과同一bytes（root定数のみ差し替え）
  - type: depends_on
    target: K1097
    note: "win16 footprint（root 120000038: claimed == intrinsic == 3行）をg19で照合。"
  - type: depends_on
    target: K1109
    note: 抽出器・監査機械の直接の前段。K1109出版機材のroot差し替え版として本項を構成
  - type: depends_on
    target: K1111
    note: fold14後の残余58行レーンで実施。主張3行がfold14正本residual_row_hex_afterに全て残存
  - type: depends_on
    target: K1113
    note: 並走レーンの前段抽出root 00000000010000889002000080100000とは別root・独立プロセス
artifacts:
  - path: research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/certs/win8-root-00000000012000003800080009000000-20261120.n11
    role: certificate
    note: 1,171,958 bytes・32,470行・SHA-256 5a135903…
  - path: research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 ab8cd535…）
  - path: research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/scripts/cert_extractor_win8_root120000038.ts
    role: source
    note: K1109抽出器のroot差し替え版（探索核同一bytes・diff 6行）
  - path: research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/scripts/assemble_win8_audit_root120000038.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・g19継承（len 3行）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000012000003800080009000000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 26c88746・先行出版）
  - path: research/log/2026-11-20-n11-residual58-win8-cert-extract-root120000038.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 120000038 証明書抽出・三重検証

単一オーナー宣言ノート（commit `26c88746b24dc510cb42f3cd64ec0ee746f6da06`・先行出版）の
下で、K1086 addtwo-greedy23掃引が両AND順序 uncapped（andclose1 657,152・
andclose0 825,127・どちらも loss=true・terminal石数 [14,18]）で WIN8-D10 candidate
として確定した8石root `00000000012000003800080009000000`（石
[24,27,43,59,60,61,85,88]・quadruple-free・**loser初手53手**）に対して、
完全勝利戦略証明書の盲抽出と三重検証を行った。fold14（K1111）後の残余58行レーンで、
並走宣言済み3根（`…8180000`・`…0810000a`・K1113の `…889002…80100000`）と抽出・
fold済み4根（`…8003180`・`…8005021`・`…9840004`・`…9090022`）を除く
次安価の未宣言根である（主張3行はfold14正本の残余58行に全て残存）。

**結果**: 証明書 32,470行・1,171,958 bytes（SHA-256
`5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c`・3実行
行集合完全一致）。抽出は A1（初手毎53プロセス・総nodes 2,723,200・最大初手
bit 110 の223,518・fbt_drops 0）・A2（完全再実行・初手単位node-exact一致・
行bytes一致）・B（単一プロセス・別cwd・総nodes 2,141,807・行集合不変）の3実行で
行集合が完全一致。三重検証（TS BigInt 3×3余因子・TS Bareiss 4×4・python第三方法
全木再走査）が visited 69,115・winner-to-move 44,580・ loser-to-move 13,197・
loser応手辺 61,058・終端 11,338（全てloser-stuck）・終端石数 [14,18]・
consumed union 32,470 == 証明書行（missing 0/extra 0）の全数値で一致。
監査機械（K1109機械のroot定数差し替え・g19継承）は**19/19 gate PASS**
（probe再現のK1086出版値node-exact一致・root mobility 53の独立再導出・
行format sorted-unique・証明書SHA pin・K1097 win16 footprint三点一致を含む）で、
同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical（SHA-256 `ab8cd535…`）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
