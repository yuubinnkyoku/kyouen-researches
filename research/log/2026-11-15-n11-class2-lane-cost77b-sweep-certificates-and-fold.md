# 2026-11-15：cost-77b sweep・WIN7証明書4件・receipt fold — 第二class-2 target S5が15→14行（head 1282→1286）

開始時main: `d4ccb698a`（cost-77a fold後のhead 1282/6565/518522/4835/382245）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000000000801202000200200000`（stones [21,33,49,57,60,71]・需要 c1=0,c2=1,c4=0・開親は第二targetのみ）をcost-77bとしてsweepした（77aは別childでfold済み）。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**77/77候補・WIN7-D10 4件（bits 9,12,59,105）・73 REFUTED-D10・0 capped・総nodes 153,463,195**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで4 WIN loss=true（nodes 10,783,807/3,915,437/8,075,736/5,782,418・sum 28,557,398）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書4件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 9 | 60 | 61,131 | 14,137,439 | 2,214,402 |
| 12 | 55 | 34,176 | 6,080,106 | 1,235,435 |
| 59 | 54 | 46,606 | 14,725,087 | 1,683,871 |
| 105 | 62 | 49,024 | 11,533,110 | 1,770,759 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**190,937行・6,904,467 bytes・46,475,742 extraction nodes・231 sub-roots**。bit9のみ行境界2分割、他3件は単一ファイル。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**4/4 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1282 → 1286）

`recompute_frontier_cost77b_receipts_20261115.py` はcost-77a fold scriptをrunpyで再実行してhead 1282/6565/518522/4835/382245をbyte-identicalに再現し、公開順 [9,12,59,105] で4 receiptをfoldした。

- 新canonical head: **`1286/6561/518211/4831/381934`**（solved 1282→1286、in-manifest marginal 4、raw marginal 20、zero-mim bit59）。
- child `00000000000000801202000200200000` は**bit9**で閉鎖。
- **第二target S5: 15行/1172 → 14行/1095**（childのみ喪失）。
- set等式 `s_after == s_1282 ∪ covers(4 roots)`、553 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `b648ed06…`・8,073 B）、ranking CSV（`aca61cbd…`・7,539 B）、top-candidates CSV（`9c59ceb9…`・7,675 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り14行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- cost-75d（第二targetのcost-75行）は4証明書公開済みでfold待ち。
- 第二targetの次の未sweep行（cost-77 `00000000040000801202000000200000`・`00000000100000801202000000200000` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1286へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77b_receipts_20261115.py
```

cost-77a baselineを再実行し、head 1282のbyte-identical再現から4 receiptsをfoldする。実行時間は約1〜2分。
