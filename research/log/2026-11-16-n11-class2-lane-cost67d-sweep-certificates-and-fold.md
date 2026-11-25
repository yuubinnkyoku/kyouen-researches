# 2026-11-16：cost-67d sweep・WIN7証明書1件・receipt fold — 第二候補S5が9→8行（head 1396→1398）

開始時main: `784f14994`（cost-65m fold後のhead 1396/6452/510115/4722/373838）。第二coverable class-2 candidate S5 `00000000000000801202000040000000` のcost-67 child `00000000000000801202000040002000`（stones [13,30,49,57,60,71]・需要 c1=0,c2=1,c4=1・開親は第二候補とclass-2 S5 `00000000000000801002000001080000`）をcost-67dとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・9バッチ・pilot 3402×9全PASS）

**67/67候補・WIN7-D10 1件（bit97）・66 REFUTED-D10・0 capped・総nodes 65,246,890**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンでbit97 WIN loss=true（9,849,920 nodes）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書1件（blind抽出・二重独立検証PASS）

bit97 root `00000002000000801202000040002000`（mobility 56）。**46,661行・1,685,346 bytes・16,992,795 extraction nodes・56 sub-roots**。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**1/1 PASS**（union 0/0・terminal [13,17]）。

## receipt fold（head 1396 → 1398）

`recompute_frontier_cost67d_receipts_20261116.py` はcost-65m fold scriptをrunpyで再実行してhead 1396/6452/510115/4722/373838をbyte-identicalに再現し、1 receiptをfoldした。

- 新canonical head: **`1398/6450/509974/4720/373697`**（solved 1396→1398、in-manifest marginal 2、raw marginal 5、zero-mimなし）。
- child `00000000000000801202000040002000` は**bit97**で閉鎖。
- **第二候補S5: 9行/639 → 8行/572**（childのみ喪失）。
- 第2開親 `00000000000000801002000001080000`: 84行/6410 → 82行/6269（child+1親orbit喪失）。
- set等式 `s_after == s_1396 ∪ covers(1 root)`、704 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `304c6afe…`・6,232 B）、ranking CSV（`876b4062…`・7,535 B）、top-candidates CSV（`3604fa01…`・3,973 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5（3行/209）は全残行REFUTED-D10でdepth-10 receipt限界のまま。第二候補S5は残り8行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-70/71/75/76など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1398へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost67d_receipts_20261116.py
```

cost-65m baselineを再実行し、head 1396のbyte-identical再現から1 receiptをfoldする。実行時間は約2分。
