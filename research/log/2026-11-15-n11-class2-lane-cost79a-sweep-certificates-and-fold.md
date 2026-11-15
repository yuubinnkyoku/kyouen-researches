# 2026-11-15：cost-79a sweep・WIN7証明書3件・receipt fold — 第二class-2 target S5が11→10行（head 1302→1304）

開始時main: `a5dbca379`（warm-hygiene merge後のhead 1302/6545/517025/4815/380748）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-79 child `00000000000000801212000000200000`（stones [21,49,52,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000801212000000000000`）をcost-79aとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**79/79候補・WIN7-D10 3件（bits 9,50,64）・76 REFUTED-D10・0 capped・総nodes 131,934,659**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで3 WIN loss=true（sum 27,708,883）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書3件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 9 | 65 | 71,548 | 18,550,971 | 2,591,246 |
| 50 | 60 | 60,903 | 18,985,645 | 2,201,858 |
| 64 | 53 | 32,758 | 2,678,972 | 1,184,838 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**165,209行・5,977,942 bytes・40,215,588 extraction nodes・178 sub-roots**。bit64は単一ファイル、bit9/bit50は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**3/3 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1302 → 1304）

`recompute_frontier_cost79a_receipts_20261115.py` はmerged 75d+77d scriptをrunpyで再実行してhead 1302/6545/517025/4815/380748をbyte-identicalに再現し、公開順 [9,50,64] で3 receiptをfoldした。

- 新canonical head: **`1304/6543/516873/4813/380596`**（solved 1302→1304、in-manifest marginal 2、raw marginal 14、zero-mim bit64）。
- child `00000000000000801212000000200000` は**bit9**で閉鎖。
- **第二target S5: 11行/866 → 10行/787**（childのみ喪失）。
- 第2開親 `00000000000000801212000000000000`: 73行/5750 → 71行/5598（child+1親orbit喪失）。
- set等式 `s_after == s_1302 ∪ covers(3 roots)`、580 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `7dea99ff…`・7,452 B）、ranking CSV（`d31201b1…`・7,538 B）、top-candidates CSV（`34efacb3…`・7,330 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り10行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二targetの次の未sweep行（cost-80 `00000008000000809002000000000400`・cost-82 `00000000200040003800000000000200`・cost-83 3行など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1304へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost79a_receipts_20261115.py
```

merged 1302 baselineを再実行し、head 1302のbyte-identical再現から3 receiptsをfoldする。実行時間は約1〜2分。
