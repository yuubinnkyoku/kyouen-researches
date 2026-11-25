# 2026-11-15：cost-77c sweep・WIN7証明書8件・receipt fold — 第二class-2 target S5が14→13行（head 1286→1290）

開始時main: `2dc9fc64d`（cost-77b fold後のhead 1286/6561/518211/4831/381934）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000040000801202000000200000`（stones [21,49,57,60,71,90]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000009000000`）をcost-77cとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**77/77候補・WIN7-D10 8件（bits 10,40,50,54,58,95,96,111）・69 REFUTED-D10・0 capped・総nodes 98,545,191**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで8 WIN loss=true（sum 38,837,101）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書8件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 10 | 64 | 70,081 | 19,127,774 | 2,525,643 |
| 40 | 54 | 34,269 | 6,865,661 | 1,233,904 |
| 50 | 50 | 32,703 | 4,842,395 | 1,178,602 |
| 54 | 58 | 44,441 | 6,985,479 | 1,603,365 |
| 58 | 54 | 40,450 | 5,679,053 | 1,457,491 |
| 95 | 55 | 40,339 | 9,969,506 | 1,453,158 |
| 96 | 61 | 50,927 | 8,672,633 | 1,834,104 |
| 111 | 61 | 49,152 | 6,431,349 | 1,769,123 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**362,362行・13,055,390 bytes・68,573,850 extraction nodes・457 sub-roots**。bit10のみ行境界2分割、他7件は単一ファイル。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**8/8 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1286 → 1290）

`recompute_frontier_cost77c_receipts_20261115.py` はcost-77b fold scriptをrunpyで再実行してhead 1286/6561/518211/4831/381934をbyte-identicalに再現し、公開順 [10,40,50,54,58,95,96,111] で8 receiptをfoldした。

- 新canonical head: **`1290/6557/517923/4827/381646`**（solved 1286→1290、in-manifest marginal 4、raw marginal 36、zero-mim bits 50/58/95/111）。
- child `00000000040000801202000000200000` は**bit10**で閉鎖。
- **第二target S5: 14行/1095 → 13行/1018**（childのみ喪失）。
- 第2開親 `00000000000000003800000009000000`: 57行/4337 → 53行/4049（child+3親orbit喪失）。
- set等式 `s_after == s_1286 ∪ covers(8 roots)`、557 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `7f2badce…`・10,558 B）、ranking CSV（`9ada5dfc…`・7,539 B）、top-candidates CSV（`8d5583e0…`・7,589 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り13行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- cost-75d（第二targetのcost-75行）は4証明書公開済みでfold待ち。
- 第二targetの次の未sweep行（cost-77 `00000000100000801202000000200000`・cost-79 `00000000000000801212000000200000` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1290へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77c_receipts_20261115.py
```

cost-77b baselineを再実行し、head 1286のbyte-identical再現から8 receiptsをfoldする。実行時間は約1〜2分。
