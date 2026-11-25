# 2026-11-15：cost-82c sweep・WIN7証明書5件・receipt fold — 第二class-2 target S5が9→8行（head 1305→1306）

開始時main: `039e2a400`（cost-80d fold後のhead 1305/6542/516793/4812/380516）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-82 child `00000000200040003800000000000200`（stones [9,59,60,61,78,93]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000408000000`）をcost-82cとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**82/82候補・WIN7-D10 5件（bits 16,37,47,71,82）・77 REFUTED-D10・0 capped・総nodes 151,736,232**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで5 WIN loss=true（sum 23,632,583）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書5件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 16 | 61 | 49,980 | 5,680,783 | 1,809,994 |
| 37 | 65 | 72,376 | 12,379,080 | 2,620,829 |
| 47 | 60 | 52,053 | 7,206,555 | 1,884,269 |
| 71 | 61 | 49,019 | 10,438,190 | 1,772,277 |
| 82 | 64 | 66,483 | 11,499,042 | 2,400,803 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**289,911行・10,488,172 bytes・47,203,650 extraction nodes・311 sub-roots**。bit16/bit71は単一ファイル、bit37/bit47/bit82は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**5/5 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1305 → 1306）

`recompute_frontier_cost82c_receipts_20261115.py` はcost-80d fold scriptをrunpyで再実行してhead 1305/6542/516793/4812/380516をbyte-identicalに再現し、公開順 [16,37,47,71,82] で5 receiptをfoldした。

- 新canonical head: **`1306/6541/516711/4811/380434`**（solved 1305→1306、in-manifest marginal 1、raw marginal 21、zero-mim bits 37/47/71/82）。
- child `00000000200040003800000000000200` は**bit16**で閉鎖。
- **第二target S5: 9行/707 → 8行/625**（childのみ喪失）。
- 第2開親 `00000000000000003800000408000000`: 60行/4936 → 59行/4854（childのみ喪失）。
- set等式 `s_after == s_1305 ∪ covers(5 roots)`、587 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `4ee6aaab…`・8,587 B）、ranking CSV（`cc89c52b…`・7,537 B）、top-candidates CSV（`6a1a2185…`・7,157 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り8行で未解決のまま（best coverable class-2）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-83 3行 `00000000000000801202000000200008`・`...200010`・`00000000200000003800000000400200` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1306へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost82c_receipts_20261115.py
```

cost-80d baselineを再実行し、head 1305のbyte-identical再現から5 receiptsをfoldする。実行時間は約1〜2分。
