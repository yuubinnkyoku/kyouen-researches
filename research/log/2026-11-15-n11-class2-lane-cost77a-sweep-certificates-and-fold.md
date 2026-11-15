# 2026-11-15：cost-77a sweep・WIN7証明書3件・receipt fold — 第二class-2 target S5が16→15行（head 1280→1282）

開始時main: `1aaf346ca`（cost-76b fold後のhead 1280/6567/518678/4837/382401）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000000000801202000000204000`（stones [14,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000408000000`）をcost-77aとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**77/77候補・WIN7-D10 3件（bits 40,64,111）・74 REFUTED-D10・0 capped・総nodes 103,356,793**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで3 WIN loss=true（nodes 8,989,854/2,953,791/4,578,937・sum 16,522,582）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書3件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 40 | 64 | 59,980 | 14,933,960 | 2,161,292 |
| 64 | 58 | 40,614 | 5,049,082 | 1,463,572 |
| 111 | 60 | 56,881 | 8,580,399 | 2,047,120 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**157,475行・5,671,984 bytes・28,563,441 extraction nodes・182 sub-roots**。bit64は単一ファイル、bit40/bit111は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**3/3 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1280 → 1282）

`recompute_frontier_cost77a_receipts_20261115.py` はcost-76b fold scriptをrunpyで再実行してhead 1280/6567/518678/4837/382401をbyte-identicalに再現し、公開順 [40,64,111] で3 receiptをfoldした。

- 新canonical head: **`1282/6565/518522/4835/382245`**（solved 1280→1282、in-manifest marginal 2、raw marginal 14、zero-mim bits 64/111）。
- child `00000000000000801202000000204000` は**bit40**で閉鎖。
- **第二target S5: 16行/1249 → 15行/1172**（childのみ喪失）。
- 第2開親 `00000000000000003800000408000000`: 62行/5092 → 60行/4936（child+1親orbit喪失）。
- set等式 `s_after == s_1280 ∪ covers(3 roots)`、550 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `a2ba7235…`・7,554 B）、ranking CSV（`502eadcc…`・7,539 B）、top-candidates CSV（`4365f8ea…`・7,761 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り15行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- cost-75d（第二targetのcost-75行）は4証明書公開済みでfold待ち。
- 第二targetの次の未sweep行（cost-77 `00000000000000801202000200200000` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1282へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77a_receipts_20261115.py
```

cost-76b baselineを再実行し、head 1280のbyte-identical再現から3 receiptsをfoldする。実行時間は約1〜2分。
