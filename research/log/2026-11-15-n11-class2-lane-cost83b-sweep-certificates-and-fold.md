# 2026-11-15：cost-83b sweep・WIN7証明書5件・receipt fold — 第二class-2 target S5が7→6行（head 1309→1312）

開始時main: `fe7c785c8`（cost-83a fold後のhead 1309/6538/516477/4808/380200）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-83 child `00000000000000801202000000200010`（stones [4,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800100008000000`）をcost-83bとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**83/83候補・WIN7-D10 5件（bits 9,12,58,64,96）・78 REFUTED-D10・0 capped・総nodes 147,896,427**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで5 WIN loss=true（sum 29,471,397）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書5件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 9 | 66 | 55,508 | 11,131,161 | 2,011,820 |
| 12 | 61 | 48,038 | 6,409,037 | 1,736,247 |
| 58 | 67 | 80,596 | 15,647,490 | 2,912,776 |
| 64 | 58 | 37,677 | 4,852,027 | 1,363,767 |
| 96 | 65 | 53,829 | 8,102,358 | 1,943,612 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**275,648行・9,968,222 bytes・46,142,073 extraction nodes・317 sub-roots**。bit12/bit64は単一ファイル、bit9/bit58/bit96は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**5/5 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1309 → 1312）

`recompute_frontier_cost83b_receipts_20261115.py` はcost-83a fold scriptをrunpyで再実行してhead 1309/6538/516477/4808/380200をbyte-identicalに再現し、公開順 [9,12,58,64,96] で5 receiptをfoldした。

- 新canonical head: **`1312/6535/516227/4805/379950`**（solved 1309→1312、in-manifest marginal 3、raw marginal 23、zero-mim bits 58/64/96）。
- child `00000000000000801202000000200010` は**bit9**で閉鎖。
- **第二target S5: 7行/542 → 6行/459**（childのみ喪失）。
- 第2開親 `00000000000000003800100008000000`: 70行/5822 → 67行/5572（child+2親orbit喪失）。
- set等式 `s_after == s_1309 ∪ covers(5 roots)`、596 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `b089bd95…`・8,651 B）、ranking CSV（`c06ab3bb…`・7,537 B）、top-candidates CSV（`13670c6a…`・6,985 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り6行で未解決のまま（best coverable class-2）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-83 `00000000200000003800000000400200` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1312へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83b_receipts_20261115.py
```

cost-83a baselineを再実行し、head 1309のbyte-identical再現から5 receiptsをfoldする。実行時間は約1〜2分。
