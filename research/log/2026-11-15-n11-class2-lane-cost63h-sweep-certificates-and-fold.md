# 2026-11-15：cost-63h sweep・WIN7証明書1件・receipt fold — 三開親行の閉鎖（head 1360→1362）

開始時main: claim時はhead `1326/6522/515251/4792/378974`（cost-62a fold後）。第二coverable class-2候補S5 `00000000000000801202000040000000` のcost-63 child `00000000000000801202000040080000`（stones [19,30,49,57,60,71]・需要 c1=0,c2=2,c4=2・**三開親**: 当時34/2368・69/5265・77/5548）をcost-63hとしてsweepした。**sweep実行中に並走のcost-58c fold（`dcd2ead`）が着地しheadが1360へ移動**したため、receipt foldは58c chain head `1360/6488/512785/4758/376508` にre-baseして実施した（sweep verdictはbaseline非依存のper-position深さ10結果）。

## sweep（v16 d10・cap 1e9・andclose 1・4バッチ・pilot 3402×4全PASS）

**63/63候補・WIN7-D10 1件（bit 89）・62 REFUTED-D10・0 capped・総nodes 44,015,867**。全候補 terminal [13,17]。determinism rerun（全63候補・4バッチ再実行）**node-exact**、v15交差エンジンでbit89 loss=true（nodes 1,474,445）・REFUTEDアンカーbits 0/1/3 loss=false・pilot 5949。

## 証明書1件（二重独立検証PASS）

| bit | mobility | rows | bytes | md5 |
|---|---:|---:|---:|---|
| 89 | 47 | 26,070 | 941,299 | b721d428… |

root `00000000020000801202000040080000`（child｜1<<89・7石）。**BigInt 3x3 + Number Bareiss**の二独立検証器でPASS（union missing/extra 0/0・subroots 47/47・terminal [13,17]）・consumed 38,182行→distinct 26,070 == rows・rows sorted-unique。公開: `class2-lane-cost63h-certificates/bit89-root-00000000020000801202000040080000.cert`（単一ファイル）。

## receipt fold（head 1360 → 1362）

`recompute_frontier_cost63h_receipts_20261115.py` はcost-58c fold scriptをrunpyで再実行してhead `1360/6488/512785/4758/376508` をbyte-identicalに再現（runpy鎖は62a→84a→83d→…まで全CONTROL PASS）し、bit-89 receipt 1件をfoldした。

- 新canonical head: **`1362/6486/512653/4756/376376`**（solved 1360→1362、in-manifest marginal 2、raw marginal 5、zero-mimなし）。
- child `00000000000000801202000040080000` は**bit89**で閉鎖。
- **第二候補S5: 21行/1454 → 20行/1391**（childのみ喪失）。
- dual class-2+4 S5 `00000000000000801202000000080000`: 69行/5265 → 68行/5202（childのみ喪失）。
- class-4 S5 `00000000000000003800000001800000`: 77行/5548 → **75行/5416**（childに加え、bit-89 receiptのmarginalが第2manifest orbit `00000000020000801002000040080000` を追加閉鎖）。
- 1360 baselineでの三開親保持（21/1454・69/5265・77/5548）・需要 c1=0,c2=2,c4=2 再導出・lift stones {19, 30, 57}、set等式 `s_after == s_1360 ∪ covers(root)`、649 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `647498b9…`・6,852 B）、ranking CSV（`2a264dad…`・7,537 B）、top-candidates CSV（`bfb1538f…`・5,007 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンド・rebase noteを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 58c tmp再構成scriptの補完（gap-fill）

並走のcost-58c foldはtmp-cost58c中間体の再構成scriptを公開していなかった。`reconstruct_tmp_cost58c_20261116.py`（62a版の機械適応・bit76除外はfold入力でないため再構成対象外）を執筆・公開し、33証明書（1,156,691行・md5 33/33一致）のtsverify+BigIntを再実行して鎖のhead 1360再現を独立に確認した。63h自身のtmpは `reconstruct_tmp_cost63h_20261115.py` で再構成可能。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書はbit-89 rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二候補S5は残り20行で未解決のまま。best coverable class-2は `00000000000000801202000000200000` 3行/209（REFUTED-D10のみ）。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。

## 並走・次の一手

- 並走laneがcost-63i claim（`00000000000000c09002000001000000`・別child・2開親）を1360 baselineでin-flight公開済み。63i foldは**新head 1362へのre-baseが必須**（63h foldは63i childを閉じていないため63i側の数値は需要・開親とも影響なしのはずだが、baseline再取得は必須）。
- 第二候補S5の残り20行のうち次の安い行はcost-63が2行（`00000000000000c09002000001000000`=63i claimed・`00000000040000003800000048000000`）。
- 以後のfoldは新head 1362へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost58c_20261116.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost63h_20261115.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost63h_receipts_20261115.py
```

58c baseline（tmp-cost58c再構成後）を再実行し、head 1360のbyte-identical再現からbit-89 receiptをfoldする。実行時間は約2〜3分。
