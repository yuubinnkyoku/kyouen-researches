# 2026-11-16：cost-70g fork解消 — 7 receiptをcanonical head 1400へre-base（head 1400/1403 → 1405）

開始時main: `977cae45`（cost-76c IN FLIGHT claimまでmerge済み）。この時点でmainには**non-nested fork**が残っていた。cost-70g landing `dee808f0` は7件のWIN7-D10 receipt（bits 18/24/28/59/89/112/120・child `00000000000000801202000040000001`）を**superseded branch D head 1398/6450/509974/4720/373697**（cost-67d foldのみ）にfoldしてhead **1403/6445/509589/4715/373312**を宣言した一方、merged fold `2fbb5aa2` は63h+67d両receiptを1396共通baselineにfoldしたcanonical head **1400/6448/509842/4718/373565**を確定していた。cost-75e claim（`bc893758`追記）はこのreconciliation foldを必須と記録していたが未実施だった。本作業でそれを実施した。

## reconciliationの構成（`recompute_frontier_reconcile_canonical1400_cost70g_20261116.py`）

- cost-70g fold script `recompute_frontier_cost70g_receipts_20261116.py` をrunpyで再実行（内部でcost-67d chain全体をbyte-identical再現・sweepを9 raw batchから再導出・証明書7件を結合LF bytes対照で再assert・completed claim fold記録と出力3 blobのbyte-identityを再assert）。fork head 1403とbranch D head 1398'の数値を再確認。
- canonical 1400を **`s_1400 == s_base | cov(63h bit-89 root)`** としてbranch D head上に再構成。63h receiptのin-manifest marginals 2 orbit（`00000000000000801202000040080000`・`00000000020000801002000040080000`）がpublished branch C foldと一致、summary 5数値・histogram・published 5親（第二候補7/509、dual 68/5202、class4 75/5416、cost67d_parent2 82/6269、cost63i_second 24/1704）・best/next ranking全一致、さらに**再生成ranking CSVがpublished merged foldのCSVとbyte-identical**。
- 7 rootと**706 folded roots**（branch D 705 + 63h root）のraw-hex・D4 disjointness。
- childは1400でgenuinely remaining（第二候補S5 7行/509がedge cost 70のchild行を保持・parent2 53行/4270も保持・需要 c1=0,c2=2,c4=0）。published 70g in-manifest marginals 5 orbitと63h coverの重複は**0**（hex集合の直接照合）。
- 公開順 [18,24,28,59,89,112,120] で7 receiptを**canonical 1400にfold**。per-bit in-manifest marginalsはbranch D baselineと同一（overlap 0の帰結）。child orbitはbit18でちょうど1回閉鎖。
- **fork可換性**: `s_reconciled == s_1400 ∪ cov(7 roots) == s_1403 ∪ cov(63h root)`（reverse-order replay: 1403へ63h coverをfoldしても同一集合・同一summary）。
- **事前予測の照合**: 70gの閉鎖5 orbitは両baselineで同一・開親multiplicityも不変（63h coverとmarginalsが素）なのでΔ=-385/-385、head は **`1405/6443/509457/4713/373180`** と厳密に予測でき、実測が一致。

## 結果

- **新canonical head: `1405/6443/509457/4713/373180`**（solved 1400→1405、in-manifest marginal 5、raw marginal 33、zero-mim bits 59/89/112）。fork head 1403・merged head 1400はともにsuperseded。
- **第二候補S5 `00000000000000801202000040000000`: 7行/509 → 6行/439**（child行のみ喪失）。
- cost70g parent2 `00000000000000003800000008000001`: 53行/4270 → 48行/3885（child+4 orbit喪失、失った行はすべてcov(7 roots)内）。他のpublished親（dual/class4/cost67d/cost63i）は不変。
- best class-2 target S5 `00000000000000801202000000200000`（3行/209）・audit-blocked `00000000000000809082000000000000`（10行/698）・best class-4 blocker（18行/1460）不変。
- 証明書7件の再assert: 350,567行 / 12,679,157 bytes / 395 sub-roots（BigInt + tsverify union 0/0、terminal [13,17]）。
- 出力: head JSON（blob `b3ad19d7…`・11,352 B）、ranking CSV（`26fa720b…`・7,535 B）、top-candidates CSV（`c3433eee…`・3,801 B）。

## coordination（以後のfold・claimへの必須事項）

- **cost-75e IN FLIGHT claim**（child `00000000040000809002000000000002`・baseline 1400）と**cost-76c IN FLIGHT claim**（child `00000000010000809002000001000000`・baseline 1403）は**ともにsuperseded baselineを参照**しており、着地時はこのreconciled head **1405**へのre-baseが必須。
- bits 59/89/112はcanonical 1400でもzero-mim（branch D baselineと同じ）。
- cost-70g childのcost-70行は閉鎖済み。cost-71d row `00000000000000801202000040000400` はSTERILE（depth-10 receiptでは閉鎖不能）。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1 / class 2 / class 4 は引き続き UNKNOWN。**

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_reconcile_canonical1400_cost70g_20261116.py
```

前提: `reconstruct_tmp_cost{84a,83d,83c,83a,69i,62a,58c,63i,63j,65m,63h,67d,70g}_*.py` を依存順に実行してtmp-cost各種を再構成済みであること（fold script自体は全入力をmain上のartifactから再導出する）。
