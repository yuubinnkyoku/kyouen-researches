# 2026-11-16：cost-70g sweep・WIN7証明書7件・receipt fold — 第二候補S5が8→7行（head 1398→1403）

開始時main: `b4dffee1b`（cost-67d fold後のhead 1398/6450/509974/4720/373697）。第二coverable class-2 candidate S5 `00000000000000801202000040000000` のcost-70 child `00000000000000801202000040000001`（stones [0,30,49,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二候補とclass-2 S5 `00000000000000003800000008000001`）をcost-70gとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・9バッチ・pilot 3402×9全PASS）

**70/70候補・WIN7-D10 7件（bits 18,24,28,59,89,112,120）・63 REFUTED-D10・0 capped・総nodes 124,066,734**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで7 WIN loss=true（sum 45,164,332）・合法REFUTEDアンカーbits 1/2 loss=false・pilot 5949。**注**: v15でbit0（非合法候補）を追加probeしたところnodes=1・terminal [7,7]のWINを返したが、bit0はlegal_candidatesに含まれないためfold対象外。

## 証明書7件（blind抽出・二重独立検証PASS）

合計**350,567行・12,679,157 bytes・395 sub-roots**。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**7/7 PASS**（union 0/0・terminal [13,17]）。

## receipt fold（head 1398 → 1403）

`recompute_frontier_cost70g_receipts_20261116.py` はcost-67d fold scriptをrunpyで再実行してhead 1398/6450/509974/4720/373697をbyte-identicalに再現し、公開順 [18,...,120] で7 receiptをfoldした。

- 新canonical head: **`1403/6445/509589/4715/373312`**（solved 1398→1403、in-manifest marginal 5、raw marginal 33、zero-mim bits 59/89/112）。
- child `00000000000000801202000040000001` は**bit18**で閉鎖。
- **第二候補S5: 8行/572 → 7行/502**（childのみ喪失）。
- 第2開親 `00000000000000003800000008000001`: 53行/4270 → 48行/3885（child+4親orbit喪失）。
- set等式 `s_after == s_1398 ∪ covers(7 roots)`、705 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `8eb71c91…`・9,896 B）、ranking CSV（`df92f3d0…`・7,535 B）、top-candidates CSV（`22607d3a…`・3,887 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5（3行/209）は全残行REFUTED-D10でdepth-10 receipt限界のまま。第二候補S5は残り7行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-71/75/76など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1403へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost70g_receipts_20261116.py
```

cost-67d baselineを再実行し、head 1398のbyte-identical再現から7 receiptsをfoldする。実行時間は約2〜3分。
