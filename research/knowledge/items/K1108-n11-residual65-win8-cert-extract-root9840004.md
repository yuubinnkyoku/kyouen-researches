---
id: K1108
title: 残余65行のWIN8-D10証明書抽出 root 9840004（三重検証・19 gate・45,286行はn11証明書最大）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 9840004
  - 残余65行WIN8候補最安価8石rootの完全勝利戦略45,286行
relations:
  - type: depends_on
    target: K1085
    note: K1086 addtwo-greedy23掃引の入力census。本項ではK1086正本（SHA-256 3045e152…）のper_root記録を直接pin
  - type: depends_on
    target: K1086
    note: 両AND順序uncapped probe（1,143,198/1,528,656・loss=true）の出版値を本環境でnode-exact再現
  - type: depends_on
    target: K1096
    note: 抽出器・BigInt検証器・Bareiss検証器・監査機械の機材はK1096実験と同一bytes（root定数のみ差し替え）
  - type: depends_on
    target: K1097
    note: "win16 footprint（root 9840004: claimed == intrinsic == 3行）をg19で照合。"
  - type: depends_on
    target: K1107
    note: fold12直後の残余65行レーン。root 8005021のfoldとは別root・独立プロセス
artifacts:
  - path: research/experiments/n11-residual65-win8-cert-extract-root9840004-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual65-win8-cert-extract-root9840004-20261120/certs/win8-root-00000000000000003800000009840004-20261120.n11
    role: certificate
    note: 1,640,220 bytes・45,286行・SHA-256 5b114b9e…
  - path: research/experiments/n11-residual65-win8-cert-extract-root9840004-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 2e453a76…）
  - path: research/experiments/n11-residual65-win8-cert-extract-root9840004-20261120/scripts/cert_extractor_win8_root9840004.ts
    role: source
    note: K1096抽出器のroot差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual65-win8-cert-extract-root9840004-20261120/scripts/assemble_win8_audit_root9840004.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・g19継承
  - path: research/log/2026-11-20-n11-win8-cert-extract-root9840004-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 45920e13・先行出版）
  - path: research/log/2026-11-20-n11-residual65-win8-cert-extract-root9840004.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 9840004 証明書抽出・三重検証

単一オーナー宣言ノート（commit `45920e13edb746f4867524e7160baf3f0ff15492`・先行出版）の
下で、K1086 addtwo-greedy23掃引が両AND順序 uncapped（andclose1 1,143,198・
andclose0 1,528,656・どちらも loss=true）で WIN8-D10 candidate として確定した
8石root `00000000000000003800000009840004`（石 [2,18,23,24,27,59,60,61]・
quadruple-free・D4正準・loser初手57手）に対して、完全勝利戦略証明書の盲抽出と
三重検証を行った。fold12（K1107）直後の残余65行レーンで、証明済み2根
（K1096/K1106）と並走宣言済み2根を除く候補中で抽出費用が最安価の未着手根である。

**結果**: 証明書 45,286行・1,640,220 bytes（SHA-256
`5b114b9e739b7a0a300434afb7ec5326564fc54b0d234df5e3d61abc44541143`・3実行
byte-identical・n11-terminal-strategy-v1全証明書中で最大行数）。抽出は
A1（初手毎57プロセス・総nodes 4,109,768・fbt_drops 0）・A2（完全再実行・初手単位
node-exact一致）・B（単一プロセス・総nodes 3,075,922・戦略行不変）の3実行で
行集合が完全一致。三重検証（TS BigInt 3×3余因子・TS Bareiss 4×4・python第三方法
全木再走査）が visited 103,531・winner-to-move 66,627・loser-to-move 19,571・
loser応手辺 91,337・終端 17,333（全てloser-stuck）・終端石数 [14,18]・
consumed union 45,286 == 証明書行（missing 0/extra 0）の全数値で一致。
監査機械（K1106機械のroot差し替え・g19継承）は**19/19 gate PASS**
（probe再現のK1086出版値node-exact一致・root mobility 57の独立再導出・
行format sorted-unique・証明書SHA pin・K1097 win16 footprint三点一致を含む）で、
同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical（SHA-256 `2e453a76…`）。

K番号はpush直前3点確認（git trees recursive走査・README grep・list_commits）で
K1108を取得した（K1107は前段の当レーン使用済み）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold（fold13候補）は別工程であり、行の閉鎖claimは本項では行わない。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
