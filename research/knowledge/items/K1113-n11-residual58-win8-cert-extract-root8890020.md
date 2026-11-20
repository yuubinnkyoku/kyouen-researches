---
id: K1113
title: 残余58行のWIN8-D10証明書抽出 root 8890020（三重検証・19 gate・環境リセットを跨いだ決定的再現）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 8890020
  - 残余58行WIN8候補最安価8石rootの完全勝利戦略21,446行（K1113）
relations:
  - type: depends_on
    target: K1085
    note: K1086 addtwo-greedy23掃引の入力census。本項ではK1086正本（SHA-256 3045e152…）のper_root記録を直接pin
  - type: depends_on
    target: K1086
    note: 両AND順序uncapped probe（409,407/575,570・loss=true）の出版値を本環境でnode-exact再現
  - type: depends_on
    target: K1096
    note: 抽出器・BigInt検証器・Bareiss検証器・監査機械の機材系譜（K1096→K1108→K1109→本項まで機材同一bytes・root定数のみ差し替え）
  - type: depends_on
    target: K1097
    note: win16 footprint（root 8890020: claimed == intrinsic == 4行）をg19で照合。
  - type: depends_on
    target: K1109
    note: 抽出器・監査機械の直接の親機材（本項はK1109実験dirのroot差し替え版）。主張4行構成も同一（g07/g19の`== 4`定数が不変）
  - type: depends_on
    target: K1111
    note: fold14 root 9090022 receipt fold完了後の残余58行レーンで着手
artifacts:
  - path: research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/certs/win8-root-00000000010000889002000080100000-20261120.n11
    role: certificate
    note: 775,317 bytes・21,446行・SHA-256 105e1e2a…
  - path: research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 b8c264e6…）
  - path: research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/scripts/cert_extractor_win8_root8890020.ts
    role: source
    note: K1109抽出器のroot差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/scripts/assemble_win8_audit_root8890020.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・g19継承（len 4行）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00010000889002000080100000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 60e2940c・先行出版）
  - path: research/log/2026-11-20-n11-residual58-win8-cert-extract-root8890020.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 8890020 証明書抽出・三重検証

単一オーナー宣言ノート（commit `60e2940cf079c8e98efc9c0e72150835b87e5184`・先行出版）の
下で、K1086 addtwo-greedy23掃引が両AND順序 uncapped（andclose1 409,407・
andclose0 575,570・どちらも loss=true）で WIN8-D10 candidate として確定した
8石root `00000000010000889002000080100000`（石 [20,31,49,60,63,67,71,88]・
quadruple-free・D4正準・loser初手50手）に対して、完全勝利戦略証明書の盲抽出と
三重検証を行った。fold14（K1111）直後の残余58行レーンで、並走宣言済み2根
（`…8180000`・`…0810000a`）と抽出・fold済み4根（`…8003180`・`…8005021`・
`…9840004`・`…9090022`）を除く最安価の未着手根である（主張4行）。

**結果**: 証明書 21,446行・775,317 bytes（SHA-256
`105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4`・3実行
byte-identical）。抽出は A1（初手毎50プロセス・総nodes 4,424,758・最大初手
bit 14 937,490・fbt_drops 0）・A2（完全再実行・初手単位node-exact一致）・
B（単一プロセス・総nodes 4,424,758・戦略行不変）の3実行で行集合が完全一致。
三重検証（TS BigInt 3×3余因子・TS Bareiss 4×4・python第三方法全木再走査）が
visited 48,855・winner-to-move 31,320・loser-to-move 9,882・
loser応手辺 43,837・終端 7,653（全てloser-stuck）・
終端石数 [14,18]・consumed union 21,446 == 証明書行（missing 0/extra 0）の
全数値で一致。監査機械（K1109機械のroot差し替え・g19継承）は**19/19 gate
PASS**（probe再現のK1086出版値node-exact一致・root mobility 50の独立再導出・
行format sorted-unique・証明書SHA pin・K1097 win16 footprint三点一致を含む）で、
同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical（SHA-256 `b8c264e6…`）。

**環境リセットを跨いだ決定的再現**: 初回抽出一式（監査19 gate PASSまで）完了
直後に実行環境（Koyeb sandbox）が503 upstream resetで消失し、作業dirを喪失した。
repo出版済みのK1109実験dir機材（SHA pin照合）から全工程を再実行したところ、
証明書SHA-256・総nodes・全行集合・三重検査の全数値が初回と完全一致した
（抽出パイプライン全体の環境横断byte-exact再現。K1036の証明書SHA再現に続き、
監査JSON再構成を含む第2例）。

K番号はpush直前3点確認（list_commits・README grep・items 404）で
**K1113**を取得した（当初K1112は着手準備中に並走のy=4パラメトリック全称証明
（K1112・commits 3a3f48f950〜280f1155ce）が使用したため、衝突側再採番規約に
よって本項が再採番した）。また並走がroot `00000000012000003800080009000000`
の抽出を宣言済み（commit 26c88746b2）のため、同rootの抽出には着手しない。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
