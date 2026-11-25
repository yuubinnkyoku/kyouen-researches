# 2026-11-15：cost-80d sweep・WIN7証明書4件・receipt fold — 第二class-2 target S5が10→9行（head 1304→1305）

開始時main: `b39276c3e`（cost-79a fold後のhead 1304/6543/516873/4813/380596）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-80 child `00000008000000809002000000000400`（stones [10,49,60,63,71,99]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000008000001`）をcost-80dとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**80/80候補・WIN7-D10 4件（bits 48,61,81,96）・76 REFUTED-D10・0 capped・総nodes 131,430,976**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで4 WIN loss=true（sum 26,180,333）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書4件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 48 | 62 | 48,901 | 11,626,262 | 1,769,430 |
| 61 | 58 | 39,548 | 8,507,557 | 1,429,017 |
| 81 | 57 | 61,133 | 16,486,963 | 2,209,403 |
| 96 | 66 | 52,690 | 12,079,986 | 1,902,117 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**202,272行・7,309,967 bytes・48,700,768 extraction nodes・243 sub-roots**。bit48/bit61は単一ファイル、bit81/bit96は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**4/4 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1304 → 1305）

`recompute_frontier_cost80d_receipts_20261115.py` はcost-79a fold scriptをrunpyで再実行してhead 1304/6543/516873/4813/380596をbyte-identicalに再現し、公開順 [48,61,81,96] で4 receiptをfoldした。

- 新canonical head: **`1305/6542/516793/4812/380516`**（solved 1304→1305、in-manifest marginal 1、raw marginal 18、zero-mim bits 61/81/96）。
- child `00000008000000809002000000000400` は**bit48**で閉鎖。
- **第二target S5: 10行/787 → 9行/707**（childのみ喪失）。これで第二targetが**best coverable class-2**（9行）に。
- 第2開親 `00000000000000003800000008000001`: 55行/4417 → 54行/4337（childのみ喪失）。
- set等式 `s_after == s_1304 ∪ covers(4 roots)`、583 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `289c9337…`・8,033 B）、ranking CSV（`723e1e1e…`・7,537 B）、top-candidates CSV（`a38f1563…`・7,243 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り9行で未解決のまま。best class-2は第二target（9行/707）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-82 `00000000200040003800000000000200`・cost-83 3行など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1305へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost80d_receipts_20261115.py
```

cost-79a baselineを再実行し、head 1304のbyte-identical再現から4 receiptsをfoldする。実行時間は約1〜2分。
