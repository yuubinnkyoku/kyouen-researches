# 2026-11-15：cost-83d sweep・WIN7証明書3件・receipt fold — 第二class-2 target S5が5→4行（head 1313→1314）

開始時main: `3ba611fcf`（cost-83c fold後のhead 1313/6534/516144/4804/379867）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-83 child `00000000200000003800100000000200`（stones [9,44,59,60,61,93]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000043800000008000000`）をcost-83dとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**83/83候補・WIN7-D10 3件（bits 16,51,82）・80 REFUTED-D10・0 capped・総nodes 153,125,301**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで3 WIN loss=true（sum 29,933,192）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書3件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 16 | 62 | 67,775 | 15,371,324 | 2,452,971 |
| 51 | 58 | 58,094 | 12,272,343 | 2,099,877 |
| 82 | 68 | 90,769 | 23,807,535 | 3,277,412 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**216,638行・7,830,260 bytes・51,451,202 extraction nodes・188 sub-roots**。3件とも行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**3/3 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1313 → 1314）

`recompute_frontier_cost83d_receipts_20261115.py` はcost-83c fold scriptをrunpyで再実行してhead 1313/6534/516144/4804/379867をbyte-identicalに再現し、公開順 [16,51,82] で3 receiptをfoldした。

- 新canonical head: **`1314/6533/516061/4803/379784`**（solved 1313→1314、in-manifest marginal 1、raw marginal 13、zero-mim bits 51/82）。
- child `00000000200000003800100000000200` は**bit16**で閉鎖。
- **第二target S5: 5行/376 → 4行/293**（childのみ喪失）。
- 第2開親 `00000000000000043800000008000000`: 72行/6019 → 71行/5936（childのみ喪失）。
- set等式 `s_after == s_1313 ∪ covers(3 roots)`、603 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `49cb8022…`・7,407 B）、ranking CSV（`d8adfb7e…`・7,537 B）、top-candidates CSV（`454568f2…`・6,813 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り4行で未解決のまま（best coverable class-2）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-84 `00000000000040809002000000000800` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1314へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83d_receipts_20261115.py
```

cost-83c baselineを再実行し、head 1313のbyte-identical再現から3 receiptsをfoldする。実行時間は約1〜2分。
