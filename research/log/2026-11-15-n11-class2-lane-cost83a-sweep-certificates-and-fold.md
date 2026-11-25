# 2026-11-15：cost-83a sweep・WIN7証明書4件・receipt fold — 第二class-2 target S5が8→7行（head 1306→1309）

開始時main: `7aaa8a4e0`（cost-82c fold後のhead 1306/6541/516711/4811/380434）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-83 child `00000000000000801202000000200008`（stones [3,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000208000000`）をcost-83aとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**83/83候補・WIN7-D10 4件（bits 12,58,72,95）・79 REFUTED-D10・0 capped・総nodes 152,978,839**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで4 WIN loss=true（sum 22,798,759）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書4件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 12 | 60 | 40,417 | 6,052,118 | 1,460,879 |
| 58 | 58 | 41,891 | 5,624,847 | 1,513,561 |
| 72 | 57 | 36,293 | 4,357,281 | 1,308,925 |
| 95 | 68 | 58,190 | 19,278,673 | 2,103,150 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**176,791行・6,386,515 bytes・35,312,919 extraction nodes・243 sub-roots**。bit95のみ行境界2分割、他3件は単一ファイル。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**4/4 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1306 → 1309）

`recompute_frontier_cost83a_receipts_20261115.py` はcost-82c fold scriptをrunpyで再実行してhead 1306/6541/516711/4811/380434をbyte-identicalに再現し、公開順 [12,58,72,95] で4 receiptをfoldした。

- 新canonical head: **`1309/6538/516477/4808/380200`**（solved 1306→1309、in-manifest marginal 3、raw marginal 19、zero-mim bits 58/95）。
- child `00000000000000801202000000200008` は**bit12**で閉鎖。
- **第二target S5: 8行/625 → 7行/542**（childのみ喪失）。
- 第2開親 `00000000000000003800000208000000`: 70行/5743 → 67行/5509（child+2親orbit喪失）。
- set等式 `s_after == s_1306 ∪ covers(4 roots)`、592 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `74e35f22…`・8,068 B）、ranking CSV（`70eab6c4…`・7,537 B）、top-candidates CSV（`fad56f79…`・7,071 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り7行で未解決のまま（best coverable class-2）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-83 `00000000000000801202000000200010`・`00000000200000003800000000400200` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1309へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83a_receipts_20261115.py
```

cost-82c baselineを再実行し、head 1306のbyte-identical再現から4 receiptsをfoldする。実行時間は約1〜2分。
