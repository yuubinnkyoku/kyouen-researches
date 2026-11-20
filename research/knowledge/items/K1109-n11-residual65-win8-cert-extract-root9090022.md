---
id: K1109
title: 残余65行のWIN8-D10証明書抽出 root 9090022（三重検証・19 gate・主張4行の候補初抽出）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 9090022
  - 残余65行WIN8候補次安価8石rootの完全勝利戦略29,942行
relations:
  - type: depends_on
    target: K1085
    note: K1086 addtwo-greedy23掃引の入力census。本項ではK1086正本（SHA-256 3045e152…）のper_root記録を直接pin
  - type: depends_on
    target: K1086
    note: 両AND順序uncapped probe（512,590/614,246・loss=true）の出版値を本環境でnode-exact再現
  - type: depends_on
    target: K1096
    note: 抽出器・BigInt検証器・Bareiss検証器・監査機械の機材はK1096実験と同一bytes（root定数のみ差し替え）
  - type: depends_on
    target: K1097
    note: win16 footprint（root 9090022: claimed == intrinsic == 4行）をg19で照合。
  - type: depends_on
    target: K1108
    note: 同一実行内の前段抽出root 9840004（fold13候補）とは別root・独立プロセス
artifacts:
  - path: research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120/certs/win8-root-00000000000000909002200080100000-20261120.n11
    role: certificate
    note: 1,082,873 bytes・29,942行・SHA-256 b8a15f9a…
  - path: research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 00836a6e…）
  - path: research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120/scripts/cert_extractor_win8_root9090022.ts
    role: source
    note: K1096抽出器のroot差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120/scripts/assemble_win8_audit_root9090022.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・g19継承（len 4行）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root9090022-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 02020572・先行出版）
  - path: research/log/2026-11-20-n11-residual65-win8-cert-extract-root9090022.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 9090022 証明書抽出・三重検証

単一オーナー宣言ノート（commit `0202057295a20f3c3c3e99036014697f34eecb58`・先行出版）の
下で、K1086 addtwo-greedy23掃引が両AND順序 uncapped（andclose1 512,590・
andclose0 614,246・どちらも loss=true）で WIN8-D10 candidate として確定した
8石root `00000000000000909002200080100000`（石 [20,31,45,49,60,63,68,71]・
quadruple-free・D4正準・loser初手50手）に対して、完全勝利戦略証明書の盲抽出と
三重検証を行った。fold12（K1107）直後の残余65行レーンで、K1108（root 9840004）
の次に安価な未着手根である（主張4行はWIN8候補として最多タイのclaimer）。

**結果**: 証明書 29,942行・1,082,873 bytes（SHA-256
`b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54`・3実行
byte-identical）。抽出は A1（初手毎50プロセス・総nodes 6,102,650・fbt_drops 0）・
A2（完全再実行・初手単位node-exact一致）・B（単一プロセス・総nodes 6,102,650・
戦略行不変）の3実行で行集合が完全一致。三重検証（TS BigInt 3×3余因子・
TS Bareiss 4×4・python第三方法全木再走査）が visited 65,134・winner-to-move 42,115・
loser-to-move 12,780・loser応手辺 58,084・終端 10,239（全てloser-stuck）・
終端石数 [14,18]・consumed union 29,942 == 証明書行（missing 0/extra 0）の
全数値で一致。監査機械（K1108機械のroot差し替え・g19継承）は**19/19 gate
PASS**（probe再現のK1086出版値node-exact一致・root mobility 50の独立再導出・
行format sorted-unique・証明書SHA pin・K1097 win16 footprint三点一致を含む）で、
同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical（SHA-256 `00836a6e…`）。

K番号はpush直前3点確認（git trees recursive走査・README grep・list_commits）で
K1109を取得した（K1108は前段の当レーン使用済み）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
