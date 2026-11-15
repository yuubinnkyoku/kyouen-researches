# 2026-11-15：cost-75d + cost-77d のwarm-hygiene merge — canonical head 1302（77d childは75d bit92が既閉鎖）

開始時main: `c69a23aa7`。cost-77d laneのlane-local fold（1290→1299）実行中に、並走のcost-75d foldがhead **1296/6551/517468/4821/381191** で着地していた。75dのbit92 receiptが77d child `00000000100000801202000000200000` を**cross-coverで既に閉鎖**しているため、77d foldを1296 baselineへrebaseし、warm-hygiene統制（child closureを二重計上しない）を適用した。

## warm-hygieneの内容

- 1296 baselineで77d childは**solved済み**（`CHILD_V in s_base`）で、両開親のremaining rowsに不在（第二target 11行/866、第2開親64行/5036）。
- 77dの12 WIN rootsのうち**bit78 root `00000000100040801202000000200000` は75d bit92 rootと完全一致**（cross-lane root collision）。この1件はfoldから除外（既にfold済み）。
- 残り11 receiptsを公開順 [7,12,39,58,62,64,66,94,96,108,111] でfoldし、child closureは**主張しない**。

## 結果

- 新canonical head: **`1302/6545/517025/4815/380748`**（solved 1296→1302、in-manifest marginal 6、raw marginal 51、zero-mim bits 7/39/58/64/108）。
- 第二target S5: 11行/866（不変 — 77d receiptsのmarginalは第二targetに追加なし）。
- 第2開親 `00000000000000003800400008000000`: **64行/5036 → 58行/4593**（6行喪失）。
- best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 出力: head JSON（blob `97130384…`・12,460 B）、ranking CSV（`aba88980…`・7,538 B）、top-candidates CSV（`49b7f378…`・7,416 B）。

## 信頼境界

- warm-hygiene mergeは公開receiptの帳簿更新であり、いかなる局面の勝敗判定でもない。child closureの帰属は75d bit92にあり、77d foldはそれを再主張しない。
- 77dのlane-local fold（1290→1299）は履歴として残るが、canonical chainは1302。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 次の一手

- 第二target S5の次の未sweep行（cost-79 `00000000000000801212000000200000`・cost-80 `00000008000000809002000000000400` など）とclass-4 blocker S5の残行。
- 以後のfoldはhead 1302へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost75d_77d_20261115.py
```
