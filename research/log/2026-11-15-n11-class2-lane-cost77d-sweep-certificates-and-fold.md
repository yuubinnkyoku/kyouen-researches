# 2026-11-15：cost-77d sweep・WIN7証明書12件・receipt fold — 第二class-2 target S5が13→11行（head 1290→1299）

開始時main: `5a08dbb44`（cost-77c fold後のhead 1290/6557/517923/4827/381646）。第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000100000801202000000200000`（stones [21,49,57,60,71,92]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800400008000000`）をcost-77dとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**77/77候補・WIN7-D10 12件（bits 7,12,39,58,62,64,66,78,94,96,108,111）・65 REFUTED-D10・0 capped・総nodes 152,577,045**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで12 WIN loss=true（sum 72,370,343）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書12件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes | bytes |
|---|---:|---:|---:|---:|
| 7 | 58 | 46,522 | 7,782,348 | 1,681,877 |
| 12 | 59 | 48,522 | 5,432,671 | 1,753,793 |
| 39 | 54 | 37,357 | 4,272,617 | 1,347,439 |
| 58 | 60 | 54,403 | 8,793,907 | 1,963,212 |
| 62 | 50 | 28,137 | 4,446,004 | 1,013,765 |
| 64 | 53 | 33,729 | 5,294,013 | 1,220,093 |
| 66 | 60 | 55,866 | 15,367,865 | 2,015,227 |
| 78 | 66 | 75,290 | 24,986,145 | 2,719,747 |
| 94 | 64 | 50,607 | 10,274,932 | 1,826,619 |
| 96 | 55 | 35,532 | 8,372,197 | 1,282,169 |
| 108 | 63 | 56,913 | 18,851,852 | 2,051,023 |
| 111 | 61 | 58,783 | 10,272,392 | 2,117,156 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**581,661行・20,992,120 bytes・124,146,943 extraction nodes・703 sub-roots**。bit58/66/78/108/111は行境界2分割、他7件は単一ファイル。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**12/12 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1290 → 1299）

`recompute_frontier_cost77d_receipts_20261115.py` はcost-77c fold scriptをrunpyで再実行してhead 1290/6557/517923/4827/381646をbyte-identicalに再現し、公開順 [7,12,39,58,62,64,66,78,94,96,108,111] で12 receiptをfoldした。

- 新canonical head: **`1299/6548/517249/4818/380972`**（solved 1290→1299、in-manifest marginal 9、raw marginal 58、zero-mim bits 39/58/64/108）。
- child `00000000100000801202000000200000` は**bit7**で閉鎖。
- **第二target S5: 13行/1018 → 11行/866**（child + `00000000000040801202000000200000` の2行喪失）。
- 第2開親 `00000000000000003800400008000000`: 66行/5192 → 58行/4593（child+7親orbit喪失）。
- set等式 `s_after == s_1290 ∪ covers(12 roots)`、565 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `d19c96b7…`・13,128 B）、ranking CSV（`a69f5e7a…`・7,538 B）、top-candidates CSV（`49b7f378…`・7,416 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り11行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- cost-75d（第二targetのcost-75行）は4証明書公開済みでfold待ち。
- 第二targetの次の未sweep行（cost-79 `00000000000000801212000000200000`・cost-80 `00000008000000809002000000000400` など）とclass-4 blocker S5の残行が候補。
- 以後のfoldは新head 1299へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77d_receipts_20261115.py
```

cost-77c baselineを再実行し、head 1290のbyte-identical再現から12 receiptsをfoldする。実行時間は約1〜2分。
