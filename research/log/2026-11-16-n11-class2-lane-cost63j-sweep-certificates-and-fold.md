# 2026-11-16：cost-63j sweep・WIN7証明書29件・receipt fold — 第二候補S5が17→10行（head 1367→1394）

開始時main: `356d5bc0a`（cost-63i fold後のhead 1367/6481/512295/4751/376018）。第二coverable class-2 candidate S5 `00000000000000801202000040000000` のcost-63 child `00000000040000003800000048000000`（stones [27,30,59,60,61,90]・需要 c1=0,c2=2,c4=0・開親は第二候補とclass-2 S5 `00000000000000003800000009000000`）をcost-63jとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）

**63/63候補・WIN7-D10 29件・34 REFUTED-D10・0 capped・総nodes 40,372,308**。terminal範囲に (13,15) を含む。batch-5 determinism rerun node-exact、v15交差エンジンで29 WIN loss=true（sum 70,752,352）・REFUTEDアンカーbits 0/2 loss=false・pilot 5949。**注**: v15でbit5（非合法候補）を追加probeしたところWINを返したが、bit5はlegal_candidatesに含まれないためfold対象外。

## 証明書29件（blind抽出・二重独立検証PASS）

合計**1,000,747行・36,115,333 bytes・1,489 sub-roots**。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**29/29 PASS**（union 0/0・terminal [13,17]）。

## receipt fold（head 1367 → 1394）

`recompute_frontier_cost63j_receipts_20261116.py` はcost-63i fold scriptをrunpyで再実行してhead 1367/6481/512295/4751/376018をbyte-identicalに再現し、公開順 [1,...,113] で29 receiptをfoldした。

- 新canonical head: **`1394/6454/510249/4724/373972`**（solved 1367→1394、in-manifest marginal 27、raw marginal 138、zero-mim 8件）。
- child `00000000040000003800000048000000` は**bit1**で閉鎖。
- **第二候補S5: 17行/1185 → 10行/704**（child+6親orbit喪失）。
- 第2開親 `00000000000000003800000009000000`: 52行/3979 → 31行/2351（child+20親orbit喪失）。
- set等式 `s_after == s_1367 ∪ covers(29 roots)`、667 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `35236daf…`・23,315 B）、ranking CSV（`2d41a386…`・7,536 B）、top-candidates CSV（`1b5d6773…`・4,146 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5（3行/209）は全残行REFUTED-D10でdepth-10 receipt限界のまま。第二候補S5は残り10行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-63残り1行・cost-64など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1394へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost63j_receipts_20261116.py
```

cost-63i baselineを再実行し、head 1367のbyte-identical再現から29 receiptsをfoldする。実行時間は約3〜4分。
