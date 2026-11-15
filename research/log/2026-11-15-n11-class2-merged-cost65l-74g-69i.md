# 2026-11-15：cost-65l + cost-74g + cost-69i のunified merge — canonical head 1277（第三target S5閉鎖を含む）

開始時main: `eddb4f667`（cost-69i fold後のhead 1273/6574/519179/4844/382902）。並走のcost-65l fold（head 1261）とcost-74g fold（head 1266）は1257から分岐しており、並走レーンが65l+74gのmerged head **1270/6577/519427/4847/383150** を公開していた。本作業はこのmerged 1270にcost-69iの4 receiptsを統合し、**65l + 74g + 69iの単一canonical chain**を確定した。

## 統合方法

`recompute_frontier_merged_cost65l_74g_69i_20261115.py` は公開merged script `recompute_frontier_merged_cost65l_74g_20261115.py` をrunpyで再実行し、head 1270/6577/519427/4847/383150をbyte-identicalに再現（head JSON blob `02109530…`・ranking `5d88b9c1…`・top-candidates `7de39cf8…`）。その上でcost-69iの4 receipts（bits 21,29,97,100）をfoldした。

- 69iの親S5はmerged 1270でも不変: 第三target `00000000000000809102000000000000`（1行/69）・第2開親 `00000000000000801202000000080000`（72行/5477）・class-4開親 `00000000000000003800000000810000`（84行/6815）。
- 65l/74gのreceiptsと69iの親orbitの交差は0で、69iのmarginalは19/7のまま。
- 542（69i fold時点のfolded roots）+ 12（65l+74g merged roots）= 544 rootsとのraw/D4 disjointnessをassert。

## 結果

- 新canonical head: **`1277/6570/518896/4840/382619`**（solved 1270→1277、in-manifest marginal 7、raw marginal 19）。
- **第三target S5 `00000000000000809102000000000000`: 1行/69 → 0行/0（閉鎖）**。class-2 blockerは条件付きで閉鎖。
- 第2開親 `00000000000000801202000000080000`: 72行/5477 → 69行/5265。
- class-4開親 `00000000000000003800000000810000`: 84行/6815 → 79行/6427。
- best class-2はaudit-blocked S5 `00000000000000809082000000000000`（10行/698）、best class-4 blocker S5は`00000000020000003800000080000000`（18行/1460）。
- 出力: head JSON（blob `0f16cdac56468811687525d7ebdfd1f85a2988d1`・9,127 B）、ranking CSV（`b149e71379e2e38f277e2ca59b4a27d41f35024e`・7,539 B）、top-candidates CSV（`8f72d7a8faf40d5437b2215cfb94eae719643c25`・7,933 B）。

## 信頼境界

- 統合は公開receiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- 第三target S5の閉鎖は「全6石子が先手WIN」というmanifest被覆に基づく条件付きclosureであり、blocker全体の独立証明ではない。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 次の一手

- 第二coverable class-2 target S5 `00000000000000801202000000200000` は17行/1325（merged head）。cost-74h（child `00000000000000889002000000000800`）が並走でsweep中。
- best class-4 blocker S5は18行/1460。class-4 laneの次候補（cost-86/87行）が残る。
- 以後のfoldは新head 1277へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost65l_74g_69i_20261115.py
```

merged 65l+74g baselineを再実行し、head 1270のbyte-identical再現から69i receiptsをfoldする。実行時間は約1〜2分。
