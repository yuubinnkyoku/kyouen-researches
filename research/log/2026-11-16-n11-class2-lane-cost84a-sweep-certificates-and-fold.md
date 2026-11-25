# 2026-11-16：cost-84a sweep・WIN7証明書4件・receipt fold — 第二class-2 target S5が4→3行（head 1314→1318）

開始時main: `cec93b402`（cost-83d fold後のhead 1314/6533/516061/4803/379784）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-84 child `00000000000040809002000000000800`（stones [11,49,60,63,71,78]・需要 c1=0,c2=1,c4=0・開親は第二targetのみ）をcost-84aとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**84/84候補・WIN7-D10 4件（bits 1,62,70,90）・80 REFUTED-D10・0 capped・総nodes 138,214,313**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで4 WIN loss=true（sum 38,214,843）・REFUTEDアンカーbits 0/2/3 loss=false・pilot 5949。

## 証明書4件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 1 | 65 | 55,267 | 16,431,199 | 2,000,341 |
| 62 | 63 | 60,795 | 21,497,173 | 2,193,052 |
| 70 | 61 | 42,721 | 9,364,231 | 1,539,101 |
| 90 | 60 | 49,552 | 14,002,958 | 1,785,845 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**208,335行・7,518,339 bytes・61,295,561 extraction nodes・249 sub-roots**。bit70/bit90は単一ファイル、bit1/bit62は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**4/4 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1314 → 1318）

`recompute_frontier_cost84a_receipts_20261115.py` はcost-83d fold scriptをrunpyで再実行してhead 1314/6533/516061/4803/379784をbyte-identicalに再現し、公開順 [1,62,70,90] で4 receiptをfoldした。

- 新canonical head: **`1318/6530/515822/4800/379545`**（solved 1314→1318、in-manifest marginal 4、raw marginal 20、zero-mim bit70）。
- child `00000000000040809002000000000800` は**bit1**で閉鎖。
- **第二target S5: 4行/293 → 3行/209**（childのみ喪失）。
- set等式 `s_after == s_1314 ∪ covers(4 roots)`、606 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `f5624e99…`・7,935 B）、ranking CSV（`41fe1225…`・7,537 B）、top-candidates CSV（`c00f7306…`・6,641 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り3行で未解決のまま（best coverable class-2）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-85以降）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1318へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost84a_receipts_20261115.py
```

cost-83d baselineを再実行し、head 1314のbyte-identical再現から4 receiptsをfoldする。実行時間は約1〜2分。
