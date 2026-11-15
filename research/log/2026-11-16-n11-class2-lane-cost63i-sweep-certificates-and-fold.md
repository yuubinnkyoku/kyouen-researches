# 2026-11-16：cost-63i sweep・WIN7証明書18件・receipt fold — 第二候補S5が21→17行（head 1360→1367）

開始時main: `632189836`（cost-58c fold後のhead 1360/6488/512785/4758/376508）。第二coverable class-2 candidate S5 `00000000000000801202000040000000` のcost-63 child `00000000000000c09002000001000000`（stones [24,49,60,63,70,71]・需要 c1=0,c2=2,c4=0・開親は第二候補とclass-2 S5 `00000000000000403800000008000000`）をcost-63iとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）

**63/63候補・WIN7-D10 18件（bits 30,32,41,45,54,61,62,66,77,81,99,105,107,112,114,116,119,120）・45 REFUTED-D10・0 capped・総nodes 67,040,399**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで18 WIN loss=true（sum 131,760,101）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書18件（blind抽出・二重独立検証PASS）

合計**648,506行・23,385,620 bytes・915 sub-roots**。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**18/18 PASS**（union 0/0・terminal [13,17]）。

## receipt fold（head 1360 → 1367）

`recompute_frontier_cost63i_receipts_20261116.py` はcost-58c fold scriptをrunpyで再実行してhead 1360/6488/512785/4758/376508をbyte-identicalに再現し、公開順 [30,...,120] で18 receiptをfoldした。

- 新canonical head: **`1367/6481/512295/4751/376018`**（solved 1360→1367、in-manifest marginal 7、raw marginal 80、zero-mim 11件）。
- child `00000000000000c09002000001000000` は**bit30**で閉鎖。
- **第二候補S5: 21行/1454 → 17行/1185**（child+3親orbit喪失）。
- 第2開親 `00000000000000403800000008000000`: 27行/1915 → 24行/1704（child+2親orbit喪失）。
- set等式 `s_after == s_1360 ∪ covers(18 roots)`、649 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `db0288f1…`・16,455 B）、ranking CSV（`3251313b…`・7,537 B）、top-candidates CSV（`77836374…`・4,749 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5（3行/209）は全残行REFUTED-D10でdepth-10 receipt限界のまま。第二候補S5は残り17行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-63残り2行・cost-64など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1367へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost63i_receipts_20261116.py
```

cost-58c baselineを再実行し、head 1360のbyte-identical再現から18 receiptsをfoldする。実行時間は約2〜3分。
