# 2026-11-16：cost-64a sterile + cost-65m sweep・WIN7証明書8件・receipt fold — 第二候補S5が10→9行（head 1394→1396）

開始時main: `6fd42c8de`（cost-63j fold後のhead 1394/6454/510249/4724/373972）。第二coverable class-2 candidate S5 `00000000000000801202000040000000` の残行を順に処理した。

## cost-64a: sterile（WIN7-D10 0件）

child `00000000000000801282000040000000`（stones [30,49,55,57,60,71]・需要 c1=1,c2=1,c4=0）をsweep。**64/64候補すべてREFUTED-D10・0 WIN・38,157,151 nodes**。WIN7 receiptが存在しないため証明書もfoldもなし。REFUTED-D10はLOSS証明ではない。

## cost-65m sweep（第二候補S5のcost-65 child）

child `00000000000000801202000040001000`（stones [12,30,49,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二候補とclass-2 S5 `00000000000000003800000008001000`）。**65/65候補・WIN7-D10 8件（bits 21,22,28,35,44,67,76,83）・57 REFUTED-D10・0 capped・74,130,403 nodes**、pilot 3402×9・determinism rerun node-exact・v15 8 WIN+3 refuted anchors一致。

## 証明書8件（blind抽出・二重独立検証PASS）

合計**329,770行・11,907,545 bytes・411 sub-roots**。**BigInt 3x3 + Number Bareiss 4x4**で**8/8 PASS**（union 0/0・terminal [13,17]）。

## receipt fold（head 1394 → 1396）

`recompute_frontier_cost65m_receipts_20261116.py` はcost-63j fold scriptをrunpyで再実行してhead 1394/6454/510249/4724/373972をbyte-identicalに再現し、公開順 [21,...,83] で8 receiptをfoldした。

- 新canonical head: **`1396/6452/510115/4722/373838`**（solved 1394→1396、in-manifest marginal 2、raw marginal 35、zero-mim 6件）。
- child `00000000000000801202000040001000` は**bit21**で閉鎖。
- **第二候補S5: 10行/704 → 9行/639**（childのみ喪失）。
- 第2開親 `00000000000000003800000008001000`: 48行/3582 → 46行/3448（child+1親orbit喪失）。
- set等式 `s_after == s_1394 ∪ covers(8 roots)`、696 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `9798a9fc…`・10,414 B）、ranking CSV（`ad9a62f6…`・7,535 B）、top-candidates CSV（`6df96d8f…`・4,059 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **cost-64a childはsterile（64/64 REFUTED-D10）でdepth-10 receiptでは閉鎖不能**。
- 第二target S5（3行/209）は全残行REFUTED-D10でdepth-10 receipt限界のまま。第二候補S5は残り9行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-67/70/71/75など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1396へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost65m_receipts_20261116.py
```

cost-63j baselineを再実行し、head 1394のbyte-identical再現から8 receiptsをfoldする。実行時間は約2〜3分。
