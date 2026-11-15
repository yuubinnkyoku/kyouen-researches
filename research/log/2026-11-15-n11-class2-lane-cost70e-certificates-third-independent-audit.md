# 2026-11-15：cost-70e WIN7証明書5件の第三独立監査 — 5/5 PASS・236,784行・fold待ち・11×11はUNKNOWN

開始時main: `267417cdc`（cost-70e証明書part出版・cost-84 sterile・cost-86d claim着地後）。canonical chain headは **1227/6620/522561/4890/386284**（cost-69h foldがcost-78a head 1225にrebaseした形）。AGENTS.md、`research/knowledge/README.md`、K0783、直近のn11 log・experimentを確認した。規約どおりmainを直接更新し、branch / PRは作らない。

## 対象

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-70 child `00000000000000801202000000200004`（edge cost 70・需要 c1=0,c2=2,c4=0）に対するsweepの5 WIN7-D10 roots（bits 0, 8, 24, 66, 79）。並走レーンがraw batch 1–9・v16 determinism rerun・v15 crosscheck・sweep audit・証明書5件（各2 part）を公開済みで、証明書manifestとreceipt foldは未着地だった。

## 監査手法

`audit_cost70e_certificates_third_independent_20261115.py`（Python標準ライブラリ＋公開検証器のsubprocess実行）:

1. 公開2 partを行境界で連結し、CRLF→LFへ正規化（canonical git-blob content）。whole md5/sha256/git blob sha・part blob sha・行数を記録。
2. **BigInt 3x3余因子検証器**（`verify_win7_certificate_bigint_independent.mjs`・solver/verdict cache/repo engine/repo検証器importなし）を5件に再実行。
3. **Number Bareiss 4x4検証器**（`verify_bit7_win7_cert.ts --root-check --subroots <全合法手> --consumed-out`）を5件に再実行し、consumed winner-state unionが証明書行集合と完全一致（missing/extra 0/0）することをassert。
4. exact-integer D4正準化で各rootのcanonical hexと6個の一石削除親orbitを再導出し、cost-70e child orbitが全証明書に含まれることをassert。

## 結果（5/5 PASS）

| bit | root | mobility | rows | bytes | terminal |
|---|---|---:|---:|---:|---|
| 0 | `00000000000000801202000000200005` | 60 | 67,895 | 2,457,954 | [13,17] |
| 8 | `00000000000000801202000000200104` | 63 | 47,877 | 1,731,491 | [13,17] |
| 24 | `00000000000000801202000001200004` | 56 | 46,324 | 1,675,589 | [13,17] |
| 66 | `00000000000000841202000000200004` | 49 | 36,897 | 1,333,617 | [13,17] |
| 79 | `00000000000080801202000000200004` | 52 | 37,791 | 1,365,523 | [13,17] |

- 合計 **236,784行・8,564,174 bytes・280 sub-roots・31 distinct parent-lift orbits**。
- BigInt 5/5 PASS（union missing/extra 0/0・terminal [13,17]）、Number Bareiss 5/5 PASS（consumed union == 証明書行集合 0/0・root mobility == 全合法手数）。
- 5 rootのD4 canonical hexは互いにdistinct。child orbit `00000000000000801202000000200004` は5証明書すべての親orbitに含まれる。
- 監査JSON: `class2-lane-cost70e-certificates-third-independent-audit-20261115.json`。

## 実行環境上の注意

公開partはworking treeでCRLFのため、連結したwholeをLFへ正規化してからTS検証器に渡した（TS検証器は`\n`のみでsplitするため、CRLFのままではheader検査に落ちる）。BigInt検証器は`\r?\n`を許容するが、canonical hashはLF内容で記録した。

## 解釈上の注意

**fold未実施**: 5証明書はfold材料だが、receipt fold（child orbitの閉鎖・両開親の残行減）は別工程。監査時点でcanonical head 1227/6620/522561/4890/386284は不変で、childは両開親の未解決S6行のまま。cost-70eのfoldはfold時点のcanonical headへのrebaseが必須。REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l receipts foldがIN FLIGHT（head 1227基準・bits 21/48）。class-4 laneはcost-84 sterile・cost-86d sweep in flight。cost-70eの証明書manifest・foldは未claim。本監査はfoldの代わりではなく、fold実行者が利用できる独立証拠である。

## 成果物

- audit script: [audit_cost70e_certificates_third_independent_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70e_certificates_third_independent_20261115.py)
- audit JSON: [class2-lane-cost70e-certificates-third-independent-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-certificates-third-independent-audit-20261115.json)
- certificates: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-certificates/`（5件×2 part）
