# 2026-11-15：cost-76b sweep・WIN7証明書2件・receipt fold — 第二class-2 target S5が17→16行（head 1277→1280）

開始時main: `38f162a37`（3-way merged fold後のcanonical head 1277/6570/518896/4840/382619）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-76 child `00000000000000801302000000200000`（stones [21,49,56,57,60,71]・需要 c1=0,c2=1,c4=0・開親は第二targetのみ）をcost-76bとしてsweepした（cost-76aは別childでfold済みのため76b命名）。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**76/76候補・WIN7-D10 2件（bits 72,96）・74 REFUTED-D10・0 capped・総nodes 107,961,863**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで2 WIN loss=true（nodes 3,999,895/7,364,097・sum 11,363,992）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書2件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 72 | 60 | 50,796 | 7,012,779 | 1,832,366 |
| 96 | 61 | 67,641 | 12,020,661 | 2,440,105 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**118,437行・4,272,471 bytes・19,033,440 extraction nodes・121 sub-roots**。bit72は単一ファイル（1.75 MiB未満）、bit96は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**2/2 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1277 → 1280）

`recompute_frontier_cost76b_receipts_20261115.py` はcanonical merged scriptをrunpyで再実行してhead 1277/6570/518896/4840/382619をbyte-identicalに再現し、公開順 [72,96] で2 receiptをfoldした。

- 新canonical head: **`1280/6567/518678/4837/382401`**（solved 1277→1280、in-manifest marginal 3、raw marginal 11、zero-mimなし）。
- child `00000000000000801302000000200000` は**bit72**で閉鎖。
- **第二target S5: 17行/1325 → 16行/1249**（childのみ喪失）。
- set等式 `s_after == s_1277 ∪ covers(2 roots)`、548 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `0c357597…`・6,899 B）、ranking CSV（`25e4cd03…`・7,539 B）、top-candidates CSV（`5f16284c…`・7,847 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り16行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- cost-75d（第二targetのcost-75行）は並走sweep中。
- 第二targetの次の未sweep行（cost-77 `00000000000000801202000000204000` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1280へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost76b_receipts_20261115.py
```

merged 1277 baselineを再実行し、head 1277のbyte-identical再現から2 receiptsをfoldする。実行時間は約1〜2分。
