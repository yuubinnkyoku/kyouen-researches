# 2026-11-16：cost-62a sweep・WIN7証明書6件・receipt fold — 第二候補S5が39→34行（head 1318→1326）

開始時main: `5c9d1cb62`（cost-84a fold後のhead 1318/6530/515822/4800/379545）。**第二coverable class-2 target S5 `00000000000000801202000000200000` の残り3行（cost 65/70/74）はすべて既sweepのREFUTED-D10**で、depth-10 WIN7 receiptでは閉鎖できない（receipt-based closureの限界）。次frontierとして第二coverable class-2 candidate S5 `00000000000000801202000040000000`（39行/2708）のcost-62 child `00000000040000003800000008100000`（stones [20,27,59,60,61,90]・需要 c1=0,c2=2,c4=0・開親は第二候補とclass-2 S5 `00000000000000003800000008001000`）をcost-62aとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）

**62/62候補・WIN7-D10 6件（bits 7,15,35,76,81,98）・56 REFUTED-D10・0 capped・総nodes 46,968,169**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで6 WIN loss=true（sum 17,034,740）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書6件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 7 | 54 | 53,161 | 9,361,655 | 1,925,726 |
| 15 | 44 | 31,620 | 3,848,743 | 1,141,235 |
| 35 | 45 | 29,085 | 3,044,835 | 1,051,582 |
| 76 | 57 | 55,814 | 6,860,805 | 2,014,677 |
| 81 | 50 | 35,412 | 3,647,451 | 1,280,694 |
| 98 | 50 | 30,842 | 2,699,962 | 1,110,987 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**235,934行・8,524,901 bytes・29,463,451 extraction nodes・300 sub-roots**。bit7/bit76は行境界2分割、他4件は単一ファイル。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**6/6 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1318 → 1326）

`recompute_frontier_cost62a_receipts_20261116.py` はcost-84a fold scriptをrunpyで再実行してhead 1318/6530/515822/4800/379545をbyte-identicalに再現し、公開順 [7,15,35,76,81,98] で6 receiptをfoldした。

- 新canonical head: **`1326/6522/515251/4792/378974`**（solved 1318→1326、in-manifest marginal 8、raw marginal 32、zero-mim bit35）。
- child `00000000040000003800000008100000` は**bit7**で閉鎖。
- **第二候補S5: 39行/2708 → 34行/2368**（child+4親orbit喪失）。
- 第2開親 `00000000000000003800000008001000`: 52行/3875 → 48行/3582（child+3親orbit喪失）。
- set等式 `s_after == s_1318 ∪ covers(6 roots)`、610 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `3989e9dd…`・9,434 B）、ranking CSV（`f99c7561…`・7,537 B）、top-candidates CSV（`cec2b833…`・6,211 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **第二target S5（3行/209）は全残行がREFUTED-D10で、depth-10 receiptでは閉鎖不能**。より深い探索か別証明が必要。
- 第二候補S5は残り34行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-63 4行など）とclass-4 blocker S5の残行が候補。
- 第二target S5はdepth-10 receipt限界のため、深さ11+の探索または別アプローチが必要。
- 以後のfoldは新head 1326へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost62a_receipts_20261116.py
```

cost-84a baselineを再実行し、head 1318のbyte-identical再現から6 receiptsをfoldする。実行時間は約1〜2分。
