# 2026-11-15：cost-69i sweep・WIN7証明書4件・receipt fold — 第三class-2 target S5が閉鎖（head 1266→1273）

開始時main: `e94f6b56b`（cost-74g fold後のhead 1266/6581/519710/4851/383433）。第三coverable class-2 target S5 `00000000000000809102000000000000` の**最後の残行** cost-69 child `00000000000000809102000000002000`（stones [13,49,56,60,63,71]・需要 c1=0,c2=2,c4=2）をcost-69iとしてsweepした。既存のcost-69g claim（head 1163・planのみ・artifactsなし）と、別childを扱う既存cost-69h lane（bits 58/96・fold済み）との名前衝突を避けて69iとした（69hのclaim/certsは復元・不可侵）。

## sweep（v16 d10・cap 1e9・andclose 1・9バッチ・pilot 3402×9全PASS）

**69/69候補・WIN7-D10 4件（bits 21,29,97,100）・65 REFUTED-D10・0 capped・総nodes 62,994,015**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで4 WIN loss=true（nodes 9,738,823/20,539,472/4,349,523/16,766,956・sum 51,394,774）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書4件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes |
|---|---:|---:|---:|
| 21 | 56 | 49,504 | 16,283,133 |
| 29 | 56 | 70,471 | 31,108,234 |
| 97 | 46 | 27,080 | 6,392,588 |
| 100 | 58 | 57,284 | 22,963,530 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**204,339行・7,379,919 bytes・76,747,485 extraction nodes・216 sub-roots**。bit21/bit97は単一ファイル、bit29/bit100は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**4/4 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1266 → 1273）— 第三target S5の閉鎖

`recompute_frontier_cost69i_receipts_20261115.py` はcost-74g fold scriptをrunpyで再実行してhead 1266をbyte-identicalに再現し、公開順 [21,29,97,100] で4 receiptをfoldした。

- 新canonical head: **`1273/6574/519179/4844/382902`**（solved 1266→1273、in-manifest marginal 7、raw marginal 19、zero-mimなし）。
- child `00000000000000809102000000002000` は**bit21**で閉鎖。
- **第三target S5 `00000000000000809102000000000000`: 1行/69 → 0行/0（閉鎖）**。このS5の6石の子はすべて先手WINとなったため、S5自体が先手WINとなり、**class-2 blockerが条件付きで閉鎖**される。
- 第2開親 `00000000000000801202000000080000`: **72行/5477 → 69行/5265**（child+2親orbit喪失）。
- 第3開親（class-4）`00000000000000003800000000810000`: **84行/6815 → 79行/6427**（child+4親orbit喪失）。
- set等式 `s_after == s_1266 ∪ covers(4 roots)`、542 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証、**第三targetの残行0制御**をassert。
- 出力: head JSON（blob `8692a7a67fc9e51c440a91cb2e95809b7d1825e8`・9,103 B）、ranking CSV（`7ce2e616dedb3a2c496fe4ef7779e05af943f5b9`・7,539 B）、top-candidates CSV（`945f65568f9edd4f33177920a93b3aa09e0a12d6`・8,019 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第三target S5の閉鎖は「このS5の全6石の子が先手WIN」というmanifest被覆の事実に基づく。S5は5石で先手番（偶数OR/奇数ANDの規約では5石は先手番）なので、全子WINはS5の先手WINを意味する。class-2 blockerの閉鎖はこのS5の役割に条件付きであり、blocker全体の独立証明ではない。
- 証明書木そのものの再走査は本foldの範囲外。公開receiptの二重独立検証に依拠し、foldはjoined LF bytes・root同定・sub-roots・終端範囲・親orbit・D4正準性を再検証した。

## 並走・次の一手

- cost-65l fold（head 1261）は本head 1273へのrebase・mergeが必須（1257からのfork）。
- 第二coverable class-2 target S5 `00000000000000801202000000200000` は本chainで18行/1390（65l fork側では17行/1325）で、次の主要frontier。
- best class-4 blocker S5 `00000000020000003800000080000000` は18行/1460。
- 第三target S5の閉鎖により、class-2 blockerの残作業は第二targetとaudit-blocked S5（10行/698）に集約された。

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は **UNKNOWN**。class-2 blockerは条件付きで閉鎖。今回のfoldは盤全体の勝敗判定を変更しない。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69i_receipts_20261115.py
```

cost-74g baselineを再実行し、head 1266のbyte-identical再現から全制約を再検証した上でfoldする。実行時間は約1〜2分。
