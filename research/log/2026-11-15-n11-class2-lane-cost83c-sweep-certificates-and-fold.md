# 2026-11-15：cost-83c sweep・WIN7証明書2件・receipt fold — 第二class-2 target S5が6→5行（head 1312→1313）

開始時main: `47e850e6e`（cost-83b fold後のhead 1312/6535/516227/4805/379950）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-83 child `00000000200000003800000000400200`（stones [9,22,59,60,61,93]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000801202000000000100`）をcost-83cとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**83/83候補・WIN7-D10 2件（bits 16,82）・81 REFUTED-D10・0 capped・総nodes 132,219,127**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで2 WIN loss=true（sum 6,145,186）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書2件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 16 | 61 | 47,205 | 6,473,198 | 1,708,430 |
| 82 | 60 | 42,939 | 3,517,936 | 1,549,434 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**90,144行・3,257,864 bytes・9,991,134 extraction nodes・121 sub-roots**。両方とも単一ファイル（1.75 MiB未満）。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**2/2 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1312 → 1313）

`recompute_frontier_cost83c_receipts_20261115.py` はcost-83b fold scriptをrunpyで再実行してhead 1312/6535/516227/4805/379950をbyte-identicalに再現し、公開順 [16,82] で2 receiptをfoldした。

- 新canonical head: **`1313/6534/516144/4804/379867`**（solved 1312→1313、in-manifest marginal 1、raw marginal 9、zero-mim bit82）。
- child `00000000200000003800000000400200` は**bit16**で閉鎖。
- **第二target S5: 6行/459 → 5行/376**（childのみ喪失）。
- 第2開親 `00000000000000801202000000000100`: 65行/5330 → 64行/5247（childのみ喪失）。
- set等式 `s_after == s_1312 ∪ covers(2 roots)`、601 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `fc7832ed…`・6,811 B）、ranking CSV（`08f0d715…`・7,537 B）、top-candidates CSV（`6a40509d…`・6,899 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り5行で未解決のまま（best coverable class-2）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-83の3行は全てfold済み、次はcost-85以降）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1313へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83c_receipts_20261115.py
```

cost-83b baselineを再実行し、head 1312のbyte-identical再現から2 receiptsをfoldする。実行時間は約1〜2分。
